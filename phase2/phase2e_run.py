"""Phase 2.2e: the amended boundary experiment on the evaluation split.

Executes `phase2/PREREG.md` as amended by **Amendment 1** and **Addendum 1a**,
frozen at Phase 2.2d before any number in this file existed. Nothing here is
calibrated, re-banded or redefined: the split, the ADS bands, the SV and
SV_resid band edges, the margins, the seeds and the four-verdict rule all carry
over from the 2.2a freeze and `phase2b_constants.py`; k is fixed by definition
at 5 and section 7 is void.

Mechanism A is the exact-evidence rule, unchanged. Mechanism B is the k-nearest
vote of `phase2e_mech.py`, whose regression check reproduces the 2.2c
calibration-split two-sidedness counts before this file may be run.

What it produces, in PREREG order:

- section 3         population accounting and the named exclusions
- section 10 / H1   the ADS-to-accuracy validity check, both mechanisms
- section 8         per-block four-verdict distribution and pooled band verdict,
                    delta 0.05 primary with the 0.02 / 0.03 robustness curve
- Amendment 1       the k in {2, 3, 5, 10} sensitivity curve, mandatory
- section 9         the 5 x 4 ADS-by-SV grid, the three structural outcomes,
                    SV_resid, INIT and the Jaro-Winkler arm
- Addendum 1a       the decidability gradient, the eta-squared variance
                    decomposition and the averaged-range test
- section 11        per dataset, inspire alone, pooled non-inspire
- section 10        the amended falsification table, evaluated

Run: python phase2/phase2e_run.py
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
    ADS_BANDS, BLOCKS_CACHE, DELTAS, DELTA_PRIMARY, INIT_BANDS, MIN_BLOCKS,
    MIN_DATASET_BLOCKS, SEED, SV_BAND_NAMES, ads_band, band_seed,
    block_bootstrap_ci, init_band, ols_robust, pooled_block_ci,
    spearman_block_ci, sv_band, verdict,
)
from phase2b_build import load_signatures  # noqa: E402
from phase2b_constants import SV_BAND_EDGES, SV_RESID_BAND_EDGES  # noqa: E402
from phase2b_run import dump, md_table, populations, size_bin, verify_no_leakage  # noqa: E402
from phase2e_mech import ARMS, KS, K_PRIMARY, block_predictions  # noqa: E402

SIG_CACHE = HERE / "data" / "phase2e_eval_sigs.parquet"
FIGS = HERE / "reports" / "figs"
TABLES = HERE / "reports" / "tables"
REPORT = HERE / "reports" / "phase2e_boundary.md"

# Amendment 1, section 8: the renames are cosmetic, the rule is unchanged.
RENAME = {"exact wins": "rule wins", "fuzzy wins": "k-NN wins"}
VERDICTS = ("rule wins", "k-NN wins", "tie", "undecided")
DECIDED = ("rule wins", "k-NN wins")
PRIMARY = "levenshtein_k5"
COMBOS = [("levenshtein", k) for k in KS] + [("jarowinkler", K_PRIMARY)]
SIZE_BINS = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 16), (17, 32), (33, 64), (65, 10 ** 9)]
ADS_BELOW_ONE = ADS_BANDS[:-1]
# Addendum 1a's degenerate case is "SS_total is zero". Decided-winner rates are
# rationals over block counts, so a real between-cell difference is at least
# 1/n_blocks and contributes at least ~1e-8 to SS_total; anything below this is
# floating-point noise around an exactly flat grid, not a signal.
SS_EPS = 1e-18


def combo(arm, k):
    return "{}_k{}".format(arm, k)


def vrd(lo, hi, delta):
    """PREREG section 8's four verdicts under the Amendment 1 names."""
    return RENAME.get(verdict(lo, hi, delta), verdict(lo, hi, delta))


# --------------------------------------------------------------------------
# 1. mechanisms on the evaluation split
# --------------------------------------------------------------------------

def mechanism_pass(sig, blocks):
    """Both mechanisms over every evaluation block, both metric arms, every k."""
    if SIG_CACHE.exists():
        print("reusing {}".format(SIG_CACHE.name))
        return pd.read_parquet(SIG_CACHE)
    wanted = set(zip(blocks.dataset, blocks.block_key))
    live = sig[sig.is_live]
    out, n = [], 0
    for (dataset, block_key), grp in live.groupby(["dataset", "block_key"], sort=True):
        if (dataset, block_key) not in wanted:
            continue
        tr, te = grp[grp.is_train], grp[~grp.is_train]
        tf, tl = tr.surface_form.tolist(), tr.author_label.tolist()
        forms, truth = te.surface_form.tolist(), te.author_label.values
        rec = {"dataset": dataset, "block_key": block_key,
               "block_index": te.block_index.values}
        for arm, simfunc in ARMS.items():
            preds = block_predictions(tf, tl, forms, ks=KS, simfunc=simfunc)
            if arm == "levenshtein":
                rule = preds["rule"]
                rec["rule_fires"] = np.array([p is not None for p in rule])
                rec["rule_ok"] = np.array([p is not None and p == t
                                           for p, t in zip(rule, truth)])
            for k in KS:
                c = combo(arm, k)
                rec["ok_" + c] = np.array([p == t for p, t in zip(preds[k], truth)])
                # identical predictions; B never abstains, so A abstaining is a
                # disagreement by definition (PREREG section 4 agreement rate).
                rec["agree_" + c] = np.array([p is not None and p == q
                                              for p, q in zip(preds["rule"], preds[k])])
        out.append(pd.DataFrame(rec))
        n += 1
        if n % 2000 == 0:
            print("  {:,} blocks".format(n))
    res = pd.concat(out, ignore_index=True)
    res.to_parquet(SIG_CACHE, index=False)
    print("wrote {}  ({:,} test signatures)".format(SIG_CACHE.name, len(res)))
    return res


def score_blocks(res, blocks):
    """Collapse the signature table to one row per block, for every combo."""
    res = res.copy()
    for arm, k in COMBOS:
        c = combo(arm, k)
        res["g_" + c] = res.rule_ok.astype("int8") - res["ok_" + c].astype("int8")

    agg = {"n_test": ("rule_ok", "size"),
           "rule_correct": ("rule_ok", "sum"),
           "rule_fires_n": ("rule_fires", "sum")}
    for arm, k in COMBOS:
        c = combo(arm, k)
        agg["knn_correct_" + c] = ("ok_" + c, "sum")
        agg["agree_n_" + c] = ("agree_" + c, "sum")
        agg["n_plus_" + c] = ("g_" + c, lambda s: int((s == 1).sum()))
        agg["n_minus_" + c] = ("g_" + c, lambda s: int((s == -1).sum()))
    bk = res.groupby(["dataset", "block_key"], sort=True).agg(**agg).reset_index()
    bk = bk.merge(blocks.drop(columns=["n_test"]), on=["dataset", "block_key"], how="inner")

    bk["rule_acc"] = bk.rule_correct / bk.n_test
    bk["rule_cov"] = bk.rule_fires_n / bk.n_test
    for arm, k in COMBOS:
        c = combo(arm, k)
        bk["knn_acc_" + c] = bk["knn_correct_" + c] / bk.n_test
        bk["agree_rate_" + c] = bk["agree_n_" + c] / bk.n_test
        bk["net_" + c] = bk.rule_correct - bk["knn_correct_" + c]
        bk["gap_" + c] = bk["net_" + c] / bk.n_test
        bk["n_zero_" + c] = bk.n_test - bk["n_plus_" + c] - bk["n_minus_" + c]
    return bk


def block_verdicts(bk):
    """PREREG section 8: paired per-block bootstrap, seed 20260918 + block index."""
    for arm, k in COMBOS:
        c = combo(arm, k)
        los, his = [], []
        for r in bk.itertuples(index=False):
            lo, hi = block_bootstrap_ci(getattr(r, "n_plus_" + c),
                                        getattr(r, "n_zero_" + c),
                                        getattr(r, "n_minus_" + c),
                                        seed=SEED + int(r.block_index))
            los.append(lo)
            his.append(hi)
        bk["ci_lo_" + c] = los
        bk["ci_hi_" + c] = his
        for d in DELTAS:
            bk["bverdict_{}_{:.2f}".format(c, d)] = [vrd(lo, hi, d) for lo, hi in zip(los, his)]
    return bk


# --------------------------------------------------------------------------
# 2. pooled band verdicts and the decided-winner rate
# --------------------------------------------------------------------------

def pooled_table(bk, keys, c, tag):
    """PREREG section 8 pooled verdict per group, resampling blocks not signatures.

    Also carries the per-block verdict distribution, whose `rule wins` plus
    `k-NN wins` share is the decided-winner rate Amendment 1 resolution 4 uses.
    """
    rows = []
    for gkey, grp in bk.groupby(keys, sort=False, dropna=False):
        gkey = gkey if isinstance(gkey, tuple) else (gkey,)
        if any(g is None or (isinstance(g, float) and np.isnan(g)) for g in gkey):
            continue
        label = tag + "|" + "|".join(str(g) for g in gkey)
        pt, lo, hi = pooled_block_ci(grp["net_" + c].values, grp.n_test.values,
                                     seed=band_seed(label))
        row = dict(zip(keys, gkey))
        row.update({
            "n_blocks": len(grp),
            "n_test": int(grp.n_test.sum()),
            "pooled_gap": pt, "ci_lo": lo, "ci_hi": hi,
            "mean_block_gap": float(grp["gap_" + c].mean()),
            "median_block_gap": float(grp["gap_" + c].median()),
            "rule_acc": float(grp.rule_correct.sum() / grp.n_test.sum()),
            "knn_acc": float(grp["knn_correct_" + c].sum() / grp.n_test.sum()),
            "rule_cov": float(grp.rule_fires_n.sum() / grp.n_test.sum()),
            "knn_cov": 1.0,
            "agreement": float(grp["agree_n_" + c].sum() / grp.n_test.sum()),
            "under_powered": len(grp) < MIN_BLOCKS,
        })
        for d in DELTAS:
            row["verdict_{:.2f}".format(d)] = vrd(lo, hi, d)
            col = grp["bverdict_{}_{:.2f}".format(c, d)]
            counts = col.value_counts()
            n_dec = int(sum(counts.get(v, 0) for v in DECIDED))
            row["n_decided_{:.2f}".format(d)] = n_dec
            row["decided_rate_{:.2f}".format(d)] = n_dec / len(grp)
            for v in VERDICTS:
                row["share_{}_{:.2f}".format(v.replace(" ", "_").replace("-", ""), d)] = \
                    float(counts.get(v, 0) / len(grp))
        rows.append(row)
    return pd.DataFrame(rows)


def order_bands(t, col, order):
    present = [o for o in order if o in set(t[col])]
    return t.set_index(col).reindex(present).reset_index()


def sort_cells(t, svcol="sv_band"):
    return t.sort_values(
        ["ads_band", svcol],
        key=lambda s: s.map({v: i for i, v in enumerate(
            ADS_BANDS if s.name == "ads_band" else SV_BAND_NAMES)})).reset_index(drop=True)


# --------------------------------------------------------------------------
# 3. the three structural outcomes (PREREG section 9)
# --------------------------------------------------------------------------

def structural(cells, fixed, vary, order, delta):
    """At each level of `fixed`, classify what happens across `vary`.

    Winner reversal, tie-crossing, or gap compression only. The gate is two
    eligible bands; whether two of them are *decided* is tracked separately
    because that is the section 10 power floor, which the Order of evaluation
    rule makes a hypothesis-level test.
    """
    col = "verdict_{:.2f}".format(delta)
    levels = [lv for lv in (ADS_BANDS if fixed == "ads_band" else
                            INIT_BANDS if fixed == "init_band" else SV_BAND_NAMES)
              if lv in set(cells[fixed])]
    rows = []
    for lvl in levels:
        grp = cells[cells[fixed] == lvl]
        elig = grp[~grp.under_powered]
        elig = elig.set_index(vary).reindex([o for o in order if o in set(elig[vary])])
        verdicts = elig[col].tolist()
        decided = [v for v in verdicts if v in DECIDED]
        if len(elig) < 2:
            outcome = "not eligible"
        elif len(set(decided)) > 1:
            outcome = "winner reversal"
        elif decided and "tie" in verdicts:
            outcome = "tie-crossing"
        else:
            outcome = "gap compression only"
        rows.append({fixed: lvl, "eligible_bands": len(elig), "decided_bands": len(decided),
                     "verdicts": " / ".join("{}={}".format(i, v)
                                            for i, v in zip(elig.index, verdicts)),
                     "outcome": outcome})
    # explicit columns for the same reason as in `gradient_clauses`: a population
    # can have no level of `fixed` at all, and callers still read the columns
    return pd.DataFrame(rows, columns=[fixed, "eligible_bands", "decided_bands",
                                       "verdicts", "outcome"])


# --------------------------------------------------------------------------
# 4. Addendum 1a: the decidability drivers
# --------------------------------------------------------------------------

def eta2_decomposition(cells, value, weight=None):
    """Addendum 1a one-way variance decomposition over the eligible cells.

    `cells` is already restricted to eligible cells. With `weight=None` each
    cell is one observation and `m_b` is the number of eligible cells in band
    b, which is the addendum's primary, unweighted measure. Passing
    `weight="n_blocks"` gives the block-weighted diagnostic, which decides
    nothing.

    Returns (ss_total, eta2_ADS, eta2_SV), with the eta-squareds NaN when
    ss_total is zero, which the addendum calls a degenerate case.
    """
    w = np.ones(len(cells)) if weight is None else cells[weight].values.astype(float)
    p = cells[value].values.astype(float)
    pbar = float(np.average(p, weights=w))
    ss_total = float((w * (p - pbar) ** 2).sum())
    ss = {}
    for factor in ("ads_band", "sv_band"):
        total = 0.0
        for _, g in cells.groupby(factor):
            gw = np.ones(len(g)) if weight is None else g[weight].values.astype(float)
            total += gw.sum() * (float(np.average(g[value].values.astype(float),
                                                  weights=gw)) - pbar) ** 2
        ss[factor] = total
    if ss_total <= SS_EPS:
        return ss_total, float("nan"), float("nan")
    return ss_total, ss["ads_band"] / ss_total, ss["sv_band"] / ss_total


def averaged_range(cells, fixed, vary, marginal, value):
    """Resolution 5, kept verbatim as Addendum 1a's second required condition.

    For each `fixed` band with 30 or more blocks, the range of the
    decided-winner rate across its eligible `vary` cells, averaged over bands.
    """
    ok = set(marginal[~marginal.under_powered][fixed])
    ranges, detail = [], []
    for lvl, g in cells.groupby(fixed):
        if lvl not in ok or not len(g):
            continue
        v = g[value].values.astype(float)
        ranges.append(float(v.max() - v.min()))
        detail.append({fixed: lvl, "eligible_cells": len(g), "range": ranges[-1]})
    return (float(np.mean(ranges)) if ranges else float("nan"),
            pd.DataFrame(detail), len(ranges))


def gradient_clauses(cells, ads_marg, sv_marg, delta):
    """The H2 gradient clauses of the amended section 10, computed not judged."""
    col = "decided_rate_{:.2f}".format(delta)
    elig = cells[~cells.under_powered]
    sv_ok = [s for s in SV_BAND_NAMES if s in set(sv_marg[~sv_marg.under_powered].sv_band)]
    rows = []
    for s in sv_ok:
        g = order_bands(elig[elig.sv_band == s], "ads_band", ADS_BANDS)
        if len(g) < 2:
            rows.append({"sv_band": s, "eligible_ADS_cells": len(g), "non_increasing": None,
                         "top_below_bottom": None, "rates": ""})
            continue
        v = g[col].values
        rows.append({
            "sv_band": s, "eligible_ADS_cells": len(g),
            "non_increasing": bool(np.all(np.diff(v) <= 1e-12)),
            "top_below_bottom": bool(v[-1] < v[0] - 1e-12),
            "rates": " / ".join("{}={:.4f}".format(a, x) for a, x in zip(g.ads_band, v)),
        })
    # explicit columns: a population with no eligible SV band yields no rows,
    # and an empty frame with no columns breaks every access below
    per_sv = pd.DataFrame(rows, columns=["sv_band", "eligible_ADS_cells",
                                         "non_increasing", "top_below_bottom", "rates"])
    usable = per_sv[per_sv.non_increasing.notna()]
    am = order_bands(ads_marg[~ads_marg.under_powered], "ads_band", ADS_BANDS)
    marg_top_below_bottom = (bool(am[col].values[-1] < am[col].values[0] - 1e-12)
                             if len(am) >= 2 else None)
    return {
        "per_sv": per_sv,
        "usable_sv_bands": len(usable),
        "non_increasing_majority": bool(len(usable) and
                                        usable.non_increasing.sum() > len(usable) / 2),
        "top_below_bottom_majority": bool(len(usable) and
                                          usable.top_below_bottom.sum() > len(usable) / 2),
        "marginal_rates": am[["ads_band", "n_blocks", col]],
        "marginal_top_below_bottom": marg_top_below_bottom,
    }


def decidable_region(cells_or_marg, delta):
    """Resolution 6: an ADS band below 1.0 with 30+ blocks and 30+ decided verdicts."""
    t = cells_or_marg
    hit = t[(t.ads_band.isin(ADS_BELOW_ONE)) & (~t.under_powered)
            & (t["n_decided_{:.2f}".format(delta)] >= MIN_BLOCKS)]
    return list(hit.ads_band), bool(len(hit))


def driver_comparison(cells, ads_marg, sv_marg, delta, label):
    """Addendum 1a: both required measures plus the block-weighted diagnostic."""
    col = "decided_rate_{:.2f}".format(delta)
    elig = cells[~cells.under_powered].copy()
    n_ads_levels = elig.ads_band.nunique()
    n_sv_levels = elig.sv_band.nunique()
    ss_total, e_ads, e_sv = eta2_decomposition(elig, col)
    _, w_ads, w_sv = eta2_decomposition(elig, col, weight="n_blocks")
    r_ads, d_ads, n_ads_bands = averaged_range(elig, "sv_band", "ads_band", sv_marg, col)
    r_sv, d_sv, n_sv_bands = averaged_range(elig, "ads_band", "sv_band", ads_marg, col)
    degenerate = (len(elig) < 4 or n_ads_levels < 2 or n_sv_levels < 2
                  or ss_total <= SS_EPS or np.isnan(e_ads))
    if degenerate:
        clause = "Inconclusive"
    elif e_ads > e_sv and r_ads > r_sv:
        clause = "met"
    elif e_ads > e_sv or r_ads > r_sv:
        clause = "split"          # Partial, never Supported
    else:
        clause = "failed"
    return {
        "label": label, "delta": delta, "eligible_cells": len(elig),
        "ADS levels": n_ads_levels, "SV levels": n_sv_levels,
        "SS_total": ss_total, "eta2_ADS": e_ads, "eta2_SV": e_sv,
        "eta2_ADS_blockweighted": w_ads, "eta2_SV_blockweighted": w_sv,
        "avg_range_ADS": r_ads, "avg_range_SV": r_sv,
        "range_bands_ADS": n_ads_bands, "range_bands_SV": n_sv_bands,
        "clause": clause, "_detail_ads": d_ads, "_detail_sv": d_sv,
    }


def demo():
    """Assert-based self-check for the quantities this module introduces."""
    # eta-squared: variation purely along ADS must give eta2_ADS = 1, eta2_SV = 0
    grid = pd.DataFrame([{"ads_band": a, "sv_band": s, "p": i / 4, "n_blocks": 50}
                         for i, a in enumerate(ADS_BANDS) for s in SV_BAND_NAMES])
    ss, ea, es = eta2_decomposition(grid, "p")
    assert abs(ea - 1.0) < 1e-12 and abs(es) < 1e-12, (ea, es)
    # ... and purely along SV, the other way round
    grid2 = grid.copy()
    grid2["p"] = [SV_BAND_NAMES.index(s) / 3 for s in grid2.sv_band]
    _, ea2, es2 = eta2_decomposition(grid2, "p")
    assert abs(es2 - 1.0) < 1e-12 and abs(ea2) < 1e-12, (ea2, es2)
    # the measure is invariant to band count, which is why it replaced the range
    half = grid[grid.sv_band.isin(SV_BAND_NAMES[:2])]
    _, ea3, es3 = eta2_decomposition(half, "p")
    assert abs(ea3 - 1.0) < 1e-12 and abs(es3) < 1e-12, (ea3, es3)
    # a flat grid is the degenerate case: SS_total = 0, ratios undefined
    flat = grid.copy()
    flat["p"] = 0.3
    ss0, ea0, es0 = eta2_decomposition(flat, "p")
    assert ss0 <= SS_EPS and np.isnan(ea0) and np.isnan(es0), (ss0, ea0, es0)
    # ... but a genuine one-block difference in a 10,000-block cell is not noise
    almost = grid.copy()
    almost["p"] = 0.3
    almost.loc[almost.index[0], "p"] = 0.3 + 1e-4
    ss1, ea1, _ = eta2_decomposition(almost, "p")
    assert ss1 > SS_EPS and not np.isnan(ea1), (ss1, ea1)
    # block weighting really does weight: on a grid that varies along both axes,
    # making one row heavy changes the answer, which is why Addendum 1a unweights.
    mix = grid.copy()
    mix["p"] = [ADS_BANDS.index(a) / 4 + SV_BAND_NAMES.index(s) / 6
                for a, s in zip(mix.ads_band, mix.sv_band)]
    _, ua, us = eta2_decomposition(mix, "p")
    wmix = mix.copy()
    wmix.loc[wmix.ads_band == ADS_BANDS[-1], "n_blocks"] = 100000
    _, wa, ws = eta2_decomposition(wmix, "p", weight="n_blocks")
    assert abs(ua - wa) > 1e-6 or abs(us - ws) > 1e-6, (ua, us, wa, ws)

    # averaged range, against a hand-computed answer
    cells = pd.DataFrame([
        {"ads_band": "[0,0.5)", "sv_band": "SV=0", "p": 0.8, "n_blocks": 50, "under_powered": False},
        {"ads_band": "1.0", "sv_band": "SV=0", "p": 0.2, "n_blocks": 50, "under_powered": False},
        {"ads_band": "[0,0.5)", "sv_band": "SV low", "p": 0.6, "n_blocks": 50, "under_powered": False},
        {"ads_band": "1.0", "sv_band": "SV low", "p": 0.5, "n_blocks": 50, "under_powered": False},
    ])
    marg_sv = pd.DataFrame({"sv_band": ["SV=0", "SV low"], "under_powered": [False, False]})
    marg_ads = pd.DataFrame({"ads_band": ["[0,0.5)", "1.0"], "under_powered": [False, False]})
    ra, _, nb = averaged_range(cells, "sv_band", "ads_band", marg_sv, "p")
    assert abs(ra - (0.6 + 0.1) / 2) < 1e-12 and nb == 2, ra
    rs, _, _ = averaged_range(cells, "ads_band", "sv_band", marg_ads, "p")
    assert abs(rs - (0.2 + 0.3) / 2) < 1e-12, rs
    # an under-powered marginal band is excluded from the average
    marg_sv2 = pd.DataFrame({"sv_band": ["SV=0", "SV low"], "under_powered": [False, True]})
    ra2, _, nb2 = averaged_range(cells, "sv_band", "ads_band", marg_sv2, "p")
    assert abs(ra2 - 0.6) < 1e-12 and nb2 == 1, ra2

    # the verdict renames are cosmetic: same rule, new labels
    assert vrd(0.06, 0.20, 0.05) == "rule wins"
    assert vrd(-0.20, -0.06, 0.05) == "k-NN wins"
    assert vrd(-0.04, 0.04, 0.05) == "tie"
    assert vrd(0.04, 0.20, 0.05) == "undecided"

    # structural classification, on hand-built bands
    def cell(a, s, v):
        return {"ads_band": a, "sv_band": s, "under_powered": False, "verdict_0.05": v}
    rev = pd.DataFrame([cell("[0,0.5)", "SV=0", "rule wins"),
                        cell("[0,0.5)", "SV high", "k-NN wins")])
    assert structural(rev, "ads_band", "sv_band", SV_BAND_NAMES, 0.05).outcome[0] == "winner reversal"
    tc = pd.DataFrame([cell("[0,0.5)", "SV=0", "tie"), cell("[0,0.5)", "SV high", "k-NN wins")])
    assert structural(tc, "ads_band", "sv_band", SV_BAND_NAMES, 0.05).outcome[0] == "tie-crossing"
    comp = pd.DataFrame([cell("[0,0.5)", "SV=0", "tie"), cell("[0,0.5)", "SV high", "tie")])
    assert structural(comp, "ads_band", "sv_band", SV_BAND_NAMES, 0.05).outcome[0] == "gap compression only"
    one = pd.DataFrame([cell("[0,0.5)", "SV=0", "tie")])
    assert structural(one, "ads_band", "sv_band", SV_BAND_NAMES, 0.05).outcome[0] == "not eligible"

    print("phase2e_run self-check: all assertions passed")


# --------------------------------------------------------------------------
# 5. report sections
# --------------------------------------------------------------------------

def header(blocks, ev, prim, bk, bk2, sig):
    n_sig = len(sig)
    singles = sig[~sig.is_live]
    return [
        "# Phase 2.2e: the amended boundary experiment",
        "",
        "Produced by `phase2/phase2e_run.py`, executing `phase2/PREREG.md` as amended by "
        "**Amendment 1** and **Addendum 1a**, both frozen on 2026-09-18 at Phase 2.2d "
        "before any number on this page existed. Mechanism B is the k-nearest vote of "
        "`phase2/phase2e_mech.py`, whose regression check reproduces the 2.2c "
        "calibration-split two-sidedness counts exactly (see the next section). Nothing "
        "below re-tunes, re-bands or redefines anything the pre-registration fixed: "
        "section 7 is void, k is fixed by definition at {}, and the split, the ADS bands, "
        "the SV and SV_resid band edges, the margins and the seeds all carry over from the "
        "2.2a freeze and `phase2b_constants.py`.".format(K_PRIMARY),
        "",
        "Frozen inputs used here: SV band edges {:.6f} / {:.6f}; SV_resid band edges "
        "{:.6f} / {:.6f}; seed 20260918; B = 2000; delta = 0.05 primary with 0.02 and 0.03 "
        "as the robustness curve.".format(*SV_BAND_EDGES, *SV_RESID_BAND_EDGES),
        "",
        "The 2.2b numbers are not recomputed, not overwritten and not withdrawn. They stay "
        "in `reports/phase2b_boundary.md` as the record of the nested pair.",
        "",
        "## Population accounting (PREREG section 3)",
        "",
        "| stratum | blocks | signatures | share of signatures |",
        "| --- | ---: | ---: | ---: |",
        "| all signatures | {:,} | {:,} | 100.00% |".format(
            len(blocks) + int((~sig.is_live).sum()), n_sig),
        "| singleton blocks, outside the live set | {:,} | {:,} | {:.2f}% |".format(
            int((~sig.is_live).sum()), len(singles), 100 * len(singles) / n_sig),
        "| live blocks (2+ signatures) | {:,} | {:,} | {:.2f}% |".format(
            len(blocks), int(blocks.n_train.sum() + blocks.n_test.sum()),
            100 * (blocks.n_train.sum() + blocks.n_test.sum()) / n_sig),
        "| - calibration split (15%) | {:,} | {:,} | {:.2f}% |".format(
            int(blocks.is_cal.sum()),
            int(blocks[blocks.is_cal].n_train.sum() + blocks[blocks.is_cal].n_test.sum()),
            100 * (blocks[blocks.is_cal].n_train.sum() + blocks[blocks.is_cal].n_test.sum()) / n_sig),
        "| - evaluation split (85%) | {:,} | {:,} | {:.2f}% |".format(
            len(ev), int(ev.n_train.sum() + ev.n_test.sum()),
            100 * (ev.n_train.sum() + ev.n_test.sum()) / n_sig),
        "| - - **primary analysis population** (n_train >= 2) | {:,} | {:,} | {:.2f}% |".format(
            len(prim), int(prim.n_train.sum() + prim.n_test.sum()),
            100 * (prim.n_train.sum() + prim.n_test.sum()) / n_sig),
        "| - - block-size-2 stratum, named exclusion | {:,} | {:,} | {:.2f}% |".format(
            len(bk2), int(bk2.n_train.sum() + bk2.n_test.sum()),
            100 * (bk2.n_train.sum() + bk2.n_test.sum()) / n_sig),
        "",
        "Both exclusions are counted and reported, never silently dropped. ADS = 1.0 blocks "
        "are **not** excluded: Amendment 1 keeps them because the decline of decidability "
        "into that band is what H2 is about.",
        "",
        "Every reported number below comes from the {:,} blocks and {:,} test signatures of "
        "the primary analysis population.".format(len(bk), int(bk.n_test.sum())),
        "",
    ]


def section_regression_check(regr, out):
    out += [
        "## Regression check: mechanism B reproduces the 2.2c design diagnostics",
        "",
        "Mandatory first step, run before any evaluation-split signature was read. "
        "`phase2/phase2e_mech.py` is written independently of `phase2c_probe.py`, so this "
        "is a check rather than a restatement. It reruns the 2.2c two-sidedness counts on "
        "the **calibration split only** and asserts them against "
        "`reports/tables/phase2c_pair_twosidedness.csv`. If it fails, the bug is in the "
        "mechanism and no evaluation number may be produced.",
        "",
        md_table(regr),
        "",
        "All four k values reproduce the frozen counts exactly, including the k = 5 pair "
        "**546 rule wins against 744 k-NN wins**, and mechanism A's accuracy 0.8234 is "
        "identical across k as it must be, since A does not depend on k. The monotone fall "
        "of B's accuracy from k = 2 to k = 10 is the calibration trap Amendment 1 voided "
        "section 7 over: maximizing accuracy would walk the design back to the k = 1 "
        "nesting limit.",
        "",
        "Table: " + dump(regr, "phase2e_regression_check.csv"),
        "",
    ]


def section_accuracy(bk, bk2, out):
    out += ["## Held-out accuracy and coverage", ""]
    rows = []
    for name, grp in populations(bk):
        if not len(grp):
            continue
        n = grp.n_test.sum()
        rows.append({
            "population": name, "blocks": len(grp), "test signatures": int(n),
            "rule accuracy": grp.rule_correct.sum() / n,
            "k-NN accuracy": grp["knn_correct_" + PRIMARY].sum() / n,
            "gap (rule - k-NN)": (grp.rule_correct.sum() - grp["knn_correct_" + PRIMARY].sum()) / n,
            "rule coverage": grp.rule_fires_n.sum() / n,
            "k-NN coverage": 1.0,
            "agreement": grp["agree_n_" + PRIMARY].sum() / n,
            "qualifies (>=100 blocks)": len(grp) >= MIN_DATASET_BLOCKS,
        })
    tab = pd.DataFrame(rows)
    out += [md_table(tab), "",
            "Abstention sits entirely on the rule's side, as Amendment 1 says it must: the "
            "rule abstains on {:.2%} of test signatures and the k-nearest vote never "
            "abstains. Abstention is scored as incorrect throughout.".format(
                1 - bk.rule_fires_n.sum() / bk.n_test.sum()),
            ""]
    if len(bk2):
        n2 = bk2.n_test.sum()
        out += ["**Block-size-2 stratum, reported not interpreted.** {:,} blocks, {:,} test "
                "signatures. Rule accuracy {:.4f}, k-NN accuracy {:.4f}, rule coverage "
                "{:.4f}. These blocks are excluded from every hypothesis test.".format(
                    len(bk2), int(n2), bk2.rule_correct.sum() / n2,
                    bk2["knn_correct_" + PRIMARY].sum() / n2, bk2.rule_fires_n.sum() / n2),
                ""]
    out += ["Table: " + dump(tab, "phase2e_accuracy_by_population.csv"), ""]

    # two-sidedness on the evaluation split, the thing 2.2b could not have
    both = []
    for arm, k in COMBOS:
        c = combo(arm, k)
        both.append({"arm": arm, "k": k,
                     "A right, B wrong": int(bk["n_plus_" + c].sum()),
                     "B right, A wrong": int(bk["n_minus_" + c].sum()),
                     "rule acc": float(bk.rule_correct.sum() / bk.n_test.sum()),
                     "k-NN acc": float(bk["knn_correct_" + c].sum() / bk.n_test.sum()),
                     "pooled gap": float((bk.rule_correct.sum() - bk["knn_correct_" + c].sum())
                                         / bk.n_test.sum())})
    ts = pd.DataFrame(both)
    out += ["### Two-sidedness on the evaluation split", "",
            "The single quantity 2.2b could not produce. `rule wins` measured **zero** for "
            "the retired pair on 199,713 signatures; for the amended pair it is a positive "
            "count at every k on the mandatory curve, so the winner construct is reachable "
            "in both directions before any band is cut.", "",
            md_table(ts), "", "Table: " + dump(ts, "phase2e_twosidedness_eval.csv"), ""]
    return ts


def section_h1(bk, out):
    out += ["## H1, accuracy: does train-only ADS track each mechanism's own accuracy?", "",
            "Amendment 1 keeps H1 as a construct-validity check, not a contribution. "
            "Spearman correlation between train-only ADS and the block's held-out accuracy, "
            "with a 95% block-bootstrap interval, for the exact-evidence rule and for the "
            "k-nearest vote at k = {}.".format(K_PRIMARY), ""]
    rows, res = [], {}
    for name, grp in populations(bk):
        if len(grp) < 3:
            continue
        row = {"population": name, "blocks": len(grp),
               "qualifies": len(grp) >= MIN_DATASET_BLOCKS}
        ok = True
        for mech, col in [("rule", "rule_acc"), ("k-NN", "knn_acc_" + PRIMARY)]:
            pt, lo, hi = spearman_block_ci(grp.ads.values, grp[col].values,
                                           seed=band_seed("h1e|" + name + "|" + mech))
            row["rho " + mech], row["lo " + mech], row["hi " + mech] = pt, lo, hi
            ok = ok and (lo > 0)
        row["both positive, interval excludes 0"] = ok
        rows.append(row)
        res[name] = row
    tab = pd.DataFrame(rows)
    out += [md_table(tab), "", "Table: " + dump(tab, "phase2e_h1_spearman.csv"), ""]

    band = bk.groupby("ads_band").agg(
        blocks=("ads", "size"), rule=("rule_acc", "mean"),
        knn=("knn_acc_" + PRIMARY, "mean"), rule_cov=("rule_cov", "mean")
    ).reindex(ADS_BANDS).reset_index()
    out += ["Mean per-block accuracy by ADS band:", "", md_table(band), ""]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(band))
    ax.plot(x, band.rule, "o-", label="exact-evidence rule (A)")
    ax.plot(x, band.knn, "s-", label="k-nearest vote, k = {} (B)".format(K_PRIMARY))
    ax.set_xticks(x)
    ax.set_xticklabels(band.ads_band)
    ax.set_xlabel("train-only ADS band")
    ax.set_ylabel("mean per-block held-out accuracy")
    ax.set_title("H1: ADS tracks each mechanism's own accuracy")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "phase2e_h1_ads_accuracy.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2e_h1_ads_accuracy.png`", ""]

    qual = [d for d in sorted(bk.dataset.unique())
            if d != "inspire" and res.get(d, {}).get("qualifies")]
    held = [d for d in qual if res[d]["both positive, interval excludes 0"]]
    generalizes = (res.get("pooled non-inspire", {}).get("both positive, interval excludes 0", False)
                   and len(held) > len(qual) / 2)
    out += ["Qualifying non-inspire datasets ({}): {}. H1 holds in {} of them: {}."
            .format(len(qual), ", ".join(qual) or "none", len(held), ", ".join(held) or "none"), ""]
    return {"res": res, "qualifying_non_inspire": qual, "held": held,
            "generalizes": generalizes, "pooled": res.get("all (primary population)")}


def section_winner(bk, out):
    out += ["## The winner (PREREG section 8, verdicts renamed by Amendment 1)", "",
            "Per block: paired bootstrap on the accuracy difference, B = 2000, seed "
            "20260918 + block index, 95% percentile interval, four mutually exclusive "
            "verdicts `rule wins`, `k-NN wins`, `tie`, `undecided`. Per band and per cell: "
            "the pooled gap with an interval from resampling **blocks** with replacement. "
            "delta = 0.05 is primary, 0.02 and 0.03 the robustness curve.", ""]

    counts = bk["bverdict_{}_{:.2f}".format(PRIMARY, DELTA_PRIMARY)].value_counts()
    out += ["Overall per-block verdict distribution, delta = 0.05, k = 5:", "",
            md_table(pd.DataFrame({"verdict": list(VERDICTS),
                                   "blocks": [int(counts.get(v, 0)) for v in VERDICTS],
                                   "share": [float(counts.get(v, 0) / len(bk)) for v in VERDICTS]})),
            ""]

    grids = {}
    specs = [("ads", ["ads_band"], PRIMARY, ADS_BANDS),
             ("sv", ["sv_band"], PRIMARY, SV_BAND_NAMES),
             ("svr", ["svr_band"], PRIMARY, SV_BAND_NAMES),
             ("cells_sv", ["ads_band", "sv_band"], PRIMARY, None),
             ("cells_svr", ["ads_band", "svr_band"], PRIMARY, None),
             ("sv_jw", ["sv_band"], combo("jarowinkler", K_PRIMARY), SV_BAND_NAMES),
             ("cells_sv_jw", ["ads_band", "sv_band"], combo("jarowinkler", K_PRIMARY), None),
             ("init_sv", ["init_band", "sv_band"], PRIMARY, None)]
    for name, keys, c, order in specs:
        t = pooled_table(bk, keys, c, name)
        if order is not None:
            t = order_bands(t, keys[0], order)
        grids[name] = t
        dump(t, "phase2e_pooled_{}.csv".format(name))

    show = ["n_blocks", "n_test", "rule_acc", "knn_acc", "pooled_gap", "ci_lo", "ci_hi",
            "verdict_0.05", "verdict_0.03", "verdict_0.02", "under_powered"]
    out += ["### Pooled verdict by ADS band (marginal)", "",
            md_table(grids["ads"], ["ads_band"] + show + ["decided_rate_0.05"]), "",
            "### Pooled verdict by SV band (marginal)", "",
            md_table(grids["sv"], ["sv_band"] + show + ["decided_rate_0.05"]), "",
            "### Pooled verdict by SV_resid band (marginal)", "",
            md_table(grids["svr"], ["svr_band"] + show), ""]

    cells = sort_cells(grids["cells_sv"])
    out += ["### The 5 x 4 ADS-by-SV grid (PREREG section 9)", "",
            "The SV effect is only ever shown at fixed ADS and the ADS effect only at fixed "
            "SV, because the two axes correlate (Phase 2.1: Pearson -0.2988). Cells under "
            "30 blocks are marked under-powered and decide nothing.", "",
            md_table(cells, ["ads_band", "sv_band"] + show +
                     ["decided_rate_0.05", "agreement", "rule_cov"]), "",
            "Table: reports/tables/phase2e_pooled_cells_sv.csv", ""]

    heat(cells, "sv_band", "pooled_gap", "phase2e_grid_gap_sv.png",
         "Pooled rule minus k-NN gap, ADS by SV",
         "(positive = the rule ahead, negative = the k-nearest vote ahead)", diverging=True)
    heat(sort_cells(grids["cells_svr"], "svr_band"), "svr_band", "pooled_gap",
         "phase2e_grid_gap_svresid.png", "Pooled rule minus k-NN gap, ADS by SV_resid",
         "(positive = the rule ahead, negative = the k-nearest vote ahead)", diverging=True)
    heat(cells, "sv_band", "decided_rate_0.05", "phase2e_grid_decided_sv.png",
         "Decided-winner rate, ADS by SV (delta = 0.05)",
         "(share of the cell's blocks whose per-block verdict is rule wins or k-NN wins)",
         diverging=False)
    out += ["Figures: `reports/figs/phase2e_grid_gap_sv.png`, "
            "`reports/figs/phase2e_grid_gap_svresid.png`, "
            "`reports/figs/phase2e_grid_decided_sv.png`", ""]

    verdict_bars(grids["ads"], "ads_band", "phase2e_verdicts_by_ads.png",
                 "Per-block verdict shares by ADS band (delta = 0.05, k = 5)")
    verdict_bars(grids["sv"], "sv_band", "phase2e_verdicts_by_sv.png",
                 "Per-block verdict shares by SV band (delta = 0.05, k = 5)")
    out += ["Figures: `reports/figs/phase2e_verdicts_by_ads.png`, "
            "`reports/figs/phase2e_verdicts_by_sv.png`", ""]

    X = np.column_stack([np.ones(len(bk)), bk.ads.values, bk.sv.values, np.log(bk.n_test.values)])
    fit = ols_robust(X, bk["gap_" + PRIMARY].values,
                     ["intercept", "ADS", "SV", "log(test-set size)"])
    out += ["### Compact regression summary", "",
            "Per-block gap (rule minus k-NN) on ADS and SV together, with test-set size as a "
            "covariate and heteroskedasticity-robust standard errors, for the reason "
            "`phase2b_core.ols_robust` states. A summary of the grid, not a substitute for "
            "it; no hypothesis is decided from it.", "", md_table(fit), ""]
    dump(fit, "phase2e_regression.csv")
    return grids


def heat(cells, svcol, value, fname, title, subtitle, diverging):
    piv = cells.pivot_table(index="ads_band", columns=svcol, values=value)
    piv = piv.reindex(index=[a for a in ADS_BANDS if a in piv.index],
                      columns=[s for s in SV_BAND_NAMES if s in piv.columns])
    cnt = cells.pivot_table(index="ads_band", columns=svcol, values="n_blocks").reindex(
        index=piv.index, columns=piv.columns)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    if diverging:
        lim = float(np.nanmax(np.abs(piv.values))) or 0.01
        im = ax.imshow(piv.values, cmap="RdBu_r", vmin=-lim, vmax=lim)
        mid = lim * 0.6
    else:
        im = ax.imshow(piv.values, cmap="viridis", vmin=0, vmax=float(np.nanmax(piv.values)) or 1)
        mid = float(np.nanmax(piv.values)) * 0.5 or 0.5
    ax.set_xticks(range(len(piv.columns)))
    ax.set_xticklabels(piv.columns)
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels(piv.index)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v, c = piv.values[i, j], cnt.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, "{:+.3f}\nn={:.0f}".format(v, c) if diverging
                        else "{:.3f}\nn={:.0f}".format(v, c), ha="center", va="center",
                        fontsize=8, color="black" if abs(v) < mid else "white")
    ax.set_xlabel(svcol)
    ax.set_ylabel("ADS band")
    ax.set_title(title + "\n" + subtitle, fontsize=10)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(FIGS / fname, dpi=150)
    plt.close(fig)


def verdict_bars(tab, col, fname, title):
    keys = ["share_{}_{:.2f}".format(v.replace(" ", "_").replace("-", ""), DELTA_PRIMARY)
            for v in VERDICTS]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bottom = np.zeros(len(tab))
    for v, k in zip(VERDICTS, keys):
        ax.bar(tab[col], tab[k], bottom=bottom, label=v)
        bottom += tab[k].values
    ax.set_ylabel("share of blocks")
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / fname, dpi=150)
    plt.close(fig)


def section_decidability(bk, grids, out):
    """Amendment 1 H2 and Addendum 1a: the gradient and the driver comparison."""
    out += ["## Decidability: the gradient and its drivers (Amendment 1 H2, Addendum 1a)", "",
            "The decided-winner rate of a cell is the share of that cell's blocks whose "
            "**per-block** verdict is `rule wins` or `k-NN wins` (resolution 4). H2 says it "
            "declines as ADS rises, approaching zero in the top ADS band while staying "
            "non-trivially positive below it, and that ADS is the stronger driver of it "
            "than SV.", "",
            "The decline into the ADS = 1.0 band is **partly structural** and Amendment 1 "
            "says so in its own text: a block whose train history names one author returns "
            "that author from any non-empty pool, so only abstention can differ there. The "
            "load-bearing empirical content is the gradient below 1.0 and the existence of "
            "a decidable region. Both statements belong in the paper together.", ""]

    cells = sort_cells(grids["cells_sv"])
    dec_cols = ["ads_band", "sv_band", "n_blocks"] + \
               ["decided_rate_{:.2f}".format(d) for d in DELTAS] + \
               ["n_decided_{:.2f}".format(DELTA_PRIMARY), "under_powered"]
    out += ["### Decided-winner rate over the frozen 5 x 4 grid", "",
            md_table(cells[dec_cols]), "",
            "Table: " + dump(cells[dec_cols], "phase2e_decided_rate_cells.csv"), ""]

    marg = grids["ads"][["ads_band", "n_blocks"] +
                        ["decided_rate_{:.2f}".format(d) for d in DELTAS] +
                        ["n_decided_{:.2f}".format(DELTA_PRIMARY), "under_powered"]]
    out += ["Marginal decided-winner rate by ADS band:", "", md_table(marg), ""]

    grad = {d: gradient_clauses(cells, grids["ads"], grids["sv"], d) for d in DELTAS}
    g = grad[DELTA_PRIMARY]
    out += ["### The gradient at fixed SV (delta = 0.05)", "",
            "Within each eligible SV band, the decided-winner rate across the eligible ADS "
            "cells, in ADS order.", "",
            md_table(g["per_sv"]), "",
            "Non-increasing across ADS in {} of {} usable SV bands; strictly lower in the "
            "top ADS band than the bottom in {} of {}. The marginal ADS reading, which is "
            "the other available construction of the same clause, gives top below bottom: "
            "**{}**.".format(int(g["per_sv"].non_increasing.sum(skipna=True)),
                             g["usable_sv_bands"],
                             int(g["per_sv"].top_below_bottom.sum(skipna=True)),
                             g["usable_sv_bands"],
                             g["marginal_top_below_bottom"]), "",
            "Both readings of the clause are reported because the frozen sentence admits "
            "both; the falsification table below requires them to agree and says so if they "
            "do not.", ""]
    dump(pd.concat([grad[d]["per_sv"].assign(delta=d) for d in DELTAS]),
         "phase2e_gradient_by_sv.csv")

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    for s in SV_BAND_NAMES:
        sub = order_bands(cells[(cells.sv_band == s) & (~cells.under_powered)],
                          "ads_band", ADS_BANDS)
        if len(sub):
            ax.plot(sub.ads_band, sub["decided_rate_0.05"], "o-", label=s)
    mm = order_bands(grids["ads"][~grids["ads"].under_powered], "ads_band", ADS_BANDS)
    ax.plot(mm.ads_band, mm["decided_rate_0.05"], "k--", lw=2, label="marginal (all SV)")
    ax.set_xlabel("train-only ADS band")
    ax.set_ylabel("decided-winner rate")
    ax.set_title("H2: decidability against ADS, at fixed SV (delta = 0.05, k = 5)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "phase2e_decidability_gradient.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2e_decidability_gradient.png`", ""]

    # --- Addendum 1a driver comparison
    drv = {d: driver_comparison(cells, grids["ads"], grids["sv"], d, "full grid")
           for d in DELTAS}
    sub_cells = cells[cells.ads_band.isin(ADS_BELOW_ONE)]
    drv_sub = driver_comparison(sub_cells, grids["ads"][grids["ads"].ads_band.isin(ADS_BELOW_ONE)],
                                grids["sv"], DELTA_PRIMARY, "ADS < 1.0 only (diagnostic)")
    keep = ["label", "delta", "eligible_cells", "ADS levels", "SV levels", "SS_total",
            "eta2_ADS", "eta2_SV", "avg_range_ADS", "avg_range_SV",
            "eta2_ADS_blockweighted", "eta2_SV_blockweighted", "clause"]
    dtab = pd.DataFrame([{k: v for k, v in r.items() if k in keep}
                         for r in [drv[d] for d in DELTAS] + [drv_sub]])[keep]
    out += ["### Which signal drives decidability (Addendum 1a)", "",
            "Primary measure: the one-way, eta-squared style variance decomposition over "
            "the eligible cells of the frozen 5 x 4 grid, each cell one unweighted "
            "observation. Second required condition: the averaged-range test of the "
            "original resolution 5, kept verbatim. **ADS is the stronger driver only if it "
            "is larger under both.** A split makes the clause Partial and is reported with "
            "both pairs of numbers.", "",
            md_table(dtab, floats=4), "",
            "Table: " + dump(dtab, "phase2e_driver_comparison.csv"), "",
            "The block-weighted decomposition is printed above beside the unweighted one "
            "and **decides nothing**, for the reason Addendum 1a gives: the ADS = 1.0 row "
            "holds most of the population and its low decidability is the part of H2 that "
            "is conceded to be structural, so block-weighting would hand that one row "
            "decisive leverage over exactly the comparison H2 needs ADS to win.", "",
            "The last row restricts the same computation to the four ADS bands below 1.0. "
            "It is a **labeled diagnostic and decides nothing**: deleting the top row tests "
            "a different hypothesis from the one H2 states, and Addendum 1a pre-registers "
            "no such variant. It is reported because a reader is entitled to see how much "
            "of the comparison rests on the structural row.", ""]
    for r, tag in [(drv[DELTA_PRIMARY], "full grid"), (drv_sub, "ADS < 1.0 diagnostic")]:
        out += ["Per-band ranges, {}: ADS ranges within each SV band {}; SV ranges within "
                "each ADS band {}.".format(
                    tag,
                    ", ".join("{}={:.4f}".format(a, b) for a, b in
                              zip(r["_detail_ads"].iloc[:, 0], r["_detail_ads"]["range"])),
                    ", ".join("{}={:.4f}".format(a, b) for a, b in
                              zip(r["_detail_sv"].iloc[:, 0], r["_detail_sv"]["range"]))), ""]

    region_bands, region_ok = decidable_region(grids["ads"], DELTA_PRIMARY)
    out += ["### A non-trivial decidable region (resolution 6)", "",
            "At least one ADS band below 1.0 with 30 or more blocks in which 30 or more "
            "blocks carry a decided per-block verdict. Bands meeting it at delta = 0.05: "
            "**{}**.".format(", ".join(region_bands) if region_ok else "none"), ""]
    return {"cells": cells, "gradient": grad, "driver": drv, "driver_sub": drv_sub,
            "region_bands": region_bands, "region_ok": region_ok}


def section_k_curve(bk, out):
    """Amendment 1: the k in {2, 3, 5, 10} sensitivity curve, mandatory."""
    out += ["## The k sensitivity curve (Amendment 1, mandatory)", "",
            "k is fixed by definition at 5 and is never calibrated by maximizing accuracy, "
            "because B's accuracy is monotone toward the single-nearest limit, which is the "
            "2.2b nesting. Every H2 and H3 outcome is recomputed across the curve; an "
            "outcome that holds at k = 5 and flips elsewhere is k-dependent and is treated "
            "as Partial, not Supported. k = 1 is off the curve as the known-degenerate "
            "case (resolution 3).", ""]
    rows, per_k = [], {}
    for k in KS:
        c = combo("levenshtein", k)
        cells = sort_cells(pooled_table(bk, ["ads_band", "sv_band"], c, "kcells{}".format(k)))
        ads_m = order_bands(pooled_table(bk, ["ads_band"], c, "kads{}".format(k)),
                            "ads_band", ADS_BANDS)
        sv_m = order_bands(pooled_table(bk, ["sv_band"], c, "ksv{}".format(k)),
                           "sv_band", SV_BAND_NAMES)
        per_k[k] = {"cells": cells, "ads": ads_m, "sv": sv_m}
        n = bk.n_test.sum()
        drv = driver_comparison(cells, ads_m, sv_m, DELTA_PRIMARY, "k={}".format(k))
        grad = gradient_clauses(cells, ads_m, sv_m, DELTA_PRIMARY)
        st = structural(cells[cells.ads_band.isin(ADS_BELOW_ONE)], "ads_band", "sv_band",
                        SV_BAND_NAMES, DELTA_PRIMARY)
        _, region_ok = decidable_region(ads_m, DELTA_PRIMARY)
        rows.append({
            "k": k,
            "rule acc": float(bk.rule_correct.sum() / n),
            "k-NN acc": float(bk["knn_correct_" + c].sum() / n),
            "pooled gap": float((bk.rule_correct.sum() - bk["knn_correct_" + c].sum()) / n),
            "A right B wrong": int(bk["n_plus_" + c].sum()),
            "B right A wrong": int(bk["n_minus_" + c].sum()),
            "decided rate": float((bk["bverdict_{}_{:.2f}".format(c, DELTA_PRIMARY)]
                                   .isin(DECIDED)).mean()),
            "decidable region": region_ok,
            "gradient non-increasing (majority)": grad["non_increasing_majority"],
            "eta2_ADS": drv["eta2_ADS"], "eta2_SV": drv["eta2_SV"],
            "driver clause": drv["clause"],
            "SV reversal below ADS 1.0": bool((st.outcome == "winner reversal").any()),
            "tie-crossing below ADS 1.0": bool((st.outcome == "tie-crossing").any()),
        })
    tab = pd.DataFrame(rows)
    out += [md_table(tab), "", "Table: " + dump(tab, "phase2e_k_curve.csv"), ""]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(tab.k, tab["A right B wrong"], "o-", label="rule right, k-NN wrong")
    axes[0].plot(tab.k, tab["B right A wrong"], "s-", label="k-NN right, rule wrong")
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("test signatures")
    axes[0].set_title("Two-sidedness against k")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)
    axes[1].plot(tab.k, tab["decided rate"], "o-", label="decided-winner rate")
    axes[1].plot(tab.k, tab["eta2_ADS"], "s-", label="eta2 ADS")
    axes[1].plot(tab.k, tab["eta2_SV"], "^-", label="eta2 SV")
    axes[1].set_xlabel("k")
    axes[1].set_title("Decidability and its drivers against k")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.3)
    fig.suptitle("Mandatory k sensitivity curve (delta = 0.05)")
    fig.tight_layout()
    fig.savefig(FIGS / "phase2e_k_curve.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2e_k_curve.png`", ""]
    return tab, per_k


def section_power(bk, out):
    out += ["## Power report (PREREG section 8, mandatory)", "",
            "Verdict share as a function of test-set size, so a reader can see how much of "
            "any no-winner region is demonstrated equivalence and how much is a small test "
            "set. Tie and undecided are never merged.", ""]
    bk["size_bin"] = [size_bin(n) for n in bk.n_test]
    order = [size_bin(lo) for lo, _ in SIZE_BINS]
    rows = []
    for d in DELTAS:
        col = "bverdict_{}_{:.2f}".format(PRIMARY, d)
        for b in order:
            grp = bk[bk.size_bin == b]
            if not len(grp):
                continue
            dist = grp[col].value_counts(normalize=True)
            rows.append({"delta": d, "test-set size": b, "blocks": len(grp),
                         **{v: float(dist.get(v, 0.0)) for v in VERDICTS}})
    tab = pd.DataFrame(rows)
    out += [md_table(tab[tab.delta == DELTA_PRIMARY].drop(columns=["delta"])), "",
            "Full curve across all three margins: " + dump(tab, "phase2e_power_by_size.csv"), ""]

    fig, axes = plt.subplots(1, len(DELTAS), figsize=(13, 4), sharey=True)
    for ax, d in zip(axes, DELTAS):
        sub = tab[tab.delta == d].set_index("test-set size").reindex(
            [b for b in order if b in set(tab["test-set size"])])
        bottom = np.zeros(len(sub))
        for v in VERDICTS:
            ax.bar(sub.index, sub[v], bottom=bottom, label=v)
            bottom += sub[v].values
        ax.set_title("delta = {:.2f}".format(d))
        ax.set_xlabel("test-set size")
        ax.tick_params(axis="x", rotation=45)
    axes[0].set_ylabel("share of blocks")
    axes[-1].legend(fontsize=8, loc="lower right")
    fig.suptitle("Verdict share by test-set size: power, not equivalence")
    fig.tight_layout()
    fig.savefig(FIGS / "phase2e_power_by_size.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2e_power_by_size.png`", ""]


def section_structure(bk, grids, out):
    out += ["## Winner structure: reversal, tie-crossing, or compression only "
            "(PREREG section 9)", "",
            "A **winner reversal** is two bands with decided pooled verdicts of opposite "
            "identity. A **tie-crossing** is one band decided and another a demonstrated "
            "tie, with no band decided the opposite way. **Gap compression only** is a "
            "change of magnitude with neither. H3's direction-by-SV clause is scoped to ADS "
            "bands below 1.0 by Amendment 1's own wording; the full grid is printed too.", ""]
    tables = {}
    for d in DELTAS:
        tables[("h3", "sv", d)] = structural(grids["cells_sv"], "ads_band", "sv_band",
                                             SV_BAND_NAMES, d)
        tables[("h3", "svr", d)] = structural(grids["cells_svr"], "ads_band", "svr_band",
                                              SV_BAND_NAMES, d)
        tables[("h3", "sv_jw", d)] = structural(grids["cells_sv_jw"], "ads_band", "sv_band",
                                                SV_BAND_NAMES, d)
        tables[("h2", "sv", d)] = structural(grids["cells_sv"], "sv_band", "ads_band",
                                             ADS_BANDS, d)
    for tag, title in [("h3", "H3, direction by SV: across SV bands at fixed ADS"),
                       ("h2", "H3, non-direction by ADS: across ADS bands at fixed SV")]:
        out += ["### {}".format(title), ""]
        for arm in dict.fromkeys(k[1] for k in tables if k[0] == tag):
            out += ["**signal/metric: {}**".format(arm), ""]
            for d in DELTAS:
                out += ["delta = {:.2f}".format(d), "", md_table(tables[(tag, arm, d)]), ""]
            dump(pd.concat([tables[(tag, arm, d)].assign(delta=d) for d in DELTAS]),
                 "phase2e_structural_{}_{}.csv".format(tag, arm))

    gen_rows = []
    for name, grp in populations(bk, with_all=False):
        cells = pooled_table(grp, ["ads_band", "sv_band"], PRIMARY, "gen|" + name)
        st = structural(cells[cells.ads_band.isin(ADS_BELOW_ONE)], "ads_band", "sv_band",
                        SV_BAND_NAMES, DELTA_PRIMARY)
        ads_m = pooled_table(grp, ["ads_band"], PRIMARY, "genads|" + name)
        _, region_ok = decidable_region(ads_m, DELTA_PRIMARY)
        gradg = gradient_clauses(cells, ads_m, pooled_table(grp, ["sv_band"], PRIMARY,
                                                            "gensv|" + name), DELTA_PRIMARY)
        gen_rows.append({
            "population": name, "blocks": len(grp),
            "qualifies (>=100 blocks)": len(grp) >= MIN_DATASET_BLOCKS,
            "ADS bands (<1.0) with 2+ eligible SV bands": int((st.eligible_bands >= 2).sum()),
            "ADS bands (<1.0) with 2+ decided SV bands": int((st.decided_bands >= 2).sum()),
            "winner reversal": bool((st.outcome == "winner reversal").any()),
            "tie-crossing": bool((st.outcome == "tie-crossing").any()),
            "decidable region": region_ok,
            "gradient non-increasing (majority)": gradg["non_increasing_majority"],
            "gradient top<bottom (marginal)": gradg["marginal_top_below_bottom"],
        })
    gen = pd.DataFrame(gen_rows)
    out += ["### Per-dataset generalization (PREREG section 11)", "",
            "inspire is the great majority of live blocks, so a pooled number is mostly an "
            "inspire number. A finding generalizes only if it holds pooled non-inspire "
            "**and** in a majority of qualifying non-inspire datasets (100 or more blocks "
            "in the primary analysis population).", "",
            md_table(gen), "", "Table: " + dump(gen, "phase2e_generalization.csv"), ""]
    return tables, gen


def section_diagnostics(bk, grids, out):
    out += ["## Diagnostics required by the pre-registration", ""]
    sizes = bk.groupby("sv_band").n_test.agg(median_n_test="median",
                                             mean_n_test="mean").reset_index()
    ag = grids["sv"][["sv_band", "n_blocks", "n_test", "agreement", "rule_cov", "rule_acc",
                      "knn_acc"]].merge(sizes, on="sv_band")
    out += ["### Mechanism agreement rate per SV band (PREREG section 4)", "",
            "The share of test signatures on which the two mechanisms return the identical "
            "prediction. B never abstains, so a rule abstention counts as a disagreement. "
            "Under the retired 2.2b pair this diagnostic collapsed to the identity `exact "
            "coverage + fuzzy abstention rate`; under the amended pair it is an observation "
            "again, because the two mechanisms can disagree while both firing.", "",
            md_table(ag), ""]

    out += ["### Jaro-Winkler robustness arm (PREREG section 9, restated by Amendment 1)", "",
            "The same k-nearest vote with Jaro-Winkler similarity in place of normalized "
            "Levenshtein. It calibrates nothing, because there is no cutoff to calibrate.", "",
            md_table(grids["sv_jw"], ["sv_band", "n_blocks", "n_test", "rule_acc", "knn_acc",
                                      "pooled_gap", "ci_lo", "ci_hi", "verdict_0.05",
                                      "decided_rate_0.05", "under_powered"]), ""]

    init = grids["init_sv"].sort_values(
        ["init_band", "sv_band"],
        key=lambda s: s.map({v: i for i, v in enumerate(
            INIT_BANDS if s.name == "init_band" else SV_BAND_NAMES)}))
    out += ["### INIT stratification (PREREG section 9, secondary control)", "",
            "INIT is the train-only share of signatures whose given-name field is an initial "
            "only. The SV-to-winner relationship is shown inside each INIT band, which asks "
            "whether the effect exists among blocks homogeneous in initialization style.", "",
            md_table(init, ["init_band", "sv_band", "n_blocks", "n_test", "pooled_gap",
                            "ci_lo", "ci_hi", "verdict_0.05", "decided_rate_0.05",
                            "agreement", "under_powered"]), ""]
    for d in DELTAS:
        out += ["Structure across SV within each INIT band, delta = {:.2f}:".format(d), "",
                md_table(structural(grids["init_sv"], "init_band", "sv_band",
                                    SV_BAND_NAMES, d)), ""]

    corr = bk[["ads", "sv", "sv_resid", "init"]].corr(method="spearman")
    out += ["### How much of SV is forename initialization?", "",
            "Spearman correlations among the design-time signals on the primary analysis "
            "population. Unchanged from 2.2b, since the signals are unchanged; reprinted "
            "because the SV_resid control is load-bearing for H3.", "",
            md_table(corr.reset_index().rename(columns={"index": ""})), ""]
    dump(corr.reset_index(), "phase2e_signal_correlations.csv")


# --------------------------------------------------------------------------
# 6. the amended falsification table
# --------------------------------------------------------------------------

def _marginal_decided(tab, col, delta):
    ok = tab[(~tab.under_powered) & (tab["verdict_{:.2f}".format(delta)].isin(DECIDED))]
    return list(ok[col])


def h1_outcome(h1, n_blocks):
    p = h1["pooled"]
    facts = {"primary analysis population blocks": "{:,}".format(n_blocks),
             "qualifying non-inspire datasets": "{} ({})".format(
                 len(h1["qualifying_non_inspire"]), ", ".join(h1["qualifying_non_inspire"])),
             "Spearman rho, rule": "{:.4f}, 95% CI [{:.4f}, {:.4f}]".format(
                 p["rho rule"], p["lo rule"], p["hi rule"]),
             "Spearman rho, k-NN": "{:.4f}, 95% CI [{:.4f}, {:.4f}]".format(
                 p["rho k-NN"], p["lo k-NN"], p["hi k-NN"]),
             "generalizes": h1["generalizes"]}
    if n_blocks < 500 or len(h1["qualifying_non_inspire"]) < 2:
        return "Inconclusive", facts
    pos = {m: p["lo " + m] > 0 for m in ("rule", "k-NN")}
    neg = {m: p["hi " + m] < 0 for m in ("rule", "k-NN")}
    if (not any(pos.values()) and not any(neg.values())) or any(neg.values()):
        return "Not supported", facts
    if all(pos.values()) and h1["generalizes"]:
        return "Supported", facts
    return "Partial", facts


def h2_outcome(dec, grids, gen, delta):
    """The amended H2 row. Inconclusive first, then the five Supported clauses."""
    ads_dec = _marginal_decided(grids["ads"], "ads_band", delta)
    sv_dec = _marginal_decided(grids["sv"], "sv_band", delta)
    g = dec["gradient"][delta]
    drv = dec["driver"][delta]
    region_bands, region_ok = decidable_region(grids["ads"], delta)
    ni = gen[gen.population == "pooled non-inspire"]
    ni_ok = bool(len(ni) and ni["decidable region"].iloc[0]
                 and ni["gradient non-increasing (majority)"].iloc[0]
                 and ni["gradient top<bottom (marginal)"].iloc[0])
    facts = {
        "decided ADS bands (30+ blocks, pooled verdict)": ads_dec,
        "decided SV bands (30+ blocks, pooled verdict)": sv_dec,
        "gradient non-increasing across ADS in a majority of eligible SV bands":
            "{} ({} of {} usable SV bands)".format(
                g["non_increasing_majority"],
                int(g["per_sv"].non_increasing.sum(skipna=True)), g["usable_sv_bands"]),
        "top ADS band strictly below the bottom, per SV band (majority)":
            "{} ({} of {})".format(g["top_below_bottom_majority"],
                                   int(g["per_sv"].top_below_bottom.sum(skipna=True)),
                                   g["usable_sv_bands"]),
        "top ADS band strictly below the bottom, marginal reading":
            g["marginal_top_below_bottom"],
        "non-trivial decidable region below ADS = 1.0 (resolution 6)":
            "{} ({})".format(region_ok, ", ".join(region_bands) or "none"),
        "eta2_ADS vs eta2_SV (Addendum 1a primary)": "{:.4f} vs {:.4f}".format(
            drv["eta2_ADS"], drv["eta2_SV"]),
        "averaged range ADS vs SV (Addendum 1a second condition)": "{:.4f} vs {:.4f}".format(
            drv["avg_range_ADS"], drv["avg_range_SV"]),
        "ADS is the stronger driver": drv["clause"],
        "block-weighted eta2 (diagnostic, decides nothing)": "{:.4f} vs {:.4f}".format(
            drv["eta2_ADS_blockweighted"], drv["eta2_SV_blockweighted"]),
        "holds in the pooled non-inspire analysis": ni_ok,
    }
    if len(ads_dec) < 2 or len(sv_dec) < 2:
        return "Inconclusive", facts
    if drv["clause"] == "Inconclusive":
        return "Inconclusive", facts
    if not region_ok:
        return "Not supported", facts
    declines = bool(g["marginal_top_below_bottom"]) and bool(g["top_below_bottom_majority"])
    if not (g["marginal_top_below_bottom"] or g["top_below_bottom_majority"]):
        return "Not supported", facts
    if (declines and g["non_increasing_majority"] and drv["clause"] == "met" and ni_ok):
        return "Supported", facts
    return "Partial", facts


def h3_outcome(tables, grids, gen, delta):
    """The amended H3 row. Inconclusive first."""
    def below_one(t):
        return t[t.ads_band.isin(ADS_BELOW_ONE)]
    sv = below_one(tables[("h3", "sv", delta)])
    svr = below_one(tables[("h3", "svr", delta)])
    jw = below_one(tables[("h3", "sv_jw", delta)])
    ads_side = tables[("h2", "sv", delta)]
    floor = int((tables[("h3", "sv", delta)].decided_bands >= 2).sum())
    facts = {
        "ADS bands with 2+ eligible SV bands (any ADS)":
            int((tables[("h3", "sv", delta)].eligible_bands >= 2).sum()),
        "ADS bands with 2+ decided SV bands (any ADS)": floor,
        "ADS bands below 1.0 with 2+ decided SV bands": int((sv.decided_bands >= 2).sum()),
        "SV reversal below ADS = 1.0": bool((sv.outcome == "winner reversal").any()),
        "tie-crossing below ADS = 1.0": bool((sv.outcome == "tie-crossing").any()),
        "no ADS-driven reversal at fixed SV (non-direction by ADS)":
            not bool((ads_side.outcome == "winner reversal").any()),
        "SV_resid reversal below ADS = 1.0": bool((svr.outcome == "winner reversal").any()),
        "Jaro-Winkler reversal below ADS = 1.0": bool((jw.outcome == "winner reversal").any()),
    }
    if floor < 1:
        facts["generalizes"] = None
        return "Inconclusive", facts

    qual = gen[(gen["qualifies (>=100 blocks)"]) &
               (~gen.population.isin(["inspire", "inspire alone", "pooled non-inspire"]))]
    held = qual[qual["winner reversal"]]
    pooled_ni = gen[gen.population == "pooled non-inspire"]
    generalizes = bool(pooled_ni["winner reversal"].any()) and len(held) > len(qual) / 2
    facts["generalizes (pooled non-inspire + majority of qualifying datasets)"] = generalizes
    facts["qualifying non-inspire datasets"] = list(qual.population)
    facts["... with a reversal"] = list(held.population)

    if facts["SV reversal below ADS = 1.0"]:
        if (facts["SV_resid reversal below ADS = 1.0"]
                and facts["Jaro-Winkler reversal below ADS = 1.0"]
                and facts["no ADS-driven reversal at fixed SV (non-direction by ADS)"]
                and generalizes):
            return "Supported", facts
        return "Partial", facts
    if facts["tie-crossing below ADS = 1.0"]:
        return "Partial", facts
    return "Not supported", facts


def _facts_md(facts):
    return "\n".join("- {}: {}".format(k, v) for k, v in facts.items())


def section_falsification(h1, dec, tables, grids, gen, kcurve, bk, out):
    out += ["## The amended falsification table, evaluated (Amendment 1 section 10)", "",
            "Outcomes are read off the rules frozen at Phase 2.2d, in the order the "
            "pre-registration fixes: **Inconclusive is evaluated first** and takes "
            "precedence over every other row. An outcome that holds at one margin or one k "
            "and flips elsewhere is margin-dependent or k-dependent and is treated as "
            "Partial, not Supported.", ""]

    o1, f1 = h1_outcome(h1, len(bk))
    out += ["### H1, accuracy (validity check, not a contribution)", "",
            "**Outcome: {}**".format(o1), "", _facts_md(f1), ""]

    curve = {d: (h2_outcome(dec, grids, gen, d)[0], h3_outcome(tables, grids, gen, d)[0])
             for d in DELTAS}
    o2, f2 = h2_outcome(dec, grids, gen, DELTA_PRIMARY)
    o3, f3 = h3_outcome(tables, grids, gen, DELTA_PRIMARY)
    h2_stable = len({curve[d][0] for d in DELTAS}) == 1
    h3_stable = len({curve[d][1] for d in DELTAS}) == 1

    # k-dependence: the clauses each hypothesis rests on, across the mandatory curve
    k_h2 = kcurve.set_index("k")[["decidable region", "gradient non-increasing (majority)",
                                  "driver clause"]]
    k_h3 = kcurve.set_index("k")[["SV reversal below ADS 1.0", "tie-crossing below ADS 1.0"]]
    h2_k_stable = all(len(set(k_h2[c])) == 1 for c in k_h2.columns)
    h3_k_stable = all(len(set(k_h3[c])) == 1 for c in k_h3.columns)

    o2f = o2 if o2 != "Supported" or (h2_stable and h2_k_stable) else \
        "Partial ({})".format("margin-dependent" if not h2_stable else "k-dependent")
    o3f = o3 if o3 != "Supported" or (h3_stable and h3_k_stable) else \
        "Partial ({})".format("margin-dependent" if not h3_stable else "k-dependent")

    out += ["### H2, consistency gates decidability", "",
            "**Outcome: {}**".format(o2f), "", _facts_md(f2), "",
            "### H3, surface stability directs the choice", "",
            "**Outcome: {}**".format(o3f), "", _facts_md(f3), "",
            "### Margin sensitivity (PREREG section 8)", "",
            md_table(pd.DataFrame([{"delta": d, "H2": curve[d][0], "H3": curve[d][1]}
                                   for d in DELTAS])), "",
            "H2 constant across margins: {}. H3 constant across margins: {}.".format(
                "yes" if h2_stable else "**no, margin-dependent**",
                "yes" if h3_stable else "**no, margin-dependent**"), "",
            "### k sensitivity (Amendment 1, mandatory)", "",
            "The clauses each hypothesis rests on, recomputed across k in {2, 3, 5, 10} at "
            "the primary margin.", "",
            md_table(k_h2.reset_index()), "", md_table(k_h3.reset_index()), "",
            "H2's clauses constant across k: {}. H3's clauses constant across k: {}.".format(
                "yes" if h2_k_stable else "**no, k-dependent**",
                "yes" if h3_k_stable else "**no, k-dependent**"), ""]
    dump(pd.DataFrame([{"delta": d, "H2": curve[d][0], "H3": curve[d][1]} for d in DELTAS]),
         "phase2e_margin_sensitivity.csv")

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    t = grids["sv"]
    x = np.arange(len(t))
    ax.errorbar(x, t.pooled_gap, yerr=[t.pooled_gap - t.ci_lo, t.ci_hi - t.pooled_gap],
                fmt="o", capsize=3, color="black", label="pooled gap")
    for i, d in enumerate(sorted(DELTAS)):
        ax.axhline(d, ls=":", lw=0.8, color="C{}".format(i))
        ax.axhline(-d, ls=":", lw=0.8, color="C{}".format(i), label="delta = {:.2f}".format(d))
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(t.sv_band)
    ax.set_ylabel("pooled gap, rule minus k-NN")
    ax.set_title("Pooled gap by SV band against the three pre-registered margins")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGS / "phase2e_margin_sensitivity.png", dpi=150)
    plt.close(fig)
    out += ["Figure: `reports/figs/phase2e_margin_sensitivity.png`", ""]
    return o1, o2f, o3f, f2, f3


def section_epilogue(dec, grids, bk, out):
    """What the verdicts do and do not say, and the substance beside them.

    PREREG section 9 requires the structural reading to be stated whatever the
    verdict returns, and charter invariant 8 requires the paper to lead with the
    frozen table rather than with the framing that motivated the run. Both the
    verdicts and the substance are reported, separately, rather than the more
    favourable one being chosen.
    """
    ads = order_bands(grids["ads"], "ads_band", ADS_BANDS)
    sv = order_bands(grids["sv"], "sv_band", SV_BAND_NAMES)
    g = dec["gradient"][DELTA_PRIMARY]
    drv = dec["driver"][DELTA_PRIMARY]
    sub = dec["driver_sub"]
    rate_col = "decided_rate_{:.2f}".format(DELTA_PRIMARY)
    rates = ads[rate_col].values
    dip = int(np.argmin(rates))
    n_decided = int(bk["bverdict_{}_{:.2f}".format(PRIMARY, DELTA_PRIMARY)].isin(DECIDED).sum())
    out += [
        "## What these outcomes do and do not say",
        "",
        "**Why H2 and H3 are Inconclusive.** The Order of evaluation rule puts the power "
        "floor first and it is not met at the primary margin. Every marginal pooled verdict "
        "at delta = 0.05 is a demonstrated tie, because every marginal pooled gap is smaller "
        "than 0.05 in absolute value: {} across ADS bands, {} across SV bands. H2 needs two "
        "decided ADS bands and two decided SV bands and has none of either; H3 needs two "
        "decided SV bands inside a single ADS band and has none. This is the same floor that "
        "bit in 2.2b, for a different reason. In 2.2b no winner was reachable at all. Here "
        "the pair is two-sided, the gap changes sign on both axes, and the margin is simply "
        "wider than the effect.".format(
            ", ".join("{:+.4f}".format(v) for v in ads.pooled_gap),
            ", ".join("{:+.4f}".format(v) for v in sv.pooled_gap)),
        "",
        "Four things stand beside the verdict. None is a hypothesis outcome and none is "
        "offered in place of one.",
        "",
        "**1. The pooled gap changes sign on both axes.** Across ADS bands it runs {}, from "
        "the rule ahead at low consistency to the k-nearest vote ahead at ADS = 1.0. Across "
        "SV bands it runs {}, from the vote ahead where the history is written one way to "
        "the rule ahead where it is most varied. At delta = 0.02 the ADS ordering becomes a "
        "decided marginal reversal, `rule wins` in {} against `k-NN wins` at {}. Both "
        "design-time signals therefore carry winner-identity information, which is more than "
        "H3's SV clause claims and more than the retired selection-blindness claim allowed "
        "for ADS.".format(
            " -> ".join("{:+.4f}".format(v) for v in ads.pooled_gap),
            " -> ".join("{:+.4f}".format(v) for v in sv.pooled_gap),
            ADS_BANDS[0], ADS_BANDS[-1]),
        "",
        "**2. The decidability gradient is not monotone and does not approach zero at ADS = "
        "1.0.** The marginal decided-winner rate runs {}. It falls through the first four "
        "bands and then **rises** in the top band, from {:.4f} in {} to {:.4f} at ADS = 1.0. "
        "Amendment 1 predicted it would approach zero there. It does not, and the reason is "
        "the structural argument the amendment itself makes: at ADS = 1.0 the only move the "
        "rule can make is to abstain, and in the blocks where it abstains often the vote "
        "wins by a wide and decidable margin. The collapse Amendment 1 conceded is real in "
        "the pooled gap but not in the decided-winner rate, and the top ADS band holds "
        "{:,} of the {:,} blocks in the primary analysis population.".format(
            " / ".join("{}={:.4f}".format(a, v) for a, v in zip(ads.ads_band, rates)),
            rates[dip], ads.ads_band.iloc[dip], rates[-1],
            int(ads.n_blocks.iloc[-1]), len(bk)),
        "",
        "**3. SV, not ADS, is the stronger driver of decidability.** Addendum 1a's clause "
        "fails, and it fails under **both** required measures rather than splitting: "
        "eta2_ADS {:.4f} against eta2_SV {:.4f}, averaged ranges {:.4f} against {:.4f}. It "
        "fails at every margin on the robustness curve and at every k on the mandatory "
        "curve, so it is neither margin-dependent nor k-dependent. Dropping the structural "
        "ADS = 1.0 row widens the gap rather than closing it, {:.4f} against {:.4f}, so the "
        "failure is not an artifact of the row Amendment 1 conceded. This is the clause H2 "
        "needed ADS to win. It does not decide H2, because the power floor is evaluated "
        "first, but it is the sharpest measurement in this pass and it points against the "
        "role assignment the 2.2d reframe adopted.".format(
            drv["eta2_ADS"], drv["eta2_SV"], drv["avg_range_ADS"], drv["avg_range_SV"],
            sub["eta2_ADS"], sub["eta2_SV"]),
        "",
        "**4. There is no SV-driven winner reversal anywhere below ADS = 1.0, at any "
        "margin.** The strongest structure the frozen rules find below the top band is a "
        "tie-crossing at delta = 0.02. Substantively the shape is the pre-registered **gap "
        "compression** one: at fixed ADS the gap rises with SV and changes sign, but only "
        "the high-SV side ever clears a margin. Under the frozen rules that reading is a "
        "hypothesis outcome only above the power floor, which the primary margin does not "
        "clear, so it is reported here as substance and not as H3 Not supported.",
        "",
        "**One pre-registration ambiguity, found at run time and handled by reporting both "
        "readings.** Amendment 1's H2 Supported row reads: holding SV fixed, the "
        "decided-winner rate is non-increasing across ADS bands in the majority of eligible "
        "SV bands, **and** is strictly lower in the top ADS band than in the bottom. The "
        "second clause admits two constructions, within each eligible SV band or on the "
        "marginal ADS bands, and they disagree here. Per SV band it holds in {} of {} usable "
        "bands, so not a majority; marginally it holds. Both are printed in the H2 facts "
        "above and neither was picked after seeing which way it fell. The disagreement "
        "changes no outcome, because H2 is Inconclusive on the power floor, which is "
        "evaluated first. It is recorded so that the construction is fixed before it can "
        "matter.".format(int(g["per_sv"].top_below_bottom.sum(skipna=True)),
                         g["usable_sv_bands"]),
        "",
        "**What this leaves for Phase 2.3.** The blocking issue of 2.2b is gone: the pair is "
        "two-sided, `rule wins` is reachable, and {:,} blocks carry a decided per-block "
        "verdict at the primary margin, so a selector has something to select over. What the "
        "pass does not supply is a measured basis for the two-signal role assignment, "
        "because the one pre-registered clause that tested it came out against ADS. Whether "
        "2.3 proceeds on the amended framing, and what charter invariant 4's ADS-only and "
        "SV-only baselines should now be expected to show, is a decision for review and not "
        "for this pass.".format(n_decided),
        "",
    ]


def summary(o1, o2, o3, bk, grids, dec, ts, out):
    n = bk.n_test.sum()
    prim_gap = (bk.rule_correct.sum() - bk["knn_correct_" + PRIMARY].sum()) / n
    drv = dec["driver"][DELTA_PRIMARY]
    return [
        "## What this pass found, in short",
        "",
        "**H1 {}. H2 {}. H3 {}.** The rules behind those three words are in the amended "
        "falsification table at the end of this report; nothing was decided by "
        "inspection.".format(o1, o2, o3),
        "",
        "1. **The mechanism pair is two-sided on the evaluation split.** `rule wins` was "
        "structurally unreachable in 2.2b and measured zero on 199,713 signatures. Here the "
        "rule is right and the k-nearest vote wrong on **{:,}** test signatures, against "
        "**{:,}** the other way, at k = 5. A winner exists to be predicted.".format(
            int(ts[(ts.arm == 'levenshtein') & (ts.k == K_PRIMARY)]['A right, B wrong'].iloc[0]),
            int(ts[(ts.arm == 'levenshtein') & (ts.k == K_PRIMARY)]['B right, A wrong'].iloc[0])),
        "",
        "2. **Pooled, the two mechanisms are close.** Rule accuracy {:.4f} against k-NN "
        "{:.4f}, a pooled gap of {:+.4f}, with the rule abstaining on {:.2%} of test "
        "signatures and the vote never abstaining.".format(
            bk.rule_correct.sum() / n, bk["knn_correct_" + PRIMARY].sum() / n, prim_gap,
            1 - bk.rule_fires_n.sum() / n),
        "",
        "3. **Decidability and its drivers.** The decided-winner rate over the primary "
        "population is {:.4f} at delta = 0.05. Over the eligible cells of the frozen grid, "
        "eta2_ADS = {:.4f} against eta2_SV = {:.4f}, and the averaged ranges are {:.4f} "
        "against {:.4f}. Addendum 1a requires ADS to win under both; the clause comes out "
        "**{}**.".format(
            float(bk["bverdict_{}_{:.2f}".format(PRIMARY, DELTA_PRIMARY)].isin(DECIDED).mean()),
            drv["eta2_ADS"], drv["eta2_SV"], drv["avg_range_ADS"], drv["avg_range_SV"],
            drv["clause"]),
        "",
        "Nothing here was re-tuned, re-banded or redefined. Section 7 is void, k is fixed by "
        "definition, and the band edges and margins are the ones committed before 2.2b ran.",
        "",
    ]


# --------------------------------------------------------------------------
# 7. main
# --------------------------------------------------------------------------

def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    print("== mandatory regression check ==")
    from phase2e_mech import main as regression_main
    regr = regression_main()
    print("== regression check cleared; reading the evaluation split ==")

    blocks = pd.read_parquet(BLOCKS_CACHE)
    sig = load_signatures()
    verify_no_leakage(sig, blocks)

    ev = blocks[~blocks.is_cal]
    prim = ev[(ev.n_train >= 2) & (ev.n_test >= 1)]
    print("evaluation blocks {:,}  primary population {:,}".format(len(ev), len(prim)))

    res = mechanism_pass(sig, ev)
    bk_all = block_verdicts(score_blocks(res, ev))
    bk = bk_all[(bk_all.n_train >= 2) & (bk_all.n_test >= 1)].copy()
    bk2 = bk_all[bk_all.n_train < 2].copy()

    bk["ads_band"] = [ads_band(v) for v in bk.ads]
    bk["sv_band"] = [sv_band(v, *SV_BAND_EDGES) for v in bk.sv]
    bk["svr_band"] = [sv_band(v, *SV_RESID_BAND_EDGES) for v in bk.sv_resid]
    bk["init_band"] = [init_band(v) for v in bk.init]
    dump(bk, "phase2e_blocks_scored.csv.gz")

    body = []
    section_regression_check(regr, body)
    ts = section_accuracy(bk, bk2, body)
    h1 = section_h1(bk, body)
    grids = section_winner(bk, body)
    dec = section_decidability(bk, grids, body)
    kcurve, _ = section_k_curve(bk, body)
    section_power(bk, body)
    tables, gen = section_structure(bk, grids, body)
    section_diagnostics(bk, grids, body)
    o1, o2, o3, _, _ = section_falsification(h1, dec, tables, grids, gen, kcurve, bk, body)
    section_epilogue(dec, grids, bk, body)

    out = header(blocks, ev, prim, bk, bk2, sig)
    out += summary(o1, o2, o3, bk, grids, dec, ts, body)
    out += body
    REPORT.write_text("\n".join(out), encoding="utf-8")
    print("wrote", REPORT)
    print("H1: {}   H2: {}   H3: {}".format(o1, o2, o3))


if __name__ == "__main__":
    demo()
    main()
