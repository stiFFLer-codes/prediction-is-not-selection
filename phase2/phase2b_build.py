"""Phase 2.2b step 1: the split, the train-only signals, and the one calibration.

Two things happen here and nothing else. No evaluation-split accuracy is
produced, computed, or printed by this file.

1. The frozen split of PREREG section 3, and the four train-only block signals:
   ADS (section 5), SV (section 6), SV_resid and INIT (section 9). All four are
   computed on the train half only, for every live block, and cached to
   `data/phase2b_blocks.parquet`. These are signals, not results: none of them
   touches a label of a test signature or the output of a mechanism.

2. The one calibration PREREG allows, run on the calibration split only:
   - the fuzzy similarity cutoff, section 7, once per metric family;
   - the SV and SV_resid band edges, section 6.

   Both are written to `phase2b_constants.py`, which is committed *before* any
   evaluation-split run. From that commit they are frozen.

Run: python phase2/phase2b_build.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_core import (  # noqa: E402
    ads, BLOCKS_CACHE, CUTOFF_GRID, METRICS, SEED, TABLE, assign_splits,
    canonical_init_form, init_share, run_block, sv_band_edges,
)
from s2and_blocking import surface_variability  # noqa: E402

CONSTANTS = HERE / "phase2b_constants.py"
REPORT = HERE / "reports" / "phase2b_calibration.md"

COLS = ["sid", "dataset", "block_key", "author_label", "surface_form",
        "first", "middle", "last", "suffix"]


def load_signatures():
    sig = pd.read_parquet(TABLE, columns=COLS)
    for c in ("first", "middle", "last", "suffix", "surface_form", "author_label"):
        sig[c] = sig[c].astype(object).where(sig[c].notna(), "")
    # SV_resid canonical form, computed once per distinct name tuple.
    keys = sig[["first", "middle", "last", "suffix"]].drop_duplicates()
    keys["canon_form"] = [canonical_init_form(f, m, l, s) for f, m, l, s in keys.itertuples(index=False)]
    sig = sig.merge(keys, on=["first", "middle", "last", "suffix"], how="left")
    return assign_splits(sig)


def block_signals(sig):
    """One row per live block: the four train-only signals plus bookkeeping."""
    live = sig[sig.is_live]
    train = live[live.is_train]
    rows = []
    for (dataset, block_key), grp in train.groupby(["dataset", "block_key"], sort=True):
        n_train = len(grp)
        forms = grp.surface_form.value_counts().to_dict()
        canon = grp.canon_form.value_counts().to_dict()
        rows.append({
            "dataset": dataset,
            "block_key": block_key,
            "n_train": n_train,
            "ads": ads(grp.author_label.values),
            "sv": surface_variability(forms),
            "sv_resid": surface_variability(canon),
            "init": init_share(grp.first.tolist()),
            "n_train_forms": len(forms),
            "n_train_authors": grp.author_label.nunique(),
        })
    blocks = pd.DataFrame(rows)
    meta = (live.groupby(["dataset", "block_key"], sort=True)
            .agg(block_index=("block_index", "first"),
                 block_size=("block_size", "first"),
                 is_cal=("is_cal", "first"),
                 n_test=("is_train", lambda s: int((~s).sum())))
            .reset_index())
    return blocks.merge(meta, on=["dataset", "block_key"], how="left")


def mechanism_pass(sig, block_keys, metric_name):
    """Run both mechanisms over the given blocks. Returns one row per test signature."""
    simfunc = METRICS[metric_name]
    wanted = set(block_keys)
    live = sig[sig.is_live]
    out = []
    for (dataset, block_key), grp in live.groupby(["dataset", "block_key"], sort=True):
        if (dataset, block_key) not in wanted:
            continue
        tr = grp[grp.is_train]
        te = grp[~grp.is_train]
        ep, fp, fs = run_block(tr.surface_form.tolist(), tr.author_label.tolist(),
                               te.surface_form.tolist(), simfunc)
        out.append(pd.DataFrame({
            "dataset": dataset,
            "block_key": block_key,
            "block_index": te.block_index.values,
            "truth": te.author_label.values,
            "exact_pred": ep,
            "fuzzy_cand": fp,
            "fuzzy_sim": fs,
        }))
    return pd.concat(out, ignore_index=True)


def score(res, cutoff):
    """Apply a cutoff to the recorded fuzzy candidate and score both mechanisms."""
    fuzzy_fires = res.fuzzy_sim.values >= cutoff
    exact_pred = res.exact_pred.values
    truth = res.truth.values
    exact_ok = np.array([p is not None and p == t for p, t in zip(exact_pred, truth)])
    fuzzy_ok = fuzzy_fires & (res.fuzzy_cand.values == truth)
    return exact_ok, fuzzy_ok, fuzzy_fires


def main():
    print("loading signatures ...")
    sig = load_signatures()

    print("computing train-only block signals ...")
    blocks = block_signals(sig)
    blocks.to_parquet(BLOCKS_CACHE, index=False)
    print("  wrote {}  ({:,} live blocks)".format(BLOCKS_CACHE.name, len(blocks)))

    cal = blocks[blocks.is_cal]
    cal_keys = set(zip(cal.dataset, cal.block_key))
    print("calibration blocks: {:,}".format(len(cal_keys)))

    # --- PREREG section 6: SV and SV_resid band edges, calibration split only
    sv_edges = sv_band_edges(cal.sv.tolist())
    svr_edges = sv_band_edges(cal.sv_resid.tolist())
    print("SV band edges       {:.6f} {:.6f}".format(*sv_edges))
    print("SV_resid band edges {:.6f} {:.6f}".format(*svr_edges))

    # --- PREREG section 7: one global fuzzy cutoff per metric family
    curves = {}
    chosen = {}
    for metric in METRICS:
        print("mechanism pass on calibration split, {} ...".format(metric))
        res = mechanism_pass(sig, cal_keys, metric)
        rows = []
        for c in CUTOFF_GRID:
            _, fuzzy_ok, fires = score(res, c)
            rows.append({"cutoff": c,
                         "fuzzy_accuracy": float(fuzzy_ok.mean()),
                         "fuzzy_coverage": float(fires.mean())})
        curve = pd.DataFrame(rows)
        best = curve.fuzzy_accuracy.max()
        # PREREG section 7 step 4: highest pooled accuracy, ties broken toward
        # the HIGHER cutoff, which is the more conservative (more abstaining) one.
        pick = float(curve.cutoff[curve.fuzzy_accuracy >= best - 1e-12].max())
        curves[metric] = curve
        chosen[metric] = pick
        exact_ok, _, _ = score(res, pick)
        print("  n_test={:,}  chosen cutoff {:.2f}  fuzzy acc {:.4f}  (exact acc {:.4f}, context only)"
              .format(len(res), pick, best, float(exact_ok.mean())))

    write_constants(chosen, sv_edges, svr_edges, curves, cal, blocks)
    write_report(chosen, sv_edges, svr_edges, curves, cal, blocks)
    print("wrote {} and {}".format(CONSTANTS.name, REPORT.name))


def write_constants(chosen, sv_edges, svr_edges, curves, cal, blocks):
    lines = [
        '"""FROZEN Phase 2.2b calibration constants.',
        "",
        "Produced once by `phase2b_build.py` on the calibration split only, which is",
        "disjoint at block level from every block that produces a reported number.",
        "Committed before any evaluation-split run, per PREREG sections 6 and 7.",
        "Do not edit. Re-running `phase2b_build.py` reproduces this file exactly.",
        '"""',
        "",
        "SEED = {}".format(SEED),
        "N_CALIBRATION_BLOCKS = {}".format(len(cal)),
        "N_LIVE_BLOCKS = {}".format(len(blocks)),
        "",
        "# PREREG section 7: one global cutoff per metric family, highest pooled",
        "# calibration accuracy, ties broken toward the higher cutoff.",
        "FUZZY_CUTOFF = {",
    ]
    for metric, value in chosen.items():
        lines.append("    {!r}: {:.2f},".format(metric, value))
    lines += [
        "}",
        "",
        "# PREREG section 6: terciles of the strictly positive values, calibration split.",
        "SV_BAND_EDGES = ({:.12f}, {:.12f})".format(*sv_edges),
        "SV_RESID_BAND_EDGES = ({:.12f}, {:.12f})".format(*svr_edges),
        "",
        "# The full accuracy-versus-cutoff curve PREREG section 7 step 5 requires,",
        "# as (cutoff, pooled fuzzy accuracy, fuzzy coverage) on the calibration split.",
        "CUTOFF_CURVE = {",
    ]
    for metric, curve in curves.items():
        lines.append("    {!r}: [".format(metric))
        for r in curve.itertuples(index=False):
            lines.append("        ({:.2f}, {:.6f}, {:.6f}),".format(
                r.cutoff, r.fuzzy_accuracy, r.fuzzy_coverage))
        lines.append("    ],")
    lines += ["}", ""]
    CONSTANTS.write_text("\n".join(lines), encoding="utf-8")


def write_report(chosen, sv_edges, svr_edges, curves, cal, blocks):
    out = ["# Phase 2.2b calibration, frozen",
           "",
           "Produced by `phase2/phase2b_build.py`. Everything on this page comes from the "
           "**calibration split only**: a random 15% of live blocks drawn at block level with "
           "seed 20260918, disjoint from every block that produces a reported result. "
           "PREREG sections 6 and 7 allow exactly these two calibrations and no others. "
           "The values are written to `phase2/phase2b_constants.py` and committed before any "
           "evaluation-split run.",
           "",
           "## Split",
           "",
           "| quantity | value |",
           "| --- | ---: |",
           "| live blocks | {:,} |".format(len(blocks)),
           "| calibration blocks | {:,} |".format(len(cal)),
           "| evaluation blocks | {:,} |".format(len(blocks) - len(cal)),
           "| calibration share | {:.4%} |".format(len(cal) / len(blocks)),
           "| calibration signatures (train + test) | {:,} |".format(
               int(cal.n_train.sum() + cal.n_test.sum())),
           "| calibration test signatures | {:,} |".format(int(cal.n_test.sum())),
           "",
           "## SV and SV_resid band edges (PREREG section 6)",
           "",
           "Band 0 is SV exactly 0 and is structural, never merged into a quantile. "
           "Bands 1 to 3 are the terciles of the **strictly positive** values, cut at the "
           "33.33rd and 66.67th percentiles of the calibration blocks.",
           "",
           "| signal | calibration blocks with the signal defined | strictly positive | 33.33rd pct | 66.67th pct |",
           "| --- | ---: | ---: | ---: | ---: |",
           "| SV | {:,} | {:,} | {:.6f} | {:.6f} |".format(
               int(cal.sv.notna().sum()), int((cal.sv > 0).sum()), *sv_edges),
           "| SV_resid | {:,} | {:,} | {:.6f} | {:.6f} |".format(
               int(cal.sv_resid.notna().sum()), int((cal.sv_resid > 0).sum()), *svr_edges),
           "",
           "## Fuzzy cutoff (PREREG section 7)",
           "",
           "One global cutoff per metric family. Not one per dataset, not one per band. "
           "Selection rule, fixed in advance: highest pooled accuracy over all calibration "
           "test signatures, ties broken toward the **higher** cutoff because it abstains more.",
           ""]
    for metric, curve in curves.items():
        out += ["### {}".format(metric),
                "",
                "| cutoff | pooled fuzzy accuracy | fuzzy coverage |",
                "| ---: | ---: | ---: |"]
        for r in curve.itertuples(index=False):
            mark = "  **<- chosen**" if abs(r.cutoff - chosen[metric]) < 1e-9 else ""
            out.append("| {:.2f} | {:.4f} | {:.4f}{} |".format(
                r.cutoff, r.fuzzy_accuracy, r.fuzzy_coverage, mark))
        note = ""
        if abs(chosen[metric] - min(CUTOFF_GRID)) < 1e-9:
            note = (" The curve is monotonically decreasing in the cutoff, so the selected "
                    "value sits on the **lower boundary of the pre-registered grid**. "
                    "The grid was fixed in advance in PREREG section 7 and is not widened "
                    "here. What it means substantively is that on this data the fuzzy "
                    "mechanism is never helped by abstaining: a nearest neighbour, however "
                    "far, beats no answer at all, because an abstention is scored as wrong. "
                    "The practical consequence is a fuzzy arm with near-total coverage, "
                    "which is reported beside every accuracy number.")
        out += ["", "**Frozen cutoff for {}: {:.2f}.**{}".format(metric, chosen[metric], note), ""]
    out += ["## What is deliberately absent",
            "",
            "No evaluation-split number appears above. No winner, no verdict, no ADS-band or "
            "SV-band result, no hypothesis outcome. Those exist only after this file and "
            "`phase2b_constants.py` are committed.",
            ""]
    REPORT.write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
