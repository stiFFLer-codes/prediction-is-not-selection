# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.2d (pre-registration revision) complete. `PREREG.md`
  Amendment 1 and Addendum 1a are appended, dated and binding. Nothing was
  measured.** Awaiting human review before 2.2e runs.
- **Next is 2.2e**, the re-run against Amendment 1 as revised by Addendum 1a.
  Phase 2.3 stays blocked until 2.2e produces numbers.
- **Nothing is outstanding.** The pre-registration-integrity subsection is locked
  into PLAN.md as a required Phase 2.5 writing deliverable, author-drafted blind
  to the 2.2e result, reproduced verbatim, and marked not to be softened or
  strengthened by what 2.2e returns.
- Phase 2.2c (mechanism redesign) complete: three two-sided candidate pairs
  checked on the calibration split, P3 recommended and now adopted. Phase 2.2b
  complete; its numbers are the frozen record of the nested pair and are
  untouched. Phase 2.1 complete, hard gate passed. Phase 2.2a complete.
- **PREREG.md has been amended once**, at 2.2d. The amendment is appended, not
  edited in, so the 2.2a text and the 2.2b run conditions remain readable in
  full. Sections 2, 4, 7 and 10 carry banners pointing to it.

## The 2.2d reframe in one paragraph

The paper's claim was rebuilt rather than repaired. It used to say a consistency
signal predicts each mechanism's accuracy but is blind to which mechanism wins.
2.2c showed that cannot be true of any mechanism pair in this family, because a
block whose train history names one author returns that author from any
mechanism that assigns from history, so a precision-first rule cannot win there
and consistency necessarily carries some winner information. The claim is now a
role separation: **consistency gates whether the mechanism choice is live at
all, surface stability directs it where it is, and neither signal alone predicts
the winner.** H1 is unchanged and still a validity check. H2 is now a gating
hypothesis about the decided-winner rate declining as ADS rises. H3 keeps the SV
reversal requirement and adds the non-direction-by-ADS half, which is the old
blindness claim correctly scoped to decidable blocks at fixed surface stability.
Mechanism B is the k-nearest vote at k = 5. None of this is measured; it is a
frozen falsification table awaiting 2.2e.

## What Amendment 1 changed, in one list

- **Section 2, replaced.** New H2 (gating) and H3 (directing, two required
  parts), new contribution statement. H1 unchanged in substance.
- **Section 4, amended.** Mechanism B is the k-nearest-vote retriever: pool
  nearest training signatures, whole forms at a time, until at least k are
  pooled, then a signature-weighted author vote. It never abstains. Mechanism A,
  the exact-evidence rule, is untouched.
- **Section 7, void for 2.2e.** B has no similarity cutoff. k = 5 is fixed by
  definition, never by maximizing accuracy, because accuracy is monotone toward
  the single-nearest limit, which is the 2.2b nesting. The k in {2, 3, 5, 10}
  sensitivity curve is mandatory and a k-dependent outcome is Partial.
- **Section 8, renamed only.** `exact wins` becomes `rule wins`, `fuzzy wins`
  becomes `k-NN wins`. Bootstrap, seeds, margins and the four-verdict rule are as
  frozen at 2.2a.
- **Section 10, replaced.** New falsification table for the new H2 and H3.
  Inconclusive still evaluated first. Two new acceptable outcomes: the choice is
  never live, and consistency directs as well as gates.
- **Unchanged and not recomputed:** the section 3 split and population, the
  section 5 ADS bands, the section 6 SV and SV_resid band edges frozen in
  `phase2b_constants.py` at `5e13e38`, the section 9 controls and grid, and the
  section 11 per-dataset rule.

## Six resolutions flagged for review

The revision as handed over was under-determined or drifted from what 2.2c
measured in six places. Each is resolved in the amendment, before any number
exists, and **each can be overruled before 2.2e starts and not after**. Full text
in `PREREG.md` Amendment 1, "Resolutions of ambiguity".

1. "k nearest" counts **signatures**, not forms. That is what 2.2c measured; the
   form-counted reading is untested.
2. Mechanism B uses the **frozen section 4 tie-break chain**, not "toward the
   nearest form", which is under-determined and would give the two mechanisms
   different tie-breaks.
3. The nesting limit is **k = 1**, not k = 2. k = 1 is off the sensitivity curve
   as the known-degenerate case.
4. "Decided" in H2 means the **per-block** verdict; H3's reversal keeps using the
   **pooled band** verdict.
5. "ADS is the stronger driver of decidability" is now a two-part test, set by
   **Addendum 1a**: ADS must have the larger one-way variance component
   (eta-squared style, unweighted over eligible cells) **and** the larger
   averaged range. A split makes the clause Partial. The original
   range-only test was replaced because range is not invariant to band count and
   the grid is 5 by 4, which handed ADS an unearned edge.
6. "A non-trivial decidable region" means at least one ADS band below 1.0 with 30
   or more blocks holding 30 or more decided per-block verdicts.

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
- Pass 7 (Phase 2.2c): mechanism redesign, design-and-propose. Three two-sided
  candidate pairs checked on the calibration split, one recommended, and two
  structurally-zero winner cells found that H2's old wording could not survive.
  No evaluation, no amendment.
- Pass 8 (Phase 2.2d): pre-registration revision. `PREREG.md` Amendment 1
  appended and dated, reframing the paper from one-signal blindness to two-signal
  role separation, adopting the k-nearest vote at k = 5, and voiding the
  accuracy-maximizing calibration. Identity updated in the charter, the spec and
  PLAN.md. Nothing measured.
- Pass 9 (Phase 2.2d continued): Addendum 1a, replacing resolution 5's
  band-count-biased range test with a one-way variance decomposition plus the
  range test as a second required condition. One requested deliverable left
  outstanding for want of its supplied text. Nothing measured.
- **Pass 10 (Phase 2.2d closed): the pre-registration-integrity subsection locked
  into PLAN.md verbatim, drafted blind to the 2.2e result. Two wording checks
  against the repository record were noted beside it rather than edited into it,
  because it is locked. Nothing measured. 2.2d is complete with nothing
  outstanding.**

## Next: review verifies Amendment 1, then a fresh session runs 2.2e

Do not run any evaluation until the amendment is signed off. Review should read
`PREREG.md` Amendment 1 end to end, and in particular:

1. **The six resolutions above**, and **Addendum 1a**, which replaced
   resolution 5. They are the only places where this pass made a judgement call
   rather than transcribing the instruction. Overrule now or not at all.
2. **The new H2 and H3, and their falsification table.** Especially whether
   resolution 6 and Addendum 1a set the H2 bar in the right place, since they are
   the thresholds that were not given.
3. **That the amendment claims nothing.** Every hypothesis in it is untested.
4. **The locked Phase 2.5 deliverable** in PLAN.md, if it has not been read
   since it was written. It is fixed in advance on purpose, so the moment to
   object to it is before 2.2e, not after.

Then a fresh session runs 2.2e: implement mechanism B with its own assert-based
self-check, confirm the self-check reproduces the 2.2c calibration counts,
re-run the frozen analysis with the renamed verdicts, and report against the
amended falsification table plus the mandatory k and delta curves. Nothing new is
calibrated in 2.2e; the split, the band edges and the margins all carry over.
Both decidability measures of Addendum 1a are computed and reported, the
unweighted decomposition deciding and the block-weighted variant beside it as a
diagnostic that decides nothing.

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

Decided at 2.2d and now frozen in `PREREG.md` Amendment 1, not to be
re-decided once 2.2e starts:

- The mechanism pair: the exact-evidence rule against the k-nearest vote at
  k = 5, with the k curve mandatory.
- The hypotheses, the contribution statement and the falsification table.
- That section 7 is void and nothing new is calibrated for 2.2e.
- The six resolutions of ambiguity, with resolution 5 as replaced by
  Addendum 1a.

Still open:

- **Sign-off on Amendment 1**, and on the six resolutions in particular. This is
  the only live decision, and it closes when 2.2e starts.
- Whether a third mechanism enters at all. Charter invariant 6 keeps it out
  unless it is actually implemented and evaluated. 2.2c did not propose one.
- Title: three new candidates in PLAN.md, all built on the two-signal framing.
  They are provisional until 2.2e returns outcomes.

## Live risks

- **The nesting has fired and is now repairable.** 2.2c found three two-sided
  replacement pairs, so this is a design decision with a recommendation attached
  rather than an open risk. The nesting itself stays in the paper as a result.
- **ADS cannot be blind to the winner.** Found at 2.2c, absorbed at 2.2d. The
  charter, PLAN.md and phase2-spec.md now state the two-signal framing, and
  `PREREG.md` Amendment 1 is the binding version. No longer an open risk, but the
  reason the paper's identity changed, and it belongs in the paper.
- **The parameter calibration protocol selects for degeneracy.** Fixed at 2.2d:
  section 7 is void, k = 5 is fixed by definition, and the k curve is mandatory.
  The residual risk is that k = 5 was chosen on the calibration split for contest
  balance, which is disclosed in the amendment and is what the k curve exists to
  expose.
- **The reframe is post hoc and a reviewer will say so.** New at 2.2d, and the
  dominant framing risk. The hypotheses were rewritten after 2.2b and 2.2c
  returned results. The defence is procedural and has to be visible in the paper:
  the amendment is dated and appended rather than edited in, the superseded text
  and the 2.2b numbers stay in the repository, what forced each change is a
  measured structural fact rather than a disappointing number, and no accuracy
  for the new mechanism existed when the amendment was written. Whether that
  defence holds is review's call, not this pass's.
- **The new H2 has a partly structural component.** The decline of decidability
  into the ADS = 1.0 band is guaranteed, not discovered. The amendment says so in
  its own text and puts the load-bearing content on the gradient below 1.0 and on
  the existence of a decidable region. Addendum 1a reduces that row's leverage on
  the role-separation clause by unweighting cells, but does not remove the row,
  and says so. A reviewer who reads only the headline will still mistake one for
  the other, so the two statements go in the paper adjacent.
- **Measures chosen to decide a hypothesis can tilt toward it.** Surfaced at
  Pass 9 and worth carrying: resolution 5's range test favoured ADS purely
  because the grid is 5 by 4. Every remaining threshold that was set rather than
  given, resolution 6 and the two halves of Addendum 1a, deserves the same
  question before 2.2e starts, since none can be changed after.
- **The post hoc objection is now answered in a fixed text, not improvised
  later.** The Phase 2.5 pre-registration-integrity subsection is locked in
  PLAN.md, drafted blind to the 2.2e result. The risk it does not remove is that
  a reader may still judge the amendment inadequate; what it removes is the
  weaker position of arguing the point after seeing the outcome it defends.
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
phase2/PLAN.md (arc) -> phase2/phase2-spec.md (method) -> phase2/PREREG.md,
**reading Amendment 1 at the end of that file first, because it is what binds**
and it supersedes sections 2, 4, 7 and 10 -> phase2/reports/phase2b_boundary.md
(what 2.2b found, against the retired pair) ->
phase2/reports/phase2c_pair_design.md (why the pair changed and what constrains
any replacement) -> phase2/PASSLOG.md (history).
