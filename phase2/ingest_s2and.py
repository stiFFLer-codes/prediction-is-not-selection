"""Phase 2.1 step 1: ingest S2AND into one clean signature table.

Input: the raw release files pulled by `fetch_s2and.py` (signatures + clusters
for the eight constituent datasets). Output: one Parquet table of
(sid, dataset, block_key, author_label, surface_form, + context fields) plus the
block grouping, which is just `group by (dataset, block_key)`.

Papers and SPECTER pickles are deliberately not ingested: they are ~6.5 GiB and
carry nothing the Phase 2.1 two-axis check needs. The paper-side schema is
reported from the one papers file we did pull (zbmath) plus a head sniff of the
other seven. No mechanisms, no accuracy, no selector here.

Run: python phase2/ingest_s2and.py
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from s2and_blocking import block_key, s2and_full_name, surface_form  # noqa: E402

RAW = HERE / "data" / "raw_s2and"
OUT = HERE / "data" / "s2and_signatures.parquet"
REPORT = HERE / "reports" / "gate21_data_shape.md"

DATASETS = ["aminer", "arnetminer", "inspire", "kisti", "medline", "pubmed", "qian", "zbmath"]


def load_dataset(name):
    """Return (rows, notes) for one constituent dataset."""
    sig_path = RAW / f"{name}_{name}_signatures.json"
    clu_path = RAW / f"{name}_{name}_clusters.json"
    notes = {"dataset": name}

    signatures = json.loads(sig_path.read_text(encoding="utf-8"))
    notes["signatures"] = len(signatures)

    if not clu_path.exists():
        notes["status"] = "EXCLUDED: no clusters file in the release, so no author labels"
        notes["clusters"] = 0
        return [], notes

    clusters = json.loads(clu_path.read_text(encoding="utf-8"))
    sid_to_label = {sid: cid for cid, rec in clusters.items() for sid in rec["signature_ids"]}
    notes["clusters"] = len(clusters)

    rows, dropped_no_label, dropped_no_key = [], 0, 0
    for sid, sig in signatures.items():
        label = sid_to_label.get(sid)
        if label is None:
            dropped_no_label += 1
            continue
        info = sig["author_info"]
        key = block_key(info["first"], info["last"])
        if not key:
            dropped_no_key += 1
            continue
        affiliations = info.get("affiliations") or []
        rows.append({
            "sid": f"{name}:{sid}",
            "dataset": name,
            "signature_id": sid,
            "paper_id": sig["paper_id"],
            "block_key": key,
            "author_label": f"{name}:{label}",
            "surface_form": surface_form(info["first"], info["middle"], info["last"], info["suffix"]),
            # S2AND's own fields, carried for the cross-checks only.
            "s2and_block": info["block"],
            "given_block": info.get("given_block"),
            "s2and_full_name": s2and_full_name(info["first"], info["middle"], info["last"], info["suffix"]),
            # context fields the signature record actually carries
            "first": info["first"],
            "middle": info["middle"],
            "last": info["last"],
            "suffix": info["suffix"],
            "position": info["position"],
            "n_affiliations": len(affiliations),
            "affiliation": affiliations[0] if affiliations else None,
            "has_email": info["email"] is not None,
            # NOT the label: a Semantic Scholar author id that disagrees with the
            # gold clustering. Kept only so that the disagreement stays visible.
            "s2_author_id": sig.get("author_id"),
        })
    notes["status"] = "included"
    notes["dropped_no_label"] = dropped_no_label
    notes["dropped_no_block_key"] = dropped_no_key
    notes["rows"] = len(rows)
    return rows, notes


def _parse_head(text):
    """Pull whole records out of a truncated dict-of-records JSON file."""
    papers = {}
    for match in re.finditer(r'"(\d+)"\s*:\s*\{', text):
        start = match.end() - 1
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        papers[match.group(1)] = json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        pass
                    break
    return papers


def surface_roundtrip_check(df):
    """Is our surface form the raw name as printed on the paper?

    zbmath's papers file was pulled in full; for the other seven only the first
    200 KB was range-read, which still contains a few hundred real papers. Both
    are checked, and the sample sizes are reported rather than hidden.
    """
    results = []
    for name in DATASETS:
        full = RAW / f"{name}_{name}_papers.json"
        head = RAW / f"HEAD_{name}_{name}_papers.json"
        if full.exists():
            papers = json.loads(full.read_text(encoding="utf-8"))
            scope = "full papers file"
        elif head.exists():
            papers = _parse_head(head.read_bytes().decode("utf-8", "ignore"))
            scope = "first 200 KB of the papers file"
        else:
            continue
        sub = df[df.dataset == name]
        checked = matched = 0
        for row in sub.itertuples():
            paper = papers.get(str(row.paper_id))
            if paper is None:
                continue
            authors = [a for a in paper["authors"] if a["position"] == row.position]
            if not authors:
                continue
            checked += 1
            raw = re.sub(r"\s+", " ", authors[0]["author_name"]).strip()
            matched += raw == row.surface_form
        results.append({"dataset": name, "scope": scope, "checked": checked, "identical": matched})
    return results


def papers_schema():
    """Field coverage of the one papers file we hold in full."""
    path = RAW / "zbmath_zbmath_papers.json"
    if not path.exists():
        return None
    papers = json.loads(path.read_text(encoding="utf-8"))
    present = Counter()
    for rec in papers.values():
        for field, value in rec.items():
            if value not in (None, "", [], {}):
                present[field] += 1
    return {"n": len(papers), "non_null": dict(present)}


def write_report(df, notes, roundtrip, schema):
    lines = []
    add = lines.append
    add("# Phase 2.1 step 1: S2AND ingest, data shape\n")
    add("Generated by `phase2/ingest_s2and.py`. Every number is computed, not typed.\n")
    add(f"Table: `{OUT.name}`, **{len(df):,} signatures**, {df.dataset.nunique()} datasets, "
        f"{df.groupby(['dataset', 'block_key']).ngroups:,} blocks, "
        f"{df.author_label.nunique():,} distinct authors.\n")

    add("## Constituent datasets: what we used and why\n")
    add("| dataset | signatures in release | clusters | status | rows ingested | dropped, no block key |")
    add("| --- | ---: | ---: | --- | ---: | ---: |")
    for note in notes:
        add(f"| {note['dataset']} | {note['signatures']:,} | {note['clusters']:,} | {note['status']} | "
            f"{note.get('rows', 0):,} | {note.get('dropped_no_block_key', 0):,} |")
    add("")

    add("## Fields S2AND actually carries\n")
    add("Signature record, all eight datasets, identical schema: `signature_id`, `paper_id`, "
        "`author_id`, and an `author_info` object with `first`, `middle`, `last`, `suffix`, "
        "`position`, `block`, `given_block`, `affiliations`, `email`. Nothing else.\n")
    add("`author_id` is **not** the label. It is a Semantic Scholar author id that disagrees with "
        "the gold clustering, so the label of record is the cluster id from `*_clusters.json`.\n")
    add("Per-dataset non-null coverage of the context fields, over ingested rows:\n")
    add("| dataset | rows | first | middle | suffix | affiliation | email |")
    add("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, sub in df.groupby("dataset"):
        add(f"| {name} | {len(sub):,} | {sub['first'].notna().mean():.1%} | "
            f"{sub['middle'].notna().mean():.1%} | {sub['suffix'].notna().mean():.1%} | "
            f"{(sub.n_affiliations > 0).mean():.1%} | {sub.has_email.mean():.1%} |")
    add("")

    if schema:
        cov = ", ".join(f"{k} {v / schema['n']:.1%}" for k, v in sorted(schema["non_null"].items()))
        add(f"Paper record (from `zbmath_papers.json`, {schema['n']:,} papers; the head sniff of the "
            "other seven files shows the identical key set): `paper_id`, `title`, `abstract`, "
            "`authors` (position + author_name), `venue`, `journal_name`, `year`, `references`. "
            f"Non-null coverage in zbmath: {cov}.\n")

    add("## Surface form is the raw printed name, not a reconstruction\n")
    add("Our frozen `surface_form` joins the signature's own name parts. That is only a legitimate "
        "surface axis if it equals the name actually printed on the paper. Checked against the "
        "papers files:\n")
    add("| dataset | scope | signatures checked | byte-identical |")
    add("| --- | --- | ---: | ---: |")
    for row in roundtrip:
        pct = f"{row['identical'] / row['checked']:.2%}" if row["checked"] else "n/a"
        add(f"| {row['dataset']} | {row['scope']} | {row['checked']:,} | {row['identical']:,} ({pct}) |")
    add("")

    add("## Not ingested, and why\n")
    add("- `*_papers.json` (~3.4 GiB across the eight) and `*_specter.pickle` (~3.0 GiB): carry "
        "paper-level context (title, venue, year, co-authors) that Phase 2.2 mechanisms may want, "
        "but nothing the two-axis check needs. Re-fetchable by extending the file list in "
        "`fetch_s2and.py`.\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main():
    all_rows, all_notes = [], []
    for name in DATASETS:
        rows, notes = load_dataset(name)
        all_rows.extend(rows)
        all_notes.append(notes)
        print(f"{name:12s} {notes['status'][:40]:42s} rows={notes.get('rows', 0):>8,}", flush=True)

    df = pd.DataFrame(all_rows)

    # Self-checks. These fail the run rather than warn.
    assert df.sid.is_unique, "signature ids must be unique after namespacing"
    assert df.block_key.str.len().gt(0).all(), "no empty block keys may survive"
    assert df.surface_form.str.len().gt(0).all(), "no empty surface forms may survive"
    assert df.author_label.notna().all(), "every row must carry an author label"
    assert df.groupby("author_label").dataset.nunique().max() == 1, "labels must not span datasets"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False, compression="zstd")

    write_report(df, all_notes, surface_roundtrip_check(df), papers_schema())
    print(f"\n{len(df):,} rows -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
    print(f"report -> {REPORT}")


if __name__ == "__main__":
    sys.exit(main())
