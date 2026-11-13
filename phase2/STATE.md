# Phase 2 state

Single current-status file. Read this first every session, right after the
charter. Updated at the end of every phase. History lives in PASSLOG.md, the
full arc in PLAN.md, the method in phase2-spec.md.

## Where we are

- Status: **Phase 2 released as v2.0.0 on 2026-11-13. Complete.** Markie
  pushed `main` and the tags, and `v2.0.0` (`9e4df78`) is the citable
  release, DOI `10.5281/zenodo.24184394`. GitHub, Zenodo and Software
  Heritage all carry it, and the Zenodo related works are fixed. The root
  `README.md` now holds the approved public text, in one commit past the
  tag, which goes out when Markie pushes `main`. Phase 2 has no other next
  step. See PASSLOG Pass 29.
- Previous status, **Phase 2 manuscript and repository complete, 2026-11-13 (gate 2.9e,
  master plan WO-6 and WO-6b). The release gate is next.**
  The release wording, the DOI `10.5281/zenodo.24184394`, the landing page and
  the paper PDF are committed, and the verifier's eight open items are cleared.
  The PDF is `paper/main.pdf`, 31 pages, sha256
  `b06ff412c0e09366c55a5b168996e6874fc2c90cf65a67eebe75762e55914cac`. Do not
  rebuild it for the release. The locked quote is unchanged (`dcaa1bc…f8f4`).
  See PASSLOG Pass 28.
- Previous status, **Gate 2.9d done, 2026-11-12 (master plan WO-5 and WO-5b). Runbook
  steps 1 to 3 are next, then WO-6.** An independent verifier checked the
  paper and repository at `26bf2e9` and changed nothing. The number ledger has
  829 rows: 801 matched, 26 arithmetic, 2 unmatched. Of the plan's findings,
  25 are fixed, 1 is in `ERRATA.md` and 2 are scheduled for WO-6. A3, A4, A5,
  A6, A7, B5 and C4 pass. Eight items are still open, all minor, and all go
  to WO-6. The report is `reports/phase2_9d_verifier.md` and the ledger is
  `reports/tables/phase2_9d_number_ledger.csv`. See PASSLOG Pass 27.
- Previous status, **Gate 2.9c complete, 2026-11-12 (master plan WO-4 and WO-4b). WO-5,
  the independent verifier, is next.** A cold run from a fresh clone, with no
  cache, reproduced all 108 compared output files in content, re-derived the
  frozen record, and built the paper at 31 pages. The raw S2AND path also
  reproduced. The report is `reports/phase2_9c_cold_run.md`. `README.md` now
  carries this run's step times and the five README fixes it found. Still to
  fill in: `<DOI>` (WO-6). See PASSLOG Pass 26.
- Previous status, **Gate 2.9c done, 2026-11-12 (master plan WO-3, with the WO-3b
  review fixes). WO-4, the cold run from a fresh clone, is next.** Commit
  `47c6cb3` added the release files: `README.md`, `requirements-lock.txt`,
  `DATA_LICENSES.md`, `ERRATA.md`, the root `LICENSE-TEXT`, and dated notes in
  the charter, PLAN and STATE. The next commit removed the deprecated earlier
  tree from the tip. The root now holds only `.gitattributes`, `.gitignore`,
  `CITATION.cff`, `CLAUDE.md`, `LICENSE`, `LICENSE-TEXT`, `README.md` and
  `phase2/`, and history keeps the rest. Still to fill in: `<cold run>` times
  in `README.md` (WO-4) and `<DOI>` (WO-6). See PASSLOG Pass 25.
- Previous status, **Phase 2.9b step 2 complete, 2026-11-12 (master plan WO-2 and the
  WO-2b review fixes). The manuscript now says only what the 2.9a and 2.9b
  records support; WO-3, the release files, is next.** Changed: `paper/main.tex`,
  `paper/references.bib`, `paper/main.bbl`. The build is clean, at 31 pages,
  and the locked 6.4 quote is byte-identical (sha256 `dcaa1bc…f8f4`). No
  hypothesis outcome moved. What changed in the paper:
  1. **The per-dataset result is in** (N3 (a)). New subsection 7.8 "Two
     datasets are not like the pool" (`sec:per-dataset`): kisti `rule wins`
     through matching and zbmath `k-NN wins` through abstention, plus the
     pooled non-inspire reversal at 0.05. Every "no signal" and "only signal"
     claim is now scoped to the seven-dataset pool.
  2. **"Cannot have a winner" is gone** (N4 (a)). Section 4 is "A comparison
     only one side can win", and section 5 is "A pair either side can win".
     The containment states its identity condition. The second structural
     region is narrowed to surface-only mechanisms.
  3. **Section 6.4 now has eight points of record.** New ones cover the
     `a41a67a` insertion, the calibration split's three uses, "any similarity
     function", and the run timing from local file times. The "external read"
     is named as a simulated peer review.
  4. **Smaller fixes.** The matched precision margin is 0.0153. The contested
     share is 42.2% on the evaluation split. Experiment 1 is 115 of 120. The
     S2AND redistribution is disclosed with attribution. The earlier study is
     cited at v1.1.0 and marked deprecated. The AI disclosure is widened.
- Previous status, **Phase 2.9b step 1 complete, 2026-11-12 (master plan WO-1). Every
  number the manuscript edits need is now in committed tables; the manuscript
  edits (WO-2) are next, after the author rules on decisions N3 and N4.** One
  new script, `phase2_9b_supplement.py`, six `reports/tables/phase2_9b_*.csv`,
  `reports/phase2_9b_report.md` and `reports/phase2_9b_reflog_phase2.txt`.
  Nothing in `paper/`, `PREREG.md` or any existing script, report, table or
  figure moved. Not pushed, tagged or released. What it found, all at
  delta = 0.05 unless stated:
  1. **The pooled null is mostly one dataset's (W2).** kisti as a whole is
     `rule wins`, +0.1131 [+0.1015, +0.1250]. zbmath as a whole is `k-NN wins`,
     -0.0631 [-0.0761, -0.0512]. pubmed (34 blocks, not a qualifying dataset)
     is `rule wins`, +0.2466. Inside kisti, SV high (+0.1654), ADS [0, 0.5)
     (+0.1762) and [0.5, 0.7) (+0.1100) are `rule wins`. Pooled non-inspire
     has a winner reversal across ADS at fixed SV high: [0, 0.5) +0.0629 and
     [0.5, 0.7) +0.1024 `rule wins`, against ADS = 1.0 -0.1130 `k-NN wins`.
     Its marginal SV-high band is `rule wins` by 0.0001 on the lower bound
     (0.0501). Without kisti, every non-inspire ADS band below 1.0 and every
     SV band is a tie.
  2. **INIT (W1).** The INIT bands on their own are all ties. The `rule wins`
     cell INIT = 0 x SV high (+0.1363) is kisti's: 3,781 of 4,746 test
     signatures at +0.1698, and +0.0052 (a tie) without kisti. The `k-NN wins`
     cell INIT >= 0.5 x SV = 0 has zero rule-right-vote-wrong signatures.
  3. **Experiment 1 (W8).** 115 of 120 clean conditions have the interval
     inside +-0.02, read from the `v1.1.0` tag. The count is now committed code.
  4. **Run timing (O3).** On local file times, which are not repository
     evidence, the evaluation predictions were first cached at 13:27:30, 23 min
     after Addendum 1a. No trace puts them earlier.
- Previous status, **Phase 2.9a complete, 2026-11-12. The release pass has started.
  2.9a gathered the facts the manuscript edits need and committed one
  analysis script; 2.9b, the manuscript edits, is next.** The paper is
  declared complete and goes public on GitHub plus a **new** Zenodo record.
  There is no journal and no arXiv, so the arXiv and venue items below are
  moot, and the charter's word ceiling is not enforced for this release, both
  by the 2.9 brief. 2.9a made new files only: `phase2_9a_matched.py`, three
  `reports/tables/phase2_9a_*.csv` and `reports/phase2_9a_report.md`. Nothing
  in `paper/`, `PREREG.md` or any existing report, table or figure moved. Not
  pushed, tagged or released.
- **What 2.9a found that the paper has to absorb**, all in
  `reports/phase2_9a_report.md` with evidence:
  1. "Where the rule commits it is the more accurate arm by 0.0218" uses
     mismatched denominators. On the same fired items the margin is **+0.0153
     [+0.0142, +0.0165]**. It is positive in all seven block-size bands and all
     seven datasets.
  2. Section 4.3's "where the history is written one way, no mechanism can
     win ... a tie by construction" is **false as written**. In SV = 0 the rule
     never beats the vote (0), but the vote beats the rule on 696 signatures,
     all of them abstentions on unseen forms. The rule cannot win there; the
     vote can.
  3. The containment wording ("any similarity function") needs the maximum to
     be attained only at identity. That holds for the two functions used
     (0 of 210,537 distinct-form pairs score 1.0) and fails for rapidfuzz's
     token and partial ratios. main.tex:722 sits inside the locked quote.
  4. Section 8.3's "demonstrated equivalent there" fails for 5 of the 120
     clean Experiment 1 conditions.
  5. The evaluation-split contested share is 42.2%, against the calibration
     figure of 41%.
  6. `a41a67a`, the post-freeze PREREG edit, came before any calibration or
     evaluation number on every trace. The paper does not mention it.
  7. The runs were CPython 3.14.2, with no scientific package changed since
     2026-09-18.
- Previous status, **Phase 2.8a complete. The citations are locked, the H1 figure is
  back, the paper states its contributions on page 3, and the moderation audit
  has been re-run.** 27 pages, 25 references and every one of them verified,
  zero undefined citations, zero undefined references, zero LaTeX warnings,
  zero em dashes in the source and in the rendered PDF. Nothing was measured.
  No number new to the paper was written and none was removed, checked by
  diffing every numeric token against the pre-pass file. `PREREG.md`
  untouched, no frozen result moved, no verdict changed, and the locked 6.4
  quote is byte-identical (sha256 `dcaa1bc…f8f4`, computed over
  `\begin{quote}` through `\end{quote}` plus the trailing newline).
- **The eight Block E citations are verified and locked.** Every `note =
  {Unverified, verify at review}` is gone from `references.bib`, `main.bbl` and
  the PDF. Fields are the values the author confirmed externally, and all eight
  DOIs were also resolved against Crossref this pass, which agrees with them
  field for field, including the six-author AutoBlock list and the nine-author
  Mudgal list. Two deliberate departures from raw Crossref metadata, recorded
  in the bib header: Crossref spells the last AutoBlock author "Davd", a typo
  for David Page, and gives Lakens as Dani\"el, which the bib keeps although
  the confirmed list wrote it in ASCII. AutoBlock's arXiv pointer went with
  its note field. **The charter's "every citation verified and resolvable"
  rule is met again.**
- **The H1 figure is restored as Figure 1, by author decision; the
  decidability gradient stays cut, also by author decision.** The restored
  caption corrects what the old text said about the plot: it is a line plot of
  mean per-block accuracy by ADS band, not a per-block scatter, and its top
  band, where the rule sits below the vote, is explained by pointing at the
  section 4.3 argument rather than by a new number. It costs one page, 26 to
  27. **The 2.7d typographic changes (`\parskip` 0pt, the tightened
  `\bibsep`, the loosened float fractions) were not addressed at 2.8a and
  stand.** They belong to the venue-specific trim, since a venue style file
  sets its own.
- **The paper now says what it contributes, early and in one place.** A new
  section 1.4, "Contributions", lists four: the structural result and its
  unreachable-verdict consequence, with the AutoBlock precedent conceded inside
  the item; the pre-registered study, with both hypotheses named Inconclusive;
  the block-size deflation, with "did not pre-register" inside the item; and
  the cautions for portfolio and benchmark design, including the calibration
  trap. Five further framing edits: "avoids both problems" in the abstract and
  1.3 became "in which neither mechanism contains the other", because no pair
  avoids the general form's empty regions; the abstract's "the same statistic",
  which since 2.7c read as block size predicting accuracy, became "the
  consistency statistic"; 4.3's "a theorem anyone needs" and 8.1's "most of
  what this paper has to offer" were restated without underselling. Report:
  `reports/phase2_8a_moderation_audit.md`.
- **Five flags for human review, none acted on because each needs new analysis
  or changes a claim.** F1 is the one that matters: **section 5.2 overstates
  the calibration trap for the k-nearest family.** It says accuracy
  calibration "selects the degenerate parameter" in either family; that is
  exact for the radius vote (r = 0.95, rule-side count 0) but on the k grid it
  selects k = 2, still two-sided at 181/736 on calibration and 987/3,990 on
  evaluation. The overstatement is inherited from `phase2c_pair_design.md`.
  F2, the 41% contested-region figure is calibration-split only; F3, the entity
  resolution width would become a demonstration with one non-AND benchmark;
  F4, the calibration trap is not in the abstract because it would push the
  abstract past 250 words; F5, section 4 could be set as a proposition with a
  proof. Details in the audit report.
- **Length.** 27 pages. `texcount -inc` 12,375 text words, 230 in headers, 692
  in captions, so the prose total is 13,297 against the charter's 10,000, up
  353 on 2.7d: about 270 for the contributions list and 56 for the restored
  caption. **The word-ceiling question now folds into the venue-specific
  trim**, which is where a venue's own limit replaces the charter's.
- **Abstract** 249 words, 1,565 characters with the one `{,}` retyped, against
  arXiv's 1,920. Peer-review minor 1's 200-250 band still holds.
- **The seven section 6.4 commit hashes all still resolve on `phase-2`**, each
  an ancestor of the branch tip, with subjects matching the roles 6.4 assigns
  them: `8869b82` 01:32:56, `5e13e38` 10:46:50, `3d86959` 11:43:11,
  `c20239a` 12:09:23, `5f452ad` 12:36:16, `3e79a48` 13:04:42, `9e3d921`
  14:25:07, all on 2026-09-18. No history was rebased, squashed or amended.
- **No hypothesis verdict moved and none could.** H1 Supported, H2
  Inconclusive, H3 Inconclusive at the primary margin and Partial at
  delta = 0.02.
- **The one thing that gates a first upload is still not a manuscript edit.**
  `phase-2` has never been pushed, so section 6.4's hashes and the
  availability statement point at a repository that does not yet contain what
  the paper says it contains. **Do not upload before the release pass.** Not
  pushed, tagged or released this pass, by instruction; the availability
  statement stays in the future tense until then.
- **The manuscript is at `phase2/paper/main.tex`**, with
  `phase2/paper/references.bib` and the committed `phase2/paper/main.bbl`,
  regenerated this pass with 25 `\bibitem`s. Venue-neutral LaTeX, generic
  `article` class, no journal style file, one appendix.
- **Two PNGs in `paper/figs/` are unused by the build**
  (`phase2e_decidability_gradient.png`, `phase2e_k_curve.png`). An isolated
  AutoTeX-style build with only the three used figures, `main.tex` and
  `main.bbl` came out clean, so both can be left out of the tarball.
- **Open moderation items, all submission-time and none acted on:** the one
  `{,}` separator in the metadata abstract; the cross-list, where cs.DB is now
  better supported than cs.LG because the paper cites the entity resolution
  literature; the arXiv licence; and the ORCID on the arXiv account.
- **Still true from 2.6b: the corresponding address is a personal Gmail
  account.** Fine in print, and it forecloses arXiv's automatic endorsement.
  Registering an `adit.ac.in` or `cvmu.edu.in` address with arXiv is the
  cheapest remaining item and has the longest lead time.
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

*Dated note, 2026-11-12 (gate 2.9c). The paragraph above is kept as written.
"At every k" should read "at k = 3, 5 and 10; split at k = 2"
(`reports/phase2e_boundary.md:296`). See `ERRATA.md`, entry 1, which also lists
the other governance statements the later record narrows.*

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

- **Pass 20 (Phase 2.7d): citations, declarations, trim and polish.** Eight
  references added and flagged unverified, keywords and three declarations
  added, the manuscript trimmed from 30 pages to 26, nine peer-review minors
  closed, the Zenodo concept DOI verified against the Zenodo API, and
  `/anti-ai` run over the new and revised prose. Nothing measured, `PREREG.md`
  untouched, no frozen result moved, no verdict changed, the locked 6.4 quote
  byte-identical and all seven of its commit hashes still resolving. Three
  changes go beyond the instruction and need sign-off: two extra float cuts and
  two typographic settings.

- **Pass 21 (Phase 2.8a): citation lock, figure restore, and a
  contribution-and-moderation scan.** The eight Block E citations set to the
  author's confirmed values and cross-checked against Crossref; the H1 figure
  restored with a corrected caption; a contributions subsection and five
  framing edits; the arXiv moderation audit re-run over its seven dimensions,
  with five flags for review and every submission-time item left alone.
  Nothing measured, no number new to the paper, `PREREG.md` untouched, the
  locked quote byte-identical, all seven hashes resolving. Not pushed, tagged
  or released.

- **Pass 22 (Phase 2.9a): release-pass facts and the like-for-like precision
  comparison.** This pass was read-only fact-gathering on:
  - the a41a67a edit;
  - section 8.3 against the Experiment 1 paper;
  - the section 4.3 region;
  - the containment condition;
  - the sources for five numbers;
  - the WDC gates;
  - seven Crossref GETs;
  - the interpreter and packages;
  - quotes of minors 10 and 20 and flags F1 to F5.

  It also added `phase2_9a_matched.py`, which halts unless the frozen
  population reproduces, and three tables. Report:
  `reports/phase2_9a_report.md`. Not pushed, tagged or released.

- **Pass 23 (Phase 2.9b step 1, master plan WO-1): per-population verdicts, the
  INIT control cells, and the Experiment 1 interval count.** One new script,
  `phase2_9b_supplement.py`. It halts unless the frozen population reproduces
  and checks every `all` row against the committed pooled tables. It writes six
  tables and a report whose last section, the local file times for the 2.2e
  run, is hand-written. Also the phase-2 reflog, with one line withheld for a
  scan-term match. No existing file changed. Not pushed, tagged or released.

- **Pass 24 (Phase 2.9b step 2, master plan WO-2 and WO-2b): the manuscript
  corrected against the 2.9a and 2.9b records.** Edits E1 to E20, the
  overrides O-E1 to O-E20 and the review fixes R1 to R14, in `paper/main.tex`
  and `paper/references.bib`, with `main.bbl` regenerated. Every added number
  is listed with its source table in the PASSLOG entry. No script, report,
  table, figure or `PREREG.md` changed. Not pushed, tagged or released.


## Next: WO-3, the release files, then the release

0. **Done at Pass 24:** the manuscript edits (item 1 below) are applied,
   following master plan WO-2 and the orchestrator's overrides and review
   fixes. Next is WO-3: `phase2/README.md`, the requirements lock, the data
   licences, `ERRATA.md`, and the Phase 1 tip deletion. The WO-6 items (the
   6.4 push sentence and the tense of the availability paragraph) wait for
   the DOI. Q3, on why kisti differs, is still open.
0. **Done at Pass 23:** every number the edits need is in committed tables
   (`reports/phase2_9b_report.md`), including the 115/120 count. The edits
   follow the master plan's WO-2, once the author has ruled on N3 and N4.
1. **2.9b, the manuscript edits.** These are written by the orchestrating
   chat from `reports/phase2_9a_report.md`. The facts are gathered. The
   decisions are the author's: how to disclose `a41a67a` in 6.4 and its
   footnote, how to word the "external read", the matched margin, and the
   narrower 4.3 region-2 sentence. Also the containment condition (with
   main.tex:722 locked), the 8.3 (j) sentence, the 42.2% figure, F1, the
   S2AND redistribution sentence (main.tex:1672), and the citation of the
   earlier study by version DOI. Numbers for the paper come from committed
   tables only. The 115/120 Experiment 1 count needs a committed script
   first.
2. **The release itself, after 2.9b.** The recon (one level above the root,
   `RECON_ads_cascade_2026-11-12.md`, section 8) sets out the push and tag
   with no rebase, a new separate Zenodo record rather than a version under
   concept 21644207, and the front-door files. The availability statement
   moves to the present tense once the push is real.


## Superseded: the release pass and venue trim as planned at 2.8a (split at Pass 22)

**Superseded at Phase 2.9a, 2026-11-12. Kept, not deleted, as the record of
what was planned.** Under the 2.9 brief, items 3 (venue trim) and 4 (arXiv
mechanics) are moot and the word ceiling is not enforced. Item 2 is carried
into the section above. "Cut Zenodo v2" there is replaced by a new Zenodo
record, per the recon. Read below for what was planned, not for what to do
next.

**Two passes remain and neither is prose revision.** 2.8a closed the last
manuscript item that blocked submission, the unverified citations.

1. **Decisions for review first.** Whether section 5.2's calibration-trap
   sentence is narrowed to what the k grid shows (flag F1 in
   `reports/phase2_8a_moderation_audit.md`), and whether any of F2 to F5 is
   wanted. F1 is a claim edit and is the author's call; F2 and F3 need new
   analysis.
2. **The release pass.** Push `phase-2` and tag the state section 6.4
   describes, a push plus a tag and never a rebase, because the hashes are in
   published text. Cut Zenodo v2 from that tag. Move the availability
   statement to the present tense once the push is real. Deposit the frozen
   `PREREG.md`, Amendment 1 and Addendum 1a with a timestamp the author does
   not control and cite it from section 6.4 (peer-review major 6). Leave
   `phase2e_decidability_gradient.png` and `phase2e_k_curve.png` out of the
   upload tarball, and ship `main.bbl` in it. `CITATION.cff` can gain the
   affiliation here.
3. **The venue-specific trim**, once a venue is chosen. It absorbs the
   charter's word-ceiling question (13,297 prose words against 10,000), the
   2.7d typographic settings, and whether the calibration trap goes into the
   abstract (flag F4).
4. **arXiv mechanics, in parallel and started first.** Register an
   institutional address, then request cs.DL endorsement; it is the only item
   measured in weeks. At submission: retype the one `{,}` in the metadata
   abstract, choose the cross-list (cs.IR, and cs.DB over cs.LG), choose the
   licence, and attach the ORCID to the account.


## Superseded: Phase 2.8 as planned at 2.7d (split at Pass 21)

**Superseded at Phase 2.8a, 2026-09-23. Kept, not deleted, as the record of
what was planned.** 2.8 was split: 2.8a took item 4 (citations) and the
float half of item 1 (the author restored the H1 figure and kept the gradient
cut), and folded the word-ceiling half of item 1 into the venue-specific
trim. Items 2, 3, 5, 6 and 7 are carried into the section above. Read below
for what was planned, not for what to do next.

**2.8 is the next pass, and almost none of it is writing.** The manuscript is
submission-shaped: 26 pages, 25 references, clean build, declarations in, the
peer-review minors closed. What is left is the repository, the record and the
account.

1. **Two decisions for review, at the top of the pass, before anything else.**
   Whether the three changes 2.7d made beyond its instruction stand: the two
   extra float cuts (the H1 scatter and the decidability gradient), the zeroed
   `\parskip`, and the tightened `\bibsep` with the loosened float fractions.
   And whether the charter's 10,000-word prose ceiling is enforced or formally
   relaxed to the page count, since the manuscript is at 12,944 and closing
   that gap means removing argument rather than wording. Both decisions are the
   author's and both change what 2.8 does.
2. **Push and tag `phase-2`.** This is the only thing that makes section 6.4's
   seven commit hashes and the availability statement true for a reader, and it
   gates the upload. A push plus a tag, never a rebase: the hashes are in
   published text.
3. **Deposit the frozen `PREREG.md`, Amendment 1 and Addendum 1a** somewhere
   with a timestamp the author does not control, on OSF, AsPredicted or a dated
   Zenodo deposit, and cite it from section 6.4. This is peer-review major 6,
   and section 6.4's fifth point of record currently concedes the gap rather
   than closing it.
4. **Verify the eight Block E citations** against DOI and venue records, to the
   standard Block C was held to at 2.6, and clear the `Unverified, verify at
   review` notes as each one passes. This blocks submission, not the upload.
5. **arXiv mechanics.** Register an institutional address, then open the cs.DL
   endorsement request; endorsement is the only item measured in weeks. Then
   the three remaining moderation decisions: the `{,}` separators in the
   plain-text metadata abstract, whether cs.LG or cs.DB is worth requesting as
   a cross-list beside cs.IR, and the arXiv licence.
6. **Trim the upload bundle.** Three PNGs in `paper/figs/` are no longer
   referenced by the build. Decide whether they ship.
7. **Housekeeping, only after review.** `CITATION.cff` still carries no
   affiliation and could be brought into line with the manuscript's. The
   charter's final cleanup pass for stale repo files is still unscheduled.


## Superseded: Phase 2.7d, the trim and the back matter (done at Pass 20)

**Superseded at Phase 2.7d, 2026-09-21. Kept, not deleted, as the record of
what the pass was asked to do.** All five items were taken. The trim reached
26 pages rather than the 10,000-word ceiling this section assumed, and how it
got there is set out under "Where we are". Read below for what was asked, not
for what to do next.


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

- **Closed at 2.7d: the Zenodo DOI for the earlier study is verified.** The
  Zenodo REST API gives `10.5281/zenodo.21644207` as the concept DOI
  (`conceptrecid` 21644207), currently resolving to v1.1.0 at
  `10.5281/zenodo.22258609`, and `10.5281/zenodo.21644208` as v1.0.0.
  `references.bib` and the availability statement already said that, so no
  text changed; the check is recorded as a comment in the bib. Peer-review
  minor 17 closed.
- **Section 6.4's commit hashes: re-checked at 2.7d and they hold.** All seven
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

- **Body length, restated at 2.7d and now the open decision rather than the
  open task.** The page target is met at 26. The charter's prose ceiling is
  not: 12,079 text words plus 229 headers and 636 captions is 12,944 against
  10,000. 2.7c added about 3,700 words on instruction and 2.7d took about
  1,200 back out; the remaining four pages came from three floats and from
  typography. Closing the word gap means cutting argument rather than wording,
  and the candidates are named under "Where we are". **The decision for review
  is whether the ceiling is enforced or formally relaxed to the page count.**
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

- **New at 2.8a: section 5.2 states the calibration trap more strongly than
  the k grid supports.** "Selects the degenerate parameter and walks the design
  straight back into a comparison that cannot have a winner" is exact for the
  radius vote and not for the k-nearest vote, where accuracy calibration picks
  k = 2 and k = 2 is still two-sided (987 against 3,990 on evaluation, in the
  paper's own Table 2). A reviewer who reads Table 2 against section 5.2 will
  find it. Flag F1; a claim edit, so left for the author.
- **Retired at 2.8a: the unverified references.** All eight Block E entries
  are verified and locked, and the note fields are gone. Kept below as the
  record.
- **New and top at 2.7d: eight of the twenty-five references are unverified.**
  Block E of `references.bib` was added this pass on instruction and every
  entry says so in its own `note` field. Author lists, page ranges, volume
  numbers and DOIs in that block are plausible reconstructions, not checked
  records, and one of them (`kim2019`) was chosen from the peer review's search
  directions rather than from a verified citation. The charter's "every
  citation verified and resolvable" rule is **not** met while Block E stands,
  and a wrong DOI in a submitted manuscript is the cheapest possible way to
  lose a reviewer's trust. Verify all eight before submission.
- **Updated at 2.8a: the page count is now 27 and the prose total 13,297,
  33% over the charter ceiling.** The H1 figure's page came back and the
  contributions list added about 270 words. The rest of this entry stands and
  the question moves to the venue-specific trim.
- **New at 2.7d: four of the six pages cut did not come out of prose.** Two
  came from removing the H1 scatter and the decidability-gradient figures, one
  from zeroing `\parskip`, one from tightening `\bibsep` and loosening the
  float fractions. The manuscript is 26 pages and 12,944 prose words, so a
  venue that counts words rather than pages will see a paper 29% over the
  charter's own ceiling. Reversing any of the typographic changes, or a venue
  style file that sets its own, puts pages back.
- **Settled at 2.8a by the author: the H1 figure is restored and the
  decidability gradient stays cut.** The entry below is the record.
- **New at 2.7d: two figures were cut that nobody asked to cut.** The
  instruction authorized one float cut and the pass made three. The two extra
  are defensible on the merits, since both plotted numbers the text states in
  full and both PNGs remain in the repository, but they are the pass's own
  judgement rather than a reviewer's or the author's, and they are the first
  thing to reverse if review disagrees.
- **New at 2.7: the per-block winner construct is degenerate at one
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
it, and what 2.7b has to answer)** ->
**phase2/reports/phase2_8a_moderation_audit.md (the current moderation state
and the five flags awaiting review)** -> phase2/PASSLOG.md (history).
