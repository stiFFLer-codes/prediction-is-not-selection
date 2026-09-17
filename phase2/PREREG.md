# Phase 2.2 pre-registration, frozen

**Frozen 2026-09-18, Phase 2.2a, before any accuracy, similarity cutoff, winner,
or selector existed anywhere under `phase2/`.** Charter invariant 5 requires this
document to be committed before the measurement it governs. It supersedes the
pre-registration draft in `phase2-spec.md` section 8.

This document fixes, in advance: the hypotheses, the falsification rules, the
signals and their thresholds, the split, the mechanisms, the winner definition,
the analysis structure, the controls, and the reporting requirements. Nothing
here was chosen after seeing a result, because no result exists. The only numbers
quoted are Phase 2.1 corpus-level measurements, already committed and already
reviewed, and they appear as context for design choices, never as evidence for a
hypothesis.

**Amendment rule.** If any part of this document turns out to be unrunnable or
ill-defined once 2.2b starts, the change is made by appending a dated amendment
section to this file, stating what changed and why, in the same commit as the
code that needs it and before the affected numbers are produced. The original
text is never edited away.

---

## 1. What is being tested

Two mechanisms assign a held-out author mention to an author using only that
name block's own history. A design-time consistency statistic, ADS, is claimed to
predict how well each mechanism does but not which one to pick. A design-time
surface-stability statistic, SV, is claimed to carry the selection information
ADS lacks.

Both signals are computed from the training half only, are label-free in SV's
case, and are available before any mechanism is run. That is what "design-time"
means here and it is load-bearing: a signal that needs the test labels, or the
test items, is not a signal a practitioner can act on.

---

## 2. Hypotheses

Phrased to claim the specific design-time, per-block, measured dissociation. The
general statement that surface form affects the margin between two disambiguation
methods is already established at dataset level by Kim and Kim (2020) and is not
claimed as new here. See `reports/kim2020_positioning.md`.

### H1, accuracy (construct validity, not a contribution)

Across evaluation blocks, train-only ADS is positively associated with each
mechanism's own held-out accuracy, separately for exact match and for fuzzy
retrieval.

H1 is stated as a validity check. That disambiguation accuracy degrades as
homonymity rises is visible in Kim and Kim's homonym-centric datasets and in the
S2AND paper. H1 confirms that our per-block ADS behaves like the established
dataset-level quantity. It is reported as such and is not presented as a finding.

### H2, selection blindness

Across its observed range, train-only ADS does not predict **which** of the two
mechanisms wins a per-block comparison. Concretely: holding SV band fixed, the
identity of the decided winner does not change across ADS bands.

H2 is a claim about the **sign and identity** of the winner, not about the
magnitude of the gap. ADS is expected to predict gap magnitude, because that is
what Kim and Kim report at dataset level, and finding it here is not a refutation
of H2. The magnitude relationship is reported beside H2 as a previously known
effect reproduced at block level, with the citation.

### H3, co-signal

A design-time, label-free, train-only surface-stability measure, SV, predicts the
winner identity where ADS cannot. Concretely: holding ADS band fixed, the
identity of the decided winner changes across SV bands, and the change is a
**winner reversal** as defined in section 8, not only gap compression.

H3 additionally requires the effect to survive the initialization control of
section 9: the same winner reversal must be present when SV is replaced by
SV_resid, the initialization-free residual surface measure. Without that, the
surface axis is forename initialization, which is Kim and Kim's manipulated
variable observed rather than set, and the paper says so.

### Out of scope for 2.2, pre-registered here for completeness

The two-signal selector is Phase 2.3. Per charter invariant 4, it is reported
only beside an ADS-only selector and an SV-only selector, on held-out blocks, and
the dual-signal claim survives only if the two-signal version beats both by more
than the same margin delta used for the winner test. If SV-only suffices, that is
what gets reported. A fixed always-fuzzy and a fixed always-exact policy are also
reported as floor baselines; if neither selector beats the better fixed policy,
that is reported plainly as well.

---

## 3. Data, split, and analysis population

Substrate: `phase2/data/s2and_signatures.parquet`, 766,133 signatures, 7 S2AND
sub-datasets, blocked by the frozen key in `phase2/s2and_blocking.py`. Frozen in
Phase 2.1, not re-tuned.

**Live blocks.** Blocks with at least 2 signatures. 18,984 of 26,939 at Phase 2.1,
covering 99.0% of signatures.

**Calibration split.** A random 15% of live blocks, drawn with seed 20260918 at
block level. Used exactly once, for the fuzzy cutoff (section 7) and for the SV
and SV_resid band edges (section 6). Never used for any reported hypothesis
number.

**Evaluation split.** The remaining 85% of live blocks. Every reported result
comes from these.

**Within-block train and test.** Inside each evaluation block, signatures are
randomly assigned with seed 20260918 to a train half and a test half by

    n_train = max(1, min(n - 1, floor(0.7 * n)))

so a block of 2 gives 1 and 1, a block of 5 gives 3 and 2, a block of 10 gives 7
and 3. The train signatures are the block's historical knowledge base. The test
signatures are scored. No test signature is ever visible to a signal, a cutoff,
or a mechanism.

**ADS is recomputed train-only**, on the block's train signatures alone. The
Phase 2.1 numbers are corpus-level and are not reused as ADS values.

**SV is also computed train-only.** SV needs no labels, so restricting it to the
train half is a choice rather than a necessity. It is made because a design-time
selector sees history and nothing else, and a signal computed partly from the
items it is about to route would not be usable in practice.

**Primary analysis population.** Evaluation blocks with `n_train >= 2` and
`n_test >= 1`, that is blocks of 3 or more signatures. Below that, ADS on a
single train signature is 1.0 by construction and SV is undefined, so the signals
carry no information. Blocks of exactly 2 are a **named, counted, reported
exclusion**, never a silent drop: their count, their share of signatures, and
their per-mechanism accuracy are reported as a separate stratum. Singleton blocks
were already outside the live set and are reported the same way.

**Minimum sizes, fixed now.** A cell, band, or dataset with fewer than 30 blocks
is reported with its count and marked under-powered, and is not interpreted and
not used to decide a hypothesis. A dataset qualifies for the generalization rule
in section 10 if it contributes at least 100 blocks to the primary analysis
population.

---

## 4. Mechanisms

Both mechanisms use only the block's train signatures, each carrying a surface
form and an author label. Both may abstain.

**Exact match.** If the test signature's surface form occurs among the train
surface forms, assign the most frequent author among train signatures carrying
that exact form. Otherwise abstain. No parameter.

**Fuzzy retrieval.** Compute the similarity between the test surface form and
every distinct train surface form. Take the highest. If it is at or above the
frozen cutoff, assign the most frequent author among train signatures carrying
that form. Otherwise abstain. One parameter, the cutoff, calibrated once per
section 7 and then global and fixed.

Similarity is `1 - Levenshtein.normalized_distance`, the same distance family SV
is built from. Section 9 pre-registers a Jaro-Winkler robustness arm against the
criticism that follows from sharing a metric.

**Tie-breaking, deterministic and fixed now.** Among candidate authors: the most
frequent author within the matched form, then the most frequent author within the
block, then the lexicographically smallest author id. Among candidate forms at
equal similarity: the form carried by more train signatures, then the
lexicographically smallest form.

**Metric.** Whole-set accuracy over the block's test signatures, with abstention
counted as incorrect. Coverage, the share of test signatures not abstained on, is
reported separately for each mechanism at every level at which accuracy is
reported. The asymmetry that exact abstains and fuzzy mostly does not is a result
to report, not a nuisance to normalize away.

**Mechanism agreement rate.** At every SV band, report the share of test
signatures on which the two mechanisms return the identical prediction, including
identical abstentions. This distinguishes genuine practical equivalence from the
structural case where a single-surface-form history makes the two mechanisms the
same procedure. Pre-registered because a tie-dominated low-SV region would
otherwise be indistinguishable from a measurement artifact.

---

## 5. The consistency signal, ADS

ADS(block) = the share of the block's **train** signatures belonging to its single
most frequent author. Range (0, 1], 1.0 when the block's history names one author.

**Bands, fixed now**, the same five used in the Phase 2.1 report so the two passes
are comparable: `[0, 0.5)`, `[0.5, 0.7)`, `[0.7, 0.9)`, `[0.9, 1.0)`, and exactly
`1.0`. Band edges are fixed by the definition of purity, not read off a
distribution, so no calibration data is needed for them.

---

## 6. The surface-stability signal, SV, and its thresholds

SV(block) = the expected normalized Levenshtein distance between two signatures
drawn at random without replacement from the block's **train** signatures,
computed on the frozen surface form. Signature-weighted. Implemented as
`surface_variability` in `phase2/s2and_blocking.py`, frozen in Phase 2.1 with a
runnable self-check. The function is unchanged; only its input set changes, from
all of a block's signatures to the train half.

Higher SV means less surface stability. The name is kept as SV, variability, to
match the frozen code, and the sign is stated everywhere it is used.

**Thresholds come from the observed distribution, not from the [0, 1] scale.** SV
is bounded well below 1 by construction, because every signature in a block shares
a surname: at Phase 2.1 the corpus median was 0.0752 and the 99th percentile
0.4502. Fixed bands on the nominal scale would be meaningless.

**Band rule, fixed now, values computed at run time:**

- Band 0: SV exactly 0. A block whose history is written one way. Structural, so
  it is its own band and is never merged into a quantile.
- Bands 1, 2, 3: the terciles of the **strictly positive** SV values, with cut
  points taken from the **calibration split** blocks only, at the 33.33rd and
  66.67th percentiles.

Cut points are computed on calibration blocks so that not even the band edges are
chosen using evaluation data. The realized cut points are printed and committed
before any evaluation-split number is produced. The same rule, with its own
separately computed cut points, defines the SV_resid bands of section 9.

---

## 7. The fuzzy cutoff calibration protocol

Specified here, executed in 2.2b, not in this pass.

1. Run only on the **calibration split** blocks, which are disjoint from every
   block that produces a reported number.
2. Candidate grid, fixed now: similarity cutoff in {0.50, 0.55, 0.60, 0.65, 0.70,
   0.75, 0.80, 0.85, 0.90, 0.95}.
3. For each candidate, run the fuzzy mechanism over the calibration blocks under
   the same train and test construction as section 3, and compute pooled accuracy
   over all calibration test signatures.
4. Select the candidate with the highest pooled accuracy. Ties are broken toward
   the **higher** cutoff, which is the more conservative choice because it
   abstains more.
5. Write the chosen value into a committed constants module together with the
   full accuracy-versus-cutoff curve, and commit it before any evaluation-split
   run. From that commit it is frozen.

**One global cutoff.** Not one per dataset, not one per ADS band, not one per SV
band. A per-stratum cutoff would hand fuzzy a tuning advantage that exact, which
has no parameter, cannot receive, and would make every winner comparison a
comparison of tuning budgets. The asymmetry that remains, one tuned parameter
against none, is stated in the paper.

---

## 8. Winner definition

### Per block

Let `d_b = accuracy_exact(b) - accuracy_fuzzy(b)` over block b's test signatures.

Paired bootstrap: resample block b's test signatures with replacement, B = 2000
draws, seed 20260918 offset by the block index; both mechanisms are scored on the
same resample, so the comparison is paired. Take the 95% percentile interval for
`d_b`.

**Practical-equivalence margin, fixed now: delta = 0.05 accuracy points.** It sits
below the granularity of small blocks, so a block with 2 test signatures can only
be decided by the interval and will usually come out undecided, which is the
honest answer for two observations. For larger blocks 5 accuracy points is a
difference a practitioner would act on.

**Four verdicts, mutually exclusive:**

| verdict | rule |
| --- | --- |
| exact wins | interval lower bound > +delta |
| fuzzy wins | interval upper bound < -delta |
| tie | interval entirely inside [-delta, +delta] |
| undecided | anything else, the interval straddles a margin boundary |

Tie means equivalence was demonstrated. Undecided means there was not enough
evidence to decide. They are kept apart, because merging them would let a
low-power result read as a positive finding of equivalence.

**Power reporting is mandatory.** The share of blocks in each verdict is reported
as a function of test-set size, so a reader can see how much of any "no winner"
region is genuine equivalence and how much is a small test set.

### Per ADS band, and per cell

Two summaries are reported at every band and every two-dimensional cell, and both
are required, because they answer different questions.

1. **Verdict distribution.** The share of that band's blocks falling in each of
   the four per-block verdicts.
2. **Pooled band verdict.** Pool the test signatures of all blocks in the band,
   compute the pooled accuracy difference, and bootstrap by **resampling blocks
   with replacement**, not signatures, because the block is the independent unit.
   B = 2000, same seed scheme. Apply the same delta and the same four-verdict rule
   to the resulting interval.

The pooled band verdict is what section 9's reversal and compression tests
operate on.

---

## 9. Winner-structure analysis, stated in advance

**2.2b will report whether the pattern is a genuine winner change or only gap
compression.** This is stated up front so that the answer cannot be chosen after
the fact.

### The two-dimensional stratified analysis

The exact-minus-fuzzy gap is reported as a function of **both** ADS and SV, in a
5 by 4 grid of ADS bands crossed with SV bands. This is required rather than
optional because the two axes are correlated at Pearson -0.2988 and Spearman
-0.2612 (Phase 2.1). A marginal SV effect could be an ADS effect in disguise and
the reverse, so SV's effect is only ever shown **at fixed ADS**, and ADS's effect
only ever **at fixed SV**.

Each of the 20 cells reports: block count, signature count, mean and median
per-block gap, pooled gap with its block-bootstrap interval, the pooled verdict,
the four-way verdict distribution, both coverages, and the mechanism agreement
rate. Cells under 30 blocks are printed with their count and marked
under-powered, and are excluded from every decision rule.

Alongside the grid, a single regression of the per-block gap on ADS and SV
together, with block-clustered standard errors and with test-set size as a
covariate, is reported as a compact summary. It is a summary of the grid, not a
substitute for it, and no hypothesis is decided from it.

### The three structural outcomes, defined now

Applied within each ADS band that has at least two SV bands of 30 or more blocks
with a decided pooled verdict:

- **Winner reversal.** Two SV bands have decided pooled verdicts of opposite
  identity, one exact and one fuzzy, under the same delta.
- **Tie-crossing.** One SV band has a decided pooled verdict and another has a
  tie, with no band decided the opposite way. Weaker than a reversal, stronger
  than compression alone.
- **Gap compression only.** The magnitude of the pooled gap changes across SV
  bands but no band pair is decided in opposite directions and no decided-to-tie
  crossing occurs.

The same three definitions are applied across ADS bands at fixed SV, for H2.

**If the result is gap compression only, that is what the paper reports**, in
those words, as a per-block, design-time, measured version of Kim and Kim's
dataset-level gap-compression finding obtained with two simple mechanisms. The
dissociation claim is dropped, the title leads with the boundary finding, and the
comparison to Kim and Kim is made explicitly in the results, not buried in
related work.

### Control for the Kim and Kim overlap

**2.2b will check whether the surface effect on the winner survives controlling
for plain forename initialization**, so that our surface axis is shown to be more
than initialization alone. Kim and Kim's manipulated variable is the full-forename
ratio. If our SV is a proxy for it, H3 reduces to their finding at a finer grain.

**Primary control, SV_resid.** Define an initialization-canonical surface form
from the structured name fields: transliterate to ASCII, lowercase, keep letters
only, reduce the first name to its first letter, reduce each middle-name token to
its first letter, keep the last name in full, keep the suffix, and join by single
spaces. Under this map "John Smith" and "J. Smith" become the identical string,
so forename initialization contributes exactly zero. SV_resid is the frozen
`surface_variability` function applied to these canonical forms over the block's
train signatures. What remains in SV_resid is spelling variation, diacritics,
hyphenation, transliteration, presence or absence of a middle name, and suffixes.

The entire section 9 analysis is rerun with SV_resid in place of SV, with its own
calibration-split band edges. H3 requires the reversal to be present in both.

**Secondary control, initialization stratification.** Define INIT(block) as the
share of the block's train signatures whose given-name field is an initial only,
that is a single ASCII letter optionally followed by a period. Bands fixed now:
INIT = 0, 0 < INIT < 0.5, INIT >= 0.5. Report the SV-to-winner relationship
within each INIT band. This answers a different question from SV_resid, namely
whether the effect exists among blocks that are homogeneous in initialization
style, and it is cheap, so both are run.

**Metric-family robustness arm.** SV and the fuzzy mechanism are both built on
normalized edit distance. The winner is defined by labelled accuracy, so this is
not the tautology charter invariant 2 forbids, but the shared metric is a fair
objection. 2.2b reruns the fuzzy mechanism with Jaro-Winkler similarity, with its
own cutoff calibrated on the calibration split by the section 7 protocol, and
reports whether the SV-to-winner relationship survives the change of metric
family. If it does not, that is reported as a limit on the finding.

---

## 10. Falsification table

Four outcomes per hypothesis, fixed now. Every rule below is evaluated on the
evaluation split only, and "generalizes" always means the section 10
generalization rule: the result holds in the pooled non-inspire analysis **and**
in a majority of qualifying non-inspire datasets, where qualifying means at least
100 blocks in the primary analysis population.

### H1, accuracy

| outcome | rule |
| --- | --- |
| Supported | Spearman correlation of train-only ADS with held-out accuracy is positive with a 95% block-bootstrap interval excluding 0, for **both** mechanisms, and it generalizes. |
| Partial | Positive and interval-excluding-0 for one mechanism but not the other, or pooled but not generalizing. |
| Not supported | Interval includes 0 for both mechanisms, or the correlation is negative with an interval excluding 0 for either. |
| Inconclusive | Fewer than 500 blocks in the primary analysis population, or fewer than 2 qualifying non-inspire datasets. |

### H2, selection blindness

| outcome | rule |
| --- | --- |
| Supported | Within every SV band holding 30 or more blocks, the identity of the decided pooled verdict is constant across all ADS bands with 30 or more blocks, or all such verdicts are tie or undecided. No ADS-driven winner reversal anywhere. |
| Partial | Winner identity is constant across ADS in most but not all eligible SV bands, or the only ADS-driven changes are tie-crossings rather than reversals. |
| Not supported | At fixed SV band, two ADS bands have decided pooled verdicts of opposite identity. **This is the outcome Kim and Kim's dataset-level result would predict.** If it occurs it is reported as their finding reproduced at block level, the boundary framing is abandoned, and the paper is rewritten around a two-signal difficulty account instead. |
| Inconclusive | Fewer than 2 SV bands and 2 ADS bands with 30 or more blocks and a decided pooled verdict. |

### H3, co-signal

| outcome | rule |
| --- | --- |
| Supported | Within at least one ADS band with 30 or more blocks per SV cell, two SV bands have decided pooled verdicts of opposite identity, a winner reversal; the same reversal is present with SV_resid; and it generalizes. |
| Partial | A tie-crossing rather than a reversal; **or** a reversal with SV but not with SV_resid, meaning the surface axis is forename initialization; **or** a reversal that holds pooled but does not generalize; **or** a reversal that holds with edit distance but not with Jaro-Winkler. |
| Not supported | **Gap compression only.** The magnitude of the gap varies with SV but no SV band pair is decided in opposite directions in any ADS band, in any qualifying analysis. This is an honest, publishable outcome and is reported in those words: a per-block, design-time, measured version of Kim and Kim's gap-compression finding, obtained with two simple mechanisms. The dissociation claim is dropped. |
| Inconclusive | Fewer than 2 SV bands with 30 or more blocks and a decided pooled verdict inside any single ADS band. |

### Outcomes that are explicitly acceptable, not failures to hide

Listed separately so that none of them can later be treated as a result to be
avoided rather than reported.

- **The gap only compresses, there is no reversal.** H3 not supported. The
  boundary finding stands on its own and leads the paper. Charter section on
  honest framing already commits to this.
- **The co-signal does not help.** In 2.3, the SV-only selector matches or beats
  the two-signal selector out of sample, or neither beats the better fixed policy.
  Reported plainly per charter invariant 4. If SV-only suffices, the paper says
  SV-only suffices.
- **SV is forename initialization.** The effect is present in SV and absent in
  SV_resid. Reported as such, with the explicit statement that our surface axis
  then amounts to Kim and Kim's manipulated variable observed instead of set, and
  the contribution narrows to the unit of analysis and the design-time framing.
- **The low-SV region is structurally tied.** The two mechanisms return identical
  predictions on most low-SV blocks. Reported via the mechanism agreement rate,
  and the claim becomes one-sided, fuzzy wins at high SV and the mechanisms
  coincide at low SV, which is a weaker and differently shaped finding.
- **ADS predicts gap magnitude.** Expected, consistent with Kim and Kim, and not
  a refutation of H2, which is about winner identity. Reported with the citation.
- **The primary analysis population is too thin.** Inconclusive is a permitted
  verdict and will be used rather than reaching for a smaller threshold.

---

## 11. Per-dataset reporting, mandatory

inspire contributed 15,077 of 18,984 live blocks at Phase 2.1, about 79%. Any
pooled number is therefore mostly an inspire number, and a pooled-only result
would be a single-dataset result wearing a seven-dataset label.

Every headline table and every hypothesis decision is reported in three forms:

1. **Per dataset**, all seven of aminer, arnetminer, inspire, kisti, pubmed,
   qian, zbmath, each with its block count and each marked under-powered where it
   falls below the section 3 thresholds.
2. **inspire alone**, labelled as such.
3. **Pooled non-inspire**, the other six datasets combined.

**Generalization rule, fixed now.** A finding is reported as generalizing only if
it holds in the pooled non-inspire analysis **and** in a majority of the
qualifying non-inspire datasets, where a dataset qualifies at 100 or more blocks
in the primary analysis population. A finding that holds only pooled, or only on
inspire, is reported as an inspire finding in those words.

---

## 12. Reproducibility and invariant checks for 2.2b

- All seeds fixed at 20260918 and recorded in the committed code. Every reported
  number is produced by committed, re-runnable code, per charter invariant 5.
- No test signature reaches any signal, cutoff, or band edge. Calibration blocks
  are disjoint from evaluation blocks. Per charter invariant 3.
- The winner is defined only by labelled accuracy. Neither ADS nor SV nor SV_resid
  appears in the definition of the winner. Per charter invariant 2.
- Offline, CPU-only, no API key, no paid call, deterministic. Per charter
  invariant 7.
- Two mechanisms only. No semantic or LLM arm is built in 2.2. Per charter
  invariant 6.
- Every quantity introduced here gets an assert-based self-check in the module
  that defines it, following `s2and_blocking.py`.
