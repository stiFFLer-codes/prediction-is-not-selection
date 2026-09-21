# Phase 2.5 manuscript outline

Built at Phase 2.5a, 2026-09-18, against the rewritten paper identity in
`phase2/CLAUDE.md`, `phase2/PLAN.md` and `phase2/phase2-spec.md` section 1. It
adapts the skeleton in `phase2-spec.md` section 10 to a paper whose result is
methodological and null, and it supersedes that section's budget. No manuscript
body text is drafted here. This file is the plan the drafting pass executes.

Inputs, all committed: `phase2/PREREG.md` with Amendment 1 and Addendum 1a
(frozen, never edited by a writing pass), `reports/phase2b_boundary.md`,
`reports/phase2c_pair_design.md`, `reports/phase2e_boundary.md`,
`reports/kim2020_positioning.md`, `reports/gate21_two_axes.md`, and the tables
under `reports/tables/`.

---

## Writing constraints for the whole of Phase 2.5

Recorded here because they govern every drafting session, not just this one.

- Plain English. Short, concrete sentences. Say the thing, then stop.
- Sentence-case headings throughout, including subsections and captions.
- No em dashes anywhere. Commas, full stops, or a rewrite.
- Venue-neutral LaTeX, generic `article` class, no journal style file.
- Honest framing, no overclaim. Inconclusive means the frozen rules declined to
  decide, which is not the same as an effect being absent, and the paper never
  slides between those two statements.
- Every number traceable to a committed table or figure under `reports/`. If a
  number cannot be pointed at a file, it does not go in the paper.
- The verdicts come from the frozen falsification table, never from inspection.
  Substance reported beside a verdict is labelled as substance.
- `PREREG.md` is frozen. The writing pass quotes it and never edits it.
- The pre-registration-integrity subsection is reproduced from the locked text in
  `PLAN.md`, not rewritten. Its own fill-at-writing checklist is worked through.
- The `/anti-ai` pass is a dedicated session at 2.5c. Do not apply it while
  drafting. Draft for accuracy first.

---

## The finding, in one paragraph

This is the spine of the whole paper. Every section serves it.

A designer choosing between a precision-first rule and a coverage-first retriever
would like to measure something about their own data first and be told which to
build. On seven public author name disambiguation datasets, they cannot be. The
obvious comparison, exact match against fuzzy retrieval, is not a comparison at
all: a test surface form present in the history sits at the maximum of any
similarity function, so exact match is a strict sub-case of single-nearest
retrieval and cannot win, at any cutoff, in any metric family. We measured that
as zero rule wins on 199,713 held-out signatures before we understood it, and the
general form covers any pair of mechanisms that assigns an author from the
block's own history. We then built a pair that is genuinely two-sided, an
exact-evidence rule against a k-nearest vote, pre-registered the analysis before
running it, and found that where a contest is structurally possible it is
empirically tiny. The two mechanisms are within half an accuracy point pooled.
The gap compresses with surface stability and changes sign marginally on both
axes, but no band clears the pre-registered margin, so both selection hypotheses
return Inconclusive. The one pre-registered clause that asked which signal drives
decidability found surface stability, not consistency, and it found it at every k
and every margin. The consistency signal is real: it predicts each mechanism's
own accuracy with Spearman 0.51 and 0.83. It just does not tell you what to
build.

## What the paper claims, and what it does not

Claims:

1. Exact match is a strict sub-case of single-nearest retrieval. A comparison
   between them cannot have a winner. Structural, general, and measured.
2. For any pair of mechanisms that assigns an author from the block's own
   history, a precision-first rule cannot win where the history names one author,
   and cannot win where the history is written one way.
3. On a pair built to avoid both problems, neither design-time signal yields an
   actionable selection rule at the pre-registered margin.
4. A design-time consistency statistic does predict each mechanism's own
   accuracy, and generalizes across datasets. Prediction is not selection.

Does not claim:

- That no design-time selection signal exists for any mechanism pair anywhere.
  The claim is scoped to this substrate, these two mechanisms, and this margin.
- That the effects measured below the margin are zero. They are small, sign
  changing, and not decidable under the frozen rules.
- Anything about a selector. None was built and none is evaluated.
- Anything about learned disambiguation systems. Both mechanisms are untrained
  lookups, on purpose.

---

## Section outline, spines and budgets

### Abstract, 250 words

**Spine.** A designer cannot measure their data at design time and learn which of
two mechanisms to build, for one structural reason and one empirical one.

Leads with the structural result, states the pre-registration, gives H1 as the
contrast (the signal works for prediction), gives H2 and H3 as Inconclusive with
the reason (the margin is wider than every effect), and names the substrate.
No selector mentioned except as not-attempted.

### 1. Introduction, 900 words

**Spine.** Establishes the prediction-to-selection question, states that this
paper answers it negatively on real data, and lists the four claims above.

- 1.1 The design-time question, 250. A practitioner has history and no labels for
  the future. Prediction of difficulty is well studied. Selection between
  mechanisms at design time is the question, and it is different.
- 1.2 Why author name disambiguation, 200. Two block-level axes vary natively and
  separately, homonymity and synonymity, and S2AND ships seven datasets in one
  format. Point forward to section 3.
- 1.3 What we found, 300. The structural result first, then the empirical null,
  then H1 as the contrast that makes the null informative rather than a failure
  to measure anything.
- 1.4 Contributions and what is not claimed, 150.

### 2. Related work, 1050 words

**Spine.** Places the paper between a sibling on the economic axis and a sibling
on the surface axis, and shows that neither asks the selection question we ask.

- 2.1 Decision-focused evaluation, 250. Hand 2009, Hernandez-Orallo et al. 2012,
  Vickers and Elkin 2006, Elmachtoub and Grigas 2022. Tan (2026) as the sibling:
  a signal-versus-selection gap for model choice under decision economics, with
  an economic blind axis and no per-block unit.
- 2.2 Author name disambiguation as the home domain, 250. S2AND, WhoIsWho, one
  AND survey, Backes 2018 on string matching as a mandatory baseline.
- 2.3 The algorithm-selection spine, 250. Rice, Smith-Miles, Barbudo et al.
  Per-instance algorithm selection assumes a portfolio whose members can beat
  each other. Set up the structural result: that assumption is not free.
- 2.4 Surface-form robustness and Kim and Kim 2020, 250. Their manipulation, their
  gap-compression headline, their explicit non-claim of a winner change, and the
  four differences that matter: measured against manipulated, block against
  dataset, design-time against experimental arm, and a winner construct against a
  gap magnitude. Source: `reports/kim2020_positioning.md`.
- 2.5 Scoping paragraph, 50. Reject-option and learning-to-defer are adjacent and
  out of scope, in one sentence each.

### 3. Problem setting and constructs, 650 words

**Spine.** Defines the block as the unit, the two design-time signals, and the
winner construct, all of which were frozen before any accuracy existed.

- 3.1 Blocks, signatures and the design-time constraint, 200. Train-only,
  label-free for SV, available before any decision.
- 3.2 The two axes, 250. ADS as train-only purity, SV as expected normalized edit
  distance within the block's train forms, plus SV_resid and INIT as controls.
  Both axes measured alive at 2.1 and separable at Spearman -0.26, cross-checked
  against S2AND's own homonymity and synonymity facets at -0.818 and +0.743.
- 3.3 The winner construct, 200. Paired bootstrap, practical-equivalence margin,
  four verdicts with tie and undecided kept apart. State here, before any result,
  why merging tie and undecided would let low power read as equivalence.

### 4. A comparison that cannot have a winner, 650 words

**Spine.** The sharpest contribution: exact match is contained in single-nearest
retrieval, so the rules-versus-fuzzy comparison is degenerate by construction,
and two further cells are zero for any mechanism pair in the family.

- 4.1 The containment argument, 250. One paragraph of argument, no data needed. A
  present form sits at similarity 1.0, which is the maximum, so any single-nearest
  retriever selects it and resolves the same author under the same tie-break.
  Independent of cutoff, metric family and tie-break.
- 4.2 What we measured, 200. Zero `exact wins` on 199,713 test signatures across
  16,136 evaluation blocks, in both metric arms. The agreement diagnostic
  collapsed to an identity. The pooled gap reduced to the coverage difference.
  This was found by running a pre-registered analysis, not by deriving it first,
  and the paper says so.
- 4.3 The general form, 200. For any pair of mechanisms assigning from the
  block's own history: at ADS = 1.0 the rule can only differ by abstaining, and
  at SV = 0 every mechanism sees the same evidence. Two cells of any such design
  are zero before the data is seen. Consequence for anyone running a
  rules-versus-fuzzy comparison, stated plainly.

### 5. A pair that can, 450 words

**Spine.** Describes the redesigned mechanism pair and the calibration-split
evidence that it is two-sided, including the calibration trap that would have
recreated the degeneracy.

- 5.1 The three candidates and why the k-nearest vote, 250. Radius vote,
  normalized-key vote, k-nearest vote. Rank beats radius because every name in a
  block shares a surname, so absolute similarity has no scale. Abstention sits
  entirely on the rule's side, which is the precision-versus-coverage contrast
  the paper is about.
- 5.2 The calibration trap, 200. The retriever's accuracy is monotone toward the
  single-nearest limit, so accuracy-maximizing calibration selects the degenerate
  parameter. k is fixed by definition at 5 with a mandatory sensitivity curve,
  and the original calibration protocol is void. This is a reusable warning, not
  a housekeeping note.

### 6. Experimental design and pre-registration, 1100 words

**Spine.** States exactly what was fixed in advance, by whom and when, and hands
the reader the falsification rules before any result appears.

- 6.1 Data, blocking and splits, 250. 766,133 signatures, 7 datasets, 26,939
  blocks. Live, calibration 15%, evaluation 85%, within-block train and test,
  seed 20260918. Primary analysis population 13,902 blocks and 197,479 test
  signatures, with both exclusions named and counted.
- 6.2 Signals and their bands, 250. ADS bands fixed by definition, SV bands from
  calibration-split terciles of the strictly positive values with SV = 0 as its
  own structural band, SV_resid and INIT.
- 6.3 Mechanisms, metric and winner, 300. The exact-evidence rule, the k-nearest
  vote, abstention scored as incorrect, coverage reported separately, the frozen
  tie-break chain shared by both arms, the margins, and the order-of-evaluation
  rule that puts Inconclusive first.
- 6.4 Pre-registration and its amendment, 300. Reproduce the locked deliverable in
  `PLAN.md` lines under "Required Phase 2.5 deliverable". Do not rewrite its
  argument. Work its fill-at-writing checklist: confirm commit ids, confirm the
  amendment predates the run it governs, and settle the two wording checks
  recorded at lock time ("amended once" against two dated appends, and "two
  exploratory runs" against 2.2b being the pre-registered run).

### 7. Results, 1600 words

**Spine.** Reports what the frozen table returned, in its own order, with the
substance underneath each verdict labelled as substance.

- 7.1 The pair is two-sided now, 200. 3,025 against 4,012 at k = 5, positive at
  every k on the curve, against zero for the retired pair. A winner exists to be
  predicted, which is what the earlier design lacked.
- 7.2 H1, the consistency signal is a real difficulty signal, 250. Spearman
  0.5069 [0.4919, 0.5224] for the rule and 0.8298 [0.8190, 0.8401] for the vote,
  positive in pooled non-inspire and in all four qualifying non-inspire datasets.
  Supported. Labelled a validity check, not a contribution, with the citation to
  the dataset-level version of the same effect.
- 7.3 Head to head, 200. Pooled 0.8244 against 0.8294, gap -0.0050. Rule coverage
  0.9686, vote coverage 1.0, agreement 0.9493. Per dataset, including the two
  where the rule is ahead by a wide margin, kisti at +0.1131 and pubmed at
  +0.2466, and the inspire dominance stated in the open.
- 7.4 H2 and H3, what the frozen table returned, 350. Both Inconclusive at the
  primary margin, because the power floor is evaluated first and every marginal
  pooled gap on both axes is smaller than delta = 0.05. H3 is Partial at 0.02 and
  therefore margin-dependent. 500 of 13,902 blocks carry a decided per-block
  verdict. State plainly that the pre-registered margin is what made these
  Inconclusive, and that this is a permitted and pre-listed outcome.
- 7.5 Gap compression on both axes, 300. ADS bands +0.0334, +0.0215, +0.0123,
  -0.0028, -0.0278. SV bands -0.0388, -0.0144, -0.0115, +0.0189. No SV-driven
  reversal below ADS = 1.0 at any margin; the strongest structure below the top
  band is a tie-crossing at 0.02. The shape is the pre-registered gap-compression
  one, which is Kim and Kim's dataset-level finding reproduced at block level with
  measured surface variation. Robustness in one place: SV_resid gives the same
  shape smaller with no reversal, Jaro-Winkler reproduces it, and the regression
  summary agrees in sign.
- 7.6 Which signal drives decidability, 300. Addendum 1a's clause, reported as the
  measurement it is. eta2_ADS 0.1749 against eta2_SV 0.3837 and averaged ranges
  0.0707 against 0.0755, so the clause fails under both required measures rather
  than splitting, at every k and every margin, and wider with the structural
  ADS = 1.0 row removed (0.1755 against 0.4594). Beside it, the decidability
  gradient is not monotone: 0.1083, 0.0618, 0.0256, 0.0089, then back up to
  0.0278 in the top band, against a pre-registered prediction that it would
  approach zero. The amendment's reasoning was right and its prediction was
  wrong, in those words.

### 8. Discussion, 950 words

**Spine.** Says plainly what does not work and why, and what that leaves for
anyone hoping to choose a mechanism by measuring their data first.

- 8.1 What does not work, and why, 300. Two reasons, separately. The structural
  one is that the mechanism pair people reach for first is nested, so the winner
  is not a free variable. The empirical one is that once the pair is genuinely
  two-sided, the mechanisms are close enough that a practitioner-relevant margin
  cannot resolve them on most blocks. Neither reason is a measurement failure and
  both are actionable.
- 8.2 What the structural result means for benchmark and portfolio design, 250.
  Check that portfolio members can beat each other before selecting among them.
  Report the structurally zero cells in the design section, not as a surprise in
  the results. Applies directly to per-instance algorithm selection and to any
  rules-versus-retrieval comparison.
- 8.3 What it retroactively explains about our own earlier synthetic result, 200.
  A nested pair yields a winner that cannot vary, so the winner looks like a clean
  constant function of whatever moves the margin, and a consistency signal looks
  blind to a choice that was never open. Presented as an interpretation of a
  published result of ours, not as a new measurement, and used to make the general
  warning concrete.
- 8.4 What would have to be true for design-time selection to work, 200.
  Mechanisms far enough apart that the gap clears a margin a practitioner would
  act on, a contested region that is not a minority of the corpus, and a signal
  whose association with the winner survives both controls. Named as conditions,
  not as future work promises.

### 9. Limitations, 450 words

**Spine.** Names the four things a fair reviewer will raise, before they do.

Power in the contested region and the margin choice; the post-hoc amendment, with
the integrity subsection pointed at rather than re-argued; inspire carrying 11,110
of 13,902 blocks; two simple untrained mechanisms rather than a heuristic against
a learned system, which is the harder comparison Kim and Kim ran; and the residual
overlap between SV and forename initialization at Spearman 0.36, bounded by the
SV_resid arm.

### 10. Conclusion, 300 words

**Spine.** Prediction is not selection, and on this substrate there is nothing to
select.

Restates the four claims, states what a practitioner should do instead (measure
difficulty, expect the choice not to matter, check your two mechanisms are not
nested), and ends without a future-work wish list.

---

## Budget

| section | words |
| --- | ---: |
| 1. Introduction | 900 |
| 2. Related work | 1050 |
| 3. Problem setting and constructs | 650 |
| 4. A comparison that cannot have a winner | 650 |
| 5. A pair that can | 450 |
| 6. Experimental design and pre-registration | 1100 |
| 7. Results | 1600 |
| 8. Discussion | 950 |
| 9. Limitations | 450 |
| 10. Conclusion | 300 |
| **body total** | **8100** |
| abstract (outside body, inside total) | 250 |
| **prose total** | **8350** |

References, table content and figure captions sit outside the body budget, per
the charter. At 8,350 words of prose there is roughly 1,600 words of headroom
under the 10,000 total, which is where captions and the reference list go. If a
section overruns, the first places to cut are 2.3 and 7.3, in that order.

---

## Figure and table plan

2.2b, 2.2c and 2.2e produced 26 analysis tables and 10 figures under
`reports/tables/` and `reports/figs/`, plus the 2.2b set that stays as the frozen
record of the retired pair. The paper ships six tables and five figures. Everything
else is a supplementary pointer to the committed file, not a rendered artifact.

### Tables

| # | what it shows | why it earns the space | source |
| --- | --- | --- | --- |
| T1 | Population and split accounting: 26,939 blocks and 766,133 signatures down to 13,902 blocks and 197,479 test signatures, with both exclusions named and counted | A null result's first duty is to show nothing was dropped quietly | `reports/phase2e_boundary.md` population table, generated by `phase2e_run.py` |
| T2 | Two-sidedness: the retired pair at zero rule wins, the amended pair at 3,025 against 4,012, across k in {2, 3, 5, 10} and both metric arms | Carries the structural result and the repair in one object, and is the single most important table in the paper | `phase2e_twosidedness_eval.csv`, with the 2.2b zero from `phase2b_boundary.md` |
| T3 | Held-out accuracy, coverage and agreement per dataset, plus inspire alone and pooled non-inspire | Shows how close the mechanisms are, where they are not close, and how much of the pooled number is inspire | `phase2e_accuracy_by_population.csv` |
| T4 | Marginal pooled gap, interval, verdict at all three margins, and decided-winner rate, by ADS band and by SV band | The compression shape and the reason both hypotheses are Inconclusive, in one place | `phase2e_pooled_ads.csv`, `phase2e_pooled_sv.csv` |
| T5 | Decidability drivers: eta2_ADS against eta2_SV and the two averaged ranges, at each margin, with the block-weighted and ADS < 1.0 rows labelled as deciding nothing | The clause that tested the retired framing, reported as the measurement it is | `phase2e_driver_comparison.csv` |
| T6 | The falsification table evaluated: H1, H2, H3 with their deciding facts, plus margin sensitivity and k sensitivity | Lets a reader check every verdict against the frozen rule that produced it | `reports/phase2e_boundary.md` falsification section, `phase2e_margin_sensitivity.csv`, `phase2e_k_curve.csv` |

### Figures

| # | what it shows | why it earns the space | source |
| --- | --- | --- | --- |
| F1 | Per-block accuracy against ADS for both mechanisms | Establishes the signal is alive before the paper says it is useless for selection. Without this the null reads as a dead experiment | `phase2e_h1_ads_accuracy.png` |
| F2 | The 5 by 4 ADS by SV grid of pooled gap | The whole empirical half in one image: compression on both axes, sign change, and no cell far from zero | `phase2e_grid_gap_sv.png` |
| F3 | Decided-winner rate across ADS bands at fixed SV | The non-monotone gradient and the rise at ADS = 1.0 that the amendment predicted would fall to zero | `phase2e_decidability_gradient.png` |
| F4 | Verdict share against test-set size, tie and undecided kept apart | The honest power picture. A null paper that does not show this has not earned it | `phase2e_power_by_size.png` |
| F5 | The k curve: accuracy, two-sidedness and the driver clause across k | Ties the structural result to the design choice, and shows the conclusions do not rest on k = 5 | `phase2e_k_curve.png` |

### Named as supplementary, not shipped

Per-dataset H1 correlations (`phase2e_h1_spearman.csv`), the SV_resid and
Jaro-Winkler grids (`phase2e_pooled_cells_svr.csv`, `phase2e_pooled_cells_sv_jw.csv`,
`phase2e_grid_gap_svresid.png`), the INIT stratification
(`phase2e_pooled_init_sv.csv`), signal correlations
(`phase2e_signal_correlations.csv`), the regression summary
(`phase2e_regression.csv`), the per-block verdict distribution and the verdict
bar charts (`phase2e_verdicts_by_ads.png`, `phase2e_verdicts_by_sv.png`), the
decided-rate grid figure (`phase2e_grid_decided_sv.png`), the margin-sensitivity
figure (`phase2e_margin_sensitivity.png`), the regression check
(`phase2e_regression_check.csv`), the full 2.2b table set, the 2.2c candidate
comparison (`phase2c_pair_twosidedness.csv`, `phase2c_pair_regimes.csv`), and the
Phase 2.1 axis figures. Each is cited in the text by path where the claim it
supports is made. Robustness results are stated as numbers in section 7.5 rather
than given their own figures.

---

## Title candidates

**Superseded at Phase 2.5d, 2026-09-18. Kept, not deleted.** The title is final
and is not one of the six below:

> Prediction is not selection: a pre-registered study of design-time mechanism
> selection in entity resolution

It was set by the author, is the string in `paper/main.tex`, and PLAN.md carries
it under a "Title" heading with these six kept below it as the record of what was
considered. The list that follows is that record and is not a live choice.

Sentence case, no em dashes, matching the true finding. For the author to merge
with their own.

1. Nothing to select: a pre-registered null result for design-time mechanism
   choice in author name disambiguation.
2. Exact match is a sub-case of nearest-neighbour retrieval, and what that costs a
   mechanism comparison.
3. Two design-time signals, no decision: measuring before you build does not tell
   you what to build.
4. A comparison that cannot have a winner, and one that barely does: limits on
   design-time mechanism selection.
5. When the choice does not matter: rules against retrieval on seven real
   disambiguation datasets.
6. Measure your data first, then build what you like: a negative result on
   design-time mechanism selection.

Notes for merging. Candidate 2 leads with the structural result, which is the
most citable single sentence in the paper, but reads as a note rather than a
study. Candidate 1 is the safest for a venue that dislikes cute titles.
Candidates 3 and 6 carry the practitioner message and lose the structural half.
Deliberately avoided: anything containing "cascade", "selector", "gating",
"role", or "two-signal", all of which name the retired framing.

---

## Open inputs, to settle before or during drafting

1. **The primary margin stays delta = 0.05 unless review says otherwise.** The
   outline is written against the pre-registered margin, with 0.02 and 0.03 as
   the pre-registered robustness curve. Moving the primary margin after seeing
   which one has structure is exactly what the pre-registration exists to
   prevent, so if it moves it moves as a dated amendment and the paper says so.
   Drafting does not depend on the answer, but section 7.4 changes shape if it
   changes.
2. **Whether 2.3 and 2.4 happen at all.** The rewritten identity has no selector
   in it. If review wants the ADS-only and SV-only baselines run anyway as a
   negative control, section 8.4 becomes a short results subsection instead of a
   conditions list, and the budget takes about 400 words from sections 2 and 7.3.
3. **`phase2-spec.md` sections 7 and 9 still describe the selector and its
   success criteria.** They were out of scope for this pass. They should be
   rewritten or marked superseded before anyone reads them as live.
4. **Closed at Phase 2.6, 2026-09-21.** Citations were unverified as of this
   pass. The sweep has now run: block C of `references.bib` carries a DOI or a
   publisher URL per entry, and Tan (2026) was cut as unverifiable.

## Drafting order for 2.5b

Sections 4, 5 and 6 first, because they are the ones where the argument is fixed
and the prose is mostly transcription. Then 7, which is numbers and needs the
most care about verdict-versus-substance discipline. Then 3, 8 and 9. Then 1 and
2, which are easiest to write once the rest exists. The abstract last. Section
6.4 is reproduced from the locked text and is not drafted.
