"""Gate 1: download the WDC LSPC 2017 category slices and flatten them into a
clean (surface_string, key, label) offer table.

Source: the Web Data Commons group's own HuggingFace repo `wdc/products-2017`
(the WDC Training Dataset and Gold Standard for Large-Scale Product Matching,
v2.0). The canonical host webdatacommons.org was unreachable when this ran, so
provenance is pinned by repo revision + per-file sha256 (see MANIFEST).

The distributed files are labelled offer *pairs*. Each row carries the full
left and right offer, so exploding both sides and deduplicating on offer id
recovers the underlying offer table. No mechanisms, no ADS, no selector here.

Run: python phase2/ingest_wdc.py
"""

import gzip
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd

REPO = "wdc/products-2017"
# Pinned revision of the HF dataset repo (immutable commit sha).
REVISION = "bee4f71ca1bcfc51eb8fc41d65720fb6f487df9d"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/{REVISION}"

CATEGORIES = ["cameras", "computers", "shoes", "watches"]
SPLITS = ["train_xlarge", "valid_xlarge", "test"]

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw"
OUT = HERE / "data" / "wdc_lspc2017_offers.csv.gz"
MANIFEST = HERE / "data" / "MANIFEST.json"
REPORT = HERE / "reports" / "gate1_data_shape.md"


def fetch(cat, split):
    """Download one slice if absent; return (path, sha256)."""
    path = RAW / f"{cat}_{split}.json.gz"
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        url = f"{BASE}/{cat}/{split}.json.gz"
        print(f"  downloading {url}", file=sys.stderr)
        urllib.request.urlretrieve(url, path)
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


def offers_from(path, cat, split):
    """Explode labelled pairs into one row per offer side."""
    rows = []
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            pair = json.loads(line)
            for side in ("left", "right"):
                rows.append(
                    {
                        "offer_id": pair[f"id_{side}"],
                        "surface_string": pair[f"title_{side}"],
                        "key": pair[f"cluster_id_{side}"],
                        "label": pair[f"category_{side}"],
                        "slice": cat,
                        "split": split,
                    }
                )
    return rows


def build():
    manifest, rows = [], []
    for cat in CATEGORIES:
        for split in SPLITS:
            path, digest = fetch(cat, split)
            manifest.append(
                {
                    "file": f"{cat}/{split}.json.gz",
                    "url": f"{BASE}/{cat}/{split}.json.gz",
                    "bytes": path.stat().st_size,
                    "sha256": digest,
                }
            )
            rows.extend(offers_from(path, cat, split))

    df = pd.DataFrame(rows)
    n_sides = len(df)
    # Titles are nullable in the corpus; an offer with no surface form is
    # unusable for either framing, so drop before deduplicating.
    df = df[df["surface_string"].notna() & (df["surface_string"].str.strip() != "")]
    # One offer appears in many pairs. Keep its first occurrence.
    df = df.drop_duplicates(subset="offer_id").sort_values("offer_id")
    df = df[["offer_id", "surface_string", "key", "label", "slice", "split"]]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, compression="gzip")
    MANIFEST.write_text(
        json.dumps(
            {
                "source": "Web Data Commons — Training Dataset and Gold Standard "
                "for Large-Scale Product Matching, v2.0 (LSPC 2017)",
                "citation": "Primpeli, Peeters, Bizer (WWW '19 Companion), 381-386",
                "canonical_host": "https://webdatacommons.org/largescaleproductcorpus/v2/",
                "obtained_from": f"https://huggingface.co/datasets/{REPO}",
                "revision": REVISION,
                "files": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{n_sides} offer sides -> {len(df)} distinct offers -> {OUT}", file=sys.stderr)
    return df


def report(df):
    """Data-shape report under the as-distributed triple (key = cluster_id)."""
    per_key = df.groupby("key")["surface_string"].agg(
        rows="size", forms=lambda s: s.nunique()
    )
    rec = per_key["rows"]
    once, twice, three_plus = (rec == 1).sum(), (rec == 2).sum(), (rec >= 3).sum()
    multiform = (per_key["forms"] > 1).mean()

    # Ten examples: five from single-form keys, five from multi-form keys.
    single = per_key.index[per_key["forms"] == 1][:5]
    multi = per_key.index[per_key["forms"] > 1][:5]
    ex = df[df["key"].isin(list(single) + list(multi))]
    ex = ex.groupby("key").head(2).sort_values(["key", "offer_id"])

    lines = [
        "# Gate 1 data-shape report",
        "",
        f"Table: `{OUT.relative_to(HERE).as_posix()}`  ",
        f"Provenance: `{MANIFEST.relative_to(HERE).as_posix()}`",
        "",
        "Shape is reported under the as-distributed triple: `key` = WDC cluster id",
        "(product identity), `label` = WDC category, `surface_string` = offer title.",
        "Gate 2 re-derives Framing A and Framing B keys from this same table.",
        "",
        "## Totals",
        "",
        f"- Total rows (distinct offers): {len(df):,}",
        f"- Distinct keys (clusters): {per_key.shape[0]:,}",
        f"- Distinct surface strings: {df['surface_string'].nunique():,}",
        f"- Label cardinality (categories): {df['label'].nunique()}",
        "",
        "## Key recurrence",
        "",
        "| occurrences | keys | share |",
        "| --- | --- | --- |",
        f"| 1 | {once:,} | {once / len(per_key):.1%} |",
        f"| 2 | {twice:,} | {twice / len(per_key):.1%} |",
        f"| 3+ | {three_plus:,} | {three_plus / len(per_key):.1%} |",
        "",
        "## Distinct surface forms per key",
        "",
        f"- min {per_key['forms'].min()}, median {per_key['forms'].median():.0f}, "
        f"max {per_key['forms'].max()}",
        f"- keys with more than one surface form: {multiform:.1%}",
        "",
        "## Labels",
        "",
    ]
    lines += [f"- `{k}`: {v:,}" for k, v in df["label"].value_counts().items()]
    lines += ["", "## Example rows", "",
              "| key | forms in key | surface_string | label |", "| --- | --- | --- | --- |"]
    for r in ex.itertuples():
        s = r.surface_string.replace("|", "\\|")[:90]
        lines.append(f"| {r.key} | {per_key.loc[r.key, 'forms']} | {s} | {r.label} |")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report -> {REPORT}", file=sys.stderr)


if __name__ == "__main__":
    df = build()
    assert df["offer_id"].is_unique, "offer_id must be unique after dedup"
    assert df["surface_string"].notna().all(), "no empty surface strings"
    assert df.groupby("key").size().max() > 1, "no recurring keys — corpus is wrong"
    report(df)
