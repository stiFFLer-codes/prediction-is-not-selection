# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.2a (pre-registration) complete. `phase2/PREREG.md` is frozen
  and committed, before any accuracy exists.** Awaiting human review before
  Phase 2.2b (the measurement) starts in a fresh session.
- Phase 2.1 (data foundation) is complete and its hard gate passed.
- Nothing has been measured since 2.1. No mechanism, no accuracy, no similarity
  cutoff, no winner, no selector exists anywhere under `phase2/`.
- Dataset: S2AND (Semantic Scholar Author Name Disambiguation, Allen Institute
  for AI). Access, license, and feasibility all verified by doing, not reading.

## Dataset decision in one paragraph

The paper needs two independent axes that both vary: label consistency and
surface-form stability. WDC, and every clean product-matching benchmark, has
only surface variation; its labels are deterministic, so the consistency axis is
a point mass and the dissociation cannot be shown. Author name disambiguation
has both axes natively and separately: homonymity (a name shared by many authors,
so low consistency) and synonymity (one author written many ways, so low surface
stability). S2AND unifies eight disambiguation datasets in one format, measures
both axes, is public and offline-reproducible, and gives cross-dataset
generalization for free. As of Phase 2.1 this is no longer a bet: both axes were
measured on the real data and both are alive.

## Done so far

- Pass 0: environment cleaned. Phase 1 root CLAUDE.md and STATE.md archived under
  phase1-archive/; a minimal root CLAUDE.md now points at the phase-2 charter.
- Pass 1 (gate 1): scaffolded and ingested a WDC subset. Dataset later dropped.
- Pass 2 (gate 2): ADS-range check on WDC. Both specified framings dead (category
  is cluster-constant; full-title key is near-unique). Hard gate failed.
- Pass 3 (gate 2b): WDC salvage ruled out. WDC never stored the shop's own
  category; the category field is a classifier output. Path A closed on the
  schema, not the downed host.
- Dataset pivoted to S2AND, confirmed by the human.
- **Pass 4 (Phase 2.1): S2AND access recon, ingest, frozen blocking, two-axis
  check. Hard gate passed.** Both axes have real range and are separable.
- **Pass 5 (Phase 2.2a): Kim and Kim 2020 read in full and positioned; PREREG.md
  written and frozen.** No measurement.

## Phase 2.1 outcome, in numbers

- 766,133 signatures, 7 of 8 constituent datasets, 26,939 blocks, 59,119 authors.
  Medline excluded: the release ships no clusters file for it, so it carries no
  author labels. 18,984 blocks (70.5%) have 2+ signatures and define both axes.
- Consistency axis alive: ADS spike at exactly 1.0 is 75.77%, and the remaining
  4,600 blocks spread across the whole interval (1,385 / 1,566 / 983 / 666 in
  [0,0.5) / [0.5,0.7) / [0.7,0.9) / [0.9,1.0)), min 0.0377. Unchanged when
  recomputed on S2AND's own shipped block field (spike 75.71%).
- Surface axis alive, compressed by construction: 34.4% at exactly 0, median
  0.0752, p90 0.2637, max 1.0. Shape is a spike at 0 plus a broad decaying body.
- Separable: Pearson -0.299, Spearman -0.261, stable inside every block-size
  stratum. Thinnest median-split quadrant still holds 1,593 blocks.
- Cross-check against S2AND's own facets: ADS vs their homonymity Spearman
  -0.818; SV vs their synonymity +0.743; cross terms +0.18 and +0.06. Convergent
  high, divergent low.
- Reports: `reports/gate21_access_recon.md`, `reports/gate21_data_shape.md`,
  `reports/gate21_two_axes.md`. Figures under `reports/figs/gate21_*.png`.

## Phase 2.2a outcome, in one paragraph

Kim and Kim 2020 was read in full from the preprint at `phase2/Kim and Mim paper
for review.pdf`, verified against the arXiv record. It reports **gap compression,
not a winner reversal**: string matching never beats the machine-learning arm on
B-cubed F1 in any of their four datasets at any setting, and the only crossings
are on component metrics against their weakest classifier. Their surface axis is
manipulated, their unit is the dataset, and they build no selector.
`reports/kim2020_positioning.md` states the point-by-point differences and, more
importantly, the seven places our claim could collapse into a per-block
replication of theirs. `PREREG.md` then fixes everything in advance and writes
each of those collapse modes into the falsification table as a reportable
outcome.

## Next: Phase 2.2b, the boundary finding (fresh session, after review)

Execute `PREREG.md` exactly. Build the two mechanisms, calibrate the fuzzy cutoff
once on the calibration split and freeze it, then run the winner analysis and the
two-dimensional ADS-by-SV grid. Nothing in PREREG.md is re-decided; changes go in
as dated amendments appended to that file, before the affected numbers exist.
Read `PREREG.md` and `reports/kim2020_positioning.md` first, then the
carry-forward list at the end of `reports/gate21_two_axes.md`.

## Open decisions

Almost none remain for 2.2. What is now **frozen and committed**:

- Blocking normalization and surface-form definition, in
  `phase2/s2and_blocking.py` (Phase 2.1). Not to be re-tuned.
- Hypotheses, falsification table, splits and seeds, analysis population,
  minimum cell sizes, ADS and SV band rules, mechanism definitions and
  tie-breaking, the winner definition and the practical-equivalence margin
  (delta = 0.05), the fuzzy-cutoff calibration protocol, the two controls for
  the Kim and Kim overlap, and the per-dataset generalization rule. All in
  `phase2/PREREG.md` (Phase 2.2a).

Still open:

- The fuzzy cutoff's **value**. Its protocol is frozen; the number is produced
  once in 2.2b on the calibration split and frozen at that commit.
- SV and SV_resid band cut points. The rule is frozen; the values are computed in
  2.2b from the calibration split.
- Two-mechanism core (exact vs fuzzy) confirmed. A third semantic arm stays out
  unless it is actually implemented and tested.
- Title: working candidates in PLAN.md, locked at the writing phase with CC input.

## Live risks

- **Collapse into Kim and Kim 2020.** The 2.1 flag is now resolved into a
  specific, managed risk rather than an unread paper. The sharpest form: if our
  SV is mostly forename initialization, H3 is their manipulated variable observed
  instead of set. The pre-registered SV_resid control decides that, and the
  "gap compression only" outcome is pre-listed as H3 not supported rather than as
  a failure. Full detail in `reports/kim2020_positioning.md`.
- **Exact and fuzzy may coincide at low SV.** A block whose history has one
  surface form can make the two mechanisms the same procedure, so the low-SV half
  of H3 may be structural ties rather than exact-match wins. PREREG.md requires a
  mechanism agreement rate per SV band so this is visible, not inferred.
- inspire is 15,077 of 18,984 live blocks. Any pooled number is mostly an inspire
  number. Per-dataset reporting is not optional and PREREG.md section 11 makes it
  binding.
- The Kim and Kim preprint PDF in `phase2/` is **deliberately untracked** and
  gitignored. It is a publisher preprint and does not carry a redistribution
  licence, so it must not enter a public repo.
- S2AND's README notes some affiliation data comes from the Microsoft Academic
  Graph. The `affiliation` column is a context field and is droppable before
  public release. Flagged for the 2.6 pre-submission gate.

## Read order for a fresh session

root CLAUDE.md -> phase2/CLAUDE.md (charter) -> this file (STATE.md) ->
phase2/PLAN.md (arc) -> phase2/phase2-spec.md (method) -> phase2/PREREG.md
(binding for 2.2, supersedes spec section 8) -> phase2/PASSLOG.md (history).
