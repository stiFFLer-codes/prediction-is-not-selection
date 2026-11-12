"""Phase 2.9a: release-pass facts, and the like-for-like precision comparison.

A supplementary analysis on records that already exist, in the conventions of
`phase2_7b_reanalysis.py`. Nothing is re-run, re-tuned, re-banded or redefined:
the per-signature scores are `data/phase2e_eval_sigs.parquet` (rebuilt by the
frozen `phase2e_run.mechanism_pass` if absent), the per-block records are
`reports/tables/phase2e_blocks_scored.csv.gz`, the bootstrap is the frozen
`phase2b_core.pooled_block_ci` at the frozen `band_seed` scheme, B = 2000.

Before anything is computed the script re-derives the frozen primary population
(13,902 blocks, 197,479 test signatures, rule 0.824442, k-NN 0.829440) and halts
if any of the four differs, then checks every per-block count it aggregates
against the committed per-block record.

Outputs (reports/tables/):
1. phase2_9a_matched_precision.csv  The rule's precision where it fires against
   the k-nearest vote's accuracy **on the same fired items**, with a 95% block
   bootstrap interval for the matched difference. Pooled, the seven block-size
   octave bands of `phase2_7b_reanalysis`, and each dataset.
2. phase2_9a_region_counts.csv  Per SV band, per ADS band and for the
   ADS = 1.0 x SV = 0 cell: rule right and vote wrong, vote right and rule
   wrong (and how many of those are rule abstentions), and test signatures whose
   surface form is absent from the block's training half.
3. phase2_9a_contested_share.csv  The evaluation-split share of held-out
   signatures in blocks with ADS < 1 and SV > 0.
It also counts, over every primary block, pairs of distinct surface forms that
score the maximum 1.0 under either metric arm, as the mechanisms compute it.

Run: python phase2/phase2_9a_matched.py
"""

import platform
import sys
from importlib import metadata
from pathlib import Path

import numpy as np
import pandas as pd
from rapidfuzz import process as rf_process

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_core import (  # noqa: E402
    ADS_BANDS, BLOCKS_CACHE, BOOTSTRAP_B, SV_BAND_NAMES, band_seed, pooled_block_ci,
)
from phase2b_build import load_signatures  # noqa: E402
from phase2b_run import TABLES, dump  # noqa: E402
from phase2e_mech import ARMS  # noqa: E402
from phase2e_run import PRIMARY, mechanism_pass  # noqa: E402
from phase2_7b_reanalysis import BLOCKS, BSIZE_ORDER, bsize_band  # noqa: E402

FROZEN = {"blocks": 13902, "n_test": 197479, "rule_acc": 0.824442, "knn_acc": 0.829440}
PACKAGES = ("numpy", "pandas", "scipy", "pyarrow", "rapidfuzz", "unidecode", "matplotlib")
OK = "ok_" + PRIMARY


def halt(msg):
    sys.exit("HALT, not the frozen primary population: " + msg)


def load():
    """Per-block aggregates from the per-signature scores, checked against the record."""
    bk = pd.read_csv(BLOCKS)
    bk["bsize_band"] = [bsize_band(n) for n in bk.block_size]
    sig = load_signatures()
    blocks = pd.read_parquet(BLOCKS_CACHE)
    res = mechanism_pass(sig, blocks[~blocks.is_cal])  # reuses the cache, rebuilds it if absent
    res = res.assign(knn_ok_fired=res.rule_fires & res[OK],
                     plus=res.rule_ok & ~res[OK],
                     minus=~res.rule_ok & res[OK],
                     minus_abst=~res.rule_fires & res[OK])
    per = res.groupby(["dataset", "block_key"], sort=True).agg(
        n=("rule_ok", "size"), rule_ok=("rule_ok", "sum"), fired=("rule_fires", "sum"),
        knn_ok=(OK, "sum"), knn_ok_fired=("knn_ok_fired", "sum"), plus=("plus", "sum"),
        minus=("minus", "sum"), minus_abst=("minus_abst", "sum")).reset_index()
    b = bk.merge(per, on=["dataset", "block_key"], how="left", validate="one_to_one")

    n = int(b.n.sum())
    got = {"blocks": len(b), "n_test": n,
           "rule_acc": round(b.rule_ok.sum() / n, 6), "knn_acc": round(b.knn_ok.sum() / n, 6)}
    for key, want in FROZEN.items():
        if got[key] != want:
            halt("{} = {} against frozen {}".format(key, got[key], want))
    print("frozen primary population reproduced: {:,} blocks, {:,} test signatures, "
          "rule {:.6f}, k-NN {:.6f}".format(got["blocks"], n, got["rule_acc"], got["knn_acc"]))

    for mine, rec in (("n", "n_test"), ("rule_ok", "rule_correct"), ("fired", "rule_fires_n"),
                      ("knn_ok", "knn_correct_" + PRIMARY), ("plus", "n_plus_" + PRIMARY),
                      ("minus", "n_minus_" + PRIMARY)):
        if not (b[mine] == b[rec]).all():
            halt("per-block {} disagrees with the committed {}".format(mine, rec))
    print("every per-block count agrees with reports/tables/phase2e_blocks_scored.csv.gz")
    return b, sig


def matched_row(label, g):
    n, fired = int(g.n.sum()), int(g.fired.sum())
    prec, knn_f = g.rule_ok.sum() / fired, g.knn_ok_fired.sum() / fired
    # matched difference = sum(rule right - vote right) / sum(fired), over fired items only,
    # which is exactly the frozen pooled ratio bootstrap with `fired` as the block size.
    pt, lo, hi = pooled_block_ci((g.rule_ok - g.knn_ok_fired).values, g.fired.values,
                                 seed=band_seed("p29a|matched|" + label))
    assert abs(pt - (prec - knn_f)) < 1e-12, (label, pt, prec - knn_f)
    return {"population": label, "blocks": len(g), "test_signatures": n,
            "rule_fired": fired, "rule_coverage": fired / n,
            "rule_precision_fired": prec, "knn_acc_all": g.knn_ok.sum() / n,
            "knn_acc_fired": knn_f, "matched_diff": pt,
            "matched_ci_lo": lo, "matched_ci_hi": hi, "B": BOOTSTRAP_B}


def matched_precision(b):
    pops = [("pooled", b)]
    pops += [(band, b[b.bsize_band == band]) for band in BSIZE_ORDER]
    pops += [(d, b[b.dataset == d]) for d in sorted(b.dataset.unique())]
    return pd.DataFrame([matched_row(lbl, g) for lbl, g in pops])


def region_counts(b):
    def row(axis, band, g):
        return {"axis": axis, "band": band, "blocks": len(g), "test_signatures": int(g.n.sum()),
                "rule_right_vote_wrong": int(g.plus.sum()),
                "vote_right_rule_wrong": int(g.minus.sum()),
                "vote_right_rule_abstained": int(g.minus_abst.sum()),
                "form_absent_from_train": int((g.n - g.fired).sum())}
    rows = [row("SV band", s, b[b.sv_band == s]) for s in SV_BAND_NAMES]
    rows += [row("ADS band", a, b[b.ads_band == a]) for a in ADS_BANDS]
    rows.append(row("cell", "ADS=1.0 x SV=0", b[(b.ads_band == "1.0") & (b.sv_band == "SV=0")]))
    t = pd.DataFrame(rows)
    # the two structural regions, checked on the data rather than asserted in prose:
    # the rule never beats the vote there, and every item the vote wins is a rule abstention.
    for band in ("SV=0", "1.0", "ADS=1.0 x SV=0"):
        r = t[t.band == band].iloc[0]
        assert r.rule_right_vote_wrong == 0, r
        assert r.vote_right_rule_wrong == r.vote_right_rule_abstained, r
    for axis in ("SV band", "ADS band"):
        s = t[t.axis == axis]
        assert s.blocks.sum() == len(b) and s.test_signatures.sum() == FROZEN["n_test"], axis
    return t


def contested_share(b):
    m = (b.ads_band != "1.0") & (b.sv_band != "SV=0")
    assert (m == ((b.ads < 1.0) & (b.sv > 0))).all(), "band labels and raw values disagree"
    cells = pd.read_csv(TABLES / "phase2e_pooled_cells_sv.csv")
    from_cells = int(cells[(cells.ads_band != "1.0") & (cells.sv_band != "SV=0")].n_test.sum())
    n = int(b[m].n.sum())
    assert n == from_cells, (n, from_cells)
    return pd.DataFrame([{"split": "evaluation", "definition": "ADS < 1 and SV > 0",
                          "blocks": int(m.sum()), "of_blocks": len(b),
                          "test_signatures": n, "of_test_signatures": int(b.n.sum()),
                          "share": n / b.n.sum()}])


def max_score_collisions(sig, b):
    """Pairs of distinct surface forms in one primary block scoring 1.0, per arm.

    Every distinct form of the block, train and test, scored as the mechanisms
    score them: `rapidfuzz.process.cdist`, float32, no processor. Also returns, per
    block, whether the training half carries a single distinct form.
    """
    live = sig[sig.is_live & ~sig.is_cal]
    prim = set(zip(b.dataset, b.block_key))
    hits, pairs, one_form = {arm: 0 for arm in ARMS}, 0, {}
    for key, grp in live.groupby(["dataset", "block_key"], sort=True):
        if key not in prim:
            continue
        one_form[key] = grp.surface_form[grp.is_train].nunique() == 1
        forms = sorted(set(grp.surface_form))
        if len(forms) < 2:
            continue
        pairs += len(forms) * (len(forms) - 1) // 2
        for arm, func in ARMS.items():
            s = rf_process.cdist(forms, forms, scorer=func, dtype=np.float32)
            np.fill_diagonal(s, 0.0)
            hits[arm] += int((s >= 1.0).sum()) // 2
    single = b.set_index(["dataset", "block_key"]).index.map(one_form)
    assert (np.asarray(single, dtype=bool) == (b.sv_band == "SV=0").values).all(), \
        "SV = 0 is not the same set of blocks as a one-form training half"
    return hits, pairs


def versions():
    out = ["Python {} ({}), {}".format(platform.python_version(), sys.executable,
                                       platform.platform())]
    out += ["{} {}".format(p, metadata.version(p)) for p in PACKAGES]
    return out


def demo():
    """Assert-based self-check of the matched difference on two hand-built blocks."""
    toy = pd.DataFrame({"n": [4, 2], "fired": [3, 2], "rule_ok": [3, 1], "knn_ok": [3, 2],
                        "knn_ok_fired": [2, 2]})
    r = matched_row("demo", toy)
    assert abs(r["rule_precision_fired"] - 4 / 5) < 1e-12 and abs(r["knn_acc_fired"] - 4 / 5) < 1e-12
    assert abs(r["matched_diff"]) < 1e-12 and abs(r["knn_acc_all"] - 5 / 6) < 1e-12
    assert r["matched_ci_lo"] <= r["matched_diff"] <= r["matched_ci_hi"]
    print("phase2_9a self-check: all assertions passed")


def main():
    for v in versions():
        print(v)
    b, sig = load()

    mp = matched_precision(b)
    rc = region_counts(b)
    cs = contested_share(b)
    hits, pairs = max_score_collisions(sig, b)
    for df, name in ((mp, "phase2_9a_matched_precision.csv"),
                     (rc, "phase2_9a_region_counts.csv"),
                     (cs, "phase2_9a_contested_share.csv")):
        print("wrote", dump(df, name))

    pd.set_option("display.width", 200)
    print(mp.to_string(index=False, float_format=lambda x: "{:.4f}".format(x)))
    print(rc.to_string(index=False))
    print(cs.to_string(index=False))
    print("distinct-form pairs within primary blocks: {:,}; pairs scoring 1.0: {}"
          .format(pairs, ", ".join("{} {}".format(a, h) for a, h in hits.items())))


if __name__ == "__main__":
    demo()
    main()
