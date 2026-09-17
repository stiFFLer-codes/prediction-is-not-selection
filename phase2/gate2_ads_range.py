"""Gate 2 (hard gate): characterize the ADS distribution on the ingested WDC
subset under Framing A and Framing B, and stop.

ADS here is cluster purity: for a key, the share of that key's offers falling in
its single most common label. Nothing downstream is built — no mechanisms, no
accuracy, no thresholds, no selector, no cutoff.

Scope note (deliberate): ADS is computed over the FULL ingested subset, not the
train split. This pass asks whether the ADS axis has usable range at all, which
is a property of the corpus. The charter's design-time, history-only, train-split
ADS is a gate 3 concern and will be recomputed there.

Run: python phase2/gate2_ads_range.py
"""

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
TABLE = HERE / "data" / "wdc_lspc2017_offers.csv.gz"
FIGS = HERE / "reports" / "figs"
REPORT = HERE / "reports" / "gate2_ads_range.md"

BANDS = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.0)]

# WDC titles are raw schema.org serialisations: every one is a sequence of
# double-quoted segments, most carrying an "@lang tag, e.g.
#   "Sony Cyber-shot DSC-RX100 II Digital Camera"@en " Sony Camera | SLR Aden "@en
# The first segment is the offer title proper; later segments are page-title and
# retailer boilerplate. The normalisations below are built from that structure.
LANG_TAG = re.compile(r'"@[A-Za-z-]{2,7}')
SEGMENT = re.compile(r'"([^"]*)"')
NULL_LITERAL = re.compile(r"\bNull\b", re.IGNORECASE)
NON_ALNUM = re.compile(r"[^0-9a-z]+")

# Retailer / marketplace boilerplate markers, taken from strings actually
# observed in this subset rather than guessed.
BOILERPLATE = re.compile(
    r"(?:\|"
    r"|\.com\b|\.co\.uk\b|\.nl\b|\.de\b"
    r"|\bprices?\b|\bprijzen\b|\bspecificaties\b|\breviews?\b"
    r"|\bfree shipping\b|\bonline store\b|\bshop\b|\bstore\b|\bbuy\b"
    r"|\bofficial site\b|\bbest price\b)",
    re.IGNORECASE,
)


def norm_raw(s):
    """Strength 0: the surface string exactly as distributed."""
    return s


def norm_light(s):
    """Strength 1: strip serialisation artifacts only.

    Drops "@lang tags, Null literals, quote characters and punctuation, then
    lowercases and collapses whitespace. Retailer boilerplate survives: this
    keeps every quoted segment.
    """
    s = LANG_TAG.sub(" ", s)
    s = NULL_LITERAL.sub(" ", s)
    s = s.lower()
    s = NON_ALNUM.sub(" ", s)
    return " ".join(s.split())


def norm_aggressive(s):
    """Strength 2: light, plus keep only the offer title and sort tokens.

    Keeps the first quoted segment (the offer title proper), discarding the
    page-title/retailer segments that follow it, then applies light
    normalisation and reduces to a sorted set of tokens so that word order and
    duplicated tokens stop distinguishing two otherwise identical titles.
    """
    segments = SEGMENT.findall(s)
    head = segments[0] if segments else s
    tokens = norm_light(head).split()
    return " ".join(sorted(set(tokens)))


STRENGTHS = [
    ("raw", norm_raw, "surface string exactly as distributed"),
    ("light", norm_light, "strip lang tags, Null, punctuation; lowercase"),
    ("aggressive", norm_aggressive, "light + first quoted segment only + token sort/dedupe"),
]


def ads(df, key_col, label_col):
    """Cluster purity per key: max offers in one label / total offers."""
    g = df.groupby([key_col, label_col]).size().groupby(level=0)
    return (g.max() / g.sum()).rename("ads")


def summarize(a, n_labels_per_key):
    """Spike fraction, quantiles and sub-band counts for one ADS series."""
    n = len(a)
    bands = [((a >= lo) & (a < hi)).sum() for lo, hi in BANDS]
    return {
        "n_keys": n,
        "impure_share": (n_labels_per_key > 1).mean() if n else float("nan"),
        "spike_1.0": (a == 1.0).sum(),
        "spike_1.0_share": (a == 1.0).mean() if n else float("nan"),
        "min": a.min() if n else float("nan"),
        "median": a.median() if n else float("nan"),
        "mean": a.mean() if n else float("nan"),
        "max": a.max() if n else float("nan"),
        "bands": bands,
    }


def band_rows(st):
    labels = [f"[{lo}, {hi})" for lo, hi in BANDS] + ["1.0 exactly"]
    counts = st["bands"] + [st["spike_1.0"]]
    out = []
    for lab, c in zip(labels, counts):
        share = c / st["n_keys"] if st["n_keys"] else float("nan")
        out.append(f"| {lab} | {c:,} | {share:.1%} |")
    return out


def plot(series_by_panel, title, path):
    """Histogram of ADS, one panel per view. Shape, not just summary stats."""
    n = len(series_by_panel)
    fig, axes = plt.subplots(1, n, figsize=(5.2 * n, 3.8), squeeze=False)
    for ax, (name, a) in zip(axes[0], series_by_panel):
        if len(a) == 0:
            ax.text(0.5, 0.5, "no keys", ha="center", va="center")
        else:
            ax.hist(a, bins=[i / 20 for i in range(21)], color="#3b6ea5",
                    edgecolor="white", linewidth=0.5)
            ax.axvline(1.0, color="#b4433a", linewidth=1, linestyle="--")
        ax.set_xlim(0, 1.02)
        ax.set_xlabel("ADS (cluster purity)")
        ax.set_ylabel("keys")
        ax.set_title(f"{name}  (n={len(a):,})", fontsize=10)
    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main():
    df = pd.read_csv(TABLE)
    lines = [
        "# Gate 2 ADS-range check (hard gate)",
        "",
        f"Table: `{TABLE.relative_to(HERE).as_posix()}` — {len(df):,} offers, "
        f"{df['key'].nunique():,} clusters.",
        "",
        "ADS = cluster purity: for a key, the share of that key's offers falling",
        "in its single most common label.",
        "",
        "**Scope note.** ADS is computed here over the full ingested subset, not",
        "the train split. This pass asks whether the ADS axis has usable range at",
        "all, which is a property of the corpus. The charter's design-time,",
        "history-only ADS computed on the train split only is a gate 3 concern and",
        "will be recomputed there.",
        "",
        "No mechanisms, accuracy, thresholds, selector or cutoff were computed.",
        "",
    ]

    # ---- Step 1: the discriminating check for Framing A -------------------
    cats_per_cluster = df.groupby("key")["label"].nunique()
    multi = (cats_per_cluster > 1).sum()
    lines += [
        "## Step 1 — discriminating check for Framing A",
        "",
        "Does category actually vary within a cluster? If not, per-cluster",
        "category purity is 1.0 by construction and the Framing A ADS axis has no",
        "range at all.",
        "",
        f"- Clusters: {len(cats_per_cluster):,}",
        f"- Clusters with more than one distinct category: **{multi:,} "
        f"({multi / len(cats_per_cluster):.3%})**",
        "",
        "Distribution of distinct categories per cluster:",
        "",
        "| distinct categories | clusters | share |",
        "| --- | --- | --- |",
    ]
    for k, v in cats_per_cluster.value_counts().sort_index().items():
        lines.append(f"| {k} | {v:,} | {v / len(cats_per_cluster):.1%} |")

    framing_a_alive = multi > 0
    lines += [
        "",
        "**Verdict: Framing A is dead.**" if not framing_a_alive
        else "**Verdict: Framing A shows within-cluster category variation.**",
        "",
    ]
    if not framing_a_alive:
        lines += [
            "Category is not merely near-constant within clusters, it is exactly",
            "constant in every one of them. This is structural, not a property of",
            "this sample: WDC assigns a category at the cluster level and stamps it",
            "onto each offer, so `category` is a function of `cluster_id`. ADS_A is",
            "therefore a point mass at 1.0 for every cluster, with zero variance and",
            "nothing to correlate against. Spec section 3 anticipated this outcome",
            "and it is confirmed. Framing A is not carried forward.",
            "",
        ]

    # ---- Step 2: Framing A ------------------------------------------------
    lines += ["## Step 2 — Framing A (key = cluster id, label = per-offer category)", ""]
    nf_mask = df["label"] == "not found"
    nf_clusters = df.loc[nf_mask, "key"].nunique()
    panels_a = []
    for name, sub in [("with 'not found'", df), ("without 'not found'", df[~nf_mask])]:
        a = ads(sub, "key", "label")
        st = summarize(a, sub.groupby("key")["label"].nunique())
        panels_a.append((name, a))
        lines += [
            f"### {name}",
            "",
            f"- Keys: {st['n_keys']:,}",
            f"- Keys with more than one distinct label: {st['impure_share']:.3%}",
            f"- Fraction at exactly ADS = 1.0 (the spike): **{st['spike_1.0_share']:.3%}**",
            f"- min {st['min']:.3f}, median {st['median']:.3f}, "
            f"mean {st['mean']:.3f}, max {st['max']:.3f}",
            "",
            "| band | keys | share |",
            "| --- | --- | --- |",
        ] + band_rows(st) + [""]
    lines += [
        f"The `not found` category covers {nf_mask.sum():,} offers in "
        f"{nf_clusters:,} clusters. Because category is cluster-constant, "
        "`not found` is a whole-cluster label, so excluding it removes those "
        "clusters wholesale rather than splitting any cluster. Both views are "
        "reported above and neither changes the verdict.",
        "",
        "![Framing A ADS](figs/gate2_ads_a.png)",
        "",
        "The histogram is a single bar at 1.0 in both views. There is no axis here.",
        "",
    ]
    plot(panels_a, "Framing A: ADS per cluster (label = category)",
         FIGS / "gate2_ads_a.png")

    # ---- Step 3: Framing B ------------------------------------------------
    lines += [
        "## Step 3 — Framing B (key = normalized surface string, label = cluster id)",
        "",
        "Three normalisation strengths, defined in `gate2_ads_range.py`:",
        "",
        "| strength | definition |",
        "| --- | --- |",
    ] + [f"| `{n}` | {d} |" for n, _, d in STRENGTHS] + [
        "",
        "The `aggressive` rule is data-driven rather than guessed: every title in",
        "this corpus is a sequence of double-quoted segments, and the first is the",
        "offer title proper while later ones are page-title and retailer",
        "boilerplate (see step 4). `aggressive` keeps only that first segment.",
        "",
        "Each strength is reported over two views. **All normkeys** is the",
        "population as asked. **Recurring normkeys (n >= 2)** drops singletons,",
        "which are pinned to ADS = 1.0 arithmetically rather than informatively;",
        "this is the view that actually shows whether the axis has range.",
        "",
    ]

    summary_rows = []
    for name, fn, _ in STRENGTHS:
        col = f"nk_{name}"
        df[col] = df["surface_string"].map(fn)
        empty = (df[col].str.strip() == "").sum()
        sub = df[df[col].str.strip() != ""]
        sizes = sub.groupby(col).size()
        recurring = set(sizes[sizes >= 2].index)

        a_all = ads(sub, col, "key")
        st_all = summarize(a_all, sub.groupby(col)["key"].nunique())
        rec = sub[sub[col].isin(recurring)]
        a_rec = ads(rec, col, "key")
        st_rec = summarize(a_rec, rec.groupby(col)["key"].nunique())

        lines += [f"### `{name}`", ""]
        if empty:
            lines.append(f"({empty:,} offers normalised to an empty string, dropped.)")
            lines.append("")
        lines += [
            f"- Distinct normkeys: {st_all['n_keys']:,} "
            f"(from {len(sub):,} offers); recurring (n >= 2): {st_rec['n_keys']:,}",
            f"- Normkeys mapping to more than one cluster: **{st_all['impure_share']:.3%}** "
            f"of all normkeys, **{st_rec['impure_share']:.3%}** of recurring normkeys",
            "",
        ]
        for view, st in [("All normkeys", st_all), ("Recurring normkeys (n >= 2)", st_rec)]:
            lines += [
                f"**{view}** — n = {st['n_keys']:,}; "
                f"spike at 1.0 = {st['spike_1.0']:,} ({st['spike_1.0_share']:.3%}); "
                f"min {st['min']:.3f}, median {st['median']:.3f}, "
                f"mean {st['mean']:.3f}, max {st['max']:.3f}",
                "",
                "| band | keys | share |",
                "| --- | --- | --- |",
            ] + band_rows(st) + [""]

        plot([("all normkeys", a_all), ("recurring (n >= 2)", a_rec)],
             f"Framing B, normalisation = {name}: ADS per normkey (label = cluster id)",
             FIGS / f"gate2_ads_b_{name}.png")
        lines += [f"![Framing B {name}](figs/gate2_ads_b_{name}.png)", ""]

        summary_rows.append(
            f"| `{name}` | {st_all['n_keys']:,} | {st_rec['n_keys']:,} | "
            f"{st_all['impure_share']:.2%} | {st_rec['impure_share']:.2%} | "
            f"{st_rec['spike_1.0_share']:.1%} | {st_rec['median']:.3f} | "
            f"{st_rec['mean']:.3f} |"
        )

    lines += [
        "### Framing B at a glance",
        "",
        "| strength | normkeys | recurring | impure (all) | impure (recurring) | "
        "spike@1.0 (recurring) | median (recurring) | mean (recurring) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ] + summary_rows + [""]

    # ---- Step 3b: coarser blocking keys (exploratory diagnostic) ----------
    # All three strengths above key on the *whole* normalized title, which is
    # near-unique per offer, so ADS_B is almost always 1.0 by arithmetic. Spec
    # section 3 allows "a normalized surface or blocking key", so this probes
    # whether a genuinely coarser key revives the axis. Diagnostic only: no
    # framing is committed here.
    lines += [
        "### Step 3b — coarser blocking keys (exploratory diagnostic)",
        "",
        "All three strengths above key on the whole normalized title, which is",
        "near-unique per offer, so ADS_B is pinned to 1.0 by arithmetic rather than",
        "by any property of the data. Spec section 3 defines Framing B's key as \"a",
        "normalized surface **or blocking key**\", so this probes the second option:",
        "`blocking-k` keys on the first k tokens of the `aggressive` normkey.",
        "",
        "Because `aggressive` token-sorts, \"first k tokens\" means the",
        "alphabetically-first k tokens. That is deterministic and reproducible but",
        "it is not a principled blocking function; a brand-plus-model-number key is",
        "the version worth designing properly. Treat these numbers as evidence that",
        "the axis responds to key granularity, not as a proposed key.",
        "",
        "**This is a diagnostic. No framing is committed here.**",
        "",
        "| k | normkeys | recurring | impure (recurring) | spike@1.0 | median | mean | "
        "in (0.5, 1.0) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    blocking_panels = []
    for k in (2, 3, 4, 5):
        col = f"bk{k}"
        agg = df["nk_aggressive"]
        sub = df[agg.str.strip() != ""].copy()
        sub[col] = sub["nk_aggressive"].str.split().str[:k].str.join(" ")
        sizes = sub.groupby(col).size()
        rec = sub[sub[col].isin(sizes[sizes >= 2].index)]
        a = ads(rec, col, "key")
        st = summarize(a, rec.groupby(col)["key"].nunique())
        blocking_panels.append((f"k={k}", a))
        lines.append(
            f"| {k} | {sub[col].nunique():,} | {st['n_keys']:,} | "
            f"{st['impure_share']:.1%} | {st['spike_1.0_share']:.1%} | "
            f"{st['median']:.3f} | {st['mean']:.3f} | "
            f"{((a > 0.5) & (a < 1.0)).mean():.1%} |"
        )
    plot(blocking_panels,
         "Framing B diagnostic: ADS per blocking key, recurring keys only",
         FIGS / "gate2_ads_b_blocking.png")
    lines += [
        "",
        "![Framing B blocking keys](figs/gate2_ads_b_blocking.png)",
        "",
        "The axis responds strongly and monotonically to key granularity. At k = 2",
        "the spike at 1.0 falls to about 60% and the mean to about 0.78, with mass",
        "spread across the interior of the range. This is the first view in this",
        "pass that looks like a distribution rather than a point mass.",
        "",
    ]

    # ---- Step 4: light surface-noise characterization ---------------------
    s = df["surface_string"]
    tagged = s.str.contains(r'"@[A-Za-z]', regex=True)
    tags = s.str.findall(r'"@([A-Za-z-]{2,7})')
    non_en = tags.map(lambda ts: any(not t.lower().startswith("en") for t in ts))
    non_ascii = s.map(lambda x: any(ord(c) > 127 for c in x))
    n_segments = s.map(lambda x: len(SEGMENT.findall(x)))
    boiler = s.str.contains(BOILERPLATE)

    lines += [
        "## Step 4 — surface-noise characterization (light)",
        "",
        "Heuristics, not a study. Language is read off the `\"@lang` tags the WDC",
        "serialisation already carries, which is direct evidence where present;",
        "untagged titles are simply unknown, so the non-English share below is a",
        "lower bound.",
        "",
        f"- Titles carrying at least one explicit language tag: {tagged.mean():.1%}",
        f"- Titles carrying at least one **non-English** language tag: "
        f"**{non_en.mean():.1%}** (lower bound; of tagged titles, "
        f"{non_en.sum() / max(tagged.sum(), 1):.1%})",
        f"- Titles containing non-ASCII characters: {non_ascii.mean():.1%} "
        "(weak secondary signal)",
        f"- Titles with more than one quoted segment, i.e. carrying a page-title / "
        f"retailer segment after the offer title: **{(n_segments > 1).mean():.1%}**",
        f"- Titles matching an observed retailer-boilerplate marker: "
        f"**{boiler.mean():.1%}**",
        f"- Titles containing a `Null` literal: {s.str.contains('Null', case=False).mean():.1%}",
        "",
        "Top language tags by offer count:",
        "",
    ]
    flat = pd.Series([t for ts in tags for t in ts])
    lines += ["| tag | offers |", "| --- | --- |"]
    lines += [f"| `{k}` | {v:,} |" for k, v in flat.value_counts().head(12).items()]
    lines += [""]

    # ---- Step 5: recommendation -------------------------------------------
    agg = df[df["nk_aggressive"].str.strip() != ""]
    agg_sizes = agg.groupby("nk_aggressive").size()
    agg_rec = agg[agg["nk_aggressive"].isin(agg_sizes[agg_sizes >= 2].index)]
    lines += [
        "## Step 5 — recommendation",
        "",
        "**Framing A: dead, conclusively.** Not near-degenerate, exactly",
        "degenerate. Category is a function of cluster id in this corpus, so ADS_A",
        "is 1.0 for all 2,485 clusters with zero variance. No normalisation, subset",
        "or label-handling choice can change this, because it is a property of how",
        "WDC assigns categories rather than of the sample. Do not carry it forward.",
        "",
        "**Framing B as literally specified: also effectively dead.** Keying on the",
        "whole normalized title makes the key almost as unique as the offer itself.",
        f"Even at the `aggressive` strength only {len(agg_rec):,} of "
        f"{len(agg):,} offers ({len(agg_rec) / len(agg):.1%}) sit under a normkey",
        "that recurs at all, and among recurring normkeys the spike at ADS = 1.0 is",
        "still 90.7%. Worse, the non-spike mass is not spread: it is concentrated on",
        "a handful of small-denominator values (0.5 dominates, then 0.667), because",
        "a recurring normkey has a median of 2 offers. That is not a continuous axis",
        "with usable range; it is a near-binary pure/ambiguous flag with a base rate",
        "around 9%. Charter invariant 1 says do not proceed on a dead axis, and on",
        "these histograms this version of the axis is dead.",
        "",
        "**But the axis is not dead in principle, it is dead at this key",
        "granularity.** Step 3b shows ADS responds strongly and monotonically to how",
        "coarse the key is. At k = 2 the spike falls to about 60%, roughly 40% of",
        "recurring keys are impure, and the mass genuinely spreads across the range.",
        "Spec section 3 already permits this reading: Framing B's key is \"a",
        "normalized surface **or blocking key**\", and everything measured in steps",
        "1 to 3 tested only the first option.",
        "",
        "### What I would take forward, for review",
        "",
        "Framing B with a **blocking key**, not a whole-title normkey. Concretely,",
        "gate 3 would need a principled blocking function designed and frozen",
        "before anything downstream is built: brand token plus model-number token is",
        "the obvious candidate for this corpus, with the step 3b first-k-tokens keys",
        "as a crude fallback. The reason to prefer it over the alternatives:",
        "",
        "1. It is the only variant measured in this pass that produces a real",
        "   distribution rather than a point mass, which is what invariant 1 asks for.",
        "2. It preserves the scientific story. A blocking key that resolves to one",
        "   cluster versus several is exactly the \"generic or ambiguous strings",
        "   resolve to multiple clusters\" mechanism spec section 3 describes, and it",
        "   keeps ADS and surface stability as genuinely separate axes, so invariant",
        "   2 is not at risk.",
        "3. It costs nothing already spent. The ingested table is unchanged; only the",
        "   key derivation changes.",
        "",
        "### Caveats the reviewer should weigh",
        "",
        "- The blocking key must be frozen before gate 3 measures anything, or the",
        "  ADS range becomes a tuned quantity and invariant 5 is compromised. Step 3b",
        "  deliberately stops at characterisation for this reason.",
        "- Coarsening the key trades range for meaning. A k = 2 key is close to a",
        "  brand-level bucket, and \"this brand resolves to many products\" is a",
        "  weaker notion of decision consistency than the paper wants. A brand plus",
        "  model-number key should be checked to confirm it keeps the range without",
        "  collapsing into brand frequency.",
        "- Volume is a live risk. 15,179 offers supports characterisation but may be",
        "  thin once split for held-out evaluation under invariant 3. The per-category",
        "  offers corpus is the upgrade path if gate 3 needs more.",
        "- Roughly half these titles carry retailer boilerplate and at least 26% are",
        "  non-English (step 4), so normalisation choices move the numbers materially.",
        "  Whatever is chosen must be frozen and reported, not tuned.",
        "",
        "**No framing is committed and nothing downstream is built. Stopping for",
        "review as the hard gate requires.**",
        "",
    ]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report -> {REPORT}", file=sys.stderr)
    return df


if __name__ == "__main__":
    d = main()
    # Self-check: ADS is a purity, so it must lie in (0, 1], and a key whose
    # offers all share one label must score exactly 1.0.
    a = ads(d, "key", "label")
    assert ((a > 0) & (a <= 1)).all(), "ADS out of (0, 1]"
    pure = d.groupby("key")["label"].nunique() == 1
    assert (a[pure] == 1.0).all(), "single-label keys must score ADS 1.0"
    assert len(BANDS) == 4, "band table assumes four half-open bands plus the spike"
