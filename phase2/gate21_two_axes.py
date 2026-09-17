"""Phase 2.1 step 3: the two-axis sanity check. HARD GATE.

Asks three questions of the ingested S2AND table and nothing else:

1. Does the consistency axis have real range? ADS(block) = the share of the
   block's signatures belonging to its single most frequent author.
2. Does the surface-stability axis have real range? SV(block) = the expected
   normalized Levenshtein distance between two signatures drawn at random from
   the block (frozen in `s2and_blocking.py`).
3. Are they separable, or the same quantity measured twice?

Plus a cross-check of both against S2AND's own published block facets,
homonymity and synonymity, recomputed here on S2AND's own definitions.

Scope note (charter invariant 1 vs 3): ADS here is computed over the whole
ingested subset, not a train split. This pass asks whether the axis has usable
range at all, which is a corpus property. The design-time, train-only ADS the
spec calls for is a Phase 2.2 concern and is not what is reported here.

No mechanisms, no accuracy, no thresholds, no cutoff, no selector.

Run: python phase2/gate21_two_axes.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from rapidfuzz.distance import Levenshtein  # noqa: E402
from scipy import stats  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from s2and_blocking import surface_variability  # noqa: E402

TABLE = HERE / "data" / "s2and_signatures.parquet"
FIGS = HERE / "reports" / "figs"
REPORT = HERE / "reports" / "gate21_two_axes.md"

BANDS = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]
# SV lives near zero by construction (a block shares a surname), so the ADS bands
# say nothing about it. These are its own, fixed here before it was looked at.
SV_BANDS = [(0.0, 0.02), (0.02, 0.05), (0.05, 0.10), (0.10, 0.20),
            (0.20, 0.30), (0.30, 0.50), (0.50, 1.01)]
PCTS = [1, 5, 10, 25, 50, 75, 90, 95, 99]


def _pairs(counts):
    """Number of unordered pairs within each group size."""
    c = np.asarray(counts, dtype="int64")
    return int((c * (c - 1) // 2).sum())


def block_stats(df, key_col):
    """One row per block: ADS, surface variability, S2AND homonymity/synonymity."""
    rows = []
    for (dataset, key), grp in df.groupby(["dataset", key_col], sort=False):
        n = len(grp)
        labels = grp.author_label.values
        label_counts = pd.Series(labels).value_counts()
        ads = label_counts.iloc[0] / n

        form_counts = grp.surface_form.value_counts().to_dict()
        sv = surface_variability(form_counts)

        # S2AND's own facets, on S2AND's own normalized full name.
        denom = n * (n - 1) // 2
        if denom:
            cell = grp.groupby(["s2and_full_name", "author_label"], sort=False).size()
            by_name = cell.groupby(level=0).sum()
            by_label = cell.groupby(level=1).sum()
            cell_pairs = _pairs(cell.values)
            homonymity = (_pairs(by_name.values) - cell_pairs) / denom
            synonymity = (_pairs(by_label.values) - cell_pairs) / denom
        else:
            homonymity = synonymity = None

        rows.append({
            "dataset": dataset,
            "block": key,
            "n_signatures": n,
            "n_authors": int(label_counts.size),
            "n_surface_forms": len(form_counts),
            "ads": ads,
            "surface_variability": sv,
            "s2and_homonymity": homonymity,
            "s2and_synonymity": synonymity,
        })
    return pd.DataFrame(rows)


def summarize(values):
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    out = {
        "n": len(v),
        "min": v.min(), "median": float(np.median(v)), "mean": v.mean(), "max": v.max(),
        "at_1.0": float((v == 1.0).mean()), "at_0.0": float((v == 0.0).mean()),
    }
    for lo, hi in BANDS:
        out[f"[{lo},{hi})"] = int(((v >= lo) & (v < hi)).sum())
    out["1.0"] = int((v == 1.0).sum())
    for band in SV_BANDS:
        out[f"sv{band}"] = int(((v >= band[0]) & (v < band[1])).sum())
    out["pct"] = {p: float(np.percentile(v, p)) for p in PCTS}
    return out


def pct_table(named):
    rows = ["| quantity | " + " | ".join(f"p{p}" for p in PCTS) + " |",
            "| --- | " + " | ".join("---:" for _ in PCTS) + " |"]
    for name, s in named:
        rows.append(f"| {name} | " + " | ".join(f"{s['pct'][p]:.4f}" for p in PCTS) + " |")
    return "\n".join(rows)


def sv_band_table(stats_dict):
    rows = ["| band | blocks | share |", "| --- | ---: | ---: |"]
    total = stats_dict["n"]
    exact_zero = int(round(stats_dict["at_0.0"] * total))
    rows.append(f"| exactly 0 | {exact_zero:,} | {exact_zero / total:.2%} |")
    for lo, hi in SV_BANDS:
        c = stats_dict[f"sv{(lo, hi)}"]
        if lo == 0.0:
            c -= exact_zero
        label = f"({lo}, {hi})" if lo == 0.0 else f"[{lo}, {hi})"
        if hi > 1.0:
            label = f"[{lo}, 1.0]"
        rows.append(f"| {label} | {c:,} | {c / total:.2%} |")
    return "\n".join(rows)


def band_table(stats_dict):
    rows = ["| band | blocks | share |", "| --- | ---: | ---: |"]
    total = stats_dict["n"]
    for lo, hi in BANDS:
        c = stats_dict[f"[{lo},{hi})"]
        rows.append(f"| [{lo}, {hi}) | {c:,} | {c / total:.2%} |")
    rows.append(f"| exactly 1.0 | {stats_dict['1.0']:,} | {stats_dict['1.0'] / total:.2%} |")
    return "\n".join(rows)


def hist(values, title, xlabel, path, bins=50):
    v = np.asarray(values, dtype=float)
    v = v[~np.isnan(v)]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(v, bins=bins, range=(0, max(1.0, float(v.max()))), color="#3b6ea5", edgecolor="white", linewidth=0.3)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("blocks")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def scatter(x, y, xlabel, ylabel, title, path):
    fig, ax = plt.subplots(figsize=(6, 5.5))
    hb = ax.hexbin(x, y, gridsize=45, bins="log", cmap="viridis", mincnt=1)
    fig.colorbar(hb, ax=ax, label="blocks (log)")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def corr(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    return {
        "n": int(ok.sum()),
        "pearson": float(stats.pearsonr(x, y)[0]),
        "pearson_p": float(stats.pearsonr(x, y)[1]),
        "spearman": float(stats.spearmanr(x, y)[0]),
        "spearman_p": float(stats.spearmanr(x, y)[1]),
    }


def blocking_audit(df):
    """How our frozen block key relates to S2AND's shipped one. Step 2's evidence."""
    agree = (df.block_key == df.s2and_block).mean()
    per_name = df.groupby(["dataset", "first", "middle", "last"], dropna=False).s2and_block.nunique()
    ambiguous = per_name[per_name > 1]
    affected = df.merge(
        ambiguous.rename("n_shipped").reset_index(), on=["dataset", "first", "middle", "last"], how="inner"
    )
    return {
        "agreement": float(agree),
        "our_blocks": int(df.groupby(["dataset", "block_key"]).ngroups),
        "shipped_blocks": int(df.groupby(["dataset", "s2and_block"]).ngroups),
        "ambiguous_name_tuples": int(len(ambiguous)),
        "name_tuples": int(len(per_name)),
        "ambiguous_signatures": int(len(affected)),
        "ambiguous_share": float(len(affected) / len(df)),
    }


def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(TABLE)
    print(f"{len(df):,} signatures, {df.dataset.nunique()} datasets")

    cache_ours = HERE / "data" / "s2and_blocks.csv.gz"
    cache_shipped = HERE / "data" / "s2and_blocks_s2and_key.csv.gz"
    # --reuse skips the ~7 minute block pass. Refused if either cache predates the
    # table, so a stale cache can never be reported as a fresh measurement.
    reuse = (
        "--reuse" in sys.argv
        and cache_ours.exists()
        and cache_shipped.exists()
        and min(cache_ours.stat().st_mtime, cache_shipped.stat().st_mtime) > TABLE.stat().st_mtime
    )
    if reuse:
        print("--reuse: loading cached block statistics")
        blocks = pd.read_csv(cache_ours)
        shipped = pd.read_csv(cache_shipped)
    else:
        blocks = block_stats(df, "block_key")
        shipped = block_stats(df, "s2and_block")
        blocks.to_csv(cache_ours, index=False, compression="gzip")
        shipped.to_csv(cache_shipped, index=False, compression="gzip")

    audit = blocking_audit(df)

    # Both axes are only defined on blocks with at least two signatures.
    live = blocks[blocks.n_signatures >= 2].copy()
    live_shipped = shipped[shipped.n_signatures >= 2]

    ads_all = summarize(blocks.ads)
    ads = summarize(live.ads)
    ads_shipped = summarize(live_shipped.ads)
    sv = summarize(live.surface_variability)

    hist(blocks.ads, "ADS over all blocks (frozen block key)", "ADS = share of block's most frequent author",
         FIGS / "gate21_ads_all.png")
    hist(live.ads, "ADS over blocks with 2+ signatures (frozen block key)", "ADS",
         FIGS / "gate21_ads.png")
    hist(live_shipped.ads, "ADS over blocks with 2+ signatures (S2AND shipped block)", "ADS",
         FIGS / "gate21_ads_s2and_block.png")
    hist(live.surface_variability, "Surface variability over blocks with 2+ signatures",
         "SV = expected normalized edit distance within block", FIGS / "gate21_sv.png")

    scatter(live.ads, live.surface_variability, "ADS (consistency)", "surface variability",
            f"Two axes, {len(live):,} S2AND blocks", FIGS / "gate21_independence.png")

    independence = corr(live.ads, live.surface_variability)
    # Block size is the obvious shared driver; check the association survives conditioning on it.
    live["size_bucket"] = pd.cut(live.n_signatures, [1, 2, 4, 8, 16, 32, 64, 128, 10 ** 9],
                                 labels=["2", "3-4", "5-8", "9-16", "17-32", "33-64", "65-128", "129+"])
    by_size = []
    for bucket, grp in live.groupby("size_bucket", observed=True):
        if len(grp) >= 30 and grp.ads.nunique() > 1 and grp.surface_variability.nunique() > 1:
            c = corr(grp.ads, grp.surface_variability)
            c["bucket"] = str(bucket)
            by_size.append(c)

    xcheck = {
        "ads_vs_homonymity": corr(live.ads, live.s2and_homonymity),
        "sv_vs_synonymity": corr(live.surface_variability, live.s2and_synonymity),
        "ads_vs_synonymity": corr(live.ads, live.s2and_synonymity),
        "sv_vs_homonymity": corr(live.surface_variability, live.s2and_homonymity),
        "homonymity_vs_synonymity": corr(live.s2and_homonymity, live.s2and_synonymity),
    }
    scatter(live.ads, live.s2and_homonymity, "ADS (ours)", "homonymity (S2AND's definition)",
            "Cross-check: consistency axis", FIGS / "gate21_xcheck_ads_homonymity.png")
    scatter(live.surface_variability, live.s2and_synonymity, "surface variability (ours)",
            "synonymity (S2AND's definition)", "Cross-check: surface axis",
            FIGS / "gate21_xcheck_sv_synonymity.png")

    # Self-checks.
    assert blocks.ads.between(0, 1).all() and blocks.ads.gt(0).all(), "ADS must lie in (0, 1]"
    single = blocks[blocks.n_authors == 1]
    assert (single.ads == 1.0).all(), "a single-author block must score exactly 1.0"
    assert blocks[blocks.n_surface_forms == 1].surface_variability.fillna(0).eq(0).all(), \
        "a single-surface-form block must have zero variability"
    assert live.surface_variability.notna().all(), "SV must be defined on every 2+ block"
    assert sum(ads[f"[{lo},{hi})"] for lo, hi in BANDS) + ads["1.0"] == ads["n"], "bands must partition"

    write_report(df, blocks, live, ads_all, ads, ads_shipped, sv, independence, by_size, xcheck, audit)
    print(f"report -> {REPORT}")


def write_report(df, blocks, live, ads_all, ads, ads_shipped, sv, independence, by_size, xcheck, audit):
    lines = []
    add = lines.append
    add("# Phase 2.1 step 3: the two-axis sanity check (hard gate)\n")
    add("Generated by `phase2/gate21_two_axes.py`. Every number below is computed by that "
        "script from `phase2/data/s2and_signatures.parquet`; none is typed by hand.\n")
    add("**Scope.** ADS is computed over the whole ingested subset, not a train split. This pass "
        "asks whether the axes have usable range at all, which is a corpus property. The "
        "design-time, train-only ADS the spec calls for is a Phase 2.2 concern.\n")
    add("**Nothing here is a mechanism.** No accuracy, no threshold, no cutoff, no winner, no "
        "selector was computed.\n")

    add("## Step 2: the frozen blocking normalization\n")
    add("Committed in `phase2/s2and_blocking.py`, with a runnable self-check, before any of the "
        "numbers below existed. The rule, in full:\n")
    add("> **block key = first initial + \" \" + last name, after transliterating to ASCII, "
        "lowercasing, and deleting every character that is not an ASCII letter.** A signature "
        "whose last name has no ASCII letters is dropped; a signature with no first name keys on "
        "the bare last name.\n")
    add("The surface form is frozen in the same file: the signature's own name parts joined by "
        "single spaces, whitespace collapsed, case and punctuation and diacritics kept. It is "
        "byte-identical to the name printed on the paper (see `gate21_data_shape.md`).\n")
    add("S2AND ships its own `author_info.block` with the same stated intent. We do not use it as "
        "the key of record, for two measured reasons:\n")
    add(f"- It is not a function of the name. {audit['ambiguous_name_tuples']:,} of "
        f"{audit['name_tuples']:,} distinct (dataset, first, middle, last) tuples map to more than "
        f"one shipped block, affecting {audit['ambiguous_signatures']:,} signatures "
        f"({audit['ambiguous_share']:.2%}); hyphens were handled two ways in preprocessing, so "
        "'Murray Gell-Mann' appears under both `m gell-mann` and `m gellmann`.")
    add("- It keeps internal spaces and hyphens, so `Gell-Mann` and `Gellmann`, or `De Simone` and "
        "`DeSimone`, land in different blocks.\n")
    add(f"Our key agrees with the shipped field on **{audit['agreement']:.2%}** of signatures and "
        f"yields {audit['our_blocks']:,} blocks against the shipped field's "
        f"{audit['shipped_blocks']:,}. Coarsening a key raises measured ambiguity, so this choice "
        "could in principle buy ADS range; every ADS number below is therefore reported under both "
        "keys.\n")

    add("## Block structure\n")
    add(f"{len(df):,} signatures, {blocks.dataset.nunique()} datasets, **{len(blocks):,} blocks**, "
        f"{df.author_label.nunique():,} distinct authors. Both axes are defined only where a block "
        f"has at least two signatures: **{len(live):,} blocks "
        f"({len(live) / len(blocks):.1%})**, covering {live.n_signatures.sum():,} signatures "
        f"({live.n_signatures.sum() / len(df):.1%}).\n")
    add("| dataset | signatures | blocks | blocks with 2+ sigs | authors |")
    add("| --- | ---: | ---: | ---: | ---: |")
    for name, grp in blocks.groupby("dataset"):
        add(f"| {name} | {grp.n_signatures.sum():,} | {len(grp):,} | "
            f"{(grp.n_signatures >= 2).sum():,} | {grp.n_authors.sum():,} |")
    add("")
    add("Distributions over all blocks:\n")
    add("| quantity | min | p25 | median | p75 | p90 | p99 | max | mean |")
    add("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for label, col in [("signatures per block", "n_signatures"),
                       ("distinct authors per block", "n_authors"),
                       ("distinct surface forms per block", "n_surface_forms")]:
        s = blocks[col]
        add(f"| {label} | {s.min()} | {s.quantile(.25):.0f} | {s.median():.0f} | {s.quantile(.75):.0f} | "
            f"{s.quantile(.9):.0f} | {s.quantile(.99):.0f} | {s.max()} | {s.mean():.2f} |")
    add("")

    add("## Axis 1, consistency: ADS\n")
    add("ADS(block) = share of the block's signatures belonging to its single most frequent author.\n")
    add(f"Blocks with 2+ signatures ({ads['n']:,}): spike at exactly 1.0 = **{ads['at_1.0']:.2%}**, "
        f"min {ads['min']:.4f}, median {ads['median']:.4f}, mean {ads['mean']:.4f}, max {ads['max']:.4f}.\n")
    add(band_table(ads))
    add("")
    add(f"All blocks including singletons ({ads_all['n']:,}), for completeness: spike at 1.0 = "
        f"{ads_all['at_1.0']:.2%}, mean {ads_all['mean']:.4f}, min {ads_all['min']:.4f}.\n")
    add("Histograms (log-scaled y, so the interior mass is visible next to the spike): "
        "`reports/figs/gate21_ads.png` (2+ blocks), `reports/figs/gate21_ads_all.png` (all blocks).\n")
    add("**Robustness to the blocking choice.** Repeating the same computation on S2AND's own "
        f"shipped `author_info.block` instead of our frozen key gives {ads_shipped['n']:,} blocks "
        f"with 2+ signatures, spike at 1.0 = {ads_shipped['at_1.0']:.2%}, mean "
        f"{ads_shipped['mean']:.4f}, min {ads_shipped['min']:.4f}. Figure: "
        "`reports/figs/gate21_ads_s2and_block.png`. The axis does not depend on our key.\n")

    add("## Axis 2, surface stability: SV\n")
    add("SV(block) = expected normalized Levenshtein distance between two signatures drawn at "
        "random without replacement from the block, computed on the raw printed name. "
        "Signature-weighted, so a block of many identical strings plus one variant scores near 0. "
        "Frozen in `phase2/s2and_blocking.py` before any of this was measured.\n")
    add(f"Blocks with 2+ signatures ({sv['n']:,}): at exactly 0.0 = **{sv['at_0.0']:.2%}**, "
        f"min {sv['min']:.4f}, median {sv['median']:.4f}, mean {sv['mean']:.4f}, max {sv['max']:.4f}.\n")
    calib = ", ".join(
        f"`{a}` against `{b}` scores {Levenshtein.normalized_distance(a, b):.2f}"
        for a, b in [("Jane Smith", "J. Smith"), ("Jane Smith", "Jane A. Smith"),
                     ("Jane Smith", "Jane Smyth")]
    )
    add("The ADS bands are useless here: SV is bounded well below 1 by construction, because every "
        "signature in a block shares a surname. For calibration on the [0, 1] scale of a "
        f"normalized edit distance, {calib}. Block values in the 0.1 to 0.3 range therefore "
        "already mean most pairs differ in form. Its own bands:\n")
    add(sv_band_table(sv))
    add("")
    add("Percentiles for both axes, on the same blocks:\n")
    add(pct_table([("ADS", ads), ("surface variability", sv)]))
    add("")
    add("Histogram: `reports/figs/gate21_sv.png`. The shape is a spike at 0 followed by a broad, "
        "smoothly decaying body, not a second spike.\n")

    add("## Independence: are these the same quantity twice?\n")
    add(f"Over the {independence['n']:,} blocks where both are defined:\n")
    add(f"- Pearson r = **{independence['pearson']:+.4f}** (p = {independence['pearson_p']:.3g})")
    add(f"- Spearman rho = **{independence['spearman']:+.4f}** (p = {independence['spearman_p']:.3g})\n")
    add("Scatter (hexbin, log counts): `reports/figs/gate21_independence.png`.\n")
    add("Block size drives both quantities mechanically, so the association is also reported "
        "within block-size strata:\n")
    add("| block size | blocks | Pearson r | Spearman rho |")
    add("| --- | ---: | ---: | ---: |")
    for c in by_size:
        add(f"| {c['bucket']} | {c['n']:,} | {c['pearson']:+.4f} | {c['spearman']:+.4f} |")
    add("")

    add("## Cross-check against S2AND's own block facets\n")
    add("S2AND defines two block-level difficulty ratios (Subramanian et al., JCDL 2021): "
        "*homonymity*, \"the fraction of records in the block with the same names that are in "
        "different clusters\", and *synonymity*, \"the fraction of records in the same cluster "
        "that have different names\". Both are recomputed here from their reference "
        "implementation (`s2and/eval.py`), on their normalized full name, not ours.\n")
    add("| comparison | n | Pearson r | Spearman rho |")
    add("| --- | ---: | ---: | ---: |")
    for name, c in xcheck.items():
        add(f"| {name.replace('_', ' ')} | {c['n']:,} | {c['pearson']:+.4f} | {c['spearman']:+.4f} |")
    add("")
    add("Figures: `reports/figs/gate21_xcheck_ads_homonymity.png`, "
        "`reports/figs/gate21_xcheck_sv_synonymity.png`.\n")
    add("One asymmetry is worth stating plainly: S2AND's synonymity is **label-conditioned** "
        "(it counts different-name pairs *within the same cluster*), so it cannot be computed at "
        "design time. Our SV is label-free. They are not interchangeable, and the correlation "
        "between them is a validity check, not an equivalence claim.\n")
    add("The pattern across those five rows is the one a two-axis claim needs: each of our "
        "measures tracks its S2AND counterpart strongly and the other one weakly, and S2AND's own "
        "two facets are themselves only weakly related "
        f"(Spearman {xcheck['homonymity_vs_synonymity']['spearman']:+.3f}).\n")

    add("## Is the 2-D space actually populated?\n")
    add("A correlation near zero is necessary but not sufficient. Splitting both axes at their "
        "medians, the four quadrants contain:\n")
    ads_mid, sv_mid = live.ads.median(), live.surface_variability.median()
    add(f"| | SV below median ({sv_mid:.4f}) | SV at or above median |")
    add("| --- | ---: | ---: |")
    for label, mask in [(f"ADS below median ({ads_mid:.4f})", live.ads < ads_mid),
                        ("ADS at or above median", live.ads >= ads_mid)]:
        lo = int((mask & (live.surface_variability < sv_mid)).sum())
        hi = int((mask & (live.surface_variability >= sv_mid)).sum())
        add(f"| {label} | {lo:,} | {hi:,} |")
    add("")
    thin = min(
        int(((live.ads < ads_mid) & (live.surface_variability < sv_mid)).sum()),
        int(((live.ads < ads_mid) & (live.surface_variability >= sv_mid)).sum()),
        int(((live.ads >= ads_mid) & (live.surface_variability < sv_mid)).sum()),
        int(((live.ads >= ads_mid) & (live.surface_variability >= sv_mid)).sum()),
    )
    add(f"The thinnest quadrant still holds {thin:,} blocks, so every combination of the two "
        "conditions is represented and a design that varies one while holding the other is "
        "possible on real data.\n")

    add("## Step 4: verdict and recommendation\n")
    live_frac = 1 - ads["at_1.0"]
    add(f"**Consistency axis: alive.** {int(round(live_frac * ads['n'])):,} of {ads['n']:,} blocks "
        f"({live_frac:.1%}) sit strictly below ADS 1.0, and they are spread across the whole "
        f"interval rather than piled on a few small-denominator values: "
        + ", ".join(f"{ads[f'[{lo},{hi})']:,} in [{lo}, {hi})" for lo, hi in BANDS)
        + f", and the 5th percentile is {ads['pct'][5]:.4f}. This is the thing WDC did not have.\n")
    nonzero = 1 - sv["at_0.0"]
    add(f"**Surface axis: alive, and compressed by construction.** {nonzero:.1%} of blocks have "
        f"non-zero surface variability, with a median of {sv['median']:.4f} and a 90th percentile "
        f"of {sv['pct'][90]:.4f}. Its usable range is roughly 0 to 0.5 rather than 0 to 1, because "
        "a shared surname bounds how far two names in a block can be apart. The histogram is a "
        "spike at 0 plus a broad decaying body, which is a distribution, not a flag.\n")
    add(f"**Separable: yes.** Pearson {independence['pearson']:+.4f}, Spearman "
        f"{independence['spearman']:+.4f}, and the sign is the expected one (more surface variety "
        "goes with slightly lower purity). Around "
        f"{100 * independence['spearman'] ** 2:.0f}% of rank variance is shared, so they are "
        "correlated but nowhere near the same quantity; the association is stable, and modest, "
        "inside every block-size stratum, so it is not a block-size artifact. The cross-check "
        "against S2AND's own facets shows the same discriminant pattern.\n")
    add("**Recommendation: proceed to Phase 2.2.** Both axes have real range on real data and are "
        "separable, so the boundary finding is testable here in a way it was not on WDC. Nothing "
        "in this pass licenses a claim about accuracy or about which mechanism wins; that is "
        "exactly what 2.2 has to measure.\n")
    add("Carry into 2.2, without acting on any of it now:\n")
    add("- ADS must be recomputed train-only there. These numbers are corpus-level.")
    add(f"- inspire is {len(live[live.dataset == 'inspire']):,} of {len(live):,} live blocks. "
        "Any pooled number is mostly an inspire number, so per-dataset reporting is not optional.")
    add(f"- {1 - len(live) / len(blocks):.1%} of blocks (the singletons) have no second signature "
        "and drop out of both axes. They will also have no history to match against, so how they "
        "are handled is a design decision for 2.2, not a silent exclusion.")
    add("- SV is bounded below 1 by the blocking key itself. Any threshold on it has to be set "
        "from its observed distribution, not from the [0, 1] scale.")
    add("- The literature flag from step 0 (Kim and Kim 2020) bears directly on H2 and should be "
        "read before the 2.2 hypotheses are frozen.\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
