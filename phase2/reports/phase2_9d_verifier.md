# Phase 2.9d: independent verification of "Prediction is not selection"

Checked at V = `26bf2e9ddd22357e4010aa9cc2ae255bc848e6f2` on `phase-2` ("phase-2 gate 2.9c: cold reproduction from a fresh clone"), 2026-11-12. The verifier did none of the earlier work. It read sections 1 and 2 of the master plan and WO-5, and no PASSLOG entry whose heading names gate 2.9. Nothing in the repository was changed except this file and `reports/tables/phase2_9d_number_ledger.csv`, and nothing was staged or committed.

## Preconditions and set-up

```
$ git log -1 --format=%s
phase-2 gate 2.9c: cold reproduction from a fresh clone
$ git status --porcelain              (no output)
$ git ls-files --others --exclude-standard   (no output)
$ ls ../scan_terms.txt                (present)
```

The clone is `git clone --no-hardlinks --branch phase-2 <repository> ../verify/repo`. Its HEAD is V, and it carries tags `v1.0.0` and `v1.1.0`. The paper was built there with the four commands in `phase2/README.md`, using MiKTeX-pdfTeX 4.23 (MiKTeX 25.12). Text was extracted with `pdftotext -layout -enc UTF-8`. This is xpdf's pdftotext 4.06, not poppler's. With the default encoding it wrote Latin-1, so the run used `-enc UTF-8`.

## 1. Number ledger

`reports/tables/phase2_9d_number_ledger.csv`, 829 rows.

| status | rows |
|---|---|
| matched | 801 |
| arithmetic | 26 |
| unmatched | 2 |

**How it was built.** A script tokenized every number in the PDF text: integers with thousands separators, decimals, signed values, percentages and clock-time parts. It stopped at the reference list. It indexed every number in the allowed sources at every printed precision: `reports/**/*.md`, `*.csv` and `*.csv.gz` (except the two per-block `*_blocks_scored` tables), `reports/phase2_9b_reflog_phase2.txt`, `PREREG.md` and `data/MANIFEST*.json`. Fractions were also indexed as percentages. A token matches when a source value rounds to it at the printed precision. With that many source numbers, a four-decimal value can match by coincidence. So candidates were ranked by co-location: a candidate scored higher when neighbouring paper tokens matched the same report line or CSV row. Every row was then read by hand. For about 170 short tokens (design constants, band edges, k values, margins, small counts), the source was set by hand to the line that defines them, mostly in `PREREG.md`.

Four documents were left out of the source set because they quote the paper, so a match there would prove nothing: `reports/OUTLINE.md`, `reports/phase2_7_peer_review.md`, `reports/phase2_6_moderation_audit.md` and `reports/phase2_8a_moderation_audit.md`. `reports/kim2020_positioning.md` is used only for the cited design of Kim and Kim (2020).

**Tables checked cell by cell** against their named sources. Every cell matches at the printed precision:
- Table 1: `reports/phase2e_boundary.md:20-26`.
- Table 2: `phase2e_twosidedness_eval.csv`; the retired row against `phase2b_accuracy_by_population.csv` row 1.
- Table 3: `phase2e_accuracy_by_population.csv`, and `phase2_7b_accuracy_accounting.csv` for the ceiling.
- Table 4: `phase2e_pooled_ads.csv` and `phase2e_pooled_sv.csv`.
- Table 5: `phase2e_driver_comparison.csv` and `phase2_7b_driver_bootstrap.csv`. The 99.9% comes from 0.9985 and the 97.8% from 0.9775, both rounded half up.
- Table 6: `phase2e_margin_sensitivity.csv` and `phase2e_k_curve.csv`.
- Table 7: `phase2_7b_blocksize_pooled.csv` and `phase2_9a_matched_precision.csv`.
- Table 8 (Appendix A): `reports/phase2e_boundary.md:339-546`.

**Excluded tokens** (not ledger rows): 80 cross-reference numbers, 48 heading numbers, 38 citation years, 28 page numbers, 2 document labels ("Amendment 1"), 1 ORCID group and 1 DOI.

**Spelled-out quantities.** Fifteen rows cover quantities written as words that carry a claim. Nine are time intervals in section 6.4, each computed from the commit and file times in `reports/phase2_9b_report.md:417-516`, `reports/phase2_9a_report.md:341-342` and `reports/phase2_9b_reflog_phase2.txt:24`. All nine hold:

| paper wording | computed |
|---|---|
| appends "within half an hour of each other" | 12:36:16 to 13:04:42, 28 min 26 s |
| amendment "just under two hours" before the run commit | 12:36:16 to 14:25:07, 1 h 48 min 51 s |
| addendum "about eighty minutes" before it | 13:04:42 to 14:25:07, 1 h 20 min 25 s |
| `a41a67a` "nine hours" after the freeze (twice) | 01:32:56 to 10:27:06, 8 h 54 min 10 s |
| first run "about seventeen minutes after the addendum" | 13:04:42 to 13:22:07, 17 min 25 s |
| cached predictions "at about twenty-three" | 13:04:42 to 13:27:30, 22 min 48 s |
| script "edited for another forty minutes" | 13:27:31 to 14:07:22, 39 min 51 s |
| `c20239a` "twenty-seven minutes before the amendment" | 12:09:23 to 12:36:16, 26 min 53 s |

One more spelled row, the run time in the availability statement, is unmatched (below).

**Unmatched rows.**

1. **p. 16, `0.0147`**, `main.tex:1021`: "Against the vote its lead is 0.0147, inside the margin." Sources: `phase2b_accuracy_by_population.csv` row 1, fuzzy accuracy 0.8440695; `phase2e_accuracy_by_population.csv` row 1, k-NN accuracy 0.8294401. The difference is 0.0146294, which rounds to **0.0146**. 0.0147 is the difference of the two rounded values. No committed table holds 0.0147 for this comparison.
2. **p. 29, "about twenty minutes"**, `main.tex:1840-1842`: "one full mechanism pass over the corpus takes about twenty minutes on the consumer laptop that produced the reported run." The cold-run log on the same laptop gives 10 min for the 2.2b mechanism pass and 4 min for the 2.2e pass (`reports/phase2_9c_cold_run.md:75`, `:78`), and 19 min for the whole run order (`:82`). Line 88 calls 20 minutes each "the README's earlier figure". The sentence fits the whole run order but not "one full mechanism pass".

Every other row was traced. The `context` column follows pdftotext's layout, which reorders some table columns (Table 3's test-signature column, for example), so a row's context can show neighbours from another table row. The `locator` points at the source row.

## 2. Findings status

Quotes are from `phase2/paper/main.tex` at V.

| ID | Current text (line) | Status |
|---|---|---|
| W1 | "Block size, which we did not pre-register, is the only signal here whose own bands carry a decided verdict when all seven datasets are pooled." (214-215). Both INIT-by-SV cells reported with intervals and the kisti share (1358-1363). | fixed |
| W2 | "Of the five datasets large enough to judge, three are ties at the primary margin and two are decided, in opposite directions and for different reasons." (1471-1473); heading "Where a contest is possible, there is almost nothing to select once the datasets are pooled." (145-146) | fixed |
| W3 | "Where the history is written one way, the rule cannot win either, for mechanisms that read surface forms only." (494-495); also 142-143, 200-201, 1722-1723 | fixed (governance wording: ERRATA 2) |
| W4 | "where the rule commits it is the more accurate arm by 0.0153, with a block-bootstrap interval of $[+0.0142, +0.0165]$" (989-991) | fixed |
| W5 | "the calibration split fixes the band edges and the cutoff of the mechanism we later retired, was used again for the design probe ... and for the regression check ..., and supplies no reported hypothesis number." (600-603); fourth correction (869-876) | fixed (report wording: ERRATA 4) |
| W6 | "a simulated peer review, which the author ran on the manuscript with an AI assistant" (775-776) | fixed |
| W7 | "After its freeze commit the pre-registration file changed three times." (782); third correction (853-867) | fixed |
| W8 | "115 of its 120 clean conditions have intervals inside its two-point margin and the other five cross it on the rules side." (1618-1619) | fixed |
| W9 | "The repository does not carry the raw release. It does carry tables derived from it, redistributed under the same licence with attribution" (1831-1833) | fixed (WDC clause scheduled for WO-6) |
| W10 | "so that on all but the smallest test sets a win has to clear the margin with its whole interval; Section~\ref{sec:h2h3} reports where that protection fails." (383-385) | fixed |
| W11 | "In the radius family the accuracy-maximizing value on the grid is therefore $r = 0.95$, where the vote has shrunk to the rule's own evidence and the pair is nested again." (568); k = 2 "still two-sided at 181 against 736" (569) | fixed |
| W12 | "\emph{reversal} when two bands are decided in opposite directions, \emph{tie-crossing} when at least one band is decided, another is a demonstrated tie and none is decided the other way" (1754-1757); panel "H3, non-direction by ADS" (1785); caption names the third reversal (1769-1770) | fixed |
| O1 | "\section{A comparison only one side can win}" (404); "the rule therefore cannot win at any cutoff" (52-53) | fixed |
| O2 | "whenever the similarity function gives its maximum only to identical strings" (50); fifth correction for the locked sentence (878-883) | fixed |
| O3 | "File-system times on the author's machine, which are not repository evidence ..." (810-818) | fixed |
| O4 | "Across the first four ADS bands mean per-block rule accuracy rises ... In the top band the vote rises again to 0.9889 and the rule falls back to 0.9234" (957-961) | fixed |
| O5 | "which is 42.2\% of held-out signatures on the evaluation split" (512-513, 1653) | fixed |
| O6 | "That is one benchmark and we measured no other." (122-123) | fixed |
| O7 | "to draft the pre-registration and its amendments, ... and to run a simulated peer review and several audits of it" (1848-1851); "The repository's pass log and commit trailers record that involvement pass by pass." (1851-1852) | scheduled for WO-6 (the list is widened; the trailer sentence is the WO-6 item) |
| O8 | "The retired single-nearest retriever, at 0.8441, is more accurate pooled than either mechanism of the amended pair." (1016-1018) | fixed |
| O9 | Governance and report statements: `ERRATA.md` entries 1 to 4, with dated notes in `CLAUDE.md`, `PLAN.md:44-49` and `STATE.md:250-252` | erratum |
| O10 | Bib: `title = {{ADS-Cascade}, version 1.1.0}`, `doi = {10.5281/zenodo.22258609}` (`references.bib:196-202`), fixed. Availability: "The project is archived on Zenodo under the concept DOI 10.5281/zenodo.21644207, which resolves to the latest archived version." (1825-1827) | still open (availability half) |
| U1c | "Inconclusive is evaluated first and neither hypothesis reaches its power floor." (1083-1084) | fixed |
| U2 | "using the 2{,}450 of its blocks that have at least two training signatures and one held-out signature" (538-539) | fixed |
| U3 | "a tie-crossing, at $\delta = 0.03$ in one band and at $\delta = 0.02$ in two" (1133-1134) | fixed |
| U4 | "0.3653 against 0.3765 at the primary margin and turns the other way at the two smaller ones, 0.3972 against 0.3443 and 0.4114 against 0.3418" (1220-1221) | fixed |
| U5 | "(we keep the pre-registration's word, though the split is 70 to 30)" (605) | fixed |
| U6 | "The repository will be pushed and tagged at release" (850); "will be public at release" (1822); locked "are in the public repository" (746-747) | scheduled for WO-6 |
| U7 | "Times are Indian Standard Time, UTC+05:30." (778-779) | fixed |

Counts: fixed 25, erratum 1, scheduled for WO-6 2, still open 1.

W1 carries one point for the reader to weigh. The INIT = 0 by SV-high cell is a pooled, seven-dataset rule win made of matching, not abstention (724 rule-right signatures against 77, `phase2_9b_init.csv`). The paper reports it and attributes it to kisti (1361-1363). The summary claim "no design-time signal we examined tells a designer which mechanism resolves a name better" (1426-1427) depends on that attribution. That is a reading the paper states openly, not a defect.

## 3. Headline numbers, re-derived

Re-derived with the Python standard library from `reports/tables/phase2e_blocks_scored.csv.gz` (13,902 rows) and other committed tables. The Experiment 1 table came from the `v1.1.0` tag (`git show v1.1.0:data/outputs/experiments/exp1/final/final_condition_results.csv`). The bootstraps use the verifier's own seeds, so the intervals agree with the committed ones to about the third decimal, not exactly.

```
per-block rows 13902
1. rule accuracy = 162810 / 197479 = 0.824442;  k-NN accuracy = 163797 / 197479 = 0.829440
   rule fires on 191270 / 197479 = 0.968559; rule precision where it fires = 162810 / 191270 = 0.851205
2. vote accuracy on those signatures (phase2_9a_matched_precision.csv, pooled, knn_acc_fired) = 0.835886
   matched difference = 0.851205 - 0.835886 = 0.015319; committed interval [0.014168, 0.016544], B = 2000
3. contested share (ADS < 1 and SV > 0) = 83401 / 197479 = 0.422328  (2770 of 13902 blocks)
4. kisti: 711 blocks, 10147 test sigs; gap = (8590 - 7442) / 10147 = +0.113137; independent block bootstrap (B = 2000, my seed) [+0.1016, +0.1257] -> rule wins at delta 0.05
5. zbmath: 847 blocks, 3838 test sigs; gap = (3260 - 3502) / 3838 = -0.063054; independent block bootstrap (B = 2000, my seed) [-0.0753, -0.0506] -> k-NN wins at delta 0.05
6. v1.1.0 Experiment 1 table: 240 rows; columns include ['lexical_variation', 'p_transform', 'paired_diff_point', 'paired_diff_ci_low', 'paired_diff_ci_high']
   clean (p_transform = 0) conditions: 120; interval inside [-0.02, +0.02]: 115; outside: 5
     seed 31001: [+0.0086, +0.0211]
     seed 31016: [+0.0090, +0.0233]
     seed 31009: [+0.0080, +0.0204]
     seed 31014: [+0.0096, +0.0224]
     seed 31005: [+0.0060, +0.0203]
```

| Headline | Re-derived | Paper | Agrees |
|---|---|---|---|
| 0.8244 and 0.8294 | 0.824442 and 0.829440 | 0.8244, 0.8294 | yes |
| 0.0153 [+0.0142, +0.0165] | 0.015319; interval 0.014168 to 0.016544 from `phase2_9a_matched_precision.csv` | 0.0153 [+0.0142, +0.0165] | yes |
| 42.2% | 83,401 / 197,479 = 0.4223 | 42.2% | yes |
| kisti | +0.1131, rule wins (lower bound 0.1016 > 0.05) | +0.1131 [+0.1015, +0.1250], rule wins | yes |
| zbmath | -0.0631, k-NN wins (upper bound -0.0506 < -0.05) | -0.0631 [-0.0761, -0.0512], k-NN wins | yes |
| 115 of 120 | 115 inside ±0.02, 5 outside, all on the rules side | 115 of 120 | yes |

The per-block table has no count of the vote's correct answers restricted to the signatures where the rule fires. So the vote side of 0.0153 and its interval come from `phase2_9a_matched_precision.csv`, not from an independent bootstrap. The rule side was re-derived independently.

zbmath's verdict sits near the margin. The committed upper bound clears -0.05 by 0.0012 and this bootstrap's by 0.0006. Section 7.8 declines to count the non-inspire SV-high band, which clears by 0.0001, because "another bootstrap seed could undo" it (1495-1496). zbmath held under a second seed here, and it is reported as decided.

## 4. Cross-references

69 `\ref`, 0 `\autoref`. Each citing sentence was read against its target.

```
155 sec:per-dataset   167 sec:blocksize    180 sec:per-dataset  185 sec:no-selector
205 sec:degenerate    213 sec:design, sec:results              219 sec:blocksize
226 sec:calibration-trap, sec:portfolio    273 sec:winner-construct  277 sec:blocks
306 sec:compression   350 sec:limitations  363 sec:earlier-synthetic 385 sec:h2h3
466 sec:data          510 sec:repaired-pair 540 sec:prereg-integrity 571 sec:degenerate
580 sec:portfolio     596 tab:population   602 sec:candidates   603 sec:two-sided
647 sec:blocks        682 sec:axes         693 sec:candidates   795 sec:degeneracy-measured
820 sec:two-sided     859 sec:h2h3         882 sec:containment  900 sec:candidates
907 tab:twosided      961 fig:h1           971 sec:general-form 998 tab:accuracy
1007 tab:accuracy     1016 tab:twosided    1023 sec:calibration-trap 1098 tab:falsification
1101 fig:power        1111 sec:h2h3        1124 tab:bands, fig:grid  1158 app:margins
1169 fig:grid         1211 tab:drivers     1288 sec:h2h3        1351 tab:blocksize
1364 sec:per-dataset  1381 app:margins     1411 sec:h2h3        1422 sec:winner-construct
1532 sec:conditions   1554 sec:blocksize   1606 sec:degenerate  1671 tab:bands, tab:falsification
1675 sec:prereg-integrity 1686 sec:per-dataset 1689 sec:blocks  1697 sec:blocksize
1751 tab:margingrid   1754 sec:winning     1760 sec:compression 1769 tab:bands
1770 sec:per-dataset  1808 sec:earlier-synthetic 1824 sec:prereg-integrity 1843 sec:data
```

Mismatches:

1. **1686**, Limitations: "Section~\ref{sec:per-dataset} gives the band tables in all three forms the pre-registration requires." Section 7.8 gives prose and selected values. The tables are in `reports/phase2_9b_report.md` and `reports/tables/phase2_9b_*.csv`, as section 7.8 itself says (1466-1467).
2. **510**, minor: "The calibration-split probe of Section~\ref{sec:repaired-pair} shows the same two lines of zeros for all three candidate pairs." The data supports it. Every probe pair has 0 rule-right signatures at ADS = 1.0 and at SV = 0 (`phase2c_pair_regimes.csv`, checked for all 11 pairs). But section 5 does not print those zeros, so a reader following the reference will not find them there.

Two targets were checked against data because the sentence claims a fact. Both hold. For 1684-1686, "no dataset shows a surface-driven winner reversal": every `winner reversal` row in `phase2_9b_structure_by_population.csv` runs across ADS at fixed SV. For 1760, the appendix reversals are the two section 7.5 reports.

## 5. Definition-of-complete checks

HEAD (V) stands in for the release tag.

**A3, the locked quote.** sha256 over `\begin{quote}` through `\end{quote}` plus a trailing newline, computed in the working repository and in the clone:

```
quotes in file: 1 | CRLF in file: False
sha256 dcaa1bce36335d50958a66b825f427f83e5fef9f3dc6aeb6dde2ce45ee45f8f4
quotes in file: 1 | CRLF in file: False
sha256 dcaa1bce36335d50958a66b825f427f83e5fef9f3dc6aeb6dde2ce45ee45f8f4
$ grep -n -E 'dcaa1bc|f8f4' phase2/STATE.md
29:  and the locked 6.4 quote is byte-identical (sha256 `dcaa1bc…f8f4`). No
116:  quote is byte-identical (sha256 `dcaa1bc…f8f4`, computed over
```

Pass. The plan cites `STATE.md:50`; the value now sits at lines 29 and 116.

**A4.**

```
$ git diff aeef06c HEAD -- phase2/PREREG.md | wc -c
0
$ git log --format='%h %s' -- phase2/PREREG.md
3e79a48 phase-2 gate 2.2d: PREREG Addendum 1a, resolution 5 debiased
5f452ad phase-2 gate 2.2d: PREREG Amendment 1, the two-signal reframe
a41a67a phase-2 gate 2.2a: fold two reviewer rules into the frozen pre-registration
8869b82 phase-2 gate 2.2a: freeze the pre-registration, before any accuracy exists
```

Pass. This also bears out `phase2/README.md`'s "has not changed since commit `3e79a48`".

**A5.** The eight hashes printed in the paper (footnote, `main.tex:804-809`) and `aeef06c`:

```
8869b82 8869b82061384f5540b8021d0882d55bc1110d35 ancestor=yes
a41a67a a41a67a80016ad8ec87fb872b2951bab959095a0 ancestor=yes
5e13e38 5e13e381d95406a9c0aca6c33729a2fd38118013 ancestor=yes
3d86959 3d86959955e5efb43aca7d955e37bb62e98f9d99 ancestor=yes
c20239a c20239a7ccec39ec48cf70e44a95d48ee5f27a6b ancestor=yes
5f452ad 5f452ad770d45a9585cd552df24474602392c86f ancestor=yes
3e79a48 3e79a489d427fc0192df37cd4054e88b0ef12d1f ancestor=yes
9e3d921 9e3d9212029fee8b0e69edddb9d1c99828bac4ab ancestor=yes
aeef06c aeef06c1a9498e691942558e797d39b52952252a ancestor=yes
```

Pass. Every commit time the paper states matches `git log --format=%ci` (`c20239a` 12:09:23 +0530; `a41a67a` 10:27:06; `8869b82` 01:32:56).

**A6.**

```
undefined/multiply-defined in main.log: 0
em dash U+2014 in main.tex: 0
'---' in main.tex: none
em dash U+2014 in PDF text: 0
'--' in main.tex: only the en-dash ranges of Table 7 (lines 1446-1451)
```

All 49 headings (`\section`, `\subsection`, `\section*`) are in sentence case. Pass.

**A7.**

```
$ git diff aeef06c HEAD --stat -- 'phase2/*.py'
 phase2/phase2_9b_supplement.py | 276 +++++++++++++++++++++++++++++++++++++++++
 1 file changed, 276 insertions(+)
$ git diff aeef06c HEAD --name-status -- 'phase2/*.py'
A	phase2/phase2_9b_supplement.py
```

Pass: one new file, no existing script changed.

**B5.** In the clone, from `phase2/paper/`: `pdflatex main`, `bibtex main`, `pdflatex main`, `pdflatex main`.

```
Output written on main.pdf (31 pages, 607804 bytes).
```

Pass. The 31 pages are what the README says to expect. `bibtex` rewrites the committed `main.bbl` with CRLF line endings, so `git status` lists it as modified. `git diff --ignore-cr-at-eol` shows no change.

**C4.** `phase2/DATA_LICENSES.md` against the tracked files:

```
$ git ls-files phase2/data 'phase2/reports/tables/*.gz'
phase2/data/MANIFEST.json
phase2/data/MANIFEST_s2and.json
phase2/data/phase2b_blocks.parquet
phase2/data/s2and_blocks.csv.gz
phase2/data/s2and_blocks_s2and_key.csv.gz
phase2/data/s2and_signatures.parquet
phase2/data/wdc_lspc2017_offers.csv.gz
phase2/reports/tables/phase2b_blocks_scored.csv.gz
phase2/reports/tables/phase2e_blocks_scored.csv.gz
```

```
phase2/data/s2and_blocks.csv.gz 26939 rows 9 cols
phase2/data/s2and_blocks_s2and_key.csv.gz 27658 rows 9 cols
phase2/data/wdc_lspc2017_offers.csv.gz 15179 rows 6 cols
phase2/reports/tables/phase2b_blocks_scored.csv.gz 13902 rows 54 cols
phase2/reports/tables/phase2e_blocks_scored.csv.gz 13902 rows 91 cols
phase2/data/s2and_signatures.parquet 766133 rows, 19 columns as listed
phase2/data/phase2b_blocks.parquet 18984 rows, 13 columns as listed
csv tables under reports/tables with a name, key, affiliation or label column: []
```

Pass. The notice names every tracked data file. Each row count and column list matches, and its claim that every other table holds aggregates only holds. The paper's availability statement has no clause for the WDC extract; that item is scheduled for WO-6.

## 6. Public-text scan at V

```
$ git grep -c -i -w -F -f ../scan_terms.txt HEAD
(no output, exit 1)
$ case-insensitive search for the four leftover-wording terms (kept outside the repository)
1 line: phase2/PASSLOG.md:3333
```

As expected: one line, in `phase2/PASSLOG.md`. Line 3333 falls under the "Checks" subheading of Pass 24, whose heading names gate 2.9b. Under the read rules for this pass, that line was located by heading and not read.

## 7. Old strings in main.tex

```
0.0218            0
external read     0
redistribute none 0
will be public    1   (line 1822, availability statement)
⟦                 0
will be pushed    1   (line 850, section 6.4)
```

Both hits are the future-tense release wording scheduled for WO-6. "will be public" was on the list of strings that should be absent. It is present, and it falls under the WO-6 item.

## 8. README cold read

Read as someone who knows Python and LaTeX but not this project.

`phase2/README.md`:
1. The overview calls SV "surface stability (SV)". The paper defines SV as surface *variability*, the inverse of stability (`main.tex:363-366`). A reader who takes SV for stability gets the sign of every SV statement backwards.
2. The build section doesn't say that `bibtex main` rewrites the committed `main.bbl`. On Windows that leaves `git status` dirty with only a line-ending change. The run-order notes explain this for the scripts but not for the paper.
3. The licence section covers code (MIT), `paper/` and `reports/` (CC BY 4.0) and derived data. `PREREG.md`, `PASSLOG.md`, `STATE.md`, `PLAN.md`, `CLAUDE.md`, `ERRATA.md`, `DATA_LICENSES.md` and the two READMEs fall under none of them. `LICENSE-TEXT` limits itself to `phase2/paper/` and `phase2/reports/`.
4. `<DOI>` placeholder (line 15): scheduled for WO-6.
5. Everything else could be followed: the environment and pins, the run order with outputs and times, the line-ending note, the tags needed for step 9 (a plain clone has them), and the optional raw-data route. The figure note holds: the five files in `paper/figs/` are byte-identical to `reports/figs/`.

Root `README.md`: short and correct. It points to `phase2/README.md`, states the licences and marks the old tags deprecated. The `<DOI>` placeholder is scheduled for WO-6.

## Other observations

- The figure captions still give the PNG as their own source (`main.tex:972`, `1112-1113`, `1198-1199`). Plan section 1.4 lists this as cosmetic, with `phase2e_run.py` as the source to name.
- pdftotext drops the fi, ff and fl ligatures ("classication", "cuto"). If the PDF lacks a ToUnicode mapping for those glyphs, copying from and searching the released PDF will break those words. This was seen with one extractor only (xpdf 4.06) and was not confirmed with another.
- The bib page fields that plan section 1.4 asked for are present (`hendrickx2024`, `s2and2021`, `backes2018`).

## Still open

Findings that are not fixed, not in `ERRATA.md` and not scheduled for WO-6:

1. **`main.tex:1021`, "its lead is 0.0147".** From the committed accuracies the lead is 0.0146 (0.8440695 - 0.8294401 = 0.0146294). Ledger row, page 16.
2. **`main.tex:1840-1842`, "one full mechanism pass over the corpus takes about twenty minutes".** The committed cold-run log on the same laptop gives 10 min and 4 min per pass and 19 min for the whole run order (`reports/phase2_9c_cold_run.md:75,78,82,88`). Ledger row, page 29.
3. **O10, availability half, `main.tex:1825-1827`.** "The project is archived on Zenodo under the concept DOI 10.5281/zenodo.21644207, which resolves to the latest archived version." At V that concept holds only the earlier, deprecated work that the README marks "kept for the record only". WO-6 adds the paper DOI. Whether this sentence then still points at the right object depends on where the paper record is minted, so it is listed here for the author's ruling.
4. **Cross-reference, `main.tex:1686`.** Limitations says section 7.8 "gives the band tables in all three forms". The tables are in `reports/phase2_9b_report.md`; section 7.8 summarizes them.
5. **Cross-reference, `main.tex:510`, minor.** The "two lines of zeros" are not shown in section 5. They are in `reports/tables/phase2c_pair_regimes.csv`.
6. **`phase2/README.md`, "surface stability (SV)".** SV is surface variability.
7. **Licence coverage.** The governance and record files under `phase2/` (`PREREG.md`, `PASSLOG.md`, `STATE.md`, `PLAN.md`, `CLAUDE.md`, `ERRATA.md`, `DATA_LICENSES.md`, the READMEs) are covered by neither `LICENSE` nor `LICENSE-TEXT`.
8. **Cosmetic, figure captions** (`main.tex:972`, `1112-1113`, `1198-1199`) name the PNG as its own source.

Open and scheduled for WO-6, as listed in the work order: the `<DOI>` placeholders in `README.md:7`, `phase2/README.md:15` and `CITATION.cff:23`; the drafting comments at `main.tex:1-4`; the future tense at `main.tex:850-851` and `1821-1823` (with the locked quote's "are in the public repository" becoming true at the push); the availability statement's WDC clause and paper DOI; the title page's preprint line and the PDF metadata; and the commit-trailer sentence at `main.tex:1851-1852`.
