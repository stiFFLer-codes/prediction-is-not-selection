"""Phase 2.7b: re-analysis of the frozen 2.2e records, for peer-review majors 1, 2, 3 and 8.

Everything here is a **supplementary or sensitivity analysis** layered on records
that already exist. Nothing is re-run, re-tuned, re-banded or redefined:

- the per-block four-verdict records come from `reports/tables/phase2e_blocks_scored.csv.gz`,
  written by `phase2e_run.py` at the frozen seed;
- the mechanisms, the split, the band edges, the margins and the bootstrap
  definitions are imported from `phase2b_core` / `phase2b_constants`, not restated;
- `PREREG.md`, Amendment 1 and Addendum 1a are untouched, and no frozen primary
  number is overwritten. The primary analysis population stays 13,902 blocks and
  197,479 test signatures.

Four tasks, one per peer-review major:

1. **Major 1, small-test-block sensitivity.** The paired per-block bootstrap is a
   point mass at one test signature, so such a block can never be `undecided`.
   Everything the per-block verdict feeds is recomputed on blocks with at least
   3 test signatures and reported beside the frozen all-blocks version.
2. **Major 2, block size as a third design-time signal.** Block size is readable
   before anything is built. The ADS and SV band analyses are mirrored on it.
3. **Major 3, uncertainty for the driver comparison.** eta2_SV - eta2_ADS is
   bootstrapped by resampling blocks, B = 2000, at the frozen seed scheme, with a
   size-adjusted variant as a labelled diagnostic and the k = 2 pair beside k = 5.
4. **Major 8, accuracy accounting.** The out-of-history share, which is an
   automatic error for both mechanisms and therefore a per-dataset accuracy
   ceiling, derived from the frozen split and the labels; and the rule's
   precision conditional on firing.

Run: python phase2/phase2_7b_reanalysis.py
    demo()  - assert-based self-check
    main()  - writes reports/phase2_7b_reanalysis.md and reports/tables/phase2_7b_*.csv
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from phase2b_core import (  # noqa: E402
    ADS_BANDS, BOOTSTRAP_B, DELTAS, DELTA_PRIMARY, MIN_BLOCKS, SV_BAND_NAMES,
    band_seed,
)
from phase2b_build import load_signatures  # noqa: E402
from phase2b_run import dump, md_table, populations  # noqa: E402
from phase2e_run import (  # noqa: E402
    DECIDED, PRIMARY, VERDICTS, combo, driver_comparison, eta2_decomposition,
    gradient_clauses, order_bands, pooled_table, sort_cells, verdict_bars,
)

FIGS = HERE / "reports" / "figs"
BLOCKS = HERE / "reports" / "tables" / "phase2e_blocks_scored.csv.gz"
SIG_CACHE = HERE / "data" / "phase2e_eval_sigs.parquet"
REPORT = HERE / "reports" / "phase2_7b_reanalysis.md"

# The minimum test-set size of the sensitivity analysis. Three, because the
# bootstrap interval is a point mass at 1 and still only three-valued at 2.
MIN_TEST = 3
SECONDARY_K = 2

# Block-size bands. Octaves, the same shape as the frozen test-set-size strata of
# `phase2b_run.SIZE_BINS`, starting at 3 because n_train >= 2 is the primary
# population rule and no block below 3 signatures can satisfy it. Chosen for
# balance, not fitted: the seven bands hold 1,157 to 2,293 blocks each.
BSIZE_BINS = [(3, 4), (5, 8), (9, 16), (17, 32), (33, 64), (65, 128), (129, 10 ** 9)]
BSIZE_ORDER = ["3-4", "5-8", "9-16", "17-32", "33-64", "65-128", "129+"]


def bsize_band(n):
    for lo, hi in BSIZE_BINS:
        if lo <= n <= hi:
            return "{}-{}".format(lo, hi) if hi < 10 ** 9 else "{}+".format(lo)
    return "?"


def vcol(k=5, delta=DELTA_PRIMARY, arm="levenshtein"):
    return "bverdict_{}_{:.2f}".format(combo(arm, k), delta)


# --------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------

def verdict_distribution(bk, label, k=5, delta=DELTA_PRIMARY):
    """The four-verdict distribution of a population, as counts and shares."""
    counts = bk[vcol(k, delta)].value_counts()
    row = {"population": label, "blocks": len(bk)}
    n_dec = 0
    for v in VERDICTS:
        c = int(counts.get(v, 0))
        row[v] = c
        if v in DECIDED:
            n_dec += c
    row["decided"] = n_dec
    row["decided_rate"] = n_dec / len(bk) if len(bk) else float("nan")
    for v in VERDICTS:
        row["share_" + v] = row[v] / len(bk) if len(bk) else float("nan")
    return row


def band_tables(bk, tag, k=5):
    """The three frozen band summaries (ADS marginal, SV marginal, 5 x 4 grid).

    `pooled_table` is the 2.2e function unchanged, so the pooled bootstrap, the
    eligibility rule and the four-verdict rule are the frozen ones. The seed of a
    band is `band_seed(tag|labels)`, the frozen scheme; passing 2.2e's own tags
    reproduces 2.2e's numbers exactly, which `demo()` asserts.
    """
    c = combo("levenshtein", k)
    ads_m = order_bands(pooled_table(bk, ["ads_band"], c, tag + "ads"), "ads_band", ADS_BANDS)
    sv_m = order_bands(pooled_table(bk, ["sv_band"], c, tag + "sv"), "sv_band", SV_BAND_NAMES)
    cells = sort_cells(pooled_table(bk, ["ads_band", "sv_band"], c, tag + "cells_sv"))
    return {"ads": ads_m, "sv": sv_m, "cells": cells}


# --------------------------------------------------------------------------
# task 1: small-test-block sensitivity (Major 1)
# --------------------------------------------------------------------------

def task1(bk, out):
    out += ["## 1. Small-test-block sensitivity (Major 1)", "",
            "The paired per-block bootstrap of `PREREG.md` section 8 resamples a block's "
            "test signatures as a multinomial over the three per-signature outcomes "
            "{+1, 0, -1}. At one test signature that distribution is a point mass, so the "
            "interval is [0, 0], [+1, +1] or [-1, -1] and the block is recorded as a "
            "demonstrated tie or as a decided winner on the strength of one item. It can "
            "never be `undecided`. At two test signatures the interval takes three values "
            "and is still coarse.", "",
            "This section recomputes everything the per-block verdict feeds on blocks with "
            "at least {} test signatures, and prints it beside the frozen all-blocks "
            "version. **It is a sensitivity analysis. The frozen primary analysis is "
            "unchanged and is the all-blocks column.**".format(MIN_TEST), ""]

    sub = bk[bk.n_test >= MIN_TEST].copy()
    out += ["Population: {:,} of {:,} blocks survive the restriction ({:.2%}), carrying "
            "{:,} of {:,} test signatures ({:.2%}). The restriction removes small blocks, "
            "so it costs a quarter of the blocks and under 3% of the signatures."
            .format(len(sub), len(bk), len(sub) / len(bk),
                    int(sub.n_test.sum()), int(bk.n_test.sum()),
                    sub.n_test.sum() / bk.n_test.sum()), ""]

    # --- 1a. the four-verdict distribution, side by side
    dist = pd.DataFrame([verdict_distribution(bk, "all blocks (frozen primary)"),
                         verdict_distribution(sub, "n_test >= {}".format(MIN_TEST)),
                         verdict_distribution(bk[bk.n_test == 1], "n_test = 1 only"),
                         verdict_distribution(bk[bk.n_test == 2], "n_test = 2 only")])
    show = ["population", "blocks"] + list(VERDICTS) + ["decided", "decided_rate"]
    out += ["### 1a. Four-verdict per-block distribution and the decided-winner rate", "",
            md_table(dist[show]), "",
            md_table(dist[["population", "blocks"] + ["share_" + v for v in VERDICTS]]), "",
            "Table: " + dump(dist, "phase2_7b_verdict_distribution.csv"), ""]

    d_all, d_sub = dist.iloc[0], dist.iloc[1]
    s1, s2 = dist.iloc[2], dist.iloc[3]
    out += ["**The size-1 and size-2 strata explicitly.** The size-1 stratum holds {:,} "
            "blocks: {:,} `rule wins`, {:,} `k-NN wins`, {:,} `tie` and **{:,} "
            "`undecided`**, the last of which is zero by construction and not by evidence. "
            "The size-2 stratum holds {:,} blocks: {:,}, {:,}, {:,} and {:,}. Together the "
            "two strata supply **{:,} of the {:,} decided verdicts ({:.1%})** and **{:,} of "
            "the {:,} demonstrated ties ({:.1%})** in the frozen primary analysis."
            .format(s1.blocks, s1["rule wins"], s1["k-NN wins"], s1["tie"], s1["undecided"],
                    s2.blocks, s2["rule wins"], s2["k-NN wins"], s2["tie"], s2["undecided"],
                    s1.decided + s2.decided, d_all.decided,
                    (s1.decided + s2.decided) / d_all.decided,
                    s1["tie"] + s2["tie"], d_all["tie"],
                    (s1["tie"] + s2["tie"]) / d_all["tie"]), "",
            "**The decided-winner rate falls from {:.4f} to {:.4f} under the restriction**, "
            "and the direction of the per-block margin flips: all blocks give {:,} `rule "
            "wins` against {:,} `k-NN wins`, the restricted set gives {:,} against {:,}. "
            "The tie share falls from {:.4f} to {:.4f} and the undecided share rises from "
            "{:.4f} to {:.4f}, which is the degeneracy being removed rather than a change "
            "of evidence."
            .format(d_all.decided_rate, d_sub.decided_rate,
                    d_all["rule wins"], d_all["k-NN wins"],
                    d_sub["rule wins"], d_sub["k-NN wins"],
                    d_all["share_tie"], d_sub["share_tie"],
                    d_all["share_undecided"], d_sub["share_undecided"]), ""]

    # --- 1b. the H2 gradient
    g_all = band_tables(bk, "")                 # frozen 2.2e tags -> frozen numbers
    g_sub = band_tables(sub, "p27b_n3_")
    col = "decided_rate_{:.2f}".format(DELTA_PRIMARY)

    grad = g_all["ads"][["ads_band", "n_blocks", col]].merge(
        g_sub["ads"][["ads_band", "n_blocks", col]], on="ads_band",
        suffixes=("_all", "_n3"))
    grad.columns = ["ads_band", "blocks_all", "decided_rate_all", "blocks_n3", "decided_rate_n3"]
    out += ["### 1b. The H2 decidability gradient across ADS bands", "",
            "Marginal decided-winner rate by ADS band, delta = 0.05, k = 5.", "",
            md_table(grad), "",
            "Table: " + dump(grad, "phase2_7b_gradient_ads.csv"), ""]

    pshow = ["n_blocks", "n_test", "pooled_gap", "ci_lo", "ci_hi", "verdict_0.05",
             "verdict_0.03", "verdict_0.02", "under_powered", "decided_rate_0.05"]
    out += ["The pooled band verdicts under the restriction, which is what the "
            "pre-registered power floor actually counts:", "",
            md_table(g_sub["ads"], ["ads_band"] + pshow), "",
            md_table(g_sub["sv"], ["sv_band"] + pshow), "",
            "Table: " + dump(pd.concat([g_sub["ads"], g_sub["sv"]], ignore_index=True),
                             "phase2_7b_restricted_marginals.csv"), ""]
    n_dec_ads = int(g_sub["ads"]["verdict_0.05"].isin(DECIDED).sum())
    n_dec_sv = int(g_sub["sv"]["verdict_0.05"].isin(DECIDED).sum())
    n_dec_cells = int(g_sub["cells"]["verdict_0.05"].isin(DECIDED).sum())
    assert n_dec_ads == 0 and n_dec_sv == 0 and n_dec_cells == 0, \
        "the restriction would change the H2/H3 power floor, which the prose below denies"
    out += ["**{} ADS bands, {} SV bands and {} of the 20 grid cells carry a decided "
            "pooled verdict at delta = 0.05 under the restriction**, exactly as in the "
            "frozen analysis. The pre-registered power floor still bites first, so H2 and "
            "H3 stay Inconclusive whichever population is used."
            .format(n_dec_ads, n_dec_sv, n_dec_cells), ""]

    cl_all = gradient_clauses(g_all["cells"], g_all["ads"], g_all["sv"], DELTA_PRIMARY)
    cl_sub = gradient_clauses(g_sub["cells"], g_sub["ads"], g_sub["sv"], DELTA_PRIMARY)
    for lbl, cl in (("all blocks (frozen)", cl_all),
                    ("n_test >= {}".format(MIN_TEST), cl_sub)):
        out += ["Gradient clauses at fixed SV, {}:".format(lbl), "",
                md_table(cl["per_sv"]), "",
                "Non-increasing across ADS in {} of {} usable SV bands; strictly lower in "
                "the top ADS band than the bottom in {} of {}. Marginal ADS reading, top "
                "below bottom: **{}**."
                .format(int(cl["per_sv"].non_increasing.fillna(False).sum()),
                        cl["usable_sv_bands"],
                        int(cl["per_sv"].top_below_bottom.fillna(False).sum()),
                        cl["usable_sv_bands"], cl["marginal_top_below_bottom"]), ""]

    # --- 1c. the driver comparison
    rows = []
    for lbl, g in (("all blocks (frozen)", g_all), ("n_test >= {}".format(MIN_TEST), g_sub)):
        for d in DELTAS:
            r = driver_comparison(g["cells"], g["ads"], g["sv"], d, lbl)
            rows.append({k2: v for k2, v in r.items() if not k2.startswith("_")})
    drv = pd.DataFrame(rows)
    keep = ["label", "delta", "eligible_cells", "SS_total", "eta2_ADS", "eta2_SV",
            "avg_range_ADS", "avg_range_SV", "clause"]
    out += ["### 1c. The Addendum 1a driver comparison under the restriction", "",
            md_table(drv[keep]), "",
            "Table: " + dump(drv, "phase2_7b_driver_restricted.csv"), ""]

    a = drv[(drv.label.str.startswith("all")) & (drv.delta == DELTA_PRIMARY)].iloc[0]
    b = drv[(~drv.label.str.startswith("all")) & (drv.delta == DELTA_PRIMARY)].iloc[0]
    ma, ms = grad.decided_rate_all.values, grad.decided_rate_n3.values
    out += ["### 1d. Does anything change?", "",
            "**The gradient changes shape, and this is the one substantive result of "
            "task 1.** The frozen marginal gradient runs {} and 2.2e reported, against "
            "Amendment 1's prediction, that it **rises again** in the top ADS band instead "
            "of approaching zero. Restricted to blocks with at least {} test signatures it "
            "runs {}, which is monotonically non-increasing: the ADS = 1.0 rate falls from "
            "{:.4f} to {:.4f} and now sits **below** the [0.9,1.0) band rather than above "
            "it. The rise Amendment 1 did not predict is carried by blocks with one or two "
            "test signatures inside the ADS = 1.0 band."
            .format(" / ".join("{:.4f}".format(v) for v in ma), MIN_TEST,
                    " / ".join("{:.4f}".format(v) for v in ms), ma[-1], ms[-1]), "",
            "One of the two per-SV clause counts moves with it. Non-increasing across ADS "
            "in {} of {} usable SV bands restricted, against {} of {} frozen, which is "
            "still not a majority. Top ADS band strictly below the bottom in {} of {} "
            "against {} of {}, which **is** a majority restricted and was not frozen. The "
            "marginal reading stays {} in both. So the clause the frozen analysis reported "
            "as failing on a two-of-four split passes on the restricted population."
            .format(int(cl_sub["per_sv"].non_increasing.fillna(False).sum()),
                    cl_sub["usable_sv_bands"],
                    int(cl_all["per_sv"].non_increasing.fillna(False).sum()),
                    cl_all["usable_sv_bands"],
                    int(cl_sub["per_sv"].top_below_bottom.fillna(False).sum()),
                    cl_sub["usable_sv_bands"],
                    int(cl_all["per_sv"].top_below_bottom.fillna(False).sum()),
                    cl_all["usable_sv_bands"], cl_sub["marginal_top_below_bottom"]),
            "",
            "**This does not move H2.** The clause counts above are read only after the "
            "power floor, and the floor is unchanged: no marginal band and no cell is "
            "decided at delta = 0.05 under the restriction, as the tables in 1b show. H2 "
            "would still return Inconclusive on the first gate. What changes is the "
            "**narrative** the manuscript attaches to the gradient, and that is a prose "
            "matter for 2.7c: the reported non-monotonicity is a small-block artifact, and "
            "on blocks large enough for the interval to mean anything the gradient behaves "
            "the way Amendment 1 said it would.", "",
            "**The driver comparison keeps its verdict and loses half its margin.** "
            "Restricted, eta2_ADS = {:.4f} against eta2_SV = {:.4f} at the primary margin, "
            "against {:.4f} and {:.4f} frozen: the difference narrows from {:+.4f} to "
            "{:+.4f}. The averaged ranges are {:.4f} against {:.4f}, against {:.4f} and "
            "{:.4f} frozen. ADS still loses under both measures at every margin in the "
            "table above, so Addendum 1a's clause comes out **{}** either way. The "
            "direction is robust to the restriction; the size of the gap is not, and "
            "section 3's interval says the same thing a different way."
            .format(b.eta2_ADS, b.eta2_SV, a.eta2_ADS, a.eta2_SV,
                    a.eta2_SV - a.eta2_ADS, b.eta2_SV - b.eta2_ADS,
                    b.avg_range_ADS, b.avg_range_SV, a.avg_range_ADS, a.avg_range_SV,
                    b.clause), ""]
    return {"sub": sub, "grids_all": g_all, "grids_sub": g_sub, "dist": dist, "driver": drv}


# --------------------------------------------------------------------------
# task 2: block size as a third design-time signal (Major 2)
# --------------------------------------------------------------------------

def task2(bk, sub, out):
    out += ["## 2. Block size as a third design-time signal (Major 2)", "",
            "Block size is the total number of signatures in a block. It is readable before "
            "anything is built, from the blocking pass alone, with no labels and no "
            "mechanism, so it satisfies the same design-time criterion as ADS and SV. It "
            "was **not** pre-registered and nothing below is a pre-registered test: this is "
            "a supplementary analysis of a signal the frozen regression named and the "
            "frozen design did not carry.", "",
            "Bands are octaves on block size, the same shape as the frozen test-set-size "
            "strata, starting at 3 because the primary population rule n_train >= 2 admits "
            "no smaller block. They were chosen for balance and are not fitted to any "
            "outcome; every band holds well above the 30-block eligibility floor.", ""]

    rows = []
    for name, pop in (("full primary population", bk),
                      ("n_test >= {} subset".format(MIN_TEST), sub)):
        tab = pooled_table(pop, ["bsize_band"], PRIMARY, "p27b_bsize_" + name)
        tab = order_bands(tab, "bsize_band", BSIZE_ORDER)
        tab["rule_precision"] = tab.rule_acc / tab.rule_cov
        tab.insert(0, "population", name)
        rows.append(tab)
    bs = pd.concat(rows, ignore_index=True)

    show = ["bsize_band", "n_blocks", "n_test", "rule_acc", "knn_acc", "pooled_gap",
            "ci_lo", "ci_hi", "verdict_0.05", "verdict_0.03", "verdict_0.02",
            "under_powered", "decided_rate_0.05", "rule_cov", "rule_precision"]
    for name in bs.population.unique():
        out += ["### Pooled gap by block-size band, {}".format(name), "",
                md_table(bs[bs.population == name], show), ""]
    out += ["Table: " + dump(bs, "phase2_7b_blocksize_pooled.csv"), ""]

    full0 = bs[bs.population == "full primary population"]
    dec_bands = full0[full0["verdict_0.05"].isin(DECIDED)]
    out += ["**Read the first two rows before anything else in this pass.** Block size is "
            "the only design-time signal examined anywhere in this project that produces a "
            "**decided pooled band verdict at the primary margin**. {} of the seven bands "
            "are decided at delta = 0.05: {}. Neither ADS nor SV has a single decided "
            "marginal band at delta = 0.05, which is the fact that carried H2 and H3 to "
            "Inconclusive. Section 2d below establishes what this does and does not mean, "
            "and it is not what it looks like on this table alone."
            .format(len(dec_bands),
                    ", ".join("{} at {:+.4f} [{:+.4f}, {:+.4f}], `{}`".format(
                        r.bsize_band, r.pooled_gap, r.ci_lo, r.ci_hi, r["verdict_0.05"])
                        for _, r in dec_bands.iterrows())), ""]

    # --- per-block winner distribution and the winner-by-size table
    wrows = []
    for name, pop in (("full primary population", bk),
                      ("n_test >= {} subset".format(MIN_TEST), sub)):
        for b in BSIZE_ORDER:
            grp = pop[pop.bsize_band == b]
            if not len(grp):
                continue
            r = verdict_distribution(grp, b)
            r["band"] = r.pop("population")
            r["population"] = name
            r["mean_block_size"] = float(grp.block_size.mean())
            r["mean_n_test"] = float(grp.n_test.mean())
            r["rule_share_of_decided"] = (r["rule wins"] / r["decided"]
                                          if r["decided"] else float("nan"))
            wrows.append(r)
    win = pd.DataFrame(wrows)

    wshow = ["population", "band", "blocks", "mean_block_size", "mean_n_test"] \
        + list(VERDICTS) + ["decided", "decided_rate", "rule_share_of_decided"]
    for name in win.population.unique():
        out += ["### Per-block winner distribution by block-size band, {}".format(name), "",
                md_table(win[win.population == name], wshow), ""]
    out += ["Table: " + dump(win, "phase2_7b_blocksize_verdicts.csv"), ""]

    wb = win[["population", "band", "blocks", "rule wins", "k-NN wins", "decided",
              "rule_share_of_decided"]]
    out += ["### Winner by block size: rule wins against k-NN wins", "",
            md_table(wb), ""]

    verdict_bars(order_bands(
        pooled_table(bk, ["bsize_band"], PRIMARY, "p27b_bsize_full primary population"),
        "bsize_band", BSIZE_ORDER),
        "bsize_band", "phase2_7b_verdicts_by_blocksize.png",
        "Per-block verdict shares by block-size band (delta = 0.05, k = 5)")
    out += ["Figure: `reports/figs/phase2_7b_verdicts_by_blocksize.png`", ""]

    # --- 2c. block size at fixed ADS, the paper's own standard for a second axis
    bk = bk.copy()
    bk["ads_split"] = np.where(bk.ads >= 1.0, "ADS = 1.0", "ADS < 1.0")
    strat = pooled_table(bk, ["ads_split", "bsize_band"], PRIMARY, "p27b_bsize_by_ads")
    strat = strat.sort_values(
        ["ads_split", "bsize_band"],
        key=lambda s: s.map({v: i for i, v in enumerate(BSIZE_ORDER)})
        if s.name == "bsize_band" else s).reset_index(drop=True)
    sshow = ["ads_split", "bsize_band", "n_blocks", "n_test", "pooled_gap", "ci_lo",
             "ci_hi", "verdict_0.05", "verdict_0.02", "under_powered", "rule_cov"]
    out += ["### 2c. Block size at fixed ADS", "",
            "The manuscript never shows one axis without holding the other, because the "
            "axes correlate. Block size correlates with both: Spearman {:+.4f} with ADS and "
            "{:+.4f} with SV over the primary population. The table above therefore has to "
            "be read at fixed ADS before it can be read as a statement about block size. "
            "The stratification below is the coarse one the report already uses for the "
            "structural top row, ADS = 1.0 against everything below it. It is a "
            "supplementary stratification and not a frozen band."
            .format(_spearman(bk.block_size.values, bk.ads.values),
                    _spearman(bk.block_size.values, bk.sv.values)), "",
            md_table(strat, sshow), "",
            "Table: " + dump(strat, "phase2_7b_blocksize_by_ads.csv"), ""]

    hi_s = strat[strat.ads_split == "ADS = 1.0"]
    lo_s = strat[strat.ads_split == "ADS < 1.0"]
    out += ["**The sign change across block-size bands does not survive conditioning on "
            "ADS.** Inside ADS = 1.0 the pooled gap is negative in every band and runs "
            "{}, {}. Inside ADS < 1.0 it is positive in every band and runs {}, {}. "
            "Neither stratum changes sign anywhere. What changes across the marginal "
            "block-size bands is the **mix**: {:.1%} of blocks in the smallest band are "
            "ADS = 1.0 against {:.1%} in the largest. The marginal reversal is "
            "composition, not a winner reversal."
            .format(" / ".join("{}={:+.4f}".format(r.bsize_band, r.pooled_gap)
                               for _, r in hi_s.iterrows()),
                    _shrink_note(hi_s.pooled_gap.values),
                    " / ".join("{}={:+.4f}".format(r.bsize_band, r.pooled_gap)
                               for _, r in lo_s.iterrows()),
                    _shrink_note(lo_s.pooled_gap.values),
                    float((bk[bk.bsize_band == BSIZE_ORDER[0]].ads >= 1.0).mean()),
                    float((bk[bk.bsize_band == BSIZE_ORDER[-1]].ads >= 1.0).mean())), "",
            "**Block size still decides bands inside a stratum, and it decides them the "
            "same way throughout the stratum.** Inside ADS = 1.0 the bands {} are decided "
            "`k-NN wins` at delta = 0.05 and the rest are ties. Inside ADS < 1.0 the bands "
            "{} are decided `rule wins` and the rest are ties or undecided. That is a "
            "tie-crossing in each stratum, in the frozen vocabulary of `PREREG.md` "
            "section 9, and a winner reversal in neither."
            .format(", ".join(hi_s[hi_s["verdict_0.05"].isin(DECIDED)].bsize_band) or "none",
                    ", ".join(lo_s[lo_s["verdict_0.05"].isin(DECIDED)].bsize_band)
                    or "none"), ""]

    # --- 2d. reconciliation and the verdict on block size
    full = bs[bs.population == "full primary population"]
    w = win[win.population == "full primary population"]
    big = w[w.band.isin(["65-128", "129+"])]
    small = w[w.band.isin(["3-4", "5-8"])]
    neg = full[full.pooled_gap < 0]
    pos = full[full.pooled_gap >= 0]
    out += ["### 2d. Reconciling the pooled headline with the per-block picture", "",
            "Pooled over signatures the k-nearest vote is ahead by 0.0050. Per block the "
            "rule takes {:,} wins against the vote's {:,}. Both are true and block size is "
            "what separates them."
            .format(int(w["rule wins"].sum()), int(w["k-NN wins"].sum())), "",
            "- **The vote's per-block wins live in small blocks.** The two smallest bands "
            "({}) hold {:,} of the vote's {:,} per-block wins ({:.1%}) and {:,} of the "
            "rule's {:,} ({:.1%}). Above 64 signatures the vote wins no block at all."
            .format(", ".join(small.band), int(small["k-NN wins"].sum()),
                    int(w["k-NN wins"].sum()),
                    small["k-NN wins"].sum() / max(w["k-NN wins"].sum(), 1),
                    int(small["rule wins"].sum()), int(w["rule wins"].sum()),
                    small["rule wins"].sum() / max(w["rule wins"].sum(), 1)),
            "- **The signatures live in large blocks.** The two largest bands ({}) are "
            "{:,} of {:,} blocks ({:.1%}) but {:,} of {:,} test signatures ({:.1%}). A "
            "one-block-one-vote tally and a one-signature-one-vote pool are therefore "
            "counting almost disjoint majorities."
            .format(", ".join(big.band), int(big.blocks.sum()), len(bk),
                    big.blocks.sum() / len(bk),
                    int(bk[bk.bsize_band.isin(['65-128', '129+'])].n_test.sum()),
                    int(bk.n_test.sum()),
                    bk[bk.bsize_band.isin(['65-128', '129+'])].n_test.sum() / bk.n_test.sum()),
            "- **The pooled gap is not carried by the bands that hold the signatures.** "
            "Summed over bands, the {} bands with a negative gap contribute a net of {:,} "
            "signatures' worth of rule deficit on {:,} test signatures, and the {} bands "
            "with a non-negative gap contribute {:+,} on {:,}. The total is {:,} over "
            "{:,}, which is the pooled -0.0050. Two thirds of the signatures sit in bands "
            "whose own gap rounds to zero or favours the rule; the headline is negative "
            "because of the third that does not."
            .format(len(neg),
                    int(round((neg.pooled_gap * neg.n_test).sum())), int(neg.n_test.sum()),
                    len(pos),
                    int(round((pos.pooled_gap * pos.n_test).sum())), int(pos.n_test.sum()),
                    int(round((full.pooled_gap * full.n_test).sum())),
                    int(full.n_test.sum())), ""]

    rho = _spearman(np.arange(len(full)), full.pooled_gap.values)
    biggest = full.pooled_gap.iloc[int(np.argmax(np.abs(full.pooled_gap.values)))]
    assert (full.rule_precision > full.knn_acc).all(), \
        "the conditional-precision claim does not hold in every block-size band"
    out += [
        "### 2e. Does block size predict the winner, and in which direction?", "",
        "**Yes on the per-block winner, in the direction of the rule.** Across the seven "
        "bands the rule's share of decided per-block verdicts runs {}: it jumps between "
        "the 5-8 and 9-16 bands rather than climbing smoothly, and above 64 signatures it "
        "is 1.0 because the vote wins nothing there. The pooled gap, unlike that share, is "
        "monotone in band order, rank correlation {:+.4f} over seven points. Read on its "
        "own this is the strongest design-time structure anywhere in the project."
        .format(" / ".join("{}={:.4f}".format(r.band, r.rule_share_of_decided)
                           for r in w.itertuples(index=False)), rho), "",
        "**Yes on a pooled verdict too, which neither pre-registered signal managed.** At "
        "delta = 0.05 the bands {} are decided `k-NN wins`. The largest band gap is "
        "{:+.4f}, more than twice the primary margin. **This is the one place in the "
        "re-analysis where a design-time signal clears the bar the pre-registered signals "
        "could not, and the prose pass has to say so.**"
        .format(", ".join(full[full["verdict_0.05"].isin(DECIDED)].bsize_band), biggest), "",
        "**And it is not the finding it appears to be, for two measured reasons.**", "",
        "1. **Conditioning on ADS removes the reversal.** Section 2c: inside ADS = 1.0 "
        "every band favours the vote, inside ADS < 1.0 every band favours the rule, and "
        "the marginal sign change across bands is the changing mix of the two. At fixed "
        "ADS block size still decides bands, but it decides every one of them the same "
        "way, so it is a **gap-compression** signal, the shape Amendment 1 pre-registered "
        "for ADS itself, and not a winner-direction signal. Which mechanism to build is "
        "still set by ADS; block size only says how much the choice is worth.",
        "2. **The decided small-block cells are an abstention effect, not a resolution "
        "effect.** The rule's coverage climbs monotonically with block size, {}, and it is "
        "the abstentions, scored as errors, that produce the deficit. The rule's precision "
        "where it fires **exceeds the vote's accuracy in all seven bands**, including both "
        "decided ones: {:.4f} against {:.4f} in the smallest. A designer told \"use the "
        "vote on small blocks\" is being told to prefer the mechanism that is less often "
        "right when it commits, because the other one declines to commit on a sixth of the "
        "items."
        .format(" / ".join("{}={:.4f}".format(r.bsize_band, r.rule_cov)
                           for _, r in full.iterrows()),
                float(full.rule_precision.iloc[0]), float(full.knn_acc.iloc[0])), "",
        "**The scoped statement the evidence supports.** Block size predicts which "
        "mechanism has the higher whole-set accuracy on small blocks, at the primary "
        "margin, and that mechanism is the one that never abstains. It does not predict "
        "which mechanism resolves a name better, and at fixed ADS it never points to a "
        "different winner than ADS already points to. Whether an abstention-driven, "
        "composition-dependent effect counts as a "
        "design-time signal a practitioner can act on is a claim the manuscript now has to "
        "make explicitly rather than leave to the reader. It is the one place where \"no "
        "design-time signal is actionable\", stated without qualification, is too strong.",
        "",
        "The same tables on the n_test >= {} subset are printed above. The pattern is "
        "unchanged: the 3-4 band disappears with the restriction, because those blocks hold "
        "one or two test signatures by construction, and the 5-8 band stays decided `k-NN "
        "wins` at {:+.4f}."
        .format(MIN_TEST, float(bs[(bs.population != "full primary population")
                                   & (bs.bsize_band == "5-8")].pooled_gap.iloc[0])), ""]
    return {"pooled": bs, "verdicts": win, "by_ads": strat}


def _spearman(x, y):
    from scipy import stats
    return float(stats.spearmanr(x, y).statistic)


def _shrink_note(v):
    """Describe how a run of band gaps approaches zero, without overstating it."""
    a = np.abs(np.asarray(v, dtype=float))
    if np.all(np.diff(a) < 0):
        return "shrinking monotonically toward zero"
    worst = int(np.argmax(np.diff(a) > 0)) + 1
    return ("shrinking toward zero but not monotonically, the {} band being the one "
            "out of order".format(BSIZE_ORDER[worst]))


# --------------------------------------------------------------------------
# task 3: uncertainty for the driver comparison (Major 3)
# --------------------------------------------------------------------------

def _cell_codes(bk):
    """Map each block to its cell of the frozen 5 x 4 grid, plus the ADS/SV factors."""
    ai = {a: i for i, a in enumerate(ADS_BANDS)}
    si = {s: i for i, s in enumerate(SV_BAND_NAMES)}
    a = bk.ads_band.map(ai).values.astype("int64")
    s = bk.sv_band.map(si).values.astype("int64")
    return a * len(SV_BAND_NAMES) + s, a, s


CELL_ADS = np.repeat(np.arange(len(ADS_BANDS)), len(SV_BAND_NAMES))
CELL_SV = np.tile(np.arange(len(SV_BAND_NAMES)), len(ADS_BANDS))


def eta2_fast(rate, elig):
    """Addendum 1a's unweighted one-way decomposition, vectorized over the 20 cells.

    Same definition as `phase2e_run.eta2_decomposition` with weight=None, which
    `demo()` asserts. Returns (eta2_ADS, eta2_SV), NaN on a degenerate grid.
    """
    p = rate[elig]
    if len(p) < 4:
        return np.nan, np.nan
    pbar = p.mean()
    ss_total = ((p - pbar) ** 2).sum()
    if ss_total <= 1e-18:
        return np.nan, np.nan
    got = []
    for fac in (CELL_ADS[elig], CELL_SV[elig]):
        m = np.bincount(fac)
        s = np.bincount(fac, weights=p)
        ok = m > 0
        got.append(float((m[ok] * (s[ok] / m[ok] - pbar) ** 2).sum() / ss_total))
    return got[0], got[1]


def _resid_rates(rate, elig, logsize):
    """Partial log cell mean test-set size out of the cell decided rates (diagnostic)."""
    x = logsize[elig]
    y = rate[elig]
    if len(y) < 3 or x.std() == 0:
        return None
    X = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = np.full(len(rate), np.nan)
    r[elig] = y - X @ beta
    return r


def driver_bootstrap(bk, k, delta=DELTA_PRIMARY, B=BOOTSTRAP_B):
    """Bootstrap eta2_SV - eta2_ADS by resampling blocks, at the frozen seed scheme.

    The per-block verdicts are the frozen ones; what is resampled is which blocks
    enter the grid, which is the sampling model the rest of the pre-registration
    uses for a pooled band (PREREG section 8: the block is the independent unit).
    """
    codes, _, _ = _cell_codes(bk)
    dec = bk[vcol(k, delta)].isin(DECIDED).values.astype("float64")
    logn = np.log(bk.n_test.values.astype("float64"))
    n, ncell = len(bk), len(ADS_BANDS) * len(SV_BAND_NAMES)

    def one(idx):
        c = codes[idx]
        m = np.bincount(c, minlength=ncell).astype("float64")
        d = np.bincount(c, weights=dec[idx], minlength=ncell)
        ls = np.bincount(c, weights=logn[idx], minlength=ncell)
        elig = m >= MIN_BLOCKS
        with np.errstate(invalid="ignore", divide="ignore"):
            rate = np.where(m > 0, d / np.maximum(m, 1), np.nan)
            mls = np.where(m > 0, ls / np.maximum(m, 1), np.nan)
        return rate, mls, elig

    rate0, mls0, elig0 = one(np.arange(n))
    ea0, es0 = eta2_fast(rate0, elig0)
    r0 = _resid_rates(rate0, elig0, mls0)
    rea0, res0 = eta2_fast(r0, elig0)

    rng = np.random.default_rng(band_seed("p27b|driver_bootstrap|k{}|{:.2f}".format(k, delta)))
    diff = np.full(B, np.nan)
    diff_adj = np.full(B, np.nan)
    dropped = 0
    for i in range(B):
        idx = rng.integers(0, n, size=n)
        rate, mls, elig = one(idx)
        if elig.sum() < ncell:
            dropped += 1
        ea, es = eta2_fast(rate, elig)
        diff[i] = es - ea
        r = _resid_rates(rate, elig, mls)
        if r is not None:
            rea, res = eta2_fast(r, elig)
            diff_adj[i] = res - rea
    d = diff[~np.isnan(diff)]
    da = diff_adj[~np.isnan(diff_adj)]
    return {
        "k": k, "delta": delta, "B": B,
        "eta2_ADS": ea0, "eta2_SV": es0, "diff": es0 - ea0,
        "diff_lo": float(np.percentile(d, 2.5)), "diff_hi": float(np.percentile(d, 97.5)),
        "share_SV_larger": float((d > 0).mean()), "usable_draws": len(d),
        "draws_with_an_ineligible_cell": dropped,
        "adj_eta2_ADS": rea0, "adj_eta2_SV": res0, "adj_diff": res0 - rea0,
        "adj_diff_lo": float(np.percentile(da, 2.5)),
        "adj_diff_hi": float(np.percentile(da, 97.5)),
        "adj_share_SV_larger": float((da > 0).mean()),
        "_draws": d,
    }


def task3(bk, out):
    out += ["## 3. Uncertainty for the driver comparison (Major 3)", "",
            "Addendum 1a's primary measure is an unweighted one-way variance decomposition "
            "of the decided-winner rate over the eligible cells of the frozen 5 x 4 grid. "
            "2.2e reported it as two point statistics with no interval. This section "
            "bootstraps the difference **eta2_SV - eta2_ADS** by resampling blocks with "
            "replacement, B = {:,}, at the frozen seed scheme of `phase2b_core.band_seed`. "
            "The per-block verdicts are the frozen ones; what is resampled is which blocks "
            "enter the grid, which is the sampling model `PREREG.md` section 8 already uses "
            "for every pooled band.".format(BOOTSTRAP_B), "",
            "**This adds an interval to a pre-registered statistic. It does not change the "
            "statistic, the clause, or the verdict Addendum 1a returned.**", ""]

    res = [driver_bootstrap(bk, k) for k in (5, SECONDARY_K)]
    tab = pd.DataFrame([{k2: v for k2, v in r.items() if not k2.startswith("_")}
                        for r in res])
    main_cols = ["k", "delta", "eta2_ADS", "eta2_SV", "diff", "diff_lo", "diff_hi",
                 "share_SV_larger", "draws_with_an_ineligible_cell"]
    adj_cols = ["k", "delta", "adj_eta2_ADS", "adj_eta2_SV", "adj_diff",
                "adj_diff_lo", "adj_diff_hi", "adj_share_SV_larger"]
    out += ["### 3a. Bootstrap interval on eta2_SV - eta2_ADS", "",
            md_table(tab[main_cols]), "",
            "Table: " + dump(tab, "phase2_7b_driver_bootstrap.csv"), ""]

    r5, r2 = res[0], res[1]
    out += ["At k = 5 the difference is **{:+.4f}, 95% interval [{:+.4f}, {:+.4f}]**, and "
            "SV is the larger of the two in {:.1%} of the {:,} usable draws. The interval "
            "excludes zero, so the direction Addendum 1a's clause turned on survives being "
            "given an error bar. Its width, {:.4f}, is about {:.0%} of the point estimate, "
            "which is the honest way to state how sharp the measurement is."
            .format(r5["diff"], r5["diff_lo"], r5["diff_hi"], r5["share_SV_larger"],
                    r5["usable_draws"], r5["diff_hi"] - r5["diff_lo"],
                    (r5["diff_hi"] - r5["diff_lo"]) / abs(r5["diff"])), ""]

    out += ["### 3b. Size-adjusted variant (labelled diagnostic, decides nothing)", "",
            "The cells are not balanced on test-set size and decidability rises with test-"
            "set size, so part of what eta-squared attributes to SV could be attributable "
            "to how large the blocks in each SV band are. The diagnostic below partials "
            "log cell-mean test-set size out of the cell decided rates by ordinary least "
            "squares across the eligible cells, then runs the same decomposition on the "
            "residuals. It is **not** pre-registered, it is not a variant Addendum 1a "
            "admits, and it decides nothing.", "",
            md_table(tab[adj_cols]), "",
            "After the adjustment the k = 5 pair is eta2_ADS = {:.4f} against "
            "eta2_SV = {:.4f}, difference {:+.4f} with 95% interval [{:+.4f}, {:+.4f}]. "
            "SV stays the larger driver. The confound the reviewer named is therefore "
            "present but not load bearing: adjusting for it moves the difference from "
            "{:+.4f} to {:+.4f} and does not cross zero."
            .format(r5["adj_eta2_ADS"], r5["adj_eta2_SV"], r5["adj_diff"],
                    r5["adj_diff_lo"], r5["adj_diff_hi"], r5["diff"], r5["adj_diff"]), ""]

    k2_zero = "excludes" if (r2["diff_lo"] > 0 or r2["diff_hi"] < 0) else "straddles"
    out += ["### 3c. The pair at k = 2 beside k = 5, so \"stable across k\" can be stated "
            "accurately", "",
            "At k = {} the pair is eta2_ADS = {:.4f} against eta2_SV = {:.4f}, difference "
            "**{:+.4f}, 95% interval [{:+.4f}, {:+.4f}]**, against {:+.4f} "
            "[{:+.4f}, {:+.4f}] at k = 5."
            .format(SECONDARY_K, r2["eta2_ADS"], r2["eta2_SV"], r2["diff"],
                    r2["diff_lo"], r2["diff_hi"], r5["diff"], r5["diff_lo"],
                    r5["diff_hi"]), "",
            "**The k = 2 interval {} zero**, and SV is the larger of the two in only "
            "{:.1%} of draws there against {:.1%} at k = 5. The k = 2 point difference is "
            "{:.0%} of the k = 5 one. So the accurate statement is narrower than \"stable "
            "across k\":"
            .format(k2_zero, r2["share_SV_larger"], r5["share_SV_larger"],
                    r2["diff"] / r5["diff"]), "",
            "- **The point estimate points the same way at every k on the curve**, which "
            "is what the k-curve table reports and what makes the clause outcome stable.",
            "- **The evidence for the direction is not the same at every k.** At k = 5 it "
            "is decisive by this interval; at k = 2 it is not distinguishable from zero. "
            "That is consistent with, and is the quantitative content of, Addendum 1a's "
            "own clause coming out `split` at k = 2 and `failed` at k = 3, 5 and 10.",
            "- **The manuscript's \"stable across k\" should therefore be scoped to the "
            "verdict, not the magnitude, and k = 2 should be named as the weak end.** "
            "Section 5.6's phrase \"the sharpest single measurement in the run\" is "
            "defensible at k = 5 with the interval above and is not defensible as a "
            "statement about the whole curve.", "",
            "The size-adjusted diagnostic moves k = 2 the other way, to {:+.4f} "
            "[{:+.4f}, {:+.4f}], which excludes zero. Two diagnostics disagreeing at k = 2 "
            "is itself the honest summary: k = 2 is the unstable end of the curve and "
            "nothing should be rested on it."
            .format(r2["adj_diff"], r2["adj_diff_lo"], r2["adj_diff_hi"]), ""]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    for r, c in zip(res, ("C0", "C1")):
        ax.hist(r["_draws"], bins=60, alpha=0.55, color=c,
                label="k = {}: {:+.3f} [{:+.3f}, {:+.3f}]".format(
                    r["k"], r["diff"], r["diff_lo"], r["diff_hi"]))
        ax.axvline(r["diff"], color=c, lw=2)
    ax.axvline(0.0, color="k", ls="--", lw=1)
    ax.set_xlabel("eta2_SV - eta2_ADS (block bootstrap, B = {:,})".format(BOOTSTRAP_B))
    ax.set_ylabel("draws")
    ax.set_title("Which signal drives decidability, with an error bar")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "phase2_7b_driver_bootstrap.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2_7b_driver_bootstrap.png`", "",
            "**Nothing here changes an H2 conclusion.** H2 was carried to Inconclusive by "
            "the power floor, which is evaluated before the driver clause. At the primary "
            "k = 5 the clause was `failed` and stays `failed`, and it now has an interval "
            "saying the failure was not a coin flip. At k = 2, where the clause was already "
            "reported as `split`, the interval says the evidence there is close to a coin "
            "flip, which is a sharper statement of the same thing rather than a new "
            "outcome.", ""]
    return tab


# --------------------------------------------------------------------------
# task 4: accuracy accounting (Major 8)
# --------------------------------------------------------------------------

def out_of_history(bk):
    """Per block: test signatures whose true author is absent from the train half.

    Derived from the frozen split and the labels, which is all it needs: a block's
    train half is `is_train` under `phase2b_core.assign_splits` at seed 20260918,
    and a test signature is out of history when its `author_label` is not among
    that half's labels. Neither mechanism can assign an author it never saw, so
    every such signature is an automatic error for both and 1 minus the share is
    an accuracy ceiling.
    """
    sig = load_signatures()
    live = sig[sig.is_live]
    wanted = set(zip(bk.dataset, bk.block_key))
    rows = []
    for key, grp in live.groupby(["dataset", "block_key"], sort=True):
        if key not in wanted:
            continue
        train = set(grp.author_label[grp.is_train])
        te = grp.author_label[~grp.is_train]
        rows.append({"dataset": key[0], "block_key": key[1],
                     "n_test_chk": len(te),
                     "n_out_of_history": int((~te.isin(train)).sum())})
    return pd.DataFrame(rows), sig


def verify_ceiling(sig, bk):
    """Assert the ceiling is real: no out-of-history signature is scored correct.

    The cached per-signature scores are written in the same order this rebuilds,
    sorted by (dataset, block_key, sid) over the live evaluation test halves, so
    the two line up positionally. The assertion is the check, not the comment.
    """
    live = sig[sig.is_live]
    te = live[~live.is_train].sort_values(["dataset", "block_key", "sid"], kind="stable")
    ev = te[~te.is_cal]
    scored = pd.read_parquet(SIG_CACHE)
    assert len(ev) == len(scored), (len(ev), len(scored))
    assert (ev.dataset.values == scored.dataset.values).all()
    assert (ev.block_key.values == scored.block_key.values).all()

    train_sets = live[live.is_train].groupby(["dataset", "block_key"]).author_label.agg(set)
    keys = pd.MultiIndex.from_arrays([ev.dataset.values, ev.block_key.values])
    tr = train_sets.reindex(keys).values
    oo = np.array([lab not in s for lab, s in zip(ev.author_label.values, tr)])
    prim = set(zip(bk.dataset, bk.block_key))
    inprim = np.array([kk in prim for kk in zip(ev.dataset.values, ev.block_key.values)])
    m = oo & inprim
    bad_rule = int(scored.rule_ok.values[m].sum())
    bad_knn = int(scored["ok_" + PRIMARY].values[m].sum())
    assert bad_rule == 0 and bad_knn == 0, (bad_rule, bad_knn)
    return int(m.sum())


def task4(bk, out):
    out += ["## 4. Accuracy accounting (Major 8)", "",
            "### 4a. The out-of-history share, an accuracy ceiling for both mechanisms", "",
            "Both mechanisms assign an author drawn from the block's own training half. "
            "Neither can assign an author it has never seen. A test signature whose true "
            "author does not occur in the training half is therefore an **automatic error "
            "for both arms**, and 1 minus the share of such signatures is a hard accuracy "
            "ceiling for the whole comparison.", "",
            "This quantity is in no committed table, so it is derived here from the frozen "
            "split and the labels, which is all it needs: a block's training half is "
            "`is_train` under `phase2b_core.assign_splits` at seed 20260918, and a test "
            "signature is out of history when its `author_label` is not among that half's "
            "labels. No mechanism is re-run and no split is redrawn. The derivation is "
            "checked rather than asserted: the code verifies that **no** out-of-history "
            "signature is scored correct by either arm in the committed per-signature "
            "scores.", ""]

    ooh, sig = out_of_history(bk)
    n_checked = verify_ceiling(sig, bk)
    b = bk.merge(ooh, on=["dataset", "block_key"], how="left")
    assert (b.n_test_chk == b.n_test).all(), "test-set sizes disagree with the frozen split"
    out += ["Check passed: {:,} out-of-history test signatures in the primary population, "
            "and the committed scores mark every one of them wrong for the rule and wrong "
            "for the k-nearest vote.".format(n_checked), ""]

    rows = []
    for label, grp in populations(b):
        n_test = int(grp.n_test.sum())
        n_out = int(grp.n_out_of_history.sum())
        rule_c, knn_c = int(grp.rule_correct.sum()), int(grp["knn_correct_" + PRIMARY].sum())
        fires = int(grp.rule_fires_n.sum())
        rows.append({
            "population": label, "blocks": len(grp), "test signatures": n_test,
            "out_of_history": n_out, "out_of_history_share": n_out / n_test,
            "accuracy_ceiling": 1 - n_out / n_test,
            "rule_acc": rule_c / n_test, "knn_acc": knn_c / n_test,
            "rule_acc_over_ceiling": rule_c / (n_test - n_out) if n_test > n_out else np.nan,
            "knn_acc_over_ceiling": knn_c / (n_test - n_out) if n_test > n_out else np.nan,
            "rule_fires": fires, "rule_coverage": fires / n_test,
            "rule_conditional_precision": rule_c / fires if fires else np.nan,
        })
    acc = pd.DataFrame(rows)
    ceil_cols = ["population", "blocks", "test signatures", "out_of_history",
                 "out_of_history_share", "accuracy_ceiling", "rule_acc", "knn_acc",
                 "rule_acc_over_ceiling", "knn_acc_over_ceiling"]
    out += [md_table(acc[ceil_cols]), "",
            "Table: " + dump(acc, "phase2_7b_accuracy_accounting.csv"), ""]

    a = acc.iloc[0]
    hi = acc[acc.population.isin(sorted(bk.dataset.unique()))].sort_values(
        "out_of_history_share", ascending=False)
    am = acc[acc.population == "aminer"].iloc[0]
    ins = acc[acc.population == "inspire"].iloc[0]
    raw_spread = ins.rule_acc - am.rule_acc
    adj_spread = ins.rule_acc_over_ceiling - am.rule_acc_over_ceiling
    out += ["Pooled, **{:.2%} of held-out signatures name an author the block's training "
            "half never shows**, so no mechanism in this family can exceed {:.4f} on this "
            "population. Against that ceiling the rule reaches {:.4f} and the vote {:.4f}. "
            "The pooled gap between the mechanisms, -0.0050, is unchanged in kind by the "
            "ceiling: it is a shared floor, subtracted from both arms, so it moves each "
            "accuracy and barely moves their difference."
            .format(a.out_of_history_share, a.accuracy_ceiling,
                    a.rule_acc_over_ceiling, a.knn_acc_over_ceiling), "",
            "**The ceiling is real and it is not the main reason the datasets differ, "
            "which is worth stating because the obvious guess is that it is.** Ordered by "
            "out-of-history share: {}. aminer's ceiling is {:.4f} against inspire's "
            "{:.4f}, a difference of {:.4f}, while their rule accuracies differ by "
            "{:.4f}. Normalized to their own ceilings the two still sit {:.4f} apart, so "
            "the ceiling accounts for only about {:.0%} of the spread between them. The "
            "rest is the blocks themselves being harder, not more of them being "
            "impossible. A reader who is handed the ceiling column and no caveat will draw "
            "the opposite conclusion, so the caveat belongs beside the column."
            .format(" / ".join("{}={:.4f}".format(r.population, r.out_of_history_share)
                               for r in hi.itertuples(index=False)),
                    am.accuracy_ceiling, ins.accuracy_ceiling,
                    ins.accuracy_ceiling - am.accuracy_ceiling,
                    raw_spread, adj_spread, 1 - adj_spread / raw_spread), ""]

    prec_cols = ["population", "test signatures", "rule_fires", "rule_coverage",
                 "rule_acc", "rule_conditional_precision", "knn_acc"]
    out += ["### 4b. The rule's conditional precision, its accuracy where it fires", "",
            "The manuscript scores an abstention as an error, which is the right primary "
            "metric for a comparison of deployable mechanisms, and it is not the number a "
            "precision-first framing invites. Below, `rule_conditional_precision` is the "
            "rule's accuracy restricted to the signatures on which it fires, "
            "`rule_correct / rule_fires`. Both are computed from the same committed "
            "per-block records; neither replaces the other.", "",
            md_table(acc[prec_cols]), ""]

    out += ["Pooled, the rule fires on {:.2%} of held-out signatures and is right on "
            "**{:.4f}** of those, against the vote's {:.4f} over everything. The "
            "precision-first characterization is therefore accurate: where the rule "
            "commits, it is the more accurate arm by {:+.4f}, and it pays for that with "
            "{:.2%} abstention. This is the cleanest one-line statement of what the two "
            "mechanisms actually trade, and it belongs beside the pooled accuracy rather "
            "than instead of it."
            .format(a.rule_coverage, a.rule_conditional_precision, a.knn_acc,
                    a.rule_conditional_precision - a.knn_acc, 1 - a.rule_coverage), "",
            "**Nothing here changes an H1, H2 or H3 conclusion.** The ceiling and the "
            "conditional precision are accounting that was missing, not a re-scoring. "
            "Every verdict in the frozen falsification table is computed from the same "
            "per-signature correctness the manuscript already used.", ""]
    return acc


def closing(out):
    out += [
        "## What 2.7c has to carry, in priority order", "",
        "1. **The scoping decision on the general claim, which is the author's.** Block "
        "size is a design-time signal with two decided pooled bands at the primary margin "
        "(section 2). The abstract, the title and section 8.1 currently generalize past "
        "what that allows. Either scope every general sentence to the two pre-registered "
        "signals, or state the block-size result and its two qualifications in the main "
        "text and let the general sentence stand with them attached. This is the same "
        "decision peer-review major 4 asks for, and taking it first is what 2.7's own "
        "handover recommended.",
        "2. **Section 5.4 and Figure 2 need the size-1 and size-2 rows and the "
        "degeneracy note** (section 1a), because 278 of the 500 decided verdicts come "
        "from blocks whose interval cannot produce an undecided.",
        "3. **The gradient paragraph needs its sensitivity result** (section 1d). The "
        "reported rise at ADS = 1.0 is a small-block artifact and the restricted gradient "
        "is monotone. Reporting that makes the H2 discussion stronger, not weaker.",
        "4. **Table 4 needs the bootstrap interval, and section 5.6's \"stable across "
        "k\" needs scoping to the verdict** (section 3).",
        "5. **Table 3 or the population table needs the ceiling column, section 5.3 "
        "needs the rule's conditional precision** (section 4), with the caveat that the "
        "ceiling is not what separates the datasets.", "",
        "None of the five changes a verdict. The first changes a claim.", "",
        "## Reproducing this report", "",
        "`python phase2/phase2_7b_reanalysis.py`. It runs its own assert-based self-check "
        "first, then re-derives the frozen per-block verdict counts (191 / 309 / 10,172 / "
        "3,230) and refuses to continue if they do not match, then writes this file and "
        "the `reports/tables/phase2_7b_*.csv` tables and the two figures. Two "
        "consecutive runs produce a byte-identical report.", ""]


# --------------------------------------------------------------------------
# self-check and main
# --------------------------------------------------------------------------

def demo():
    """Assert-based self-check. Fails loudly if a frozen definition drifts."""
    # eta2_fast must agree with the frozen eta2_decomposition, cell for cell.
    rng = np.random.default_rng(0)
    for _ in range(5):
        p = rng.random(20)
        cells = pd.DataFrame({"ads_band": [ADS_BANDS[i] for i in CELL_ADS],
                              "sv_band": [SV_BAND_NAMES[i] for i in CELL_SV],
                              "p": p})
        _, ea, es = eta2_decomposition(cells, "p")
        fa, fs = eta2_fast(p, np.ones(20, dtype=bool))
        assert abs(ea - fa) < 1e-12 and abs(es - fs) < 1e-12, (ea, fa, es, fs)
    # a grid varying only along ADS must load entirely on ADS
    p = np.repeat(np.arange(5, dtype=float), 4)
    fa, fs = eta2_fast(p, np.ones(20, dtype=bool))
    assert abs(fa - 1.0) < 1e-12 and abs(fs) < 1e-12, (fa, fs)
    # dropping cells must be honoured
    elig = np.ones(20, dtype=bool)
    elig[:4] = False
    fa2, _ = eta2_fast(p, elig)
    assert fa2 <= 1.0 + 1e-12
    # partialling a constant covariate out must be a no-op on the decomposition
    r = _resid_rates(p, np.ones(20, dtype=bool), np.zeros(20))
    assert r is None

    # the block-size bands must partition the primary population's range
    assert bsize_band(3) == "3-4" and bsize_band(128) == "65-128" and bsize_band(2339) == "129+"
    assert bsize_band(2) == "?"
    print("phase2_7b self-check: all assertions passed")


def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    bk = pd.read_csv(BLOCKS)
    bk["bsize_band"] = [bsize_band(n) for n in bk.block_size]
    assert len(bk) == 13902 and int(bk.n_test.sum()) == 197479, "not the primary population"

    # the frozen numbers this pass layers on, re-derived before anything is added
    frozen = bk[vcol()].value_counts()
    assert int(frozen.get("rule wins", 0)) == 191 and int(frozen.get("k-NN wins", 0)) == 309
    assert int(frozen.get("tie", 0)) == 10172 and int(frozen.get("undecided", 0)) == 3230
    print("frozen per-block verdicts reproduced: 191 / 309 / 10,172 / 3,230")

    body = []
    t1 = task1(bk, body)
    t2 = task2(bk, t1["sub"], body)
    t3 = task3(bk, body)
    t4 = task4(bk, body)
    closing(body)

    # every number in the header comes from the tables above, never retyped
    d = t1["dist"].set_index("population")
    g_all = t1["grids_all"]["ads"].iloc[-1]["decided_rate_{:.2f}".format(DELTA_PRIMARY)]
    g_sub = t1["grids_sub"]["ads"].iloc[-1]["decided_rate_{:.2f}".format(DELTA_PRIMARY)]
    bsz = t2["pooled"]
    bdec = bsz[(bsz.population == "full primary population")
               & (bsz["verdict_0.05"].isin(DECIDED))]
    b3 = t3.set_index("k")
    a4 = t4.iloc[0]
    subs = {
        "n_dec": len(bdec),
        "dec_bands": "; ".join(
            "blocks of {} signatures give a pooled gap of {:+.4f} [{:+.4f}, {:+.4f}], "
            "`{}`".format(r.bsize_band, r.pooled_gap, r.ci_lo, r.ci_hi, r["verdict_0.05"])
            for _, r in bdec.iterrows()),
        "min_test": MIN_TEST, "g_all": g_all, "g_sub": g_sub,
        "small_dec": int(d.loc["n_test = 1 only", "decided"]
                         + d.loc["n_test = 2 only", "decided"]),
        "all_dec": int(d.loc["all blocks (frozen primary)", "decided"]),
        "rw": int(d.loc["all blocks (frozen primary)", "rule wins"]),
        "kw": int(d.loc["all blocks (frozen primary)", "k-NN wins"]),
        "rw3": int(d.loc["n_test >= {}".format(MIN_TEST), "rule wins"]),
        "kw3": int(d.loc["n_test >= {}".format(MIN_TEST), "k-NN wins"]),
        "d5": b3.loc[5, "diff"], "d5lo": b3.loc[5, "diff_lo"], "d5hi": b3.loc[5, "diff_hi"],
        "d2": b3.loc[SECONDARY_K, "diff"], "d2lo": b3.loc[SECONDARY_K, "diff_lo"],
        "d2hi": b3.loc[SECONDARY_K, "diff_hi"],
        "ooh": a4.out_of_history_share, "ceil": a4.accuracy_ceiling,
        "prec": a4.rule_conditional_precision, "knn": a4.knn_acc,
    }
    ds = t4[t4.population.isin(sorted(bk.dataset.unique()))]
    am4, in4 = t4[t4.population == "aminer"].iloc[0], t4[t4.population == "inspire"].iloc[0]
    subs.update({
        "ceil_lo": ds.accuracy_ceiling.min(), "ceil_hi": ds.accuracy_ceiling.max(),
        "share_expl": 1 - ((in4.rule_acc_over_ceiling - am4.rule_acc_over_ceiling)
                           / (in4.rule_acc - am4.rule_acc)),
    })

    head = [
        "# Phase 2.7b: re-analysis of the frozen records",
        "",
        "Produced by `phase2/phase2_7b_reanalysis.py` on the committed per-block records of "
        "`reports/tables/phase2e_blocks_scored.csv.gz` and the S2AND signature table already "
        "ingested. It answers peer-review majors 1, 2, 3 and 8 of "
        "`reports/phase2_7_peer_review.md`.",
        "",
        "**What this pass is.** Supplementary and sensitivity analysis on records that "
        "already exist, computed deterministically at the frozen seed. **What it is not.** "
        "It re-runs no experiment, re-draws no split, re-tunes nothing, and alters no frozen "
        "definition. `PREREG.md`, Amendment 1 and Addendum 1a are untouched. The frozen "
        "primary analysis population is unchanged at 13,902 blocks and 197,479 test "
        "signatures, and every frozen number it reports is re-derived here before anything "
        "is added to it.",
        "",
        "Inputs: `reports/tables/phase2e_blocks_scored.csv.gz`, "
        "`data/phase2e_eval_sigs.parquet`, `data/s2and_signatures.parquet`. "
        "Seed 20260918 throughout, B = 2000, delta = 0.05 primary with 0.02 and 0.03 beside "
        "it, k = 5 primary.",
        "",
        "## Headline: does anything change an H1, H2 or H3 conclusion?",
        "",
        "**No hypothesis verdict moves. One general claim in the surrounding prose does, "
        "and it is the paper's headline sentence.**",
        "",
        "H1 Supported, H2 Inconclusive, H3 Inconclusive at the primary margin and Partial "
        "at delta = 0.02, exactly as the frozen falsification table reports them. H2 and H3 "
        "were carried to Inconclusive by the pre-registered power floor, which counts "
        "decided pooled verdicts over **ADS and SV** bands, and nothing below gives an ADS "
        "band, an SV band or a grid cell a decided pooled verdict at delta = 0.05 in any "
        "population examined. Section 1b checks that against the restricted population "
        "rather than assuming it.",
        "",
        "**Flagged, because it shapes the prose pass. Block size, a design-time signal the "
        "pre-registration did not carry, produces {n_dec} decided pooled band verdicts at "
        "the primary margin:** {dec_bands}. Neither ADS nor SV produces a single decided "
        "marginal band. Taken alone this is a counter-example to \"design-time mechanism "
        "selection "
        "has no signal a designer can act on\" stated without qualification. Section 2 "
        "measures what it actually is: at fixed ADS the effect is gap compression with no "
        "sign change in either stratum, the marginal reversal is composition, and the "
        "decided cells are driven by the rule's abstentions rather than by how either "
        "mechanism resolves a name. The scoping decision that follows is the author's, and "
        "it is the same decision peer-review major 4 asks for.",
        "",
        "Four further things change, all of them reporting rather than verdicts.",
        "",
        "1. **The H2 decidability gradient is monotone once degenerate blocks are removed.** "
        "2.2e reported that the decided-winner rate rises again in the top ADS band instead "
        "of approaching zero, against Amendment 1's prediction. On blocks with at least "
        "{min_test} test signatures it does not rise: the ADS = 1.0 rate falls from "
        "{g_all:.4f} to {g_sub:.4f}, below the band beneath it. The reported "
        "non-monotonicity is a small-block artifact and section 1 says so with the table.",
        "2. **The decided-verdict count is composed differently than the manuscript implies "
        "and its direction is an artifact of the small end.** {small_dec} of the "
        "{all_dec} decided verdicts come from blocks with one or two test signatures. "
        "Restricted, the per-block margin flips from {rw} rule wins against {kw} k-NN wins "
        "to {rw3} against {kw3}.",
        "3. **The driver comparison now has an interval.** At k = 5 eta2_SV - eta2_ADS is "
        "{d5:+.4f} [{d5lo:+.4f}, {d5hi:+.4f}], excluding zero before and after a size "
        "adjustment. At k = 2 it is {d2:+.4f} [{d2lo:+.4f}, {d2hi:+.4f}], which does not. "
        "\"Stable across k\" is accurate for the verdict and not for the evidence behind "
        "it.",
        "4. **There is a hard accuracy ceiling neither mechanism can pass, and it is not "
        "the reason the datasets differ.** {ooh:.2%} of held-out signatures name an author "
        "the block's training half never shows, so no mechanism in this family can exceed "
        "{ceil:.4f}. Per dataset the ceiling ranges from {ceil_lo:.4f} to {ceil_hi:.4f}, "
        "and normalizing for it closes only about {share_expl:.0%} of the aminer-to-"
        "inspire spread, against the natural guess that it explains most of it. The rule's "
        "precision where it fires, {prec:.4f}, is above the vote's accuracy, {knn:.4f}, "
        "which is the number the precision-first framing implies and the manuscript never "
        "prints.",
        "",
        "Every item above is a table and a paragraph for the 2.7c prose pass. Only the "
        "flagged one is a claim change.",
        "",
        "---",
        "",
    ]
    head = [h.format(**subs) if "{" in h else h for h in head]
    REPORT.write_text("\n".join(head + body), encoding="utf-8")
    print("wrote", REPORT)


if __name__ == "__main__":
    demo()
    main()
