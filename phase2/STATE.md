# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.2b (the boundary experiment) complete. The pre-registration
  was executed exactly as frozen and the numbers exist.** Awaiting human review.
- **Phase 2.3 is blocked and must not start.** 2.2b found that the two
  mechanisms as `PREREG.md` section 4 defines them are nested: exact match is a
  strict sub-case of fuzzy retrieval. A selector choosing between a mechanism
  and a superset of itself has nothing to choose, so the 2.3 question cannot be
  asked of this pair. Review has to pick a path first; three are set out at the
  end of the Pass 6 PASSLOG entry.
- Phase 2.1 (data foundation) complete, hard gate passed. Phase 2.2a
  (pre-registration) complete and frozen. Nothing in PREREG.md has been amended.

## The 2.2b result in one paragraph

Exact match fires only when the test surface form already occurs among the
train forms. When it does, that form sits at similarity exactly 1.0, the
maximum, so the fuzzy arm retrieves the same form at any cutoff at or below 1.0
and resolves the author with the same frozen tie-break. Across all 16,136
evaluation blocks and 199,713 test signatures there are **zero** signatures on
which exact is right and fuzzy is wrong, in either metric arm. `exact wins` is
therefore an unreachable verdict, no winner reversal is possible for any signal
at any margin, the pooled gap is just minus the share of signatures where exact
abstains and fuzzy is correct, and the pre-registered mechanism agreement
diagnostic collapses to the identity exact coverage plus fuzzy abstention rate.
This was measured, not deduced, and it is reported rather than repaired,
because repairing it means amending a frozen definition after the numbers it
governs already exist.

## Phase 2.2b outcome, in numbers

Frozen inputs, committed in `5e13e38` before the evaluation split was read:
fuzzy cutoff 0.50 for both metric families (the lower boundary of the
pre-registered grid; both accuracy-versus-cutoff curves fall monotonically,
because with abstention scored as wrong the fuzzy arm is never helped by
abstaining), SV band edges 0.102644 / 0.195066, SV_resid 0.036782 / 0.082418.

- Population: 18,984 live blocks, 2,848 calibration and 16,136 evaluation.
  Primary analysis population 13,902 blocks and 197,479 test signatures. Named
  exclusions, counted and reported: 7,955 singleton blocks (1.04% of signatures)
  and 2,234 block-size-2 blocks (0.58%).
- Pooled held-out accuracy: exact 0.8244, fuzzy 0.8441, gap -0.0196. Coverage
  0.9686 and 0.9988. Agreement 0.9698.
- **H1 Supported.** Spearman of train-only ADS with held-out accuracy 0.5069
  [0.4916, 0.5224] exact and 0.7436 [0.7305, 0.7568] fuzzy, positive pooled
  non-inspire and in all four qualifying non-inspire datasets, so it
  generalizes. It is a construct-validity check, not a contribution.
- **H2 Inconclusive.** At delta = 0.05 no ADS band and no SV band has a decided
  pooled verdict, so the power floor bites first under the Order of evaluation
  rule. The reviewer rule added at the 2.2a freeze is what prevents an all-tie
  band set reading as support.
- **H3 Inconclusive at delta = 0.05, Partial at 0.02, so margin-dependent.**
- Per-block verdicts at delta 0.05: 0 exact wins, 302 fuzzy wins, 11,117 tie,
  2,483 undecided. Every ADS band, every SV band and 19 of 20 grid cells are a
  demonstrated tie.
- Substance beside the verdict: the pattern is gap compression. At fixed ADS the
  pooled gap grows with SV monotonically in four of the five ADS bands and never
  changes sign. The frozen rules make that reading available only above the
  power floor, so it is reported next to the verdict, not instead of it.
- Regression of the per-block gap: ADS -0.0495 (se 0.0043), SV -0.1443 (se
  0.0172), log test-set size +0.0308 (se 0.0015).
- Signal correlations on the primary population: SV to SV_resid 0.51, SV to
  INIT 0.36, ADS to SV -0.27. SV is correlated with forename initialization but
  is not reducible to it.
- Jaro-Winkler arm reproduces the same picture: pooled gaps -0.0379, -0.0177,
  -0.0181, -0.0192 across SV bands, all ties at delta 0.05.
- Reports: `reports/phase2b_boundary.md`, `reports/phase2b_calibration.md`.
  Tables `reports/tables/phase2b_*.csv`. Figures `reports/figs/phase2b_*.png`.

## Phase 2.1 outcome, in numbers

- 766,133 signatures, 7 of 8 constituent datasets, 26,939 blocks, 59,119 authors.
  Medline excluded: the release ships no clusters file for it. 18,984 blocks
  (70.5%) have 2+ signatures and define both axes.
- Consistency axis alive: ADS spike at exactly 1.0 is 75.77%, the remaining
  4,600 blocks spread across the whole interval, min 0.0377.
- Surface axis alive, compressed by construction: 34.4% at exactly 0, median
  0.0752, p90 0.2637.
- Separable: Pearson -0.299, Spearman -0.261, stable inside every block-size
  stratum.
- Cross-check against S2AND's own facets: ADS vs homonymity Spearman -0.818;
  SV vs synonymity +0.743; cross terms +0.18 and +0.06.
- Reports: `reports/gate21_access_recon.md`, `reports/gate21_data_shape.md`,
  `reports/gate21_two_axes.md`.

## Dataset decision in one paragraph

The paper needs two independent axes that both vary: label consistency and
surface-form stability. WDC, and every clean product-matching benchmark, has
only surface variation; its labels are deterministic, so the consistency axis is
a point mass. Author name disambiguation has both axes natively and separately:
homonymity and synonymity. S2AND unifies eight disambiguation datasets in one
format, measures both axes, is public and offline-reproducible, and gives
cross-dataset generalization for free. Both axes were measured alive at 2.1.

## Done so far

- Pass 0: environment cleaned, Phase 1 archived under `phase1-archive/`.
- Pass 1 (gate 1): WDC subset scaffolded and ingested. Dataset later dropped.
- Pass 2 (gate 2): ADS-range check on WDC. Both framings dead. Hard gate failed.
- Pass 3 (gate 2b): WDC salvage ruled out on the schema, not the downed host.
- Pass 4 (Phase 2.1): S2AND ingest, frozen blocking, two-axis check. Gate passed.
- Pass 5 (Phase 2.2a): Kim and Kim 2020 read in full and positioned; PREREG.md
  frozen. No measurement.
- **Pass 6 (Phase 2.2b): PREREG.md executed. Calibration frozen in its own
  commit first, then the evaluation split. H1 Supported, H2 and H3
  Inconclusive, and the mechanism pair found to be nested.**

## Next: review decides between three paths, then a fresh session

Do not open 2.3. The blocking issue is the nesting. Review picks one:

1. **Amend PREREG section 4** to a genuinely two-sided mechanism pair, dated and
   agreed before any new accuracy exists. Candidates: make the fuzzy arm exclude
   exact matches, or give exact an advantage fuzzy structurally lacks. Any such
   change is a new pre-registration and produces new numbers.
2. **Keep the pair and retarget the paper** on what 2.2b does establish: a
   design-time consistency signal that predicts each mechanism's accuracy and
   generalizes across datasets, and a head-to-head between a mechanism and its
   own relaxation that is a coverage question with no selection content. Smaller
   paper, different title.
3. **Replace the second mechanism** with one that is not nested. This reopens
   charter invariant 6 and is the largest scope change of the three.

The 2.2b numbers are the frozen evidence base whichever is chosen, and the
nesting is a result to report in the paper, not a mistake to erase.

## Open decisions

Frozen and committed, not to be re-decided:

- Blocking normalization and surface-form definition, `phase2/s2and_blocking.py`
  (Phase 2.1).
- Hypotheses, falsification table, splits and seeds, analysis population,
  minimum cell sizes, band rules, mechanism definitions and tie-breaking, the
  winner definition, the margins, the precedence of Inconclusive, the
  calibration protocol, the controls, the per-dataset rule: `phase2/PREREG.md`
  (Phase 2.2a).
- Fuzzy cutoff value, SV and SV_resid band edges: `phase2/phase2b_constants.py`
  (Phase 2.2b). Reproducible byte for byte from `phase2b_build.py`.

Still open:

- Which of the three paths above. This is the only live decision.
- Whether a third mechanism enters at all. Charter invariant 6 keeps it out
  unless it is actually implemented and evaluated.
- Title: working candidates in PLAN.md. Several no longer fit if path 2 is taken.

## Live risks

- **The nesting is the dominant risk and it has already fired.** It is no longer
  a risk to manage but a finding to write up and a design decision to take.
- **Collapse into Kim and Kim 2020.** Still live but now smaller: SV to SV_resid
  Spearman is 0.51 and SV to INIT 0.36, so our surface axis is not simply their
  manipulated variable observed. The SV_resid grid was run and shows the same
  shape as SV.
- **The low-SV region is structurally tied.** Confirmed, and stronger than
  expected: the whole grid is tied at the primary margin, and the agreement rate
  is an identity rather than an observation.
- inspire is 11,110 of 13,902 primary-population blocks. Per-dataset and pooled
  non-inspire reporting ran and is in the report; the H1 result does generalize.
- The Kim and Kim preprint PDF in `phase2/` is deliberately untracked and
  gitignored: publisher preprint, no redistribution licence.
- `phase2/data/phase2b_eval_sigs.parquet` is a derived cache and is gitignored.
  Delete it to force a full mechanism re-run; it takes about twenty minutes.
- S2AND's README notes some affiliation data comes from the Microsoft Academic
  Graph. The `affiliation` column is a context field and is droppable before
  public release. Flagged for the 2.6 pre-submission gate.

## Read order for a fresh session

root CLAUDE.md -> phase2/CLAUDE.md (charter) -> this file (STATE.md) ->
phase2/PLAN.md (arc) -> phase2/phase2-spec.md (method) -> phase2/PREREG.md
(binding for 2.2, supersedes spec section 8) -> phase2/reports/phase2b_boundary.md
(what 2.2b found) -> phase2/PASSLOG.md (history).
