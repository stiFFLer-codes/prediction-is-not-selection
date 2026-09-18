"""Phase 2.2c probe: is a candidate mechanism pair two-sided on the calibration split?

Design-and-propose pass only. This file runs on the **calibration blocks alone**
(the 15% held out by PREREG section 3 for exactly this kind of choice) and
produces no evaluation-split number, no hypothesis verdict, and no accuracy that
any paper claim rests on. It amends nothing.

The 2.2b finding it exists to answer: exact match is a strict sub-case of the
frozen fuzzy arm, so `exact wins` is unreachable and the dissociation cannot be
tested on that pair. The structural reason is narrow and worth stating, because
it rules out most repairs: the test signature's own surface form, when it occurs
in the train history, sits at similarity exactly 1.0, the maximum of any
similarity. **Any single-nearest-form retriever therefore selects that same form
and resolves the same author, so every 1-NN retriever contains exact match.**
Changing the metric, the cutoff or the tie-break does not touch this.

A pair can only be two-sided if mechanism B either aggregates over a
neighbourhood instead of taking the single nearest form, or matches on a
representation under which the exact form loses its privileged status. All three
candidates below do one of those.

Mechanism A, fixed across all three pairs
    `rule` - the precision-first exact-evidence rule. Unchanged from PREREG
    section 4 exact match: if the test surface form occurs among the train
    surface forms, assign the most frequent author carrying that exact form,
    with the frozen tie-break; otherwise abstain. It reads only evidence that
    names the test form itself, and never merges across forms.

Mechanism B, one per candidate pair
    `radius` (P1) - coverage-first radius vote. Pool every train signature whose
        form is within similarity r of the test form, assign the most frequent
        author in the pool. One parameter, r.
    `mergekey` (P2) - coverage-first normalized-key vote. Pool every train
        signature whose form carries the same ASCII-folded, letters-only key as
        the test form, assign the most frequent author in the pool. No parameter.
    `knn` (P3) - coverage-first k-nearest vote. Pool the nearest train
        signatures by form similarity until at least k are pooled, whole forms at
        a time, assign the most frequent author in the pool. One parameter, k.

`nn1` is also scored, the frozen 2.2b fuzzy arm, as a probe self-check: it must
report zero signatures where the rule is right and it is wrong, reproducing the
2.2b nesting on this split. If it does not, the probe is broken, not the finding.

Run: python phase2/phase2c_probe.py
"""

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from rapidfuzz import process as rf_process
from rapidfuzz.distance import Levenshtein
from unidecode import unidecode

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_constants import FUZZY_CUTOFF, SV_BAND_EDGES  # noqa: E402
from phase2b_core import TABLE, ads, ads_band, assign_splits, sv_band  # noqa: E402
from s2and_blocking import NON_LETTER, surface_variability  # noqa: E402

REPORT = HERE / "reports" / "phase2c_pair_probe.md"
TABLES = HERE / "reports" / "tables"

RADII = (0.70, 0.80, 0.85, 0.90, 0.95)
KS = (2, 3, 5, 10)
NN1_CUTOFF = FUZZY_CUTOFF["levenshtein"]


def merge_key(form):
    """P2's normalization-invariant key: ASCII-fold, lowercase, letters only.

    Case, diacritics, punctuation, hyphenation and internal spacing collapse.
    Forename fullness does **not**: "J. Smith" -> "jsmith" and "John Smith" ->
    "johnsmith" stay distinct keys. That separation is deliberate. Forename
    initialization is Kim and Kim (2020)'s manipulated variable, so a mechanism
    that merges across it would make our contribution a restatement of theirs;
    what this key merges is precisely the non-initialization synonymy their paper
    names as out of scope.
    """
    return NON_LETTER.sub("", unidecode(form or "").lower())


def block_predictions(train_forms, train_labels, test_forms):
    """Every mechanism's prediction for one block's test signatures.

    Returns a dict name -> list of author ids, with None for an abstention.

    Author order is fixed once per block by (descending block count, then author
    id), and form order by (descending signature count, then form), so `argmax`,
    which takes the first maximum, *is* the frozen PREREG section 4 tie-break:
    most frequent inside the matched evidence, then most frequent in the block,
    then the lexicographically smallest id.
    """
    block_counts = Counter(train_labels)
    authors = sorted(block_counts, key=lambda a: (-block_counts[a], a))
    aidx = {a: i for i, a in enumerate(authors)}
    form_counts = Counter(train_forms)
    forms = sorted(form_counts, key=lambda f: (-form_counts[f], f))
    fidx = {f: i for i, f in enumerate(forms)}

    # M[form, author] = how many train signatures carry that form and author.
    M = np.zeros((len(forms), len(authors)), dtype=np.float64)
    for f, l in zip(train_forms, train_labels):
        M[fidx[f], aidx[l]] += 1.0

    distinct_test = sorted(set(test_forms))
    sims = rf_process.cdist(distinct_test, forms,
                            scorer=Levenshtein.normalized_similarity, dtype=np.float32)

    def vote(mask):
        """Modal author of the pooled mask, or None where the pool is empty."""
        pooled = mask.astype(np.float64) @ M
        hit = pooled.sum(axis=1) > 0
        pick = pooled.argmax(axis=1)
        return [authors[pick[i]] if hit[i] else None for i in range(len(distinct_test))]

    per_form = {}

    # A: the exact-evidence rule. Evidence is the one matched form.
    exact_mask = np.zeros_like(sims, dtype=bool)
    for i, f in enumerate(distinct_test):
        if f in fidx:
            exact_mask[i, fidx[f]] = True
    per_form["rule"] = vote(exact_mask)

    # Probe self-check: the frozen 2.2b fuzzy arm, single nearest form.
    nn_mask = np.zeros_like(sims, dtype=bool)
    arg = sims.argmax(axis=1)
    fires = sims[np.arange(len(distinct_test)), arg] >= NN1_CUTOFF
    nn_mask[np.arange(len(distinct_test))[fires], arg[fires]] = True
    per_form["nn1"] = vote(nn_mask)

    # P1: radius vote.
    for r in RADII:
        per_form[f"radius@{r:.2f}"] = vote(sims >= r)

    # P2: normalized-key vote.
    key_of_form = np.array([merge_key(f) for f in forms])
    key_mask = np.stack([key_of_form == merge_key(f) for f in distinct_test])
    per_form["mergekey"] = vote(key_mask)

    # P3: k-nearest vote, whole forms at a time until k signatures are pooled.
    counts_in_form_order = np.array([form_counts[f] for f in forms])
    order = np.argsort(-sims, axis=1, kind="stable")   # forms already tie-broken
    cum = np.cumsum(counts_in_form_order[order], axis=1)
    for k in KS:
        take = np.argmax(cum >= k, axis=1)
        take = np.where(cum[:, -1] >= k, take, cum.shape[1] - 1)   # fewer than k: take all
        knn_mask = np.zeros_like(sims, dtype=bool)
        for i in range(len(distinct_test)):
            knn_mask[i, order[i, :take[i] + 1]] = True
        per_form[f"knn@{k}"] = vote(knn_mask)

    pos = {f: i for i, f in enumerate(distinct_test)}
    return {name: [preds[pos[f]] for f in test_forms] for name, preds in per_form.items()}


def main():
    cols = ["sid", "dataset", "block_key", "author_label", "surface_form"]
    sig = pd.read_parquet(TABLE, columns=cols)
    for c in ("surface_form", "author_label"):
        sig[c] = sig[c].astype(object).where(sig[c].notna(), "")
    sig = assign_splits(sig)

    cal = sig[sig.is_live & sig.is_cal]
    print(f"calibration blocks in scope: {cal.groupby(['dataset', 'block_key']).ngroups:,}")

    rows, names = [], None
    for (dataset, block_key), grp in cal.groupby(["dataset", "block_key"], sort=True):
        tr = grp[grp.is_train]
        te = grp[~grp.is_train]
        if len(tr) < 2 or len(te) < 1:          # PREREG section 3 primary population
            continue
        preds = block_predictions(tr.surface_form.tolist(), tr.author_label.tolist(),
                                  te.surface_form.tolist())
        names = names or list(preds)
        truth = te.author_label.tolist()
        rows.append({
            "dataset": dataset,
            "block_key": block_key,
            "n_test": len(truth),
            "ads_band": ads_band(ads(tr.author_label.values)),
            "sv_band": sv_band(surface_variability(Counter(tr.surface_form.tolist())), *SV_BAND_EDGES),
            **{f"ok__{name}": np.array([p is not None and p == t for p, t in zip(pred, truth)])
               for name, pred in preds.items()},
            **{f"fire__{name}": np.array([p is not None for p in pred])
               for name, pred in preds.items()},
        })

    blocks = pd.DataFrame(rows)
    print(f"primary-population calibration blocks: {len(blocks):,}  "
          f"test signatures: {blocks.n_test.sum():,}")

    sig_level = pd.DataFrame({
        "ads_band": np.repeat(blocks.ads_band.values, blocks.n_test.values),
        "sv_band": np.repeat(blocks.sv_band.values, blocks.n_test.values),
        **{c: np.concatenate(blocks[c].values) for c in blocks.columns if c.startswith(("ok__", "fire__"))},
    })

    a = sig_level["ok__rule"].values
    summary = []
    for name in names:
        if name == "rule":
            continue
        b = sig_level[f"ok__{name}"].values
        summary.append({
            "pair": f"rule vs {name}",
            "A right, B wrong": int((a & ~b).sum()),
            "B right, A wrong": int((b & ~a).sum()),
            "both right": int((a & b).sum()),
            "both wrong": int((~a & ~b).sum()),
            "acc A": round(a.mean(), 4),
            "acc B": round(b.mean(), 4),
            "cov B": round(sig_level[f"fire__{name}"].values.mean(), 4),
        })
    summary = pd.DataFrame(summary)
    print("\n" + summary.to_string(index=False))

    # Regime breakdown for the recommended pairs, the thing the paper needs.
    regime = []
    for name in names:
        if name == "rule":
            continue
        b = sig_level[f"ok__{name}"].values
        for (ab, sb), idx in sig_level.groupby(["ads_band", "sv_band"], sort=False).groups.items():
            i = sig_level.index.get_indexer(idx)
            regime.append({"pair": f"rule vs {name}", "ads_band": ab, "sv_band": sb,
                           "n_test": len(i),
                           "A right, B wrong": int((a[i] & ~b[i]).sum()),
                           "B right, A wrong": int((b[i] & ~a[i]).sum()),
                           "gap A-B": round(a[i].mean() - b[i].mean(), 4)})
    regime = pd.DataFrame(regime)

    TABLES.mkdir(parents=True, exist_ok=True)
    summary.to_csv(TABLES / "phase2c_pair_twosidedness.csv", index=False)
    regime.to_csv(TABLES / "phase2c_pair_regimes.csv", index=False)
    print(f"\nwrote {TABLES / 'phase2c_pair_twosidedness.csv'}")
    print(f"wrote {TABLES / 'phase2c_pair_regimes.csv'}")

    assert summary.loc[summary.pair == "rule vs nn1", "A right, B wrong"].iloc[0] == 0, \
        "probe self-check failed: the 1-NN arm must reproduce the 2.2b nesting"
    print("\nprobe self-check: 1-NN reproduces the 2.2b nesting (0 rule-right/1-NN-wrong)")


def demo():
    """Self-check on hand-built blocks. Fails loudly if a mechanism drifts."""
    assert merge_key("Gell-Mann") == merge_key("Gellmann") == "gellmann"
    assert merge_key("Jürgen Müller") == "jurgenmuller"
    assert merge_key("J. Smith") == "jsmith" != merge_key("John Smith"), \
        "forename fullness must NOT collapse: that is Kim and Kim's axis"

    # Over-merging is the whole point of B, so it must be demonstrable.
    # History: "Wei Wang" is author A once; "W. Wang" is author B three times.
    tf = ["Wei Wang", "W. Wang", "W. Wang", "W. Wang"]
    tl = ["A", "B", "B", "B"]
    p = block_predictions(tf, tl, ["Wei Wang"])
    assert p["rule"] == ["A"], p["rule"]                 # precision: uses only its own form
    assert p["nn1"] == ["A"], p["nn1"]                   # nested: 1-NN finds the same form
    assert p["radius@0.70"] == ["B"], p["radius@0.70"]   # over-merges into the block majority
    assert p["knn@3"] == ["B"], p["knn@3"]               # pools past its own form
    assert p["mergekey"] == ["A"], p["mergekey"]         # different key, no merge

    # ... and the merge key must merge where punctuation alone differs.
    p2 = block_predictions(["W Wang", "W. Wang", "W. Wang"], ["A", "B", "B"], ["W Wang"])
    assert p2["rule"] == ["A"] and p2["mergekey"] == ["B"], p2

    # Coverage the other way: an unseen form. The rule abstains, B fires.
    p3 = block_predictions(["Wei Wang", "Wei Wang"], ["A", "A"], ["Wei Wamg"])
    assert p3["rule"] == [None] and p3["radius@0.70"] == ["A"] and p3["knn@2"] == ["A"], p3

    print("phase2c_probe self-check: all assertions passed")


if __name__ == "__main__":
    demo()
    main()
