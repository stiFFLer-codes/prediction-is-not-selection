"""Phase 2.1 step 0/1: download the S2AND release files we need, with checksums.

Source: the AI2 public research bucket `s2and-release`, the data location the
allenai/S2AND README documents. Unauthenticated HTTPS against the S3 REST
endpoint, so no AWS CLI, no credentials, no paid API. Data license: ODC-BY
(LICENSE.txt ships inside the release prefix and is downloaded here too).

We take signatures + clusters for all eight constituent datasets. Papers and
SPECTER embedding pickles are multi-GB and are not needed for the Phase 2.1
two-axis check; zbmath_papers.json (the smallest) is taken in full to document
the paper-side schema, and the head of every other papers file is range-read
for a schema cross-check only.

Run: python phase2/fetch_s2and.py
"""

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

BUCKET = "https://ai2-s2-research-public.s3.amazonaws.com"
PREFIX = "s2and-release"

DATASETS = ["aminer", "arnetminer", "inspire", "kisti", "medline", "pubmed", "qian", "zbmath"]

# (key under the release prefix, local filename). Kept explicit so the manifest
# is a literal record of what we pulled, not a glob that can drift.
FILES = ["LICENSE.txt"]
for _d in DATASETS:
    FILES.append(f"{_d}/{_d}_signatures.json")
    FILES.append(f"{_d}/{_d}_clusters.json")       # medline has none; handled below
FILES += [
    "medline/train_pairs.csv",
    "medline/test_pairs.csv",
    "zbmath/zbmath_papers.json",
]

# Papers files we only sniff (first N bytes) to confirm the schema matches.
SNIFF_BYTES = 200_000
SNIFF = [f"{d}/{d}_papers.json" for d in DATASETS if d != "zbmath"]

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw_s2and"
MANIFEST = HERE / "data" / "MANIFEST_s2and.json"


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read(), dict(r.headers)


def fetch(key):
    """Download one release file if absent; return its manifest record."""
    path = RAW / key.replace("/", "_")
    url = f"{BUCKET}/{PREFIX}/{key}"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"  downloading {key} ...", flush=True)
        try:
            body, hdrs = _get(url)
        except urllib.error.HTTPError as e:
            print(f"  MISSING ({e.code}): {key}", flush=True)
            return {"key": key, "url": url, "status": f"HTTP {e.code}", "present": False}
        path.write_bytes(body)
    body = path.read_bytes()
    return {
        "key": key,
        "url": url,
        "local": str(path.relative_to(HERE)),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "present": True,
    }


def sniff(key):
    """Range-read the head of a large file we do not want in full."""
    url = f"{BUCKET}/{PREFIX}/{key}"
    path = RAW / ("HEAD_" + key.replace("/", "_"))
    if not path.exists():
        print(f"  sniffing {key} ...", flush=True)
        body, _ = _get(url, {"Range": f"bytes=0-{SNIFF_BYTES - 1}"})
        path.write_bytes(body)
    body = path.read_bytes()
    return {
        "key": key,
        "url": url,
        "local": str(path.relative_to(HERE)),
        "head_bytes": len(body),
        "head_sha256": hashlib.sha256(body).hexdigest(),
        "note": f"first {SNIFF_BYTES} bytes only, schema cross-check",
    }


def main():
    print(f"fetching from {BUCKET}/{PREFIX}/ (public, unauthenticated)")
    files = [fetch(k) for k in FILES]
    heads = [sniff(k) for k in SNIFF]
    manifest = {
        "source": "S2AND release, Allen Institute for AI (Semantic Scholar)",
        "paper": "Subramanian, King, Downey, Feldman. S2AND: A Benchmark and "
                 "Evaluation System for Author Name Disambiguation. JCDL '21.",
        "code_repo": "https://github.com/allenai/S2AND",
        "data_location_documented_at": "allenai/S2AND README, 'Download Data or Model': "
                                       "aws s3 sync --no-sign-request s3://ai2-s2-research-public/s2and-release",
        "obtained_from": f"{BUCKET}/{PREFIX}/ (REST endpoint of the same bucket, no credentials)",
        "first_party": "AI2's own public research bucket, not a third-party mirror",
        "data_license": "ODC-BY (LICENSE.txt in the release prefix; README: 'The released dataset is under ODC-BY')",
        "license_caveat": "README also notes some affiliation data comes from the Microsoft Academic Graph.",
        "files": files,
        "papers_head_sniffs": heads,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    ok = [f for f in files if f.get("present")]
    print(f"\n{len(ok)}/{len(files)} files present, {sum(f['bytes'] for f in ok):,} bytes")
    print(f"manifest -> {MANIFEST}")
    for f in files:
        if not f.get("present"):
            print(f"  ABSENT: {f['key']} ({f['status']})")


if __name__ == "__main__":
    sys.exit(main())
