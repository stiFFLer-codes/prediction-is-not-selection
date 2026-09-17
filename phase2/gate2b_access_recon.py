"""Gate 2b step 0: access recon for per-shop schema.org/category data.

Re-runnable check of the two load-bearing claims in
`reports/gate2b_access_recon.md`:

1. The WDC data hosts are unreachable.
2. The WDC LSPC distribution does not carry a per-shop schema.org/category
   property, so even a reachable host would not supply the signal gate 2b needs.

Claim 2 is checked against the sample files the WDC group commits to its own
website repo, which are first-party and reachable while the data host is not.

No data is ingested and nothing is measured. Run: python phase2/gate2b_access_recon.py
"""

import json
import sys
import urllib.error
import urllib.request

HOSTS = [
    "https://webdatacommons.org/",
    "https://data.dws.informatik.uni-mannheim.de/",
    "https://huggingface.co/api/datasets?author=wdc",
    "https://ir-ischool-uos.github.io/mwpd/",
]

# First-party samples committed to the WDC group's own website repo.
SAMPLES = "https://raw.githubusercontent.com/wbsg-uni-mannheim/wdc-page/master/categorization/"
SAMPLE_FILES = [
    "categories_gold_standard_offers_sample.json",
    "categories_clusters_training_sample.json",
    "categories_clusters_testing_sample.json",
    "amazon_training_sample.json",
]

TIMEOUT = 30


def probe(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return str(r.status)
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return f"unreachable ({type(e).__name__})"


def properties_in(url):
    """Every schema.org property name appearing in a sample file."""
    with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
        raw = r.read().decode("utf-8", "replace")
    try:
        data = json.loads(raw)
        records = data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    props = set()
    for rec in records:
        for field in ("schema.org_properties", "parent_schema.org_properties"):
            for item in rec.get(field) or []:
                if isinstance(item, dict):
                    props.update(item)
    return records, props


def main():
    print("== host reachability ==")
    for url in HOSTS:
        print(f"  {probe(url):<28} {url}")

    print("\n== per-shop category property in first-party samples ==")
    found = False
    for name in SAMPLE_FILES:
        records, props = properties_in(SAMPLES + name)
        hit = sorted(p for p in props if "categor" in p.lower())
        found = found or bool(hit)
        print(f"  {name} — {len(records)} records")
        print(f"    schema.org properties: {sorted(props) or '(none; flat record)'}")
        print(f"    category-like property: {hit or 'NONE'}")

    print(
        "\nVERDICT: per-shop schema.org/category is "
        + ("PRESENT — re-open gate 2b." if found else "ABSENT from the LSPC distribution.")
    )
    return found


if __name__ == "__main__":
    found = main()
    # Self-check: this pass concluded no per-shop category exists in these
    # samples. If that ever flips, the gate 2b verdict must be revisited, so
    # fail loudly rather than silently printing a contradiction.
    assert not found, "per-shop category found — gate 2b verdict is stale, re-run the gate"
    print("\nSelf-check passed: verdict in reports/gate2b_access_recon.md still holds.",
          file=sys.stderr)
