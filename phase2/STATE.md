# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.2c (mechanism redesign) complete as a design-and-propose
  pass. A two-sided replacement pair is proposed and checked on the calibration
  split.** Awaiting human review.
- **Phase 2.3 is still blocked and must not start.** It unblocks only after
  review adopts a mechanism pair and a new pre-registration is frozen and
  committed for it.
- Phase 2.2b (the boundary experiment) complete; its numbers are the frozen
  evidence base and are untouched by 2.2c. Phase 2.1 (data foundation) complete,
  hard gate passed. Phase 2.2a (pre-registration) complete and frozen.
  **Nothing in PREREG.md has been amended, by this pass or any other.**

## The 2.2c result in one paragraph

Three candidate mechanism pairs were designed and checked on the calibration
blocks only. All three are genuinely two-sided, so the 2.2b degeneracy is
repairable. The narrow reason the old pair failed is that a test form present in
the train history sits at similarity exactly 1.0, the maximum of any similarity,
so exact match is contained in **every** single-nearest-form retriever, whatever
the metric or cutoff. The repair is to make mechanism B aggregate over a
neighbourhood instead. But the probe also found two cells that are zero by
construction for any pair of this shape: the precision-first rule can never win
at SV = 0, where the history carries one distinct form, and can never win at
ADS = 1.0, where the history names one author, so any non-empty pool returns it
and the rule's only possible difference is to abstain. The second holds for any
pair of mechanisms that assign an author from the block's own history. A contest
therefore exists only where the history is both impure and surface-varied, which
is 41% of calibration test signatures, and **ADS necessarily predicts part of the
winner**, which H2 as currently worded denies. At fixed ADS the sign still flips
with SV in all four ADS bands below 1.0, so ADS alone does not determine the
winner either. Neither signal alone does.

## Phase 2.2c outcome, in numbers

Calibration blocks only: 2,450 blocks, 35,732 test signatures. Design
diagnostics, not results. No bootstrap, no margin, no verdict.

Two-sidedness as (A right and B wrong) / (B right and A wrong), where A is the
unchanged PREREG section 4 exact-evidence rule:

- rule vs the 2.2b fuzzy arm: **0** / 731. The probe self-check; reproduces the
  2.2b nesting and fails loudly if it does not.
- P1, radius vote: 1,461/635 at r=0.70, 793/503 at 0.80, 253/247 at 0.90,
  **0**/16 at 0.95. The r -> 1 limit recovers the degeneracy.
- P2, normalized-key vote: 158/437. No parameter on either side.
- P3, k-nearest vote: 181/736 at k=2, 314/740 at k=3, **546/744 at k=5**,
  912/748 at k=10.

Recommended pair: **P3 with k fixed a priori at 5**, rule accuracy 0.8234 against
retriever 0.8290, retriever coverage 1.0 so abstention sits entirely on the
rule's side. P2 is the fallback if review prefers zero parameters.

**The calibration trap, which the new pre-registration must avoid.** For both
parameterized pairs the retriever's pooled accuracy is monotone toward the 1-NN
limit (knn: 0.8390, 0.8354, 0.8290, 0.8188 as k grows; radius: up to 0.8239 at
r=0.95). PREREG section 7 calibrates by maximizing pooled accuracy, so applied
unchanged it would select k=2 or r=0.95 and re-create the nesting. The parameter
must be fixed by a definitional argument with a pre-registered sensitivity curve,
never chosen to maximize the retriever.

Report: `reports/phase2c_pair_design.md`. Tables
`reports/tables/phase2c_pair_twosidedness.csv`,
`reports/tables/phase2c_pair_regimes.csv`. Code `phase2/phase2c_probe.py`.

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
- Pass 6 (Phase 2.2b): PREREG.md executed. Calibration frozen in its own commit
  first, then the evaluation split. H1 Supported, H2 and H3 Inconclusive, and
  the mechanism pair found to be nested.
- **Pass 7 (Phase 2.2c): mechanism redesign, design-and-propose. Three two-sided
  candidate pairs checked on the calibration split, one recommended, and two
  structurally-zero winner cells found that H2's current wording cannot survive.
  No evaluation, no amendment.**

## Next: review adopts a pair, then a fresh session writes the new pre-registration

Do not open 2.3 and do not run any evaluation. Review decides, in this order:

1. **Which mechanism pair.** P3 (exact-evidence rule vs k-nearest vote, k = 5)
   recommended; P2 (rule vs normalized-key vote) the parameter-free fallback.
   Full rationale, risks and counts in `reports/phase2c_pair_design.md`.
2. **What replaces H2.** This is the larger decision. H2 as PREREG section 2
   words it cannot survive, because ADS = 1.0 makes the rule unable to win by
   construction, so ADS predicts part of the winner for any pair of this shape.
   The supportable shape is two-signal: consistency says whether the choice
   matters at all, surface stability says which way to go when it does. That
   changes the paper's stated identity in CLAUDE.md and PLAN.md.
3. **The analysis population and the margin.** The contested region (ADS < 1 and
   SV > 0) is the natural population, and it is smaller than 2.2b's, which was
   already power-limited at delta = 0.05.

Only after those three are settled does a fresh session write the new
pre-registration, as a dated amendment section appended to `PREREG.md` per its
own amendment rule, committed before any new accuracy exists.

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

Still open, in the order review should take them:

- **Which mechanism pair.** P3 recommended, P2 the fallback. See the Next
  section above and `reports/phase2c_pair_design.md`.
- **What replaces H2.** The largest live decision. Its current wording cannot
  survive the ADS = 1.0 structural zero, for any pair of this shape.
- **The analysis population and the margin** inside the contested region.
- Whether a third mechanism enters at all. Charter invariant 6 keeps it out
  unless it is actually implemented and evaluated. 2.2c did not propose one.
- Title: working candidates in PLAN.md. All three presume ADS is blind to the
  winner, which 2.2c shows it cannot be, so all three need replacing.

## Live risks

- **The nesting has fired and is now repairable.** 2.2c found three two-sided
  replacement pairs, so this is a design decision with a recommendation attached
  rather than an open risk. The nesting itself stays in the paper as a result.
- **ADS cannot be blind to the winner.** New at 2.2c, and the dominant risk now,
  because it is a constraint on any mechanism pair rather than on ours: at
  ADS = 1.0 a precision-first rule cannot win, so the consistency signal
  necessarily carries some winner information. The paper's stated identity in
  CLAUDE.md, PLAN.md and phase2-spec.md all say the opposite and all three need
  review.
- **The parameter calibration protocol selects for degeneracy.** PREREG section
  7 maximizes the retriever's pooled accuracy, which for both parameterized
  candidate pairs points at the 1-NN limit. Carrying section 7 over unchanged
  would re-create the 2.2b failure. Fix the parameter by definition, report a
  sensitivity curve.
- **Power in the contested region.** It is 41% of calibration test signatures
  and excludes every ADS = 1.0 block, so it is smaller than the population 2.2b
  was already power-limited on at delta = 0.05.
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
(what 2.2b found) -> phase2/reports/phase2c_pair_design.md (the proposed
replacement pair and what constrains it) -> phase2/PASSLOG.md (history).
