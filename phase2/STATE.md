# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.5a complete. The paper identity has been rewritten to the
  2.2e result and the manuscript outline is built.** Awaiting human review of
  `reports/OUTLINE.md` and the rewritten identity. No manuscript body text has
  been drafted. Phase 2.3 stays blocked and may not run at all.
- **The two-signal role separation is retired.** The charter mission, PLAN.md's
  paper identity, its working titles, and `phase2-spec.md` sections 1 and 3 now
  describe a pre-registered negative result: design-time mechanism selection for
  author name disambiguation has no signal a designer can act on, for a
  structural reason and an empirical one. Removed, not softened. `PREREG.md`
  was not touched and stays frozen.
- Phase 2.2e complete. `PREREG.md` as amended by Amendment 1 and Addendum 1a was
  executed on the evaluation split. H1 Supported, H2 Inconclusive, H3
  Inconclusive at the primary margin and Partial at delta = 0.02.
- **The mechanism pair is fixed.** The regression check reproduces the 2.2c
  counts exactly, and on the evaluation split `rule wins` is reachable: 3,025
  test signatures where the rule is right and the vote wrong, against 4,012 the
  other way, at k = 5. The 2.2b degeneracy is gone.
- **The result that pointed against the old identity has now been acted on.**
  Addendum 1a's role-separation clause required ADS to be the stronger driver of
  decidability under both its measures. It is the stronger driver under neither.
  That did not decide H2, because the power floor is evaluated first, but it was
  the sharpest measurement in 2.2e and 2.5a retired the framing it tested.
- Phase 2.2d complete, nothing outstanding. Phase 2.2c, 2.2b, 2.2a and 2.1
  complete. The 2.2b numbers stay as the frozen record of the nested pair and
  were not recomputed, overwritten or withdrawn.
- **Nothing was re-tuned, re-banded or redefined in 2.2e.** Section 7 stayed
  void, k stayed 5, the split and the band edges carried over from
  `phase2b_constants.py` at `5e13e38`, and no new constant was calibrated.

## The 2.2e result in one paragraph

The amended pair works: the k-nearest vote at k = 5 is genuinely two-sided
against the exact-evidence rule on held-out data, so a winner exists to be
predicted, which is what 2.2b lacked. But at the primary margin nothing is
decided. Every marginal pooled gap, on both axes, is smaller than delta = 0.05,
so every marginal pooled verdict is a demonstrated tie and the pre-registered
power floor carries both H2 and H3 to Inconclusive. Underneath that, the
substance is real and was reported beside the verdict: the pooled gap changes
sign across ADS bands and across SV bands; the decidability gradient falls across
the first four ADS bands and then rises again at ADS = 1.0 rather than
approaching zero as Amendment 1 predicted; and **SV, not ADS, is the stronger
driver of decidability**, under both of Addendum 1a's required measures, at every
k and every margin, and more so with the structural ADS = 1.0 row removed. There
is no SV-driven winner reversal below ADS = 1.0 at any margin; the strongest
structure there is a tie-crossing at delta = 0.02, and the shape is the
pre-registered gap-compression one.

## Phase 2.2e outcome, in numbers

Evaluation split, primary analysis population: 13,902 blocks, 197,479 test
signatures, unchanged from 2.2b because the split is unchanged. k = 5,
Levenshtein arm, delta = 0.05 unless stated.

- **Regression check, calibration split, run before any evaluation signature was
  read.** Reproduces the frozen 2.2c counts at every k: 181/736 at k = 2,
  314/740 at k = 3, **546/744 at k = 5**, 912/748 at k = 10. Rule accuracy 0.8234
  identical across k. Asserted in code; the run cannot proceed if it fails.
- **Two-sidedness on the evaluation split:** 3,025 rule-right/vote-wrong against
  4,012 vote-right/rule-wrong at k = 5. The k curve runs 987/3,990 at k = 2,
  1,724/4,004 at k = 3, 5,176/4,040 at k = 10. `rule wins` measured zero for the
  retired 2.2b pair on 199,713 signatures.
- **Pooled held-out accuracy:** rule 0.8244, k-NN 0.8294, gap -0.0050. Rule
  coverage 0.9686, vote coverage 1.0, agreement 0.9493. The rule's accuracy is
  identical to 2.2b's exact-match accuracy, as it must be.
- **H1 Supported.** Spearman of train-only ADS with held-out accuracy 0.5069
  [0.4919, 0.5224] rule and 0.8298 [0.8190, 0.8401] k-NN, positive pooled
  non-inspire and in all four qualifying non-inspire datasets. Validity check,
  not a contribution.
- **H2 Inconclusive at 0.05, 0.03 and 0.02.** No ADS band and no SV band has a
  decided pooled verdict at the primary margin, so the floor bites first.
- **H3 Inconclusive at 0.05 and 0.03, Partial at 0.02, margin-dependent.** At
  0.02 the ADS = 1.0 band clears the floor with three decided SV bands, and two
  ADS bands below 1.0 show a tie-crossing.
- **Pooled gap by ADS band:** +0.0334, +0.0215, +0.0123, -0.0028, -0.0278. At
  delta = 0.02 that becomes a decided marginal reversal, `rule wins` in [0, 0.5)
  against `k-NN wins` at 1.0.
- **Pooled gap by SV band:** -0.0388, -0.0144, -0.0115, +0.0189.
- **Decided-winner rate by ADS band:** 0.1083, 0.0618, 0.0256, 0.0089, 0.0278.
  Not monotone: it rises in the top band, which holds 10,537 of the 13,902
  blocks. Amendment 1 predicted it would approach zero there.
- **Addendum 1a driver comparison, the clause H2 needed:** eta2_ADS 0.1749
  against eta2_SV 0.3837, averaged ranges 0.0707 against 0.0755. ADS loses under
  both, so the clause **failed** rather than split. Stable across k in
  {2, 3, 5, 10} and across delta in {0.05, 0.03, 0.02}. Restricted to ADS < 1.0,
  a labeled diagnostic that decides nothing, 0.1755 against 0.4594. The
  block-weighted diagnostic, which also decides nothing, is 0.3653 against
  0.3765.
- **Non-trivial decidable region (resolution 6): present.** ADS bands [0, 0.5)
  and [0.5, 0.7) each hold 30 or more blocks with a decided per-block verdict.
  500 blocks carry a decided verdict overall at the primary margin.
- **Per-block verdicts at delta 0.05:** 500 decided, the rest tie or undecided.
- **Jaro-Winkler arm reproduces the picture:** pooled gaps -0.0388, -0.0146,
  -0.0116, +0.0181 across SV bands, same verdicts. **SV_resid** shows the same
  shape smaller: -0.0124, -0.0025, -0.0025, +0.0130, no reversal.
- **Regression of the per-block gap:** ADS -0.1889 (se 0.0076), SV +0.0548 (se
  0.0212), log test-set size +0.0208 (se 0.0018).
- **One pre-registration ambiguity found at run time**, reported rather than
  improvised: Amendment 1's "strictly lower in the top ADS band than in the
  bottom" admits a per-SV-band and a marginal construction, and they disagree
  here (2 of 4 usable SV bands, against True marginally). Both are printed; the
  disagreement changes no outcome because H2 is Inconclusive on the floor.
- Report: `reports/phase2e_boundary.md`. Tables `reports/tables/phase2e_*.csv`.
  Figures `reports/figs/phase2e_*.png`. Code `phase2/phase2e_mech.py` and
  `phase2/phase2e_run.py`.

## The 2.2d reframe in one paragraph

The paper's claim was rebuilt rather than repaired at 2.2d. It used to say a
consistency signal predicts each mechanism's accuracy but is blind to which
mechanism wins. 2.2c showed that cannot be true of any mechanism pair in this
family, because a block whose train history names one author returns that author
from any mechanism that assigns from history. The claim became a role
separation: consistency gates whether the mechanism choice is live at all,
surface stability directs it where it is, and neither signal alone predicts the
winner. **2.2e has now tested that and the one clause that measured it came out
against ADS.** The reframe's hypotheses are not refuted, because the power floor
carried them to Inconclusive, but they are not supported either, and the
role-separation clause pointed the other way. **That question was settled at
2.5a: the reframe is retired and the paper is now the negative result described
at the top of this file.** This paragraph stays as the record of what was
claimed and when.

## Phase 2.2c outcome, in numbers

Calibration blocks only: 2,450 blocks, 35,732 test signatures. Design
diagnostics, not results. Reproduced exactly by the 2.2e regression check.

Two-sidedness as (A right and B wrong) / (B right and A wrong), where A is the
unchanged PREREG section 4 exact-evidence rule:

- rule vs the 2.2b fuzzy arm: **0** / 731. The probe self-check.
- P1, radius vote: 1,461/635 at r=0.70, 793/503 at 0.80, 253/247 at 0.90,
  **0**/16 at 0.95. The r -> 1 limit recovers the degeneracy.
- P2, normalized-key vote: 158/437. No parameter on either side.
- P3, k-nearest vote: 181/736 at k=2, 314/740 at k=3, **546/744 at k=5**,
  912/748 at k=10. Adopted.

**The calibration trap, which Amendment 1 avoided.** For both parameterized
pairs the retriever's pooled accuracy is monotone toward the 1-NN limit, so
PREREG section 7 applied unchanged would have selected k = 2 and re-created the
nesting. Section 7 is void and k is fixed by definition, with a mandatory
sensitivity curve. 2.2e confirms the monotonicity on the evaluation split too:
k-NN accuracy 0.8396, 0.8360, 0.8294, 0.8187 as k grows.

Report: `reports/phase2c_pair_design.md`. Tables
`reports/tables/phase2c_pair_twosidedness.csv`,
`reports/tables/phase2c_pair_regimes.csv`. Code `phase2/phase2c_probe.py`.

## The 2.2b result in one paragraph

Exact match fires only when the test surface form already occurs among the train
forms. When it does, that form sits at similarity exactly 1.0, the maximum, so
the fuzzy arm retrieves the same form at any cutoff at or below 1.0 and resolves
the author with the same frozen tie-break. Across all 16,136 evaluation blocks
and 199,713 test signatures there are **zero** signatures on which exact is right
and fuzzy is wrong, in either metric arm. `exact wins` was an unreachable
verdict. This was measured, not deduced, and it stays in the repository as the
record of the nested pair. It is a result the paper keeps.

## Phase 2.2b outcome, in numbers

Frozen inputs, committed in `5e13e38` before the evaluation split was read:
fuzzy cutoff 0.50 for both metric families, SV band edges 0.102644 / 0.195066,
SV_resid 0.036782 / 0.082418. **These carry over to 2.2e unchanged.**

- Population: 18,984 live blocks, 2,848 calibration and 16,136 evaluation.
  Primary analysis population 13,902 blocks and 197,479 test signatures. Named
  exclusions, counted and reported: 7,955 singleton blocks (1.04% of signatures)
  and 2,234 block-size-2 blocks (0.58%).
- Pooled held-out accuracy: exact 0.8244, fuzzy 0.8441, gap -0.0196.
- **H1 Supported.** Spearman 0.5069 exact, 0.7436 fuzzy.
- **H2 Inconclusive. H3 Inconclusive at 0.05, Partial at 0.02.**
- Per-block verdicts at delta 0.05: 0 exact wins, 302 fuzzy wins, 11,117 tie,
  2,483 undecided.
- Signal correlations on the primary population: SV to SV_resid 0.51, SV to
  INIT 0.36, ADS to SV -0.27.
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
- Pass 6 (Phase 2.2b): PREREG.md executed. H1 Supported, H2 and H3 Inconclusive,
  and the mechanism pair found to be nested.
- Pass 7 (Phase 2.2c): mechanism redesign. Three two-sided candidate pairs
  checked on the calibration split, one recommended, two structurally-zero
  winner cells found.
- Pass 8 (Phase 2.2d): `PREREG.md` Amendment 1, the two-signal reframe. Nothing
  measured.
- Pass 9 (Phase 2.2d continued): Addendum 1a, replacing resolution 5's
  band-count-biased range test. Nothing measured.
- Pass 10 (Phase 2.2d closed): the pre-registration-integrity subsection locked
  into PLAN.md verbatim, drafted blind to the 2.2e result. Nothing measured.
- Pass 11 (Phase 2.2e): the amended experiment run. Mechanism B implemented and
  regression-checked against 2.2c before any evaluation signature was read, then
  the frozen analysis executed on the evaluation split. H1 Supported, H2
  Inconclusive, H3 Inconclusive and margin-dependent. The pair is two-sided. The
  role-separation clause failed under both required measures.
- **Pass 12 (Phase 2.5a): writing setup and outline. The paper identity rewritten
  to the true finding in the charter, PLAN.md and the spec; `reports/OUTLINE.md`
  built with section spines, an 8,100-word body budget, a six-table and
  five-figure plan, and six title candidates. Nothing measured. `PREREG.md`
  untouched.**

## Next: review the outline and the rewritten identity

Do not start drafting. Two things to read, in this order.

1. **The rewritten identity.** `phase2/CLAUDE.md` mission, `PLAN.md` paper
   identity and working titles, `phase2-spec.md` sections 1 and 3. The question
   is whether the negative result as stated there is the paper you want to write
   and whether anything in it overclaims. The old framing is gone from all four
   places.
2. **`reports/OUTLINE.md`.** Section list, spines, budgets, the six-table and
   five-figure plan, and six title candidates to merge with your own. It also
   records the writing constraints for the whole of 2.5 and lists four open
   inputs, including whether delta = 0.05 stays the primary margin and whether
   2.3 and 2.4 happen at all.

Then Phase 2.5b, the drafting pass, in the order OUTLINE.md's last section
gives: sections 4, 5 and 6 first, then 7, then 3, 8 and 9, then 1 and 2, then
the abstract. 2.5c is the anti-AI and citation-verification pass and is separate
by design.

The locked Phase 2.5 pre-registration-integrity subsection needs no change. It
was drafted blind and its argument is unaffected by an Inconclusive result or by
the identity rewrite.

## Open decisions

Frozen and committed, not to be re-decided:

- Blocking normalization and surface-form definition, `phase2/s2and_blocking.py`
  (Phase 2.1).
- Hypotheses, falsification table, splits and seeds, analysis population,
  minimum cell sizes, band rules, mechanism definitions and tie-breaking, the
  winner definition, the margins, the precedence of Inconclusive, the controls,
  the per-dataset rule: `phase2/PREREG.md` (Phase 2.2a), as amended at 2.2d.
- SV and SV_resid band edges: `phase2/phase2b_constants.py` (Phase 2.2b).
- The mechanism pair, the hypotheses, the falsification table, the voiding of
  section 7 and the six resolutions: `PREREG.md` Amendment 1 and Addendum 1a
  (Phase 2.2d). Sign-off closed when 2.2e started; these are now history.

Settled at Phase 2.5a:

- **The paper identity.** Retired the two-signal role separation; the paper is
  the negative result. Rewritten in the charter, PLAN.md and spec sections 1 and
  3. `PREREG.md` untouched.

Still open:

- **Is delta = 0.05 still the primary margin?** Unchanged by this pass, and the
  outline is written against it. Every marginal pooled gap on both axes falls
  below it, so the power floor decides both hypotheses before any substantive
  rule is read, and delta = 0.02 is where the data has structure. Moving it now,
  after seeing that, is the move the pre-registration exists to prevent. It is a
  decision to take explicitly and record as a dated amendment, or to decline
  explicitly. It is not a decision to slide into.
- **Whether 2.3 and 2.4 happen at all.** The rewritten identity has no selector
  in it. If they run, it is as a negative control, and OUTLINE.md open input 2
  says what changes in the outline.
- `phase2-spec.md` sections 7 and 9 still describe the selector and its success
  criteria. Out of scope for 2.5a; they should be rewritten or marked superseded.
- Whether the "strictly lower in the top ADS band than in the bottom" clause
  should be pinned to one construction. It cost nothing this time and will not
  always.
- Whether a third mechanism enters at all. Charter invariant 6 keeps it out
  unless it is actually implemented and evaluated.
- Title: six candidates now in PLAN.md and OUTLINE.md, to merge with the
  author's own.

## Live risks

- **The paper is now a null result, and it has to be written as a contribution
  rather than as a failed experiment.** New at 2.5a and now the dominant risk.
  The structural half carries it: exact match is a strict sub-case of
  single-nearest retrieval, and two cells are zero for any pair in the family.
  The empirical half is honest but thin on its own. If the drafting pass cannot
  make section 4 land as a result, the paper is in trouble and that is worth
  knowing early.
- **The role-separation clause failed, which is what retired the old identity.**
  eta2_ADS 0.1749 against eta2_SV 0.3837 and averaged ranges 0.0707 against
  0.0755, stable across k and delta, wider still without the structural ADS row.
  H2's Inconclusive verdict did not rescue the framing; it only meant the frozen
  rules declined to decide. Kept here because the paper reports the clause and
  its failure rather than dropping it.
- **The primary margin is wider than every effect on both axes.** Both
  hypotheses are decided by the power floor rather than by their own rules, at
  every margin on the curve for H2 and at two of three for H3. Whatever review
  decides about delta, the paper has to state plainly that the pre-registered
  margin is what made these Inconclusive.
- **The framing has changed twice after results, and a reviewer will say so.**
  Carried from 2.2d and widened at 2.5a: the 2.2d amendment changed the
  hypotheses, and 2.5a changed the paper identity again after they came out
  Inconclusive. The second change is safer than the first, because it moves
  toward the frozen table's own output rather than away from it, and because it
  amends no pre-registration, but it has to be stated as plainly as the first. The defence is procedural and visible: the amendment is dated and
  appended, the superseded text and the 2.2b numbers stay in the repository,
  what forced each change was a measured structural fact, and no accuracy for the
  new mechanism existed when the amendment was written. The 2.2e regression
  check now adds to that: the mechanism was verified against a pre-existing
  frozen count before any evaluation number was produced.
- **H2's structural component behaved unlike the amendment's prediction.** The
  decidability decline into ADS = 1.0 was conceded as partly structural and
  predicted to approach zero. It does not; the rate rises again in the top band.
  The amendment's reasoning was right and its prediction was wrong, which is
  worth saying in the paper in those words.
- **Power in the contested region.** Confirmed as the binding constraint. 500 of
  13,902 blocks carry a decided per-block verdict at the primary margin.
- **Collapse into Kim and Kim 2020.** Still live and now better bounded: the
  SV_resid grid shows the same shape as SV at smaller magnitude and with no
  reversal in either, so the surface effect is not only initialization but is not
  large in either form.
- inspire is 11,110 of 13,902 primary-population blocks. Per-dataset and pooled
  non-inspire reporting ran. H1 generalizes. Pooled non-inspire holds the
  decidable region and the top-below-bottom clause but not the non-increasing
  one, so H2's "holds in the pooled non-inspire analysis" clause is not met. No
  dataset shows an SV-driven winner reversal.
- The Kim and Kim preprint PDF in `phase2/` is deliberately untracked and
  gitignored: publisher preprint, no redistribution licence.
- `phase2/data/phase2b_eval_sigs.parquet` and
  `phase2/data/phase2e_eval_sigs.parquet` are derived caches and are gitignored.
  Delete either to force a full mechanism re-run; each takes about twenty
  minutes.
- S2AND's README notes some affiliation data comes from the Microsoft Academic
  Graph. The `affiliation` column is a context field and is droppable before
  public release. Flagged for the 2.6 pre-submission gate.

## Read order for a fresh session

root CLAUDE.md -> phase2/CLAUDE.md (charter) -> this file (STATE.md) ->
phase2/PLAN.md (arc) -> phase2/phase2-spec.md (method) -> phase2/PREREG.md,
**reading Amendment 1 and Addendum 1a at the end of that file first, because
they are what bind** and they supersede sections 2, 4, 7 and 10 ->
phase2/reports/phase2e_boundary.md (what 2.2e found, against the amended pair)
-> phase2/reports/phase2b_boundary.md (what 2.2b found, against the retired
pair) -> phase2/reports/phase2c_pair_design.md (why the pair changed) ->
phase2/reports/OUTLINE.md (what the paper will be) -> phase2/PASSLOG.md
(history).
