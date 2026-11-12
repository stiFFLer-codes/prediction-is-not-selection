# Phase 2.9a: release-pass facts, and the like-for-like precision comparison

Pass 2.9a, 2026-11-12, on `phase-2` at `9a5e998` before this pass's commit. It
gathers the facts the 2.9b manuscript edits need (Part A, read-only) and adds one
analysis script with three tables (Part B, new files only). Nothing in
`phase2/paper/`, `PREREG.md`, or any existing report, table or figure was touched.
Nothing was pushed, tagged or released. The only network calls were seven
read-only Crossref GETs (A5).

Times are IST (+05:30) unless stated. "Holds" means checked against the named
evidence in this pass, not recalled.

## Summary

1. **The matched comparison.** On the items where the rule fires, the rule's
   precision is 0.8512 and the vote's accuracy on those **same** items is 0.8359.
   The like-for-like margin is **+0.0153 [+0.0142, +0.0165]**, not the +0.0218 the
   paper prints, which subtracts the vote's accuracy on all items (0.8294). The
   rule is ahead on matched items in every block-size band and every dataset, and
   every interval excludes zero.
2. **a41a67a** added three passages to the frozen `PREREG.md`: a revision note,
   "Margin sensitivity" and "Order of evaluation". Nothing was written to the
   repository, its git object store or the temp folder between the freeze
   (01:32:56) and a41a67a (10:27:06). The first post-freeze Python import of the
   pipeline was at 10:33:08. **No calibration or evaluation number existed before
   a41a67a.** The "reviewer" was the between-pass reviewer of the 2.2a freeze. The
   repository does not say whether that was the human author or an orchestrating
   AI chat. It was not the simulated peer review, which came three days later.
3. **Section 8.3**, claims (a) to (l): eleven hold. Claim (j), "demonstrated
   equivalent there at that study's own margin", does not follow from (i), and
   the committed data contradict it for 5 of the 120 clean conditions.
4. **Section 4.3's second region does not hold as written.** In the SV = 0 band
   the rule is never right where the vote is wrong (0), but the vote is right
   where the rule is wrong on **696** signatures, every one a rule abstention on
   one of the **835** test forms the training half never shows. That is the
   source of Table 4's `k-NN wins` at delta 0.03 and 0.02. A narrower correct
   version is in A3.
5. **The containment argument is valid for the two functions used.** It checks
   out analytically and on the data: 0 of 210,537 distinct-form pairs score 1.0
   in either arm. Its wording ("any similarity function", "the containment holds
   for all of them") is too broad. rapidfuzz's own token and partial ratios
   give the maximum to distinct strings. The condition the argument needs is in A4.
6. **The evaluation-split contested share is 42.23%** (83,401 of 197,479 held-out
   signatures, in 2,770 of 13,902 blocks), against the 41% calibration figure
   the paper quotes.
7. **Environment.** The committed runs were made with CPython 3.14.2. None of the
   seven scientific packages has changed since 2026-09-18, and the 2.9a run
   reproduces the frozen population exactly under that interpreter.

---

## Part B: what was computed

Script: `phase2/phase2_9a_matched.py`, in the conventions of
`phase2_7b_reanalysis.py`.

- **Inputs:** the same as 2.7b. These are
  `reports/tables/phase2e_blocks_scored.csv.gz`,
  `data/phase2e_eval_sigs.parquet` (gitignored; reused, and rebuilt by the frozen
  `phase2e_run.mechanism_pass` if absent) and `data/s2and_signatures.parquet`
  through `phase2b_build.load_signatures`.
- **Bootstrap:** the frozen `phase2b_core.pooled_block_ci`, resampling blocks,
  B = 2000, seed `band_seed("p29a|matched|<population>")` under the frozen CRC32
  scheme.
- **Bands:** the seven block-size octaves are `phase2_7b_reanalysis.bsize_band`,
  imported rather than restated.

**Halting checks, run before anything is computed.** The script re-derives
13,902 blocks, 197,479 test signatures, rule accuracy 0.824442 and k-NN accuracy
0.829440, and exits otherwise. It then checks that six per-block counts
aggregated from the per-signature cache equal the committed per-block record,
block for block: n_test, rule correct, rule fires, k-NN correct, rule-right-vote-wrong
and vote-right-rule-wrong. All passed:

```
frozen primary population reproduced: 13,902 blocks, 197,479 test signatures, rule 0.824442, k-NN 0.829440
every per-block count agrees with reports/tables/phase2e_blocks_scored.csv.gz
```

**Structural checks, also asserted in the code.** In the SV = 0 band, the
ADS = 1.0 band and their intersection, rule-right-vote-wrong is 0. In the same
three, every vote-right-rule-wrong signature is a rule abstention. SV = 0 is
exactly the set of blocks whose training half carries one distinct surface
form; this is checked block by block against the signature table. The contested
count equals the sum over the 12 qualifying cells of the committed
`phase2e_pooled_cells_sv.csv`.

**Determinism.** Two consecutive runs gave byte-identical tables:

```
408d56d5…445902  phase2_9a_contested_share.csv
426e06c6…fe334b  phase2_9a_matched_precision.csv
89f2a06f…c672649 phase2_9a_region_counts.csv
```

Runtime was 47 s with the evaluation cache present.

**Line endings.** The hashes above are of the files as pandas wrote them on
Windows, with CRLF. Git stores them as LF under `.gitattributes`
(`* text=auto eol=lf`), as it does every other table. The committed blobs hash
to:

```
90f3dfc8…420b  phase2_9a_contested_share.csv
5512d259…d260  phase2_9a_matched_precision.csv
2e48be7b…81c7  phase2_9a_region_counts.csv
```

Compare against those on a fresh LF checkout.

### B1. Matched precision (`reports/tables/phase2_9a_matched_precision.csv`)

The rule's precision where it fires, set against the k-nearest vote (k = 5,
Levenshtein) on all items and on the **same items the rule fired on**. The
matched difference is (rule right minus vote right) summed over fired items,
divided by fired items. Its interval resamples blocks.

| population | blocks | test sigs | rule fired | rule coverage | rule precision (fired) | k-NN acc (all) | k-NN acc (fired) | matched diff | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| pooled | 13,902 | 197,479 | 191,270 | 0.9686 | 0.8512 | 0.8294 | 0.8359 | +0.0153 | [+0.0142, +0.0165] |
| 3-4 | 2,227 | 3,145 | 2,649 | 0.8423 | 0.9370 | 0.9037 | 0.9230 | +0.0140 | [+0.0084, +0.0196] |
| 5-8 | 2,188 | 5,323 | 4,752 | 0.8927 | 0.9529 | 0.9218 | 0.9388 | +0.0141 | [+0.0099, +0.0184] |
| 9-16 | 2,181 | 8,675 | 7,996 | 0.9217 | 0.9391 | 0.9006 | 0.9130 | +0.0261 | [+0.0209, +0.0316] |
| 17-32 | 2,293 | 17,194 | 16,370 | 0.9521 | 0.9424 | 0.9090 | 0.9172 | +0.0252 | [+0.0214, +0.0293] |
| 33-64 | 2,204 | 32,059 | 30,875 | 0.9631 | 0.9560 | 0.9276 | 0.9375 | +0.0185 | [+0.0159, +0.0213] |
| 65-128 | 1,652 | 45,924 | 44,943 | 0.9786 | 0.9599 | 0.9393 | 0.9456 | +0.0144 | [+0.0118, +0.0169] |
| 129+ | 1,157 | 85,159 | 83,685 | 0.9827 | 0.7194 | 0.7014 | 0.7076 | +0.0118 | [+0.0099, +0.0138] |
| aminer | 842 | 40,006 | 39,205 | 0.9800 | 0.4159 | 0.4038 | 0.4089 | +0.0071 | [+0.0057, +0.0086] |
| arnetminer | 82 | 1,620 | 1,587 | 0.9796 | 0.5198 | 0.5099 | 0.5154 | +0.0044 | [+0.0015, +0.0083] |
| inspire | 11,110 | 139,369 | 135,252 | 0.9705 | 0.9771 | 0.9645 | 0.9689 | +0.0082 | [+0.0073, +0.0092] |
| kisti | 711 | 10,147 | 9,353 | 0.9218 | 0.9184 | 0.7334 | 0.7885 | +0.1299 | [+0.1173, +0.1437] |
| pubmed | 34 | 803 | 762 | 0.9489 | 0.8451 | 0.5554 | 0.5748 | +0.2703 | [+0.1996, +0.3414] |
| qian | 276 | 1,696 | 1,675 | 0.9876 | 0.6155 | 0.5896 | 0.5946 | +0.0209 | [+0.0111, +0.0336] |
| zbmath | 847 | 3,838 | 3,436 | 0.8953 | 0.9488 | 0.9125 | 0.9267 | +0.0221 | [+0.0149, +0.0298] |

**Pooled, the unmatched figure the paper prints is 0.8512 − 0.8294 = +0.0218.
The matched one is +0.0153 [+0.0142, +0.0165].**

The vote is more accurate on the items the rule fires on (0.8359) than over
everything (0.8294). The unmatched subtraction therefore overstates the rule's
edge by 0.0064. The qualitative claim survives everywhere: the rule is the more
accurate arm where it commits, in all seven bands and all seven datasets, with
every lower bound above zero. These are the numbers for main.tex:158, 209-210,
911-913, 1297-1302 and the Table 7 footer at 1359-1360, all re-checked in this
pass. The matched comparators for the footer's seven k-NN values are, in band
order: 0.9230, 0.9388, 0.9130, 0.9172, 0.9375, 0.9456 and 0.7076. For
"0.9370 against 0.9037 in the smallest" (main.tex:1298) the matched comparator
is 0.9230. "The rule is ahead in all seven" still holds.

Two datasets stand out: kisti (+0.1299) and pubmed (+0.2703, 34 blocks). There,
the vote's pooled neighbourhood most often overrides a form's own evidence and
gets it wrong.

### B2. Region counts (`reports/tables/phase2_9a_region_counts.csv`)

| axis | band | blocks | test sigs | rule right, vote wrong | vote right, rule wrong | of which rule abstained | form absent from training half |
|---|---|---:|---:|---:|---:|---:|---:|
| SV band | SV=0 | 4,517 | 17,960 | 0 | 696 | 696 | 835 |
| SV band | SV low | 3,032 | 56,408 | 225 | 1,036 | 1,010 | 1,229 |
| SV band | SV mid | 3,218 | 59,433 | 391 | 1,074 | 1,061 | 1,321 |
| SV band | SV high | 3,135 | 63,678 | 2,409 | 1,206 | 1,150 | 2,824 |
| ADS band | [0,0.5) | 1,071 | 47,167 | 1,823 | 247 | 205 | 1,632 |
| ADS band | [0.5,0.7) | 1,101 | 16,079 | 629 | 284 | 252 | 687 |
| ADS band | [0.7,0.9) | 743 | 12,660 | 414 | 258 | 249 | 473 |
| ADS band | [0.9,1.0) | 450 | 12,683 | 159 | 194 | 182 | 238 |
| ADS band | 1.0 | 10,537 | 108,890 | 0 | 3,029 | 3,029 | 3,179 |
| cell | ADS=1.0 x SV=0 | 3,922 | 12,772 | 0 | 666 | 666 | 738 |

Both axes sum to the published totals:

- rule right, vote wrong: 3,025;
- vote right, rule wrong: 4,012 (`phase2e_twosidedness_eval.csv`, k = 5);
- form absent from the training half: 6,209 = 197,479 − 191,270.

The rule fires exactly when the test form occurs in the training half
(`phase2e_mech.py:94`), so the last column is the rule's abstention count. A3
reads this table.

### B3. Contested share, evaluation split (`reports/tables/phase2_9a_contested_share.csv`)

| split | definition | blocks | of blocks | test signatures | of test signatures | share |
|---|---|---:|---:|---:|---:|---:|
| evaluation | ADS < 1 and SV > 0 | 2,770 | 13,902 | 83,401 | 197,479 | 0.4223 |

The paper's 41% is the calibration-split figure, 14,680 / 35,732 = 0.4108 from
`phase2c_pair_regimes.csv`. The evaluation figure is **42.2%**.

### B4. Max-score collisions (printed by the script, no table)

The script scored every pair of distinct surface forms inside every primary
block, train and test together, exactly as the mechanisms score them:
`rapidfuzz.process.cdist`, float32, no processor. There are 210,537 such pairs.
**0 score 1.0 under Levenshtein and 0 under Jaro-Winkler.** See A4.

---

## Environment (A6)

**Which interpreter produced 9e3d921 and 4dad8fb.** PASSLOG, STATE, PLAN and
the reports record no interpreter or library version anywhere. I grepped all
four for "python 3", "3.14", "cpython", "interpreter", "pip" and "version" and
found nothing relevant. The evidence is forensic:

- **Bytecode tags.** Every file in `phase2/__pycache__/` is tagged
  `cpython-314`, with these mtimes:
  - `phase2e_run.cpython-314.pyc`: 2026-09-18 14:07:22, which is 18 min before
    9e3d921 at 14:25:07;
  - `phase2e_mech`: 2026-09-18 13:22:07;
  - `phase2b_core`: 2026-09-18 10:33:08;
  - `phase2_7b_reanalysis.cpython-314.pyc`: 2026-09-21 14:17:09, which is
    14 min before 4dad8fb at 14:31.

  That last timestamp was read before this pass ran anything. This pass's run
  rewrote that one `.pyc`, now 2026-11-12 10:30:43, because its source was
  edited after it was compiled (source mtime 2026-09-21 14:28:53). The file is
  gitignored, and no tracked file changed.
- **Interpreters on the machine** (`py -0p`):
  - CPython 3.14.2 at `...\Programs\Python\Python314\python.exe` (the launcher
    default);
  - CPython 3.12.10 at `...\Python312\python.exe` (first on the bash `PATH`);
  - uv-managed 3.14.0 and 3.12.13.

  **Only 3.14.2 has numpy, pandas, rapidfuzz, unidecode or pyarrow installed.**
  The other three have none of them. There is no venv in the repository.
- **Conclusion.** The committed Phase 2 runs were made by CPython 3.14.2 at
  `C:\Users\MaitreyaSapariya\AppData\Local\Programs\Python\Python314\python.exe`.
  This is a strong inference from bytecode tags and elimination, not a recorded
  fact: it cannot exclude an interpreter that has since been deleted.

**Now:** `Python 3.14.2 (tags/v3.14.2:df79316, Dec 5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]`,
Windows-11-10.0.26100-SP0. This is also the interpreter that produced the 2.9a
tables.

| package | installed | package folder mtime | dist-info mtime | changed since 2026-09-18? |
|---|---|---|---|---|
| numpy | 2.4.2 | 2026-02-19 14:34:48 | 2026-02-19 14:34:58 | no |
| pandas | 3.0.1 | 2026-02-19 14:36:20 | 2026-02-19 14:36:20 | no |
| scipy | 1.17.0 | 2026-02-19 14:35:08 | 2026-02-19 14:36:11 | no |
| pyarrow | 24.0.0 | 2026-08-04 12:04:16 | 2026-08-04 12:04:25 | no |
| rapidfuzz | 3.14.5 | 2026-05-18 17:05:04 | 2026-05-18 17:05:05 | no |
| unidecode | 1.4.0 | 2026-06-15 18:00:31 | 2026-06-15 18:00:36 | no |
| matplotlib | 3.11.1 | 2026-09-06 23:17:17 | 2026-09-06 23:17:40 | no |

These are the versions reported by `importlib.metadata`.

**Packages installed after 2026-09-18.** The only dist-info folders newer than
that date are these, all dated 2026-10-01 16:46-16:47:

- formulaic 1.2.2
- interface_meta 2.0.1
- patsy 1.0.3
- seaborn 0.13.2
- wrapt 2.5.0
- scikit_posthocs 0.17.0
- statsmodels 0.15.0

None of them is imported by Phase 2 code. The seven scientific packages' own
dist-info folders keep their earlier dates. The 2.9a run reproduces the frozen
population and every per-block count exactly, which is the functional check
that nothing which matters has moved. The full `pip freeze` (270 lines) is the
appendix.

---

## A1. The post-freeze edit a41a67a

**The commit.** `a41a67a80016ad8ec87fb872b2951bab959095a0`, author and committer
Maitreya Sapariya, both dates 2026-09-18 10:27:06 +0530. Trailer:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. It touches
`phase2/PASSLOG.md` (+26), `phase2/PREREG.md` (+25) and `phase2/STATE.md`
(+5 −2).

**Added to PREREG.md, verbatim** (`git show a41a67a -- phase2/PREREG.md`).

The revision note, after the amendment rule near the top:

> **Revision history.** 2026-09-18, review of the 2.2a freeze, still before any
> measurement and before 2.2b starts: two rules were added at the reviewer's
> instruction, verbatim. Section 8 gained "Margin sensitivity", which makes delta
> = 0.05 the primary margin and requires a 0.02 and 0.03 robustness curve beside
> it. Section 10 gained "Order of evaluation", which makes Inconclusive take
> precedence over every other outcome row. Both tighten the rules; neither relaxes
> one. Recorded here rather than applied silently, because this document's
> authority comes from being fixed in advance. See commit history for the exact
> diff.

Section 8, a new subsection:

> ### Margin sensitivity
>
> **Margin sensitivity, pre-registered.** The primary margin is delta = 0.05. Every
> band-level and cell-level verdict, and the H2 and H3 outcomes, are also
> recomputed at delta = 0.02 and delta = 0.03 and reported as a robustness curve
> beside the primary. An H2 or H3 outcome that holds at one margin and flips at
> another is reported as margin-dependent and treated as Partial, not Supported.
> Fixed now so the margin cannot be chosen after seeing results.

Section 10, before the H1 table:

> **Order of evaluation.** **Inconclusive is evaluated first.** If a hypothesis's
> Inconclusive power floor is met, the outcome is Inconclusive regardless of the
> other rows. In particular, a set of bands that are all tie or undecided is not H2
> Supported unless there are at least two ADS bands and two SV bands, each with 30
> or more blocks and a decided pooled verdict.

**Which review, when, and by whom.** The only sources in the repository are the
following, quoted verbatim.

- The commit message: "Applied verbatim at review of the 2.2a freeze, still
  before any measurement and before 2.2b starts."
- `PASSLOG.md:782-785`: "### Pass 5, addendum — two reviewer rules folded into
  PREREG.md / Applied at review of the 2.2a freeze, still before any measurement
  and before 2.2b starts. Both were supplied by the reviewer and are inserted
  verbatim."
- `PASSLOG.md:791` and `:797-798`, in the agent's first person: "This closes a
  hole I left" and "This closes a real loophole in the H2 Supported row as I
  wrote it".
- `PASSLOG.md:847-848` and `:857`: "Inconclusive evaluated first per the 2.2a
  reviewer rule" and "This is the reviewer rule added at the 2.2a freeze".

So the rules were written outside the agent session that drafted PREREG, by
whoever reviewed the 2.2a pass, and were pasted in verbatim. The charter's pass
protocol requires that review between passes ("Then stop... Wait for review",
`CLAUDE.md:139`).

**I cannot determine whether that reviewer was the human author or an
orchestrating AI chat.** No document says, and no 2026-09 session transcript
survives. `~/.claude/projects/c--Users-MaitreyaSapariya-Desktop-personal-research/`
holds only the two 2026-11-12 sessions.

It was **not** the simulated peer review. That review is
`reports/phase2_7_peer_review.md`, headed "Simulated peer review, Phase 2.7"
and dated by commit d18acd3 to 2026-09-21. It is what the paper calls "an
external read" (`main.tex:745`), per `PASSLOG.md:2184`.

**The window 8869b82 (01:32:56) to 5e13e38 (10:46:50).** Commits, from
`git log 8869b82^..5e13e38` and the reflog, which agree:

| hash | time | subject |
|---|---|---|
| 8869b82 | 01:32:56 | freeze the pre-registration, before any accuracy exists |
| a41a67a | 10:27:06 | fold two reviewer rules into the frozen pre-registration |
| 5e13e38 | 10:46:50 | calibration frozen, before any evaluation number |

There are no other commits on any ref, and the reflog has no reset, rebase or
amend in the window.

**Evidence of script runs.**

- **Working tree, 01:33:00 to 10:27:06.** No file in the repository, ignored
  files included and `.git` excluded, has an mtime in this interval
  (`find -newermt`).
- **Git object store.** No loose object was written in the interval. The first
  objects after the freeze are a41a67a's own three blobs, two trees and the
  commit, all at 10:27:06.5 to 10:27:06.8. Nothing was staged and abandoned.
- **Temp folder.** Nothing under `AppData/Local/Temp` (depth 4) has an mtime in
  the interval.
- **First activity after a41a67a,** in this order:
  - `phase2b_core.py` written 10:32:23;
  - `__pycache__/phase2b_core.cpython-314.pyc` at 10:33:08, the first import of
    the pipeline after the freeze;
  - `phase2b_build.py` at 10:39:50;
  - `data/phase2b_blocks.parquet` at 10:42:04, the calibration build;
  - `phase2b_constants.py` and `reports/phase2b_calibration.md` at 10:46:18;
  - commit 5e13e38 at 10:46:50;
  - `data/phase2b_eval_sigs.parquet` at 10:59:38, the first evaluation-split
    cache.
- **Before the freeze.** The 8869b82 PASSLOG entry says "This pass deliberately
  computed nothing" (`PASSLOG.md:740`). The only numbers in existence were the
  2.1 gate's axis statistics, which are design context and not calibration or
  evaluation numbers.

**Answer: no calibration or evaluation number was computed before a41a67a,** on
every trace available. The limit of the evidence is that an mtime records the
last write only. A file written in the window and overwritten later would not
show. But all of the calibration outputs, their generating code and the git
object store first appear after 10:27:06.

**Bearing on the paper.** `a41a67a` appears nowhere in `main.tex` (`grep -c`
returns 0). The footnote at main.tex:770-774 lists 8869b82, 5e13e38, 3d86959,
c20239a, 5f452ad, 3e79a48 and 9e3d921. Section 6.4 says the repository holds
"two dated appends" (main.tex:749).

---

## A2. Section 8.3 against the Experiment 1 paper

The Experiment 1 paper is `manuscript/main.tex`.

- **Title:** "Historical Consistency Predicts Mechanism Accuracy, Not Mechanism
  Ranking: Evidence from a Controlled Synthetic Study" (`manuscript/main.tex:21-22`).
- **Author affiliation:** "Independent Researcher" (`manuscript/main.tex:24`).
  This paper gives "Department of Information Technology, A. D. Patel
  Institute of Technology (ADIT), Charutar Vidya Mandal (CVM) University"
  (`phase2/paper/main.tex:34-36`).
- **Committed outputs:** `data/outputs/experiments/exp1/final/`, frozen at
  6fb6188 (2026-08-12 10:39:48).

| # | claim (phase2 main.tex:1449-1494) | evidence | holds? |
|---|---|---|---|
| a | pre-registered | It calls itself so (`manuscript/main.tex:35, 141, 640-665`). The design, falsification criteria and calibration were committed at **3c6b581** (2026-08-11 23:39:30), with `research/EXPERIMENT_1_REDESIGN_REVIEW.md` §18 "Falsification criteria" and `research/experimental_hypotheses.md` in that tree. The frozen run is 6fb6188 (2026-08-12 10:39:48); its result CSVs have mtime 10:12 that morning. The local reflog of `origin/main` shows **3c6b581 pushed 2026-08-11 23:40:13 and 6fb6188 pushed 2026-08-12 10:40:35**. There is no external registry. | **holds**, in the in-repo sense: committed, and pushed, before the run. This is a better third-party trail than Phase 2 has, if GitHub's own records confirm the pushes. I checked only the local reflog. |
| b | 240 conditions, six consistency targets, two lexical conditions | "20 seeds × 6 nominal-consistency targets × 2 lexical conditions" (`:35-36, 501, 713`). `final_frozen_config.json`: TARGETS has six values, LEXICAL_CONDITIONS two, TOTAL_CONDITIONS 240. `final_condition_results.csv` has 240 rows, all `ok`. | **holds**. Exp1 calls them "nominal-consistency targets". |
| c | Pearson above 0.9 in both lexical conditions, for each mechanism's own accuracy | Rules 0.909 (VARIED) and 0.959 (CLEAN); retrieval 0.948 and 0.955 (`:737-740, 835-836`). Recomputed from `final_condition_results.csv` with `realized_det_pct`: 0.9091 / 0.9592 and 0.9476 / 0.9549. | **holds** |
| d | the winner was a constant function of the lexical condition | VARIED: retrieval in 120 of 120. CLEAN: tie in 120 of 120 (`:755-767`; `final_summary.csv`, n_rules_wins = 0 in every row). | **holds** |
| e | a frozen threshold rule agreed with the winner in 100% in one band and 0% in another | 32 of 32 in the realized 0.70-0.90 band, 0 of 18 in the realized ≥0.90 band (`:785-786`). The by-nominal-target split is 30/30 and 2/20. | **holds**, on the per-row realized-ADS banding. Exp1 also reports the by-target split, which is 100% against 10%, not 0%. |
| f | retrieval took the single best lexical match over the same records the rules arm matched | `scripts/experiments/exp1/mechanisms.py:41-65`: `process.extract(..., scorer=fuzz.WRatio, limit=3, score_cutoff=75)` over `kb.company_products[cui]`, then over `list(kb.glob)`, taking `matches[0]` (`scripts/phase2/p2lib/retrieval.py:11-22`). Rules use `kb.company_lookup` and `kb.global_lookup` over the same KB (`mechanisms.py:26-38`). | **holds**. Detail: rapidfuzz 3.14.5 (installed 2026-05-18, before Exp1 ran) defaults to `processor=None`, and WRatio caps its token and partial components at 95 and 90. So **WRatio reaches 100 only on identical strings**, and the "tie-breaking among equal-scoring records" route the paper names (l.1464-1465) is not operative at the maximum. As an upper bound ("only through") the sentence still holds. |
| g | a two-stage company-then-global fallback shared by both arms | Rules: company exact, then global exact (`mechanisms.py:32-38`; `manuscript/main.tex:420-421`). Retrieval: company fuzzy, then global fuzzy (`mechanisms.py:48-65`; `:436-437`). They stop at different stages when the item's string is absent from the company's history: retrieval can accept a different company product scoring ≥75 where the rules arm goes to the global exact record. | **holds** |
| h | retrieval won every defined comparison and the rules arm none | 120 retrieval wins, 0 rules wins, 120 ties (`final_summary.csv`). | **holds**. Terminology: Exp1 uses "defined comparisons" for the 50 conditions where both the threshold rule's recommendation and the winner are defined (32 + 18, `:797`). Every one of those is also a retrieval win. |
| i | the clean-lexical condition contributed zero defined comparisons | `:539-540` ("zero of the 120 CLEAN conditions produce a defined empirical winner"), `:806-807`, `:890-891`. | **holds** |
| j | "demonstrated equivalent there at that study's own margin" | Exp1's winner rule has three outcomes, and "tie" means "otherwise" (`:598-601, 606-613`). It has no "undecided", so a tie there does **not** demonstrate equivalence. This paper's own vocabulary separates the two: "demonstrated equivalent within the margin, or the evidence does not settle it ... we never merge them" (phase2 `main.tex:383-385`). Recomputed against that standard from `final_condition_results.csv`: 115 of the 120 CLEAN intervals lie inside [−0.02, +0.02]. **Five cross +0.02 on the rules side**: seeds 31001, 31016, 31009, 31014 and 31005, with ci_high 0.0211, 0.0233, 0.0204, 0.0224 and 0.0203. Under this paper's rule they are `undecided`. Also, 70 of 120 CLEAN intervals have a lower bound above zero. | **does not hold as written, and is not consistent with (i).** "Zero defined comparisons" does not imply equivalence. The narrowest correct version: "the clean condition contributed zero defined comparisons; in 115 of its 120 conditions the interval lay inside that study's two-point margin, and in the other five it crossed the margin on the rules side." |
| k | a gap of about half an accuracy point in the clean condition against a two-point margin | CLEAN gaps by band: +0.0048, +0.0055, +0.0063 (`:867-872`); δ = 0.02 (`:538, 602, 710`). By target, the gap is 0.0046 to 0.0066 (`final_summary.csv`). | **holds**. The sign favours the rules arm. |
| l | the rules arm's disadvantage widened as consistency rose | VARIED gap −0.1374, −0.1678, −0.1851 across the realized bands <0.70, 0.70-0.90 and ≥0.90 (`:845-848, 867-872`). | **holds**, for VARIED. Under CLEAN the gap is flat and slightly positive. |

The recomputations in (c) and (j) were one-off commands over the committed Exp1
CSV, not committed code. I kept them out of `phase2_9a_matched.py` because no
Phase 2 script reads outside `phase2/`, and I did not want to start now.
**Invariant 5:** if 2.9b wants the 115/120 count in the paper, it needs a
committed script first. The command, run from the repo root:

```
python -c "import pandas as pd; d=pd.read_csv('data/outputs/experiments/exp1/final/final_condition_results.csv'); c=d[~d.lexical_variation]; print(((c.paired_diff_ci_low>=-0.02)&(c.paired_diff_ci_high<=0.02)).sum(), len(c))"
```

---

## A3. The second structural region (section 4.3)

**What the paper says.**

- main.tex:475-478: "**Where the history is written one way, no mechanism can
  win.** If the block's training records carry a single distinct surface form,
  every mechanism sees the same form and the same evidence attached to it, and
  all of them return the same author. The comparison is a tie by construction."
- The general-form preamble (main.tex:464-467) covers "*any* pair of mechanisms
  that assigns an author drawn from the block's own history, whatever the
  machinery inside them".
- main.tex:136-137: "no mechanism can win where the history is written one
  way".
- The conclusion is already narrower (main.tex:1569-1572): "a precision-first
  rule cannot win a block whose history names one author or is written one
  way".

**Counts.** These come from B2, evaluation split, primary population. SV = 0 is
exactly the set of blocks whose training half carries one distinct form; this
is checked block by block in the script.

| band | test sigs | rule right, vote wrong | vote right, rule wrong | of which rule abstained | test form absent from training half |
|---|---:|---:|---:|---:|---:|
| SV = 0 | 17,960 | **0** | **696** | 696 | 835 |
| SV low | 56,408 | 225 | 1,036 | 1,010 | 1,229 |
| SV mid | 59,433 | 391 | 1,074 | 1,061 | 1,321 |
| SV high | 63,678 | 2,409 | 1,206 | 1,150 | 2,824 |
| ADS [0,0.5) | 47,167 | 1,823 | 247 | 205 | 1,632 |
| ADS [0.5,0.7) | 16,079 | 629 | 284 | 252 | 687 |
| ADS [0.7,0.9) | 12,660 | 414 | 258 | 249 | 473 |
| ADS [0.9,1.0) | 12,683 | 159 | 194 | 182 | 238 |
| ADS = 1.0 | 108,890 | **0** | **3,029** | 3,029 | 3,179 |
| ADS = 1.0 × SV = 0 | 12,772 | 0 | 666 | 666 | 738 |

No committed table carried these as aggregates. They are derivable from the
committed per-block `phase2e_blocks_scored.csv.gz` (`n_plus_`, `n_minus_`,
`n_test` − `rule_fires_n`), and `phase2_9a_region_counts.csv` now prints them.
The script also checks them against the per-signature scores.

**My view: the general form does not hold as written for the second region.**

Where the training half carries one form F, the rule fires only on test
signatures whose form is F. On those it returns the block's top author. The
k-nearest vote pools the whole training half, because there is one form,
and returns the same author under the shared tie-break. So the two never
disagree where the rule fires, which is the 0 in the table.

But 835 of the band's 17,960 test signatures carry a form the history has
never seen. The rule abstains on them and the vote still answers, correctly on
696. Those 696 are the whole SV = 0 pooled gap: −696 / 17,960 = −0.0388, which
is `phase2e_pooled_sv.csv`'s −0.038753. That gap is why Table 4 shows `k-NN wins`
in the SV = 0 band at delta 0.03 and 0.02. The region is one where the rule
cannot win, not one where no mechanism can win. It is structurally the same
as the one-author region, whose ADS = 1.0 row shows the same pattern: 0
against 3,029, all abstentions.

A second, separate problem is "whatever the machinery". The first region holds
for any machinery, because a history with one author can only return that
author. The second needs both mechanisms to take their evidence from the
surface form alone. A mechanism that also reads co-authors, venue or
affiliation can separate two authors who share one written form, so "sees the
same form and the same evidence" fails for it. It also needs both to resolve
that evidence with the same author tie-break. The frozen pair meets both
conditions; the general claim does not.

**Narrowest correct version.** For two mechanisms that take their evidence
only from the block's training surface forms and resolve it with the same
author tie-break: where the training history carries one distinct form, they
return the same author on every test signature both answer. If both always
answer, the comparison there is a tie by construction. If one can abstain, as
the precision-first rule does, that one cannot win there and can lose only on
test forms absent from the history.

On this data that is 835 of 17,960 signatures, 4.6%. The vote is right on 696
of them.

---

## A4. Similarity functions and the containment argument

**Exact functions.**

| where | function | normalisation before scoring |
|---|---|---|
| retired retriever (2.2b) | `phase2b_core.py:65-68` `METRICS = {"levenshtein": Levenshtein.normalized_similarity, "jarowinkler": JaroWinkler.normalized_similarity}` (rapidfuzz.distance), scored by `rf_process.cdist(distinct_test, ordered, scorer=simfunc, dtype=np.float32)` at `phase2b_core.py:216`. The single nearest form is `argmax` at `:217`; the frozen form tie-break is the ordering at `:213` (more training signatures first, then lexicographic). | none at scoring: `cdist` is called without `processor` |
| k-nearest vote (2.2e) | `phase2e_mech.py:51-54` `ARMS`, the same two functions. `rf_process.cdist(distinct, forms, scorer=simfunc, dtype=np.float32)` at `phase2e_mech.py:88`, and a stable `argsort(-sims)` at `:96` with the same form order (`:78`) | none at scoring |

- **rapidfuzz version and defaults.** rapidfuzz 3.14.5. The `processor` default
  is `None` for `process.cdist`, `Levenshtein.normalized_similarity` and
  `JaroWinkler.normalized_similarity` (checked with `inspect.signature`).
  Jaro-Winkler `prefix_weight` is 0.1.
- **What the scorer sees.** It sees the frozen `surface_form` string
  unchanged. That string was built once at ingest by
  `s2and_blocking.surface_form` (`s2and_blocking.py:83-86`): the four name parts
  stripped, joined by single spaces, whitespace runs collapsed. Case,
  punctuation and diacritics are kept (`s2and_blocking.py:33-36`, and the
  asserts at `:145-147`). Ingest asserts no empty form survives
  (`ingest_s2and.py:240`).
- **The only many-to-one step** is that joining. Raw part splits that join to
  the same string (for example first "Jean-Paul" with no middle name, against
  first "Jean" and middle "-Paul", if both ever occur) become one frozen form.
  That defines the representation; it is not a step between the frozen forms
  and the scorer. No normalisation is applied between the two that could map
  distinct frozen forms together.

**Can two distinct frozen forms score the maximum?**

- **Analytically, no.**
  - `Levenshtein.normalized_similarity` is 1 − d / max(len) and equals 1 only
    at d = 0, which means identical strings.
  - Jaro equals 1 only when every character matches with no transpositions and
    the lengths are equal, which means identical. Jaro-Winkler, J + l·p·(1 − J)
    with l·p ≤ 0.4, equals 1 only when J = 1.
  - In float32, a distinct pair could round to 1.0 only if 1 − s < 2⁻²⁵ (about
    3·10⁻⁸). That needs strings of millions of characters.
- **Empirically, no.** 0 of 210,537 distinct-form pairs inside primary blocks
  score 1.0 under either arm, computed exactly as the mechanisms compute it
  (B4, committed code). This agrees with the 2.2b measurement of 0 rule wins in
  both arms.

**My view on the 4.1 wording: valid for these two functions, too broad as
stated.**

The argument needs more than "maximized by identity" (main.tex:420-421), which
is necessary but not sufficient. It needs **the maximum to be attained only at
identity**: s(x, y) < s(x, x) for every training form y ≠ x, evaluated after any
preprocessing the scorer applies and at the precision at which scores are
compared.

If a distinct form can tie the test form at the maximum, the retriever's tie-break
decides between them. Here that tie-break is more training signatures first,
then lexicographic, so it can pick the other form and a different author. The
rule could then be right where the retriever is wrong.

Functions that are commonly called "normalized string similarity" fail the
condition. Checked in rapidfuzz 3.14.5:

- `fuzz.token_sort_ratio("wei wang", "wang wei") = 100` (word reorder);
- `fuzz.token_set_ratio` gives 100 on the same pair;
- `fuzz.partial_ratio("smith", "j smith") = 100` (containment);
- `Levenshtein.normalized_similarity("Smith", "smith", processor=utils.default_process) = 1.0`
  (case folding).

For author names, word reorder and initial-plus-surname containment are exactly
the variation that occurs.

The condition the wording needs: **the similarity separates distinct forms at its
maximum**, meaning the induced distance is zero only for identical strings, as
for the edit and Jaro family scored without a folding processor. Failing that,
the tie-break among forms at the maximum must put the identical form first. The
rapidfuzz.distance metrics Indel, OSA, Damerau-Levenshtein, LCSseq, Prefix,
Postfix and Jaro all satisfy the first condition on the pairs above.

**Wording that overreaches.**

- main.tex:50-51 and 130: "the maximum of any similarity function".
- main.tex:420-421: "every function in the normalized string similarity family
  is maximized by identity".
- main.tex:509-510: "the containment holds for all of them".
- main.tex:722: "the maximum of any similarity function". **This is inside the
  locked 6.4 quote (lines 711-742).** It cannot be edited, so any qualification
  goes in the disclosure text after the quote, as the two existing corrections
  do.

---

## A5. Traces, the contested share, the substrate history, citations

**Sources.**

| paper value | source | value |
|---|---|---|
| SV vs INIT Spearman 0.36 (main.tex:1555) | `reports/tables/phase2e_signal_correlations.csv`, row `sv`, column `init`, written by `phase2e_run.py:1130-1136` (`corr(method="spearman")` over the primary population, 13,902 blocks; 9e3d921). The identical value appears in `phase2b_signal_correlations.csv`. | 0.36271587527378707 |
| −0.818, ADS vs homonymity (main.tex:651-653) | `reports/gate21_two_axes.md:122`, Spearman column (header at `:120`), n = 18,984 live blocks | −0.8180 |
| +0.743, SV vs synonymity | `gate21_two_axes.md:123` | +0.7427 |
| +0.18, cross term ADS vs synonymity | `gate21_two_axes.md:124` | +0.1797 |
| +0.06, cross term SV vs homonymity | `gate21_two_axes.md:125` | +0.0554 |

The −0.818 to +0.06 values are on all 18,984 live blocks from gate 2.1
(commit 4399fe1), not on the 13,902-block primary population. Homonymity and
synonymity are recomputed from S2AND's reference implementation
(`gate21_two_axes.md:118`).

**The contested share.** No committed table **states** an evaluation-split
share. It was derivable by summing the 12 cells with ads_band ≠ "1.0" and
sv_band ≠ "SV=0" in `phase2e_pooled_cells_sv.csv` (9e3d921), which gives
83,401 of 197,479. `phase2_9a_contested_share.csv` now states it, with that sum
as an asserted cross-check: **0.4223 (42.2%), 2,770 of 13,902 blocks**. The
paper's 41% (main.tex:486-488, 1505) is calibration-only, 14,680 / 35,732 =
0.4108, from `phase2c_pair_regimes.csv` (c20239a). This closes flag F2's
factual half.

**The WDC LSPC 2017 gates.**

- **Gate 1** (`reports/gate1_data_shape.md`, f34f4aa) ingested 15,179 offers
  in 2,485 product clusters from the LSPC 2017 v2.0 category slices
  (`data/MANIFEST.json`, via the Hugging Face mirror `wdc/products-2017`).
- **Gate 2** (`reports/gate2_ads_range.md`, 932a484) found:
  - **Framing A** (key = cluster, label = category): ADS is a point mass at
    1.0. 0 of 2,485 clusters carry more than one category, because WDC stamps
    the category per cluster.
  - **Framing B** (key = normalised title, label = cluster): ADS is
    near-degenerate. Raw keys: 99.65% at ADS = 1.0, and 95.0% of recurring
    keys. Aggressive normalisation: 90.7% of recurring keys at 1.0, and only
    53.9% of offers sit under a recurring key.
- **Gate 2b** (`reports/gate2b_access_recon.md`, e822dea) stopped at step 0.
  No public WDC source carries per-shop categories. The gold standard's labels
  are assigned per cluster by its own documented procedure, and the WDC data
  hosts refused connections.

**Is this the basis of main.tex:112-115?** It is the only committed evidence
for it, and it covers **one** benchmark. The paper says "Clean product-matching
and record-linkage benchmarks mostly have only the second ... the consistency
axis is a point mass", uncited. The repository measured that for WDC LSPC 2017
alone, where it is exact under one framing and near-exact under the other. No
other product-matching or record-linkage benchmark was examined.
"Mostly" is an unmeasured generalisation from one case.

**Crossref.** These are GETs against `api.crossref.org` on 2026-11-12, all
HTTP 200. The raw JSON is in the session scratchpad and is not committed.
Drafted BibTeX follows, from the Crossref record and nothing else.

```bibtex
@inproceedings{primpeli2019wdc,
  author    = {Primpeli, Anna and Peeters, Ralph and Bizer, Christian},
  title     = {The {WDC} Training Dataset and Gold Standard for Large-Scale Product Matching},
  booktitle = {Companion Proceedings of The 2019 World Wide Web Conference},
  series    = {WWW '19},
  publisher = {ACM},
  year      = {2019},
  pages     = {381--386},
  doi       = {10.1145/3308560.3316609}
}

@inproceedings{sinha2015mas,
  author    = {Sinha, Arnab and Shen, Zhihong and Song, Yang and Ma, Hao and Eide, Darrin and Hsu, Bo-June (Paul) and Wang, Kuansan},
  title     = {An Overview of {Microsoft Academic Service} ({MAS}) and Applications},
  booktitle = {Proceedings of the 24th International Conference on World Wide Web},
  series    = {WWW '15},
  publisher = {ACM},
  year      = {2015},
  pages     = {243--246},
  doi       = {10.1145/2740908.2742839}
}
```

**Notes on the two new entries.**

- Primpeli: Crossref's container title is "Companion Proceedings of The 2019
  World Wide Web Conference", the event is "WWW '19: The Web Conference", and
  it was issued 2019-05-13. It matches `data/MANIFEST.json`'s citation
  ("WWW '19 Companion, 381-386").
- Sinha: the brief calls it "WWW '15 Companion". **Crossref's container title is
  "Proceedings of the 24th International Conference on World Wide Web"**, with
  no "Companion", and it was issued 2015-05-18. The DOI prefix 10.1145/2740908
  is the one ACM used for the WWW '15 Companion volume, but I did not verify
  that from a primary source in this pass. The entry above uses Crossref's
  string. Pick the venue string at 2.9b with that in mind.
- Bo-June (Paul) Hsu's given name is as Crossref gives it.

**Volume and pages for the existing keys** (`references.bib` has neither for
any of the three):

| key | DOI | Crossref | fields to add |
|---|---|---|---|
| hendrickx2024 | 10.1007/s10994-024-06534-x | *Machine Learning*, volume 113, issue 5, pages 3073-3110; online 2024-03-29, print 2024-05 | `volume = {113}, number = {5}, pages = {3073--3110}` |
| s2and2021 | 10.1109/JCDL52503.2021.00029 | 2021 ACM/IEEE JCDL, Champaign, IL; pages 170-179; issued 2021-09; IEEE | `pages = {170--179}` (proceedings, no volume) |
| backes2018 | 10.1145/3269206.3271699 | Proceedings of the 27th ACM CIKM, Torino; pages 803-812; issued 2018-10-17; ACM | `pages = {803--812}` (proceedings, no volume) |

Titles and authors on all three match the bib, apart from case.

---

## A7. Quotes

**Peer-review minor 10** (`reports/phase2_7_peer_review.md:540-544`):

> 10. **Section 2.3 is out of proportion.** Roughly 570 words on one prior paper
>     inside a 774-word related-work section, while the rest of the AND literature
>     gets two sentences. The Kim and Kim comparison is genuinely the closest prior
>     work and the analysis of it is good; it should be a subsection of a fuller
>     related-work section rather than most of one.

**Peer-review minor 20** (`reports/phase2_7_peer_review.md:588-592`):

> 20. **The subtitle promises a study of mechanism selection and no selector is
>     built.** Section 5.7 justifies this well and the logic is sound. But a
>     reader meets the title first, and "a pre-registered study of design-time
>     mechanism selection" sets up an expectation that section 5.7 then has to
>     talk them out of. Consider naming the negative result in the subtitle.

**Flags F1 to F5** (`reports/phase2_8a_moderation_audit.md:95-124`):

> - **F1. Section 5.2 overstates the calibration trap for the k-nearest family.**
>   It says the accuracy-maximizing protocol, applied to either parameterized
>   pair, "selects the degenerate parameter and walks the design straight back
>   into a comparison that cannot have a winner". That is exact for the radius
>   vote, whose accuracy peaks at r = 0.95 with a rule-side count of 0. On the
>   k grid the protocol selects k = 2, which is still two-sided: 181 against 736
>   on the calibration split and 987 against 3,990 on evaluation (Table 2). The
>   sentence is inherited from `reports/phase2c_pair_design.md` ("would select
>   k = 2 or r = 0.95 and walk the design straight back into nesting"). The
>   accurate statement is that the protocol moves the parameter toward the
>   nested limit in both families, which is how the new contributions item and
>   section 8.2 already put it. Correcting 5.2 narrows an existing claim, so it
>   is the author's call.
> - **F2. The 41% contested-region figure is a calibration-split number.** It is
>   quoted in sections 4.3 and 8.4. The evaluation-split equivalent is
>   computable from committed records and is what a reader will assume they are
>   given (peer-review major 4, closing note). New analysis.
> - **F3. The entity resolution width of contribution 1 rests on argument.** Running
>   the one-count nesting check on one public non-author-name matching benchmark
>   would turn it into a demonstration (peer-review major 4, option 2). New
>   experiment, and the paper's own scope paragraph already states the width as
>   an argument.
> - **F4. The calibration trap is absent from the abstract.** Adding it is about
>   fourteen words and takes the abstract to about 263, over the venue band. For
>   the venue-specific trim.
> - **F5, an option rather than a gap.** Sections 4.1 and 4.3 could be set as a
>   stated proposition with a proof. Some cs moderators and reviewers read that
>   as the signal of a result. It is a restructuring of section 4 and it moves
>   the register away from the author's "practical rather than deep", so it is
>   listed and not done.

---

## Reproducing

```
python phase2/phase2_9a_matched.py
```

Use CPython 3.14 with the package versions above. The script runs its own
assert-based self-check, re-derives the frozen population and halts on any
mismatch, then checks six per-block counts against the committed record. It
writes the three `reports/tables/phase2_9a_*.csv` files and prints B4. The run
takes about 47 s with `data/phase2e_eval_sigs.parquet` present. Without it,
`phase2e_run.mechanism_pass` rebuilds the cache first, which takes about 20 min.

## Appendix: `pip freeze`, CPython 3.14.2, 2026-11-12

<details><summary>270 packages</summary>

```
aiohappyeyeballs==2.7.1
aiohttp==3.14.3
aiosignal==1.4.0
altair==6.2.2
annotated-doc==0.0.4
annotated-types==0.7.0
anthropic==0.120.2
anyio==4.12.1
asttokens==3.0.1
attrs==26.1.0
audioop-lts==0.2.2
azure-ai-documentintelligence==1.0.2
azure-core==1.41.0
azure-identity==1.25.3
beautifulsoup4==4.14.3
blinker==1.9.0
boto3==1.43.50
botocore==1.43.50
brotli==1.2.0
certifi==2026.1.4
cffi==2.0.0
charset-normalizer==3.4.4
click==8.4.1
cobble==0.1.4
colorama==0.4.6
comm==0.2.3
contourpy==1.3.3
coverage==7.15.3
cryptography==48.0.0
cycler==0.12.1
datasketch==1.10.0
ddgs==9.14.4
debugpy==1.8.19
decorator==5.2.1
defusedxml==0.7.1
distro==1.9.0
docstring_parser==0.18.0
et_xmlfile==2.0.0
executing==2.2.1
faiss-cpu==1.14.3
fake-useragent==2.2.0
fastapi==0.128.0
filelock==3.29.0
filetype==1.2.0
fonttools==4.63.0
formulaic==1.2.2
fpdf2==2.8.7
frozenlist==1.8.0
fsspec==2026.4.0
git-filter-repo==2.47.0
gitdb==4.0.12
GitPython==3.1.57
google-auth==2.56.2
google-genai==2.16.0
graphifyy==0.8.11
greenlet==3.5.4
groq==0.37.1
h11==0.16.0
h2==4.4.1
hf-xet==1.5.1
hpack==4.2.0
httpcore==1.0.9
httptools==0.8.0
httpx==0.28.1
httpx-sse==0.4.3
huggingface_hub==1.19.0
hyperframe==6.1.0
idna==3.11
iniconfig==2.3.0
interface_meta==2.0.1
ipykernel==7.1.0
ipython==9.9.0
ipython_pygments_lexers==1.1.1
ipywidgets==8.1.8
isodate==0.7.2
itsdangerous==2.2.0
jedi==0.19.2
Jinja2==3.1.6
jiter==0.15.0
jmespath==1.1.0
joblib==1.5.3
jsonpatch==1.33
jsonpointer==3.1.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
jupyter_client==8.7.0
jupyter_core==5.9.1
jupyterlab_widgets==3.0.16
kiwisolver==1.5.1
langchain-anthropic==1.5.3
langchain-classic==1.0.8
langchain-community==0.4.2
langchain-core==1.5.3
langchain-google-genai==4.3.2
langchain-groq==1.1.3
langchain-openai==1.4.1
langchain-protocol==0.0.18
langchain-text-splitters==1.1.2
langgraph==1.2.10
langgraph-checkpoint==4.1.1
langgraph-prebuilt==1.1.0
langgraph-sdk==0.4.2
langsmith==0.10.15
loguru==0.7.3
lxml==6.1.1
mammoth==1.12.0
markdown-it-py==4.2.0
markdownify==1.2.2
markitdown==0.0.2
MarkupSafe==3.0.3
matplotlib==3.11.1
matplotlib-inline==0.2.1
mdurl==0.1.2
MouseInfo==0.1.3
mpmath==1.3.0
msal==1.37.0
msal-extensions==1.3.1
multidict==6.7.1
narwhals==2.24.0
nest-asyncio==1.6.0
networkx==3.6.1
numpy==2.4.2
olefile==0.47
openai==2.53.0
openpyxl==3.1.5
orjson==3.11.9
ormsgpack==1.12.2
outcome==1.3.0.post0
packaging==25.0
pandas==3.0.1
parso==0.8.5
pathvalidate==3.3.1
patsy==1.0.3
pdfminer.six==20260107
pillow==12.2.0
platformdirs==4.5.1
pluggy==1.6.0
primp==1.3.1
prompt_toolkit==3.0.52
propcache==0.5.2
protobuf==7.35.1
psutil==7.2.1
pure_eval==0.2.3
puremagic==2.2.0
pyarrow==24.0.0
pyasn1==0.6.4
pyasn1_modules==0.4.2
PyAutoGUI==0.9.54
pycparser==3.0
pydantic==2.12.5
pydantic-settings==2.14.2
pydantic_core==2.41.5
pydeck==0.9.3
pydub==0.25.1
PyGetWindow==0.0.9
Pygments==2.19.2
PyJWT==2.13.0
PyMsgBox==2.0.1
pymupdf==1.28.2
pyparsing==3.3.2
pypdf==6.11.0
PyPDF2==3.0.1
pyperclip==1.11.0
PyRect==0.2.0
PyScreeze==1.0.1
PySocks==1.7.1
pytest==9.1.0
pytest-cov==7.1.0
python-dateutil==2.9.0.post0
python-docx==1.2.0
python-dotenv==1.2.2
python-multipart==0.0.32
python-pptx==1.0.2
pytweening==1.2.0
PyYAML==6.0.3
pyzmq==27.1.0
RapidFuzz==3.14.5
referencing==0.37.0
regex==2026.5.9
reportlab==5.0.0
requests==2.32.5
requests-toolbelt==1.0.0
rich==15.0.0
rpds-py==2026.6.3
s3transfer==0.19.1
safetensors==0.8.0
scikit-learn==1.8.0
scikit-posthocs==0.17.0
scipy==1.17.0
seaborn==0.13.2
selenium==4.43.0
sentence-transformers==5.5.1
setuptools==70.2.0
shellingham==1.5.4
six==1.17.0
smmap==5.0.3
sniffio==1.3.1
socksio==1.0.0
sortedcontainers==2.4.0
soupsieve==2.8.4
SpeechRecognition==3.16.1
SQLAlchemy==2.0.51
stack-data==0.6.3
standard-aifc==3.13.0
standard-chunk==3.13.0
starlette==0.50.0
statsmodels==0.15.0
streamlit==1.60.0
sympy==1.14.0
tenacity==9.1.4
threadpoolctl==3.6.0
tiktoken==0.13.0
tokenizers==0.22.2
toml==0.10.2
torch==2.12.0+cpu
tornado==6.5.4
tqdm==4.67.3
traitlets==5.14.3
transformers==5.12.1
tree-sitter==0.25.2
tree-sitter-bash==0.25.1
tree-sitter-c==0.24.2
tree-sitter-c-sharp==0.23.5
tree-sitter-cpp==0.23.4
tree-sitter-elixir==0.3.5
tree-sitter-fortran==0.6.0
tree-sitter-go==0.25.0
tree-sitter-groovy==0.1.2
tree-sitter-java==0.23.5
tree-sitter-javascript==0.25.0
tree-sitter-json==0.24.8
tree-sitter-julia==0.23.1
tree-sitter-kotlin==1.1.0
tree-sitter-lua==0.5.0
tree-sitter-objc==3.0.2
tree-sitter-php==0.24.1
tree-sitter-powershell==0.26.4
tree-sitter-python==0.25.0
tree-sitter-ruby==0.23.1
tree-sitter-rust==0.24.2
tree-sitter-scala==0.26.0
tree-sitter-swift==0.7.2
tree-sitter-typescript==0.23.2
tree-sitter-verilog==1.0.3
tree-sitter-zig==1.1.2
trio==0.33.0
trio-websocket==0.12.2
typer==0.25.1
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.3
Unidecode==1.4.0
urllib3==2.6.3
uuid_utils==0.17.0
uv==0.11.7
uvicorn==0.40.0
watchdog==6.0.0
wcwidth==0.2.14
websocket-client==1.9.0
websockets==15.0.1
widgetsnbextension==4.0.15
win32_setctime==1.2.0
wrapt==2.5.0
wsproto==1.3.2
xlrd==2.0.2
xlsxwriter==3.2.9
xxhash==3.8.1
yarl==1.24.5
youtube-transcript-api==1.2.4
zstandard==0.25.0
```

</details>
