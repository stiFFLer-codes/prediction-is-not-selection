# Phase 2.9c: cold reproduction from a fresh clone

Every output of the README run order came out the same as the commit it was cloned from. All 108 compared files match in content, the frozen population and counts reproduce, `phase2b_constants.py` hashes to its committed blob, and the paper builds at 31 pages with no undefined reference or citation. The optional raw path also ran: all 19 downloaded S2AND files match the committed checksums, and the signature table rebuilt from them equals the committed one. The only byte-level differences are line endings and gzip headers, listed under "Differences below content level".

The run is also a test of `phase2/README.md`, read the way a stranger would read it. Five findings are at the end. None of them changed a result.

## What was run

- Source: commit `1ef28d2` ("phase-2 gate 2.9c: remove the deprecated earlier tree from the tip") on `phase-2`, with tags `v1.0.0` and `v1.1.0`.
- Clone: `git clone --no-hardlinks --branch phase-2 <repository> ../coldrun/repo`, outside the working repository. The clone's HEAD was `1ef28d2` and it had both tags. Neither mechanism cache (`phase2/data/phase2b_eval_sigs.parquet`, `phase2/data/phase2e_eval_sigs.parquet`) existed in it.
- Guide: `phase2/README.md` in the clone, and nothing else, for the environment and the run order.

## Environment

| Item | Value |
|---|---|
| OS | Windows 11 Home Single Language 24H2, version 10.0.26100, 64-bit |
| CPU | Intel Core i5-6200U at 2.30 GHz, 2 cores, 4 threads |
| RAM | 16 GB (15.9 GB reported) |
| Interpreter | CPython 3.14.2, 64-bit, Windows |
| `python -VV` | `Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]` |
| pip | 25.3 |
| Git | 2.55.0.windows.3, `core.autocrlf=true`, set in the system gitconfig |
| TeX | MiKTeX-pdfTeX 4.23 (MiKTeX 25.12) |

`pip freeze` in the new venv after `pip install -r phase2/requirements-lock.txt`. The lock file pins the first seven packages named in it, and the other nine came in unpinned as dependencies.

```
contourpy==1.4.0
cycler==0.12.1
fonttools==4.68.0
kiwisolver==1.5.1
matplotlib==3.11.1
numpy==2.4.2
packaging==26.3
pandas==3.0.1
pillow==13.0.0
pyarrow==24.0.0
pyparsing==3.3.3
python-dateutil==4.0.0
RapidFuzz==3.14.5
scipy==1.17.0
tzdata==2026.6
Unidecode==1.4.0
```

## Commands as run

From the clone's root, in Windows PowerShell, as the README writes them:

```
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r phase2/requirements-lock.txt
```

`py -3.14` chose CPython 3.14.2. Activation worked and the install finished with no error.

The README's first step, `python s2and_blocking.py` from the repository root, fails with "can't open file" (finding 1). Every step was therefore run as `phase2/<script>` from the clone's root with the venv interpreter, which is what activation puts on the path:

```
.venv/Scripts/python.exe phase2/<script> > ../coldrun/logs/step<N>.log 2>&1
```

Steps 1 and 2 ran first, then the constants check, then steps 3 to 9 in order, halting on the first non-zero exit. None occurred. The paper was built from `phase2/paper/` with the README's four commands, each `pdflatex` given `-interaction=nonstopmode`. The raw path ran last, in the same clone: `fetch_s2and.py`, `ingest_s2and.py`, `gate21_two_axes.py`.

## Time for every step

Wall time per script, measured around the process. Steps 3 and 6 started without their caches and wrote them. Steps 7 to 9 found the cache that step 6 wrote.

| Step | Script | Wall time | Rounded | Exit |
|---|---|---|---|---|
| 1 | `phase2/s2and_blocking.py` | 0.6 s | 1 s | 0 |
| 2 | `phase2/phase2b_build.py` | 201.4 s | 3 min | 0 |
| 3 | `phase2/phase2b_run.py` | 573.6 s | 10 min | 0 |
| 4 | `phase2/phase2c_probe.py` | 15.4 s | 15 s | 0 |
| 5 | `phase2/phase2e_mech.py` | 12.1 s | 12 s | 0 |
| 6 | `phase2/phase2e_run.py` | 266.2 s | 4 min | 0 |
| 7 | `phase2/phase2_7b_reanalysis.py` | 40.4 s | 40 s | 0 |
| 8 | `phase2/phase2_9a_matched.py` | 21.5 s | 22 s | 0 |
| 9 | `phase2/phase2_9b_supplement.py` | 23.6 s | 24 s | 0 |
| | steps 1 to 9 | 1,154.8 s | 19 min | |
| paper | `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` | 12 s | 12 s | 0 |
| raw 1 | `phase2/fetch_s2and.py` | 190.1 s | 3 min | 0 |
| raw 2 | `phase2/ingest_s2and.py` | 50.3 s | 50 s | 0 |
| raw 3 | `phase2/gate21_two_axes.py` | 261.9 s | 4 min | 0 |

The download time depends on the network. Steps 3 and 6 took 10 and 4 minutes here. The README's earlier figure was about 20 minutes each.

## What the scripts checked

Every script's self-check passed. The lines that re-derive the frozen record:

- Step 2: 2,848 calibration blocks; SV band edges 0.102644 and 0.195066; chosen cutoff 0.50 under both metrics.
- Steps 3 and 6: 199,713 test signatures each; H1 Supported, H2 Inconclusive, H3 Inconclusive.
- Step 4: 1-NN reproduces the 2.2b nesting, 0 rule-right and 1-NN-wrong.
- Step 5: k = 5 reproduces 546 rule wins against 744, with the whole k curve and both accuracies.
- Step 7: per-block verdicts 191 / 309 / 10,172 / 3,230; blocks 26,939, live 18,984, calibration 2,848, evaluation 16,136.
- Step 8: 2,770 of 13,902 evaluation blocks, 83,401 of 197,479 test signatures, in the contested region.
- Step 9: Experiment 1 read from `v1.1.0`, 115 of 120 clean conditions inside plus or minus 0.02.

## The constants check

`phase2b_build.py` rewrites `phase2/phase2b_constants.py`. It was checked right after step 2, before anything else ran.

- `git diff --exit-code -- phase2/phase2b_constants.py` is clean.
- `git hash-object --path=phase2/phase2b_constants.py` gives `7440cef`, the committed blob.
- With CR removed, the file equals the committed blob byte for byte.
- It is byte-identical to the copy in the working repository, which the reported run last wrote.

The raw file does differ from the committed blob in one way. `.gitattributes` checks text out with LF, and the script writes with `Path.write_text`, which writes CRLF on Windows. All 51 lines end in CRLF and the blob's end in LF. No other byte differs. It counts as a pass, not the stop condition: git stores the identical blob, and the blob is what the release holds.

## Comparison table

How each file type was compared:

- `.csv`, `.md`, `.py`, `.json`: text after CRLF is turned into LF. Files equal as raw bytes are marked "bytes".
- `.csv.gz`: both decompressed, then compared as bytes.
- `.parquet`: loaded with pandas, columns sorted, compared with `DataFrame.equals`.
- `.png`: raw bytes.

The two caches are gitignored and have no committed blob. They were compared with the caches the reported run left in the working repository. "Output file" means every file in the clone, outside `.venv/`, `.git/` and `__pycache__/`, written at or after the start of step 1. The raw downloads and the LaTeX build by-products are not rows. Both are gitignored, and the downloads are covered by the checksum check below.

`phase2/reports/phase2_9b_report.md` was compared in two parts. Its last section, from the heading "## Local file times for the 2.2e run", is hand-written. `phase2_9b_supplement.py` keeps it by reading the existing report and copying everything from that heading on (`phase2/phase2_9b_supplement.py:56` and `:211-212`). The part above the heading equals the committed one after LF normalization, and the hand-written section came back unchanged.

Totals: 108 files compared, 108 match, 0 differ in content, 0 differ only as PNG bytes. All 26 PNGs are byte-identical.

| # | Stage | File | Compared by | Result |
|---|---|---|---|---|
| 1 | main run | `phase2/data/phase2b_blocks.parquet` | DataFrame.equals, sorted columns | match |
| 2 | main run | `phase2/data/phase2b_eval_sigs.parquet` | DataFrame.equals, sorted columns, against the reported run's local cache | match (gitignored cache) |
| 3 | main run | `phase2/data/phase2e_eval_sigs.parquet` | DataFrame.equals, sorted columns, against the reported run's local cache | match (gitignored cache) |
| 4 | main run | `phase2/phase2b_constants.py` | LF-normalized text | match |
| 5 | main run | `phase2/reports/figs/phase2_7b_driver_bootstrap.png` | bytes | match |
| 6 | main run | `phase2/reports/figs/phase2_7b_verdicts_by_blocksize.png` | bytes | match |
| 7 | main run | `phase2/reports/figs/phase2b_grid_gap_sv.png` | bytes | match |
| 8 | main run | `phase2/reports/figs/phase2b_grid_gap_svresid.png` | bytes | match |
| 9 | main run | `phase2/reports/figs/phase2b_h1_ads_accuracy.png` | bytes | match |
| 10 | main run | `phase2/reports/figs/phase2b_margin_sensitivity.png` | bytes | match |
| 11 | main run | `phase2/reports/figs/phase2b_power_by_size.png` | bytes | match |
| 12 | main run | `phase2/reports/figs/phase2b_verdicts_by_ads.png` | bytes | match |
| 13 | main run | `phase2/reports/figs/phase2b_verdicts_by_sv.png` | bytes | match |
| 14 | main run | `phase2/reports/figs/phase2e_decidability_gradient.png` | bytes | match |
| 15 | main run | `phase2/reports/figs/phase2e_grid_decided_sv.png` | bytes | match |
| 16 | main run | `phase2/reports/figs/phase2e_grid_gap_sv.png` | bytes | match |
| 17 | main run | `phase2/reports/figs/phase2e_grid_gap_svresid.png` | bytes | match |
| 18 | main run | `phase2/reports/figs/phase2e_h1_ads_accuracy.png` | bytes | match |
| 19 | main run | `phase2/reports/figs/phase2e_k_curve.png` | bytes | match |
| 20 | main run | `phase2/reports/figs/phase2e_margin_sensitivity.png` | bytes | match |
| 21 | main run | `phase2/reports/figs/phase2e_power_by_size.png` | bytes | match |
| 22 | main run | `phase2/reports/figs/phase2e_verdicts_by_ads.png` | bytes | match |
| 23 | main run | `phase2/reports/figs/phase2e_verdicts_by_sv.png` | bytes | match |
| 24 | main run | `phase2/reports/phase2_7b_reanalysis.md` | LF-normalized text | match |
| 25 | main run | `phase2/reports/phase2_9b_report.md` | LF-normalized; above hand section equal, hand section kept verbatim | match |
| 26 | main run | `phase2/reports/phase2b_boundary.md` | LF-normalized text | match |
| 27 | main run | `phase2/reports/phase2b_calibration.md` | LF-normalized text | match |
| 28 | main run | `phase2/reports/phase2e_boundary.md` | LF-normalized text | match |
| 29 | main run | `phase2/reports/tables/phase2_7b_accuracy_accounting.csv` | LF-normalized text | match |
| 30 | main run | `phase2/reports/tables/phase2_7b_blocksize_by_ads.csv` | LF-normalized text | match |
| 31 | main run | `phase2/reports/tables/phase2_7b_blocksize_pooled.csv` | LF-normalized text | match |
| 32 | main run | `phase2/reports/tables/phase2_7b_blocksize_verdicts.csv` | LF-normalized text | match |
| 33 | main run | `phase2/reports/tables/phase2_7b_driver_bootstrap.csv` | LF-normalized text | match |
| 34 | main run | `phase2/reports/tables/phase2_7b_driver_restricted.csv` | LF-normalized text | match |
| 35 | main run | `phase2/reports/tables/phase2_7b_gradient_ads.csv` | LF-normalized text | match |
| 36 | main run | `phase2/reports/tables/phase2_7b_restricted_marginals.csv` | LF-normalized text | match |
| 37 | main run | `phase2/reports/tables/phase2_7b_verdict_distribution.csv` | LF-normalized text | match |
| 38 | main run | `phase2/reports/tables/phase2_9a_contested_share.csv` | LF-normalized text | match |
| 39 | main run | `phase2/reports/tables/phase2_9a_matched_precision.csv` | LF-normalized text | match |
| 40 | main run | `phase2/reports/tables/phase2_9a_region_counts.csv` | LF-normalized text | match |
| 41 | main run | `phase2/reports/tables/phase2_9b_bands_by_population.csv` | LF-normalized text | match |
| 42 | main run | `phase2/reports/tables/phase2_9b_cells_by_population.csv` | LF-normalized text | match |
| 43 | main run | `phase2/reports/tables/phase2_9b_exp1_clean_intervals.csv` | LF-normalized text | match |
| 44 | main run | `phase2/reports/tables/phase2_9b_init.csv` | LF-normalized text | match |
| 45 | main run | `phase2/reports/tables/phase2_9b_population_verdicts.csv` | LF-normalized text | match |
| 46 | main run | `phase2/reports/tables/phase2_9b_structure_by_population.csv` | LF-normalized text | match |
| 47 | main run | `phase2/reports/tables/phase2b_accuracy_by_population.csv` | LF-normalized text | match |
| 48 | main run | `phase2/reports/tables/phase2b_blocks_scored.csv.gz` | gunzip bytes | match |
| 49 | main run | `phase2/reports/tables/phase2b_generalization.csv` | LF-normalized text | match |
| 50 | main run | `phase2/reports/tables/phase2b_h1_spearman.csv` | LF-normalized text | match |
| 51 | main run | `phase2/reports/tables/phase2b_margin_sensitivity.csv` | LF-normalized text | match |
| 52 | main run | `phase2/reports/tables/phase2b_pooled_ads.csv` | LF-normalized text | match |
| 53 | main run | `phase2/reports/tables/phase2b_pooled_cells_sv.csv` | LF-normalized text | match |
| 54 | main run | `phase2/reports/tables/phase2b_pooled_cells_sv_jw.csv` | LF-normalized text | match |
| 55 | main run | `phase2/reports/tables/phase2b_pooled_cells_svr.csv` | LF-normalized text | match |
| 56 | main run | `phase2/reports/tables/phase2b_pooled_init_sv.csv` | LF-normalized text | match |
| 57 | main run | `phase2/reports/tables/phase2b_pooled_sv.csv` | LF-normalized text | match |
| 58 | main run | `phase2/reports/tables/phase2b_pooled_sv_jw.csv` | LF-normalized text | match |
| 59 | main run | `phase2/reports/tables/phase2b_pooled_svr.csv` | LF-normalized text | match |
| 60 | main run | `phase2/reports/tables/phase2b_power_by_size.csv` | LF-normalized text | match |
| 61 | main run | `phase2/reports/tables/phase2b_regression.csv` | LF-normalized text | match |
| 62 | main run | `phase2/reports/tables/phase2b_signal_correlations.csv` | LF-normalized text | match |
| 63 | main run | `phase2/reports/tables/phase2b_structural_h2_sv.csv` | LF-normalized text | match |
| 64 | main run | `phase2/reports/tables/phase2b_structural_h3_sv.csv` | LF-normalized text | match |
| 65 | main run | `phase2/reports/tables/phase2b_structural_h3_sv_jw.csv` | LF-normalized text | match |
| 66 | main run | `phase2/reports/tables/phase2b_structural_h3_svr.csv` | LF-normalized text | match |
| 67 | main run | `phase2/reports/tables/phase2c_pair_regimes.csv` | LF-normalized text | match |
| 68 | main run | `phase2/reports/tables/phase2c_pair_twosidedness.csv` | LF-normalized text | match |
| 69 | main run | `phase2/reports/tables/phase2e_accuracy_by_population.csv` | LF-normalized text | match |
| 70 | main run | `phase2/reports/tables/phase2e_blocks_scored.csv.gz` | gunzip bytes | match |
| 71 | main run | `phase2/reports/tables/phase2e_decided_rate_cells.csv` | LF-normalized text | match |
| 72 | main run | `phase2/reports/tables/phase2e_driver_comparison.csv` | LF-normalized text | match |
| 73 | main run | `phase2/reports/tables/phase2e_generalization.csv` | LF-normalized text | match |
| 74 | main run | `phase2/reports/tables/phase2e_gradient_by_sv.csv` | LF-normalized text | match |
| 75 | main run | `phase2/reports/tables/phase2e_h1_spearman.csv` | LF-normalized text | match |
| 76 | main run | `phase2/reports/tables/phase2e_k_curve.csv` | LF-normalized text | match |
| 77 | main run | `phase2/reports/tables/phase2e_margin_sensitivity.csv` | LF-normalized text | match |
| 78 | main run | `phase2/reports/tables/phase2e_pooled_ads.csv` | LF-normalized text | match |
| 79 | main run | `phase2/reports/tables/phase2e_pooled_cells_sv.csv` | LF-normalized text | match |
| 80 | main run | `phase2/reports/tables/phase2e_pooled_cells_sv_jw.csv` | LF-normalized text | match |
| 81 | main run | `phase2/reports/tables/phase2e_pooled_cells_svr.csv` | LF-normalized text | match |
| 82 | main run | `phase2/reports/tables/phase2e_pooled_init_sv.csv` | LF-normalized text | match |
| 83 | main run | `phase2/reports/tables/phase2e_pooled_sv.csv` | LF-normalized text | match |
| 84 | main run | `phase2/reports/tables/phase2e_pooled_sv_jw.csv` | LF-normalized text | match |
| 85 | main run | `phase2/reports/tables/phase2e_pooled_svr.csv` | LF-normalized text | match |
| 86 | main run | `phase2/reports/tables/phase2e_power_by_size.csv` | LF-normalized text | match |
| 87 | main run | `phase2/reports/tables/phase2e_regression.csv` | LF-normalized text | match |
| 88 | main run | `phase2/reports/tables/phase2e_regression_check.csv` | LF-normalized text | match |
| 89 | main run | `phase2/reports/tables/phase2e_signal_correlations.csv` | LF-normalized text | match |
| 90 | main run | `phase2/reports/tables/phase2e_structural_h2_sv.csv` | LF-normalized text | match |
| 91 | main run | `phase2/reports/tables/phase2e_structural_h3_sv.csv` | LF-normalized text | match |
| 92 | main run | `phase2/reports/tables/phase2e_structural_h3_sv_jw.csv` | LF-normalized text | match |
| 93 | main run | `phase2/reports/tables/phase2e_structural_h3_svr.csv` | LF-normalized text | match |
| 94 | main run | `phase2/reports/tables/phase2e_twosidedness_eval.csv` | LF-normalized text | match |
| 95 | raw path | `phase2/data/MANIFEST_s2and.json` | LF-normalized text | match |
| 96 | raw path | `phase2/data/s2and_blocks.csv.gz` | gunzip bytes | match |
| 97 | raw path | `phase2/data/s2and_blocks_s2and_key.csv.gz` | gunzip bytes | match |
| 98 | raw path | `phase2/data/s2and_signatures.parquet` | DataFrame.equals, sorted columns | match |
| 99 | raw path | `phase2/reports/figs/gate21_ads.png` | bytes | match |
| 100 | raw path | `phase2/reports/figs/gate21_ads_all.png` | bytes | match |
| 101 | raw path | `phase2/reports/figs/gate21_ads_s2and_block.png` | bytes | match |
| 102 | raw path | `phase2/reports/figs/gate21_independence.png` | bytes | match |
| 103 | raw path | `phase2/reports/figs/gate21_sv.png` | bytes | match |
| 104 | raw path | `phase2/reports/figs/gate21_xcheck_ads_homonymity.png` | bytes | match |
| 105 | raw path | `phase2/reports/figs/gate21_xcheck_sv_synonymity.png` | bytes | match |
| 106 | raw path | `phase2/reports/gate21_data_shape.md` | LF-normalized text | match |
| 107 | raw path | `phase2/reports/gate21_two_axes.md` | LF-normalized text | match |
| 108 | paper build | `phase2/paper/main.bbl` | LF-normalized text | match |

## Raw path

`data/MANIFEST_s2and.json` lists 20 files and 260,176,690 bytes (0.26 GB), under the 1 GB limit, so the optional path ran.

- `fetch_s2and.py` downloaded 19 of 20 files, 260,176,690 bytes. `medline/medline_clusters.json` returned HTTP 404, as the committed manifest records.
- An independent sha256 and size check over the 19 downloads against the committed manifest: 19 match, 0 differ.
- The regenerated manifest equals the committed one after LF normalization, including its `local` fields. R5 expected those fields to differ on Linux only, and this run was on Windows.
- `ingest_s2and.py` rebuilt `data/s2and_signatures.parquet` with 766,133 rows. It equals the committed table under `DataFrame.equals`.
- `gate21_two_axes.py` rebuilt both block tables, both gate 2.1 reports and all 7 gate 2.1 figures. All match (rows 95 to 107).

## The paper

Built in the clone from `phase2/paper/`: 31 pages, 607,804 bytes. `main.log` has no undefined reference or citation, and `main.blg` reports 0 warnings. `bibtex` rewrote `main.bbl` with CRLF, and its content is unchanged (row 108).

## Mismatches

None in content.

## Differences below content level

These are not failures. They are recorded because a reader who checks with `git status` will see them.

1. **Line endings.** On Windows, every script writes text with CRLF, and the clone checks out LF. After the full run, `git status --porcelain` in the clone lists 78 tracked files as modified. `git diff` shows no change to any of them.
2. **gzip headers.** The four `.csv.gz` files differ as raw bytes, since gzip records a modification time. `git diff --stat` reports all four as binary changes with no change in size. Decompressed, all four are identical.
3. **No new untracked file.** The work order and the README expect step 4 to leave `phase2/reports/phase2c_pair_probe.md`. It did not. `phase2c_probe.py` defines the path at line 64 and never writes to it. The working repository has no such file either. After all steps, `git ls-files --others --exclude-standard` in the clone prints nothing. Every new file (the two caches, the raw downloads, the LaTeX by-products) is gitignored.

Not exercised: steps 8 and 9 can rebuild the step 6 cache when it is absent. Here it was present, so that path did not run.

## README findings

For the orchestrator to decide. Only the Time column and one line under the table were changed in `phase2/README.md`.

1. **Script paths.** The run-order table names scripts bare (`s2and_blocking.py`) and says to run every command from the repository root. From the root, `python s2and_blocking.py` fails with "can't open file". Run from the root, the scripts need the `phase2/` prefix. The output paths in the same table (`data/...`, `reports/...`) are relative to `phase2/` and not to the root. Suggested fix: name the scripts as `phase2/<script>`, give the command form once, and say the output paths are under `phase2/`.
2. **Step 4 output.** The table says step 4 writes `reports/phase2c_pair_probe.md`, and the notes say it leaves one new untracked file. It writes neither. Suggested fix: drop the file from step 4's row and drop that note.
3. **"Byte-identical" on Windows.** The notes say step 2's constants file "comes out byte-identical". On Windows it comes out with CRLF where the checkout has LF, so a byte comparison fails while `git diff` is clean. More broadly, "On a correct run the content comes out the same" is true, but `git status` then lists 78 files as modified, and the `.csv.gz` files differ in their gzip header. Suggested fix: say the check is `git diff --exit-code`, and that on Windows `git status` shows rewritten files as modified with no diff.
4. **Interpreter patch level.** `py -3.14` takes the newest registered 3.14, whatever its patch release. On this machine it chose 3.14.2, but the launcher also listed a 3.14.0. Suggested fix: add a check after creating the venv, for example `python -VV` should report 3.14.2.
5. **PowerShell activation.** `.venv\Scripts\activate` runs `Activate.ps1` in PowerShell. That worked here under a `RemoteSigned` execution policy for the current user. Under the Windows default `Restricted` policy it would be refused. Suggested fix: an optional note naming `Set-ExecutionPolicy -Scope Process RemoteSigned`, or the cmd form `.venv\Scripts\activate.bat`.

Not a finding: the README's build commands and its 31-page count are right, and the raw path ran in its stated order with no extra step.

All five were fixed in `phase2/README.md` in the commit that adds this report.
