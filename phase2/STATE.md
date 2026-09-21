# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2.7c complete. The manuscript prose has been rewritten
  against the committed 2.7b numbers. The title is changed, the abstract is
  rebuilt, block size is in the main text with both of its deflations, and the
  three integrity disclosures are in.** The manuscript builds clean. Nothing
  was measured this pass: every number added to the prose is cited from
  `reports/phase2_7b_reanalysis.md`, `reports/phase2e_boundary.md` or the
  committed tables. `PREREG.md` is untouched and no frozen result moved.
- **The title is now** "Prediction is not selection: a pre-registered study of
  design-time mechanism choice in author name disambiguation". Set in
  `paper/main.tex`, PLAN.md and here. The entity resolution width came out of
  the title and stayed in the paper: sections 1.2 and 1.4 still state the
  structural containment at entity resolution width and scope the empirical
  null to the author name disambiguation instance. This closes peer-review
  major 4 by the reviewer's own first option.
- **The scoping decision was taken and it is the one 2.7b handed up.** Every
  flat "no design-time signal is actionable" sentence is gone. The claim the
  paper now makes, in the abstract, in section 1.4, in section 8.1, in the
  limitations and in the conclusion, is that **neither pre-registered signal is
  actionable at the margin, and no design-time signal we examined tells a
  designer which mechanism resolves a name better**. Block size is reported in
  full as the exception that yields a decided verdict, and is then deflated by
  the two measured reasons. "Prediction is not selection" is unchanged as the
  thesis.
- **Block size is section 7.7, `sec:blocksize`, with Table 7.** (The peer
  review numbers the Results subsections 5.x and is one table off from 4
  onward; the numbers here are the ones the built PDF prints.) It states the
  two decided bands first (3-4 at -0.1145, 5-8 at -0.0712, both k-NN wins),
  then the composition result (no sign change at fixed ADS in either stratum,
  90.0% of the smallest band is ADS = 1.0 against 43.8% of the largest), then
  the abstention result (rule precision where it fires beats the vote in all
  seven bands, coverage climbing 0.8423 to 0.9827), then the reconciliation of
  the pooled -0.0050 with the 191/309 per-block count, then the distinction the
  whole subsection exists for: block size predicts which mechanism has the
  higher whole-set accuracy on small blocks, not which one resolves a name
  better, and the edge is a mechanical consequence of coverage against
  abstention that needed no measurement.
- **The body is well over budget and 2.7d has to trim it.** `texcount -inc`
  gives 13,263 text words against the pre-pass 9,537, so this pass added about
  3,700 words, and the page count went from 25 to 30. That was the instruction
  for 2.7c and it is the binding constraint on 2.7d. The likeliest trims are
  named under "Next" below.
- **Five of the eight peer-review majors are now closed in the prose.** Major 1
  (small-block sensitivity, in 7.4 and 7.6 and the Figure 2 caption), major 2
  (block size, section 7.7), major 3 (bootstrap interval in Table 5 and the
  scoping of "stable across k"), major 4 (the retitle), major 7 (the two
  delta = 0.02 reversals, in 7.5 and Appendix A). Major 8 is closed except that
  the ceiling column landed in Table 3 rather than a new table. Major 5 is
  closed by disclosure: the locked 6.4 quote is byte-identical and a fourth
  point of record below it states exactly what existed at `c20239a`. Major 6 is
  closed as prose by a fifth point of record naming the evidence as
  author-controlled git metadata; the deposit, push and tag are still open and
  are not writing items.
- **What 2.7c did not do, deferred to 2.7d by instruction.** The reference
  expansion and new citations; keywords, funding, competing interests and
  author contributions; the remaining formatting minors; the `/anti-ai` pass on
  the new prose; and the length trim. Also still open from the minors list:
  the Spearman population in 3.2, the "to every printed digit" phrasing in
  4.2, the
  six-decimal band edges, the runtime and hardware sentence, the Zenodo concept
  DOI verification, and the Figure 5 / Table 6 overlap.
- **No hypothesis verdict moved and none could.** H1 Supported, H2
  Inconclusive, H3 Inconclusive at the primary margin and Partial at
  delta = 0.02. The frozen falsification table, Table 6, is unchanged. Every
  supplementary analysis in the prose is labelled as supplementary and sits
  beside the frozen primary analysis rather than in place of it.
- **The one thing that gates a first upload is still not a manuscript edit.**
  `phase-2` has never been pushed, so the seven commit hashes in section 6.4
  and the availability statement both point at a repository that does not yet
  contain what the paper says it contains. Section 6.4 now says the repository
  will be pushed and tagged at release, which states the gap rather than
  closing it. **Do not upload before that push.**
- **Read this before anything else in 2.7d. Block size is a design-time signal
  with two decided pooled band verdicts at the primary margin.** Blocks of 3 to
  4 signatures give a pooled gap of -0.1145 [-0.1286, -0.1007] and blocks of 5
  to 8 give -0.0712 [-0.0807, -0.0614], both `k-NN wins` at delta = 0.05.
  Neither ADS nor SV has a single decided marginal band, which is the fact that
  carried H2 and H3 to Inconclusive. **Two measured qualifications sit beside
  it**: at fixed ADS the effect never changes sign, so it is gap compression
  and not a winner reversal, and the marginal reversal is composition; and the
  decided cells are an abstention effect, since the rule's precision where it
  fires beats the vote's accuracy in all seven bands, 0.9370 against 0.9037 in
  the smallest, while its coverage climbs from 0.8423 to 0.9827. **This is now
  written into the manuscript as section 7.7 and must not be trimmed away in
  2.7d.** The two deflations are what stop a reviewer saying a real selection
  signal was buried.
- **Three further 2.7b findings, all now in the prose.** (a) The H2 gradient's
  reported rise at ADS = 1.0 is a small-block artifact: the marginal decided
  rate runs 0.1083 / 0.0618 / 0.0256 / 0.0089 / 0.0278 frozen and
  0.1096 / 0.0443 / 0.0254 / 0.0089 / 0.0070 restricted, which is monotone, and
  the per-SV top-below-bottom count goes from 2 of 4 to 3 of 4. (b) The driver
  difference eta2_SV minus eta2_ADS is +0.2088 [+0.0628, +0.3473] at k = 5,
  +0.1840 [+0.0299, +0.3277] size-adjusted, and **+0.0474 [-0.2531, +0.3159] at
  k = 2, which straddles zero**, so "stable across k" is accurate for the
  verdict and not for the evidence. (c) The out-of-history accuracy ceiling is
  0.9586 pooled, and **it is not the main reason the datasets differ**: it
  closes only about 13% of the aminer-to-inspire spread. The rule's conditional
  precision is 0.8512 on 96.86% coverage against the vote's 0.8294.
- **The 2.7 peer review is the input to 2.7b and 2.7c and stays the checklist.**
  The report is `reports/phase2_7_peer_review.md`, with the same content as a
  `.docx` beside it. Twenty minors remain, most of them deferred to 2.7d.
- **Everything else the manuscript states still checks out.** The review
  re-derived every headline number from the committed CSVs and found no
  transcription error. Housekeeping is closed, the bibliography is verified,
  the affiliation is correct, the generative-AI disclosure and the data and
  code availability statement are in, and the build is self-contained. Phase
  2.3 stays blocked and, on the 2.5b negative control, has no selector left to
  build.
- **The build is self-contained and this was verified the way arXiv tests it.**
  The five PNGs live in `paper/figs/`, sha256-identical to `reports/figs/`, and
  `\graphicspath` is `{{figs/}}` with no `../` anywhere. `main.bbl` is
  committed and explicitly un-ignored, because AutoTeX does not run BibTeX.
  The 2.7c build adds no figure and no package, so the packaging is unchanged.
- **Four moderation findings stay open and are all submission-time decisions**,
  unchanged by 2.7 and 2.7c: the abstract's headroom, the `{,}` separators in
  the metadata abstract, the cs.LG cross-list question and the arXiv licence
  choice. The abstract is now 260 words against the 288 it was, which is closer
  to the 200-250 the venue class expects but is not inside it.
- **New at 2.6b and still true: the corresponding address is a personal Gmail
  account.** Fine in print, and it matters for the arXiv account. Registering
  an `adit.ac.in` or `cvmu.edu.in` address with arXiv, whatever the paper
  prints, is the cheapest remaining item and has the longest lead time.
- **The manuscript is at `phase2/paper/main.tex`**, with
  `phase2/paper/references.bib`. Venue-neutral LaTeX, generic `article` class,
  no journal style file. It now carries an appendix, Appendix A, which is new
  at 2.7c.
- **The pooled gap -0.0196 is a primary-analysis-population number**, settled
  at 2.5c against `reports/tables/phase2b_accuracy_by_population.csv`: 13,902
  blocks, 197,479 test signatures, exact 0.8244 against fuzzy 0.8441, exact
  coverage 0.9686, fuzzy coverage 0.9988, agreement 0.9698. The 0.9664 /
  0.9985 / 0.9679 triple that used to sit beside it in section 4.2 is the
  **whole evaluation split** (16,136 blocks, 199,713 signatures), which is
  also the population the zero `exact wins` count is measured on.
- **The two-signal role separation is retired.** The charter mission, PLAN.md's
  paper identity, its working titles, and `phase2-spec.md` sections 1 and 3 now
  describe a pre-registered negative result. Removed, not softened. `PREREG.md`
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
  That did not decide H2, because the power floor is evaluated first. It is the
  sharpest measurement in 2.2e at k = 5 and not across the k curve, which is
  how the manuscript now states it, and 2.5a retired the framing it tested.
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
- Per-block verdicts at delta 0.05: 0 exact wins, 298 fuzzy wins, 11,117 tie,
  2,487 undecided. **Corrected at 2.5b** from "302 / 2,483", which was a
  transcription error in this file. `reports/phase2b_boundary.md` and
  `reports/tables/phase2b_blocks_scored.csv.gz` both give 298 and 2,487. No
  report, table or manuscript number was affected.
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
- Pass 12 (Phase 2.5a): writing setup and outline. The paper identity rewritten
  to the true finding in the charter, PLAN.md and the spec; `reports/OUTLINE.md`
  built with section spines, an 8,100-word body budget, a six-table and
  five-figure plan, and six title candidates. Nothing measured. `PREREG.md`
  untouched.
- **Pass 13 (Phase 2.5b): the manuscript body drafted, in OUTLINE.md's order,
  one commit per block. Five tables and four figures placed. Section 6.4
  reproduces the locked deliverable verbatim and works its checklist against
  the committed repository, including commit ids and the
  amendment-predates-run timestamps. Section 7.7 states the logical negative
  control: no cell of the frozen grid is decided at the primary margin, so no
  selector over these two signals can beat a fixed choice, so none was built.
  Nothing measured. `PREREG.md` untouched.
- **Pass 14 (Phase 2.5c): two correctness fixes, then the `/anti-ai` pass,
  then the budget trim.** The pooled gap's population reconciled across
  section 4.2 and the Table 2 caption; the invoice-domain
  company-then-global fallback scoped in section 8.3; 22 anti-AI prose edits;
  section 2.3 cut entirely and section 7.3's prose cut to what Table 3 cannot
  say for itself, per OUTLINE.md's cut order. Four items flagged for 2.6 and
  not fixed. Nothing measured. `PREREG.md` untouched.**
- **Pass 15 (Phase 2.6): housekeeping closed, the verified bibliography in,
  the title's scope risk fixed, the moderation audit run and reported.** The
  five housekeeping items are done (affiliation, Tan removal, `n/a` cells,
  title period, OUTLINE banner); `references.bib` replaced and cite keys
  checked both ways; sections 1.2 and 1.4 rewritten so the structural result
  is stated at entity resolution width and the empirical null is stated as the
  author name disambiguation instance, which cost +198 body words. The
  moderation findings were surfaced, not fixed. Nothing measured. `PREREG.md`
  untouched. Folds in the 2.5d title micro-pass, which had no PASSLOG entry.
- **Pass 16 (Phase 2.6b): five moderation findings acted on, the build made
  self-contained.** Affiliation corrected from the wrong "Independent
  researcher" default to ADIT / CVM University; the author's generative-AI
  disclosure added verbatim and verified character for character; a data and
  code availability statement added naming the repository, the Zenodo concept
  DOI and S2AND's ODC-BY licence; the five figures copied to `paper/figs/` with
  `\graphicspath` made relative-downward, verified by an isolated flat
  directory build; `main.bbl` un-ignored and committed. No history rebased,
  squashed or amended, so section 6.4's hashes are intact. Nothing measured.
  `PREREG.md` untouched.
- **Pass 17 (Phase 2.7): the peer-review dry run.** The manuscript reviewed as
  an external artifact at Reviewer 2 severity, calibrated to a mid-tier Q2/Q3
  information science, IR or scientometrics venue class rather than a named
  journal. Every number checked against the committed reports and tables, not
  against the PASSLOG narrative. Eight majors, twenty minors, recommendation
  major revision needed, no fatal flaw. One claim found unsupported as
  written, two omissions found, no transcription error found. Report at
  `reports/phase2_7_peer_review.md` and `.docx`. The manuscript was not
  touched. Nothing measured. `PREREG.md` untouched.
- **Pass 18 (Phase 2.7b): the re-analysis of the frozen records.** Majors 1, 2,
  3 and 8 run together in one module on the committed per-block records, at the
  frozen seed, with no experiment re-run and no frozen definition altered.
  **This pass did measure**, which makes it the first since 2.2e, and
  everything it measured is supplementary or sensitivity analysis layered on the
  existing evidence base rather than a change to it. No H1, H2 or H3 verdict
  moves. One general claim does not survive: block size carries two decided
  pooled bands at the primary margin. Three further findings for the prose: the
  gradient's rise at ADS = 1.0 is a small-block artifact, the driver difference
  straddles zero at k = 2, and the out-of-history ceiling is not what separates
  the datasets. Report `reports/phase2_7b_reanalysis.md`, code
  `phase2/phase2_7b_reanalysis.py`, tables `reports/tables/phase2_7b_*.csv`,
  figures `reports/figs/phase2_7b_*.png`. The manuscript was not touched.
  `PREREG.md` untouched.

- **Pass 19 (Phase 2.7c): the prose pass.** The manuscript rewritten against
  the committed 2.7b numbers, citing that report's figures exactly and
  inventing nothing. The title changed to name the substrate, the abstract
  rebuilt to 260 words in one paragraph, block size written up as section 7.7
  with both of its deflations, the small-block sensitivity reported in 7.4 and
  7.6, the driver bootstrap added to Table 5 with "stable across k" scoped to
  the verdict, the accuracy accounting added to 7.3 and Table 3, the two
  delta = 0.02 reversals reported in 7.5 and Appendix A, and two new points of
  record added under the locked 6.4 quote, which was not edited. Seven minors
  taken. Nothing measured. `PREREG.md` untouched, no frozen result moved, no
  verdict changed. The body is about 3,700 words over where it started, which
  2.7d trims.

## Next: Phase 2.7d, the trim and the back matter

**2.7d is the next pass.** 2.7c added roughly 3,700 words and every one of them
was asked for. 2.7d pays for them and closes what was deferred, in this order.

1. **The trim, which is the binding constraint.** `texcount -inc` reads 13,263
   text words plus 226 in headers and 831 in float contents, against a charter
   ceiling of 10,000 for the prose total. The page count is 30. Roughly 3,500
   words have to come out and the pass should decide where before it starts
   cutting. Four places are the obvious candidates and none of them is section
   5.7:
   - **Section 6.4 is now five points of record** and is the longest
     subsection in the paper. The two new points are load bearing; the first
     three predate them and overlap the locked quote in places.
   - **Section 7.3 gained four paragraphs.** The conditional-precision and
     ceiling paragraphs are the substance; the kisti and inspire paragraphs are
     minors 8 and 9 and could each be a sentence.
   - **Section 8.3, the reinterpretation of the earlier synthetic study**, is
     about 700 words and was already over budget before this pass. Nothing in
     2.7c touched it beyond one clause.
   - **Section 2.3, the Kim and Kim comparison**, is minor 10 in the review:
     570 words on one prior paper inside the related-work section.
   - Minor 19 names the cheapest float cut: Figure 5 and Table 6 overlap, both
     carrying the k curve and the driver clause outcome.
   **Section 7.7 and its two deflations are not a trim target.** Reporting the
   block-size verdict without both measured qualifications is worse than not
   reporting it, because it reads as a buried selection signal.
2. **The reference expansion.** Seventeen references against the 40 to 70 the
   venue class expects (minor 11). The review's section 6 literature audit
   names the specific gaps. The retitle removes the sharpest version of this,
   since the paper no longer promises entity resolution width in its title, but
   the count is still thin.
3. **Front and back matter** (minor 2): keywords, funding statement,
   declaration of competing interests, author contributions. All four are
   standard in this venue class even for a single-author paper, and the
   generative-AI disclosure does not substitute for any of them.
4. **The remaining substantive minors**, none of which 2.7c took: the Spearman
   population in section 3.2 (minor 6), "to every printed digit" in 4.2
   (minor 5), the six-decimal band edges (minor 14), the runtime and hardware
   sentence (minor 16), the Zenodo concept DOI verification (minor 17), and the
   abstract's remaining length (minor 1, now 260 words against 200-250).
5. **An `/anti-ai` pass over the new prose, then a final rebuild.** About 3,700
   words were written this pass and none of them has been through that check.
   The locked 6.4 quote must be verified byte-identical afterwards, as at 2.5c.

**Three non-writing items are unchanged and two of them gate a first upload.**
Push `phase-2` and tag the state section 6.4 describes, because none of the
seven hashes resolves for a reader today and the manuscript now says in text
that the push will happen. Deposit the frozen `PREREG.md`, Amendment 1 and
Addendum 1a somewhere with a timestamp the author does not control, which is
what peer-review major 6 asks for and what the fifth point of record in 6.4
does not supply. And register an institutional email with arXiv, then open the
endorsement request for cs.DL; endorsement is the only item measured in weeks.

**Four moderation findings stay open and are all submission-time decisions**,
unchanged by 2.7c: the abstract's headroom, the `{,}` separators in the
metadata abstract, the cs.LG cross-list question and the arXiv licence choice.

## Superseded: Phase 2.7c, the prose pass (done at Pass 19)

**Superseded at Phase 2.7c, 2026-09-21. Kept, not deleted, as the record of
what the pass was asked to do.** The pass ran and the section above is what is
live now. All six items below were taken. Item 1, the scope decision, was taken
first as instructed and is recorded under "Where we are".

1. **The scope decision, which is the author's and blocks the rest.** It is now
   two decisions fused into one, because 2.7b's block-size result landed on the
   same sentences major 4 does. The abstract, the title and section 8.1
   generalize to "design-time mechanism selection fails" and "prediction is not
   selection". Block size is a design-time signal with two decided pooled bands
   at the primary margin, so either every general sentence gets scoped to the
   two pre-registered signals, or the block-size result and its two
   qualifications go in the main text and the general sentence stands with them
   attached. Major 4's retitle question rides on the same paragraphs. **Decide
   this before writing anything else.**
2. **Major 1 reporting.** Section 5.4 and Figure 2 need the size-1 and size-2
   rows and the note that the size-1 stratum cannot produce an undecided
   verdict by construction.
3. **The gradient sensitivity.** The H2 discussion needs the finding that the
   reported rise at ADS = 1.0 is a small-block artifact, which strengthens the
   H2 paragraph rather than weakening it.
4. **Major 3 reporting.** Table 4 needs the bootstrap interval, and section
   5.6's "stable across k" needs scoping to the verdict with k = 2 named as the
   weak end.
5. **Major 8 reporting.** Table 3 or the population table needs the ceiling
   column and section 5.3 needs the rule's conditional precision, with the
   caveat that the ceiling is **not** what separates the datasets.
6. **Majors 5 and 7, which 2.7b did not touch.** Major 5 is a fourth point of
   record under the locked quote naming what did exist at `c20239a`. Major 7 is
   two sentences or an appendix table for the two delta = 0.02 reversals.

## Superseded: Phase 2.7, the peer-review dry run (done at Pass 17)

**Superseded at Phase 2.7, 2026-09-21. Kept, not deleted, as the record of what
the pass was asked to do.** The pass ran and the section above it is what is
live now. The three places this section pointed the reviewer at were all read:
section 4 landed, section 6.4 did not survive intact (major 5), and section 8.3
drew no major. Read below for what was asked, not for what to do next.

**2.7 is the next pass.** Run the manuscript through a simulated peer review
and act on what it returns. Nothing outstanding blocks a review read: the paper
builds clean, the citations are verified, the scope is stated, and the two
back-matter statements are in. The three places 2.5c asked for a hostile read
are still the three places worth the reviewer's attention, and they are listed
under the held-over section below.

**Two slow things are worth starting in parallel, because neither is writing.**
Push `phase-2` and tag the state section 6.4 describes, which closes the last
self-containment finding without touching a commit hash. And register an
institutional email with arXiv, then open the endorsement request for cs.DL.
Endorsement is the only item here measured in weeks.

**The body-length decision is now the binding constraint, not a tidiness
question.** Counting the two back-matter statements inside the prose total puts
it at 9,985 against the charter's 10,000 ceiling: fifteen words of headroom.
Counting them outside it, which is the usual convention for availability and
disclosure statements, puts it at 9,770. Either way, **2.7 cannot add a word
without cutting one**, and a peer-review pass usually wants to add. Decide
before 2.7 runs whether back matter counts, and which of sections 4, 6, 7 and 8
may be cut into.

**Four moderation findings stay open and are all submission-time decisions**,
not manuscript edits: the abstract's 154 characters of headroom, retyping the
`{,}` separators for the plain-text metadata field, whether cs.LG is worth
requesting as a cross-list beside cs.IR (cs.DB may fit better), and which arXiv
licence to select.

The review of the draft that 2.5c asked for is still worth doing and was not
part of 2.6 or 2.6b. It is preserved below and feeds directly into 2.7.

## Held over from 2.5c: review the edited manuscript, and decide the body length

**Closed at Phase 2.7, 2026-09-21, except the body-length decision. Kept, not
deleted.** The hostile read this section asks for was done at Pass 17 and its
output is `reports/phase2_7_peer_review.md`. The three named places were all
read against the committed reports, which is what this section asked for. The
body-length decision is still open and is now listed under the 2.7b section
above, where it is binding.

The draft should be reviewed
against the committed reports rather than against the PASSLOG narrative.

**The one decision 2.5c hands up.** The body is about 9,150 words against an
8,500 target. Sections 4, 6, 7 and 8 are all over their outline budget and
2.5c cut none of them, because three of the four are the sections listed
below as the ones whose landing review has to judge. Either accept the
length, or name which sections may be cut into.

Read `phase2/paper/main.tex`, and the Pass 14 diff for the prose changes.
Three places are worth an independent, hostile read, in this order.

1. **Section 4, a comparison that cannot have a winner.** The whole paper
   rests on this landing as a contribution rather than as a note. It carries
   the containment argument, the measured zero, and the general form for any
   pair assigning from the block's own history. If it does not land, the paper
   is thinner than the outline assumed and that is worth knowing now.
2. **Section 6.4 and its three points of record.** The locked deliverable is
   reproduced verbatim; the three points after it work its fill-at-writing
   checklist against the committed repository, covering the two dated appends
   behind "amended once", what the two runs before the amendment actually
   were, and the amendment-predates-run claim against commit timestamps. This
   is the integrity argument and it has to survive a reviewer who is looking
   for the seam.
3. **Section 8.3, the reinterpretation of the Phase 1 synthetic result.** It
   reinterprets published work of the author's own. The line between what was
   an artifact of the near-nested pair, what stands, and what is intact but
   narrower has to be exactly right, and the containment there is close rather
   than exact, which the section says. 2.5c also scoped the
   company-then-global fallback there to the earlier study's invoice domain.

Two prose changes are worth checking on their own terms. Section 4.2 now
opens by naming two populations before giving any number, which has to read
as a clarification and not as hedging. Section 10's second paragraph was a
chronological recap of all four claims and is now a synthesis that separates
the structural half from the empirical one, so check that nothing load
bearing was lost with the recap.

Then settle the three open inputs still open in `reports/OUTLINE.md`, listed
again under "Still open" below. **Tan (2026) is the one that now blocks
finalization**: it is cited by PLAN.md and by `phase2-spec.md` section 1 as the paper's
sibling in framing, and no bibliographic details for it exist anywhere in the
repository. Either it gets verified or the sibling framing comes out of the
spec, PLAN.md and the abstract's surrounding argument.

Then Phase 2.6, the pre-submission gate: the citation verification sweep over
`paper/references.bib` block C, the four items 2.5c flagged and listed under
"Open decisions", and the `affiliation` column question the S2AND README
raises.

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

Settled at Phase 2.5b:

- **The selector text is marked superseded, not deleted**, in `phase2-spec.md`
  sections 7 and 9, charter invariant 4, and the last clause of charter
  invariant 6. Each carries a dated banner and keeps its original text, and
  each becomes live again unchanged if 2.3 runs. This closes OUTLINE.md open
  input 3.
- The manuscript title supplied at 2.5b was a placeholder. **Superseded: the
  title is final as of 2.5d, see below.**

Settled at Phase 2.5d:

- **Superseded at Phase 2.7c, 2026-09-21: the paper was retitled to
  "Prediction is not selection: a pre-registered study of design-time
  mechanism choice in author name disambiguation", on peer-review major 4.
  Kept, not deleted, as the record of the 2.5d decision.** The title was
  set by the author and no longer a candidate:
  "Prediction is not selection: a pre-registered study of design-time
  mechanism selection in entity resolution." It is the string in
  `paper/main.tex` and in PLAN.md, which now carries it under a "Title"
  heading with the six superseded candidates kept below it as the record of
  what was considered. `reports/OUTLINE.md` still lists those six as
  candidates and was not edited; read PLAN.md for the decision.
- **The title names entity resolution, which is broader than the substrate,
  and that is deliberate but load-bearing.** The empirical work is on seven
  author name disambiguation datasets and the abstract names them in its
  second sentence, so the scope is stated where a reader meets it first. The
  structural result is what earns the wider word: it holds for any pair of
  mechanisms assigning from the record's own history. A reviewer who reads
  "entity resolution" and then finds only author names is the risk to watch,
  and sections 1.2 and 1.4 are where the scoping has to hold.

Flagged at Phase 2.5c for the 2.6 gate, not fixed:

- **The Zenodo DOI for the earlier study.** `references.bib` gives
  `adscascade2026` the DOI `10.5281/zenodo.21644207` with a note that version
  1.0.0 is archived at `10.5281/zenodo.21644208`. Which is the concept DOI
  and which the version DOI is unverified against Zenodo. Section 8.3 is the
  only place it is cited.
- **Section 6.4's commit hashes: checked at 2.5c and they hold.** All seven
  resolve on `phase-2` and their subject lines match the roles 6.4 assigns
  them, in order. The timings check too: `5f452ad` 12:36:16, `3e79a48`
  13:04:42, `9e3d921` 14:25:07 on 2026-09-18, giving 1h49m for "just under
  two hours", 1h20m for "about eighty minutes" and 28 minutes for "within
  half an hour". Left open only because they are short hashes in published
  text and would need re-checking after any rebase.
- **Tan (2026): verify or drop.** Unchanged from 2.5b, restated below.
- **Settled at 2.6b: the author affiliation.** 2.6's "Independent researcher"
  was a wrong default and is gone. `\author{}` now carries the Department of
  Information Technology, A. D. Patel Institute of Technology (ADIT), Charutar
  Vidya Mandal (CVM) University, New Vallabh Vidyanagar, Anand, Gujarat, India,
  with `maitreyasapariya@gmail.com` as the corresponding address and the ORCID.
  Set from the author's own string. `CITATION.cff` still carries no affiliation
  and could be brought into line at the release pass.
- **Settled at 2.6b: the generative-AI disclosure.** The author's statement is
  in the manuscript verbatim, as `\section*{Generative-AI disclosure}` after
  the conclusion, verified character for character against the supplied text.

Still open:

- **Body length, and 2.6 moved it the wrong way on purpose.** About 9,150 body
  words against an 8,500 target on the Pass 14 counter, with sections 4, 6, 7
  and 8 all over budget. 2.5c cut sections 2.3 and 7.3 and stopped there. 2.6
  then added 198 words to section 1 for the instructed scope fix, measured on
  one counter across both versions so the delta is sound even though its
  absolute reads about 190 lower than Pass 14's. Prose total is still under the
  charter's 10,000 ceiling. Page count went 23 to 24.
- **Is delta = 0.05 still the primary margin?** Unchanged by this pass, and the
  outline is written against it. Every marginal pooled gap on both axes falls
  below it, so the power floor decides both hypotheses before any substantive
  rule is read, and delta = 0.02 is where the data has structure. Moving it now,
  after seeing that, is the move the pre-registration exists to prevent. It is a
  decision to take explicitly and record as a dated amendment, or to decline
  explicitly. It is not a decision to slide into.
- **Whether 2.3 and 2.4 happen at all.** The rewritten identity has no selector
  in it, and 2.5b narrowed this further: manuscript section 7.7 states the
  logical negative control, that no cell of the frozen grid is decided at the
  primary margin, so no selector reading ADS and SV can beat a fixed choice.
  If 2.3 runs anyway it runs as an empirical confirmation of that, not as a
  constructive contribution.
- **Closed at 2.6: Tan (2026) is removed.** It was unverifiable, so the entry,
  the section 2.1 TeX comment and the sibling framing in PLAN.md and
  `phase2-spec.md` are all out, each removal leaving a dated note.
  `PREREG.md` and `phase2d-prereg-revision.md` still mention it and were not
  touched; they are frozen records.
- **New at 2.6: the generative-AI disclosure.** The manuscript makes no
  statement about generative-AI use and the repository's commits carry
  `Co-Authored-By: Claude`. arXiv expects authors to disclose it. This is a
  decision about what, if anything, the paper says, and it is the author's.
- Whether the "strictly lower in the top ADS band than in the bottom" clause
  should be pinned to one construction. It cost nothing this time and will not
  always.
- Whether a third mechanism enters at all. Charter invariant 6 keeps it out
  unless it is actually implemented and evaluated.

## Live risks

- **New and top at 2.7: the per-block winner construct is degenerate at one
  test signature.** The paired bootstrap over a single test signature is a
  point mass, so the interval is [0,0], [+1,+1] or [-1,-1] and such a block can
  never be `undecided`. `phase2e_power_by_size.csv` confirms it: the size-1
  stratum has undecided exactly 0.0 at all three margins. 278 of the 500
  decided verdicts and 1,130 of the 10,172 demonstrated ties come from blocks
  with one or two test signatures, and the decided-winner rate is what H2's
  whole apparatus, including the driver comparison, is computed over. Confirmed
  in code at `phase2b_core.py:246`. This is a re-analysis on existing records,
  not a re-run.
- **New at 2.7: one manuscript sentence is not supported by the repository.**
  Section 6.4's locked quote says no k-nearest accuracy figure existed when the
  amended hypotheses were written. `c20239a` at 12:09:23 committed
  `phase2c_pair_twosidedness.csv` (pooled accuracy at every k) and
  `phase2c_pair_regimes.csv` (the per-cell ADS by SV grid whose shape the
  amended hypotheses predict), 27 minutes before the amendment at 12:36:16.
  `PREREG.md` states the scoped version correctly and the manuscript states it
  correctly elsewhere; the quote is where the qualifier is missing. This is the
  single most checkable weakness in the paper.
- **New at 2.7: the unit of analysis is not settled.** Pooled over signatures
  the vote is ahead by 0.0050; per block the rule takes 191 wins to the vote's
  309, but the vote wins no block at all above 32 test signatures while the
  rule wins 30 there. The regression's +0.0208 on log test-set size is the same
  fact. Block size is readable at design time and was never registered as a
  signal, so the general claim "no design-time signal" outruns the two signals
  actually tested.
- **The paper is a null result and has to read as a contribution rather than as
  a failed experiment.** Still the dominant framing risk, and 2.7 answers the
  question 2.5b could not: **section 4 lands.** The simulated review called the
  structural result "the best thing in the paper", correct as stated, with its
  scope conditions named precisely, and confirmed its general form against
  `phase2c_pair_regimes.csv` for all three candidate pairs. The 41% figure
  reproduces exactly. What the review disputes is not whether section 4 is a
  contribution but whether the title's "entity resolution" is earned by it.
- **Retired at 2.6: the unverified citations.** Block C is verified, every
  entry resolves by DOI or publisher URL, and the one placeholder is removed.
  The charter's "every citation verified and resolvable" rule is met.
- **Narrowed at 2.6b and still the top risk: the repository the paper points
  at does not yet contain the paper's evidence.** Section 6.4's integrity
  argument turns on seven short commit hashes, and captions name fifteen
  repository artifacts. All 22 resolve locally. 2.6b added the availability
  statement, so the paper now names `github.com/stiFFLer-codes/ADS-Cascade`
  and says the Phase 2 code and pre-registration will be public there at
  release. **`phase-2` is still unpushed**, so that sentence is a promise and
  the hashes still resolve nowhere. The strongest part of the paper's defence
  remains unverifiable by the people it is written for until the push happens.
  **This gates the upload.** The fix is a push plus a tag, never a rebase: the
  hashes are in published text and 2.6b was instructed to leave history alone.
  **Widened at 2.7 into review major 6.** The review adds two points the push
  alone does not answer: git timestamps and history are author-settable, so the
  ordering evidence is attested by the party it exculpates, and the whole cycle
  from `8869b82` at 01:32:56 to `9e3d921` at 14:25:07 is thirteen hours of one
  day. The recommended fix is an independent timestamp for the frozen
  `PREREG.md`, Amendment 1 and Addendum 1a, on OSF, AsPredicted or a dated
  Zenodo deposit, cited from section 6.4, or one sentence there conceding that
  the ordering evidence is author-controlled.
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
phase2/reports/OUTLINE.md (what the paper will be) ->
**phase2/paper/main.tex (what the paper now is, drafted at 2.5b)** ->
**phase2/reports/phase2_7_peer_review.md (what an external reviewer says about
it, and what 2.7b has to answer)** -> phase2/PASSLOG.md (history).
