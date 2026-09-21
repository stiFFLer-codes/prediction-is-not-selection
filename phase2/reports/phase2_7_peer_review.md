# Simulated peer review, Phase 2.7

**Manuscript:** "Prediction is not selection: a pre-registered study of
design-time mechanism selection in entity resolution"
(`phase2/paper/main.tex`, at commit `00dcf04`, 2026-09-21)

**Target:** not a named journal. Calibrated to a mid-tier (Q2 or Q3) information
science, information retrieval or scientometrics journal, the realistic target
class named by the author.

**Article type:** original research, empirical, with a structural (analytic)
component. No EQUATOR reporting standard applies.

**Severity register:** Harsh ("Reviewer 2"), at the author's request.

**Reviewer note.** This is a simulated review produced to help the author
self-check before submission. It is not a journal decision. Every number quoted
below was checked this session against the committed reports, tables and code in
`phase2/reports/` and `phase2/`; where a claim could not be supported by those
artifacts, the artifact and the line are named so the author can check the
finding rather than take it on trust.

---

## 1. Summary of the manuscript

The paper asks whether a practitioner can measure a property of their own data
before building anything and learn from it which of two classification
mechanisms to build. It answers no, for two reasons the paper keeps carefully
apart. The structural reason is a containment argument: a rule that assigns on
an exact surface match is a strict sub-case of a retriever that assigns from the
single nearest surface form, because an identical string sits at the maximum of
any normalized similarity function, so the rule cannot be correct where the
retriever is wrong and the verdict "the rule wins" is unreachable at any cutoff
and in any metric family. The paper reports that it measured exactly zero rule
wins across 199,713 held-out signatures in two metric arms while executing a
pre-registered analysis, and generalizes the argument to any pair of mechanisms
that assigns an entity from a record's own history: such a pair cannot be
contested where the history names one author, and cannot be contested where the
history carries one surface form. The empirical reason comes from a redesigned,
genuinely two-sided pair, an exact-evidence rule against a k-nearest vote at
k = 5, run on seven S2AND author name disambiguation datasets under a
pre-registration that was amended once, before the reported run, after the
containment was discovered. Over 13,902 held-out blocks the two mechanisms
differ by half an accuracy point, 0.8244 against 0.8294. The gap compresses and
changes sign along both design-time axes, consistency (ADS) and surface
variability (SV), but no band clears the pre-registered five-point margin, so
both selection hypotheses return Inconclusive on the pre-registered power floor,
while the same consistency statistic predicts each mechanism's own accuracy at
Spearman 0.51 and 0.83. One pre-registered clause comparing the two signals as
drivers of decidability found surface variability the stronger, against the
amendment's expectation. No selector was built, and the paper argues logically
that none could beat a fixed choice where no grid cell is decided.

## 2. Overall assessment

### Strengths

- **The structural result is correct and it is the best thing in the paper.**
  The containment argument in section 4.1 is valid as stated, the scope
  conditions are named precisely (single-nearest, shared candidate pool, shared
  tie-break), and the general form in 4.3 is checked in the committed
  calibration-split probe: for the adopted k-nearest pair, the rule-wins count
  is exactly zero in all four cells of the ADS = 1.0 row and in all five cells
  of the SV = 0 column, and the same two lines of zeros appear for the radius
  and normalized-key pairs (`phase2c_pair_regimes.csv`). The 41% contested-region
  figure reproduces exactly from that file (14,680 of 35,732 held-out
  signatures). This is a real, cheap, transferable check and the paper is right
  to lead with it.
- **The order of discovery is genuinely to the paper's credit.** The degeneracy
  was found in an empty cell of a frozen analysis output, not derived and then
  confirmed, and the paper says so rather than tidying the narrative. The zero
  is documented in `phase2b_boundary.md` line 39 and was not withdrawn when the
  design changed.
- **The four-verdict winner construct is the right instinct.** Keeping
  "demonstrated tie" apart from "undecided" is exactly what a paper made mostly
  of ties needs, and section 3.3 says why in one clear paragraph. See Major 1
  for where the implementation does not deliver on it.
- **Internal numerical consistency is unusually good.** I re-derived the
  population table, the pooled non-inspire row, the pooled accuracy from the
  per-dataset rows, the agreement identity in 4.2, the decided-verdict sum
  (191 + 309 + 10,172 + 3,230 = 13,902), the H1 coefficients, the band gaps and
  decided rates, the driver table, the regression coefficients and the k curve.
  All of them reconcile to the committed CSVs. I found no transcription error.
- **The reinterpretation of the author's own earlier synthetic study
  (section 8.3) is honest and well calibrated**, including the concession that
  the containment there is close rather than exact and the separation of what is
  an artifact from what stands.

### High-level concerns

- The per-block winner construct is degenerate on small test sets, and the
  affected blocks carry a majority of the paper's decided verdicts and a
  substantial share of its demonstrated ties (Major 1).
- Test-set size, which the paper's own regression makes the second strongest
  correlate of the per-block gap, is never treated as a candidate design-time
  signal, and it splits the per-block and pooled pictures in opposite directions
  (Major 2).
- The driver comparison, billed as the sharpest measurement in the run, is a
  comparison of two point statistics over twenty unweighted cells with no
  interval and no size adjustment (Major 3).
- "Entity resolution" in the title is carried entirely by an argument, and the
  paper cites no entity resolution literature (Major 4).
- One sentence of the locked pre-registration quote is checkably stronger than
  what the repository supports (Major 5), the pre-registration record is
  author-controlled and same-day (Major 6), and the repository the integrity
  argument depends on is not public (Major 6).
- Two winner reversals that exist in the committed output at delta = 0.02 are
  absent from the manuscript, while delta = 0.02 is used elsewhere when it
  supports the paper's reading (Major 7).

### Headline recommendation

**Major revision needed.** There is a publishable paper here for this venue
class, and I would want to see it again. There is no fatal flaw: the structural
result stands on its own, the data and code exist, and every fix below is a
re-analysis or a rescoping rather than a redesign. But several of the paper's
load-bearing quantities do not currently survive a hostile read, and the title
promises more than the evidence delivers.

---

## 3. Major comments

### Major 1. The per-block winner construct is degenerate on small test sets, and this contaminates the counts the paper leads with

**Location:** section 3.3 ("What it means to win a block"), section 5.4
(per-block verdicts), Figure 2, and `phase2b_core.py:246` (`block_bootstrap_ci`).

Section 3.3 makes an explicit virtue of separating a demonstrated tie from
insufficient evidence, and says that merging them "is how a low-powered study
comes to read as a positive finding of equivalence." The implementation does not
deliver that separation at the small end. The per-block interval is a paired
bootstrap over the block's test signatures, resampled as a multinomial over the
three per-signature outcomes {+1, 0, -1}. For a block with one test signature
the distribution is a point mass: the interval is [0, 0] when the two mechanisms
agree, and [+1, +1] or [-1, -1] when they do not. Such a block can never be
"undecided". It is recorded either as a *demonstrated tie* on the strength of a
single item, or as a decided winner on the strength of a single item.

This is visible in the committed output. In `phase2e_power_by_size.csv`, the
test-set-size-1 stratum holds 1,309 blocks and its undecided share is exactly
0.0 at all three margins, which no other stratum comes close to. Working the
shares back to counts:

| Test-set size | Blocks | Rule wins | k-NN wins | Tie | Undecided |
|---|---|---|---|---|---|
| 1 | 1,309 | 14 | 165 | 1,130 | 0 |
| 2 | 2,159 | 10 | 89 | 1,739 | 321 |

So **278 of the paper's 500 decided per-block verdicts (55.6%) come from blocks
with one or two test signatures**, and 165 of the k-nearest vote's 309 per-block
wins come from blocks with exactly one. **1,130 of the 10,172 demonstrated ties
are single-item blocks** where "demonstrated" carries no information at all.
The decided-winner rate is the dependent variable of the entire H2 apparatus:
resolution 4 of Amendment 1 defines decidability through this per-block verdict,
and the driver comparison of section 5.6, Table 4 and Figure 4 are all computed
over it. They are therefore computed over a quantity that is, for a quarter of
the analysis population, an artifact of a degenerate interval.

The population table already excludes block-size-2 blocks as a named exclusion
because "consistency is 1.0 by construction" there. The same logic applies with
more force to a block whose *test* half holds one signature, and those blocks
were not excluded.

**Suggested action.** Re-run the per-block verdict analysis with a minimum
test-set size (three is the natural floor, since the bootstrap interval is still
coarse at two), report it as a sensitivity analysis rather than as a change of
primary analysis, and state what happens to the decided-winner rate, the
gradient, and the eta-squared comparison under it. If the conclusions are
unchanged, that is a strong paragraph. If the gradient in Figure 4 flattens, the
reader needs to know. At minimum, add the size-1 and size-2 rows of the table
above to section 5.4 and annotate Figure 2 to say that the size-1 stratum cannot
produce an undecided verdict by construction.

### Major 2. Test-set size is the design-time signal the paper did not register, and it splits the per-block and pooled pictures in opposite directions

**Location:** section 5.3 (head to head), section 5.5 (the regression),
section 5.4, section 8.1, abstract, title.

The compact regression of the per-block gap reports a coefficient of +0.0208
(s.e. 0.0018, t = 11.9) on log test-set size, which the paper prints and then
sets aside as something that "summarizes the grid and decides nothing." Over the
realized range this is not small. Across roughly two orders of magnitude of
test-set size it spans about 0.10 accuracy points, twice the primary margin,
and it comfortably exceeds SV's contribution over SV's realized range
(0.0548 x roughly 0.4 = 0.022). Only ADS is larger.

This is not an incidental covariate, for two reasons.

First, it is available at design time. Test-set size is roughly 0.3 times block
size under the paper's own split rule, and block size is read off the history
before anything is built. It therefore satisfies exactly the criterion
section 3.1 sets for a design-time signal, and it was not among the two signals
pre-registered.

Second, it reverses the paper's headline depending on the unit of analysis.
Pooled over signatures the k-nearest vote is ahead by 0.0050. Per block, working
the shares in `phase2e_power_by_size.csv` back to counts, the rule takes 191 wins
against the vote's 309, but the vote's wins are entirely concentrated in small
blocks and the rule's are not:

| Test-set size | Rule wins | k-NN wins |
|---|---|---|
| 1 | 14 | 165 |
| 2 | 10 | 89 |
| 3-4 | 14 | 17 |
| 5-8 | 42 | 23 |
| 9-16 | 42 | 10 |
| 17-32 | 39 | 5 |
| 33-64 | 26 | 0 |
| 65+ | 4 | 0 |

**Above 32 test signatures the vote wins no block at all, and the rule wins 30.**
A designer choosing a mechanism for a corpus of large blocks and a designer
choosing for a corpus of small blocks are being given the same answer by this
paper, and the data does not say the same thing to them.

The consequence for the claims is the part that matters. The abstract, the title
and section 8.1 generalize to "design-time mechanism selection fails" and
"prediction is not selection". What the evidence supports is that *neither of
the two pre-registered signals* is actionable at delta = 0.05 for this pair.
Section 1.4 does some of this scoping well and should be commended for it, but
the abstract, section 8.1 and the conclusion do not inherit it, and the paper's
own regression names a third candidate it never evaluated.

**Suggested action.** Either (a) add block size as a third design-time signal
and report the same band analysis for it, which needs no new computation since
the per-block records already exist, or (b) scope every general statement about
"no design-time signal" to the two signals actually tested, in the abstract and
conclusion as well as in section 1.4. Whichever is chosen, report the per-block
verdict table above in the main text and reconcile it with the pooled headline
in one paragraph. This is currently the paper's largest unexploited finding as
well as its largest exposure.

### Major 3. The driver comparison is billed as the sharpest measurement in the run and carries no uncertainty and no size adjustment

**Location:** section 5.6 and Table 4; Addendum 1a in `PREREG.md`.

Section 5.6 calls this "the sharpest single measurement in the run" and the
retirement of the paper's earlier framing turned on it. What is actually
reported is a comparison of two point statistics, eta-squared 0.1749 for ADS
against 0.3837 for SV, computed as a one-way decomposition over the twenty
eligible cells of the frozen grid, each cell contributing one unweighted
observation. No interval, no test, no sampling distribution. Everything else in
the paper is bootstrapped; this quantity is not.

Three specific reasons the comparison needs an error bar before it can carry
this much weight.

- **SS_total is 0.0401** over twenty points whose values run from 0.0000 to
  0.1971 (`phase2e_driver_comparison.csv`, `phase2e_pooled_cells_sv.csv`). Five
  of the twenty cells have a decided rate of exactly zero. A single cell moving
  by a few hundredths moves the decomposition materially.
- **The cells are unweighted by design and vary from 43 to 3,922 blocks.** The
  addendum argues the unweighting well, and I accept the argument, but the
  consequence is that the noisiest cells carry the same weight as the
  best-estimated ones and no one has quantified how much noise that is.
- **The axes are not balanced on test-set size, which drives decidability.**
  Mean test signatures per block in the SV = 0 cells run 3.3, 4.2, 6.4, 15.4 and
  20.5; in the SV-high cells they run 12.1, 16.7, 20.2, 29.6 and 47.0. Given
  Figure 2, decidability is a function of test-set size, so part of what
  eta-squared attributes to SV may be attributable to how large the blocks in
  each SV band are. I checked the simple version of this at cell level and the
  Spearman between cell mean test size and cell decided rate is only 0.14, so
  the confound is not overwhelming, but it has not been addressed at all and the
  paper does not currently let a reader rule it out.

The stability claim also reads stronger than the table supports. At k = 2 the
two values are 0.3277 and 0.3751 (`phase2e_k_curve.csv`), a gap of 0.047 against
0.209 at k = 5, and that is the k at which the clause splits rather than fails.
"Stable across k" is defensible for the verdict; it is not accurate for the
magnitude.

**Suggested action.** Bootstrap the difference eta2_SV - eta2_ADS by resampling
blocks, and report the interval in Table 4. Add a size-adjusted variant (either
partialling log test-set size out of the cell rates, or restricting to cells of
comparable mean size) as a labelled diagnostic in the same table. Then calibrate
the prose: "the sharpest single measurement in the run" is a strong phrase to
attach to an unbounded point comparison.

### Major 4. "Entity resolution" in the title is carried by an argument, and the paper cites no entity resolution literature

**Location:** title; sections 1.2, 1.4, 4.3, 7.2, 10; the reference list.

The author already knows this is the exposed flank, and sections 1.2 and 1.4 do
about as good a job of scoping it as prose can. It is still not enough, for a
reason that is not about wording.

Every measurement in the paper is on seven author name disambiguation datasets.
The entity resolution width is carried entirely by the structural argument, and
that argument is stated, developed and demonstrated in author-block vocabulary
throughout: blocks, signatures, surname-sharing, the block's history, the
author's identifier. Section 4.3 asserts the general form covers "any pair of
mechanisms that assigns an author drawn from the block's own history" and then
demonstrates it on the same author-name substrate as everything else.

The reference list makes this worse rather than better. Seventeen entries, and
not one of them is from the entity resolution or record linkage methods
literature: no probabilistic record linkage foundation, no entity resolution
monograph or survey, no blocking survey, no benchmark-evaluation study, none of
the deep entity matching line. Section 1.2 dismisses "clean product-matching and
record-linkage benchmarks" as having a point-mass consistency axis without
citing a single one, which a reviewer from that community will read as an
assertion about their field made without engaging it. That community is
precisely who the title recruits.

**Suggested action.** Two coherent options, and I would take the first.

1. **Retitle to the substrate and keep the wider claim inside the paper.**
   Something on the order of "Prediction is not selection: a pre-registered
   study of design-time mechanism selection in author name disambiguation",
   with the abstract's opening paragraph stating that the structural half is an
   argument about entity resolution generally. The paper loses nothing it has
   evidence for and the mismatch disappears.
2. **Earn the width.** Cite the entity resolution literature properly, restate
   the containment once in entity-resolution vocabulary (records, a candidate
   set drawn from a blocking key, a similarity join) rather than only in AND
   vocabulary, and run the one-count check on one non-AND public matching
   benchmark. That last item is cheap, and the paper itself says so: "The check
   is cheap. Before running the comparison, count the items on which mechanism A
   is correct and mechanism B is not." A single additional corpus with a zero in
   that cell would convert the title from a promise into a demonstration.

Note also that the 41% contested-region figure quoted in 4.3 and 7.4 is from the
calibration split, and the same quantity on the evaluation split is computable
and is what a reader will assume they are being given.

### Major 5. One sentence of the locked pre-registration quote is checkably stronger than the repository supports

**Location:** section 6.4, inside the quoted block: "No accuracy figure for the
k-nearest mechanism existed at the time the amended hypotheses were written; the
amendment predates the run it governs."

Taken without qualification this is not what the repository shows.
`phase2c_pair_twosidedness.csv` and `phase2c_pair_regimes.csv` were committed in
`c20239a` at 12:09:23 on 2026-09-18. The amendment is `5f452ad` at 12:36:16, 27
minutes later. Those two files contain, for the k-nearest vote at k = 2, 3, 5
and 10: its pooled accuracy on the calibration split (0.8390, 0.8354, 0.8290,
0.8188), its two-sidedness counts, and its per-cell accuracy gap against the
rule across the same five-by-four ADS-by-SV grid that the amended H2 and H3 are
written over. Those per-cell gaps already show the compression-and-sign-change
shape the amended hypotheses go on to predict: at k = 5, +0.0576 in
[0, 0.5) x SV-high against -0.0526 at ADS = 1.0 x SV = 0.

The properly scoped version of the claim is in the repository and is correct.
Amendment 1 itself says "No mechanism B prediction **on the evaluation split**
has been computed, scored, or printed", and the paper's own third point of
record says the second pre-amendment run "was exploratory by construction: a
design probe confined to the calibration split, producing no evaluation-split
number." The quoted sentence drops the qualifier that makes it true, and it is
the sentence a hostile reader will pull out, because the calibration-split grid
is not merely an accuracy number, it is a preview of the pattern the amended
hypotheses assert.

I recognise the quote is locked deliberately, and that locking it was the right
call. That does not make it immune to correction.

**Suggested action.** Keep the quote locked and add, immediately below it, a
fourth point of record that states plainly what did exist at 12:09:23: the
calibration-split accuracies, the two-sidedness counts, and the per-cell grid,
with the two filenames and the commit id. Say explicitly that the amended
hypotheses were written with the calibration-split grid in view, that the
calibration split is reserved for design choices by the original
pre-registration and is never used for a reported hypothesis number, and that
the evaluation split was untouched. That is a stronger defence than the current
unqualified sentence, because it is the one that survives being checked. A
bracketed editorial insertion inside the quote ("[on the evaluation split]")
would be an acceptable alternative if the author prefers to correct in place and
footnote the insertion.

### Major 6. The pre-registration record is author-controlled, same-day, and currently unverifiable by any reader

**Location:** section 6.4 and its footnote; section 9, "Data and code
availability".

Section 6.4's integrity argument rests entirely on seven short commit hashes in
a git repository the author owns. Three observations that a reviewer will make
and the paper does not pre-empt.

- **The whole cycle is thirteen hours of one day.** `8869b82` freezes the
  pre-registration at 01:32:56 and `9e3d921` is the reported run at 14:25:07,
  both on 2026-09-18. The timings the paper quotes all check out exactly
  (amendment to run 1h48m51s for "just under two hours", addendum to run
  1h20m25s for "about eighty minutes", amendment to addendum 28m26s for "within
  half an hour"). But a pre-registration and its amendment and the run it
  governs all inside one working day is a procedural artifact of a single
  session, not a commitment separated in time from the analysis, and the paper
  invites the comparison by using the vocabulary of pre-registration without
  qualification.
- **Git timestamps and history are author-settable.** Commit dates can be set
  arbitrarily and history can be rewritten. The paper's ordering evidence is
  therefore attested by the party it exculpates. Nothing here suggests it was,
  and the 2.2e regression check against frozen 2.2c counts is a genuinely good
  independent control which the paper is right to cite. But the paper should say
  what the evidence is and is not.
- **No reader can check any of it today.** `phase-2` has no upstream
  (`git branch -vv` shows no tracking branch; `origin` holds only `main`). None
  of the seven hashes resolves for anyone but the author, and section 9 says the
  code "will be public at release". For a submitted manuscript, an integrity
  argument whose whole content is "check these commits" and a repository that
  does not contain them is the weakest possible combination.

**Suggested action.** Before submission, deposit the frozen `PREREG.md` as it
stood at `8869b82`, and the amendment and addendum as they stood at `5f452ad`
and `3e79a48`, with a timestamp the author does not control: OSF or AsPredicted
is the convention in this literature, and a dated Zenodo deposit of the
pre-amendment tree would also do. Cite the deposit in section 6.4. Push the
branch and tag it so the hashes resolve, and change section 9 from "will be
public at release" to a statement of fact. If for any reason the external
deposit does not happen, add one sentence to section 6.4 saying that the
ordering evidence is author-controlled git metadata, and let the reader weigh
it. The paper is otherwise scrupulous about naming what its evidence cannot do,
and this is the one place it is not.

### Major 7. Two winner reversals present in the committed output at delta = 0.02 are missing from the manuscript

**Location:** section 5.5, final paragraph ("Robustness, gathered in one
place"); section 5.5, "Below ADS = 1.0 there is no SV-driven winner reversal at
any margin"; `phase2e_boundary.md` lines 443-455 and 533-539.

The paper uses delta = 0.02 freely when it supports its reading: the marginal
ADS reversal in 5.5, the "different position" paragraph in 7.1, and the H3
Partial verdict. It reports the INIT stratification and the fixed-SV grid at
delta = 0.05 only. The committed report contains, at delta = 0.02, two results
that are the strongest positive structure anywhere in the run and neither
appears in the manuscript:

- **Across ADS bands at fixed SV = high, a full winner reversal**:
  [0, 0.5) rule wins, [0.5, 0.7) rule wins, [0.7, 0.9) tie, [0.9, 1.0) tie, and
  1.0 k-NN wins (`phase2e_boundary.md` line 455). Three decided bands of
  opposite identity, which is the paper's own definition of a reversal.
- **Across SV bands inside INIT = 0, a winner reversal**: SV = 0 k-NN wins,
  SV high rule wins (line 537). Section 5.5 says only that "Inside the INIT
  bands the shape survives as a tie-crossing at INIT = 0 and at INIT >= 0.5",
  which is the delta = 0.05 reading, and does not say it is only that.

Neither contradicts the sentence "Below ADS = 1.0 there is no SV-driven winner
reversal at any margin", which I checked and which is accurate for the
direction-by-SV grid. But the asymmetry is the problem, not the literal
accuracy. A paper whose contribution is a null result is judged largely on
whether it reports its own strongest counter-evidence, and here it reports
delta = 0.02 when 0.02 supports the reading and 0.05 when 0.05 does. A reviewer
who opens the committed report, which the paper invites them to do, will find
both in under a minute.

**Suggested action.** Add both to the robustness paragraph or to an appendix
table giving the winner-structure outcome at all three margins for the
direction-by-SV grid, the fixed-SV grid, and the INIT stratification. Two
sentences will do it, and reporting them makes the null claim considerably
harder to attack rather than easier.

### Major 8. The accuracy accounting is incomplete in three ways that an AND audience will notice immediately

**Location:** section 6.3 (metric), section 5.3 (head to head), Table 3.

- **No ceiling for test signatures whose true author is absent from the training
  half.** Neither mechanism assigns an author it has never seen, so every such
  signature is an automatic error for both arms, and the share of them sets a
  per-block and per-dataset accuracy ceiling. I could find no such figure
  anywhere in `phase2e_boundary.md`, `PREREG.md` or the manuscript. It is very
  likely the main reason aminer sits at 0.41 and inspire at 0.95, and without it
  the reader cannot tell how much of the "the mechanisms are close" finding is
  the mechanisms being close and how much is a shared floor of impossible items.
- **No conditional precision for the rule.** The paper's whole framing is
  precision-first against coverage-first, and it reports only accuracy with
  abstention scored as incorrect. On the primary population that hides the fact
  that the rule is the more accurate arm where it fires: 0.8244 / 0.9686 = 0.851
  against the vote's 0.8294. Whether that is the right way to normalize is
  arguable, but the number belongs in section 5.3 given how the two mechanisms
  are characterized.
- **The metric is not one this field uses.** AND is evaluated with B-cubed,
  pairwise F, cluster F or the K-metric. The paper uses whole-set accuracy over
  a block's test signatures, which is defensible because the task here is
  assignment to a known author rather than clustering, but the manuscript never
  says so, never says what comparability is lost, and cites `amigo2009` only in
  passing about someone else's study. At a scientometrics or information science
  venue this will be the first methods question asked.

**Suggested action.** Add the out-of-history share per dataset to Table 3 (or to
the population table) as an accuracy ceiling column; add rule precision
conditional on firing to section 5.3; and add three sentences to section 6.3
justifying accuracy over B-cubed for an assignment task and naming the
comparability cost.

---

## 4. Minor comments

1. **Abstract length and shape.** 288 words in three paragraphs. Most journals
   in the target class cap the abstract at 200-250 words and expect a single
   unstructured paragraph. Budget for a cut of roughly a third.

2. **Missing front and back matter.** No keywords, no funding statement, no
   declaration of competing interests, no author contributions statement. All
   four are standard requirements in this venue class even for single-author
   papers, and the generative-AI disclosure (which is well written) does not
   substitute for any of them.

3. **"ADS" is never expanded.** It appears in the manuscript title comment, in
   section 3.2, and roughly forty times after that, always as a bare acronym.
   SV is at least glossed as "surface variability". Expand ADS at first use or
   rename it; a reader outside this project cannot decode it.

4. **Table 2's "n/a" cell is not n/a.** The retired pair's "B right, A wrong"
   count is determined by the containment: since every exact-correct signature
   is fuzzy-correct, the count is exactly the accuracy gap times the test-set
   size, 0.0196274 x 197,479 = 3,876 on the primary population
   (`phase2b_accuracy_by_population.csv`). Printing 3,876 makes the retired row
   comparable to the others and makes the containment more vivid, not less.

5. **"To every printed digit" (section 4.2) is doing more work than it should.**
   The identity 0.9686 + 0.0012 = 0.9698 holds on rounded inputs; on unrounded
   ones it holds to about 4e-10, which is a floating-point residue rather than
   an identity. Either say "to four decimal places" or give the unrounded
   statement.

6. **The Spearman quoted in section 3.2 is on a different population from the
   analysis.** -0.2612 is measured across 18,984 live blocks; every result in
   the paper is on 13,902 primary-population blocks. Say which, or give both.
   The paper is otherwise scrupulous about this distinction, which makes the
   omission stand out.

7. **Figure 2 needs a note.** The size-1 stratum cannot produce an undecided
   verdict, so its tall tie bar is not evidence of equivalence. See Major 1.

8. **kisti deserves a sentence.** It is a qualifying dataset with 711 blocks and
   a gap of +0.1131, larger than any effect discussed anywhere else in the
   paper, and its agreement rate of 0.7826 is far below every other qualifying
   dataset. Table 3 prints it and the text passes over it. A reader will ask
   what is different about kisti, and "it decides nothing under the
   generalization rule" is a procedural answer to a substantive question.

9. **inspire's dominance deserves a mechanism, not only an accounting.**
   Section 9 reports that inspire is 11,110 of 13,902 blocks and that pooled
   non-inspire was run. It never says what inspire is like that makes its
   accuracy 0.95 against everyone else's 0.41 to 0.85. One sentence on its block
   structure would let the reader judge whether pooling was ever meaningful.

10. **Section 2.3 is out of proportion.** Roughly 570 words on one prior paper
    inside a 774-word related-work section, while the rest of the AND literature
    gets two sentences. The Kim and Kim comparison is genuinely the closest prior
    work and the analysis of it is good; it should be a subsection of a fuller
    related-work section rather than most of one.

11. **Seventeen references is thin** for a full-length empirical paper in this
    venue class, where 40 to 70 is typical. See the literature audit in
    section 7 for specific gaps.

12. **"Signature" is used in the abstract before it is defined** in section 6.1.
    Either gloss it in the abstract or use "held-out author mentions" there.

13. **Table 5's caption conflates the two power floors.** It says no band being
    decided at delta = 0.05 "is what carries both H2 and H3 to Inconclusive".
    H2's floor counts decided marginal bands; H3's counts ADS bands containing
    two decided SV bands. Both are met, but they are different conditions and
    the table shows only the first.

14. **Six-decimal band edges (0.102644, 0.195066, 0.036782, 0.082418) are
    spurious precision** for calibration-split quantiles. Four decimals with a
    pointer to the constants file would read better and lose nothing.

15. **Name the two undecided cells** in section 5.4 rather than only counting
    them. They are [0, 0.5) x SV-high and ADS = 1.0 x SV = 0, and both are
    substantively interesting: the first is the most contested cell in the grid
    (decided rate 0.197) and the second is the largest (3,922 blocks).

16. **Reproducibility claims have no cost figures.** The paper says the pipeline
    is offline and CPU-runnable and gives no runtime, no memory figure and no
    hardware. One sentence, since the project records the answer.

17. **The Zenodo concept DOI is flagged unverified in the project's own
    records.** `STATE.md` notes under the 2.5c flags that which of
    10.5281/zenodo.21644207 and ...208 is the concept DOI is unverified against
    Zenodo. Section 9 now asserts the first is the concept DOI. Verify before
    submission.

18. **Section 8.3's self-citation needs its status stated in text.**
    `adscascade2026` is a Zenodo-archived artifact of the author's own, not a
    peer-reviewed publication, and section 8.3 spends 700 words reinterpreting
    it. Say what it is in the sentence that introduces it, so the reader can
    calibrate.

19. **Figure 5 and Table 6 overlap substantially.** Both carry the k curve and
    the driver clause outcome. With eleven floats in a 25-page manuscript, this
    is the cheapest cut available if length becomes binding.

20. **The subtitle promises a study of mechanism selection and no selector is
    built.** Section 5.7 justifies this well and the logic is sound. But a
    reader meets the title first, and "a pre-registered study of design-time
    mechanism selection" sets up an expectation that section 5.7 then has to
    talk them out of. Consider naming the negative result in the subtitle.

---

## 5. Reporting-standard compliance

No EQUATOR reporting standard applies. This is not a clinical, epidemiological,
diagnostic-accuracy, qualitative or systematic-review manuscript, and it is not
a prediction-model study in health. The nearest community norms are the
reproducibility checklists used in machine learning and information retrieval
venues, and the pre-registration reporting conventions used in psychology and
increasingly in information science. Assessed against a general rigor rubric:

| Item | Status | Note |
|---|---|---|
| Research question stated and answerable by the design | Met | Section 1.1 states it cleanly and the design addresses it. |
| Hypotheses fixed in advance | Met, with the amendment disclosed | Amendment story is the subject of Majors 5 and 6. |
| Analysis plan fixed in advance | Met | Falsification table, margins, bands, tie-break chain and splits all frozen; section 7 voided with a stated reason. |
| Data provenance and availability | Partly met | S2AND is public and the licence is stated. The paper's own code and pre-registration are not yet public (Major 6). |
| Population accounting, exclusions named and counted | Met, exemplary | Table 1 reconciles exactly; both exclusions named. But see Major 1 on the exclusion that was not made. |
| Unit of analysis stated and consistent | Not met | Block-level and signature-level results point opposite ways and are never reconciled (Major 2). |
| Measurement validity of the constructs | Partly met | H1 is a genuine validity check for ADS. The winner construct is not validated at small n (Major 1). |
| Uncertainty quantified for every reported comparison | Not met | The driver comparison, the paper's headline secondary result, carries none (Major 3). |
| Power / sensitivity addressed | Met | The power floor is pre-registered, evaluated first, and honestly reported as what decided both hypotheses. |
| Multiplicity and margin sensitivity | Partly met | Three margins pre-registered and reported for the main axes; not reported symmetrically for INIT and the fixed-SV grid (Major 7). |
| Robustness / controls | Met | SV_resid, Jaro-Winkler arm, INIT stratification and the k curve are all pre-registered and all run. |
| Generalization beyond the dominant dataset | Met and honestly reported | The failure of the non-inspire clause is stated in section 9 rather than buried. |
| Negative result framed as a finding, not a failure | Met | Section 8.1 does this well. |
| Claims scoped to evidence | Partly met | Section 1.4 is excellent; the abstract, title and conclusion outrun it (Majors 2 and 4). |
| Code and data citation | Partly met | Every table and figure names its source file, which is good practice. The repository is not reachable (Major 6). |
| Conflicts, funding, contributions declared | Not met | Missing (Minor 2). |
| AI-assistance disclosure | Met | Clear, specific and appropriately scoped. |

---

## 6. Literature audit

**Tooling note.** The Consensus search tool specified by this review workflow was
not available in this session. The audit below was run with general web search
only, which is weaker for systematic coverage. Every URL given was retrieved
this session. Works named without a URL were **not** verified in this session
and are given as search directions, not as citations to copy.

### Field context

The manuscript sits at the intersection of three literatures and engages one of
them properly.

- **Author name disambiguation.** Engaged, but narrowly. The manuscript cites
  S2AND, WhoIsWho, the Ferreira survey, Backes 2018, and Kim and Kim 2020 at
  length. It does not engage the AND evaluation-methodology literature that a
  scientometrics reviewer will expect, which is directly relevant given
  Major 8's metric question. Verified this session:
  ["A fast and integrative algorithm for clustering performance evaluation in
  author name disambiguation"](https://arxiv.org/pdf/2102.03251) and
  ["ORCID-linked labeled data for evaluating author name disambiguation at
  scale"](https://link.springer.com/article/10.1007/s11192-020-03826-6), both in
  *Scientometrics*, and
  ["Collecting large-scale publication data at the level of individual
  researchers"](https://link.springer.com/article/10.1007/s11192-020-03410-y).
  These are the venue's own recent AND papers and the paper cites none of them.
- **Entity resolution and record linkage.** Not engaged at all. This is the
  substance of Major 4.
- **Decision-focused evaluation and algorithm selection.** Engaged well. The
  Hand 2009 and Hernandez-Orallo 2012 framing is apt and the positioning in
  section 2.1 ("our gap sits one step earlier") is a fair and useful
  distinction.

### Novelty assessment, claim by claim

| Claim | Assessment | Evidence |
|---|---|---|
| Exact match is a strict sub-case of single-nearest retrieval | **Novel as a result about winner-unreachability; not novel as an observation.** The containment intuition is stated in the blocking literature: AutoBlock observes that "a wide range of existing blocking methods can be viewed as special cases of nearest neighbor blocking, with their own similarity metrics, including traditional key-based blocking methods which use binary similarity metrics." The paper's contribution is the consequence it draws (the verdict is unreachable, so the comparison is uninformative), which I found no prior statement of. | [AutoBlock, arXiv:1912.03417](https://arxiv.org/pdf/1912.03417) |
| The comparison a practitioner reaches for first cannot have a winner | **Novel in this form, with strong adjacent prior art the paper does not cite.** The IR community has a well-developed literature on comparisons that cannot inform, under the heading of weak baselines and non-additivity. Armstrong et al. found "little evidence of improvement in ad-hoc retrieval technology over the past decade" with baselines "generally weak", and the neural-hype line continues it. The paper's structural version is sharper than any of these, which is its contribution, but presenting it with no acknowledgement of that literature understates the paper's own lineage and will read as unawareness. | [Armstrong et al., CIKM 2009](https://dl.acm.org/doi/10.1145/1645953.1646031); [Lin, SIGIR Forum](https://dl.acm.org/doi/10.1145/3308774.3308781); [Yang, Lu and Lin, SIGIR 2019](https://cs.uwaterloo.ca/~jimmylin/publications/Yang_etal_SIGIR2019.pdf) |
| Two design-time signals do not yield an actionable selection rule | **Novel as measured, correctly scoped in section 1.4.** No prior art found that asks the design-time question at block granularity. | No counter-evidence found |
| The four-verdict winner construct with a practical-equivalence margin | **Not novel, and the paper does not say so.** This is equivalence testing: a smallest effect size of interest, an equivalence region, and a conclusion of practical equivalence when the interval falls inside it, with "undecided" as the indeterminate case. The equivalence-testing literature also carries the warning the paper needs about margin choice: "the choice of equivalence margin has a consequential impact on results". Citing it would let the paper import established machinery rather than re-derive it, and would answer the reviewer who asks why not TOST. | [Lakens, "Equivalence Tests: A Practical Primer"](https://journals.sagepub.com/doi/full/10.1177/1948550617697177) |
| Reinterpretation of the author's own earlier synthetic result | Not a novelty claim; appropriately framed as interpretation. | n/a |

### Citation spot-checks

- **Kim and Kim 2020, section 2.3.** Checked against the project's own
  positioning report `phase2/reports/kim2020_positioning.md`, which is unusually
  thorough. The manuscript's characterization is faithful: string matching never
  beats the best algorithmic arm on B-cubed F1 in any of the four datasets at
  any setting, the two crossings are on component metrics and do not survive
  into F1, and the authors present neither as a change of winner. The paper's
  claim to be reproducing their compression shape at block level is fair. **No
  correction needed.** The correct external record for this paper is
  [arXiv:2102.03250](https://arxiv.org/pdf/2102.03250).
- **S2AND homonymity and synonymity, sections 1.2 and 3.2.** Used as external
  validity checks for ADS and SV, with the cross-correlations reported. This is
  a good use of the citation and is internally consistent with the 2.1 report.
  Not independently re-verified against the S2AND paper this session.

### Gaps to fill, not verified this session

Named as search directions for the author to verify before citing. In rough
priority order for this manuscript: the probabilistic record linkage foundation
(Fellegi and Sunter); a standard entity resolution reference work or survey
(Christen's monograph; the Papadakis blocking surveys); benchmark-evaluation
studies in entity matching (the Kopcke, Thor and Rahm line); the deep entity
matching baselines (the Magellan / DeepMatcher / Ditto line); the WDC product
matching gold standard, which section 1.2 discusses without citing; and the
pre-registration literature in the open-science tradition, which would let
section 6.4 make its argument by reference rather than from first principles.

---

## 7. Venue-class assessment (mid-tier Q2/Q3 information science, IR, scientometrics)

### Scope fit

**Good, in the AND framing; awkward in the entity resolution framing.** A
pre-registered negative result on author name disambiguation mechanisms,
measured on a public benchmark with full reproducibility, is squarely inside the
aims of the information science and scientometrics journals in this band, which
publish AND methodology and evaluation regularly. The same paper titled and
positioned as an entity resolution contribution sits at the edge of scope for
those journals and does not have the citation base to compete in the database or
data-management venues where entity resolution lives. This is a second argument
for Major 4's first option.

### Novelty calibration

**At or slightly above the bar for this band, with one caveat.** Journals in
this class publish incremental methodological and evaluation work, and a
well-executed pre-registered null with a clean structural result is at least as
substantial as the median paper they publish. The caveat is that the structural
result, which is the most transferable thing here, is an argument rather than a
measurement, and the empirical half is a null on two deliberately simple
untrained mechanisms whose absolute accuracies (0.41 on aminer, 0.53 pooled
non-inspire) sit far below what the AND literature builds. An editor may ask
whether a null about two lookups that nobody would deploy tells a practitioner
anything about the choice they actually face. Section 3.1 anticipates this and
answers it reasonably; the answer needs to be visible in the abstract, because
that is where the desk decision is made.

### Style match

Close. Venue-neutral LaTeX, sentence-case headings, plain prose, no AI-tell
vocabulary, source file named for every table and figure. Three mismatches:
the abstract's length and three-paragraph shape (Minor 1), the missing
declarations (Minor 2), and eleven floats across 25 pages, which is at the top
of the range for this band. The prose itself is better than most submissions in
this class: direct, specific, and willing to state what the evidence cannot do.

### Required-but-missing items

| Item | Action |
|---|---|
| Keywords | Add 5-6, including "author name disambiguation", "pre-registration", "null result", "entity resolution", "algorithm selection". |
| Abstract length | Cut to the target journal's limit, typically 200-250 words, and consider one paragraph. |
| Declaration of competing interests | Add. |
| Funding statement | Add, including "no funding" if that is the case. |
| Author contributions | Add; required by many journals in this band even for single authors. |
| Public code and data repository, reachable at submission | Push and tag `phase-2`; change section 9 from a promise to a fact (Major 6). |
| Independent pre-registration timestamp | Deposit and cite (Major 6). |
| Highlights / graphical abstract | Required by Elsevier titles in this band; prepare if the target is one. |
| Zenodo DOI verification | Confirm which DOI is the concept DOI (Minor 17). |

### Alternative venues

Not recommending a venue change, so this section is left empty by design. The
paper fits its stated target class. If the author decides to keep the entity
resolution framing rather than take Major 4's first option, the calculus
changes, and the realistic alternatives then sit in the data management and
information systems band rather than in information science.

---

## 8. Recommendation

**Major revision needed.**

This is a better paper than its current framing admits, and it is not far from
publishable in the target class. The structural result is correct, genuinely
useful, and honestly presented, including the order of discovery, which most
authors would have quietly reversed. The pre-registration discipline is real:
the falsification table was frozen, the power floor was evaluated first, the
clause that pointed against the author's own preferred framing was reported and
acted on, and the regression check against pre-amendment counts is a control
most pre-registered papers do not bother with. The numbers reconcile to the
committed artifacts everywhere I checked, which is rarer than it should be.

What holds it back is that three of its load-bearing quantities do not currently
survive being checked hard. The per-block winner construct is degenerate on the
blocks that supply most of its decided verdicts (Major 1). The driver
comparison, which the paper calls its sharpest measurement and which retired an
entire earlier framing, is a bare point comparison with no interval (Major 3).
And the paper's own regression names a design-time signal it never registered
and never tested, which splits the pooled and per-block results in opposite
directions (Major 2). None of these requires new data or new code; all three are
re-analyses of records that already exist. Alongside them, the title claims a
width the evidence does not reach and the reference list does not support
(Major 4), and the integrity apparatus in section 6.4, which is the paper's own
strongest defensive asset, is currently attested only by an unpublished
repository and contains one sentence that a checking reader will falsify
(Majors 5 and 6).

If Majors 1, 2 and 3 are addressed with re-analysis, Major 4 with either a
retitle or a non-AND demonstration, and Majors 5, 6 and 7 with disclosure rather
than argument, I would expect to recommend acceptance on the next round. I would
particularly encourage the author not to treat Major 2 defensively: the
size-dependent split between the pooled and per-block winners is the most
interesting unreported thing in this dataset, and it is a finding, not a
problem.

---

## 9. Audit log

**Manuscript.** `phase2/paper/main.tex`, 1,387 lines, at commit `00dcf04`
(2026-09-21, branch `phase-2`). Measured this session: abstract 288 words;
body 9,488 words excluding float contents; ten sections plus two back-matter
statements; 6 tables, 5 figures, 11 captions; 17 bibliography entries in
`references.bib`; compiled PDF present at `phase2/paper/main.pdf`. Per-section
body word counts: Introduction ~1,010, Related work 774, Problem setting 750,
A comparison that cannot have a winner 1,032, A pair that can 517, Experimental
design 1,733, Results 1,759, Discussion 1,286, Limitations 380, Conclusion 247.

**Supplementary information.** No separate SI file. The author directed this
review to the committed reports and tables as the equivalent, and they were
used as such.

**Artifacts consulted.** `phase2/CLAUDE.md`; `phase2/STATE.md`;
`phase2/PREREG.md` (including Amendment 1, its six resolutions, and Addendum
1a); `phase2/phase2b_core.py`; `phase2/reports/phase2e_boundary.md`;
`phase2/reports/phase2b_boundary.md`; `phase2/reports/kim2020_positioning.md`;
and the tables `phase2e_accuracy_by_population.csv`, `phase2e_h1_spearman.csv`,
`phase2e_twosidedness_eval.csv`, `phase2e_driver_comparison.csv`,
`phase2e_pooled_ads.csv`, `phase2e_pooled_sv.csv`, `phase2e_pooled_cells_sv.csv`,
`phase2e_power_by_size.csv`, `phase2e_regression.csv`,
`phase2e_margin_sensitivity.csv`, `phase2e_k_curve.csv`,
`phase2e_generalization.csv`, `phase2c_pair_twosidedness.csv`,
`phase2c_pair_regimes.csv`, `phase2b_accuracy_by_population.csv`. Commit
metadata for the seven hashes in section 6.4 was read with `git log`.

**Numbers independently re-derived and confirmed.** Table 1's row arithmetic and
all six share percentages; the pooled non-inspire accuracies and the all-primary
accuracies from the per-dataset rows; the agreement identity in section 4.2; the
decided-verdict sum; the H1 coefficients and intervals; the per-band gaps,
verdicts and decided rates on both axes; the twenty-cell verdict distribution
(18 tie, 2 undecided); the driver table at all three margins and both
diagnostics; the regression coefficients and standard errors; the k curve; the
41% contested-region figure (14,680 / 35,732); the two lines of zeros in the
calibration probe for all three candidate pairs; the H1 per-band mean accuracies
against `phase2e_boundary.md` lines 110-113; and all three commit-interval
timings in section 6.4 (1h48m51s, 1h20m25s, 28m26s).

**Claims the artifacts do not support, or support only with a qualifier.** One:
the unqualified sentence in section 6.4's locked quote about no k-nearest
accuracy figure existing (Major 5). Everything else I checked was accurate as
written.

**Omissions found in the committed output.** Two winner reversals at
delta = 0.02 absent from the manuscript (Major 7); no out-of-history accuracy
ceiling computed anywhere (Major 8).

**Literature search.** Consensus was unavailable in this session; general web
search was used instead, with four queries (nested / special-case baselines in
entity matching; weak baselines in IR; equivalence testing and practical
equivalence margins; AND evaluation surveys in *Scientometrics*). Coverage is
therefore indicative, not systematic. All URLs cited in section 6 were retrieved
this session. Works named in "gaps to fill" were not verified this session and
are flagged as such.

**Limitations of this review.** No target journal was named, so no author
guidelines were fetched and section 7 is calibrated to the venue *class* rather
than to one journal's requirements; the required-items table should be
re-checked against the chosen journal. The review did not re-execute any
analysis code, so it verifies consistency between the manuscript and the
committed artifacts, not the correctness of the artifacts themselves, except
where the code was read directly (`phase2b_core.py`). Figures were not
inspected; figure claims were checked against the underlying CSVs instead.
