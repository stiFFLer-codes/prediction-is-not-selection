"""Phase 2.2e mechanisms: the exact-evidence rule (A) and the k-nearest vote (B).

Implements `phase2/PREREG.md` section 4 as amended by **Amendment 1** (Phase
2.2d) and its resolutions 1 and 2. Nothing here is tunable and nothing here is
calibrated: k is fixed by definition, not by maximizing accuracy.

Mechanism A, the exact-evidence rule (unchanged from the original section 4).
    If the test surface form occurs among the train surface forms, assign the
    most frequent author among train signatures carrying that exact form;
    otherwise abstain.

Mechanism B, the k-nearest vote (Amendment 1, sections 4 and 7).
    Pool the nearest training signatures by similarity of their surface form to
    the test form, **whole forms at a time**, until the pool holds at least k
    training signatures; if the block holds fewer than k training signatures the
    pool is the whole block. Vote the pooled signatures' authors,
    signature-weighted. B never abstains.

    Resolution 1: "k nearest" counts **signatures**, not forms.
    Resolution 2: both mechanisms use the frozen section 4 tie-break chain,
    most frequent author inside the pooled evidence, then most frequent author
    inside the block, then the lexicographically smallest author id.

This module is written independently of `phase2c_probe.py`, which produced the
2.2c calibration-split design diagnostics, precisely so that the regression
check below is a real check rather than a restatement. `main()` reruns the
2.2c two-sidedness counts on the calibration split and **asserts** them.

Run: python phase2/phase2e_mech.py
    demo()  - assert-based self-check on hand-built blocks
    main()  - the 2.2c calibration-split regression check
"""

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from rapidfuzz import process as rf_process
from rapidfuzz.distance import JaroWinkler, Levenshtein

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_core import TABLE, assign_splits  # noqa: E402

# PREREG Amendment 1: k is fixed by definition at 5; the curve is mandatory.
K_PRIMARY = 5
KS = (2, 3, 5, 10)
ARMS = {
    "levenshtein": Levenshtein.normalized_similarity,
    "jarowinkler": JaroWinkler.normalized_similarity,
}

# The frozen 2.2c calibration-split counts this module must reproduce, from
# `reports/tables/phase2c_pair_twosidedness.csv` at commit c20239a.
# k -> (A right and B wrong, B right and A wrong)
PHASE2C_TWOSIDEDNESS = {2: (181, 736), 3: (314, 740), 5: (546, 744), 10: (912, 748)}
PHASE2C_ACC = {"rule": 0.8234, 2: 0.8390, 3: 0.8354, 5: 0.8290, 10: 0.8188}


def block_predictions(train_forms, train_labels, test_forms,
                      ks=KS, simfunc=Levenshtein.normalized_similarity):
    """Both mechanisms' predictions for one block's test signatures.

    Returns {"rule": [...], k: [...] for each k in ks}, author ids with None
    marking an abstention. Only mechanism A can abstain.

    Author order is fixed once per block by (descending block count, then author
    id) and form order by (descending signature count, then form), so `argmax`,
    which returns the first maximum, *is* the frozen section 4 tie-break chain.
    """
    block_counts = Counter(train_labels)
    authors = sorted(block_counts, key=lambda a: (-block_counts[a], a))
    aidx = {a: i for i, a in enumerate(authors)}
    form_counts = Counter(train_forms)
    forms = sorted(form_counts, key=lambda f: (-form_counts[f], f))
    fidx = {f: i for i, f in enumerate(forms)}

    # M[form, author] = train signatures carrying that form and that author.
    M = np.zeros((len(forms), len(authors)), dtype=np.float64)
    for f, lab in zip(train_forms, train_labels):
        M[fidx[f], aidx[lab]] += 1.0
    per_form_n = M.sum(axis=1)

    distinct = sorted(set(test_forms))
    sims = rf_process.cdist(distinct, forms, scorer=simfunc, dtype=np.float32)

    per_form = {"rule": {}}
    per_form.update({k: {} for k in ks})
    for i, f in enumerate(distinct):
        # A: evidence is the one matched form, or nothing at all.
        per_form["rule"][f] = authors[int(M[fidx[f]].argmax())] if f in fidx else None
        # B: forms nearest first; the stable sort keeps the frozen form tie-break.
        order = np.argsort(-sims[i], kind="stable")
        cum = np.cumsum(per_form_n[order])
        for k in ks:
            # first form index at which the pool holds at least k signatures;
            # past the end when the block has fewer than k, so the slice takes all.
            take = int(np.searchsorted(cum, k, side="left")) + 1
            pooled = M[order[:take]].sum(axis=0)
            per_form[k][f] = authors[int(pooled.argmax())]
    return {name: [preds[f] for f in test_forms] for name, preds in per_form.items()}


# --------------------------------------------------------------------------
# the 2.2c regression check
# --------------------------------------------------------------------------

def calibration_counts(ks=KS, verbose=True):
    """Rerun the 2.2c two-sidedness counts on the calibration split.

    Calibration blocks only, PREREG section 3 primary-population rule applied,
    exactly as `phase2c_probe.py` did. Produces no evaluation-split number.
    """
    cols = ["sid", "dataset", "block_key", "author_label", "surface_form"]
    sig = pd.read_parquet(TABLE, columns=cols)
    for c in ("surface_form", "author_label"):
        sig[c] = sig[c].astype(object).where(sig[c].notna(), "")
    sig = assign_splits(sig, verbose=verbose)

    cal = sig[sig.is_live & sig.is_cal]
    a_ok, b_ok, n_blocks = [], {k: [] for k in ks}, 0
    for _, grp in cal.groupby(["dataset", "block_key"], sort=True):
        tr = grp[grp.is_train]
        te = grp[~grp.is_train]
        if len(tr) < 2 or len(te) < 1:
            continue
        n_blocks += 1
        truth = te.author_label.tolist()
        preds = block_predictions(tr.surface_form.tolist(), tr.author_label.tolist(),
                                  te.surface_form.tolist(), ks=ks)
        a_ok.append([p is not None and p == t for p, t in zip(preds["rule"], truth)])
        for k in ks:
            b_ok[k].append([p == t for p, t in zip(preds[k], truth)])

    a = np.concatenate([np.asarray(x, dtype=bool) for x in a_ok])
    rows = []
    for k in ks:
        b = np.concatenate([np.asarray(x, dtype=bool) for x in b_ok[k]])
        rows.append({"k": k,
                     "A_right_B_wrong": int((a & ~b).sum()),
                     "B_right_A_wrong": int((b & ~a).sum()),
                     "both_right": int((a & b).sum()),
                     "both_wrong": int((~a & ~b).sum()),
                     "acc_A": round(float(a.mean()), 4),
                     "acc_B": round(float(b.mean()), 4)})
    return pd.DataFrame(rows), n_blocks, len(a)


def main():
    print("Phase 2.2e regression check: mechanism B against the frozen 2.2c counts.")
    tab, n_blocks, n_sigs = calibration_counts()
    print("calibration primary-population blocks: {:,}   test signatures: {:,}"
          .format(n_blocks, n_sigs))
    print("\n" + tab.to_string(index=False) + "\n")

    failures = []
    for r in tab.itertuples(index=False):
        want = PHASE2C_TWOSIDEDNESS[r.k]
        got = (r.A_right_B_wrong, r.B_right_A_wrong)
        if got != want:
            failures.append("k={}: two-sidedness {} != frozen 2.2c {}".format(r.k, got, want))
        if abs(r.acc_B - PHASE2C_ACC[r.k]) > 5e-5:
            failures.append("k={}: acc B {} != frozen 2.2c {}".format(r.k, r.acc_B, PHASE2C_ACC[r.k]))
    if abs(tab.acc_A.iloc[0] - PHASE2C_ACC["rule"]) > 5e-5:
        failures.append("acc A {} != frozen 2.2c {}".format(tab.acc_A.iloc[0], PHASE2C_ACC["rule"]))
    if len(set(tab.acc_A)) != 1:
        failures.append("mechanism A must not depend on k")
    assert not failures, "REGRESSION CHECK FAILED:\n  " + "\n  ".join(failures)

    print("regression check passed: k=5 reproduces 546 rule wins against 744, and the whole "
          "k curve and both accuracies match reports/tables/phase2c_pair_twosidedness.csv.")
    return tab


def demo():
    """Self-check on hand-built blocks. Fails loudly if a frozen definition drifts."""
    # --- the pair must be two-sided in both directions, by construction -----
    # A right, B wrong: the test form's own evidence names A, the neighbourhood
    # is dominated by B.  History: "Wei Wang"->A once, "W. Wang"->B three times.
    p = block_predictions(["Wei Wang", "W. Wang", "W. Wang", "W. Wang"],
                          ["A", "B", "B", "B"], ["Wei Wang"], ks=(3, 5))
    assert p["rule"] == ["A"], p["rule"]
    assert p[3] == ["B"] and p[5] == ["B"], p
    # B right, A wrong: an unseen form. A abstains, B still answers.
    p = block_predictions(["Wei Wang", "Wei Wang"], ["A", "A"], ["Wei Wamg"], ks=(2,))
    assert p["rule"] == [None] and p[2] == ["A"], p

    # --- resolution 1: k counts SIGNATURES, not forms -----------------------
    # Nearest form "aa" carries 4 signatures of author A; "ab" carries 1 of B.
    # Signature-counted k=2 stops at the first form.  A form-counted reading
    # would always pool two forms; these cases pin the adopted reading.
    p = block_predictions(["aa"] * 4 + ["ab"], ["A"] * 4 + ["B"], ["aa"], ks=(2, 5))
    assert p[2] == ["A"] and p[5] == ["A"], p
    # make the second form dominant: k=2 still stops inside the first form,
    # k=5 must reach past it and flip. That is the pool growing by signatures.
    p2 = block_predictions(["aa"] * 4 + ["ab"] * 9, ["A"] * 4 + ["B"] * 9, ["aa"], ks=(2, 5))
    assert p2[2] == ["A"] and p2[5] == ["B"], p2

    # --- resolution 2: the frozen section 4 tie-break chain, for BOTH --------
    # inside the pooled evidence, most frequent author wins
    p = block_predictions(["ab", "ab", "ab"], ["A", "B", "B"], ["ab"], ks=(2,))
    assert p["rule"] == ["B"] and p[2] == ["B"], p
    # equal counts inside the evidence -> most frequent inside the BLOCK
    p = block_predictions(["ab", "ab", "cd", "cd", "cd"], ["A", "B", "B", "B", "B"],
                          ["ab"], ks=(2,))
    assert p["rule"] == ["B"], p["rule"]
    # equal inside the evidence and equal inside the block -> smallest author id
    p = block_predictions(["ab", "ab"], ["B", "A"], ["ab"], ks=(2,))
    assert p["rule"] == ["A"] and p[2] == ["A"], p
    # B is NOT broken toward the nearest form: an exact-similarity tie between
    # two forms is resolved by the frozen form order (more signatures first).
    p = block_predictions(["xy", "xy", "zw"], ["A", "A", "B"], ["qq"], ks=(1,))
    assert p[1] == ["A"], p[1]

    # --- B never abstains, A does -------------------------------------------
    p = block_predictions(["aa", "bb"], ["A", "B"], ["zz"], ks=(2, 5, 10))
    assert p["rule"] == [None], p["rule"]
    assert all(p[k] == ["A"] for k in (2, 5, 10)), p   # fewer than k: whole block

    # --- k = 1 is the nesting limit, which is why it is off the curve -------
    # at k=1 only the nearest form is pooled, so B agrees with A wherever A fires
    tf = ["Wei Wang", "W. Wang", "W. Wang", "W. Wang"]
    tl = ["A", "B", "B", "B"]
    p = block_predictions(tf, tl, ["Wei Wang"], ks=(1,))
    assert p["rule"] == p[1] == ["A"], p

    # --- the metric arm is a parameter, not a redefinition ------------------
    pj = block_predictions(tf, tl, ["Wei Wang"], ks=(5,),
                           simfunc=JaroWinkler.normalized_similarity)
    assert pj["rule"] == ["A"] and pj[5] == ["B"], pj

    # --- multiple test signatures come back in input order, duplicates included
    p = block_predictions(["aa", "aa", "bb"], ["A", "A", "B"], ["bb", "aa", "bb"], ks=(2,))
    assert p["rule"] == ["B", "A", "B"], p["rule"]

    assert Levenshtein.normalized_similarity("aa", "aa") == 1.0
    print("phase2e_mech self-check: all assertions passed")


if __name__ == "__main__":
    demo()
    main()
