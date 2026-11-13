# Prediction is not selection

*A pre-registered study of design-time mechanism choice in author name disambiguation.* Maitreya Sapariya.

The paper asks whether a designer can measure a property of their own data before building anything and learn from it which classification mechanism to build. It tests this on seven public author name disambiguation datasets from S2AND. The comparison is between a precision-first exact-evidence rule and a coverage-first k-nearest vote. Both are untrained lookups over a name block's own history. The two signals, both readable at design time, are consistency (ADS, the share of a block held by its most frequent author) and surface stability, measured inversely as surface variability (SV). The pre-registration and its amendments are in `PREREG.md`. The three hypotheses came out as follows:

- **H1, Supported.** ADS predicts each mechanism's own accuracy (Spearman 0.51 and 0.83).
- **H2, Inconclusive.** Pooled over the seven datasets, no ADS band and no SV band has a decided verdict at the pre-registered margin.
- **H3, Inconclusive.** No ADS band holds two SV bands with a decided verdict.

Prediction is not selection. The paper also reports a structural result. An exact-match rule cannot win against a retriever that takes the single nearest surface form, at any cutoff, when the similarity gives its maximum only to identical strings and the two share a tie-break. Two datasets, kisti and zbmath, are decided at the margin in opposite directions: kisti for the rule, zbmath for the vote.

## The paper

- PDF and record: Zenodo, DOI [10.5281/zenodo.24184394](https://doi.org/10.5281/zenodo.24184394).
- PDF in this repository: `paper/main.pdf`, the same file as on Zenodo.
- Source: `paper/main.tex`, `paper/references.bib`, `paper/main.bbl`, figures in `paper/figs/`.

To build it, from `phase2/paper/`:

```
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Expect 31 pages. The reported build used pdfTeX from MiKTeX 25.12. `main.bbl` is committed, so `bibtex` can be skipped. If you run it, it rewrites `main.bbl`, and on Windows `git status` then shows that file as modified with no diff. The figures in `paper/figs/` are copies of the ones `phase2e_run.py` writes to `reports/figs/`.

## Environment

The interpreter is **CPython 3.14.2**. The recommended route is a fresh virtual environment with the pinned packages:

```
py -3.14 -m venv .venv            # Windows; elsewhere: python3.14 -m venv .venv
.venv\Scripts\activate            # Windows; elsewhere: source .venv/bin/activate
pip install -r phase2/requirements-lock.txt
```

Then check the interpreter: `python -VV` should report 3.14.2, because `py -3.14` takes the newest 3.14 installed. If PowerShell refuses to run the activation script, run `Set-ExecutionPolicy -Scope Process RemoteSigned` first, or use `.venv\Scripts\activate.bat` from `cmd`.

Keep the pins exact. The frozen split is drawn with NumPy's `default_rng(...).permutation`, and NumPy does not promise the same stream across feature releases. pandas 3 changed the string type that the sort and factorize steps run on. The pipeline is offline and CPU-only. It needs no API key, no GPU and no paid service.

## Data

The repository carries the derived S2AND tables the analysis starts from, so a run needs no download. `DATA_LICENSES.md` lists every derived data file, its columns and its licence. The raw S2AND release is not in the repository. `fetch_s2and.py` downloads it from AI2's public bucket and checks it against `data/MANIFEST_s2and.json`.

## Run order

Run each step from the repository root as `python phase2/<script>`, with the venv active. Script names and output paths in the table are relative to `phase2/`. Several scripts overwrite committed files, and on a correct run their content comes out the same.

| Step | Script | What it writes | Time |
|---|---|---|---|
| 1 | `s2and_blocking.py` | nothing; self-check of the frozen blocking definitions | 1 s |
| 2 | `phase2b_build.py` | `phase2b_constants.py` (frozen cutoff and band edges), `data/phase2b_blocks.parquet`, `reports/phase2b_calibration.md` | 3 min |
| 3 | `phase2b_run.py` | `data/phase2b_eval_sigs.parquet` (cache), `reports/phase2b_boundary.md`, `reports/tables/phase2b_*`, `reports/figs/phase2b_*` | 10 min |
| 4 | `phase2c_probe.py` | `reports/tables/phase2c_pair_*.csv` | 15 s |
| 5 | `phase2e_mech.py` | nothing; self-check, then the calibration-split regression check | 12 s |
| 6 | `phase2e_run.py` | `data/phase2e_eval_sigs.parquet` (cache), `reports/phase2e_boundary.md`, `reports/tables/phase2e_*`, `reports/figs/phase2e_*` | 4 min |
| 7 | `phase2_7b_reanalysis.py` | `reports/phase2_7b_reanalysis.md`, `reports/tables/phase2_7b_*.csv`, `reports/figs/phase2_7b_*.png` | 40 s |
| 8 | `phase2_9a_matched.py` | `reports/tables/phase2_9a_*.csv` | 22 s |
| 9 | `phase2_9b_supplement.py` | `reports/tables/phase2_9b_*.csv`, `reports/phase2_9b_report.md` (its last section is hand-written and kept) | 24 s |

The times are from one cold run of a fresh clone, with steps 3 and 6 building their caches, on Windows 11 Home 24H2 with an Intel Core i5-6200U (2 cores, 4 threads) and 16 GB of RAM.

Notes on the order.

- Step 2 rewrites `phase2b_constants.py`. Check it first with `git diff --exit-code -- phase2/phase2b_constants.py`, which shows no change on a correct run.
- On Windows the scripts write text with CRLF line endings. After a full run `git status` lists the rewritten files as modified while `git diff` shows no change. The `.csv.gz` files also differ in their gzip header time, so compare them decompressed.
- Step 9 reads the Experiment 1 table from the `v1.1.0` tag with `git show`, so it needs a clone that has the tags.
- The two caches under `data/` are gitignored. Step 7 reads `data/phase2e_eval_sigs.parquet` and needs step 6 first. Steps 8 and 9 rebuild that cache through the frozen mechanism pass if it is absent.

Optional, from the raw release, in this order:

1. `fetch_s2and.py` downloads into `data/raw_s2and/` and rewrites `data/MANIFEST_s2and.json`, with OS path separators in its `local` fields.
2. `ingest_s2and.py` writes `data/s2and_signatures.parquet` and `reports/gate21_data_shape.md`.
3. `gate21_two_axes.py` writes `data/s2and_blocks.csv.gz`, `data/s2and_blocks_s2and_key.csv.gz`, `reports/gate21_two_axes.md` and `reports/figs/gate21_*.png`.

The substrate check on the WDC product corpus that section 1.2 of the paper reports used `ingest_wdc.py`, `gate2_ads_range.py` and `gate2b_access_recon.py`. Nothing in the main analysis depends on them.

## Checks

There is no test suite, although charter invariant 7 says "covered by tests". Instead, every script runs assert-based self-checks and halts on any mismatch. A check is either a `demo()` on hand-built cases or a re-derivation of the frozen population and counts.

## Record

- `PREREG.md` is the pre-registration, with Amendment 1 and Addendum 1a appended at Phase 2.2d. It has not changed since commit `3e79a48`, which came before the reported run.
- Section 6.4 of the paper sets out the commit record behind the pre-registration and the points where the record departs from it, including the insertion of commit `a41a67a` into the frozen text.
- `ERRATA.md` lists statements in the governance files and reports that the later record contradicts. Those files are kept as written.

## Project log

`PREREG.md`, `PASSLOG.md`, `STATE.md`, `PLAN.md` and `CLAUDE.md` are the working record of the project, kept pass by pass with an AI assistant, as the paper's generative-AI disclosure says.

## Earlier work, deprecated

The tags `v1.0.0` and `v1.1.0` and their Zenodo records hold earlier work by the same author. They are deprecated and kept for the record only. Section 8.3 of the paper discusses that earlier study and cites `v1.1.0`, and step 9 reads one table from that tag. Nothing else here depends on them.

## Licences

Code: MIT (`LICENSE`). Paper text and reports in `paper/` and `reports/`, and every Markdown file in the repository: CC BY 4.0 (`LICENSE-TEXT`), except text quoted from third parties. Derived data, including the two `reports/tables/*_blocks_scored.csv.gz` tables: the terms of each source, set out in `DATA_LICENSES.md`.
