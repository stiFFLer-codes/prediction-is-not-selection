# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.1 (data foundation) complete. Hard gate PASSED.** Awaiting
  human review before Phase 2.2 starts in a fresh session.
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

## Next: Phase 2.2, the boundary finding (fresh session, after review)

Two mechanisms (exact match vs fuzzy retrieval), a paired-bootstrap winner, then
the dissociation: does consistency predict each mechanism's own accuracy but not
the winner, and does surface stability predict the winner. This is the keel. Read
the carry-forward list at the end of `reports/gate21_two_axes.md` first.

## Open decisions

- Blocking normalization and surface-form definition: **frozen and committed** in
  `phase2/s2and_blocking.py` (charter invariant 5), before any accuracy exists.
  Not to be re-tuned.
- ADS in Phase 2.1 is corpus-level. Phase 2.2 must recompute it train-only.
- The fuzzy similarity cutoff, the winner definition, the splits, and the
  practical-equivalence margin are still unfrozen. They are frozen at the start
  of 2.2, before any accuracy is measured.
- Two-mechanism core (exact vs fuzzy) confirmed. A third semantic arm stays out
  unless it is actually implemented and tested.
- Title: working candidates in PLAN.md, locked at the writing phase with CC input.

## Live risks

- **Kim and Kim 2020 (JASIST), "Effect of forename string on author name
  disambiguation."** Found in the 2.1 not-scooped check. It does not scoop the
  claim (their surface axis is a manipulation not a measurement, their unit is
  the dataset, they report no winner flip, they build no selector), but it does
  report that the gap between string matching and machine learning widens when
  homonymity is prevalent. That bears directly on H2. Read it in full before 2.2
  freezes hypotheses. Detail in `reports/gate21_access_recon.md`.
- inspire is 15,077 of 18,984 live blocks. Any pooled number is mostly an inspire
  number. Per-dataset reporting is not optional.
- S2AND's README notes some affiliation data comes from the Microsoft Academic
  Graph. The `affiliation` column is a context field and is droppable before
  public release. Flagged for the 2.6 pre-submission gate.

## Read order for a fresh session

root CLAUDE.md -> phase2/CLAUDE.md (charter) -> this file (STATE.md) ->
phase2/PLAN.md (arc) -> phase2/phase2-spec.md (method) -> phase2/PASSLOG.md
(history).
