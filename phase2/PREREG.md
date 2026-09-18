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

**Revision history.**

2026-09-18, Phase 2.2d, review of the Amendment 1 freeze, still before 2.2e and
still before any measurement: **Addendum 1a**, appended after Amendment 1. It
replaces resolution 5's averaged-range test for "ADS is the stronger driver of
decidability" with a one-way variance decomposition, because range is not
invariant to band count and the grid is 5 by 4, which handed ADS an edge in the
comparison H2 needs ADS to win. The range test is retained as a second required
condition, and a split between the two measures makes the clause Partial. This
tightens the rule; it does not relax one.

2026-09-18, Phase 2.2d, after 2.2b and 2.2c and before 2.2e: **Amendment 1, the
two-signal reframe**, appended at the end of this file. It supersedes sections 2,
4, 7 and 10 and renames the section 8 verdicts. Forced by two structural findings
that 2.2b and 2.2c measured: a single-nearest retriever contains exact match, and
a precision-first rule cannot win a block whose history names one author. Written
before any accuracy for the new mechanism exists anywhere under `phase2/`.

2026-09-18, review of the 2.2a freeze, still before any
measurement and before 2.2b starts: two rules were added at the reviewer's
instruction, verbatim. Section 8 gained "Margin sensitivity", which makes delta
= 0.05 the primary margin and requires a 0.02 and 0.03 robustness curve beside
it. Section 10 gained "Order of evaluation", which makes Inconclusive take
precedence over every other outcome row. Both tighten the rules; neither relaxes
one. Recorded here rather than applied silently, because this document's
authority comes from being fixed in advance. See commit history for the exact
diff.

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

> **Superseded by Amendment 1 (Phase 2.2d, 2026-09-18), at the end of this
> file.** The text below is what was frozen at 2.2a and what 2.2b was run
> against. It is kept for the record and is no longer binding.

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

> **Mechanism B and the verdict names are superseded by Amendment 1 (Phase
> 2.2d, 2026-09-18), at the end of this file.** Mechanism A, the metric, the
> tie-breaking chain and the coverage rules below are unchanged and still
> binding.

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

> **Void for 2.2e under Amendment 1 (Phase 2.2d, 2026-09-18), at the end of
> this file.** Mechanism B no longer has a similarity cutoff. The protocol
> below is the record of what produced the frozen 2.2b cutoff. Section 6's
> band edges, calibrated under the same protocol, do carry over.

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

### Margin sensitivity

**Margin sensitivity, pre-registered.** The primary margin is delta = 0.05. Every
band-level and cell-level verdict, and the H2 and H3 outcomes, are also
recomputed at delta = 0.02 and delta = 0.03 and reported as a robustness curve
beside the primary. An H2 or H3 outcome that holds at one margin and flips at
another is reported as margin-dependent and treated as Partial, not Supported.
Fixed now so the margin cannot be chosen after seeing results.

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

> **Superseded by Amendment 1 (Phase 2.2d, 2026-09-18), at the end of this
> file.** The table below is what was frozen at 2.2a and what decided the 2.2b
> outcomes. It is kept for the record and is no longer binding.

Four outcomes per hypothesis, fixed now. Every rule below is evaluated on the
evaluation split only, and "generalizes" always means the section 10
generalization rule: the result holds in the pooled non-inspire analysis **and**
in a majority of qualifying non-inspire datasets, where qualifying means at least
100 blocks in the primary analysis population.

**Order of evaluation.** **Inconclusive is evaluated first.** If a hypothesis's
Inconclusive power floor is met, the outcome is Inconclusive regardless of the
other rows. In particular, a set of bands that are all tie or undecided is not H2
Supported unless there are at least two ADS bands and two SV bands, each with 30
or more blocks and a decided pooled verdict.

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

---

# Amendment 1, Phase 2.2d, 2026-09-18: the two-signal reframe

**Status: binding. This amendment supersedes sections 2, 4, 7 and 10 of the
original text above.** Where this amendment and the original differ, this
amendment wins. Sections 1, 3, 5, 6, 8, 9, 11 and 12 carry over unchanged except
where named below.

**Made under the amendment rule at the head of this file**, which requires a
change to be a dated appended section, stating what changed and why, committed
before the affected numbers exist. The original text is left in place rather than
edited away, so that a reader can see exactly what was frozen at 2.2a and what
2.2b was run against. Sections 2, 4, 7 and 10 each carry a banner pointing here.

**Written before any new accuracy exists.** No mechanism B prediction on the
evaluation split has been computed, scored, or printed. The only measurements
that informed this amendment are the calibration-split design diagnostics of
Phase 2.2c, reported in `reports/phase2c_pair_design.md`, which are disclosed as
such below and are not evidence for any hypothesis.

## Why this amendment exists

Two findings force it, one from each of the last two passes.

**From 2.2b.** The frozen mechanism pair is nested. A test surface form that
occurs in the train history sits at similarity exactly 1.0, the maximum of any
similarity function, so any retriever taking the single nearest train form takes
that form and resolves the same author. Exact match is contained in every
single-nearest retriever, whatever the metric or cutoff. `exact wins` was
unreachable, and measured zero on 199,713 test signatures in both metric arms.
Mechanism B must therefore vote over a neighbourhood rather than take the nearest
form.

**From 2.2c.** A precision-first rule cannot win a block whose train history
names a single author, because any non-empty pool returns that author and the
rule's only possible difference is to abstain. This holds for **any** pair of
mechanisms that assign an author from the block's own history, not only for ours.
Consistency therefore necessarily carries some winner information, and H2 as
originally worded, that ADS does not predict which mechanism wins, cannot be true
of any pair in this family. It is not rescuable by changing mechanisms.

The claim is therefore rebuilt rather than repaired. Consistency is given the
role the structure forces on it, gating whether the choice is live, and surface
stability keeps the role the original H3 gave it, directing the choice where it
is live. Neither signal alone predicts the winner, which is the contribution.

---

## Section 2, replaced: hypotheses

### H1, accuracy (validity check, not a contribution)

Across evaluation blocks, train-only ADS is positively associated with each
mechanism's own held-out accuracy, separately for the exact-evidence rule (A) and
the k-nearest-vote retriever (B, k = 5). Stated as a validity check: it confirms
that per-block ADS behaves like the established dataset-level homonymity effect
reported by Kim and Kim (2020) and in the S2AND paper. Reported as such, not as a
finding.

### H2, consistency gates whether the choice is live

Train-only ADS governs whether the mechanism choice is decidable at all. Holding
SV fixed, the share of blocks with a decided winner, that is the rule wins or
k-NN wins as opposed to tie or undecided, declines as ADS rises, approaching zero
in the top ADS band, while remaining non-trivially positive in the lower ADS
bands. In words: high consistency means it does not matter which mechanism you
use, low consistency means the choice is live.

The decline toward zero at ADS = 1.0 is **partly structural** and is reported as
such in those words, because a block naming one author returns that author from
any non-empty pool, so only abstention can differ. The load-bearing empirical
content is the gradient across the rest of the range and the existence of a
non-trivial decidable region at low ADS, neither of which is structural.

**Role-separation check.** ADS's association with decidability is reported
alongside SV's, and H2 expects ADS to be the stronger driver. Operationalized in
resolution 5 below.

### H3, surface stability directs the choice, consistency does not

Among blocks where the choice is decidable, train-only surface stability governs
which mechanism wins, and consistency does not. Two parts, both required.

- **Direction by SV.** Holding ADS fixed within a band below 1.0, the decided
  pooled winner's identity changes across SV bands, and the change is a genuine
  reversal as defined in section 8, that is two SV bands with decided pooled
  verdicts of opposite identity, not only a change in gap magnitude.
- **Non-direction by ADS.** Holding SV fixed, the decided pooled winner's
  identity does not change across ADS bands. This is the original
  selection-blindness claim, now scoped to decidable blocks at fixed surface
  stability, which is where it can be true.

H3 additionally requires the SV reversal to survive the initialization control of
section 9, that is to be present with SV_resid and not only with raw SV, to hold
with the Jaro-Winkler metric arm, and to generalize beyond inspire under the
section 11 rule.

### Contribution

The contribution is the conjunction of H2 and H3: two design-time, label-free
signals play separable roles, consistency setting whether the choice matters and
surface stability setting which way to choose, and neither signal alone predicts
the winner. This is distinct from Kim and Kim (2020), who report a single
dataset-level gap magnitude modulated by a manipulated surface variable, with no
decidability axis, no per-block interaction, and no design-time signal. See
`reports/kim2020_positioning.md`.

### Out of scope for 2.2, carried over unchanged

The two-signal selector remains Phase 2.3 and the original section 2 text
governing it stands: it is reported only beside an ADS-only selector and an
SV-only selector, on held-out blocks, and the dual-signal claim survives only if
the two-signal version beats both by more than the same delta. A fixed
always-k-NN and a fixed always-rule policy are reported as floor baselines.
Charter invariant 4's two baselines are now load-bearing rather than defensive,
since this amendment expects both signals to carry part of the winner.

---

## Sections 4 and 7, amended: mechanism B and its parameter

**Mechanism A, the exact-evidence rule, is unchanged.** Original section 4's
exact-match definition, its metric, its coverage reporting and its tie-break all
stand verbatim.

**Mechanism B is now the k-nearest-vote retriever**, replacing the thresholded
fuzzy arm. For a test signature, pool the nearest training signatures in the
block by similarity of their surface form to the test form, whole forms at a
time, until the pool holds at least k training signatures; if the block holds
fewer than k training signatures, the pool is the whole block. Vote the pooled
signatures' authors, signature-weighted, and assign the winner. **B does not
abstain** when the block has at least one training signature, which on the
primary analysis population is every block, so abstention sits entirely on the
rule's side. Coverage is still reported for both mechanisms at every level at
which accuracy is reported.

**k is fixed by definition at k = 5. It is not calibrated by maximizing
accuracy.** This supersedes section 7's accuracy-maximizing cutoff calibration,
which no longer applies: B has no similarity cutoff, and B's accuracy is monotone
toward the single-nearest limit, which is exactly the nesting that killed 2.2b.
Section 7 is therefore void for 2.2e and no cutoff is calibrated. Section 6's SV
and SV_resid band edges, calibrated under the same protocol and frozen in
`phase2b_constants.py` at commit `5e13e38`, **carry over unchanged and are not
recomputed**.

**Disclosure.** k = 5 was chosen on the calibration split for contest balance,
not for accuracy, from the counts in `reports/phase2c_pair_design.md`. That is a
calibration-split design choice of exactly the kind the calibration split exists
for, and it is disclosed here rather than presented as arbitrary.

**The k sensitivity curve is mandatory.** Every H2 and H3 outcome is recomputed
at k in {2, 3, 5, 10} and reported beside the primary. An outcome that holds at
k = 5 and flips elsewhere on the curve is reported as k-dependent and treated as
Partial, not Supported. This is the same rule section 8 applies to delta.

**Metric-family robustness arm, restated.** Section 9's Jaro-Winkler arm becomes
simpler under this amendment: it is the same k-nearest vote with Jaro-Winkler
similarity in place of normalized Levenshtein, and it calibrates nothing, because
there is no cutoff to calibrate. Everything else in section 9 stands, including
SV_resid, the INIT stratification, the 5 by 4 grid, and the three structural
outcomes.

**Section 8 carries over unchanged**, except that the verdict `fuzzy wins` is
renamed `k-NN wins` and `exact wins` is renamed `rule wins`. The four verdicts
are `rule wins`, `k-NN wins`, `tie`, `undecided`; the per-block paired bootstrap,
the block-resampling pooled bootstrap, B = 2000, the seeds, the primary margin
delta = 0.05 and the {0.02, 0.03} robustness curve are all as originally frozen.
The renames are cosmetic: the same mechanisms under their new names.

**Section 3 carries over unchanged.** The primary analysis population stays
blocks with `n_train >= 2` and `n_test >= 1`. ADS = 1.0 blocks are **not**
excluded: H2 needs them, because the decline of decidability into that band is
what H2 is about. H3 is scoped to ADS bands below 1.0 by its own wording, which
is the right place for that restriction.

---

## Section 10, replaced: falsification table

**Order of evaluation, carried over.** Inconclusive is evaluated first for every
hypothesis. If the Inconclusive power floor is met, the outcome is Inconclusive
regardless of the other rows. An all-tie or all-undecided set of bands is never
read as support for H2 or H3.

"Generalizes" always means the section 11 rule: the result holds in the pooled
non-inspire analysis and in a majority of qualifying non-inspire datasets, where
a dataset qualifies at 100 or more blocks in the primary analysis population.

### H1, accuracy

| outcome | rule |
| --- | --- |
| Supported | Spearman of train-only ADS with held-out accuracy is positive with a 95% block-bootstrap interval excluding 0, for **both** mechanisms, and it generalizes. |
| Partial | Positive and interval-excluding-0 for one mechanism but not both, or pooled but not generalizing. |
| Not supported | Interval includes 0 for both mechanisms, or the correlation is negative with an interval excluding 0 for either. |
| Inconclusive | Fewer than 500 blocks in the primary analysis population, or fewer than 2 qualifying non-inspire datasets. |

### H2, consistency gates decidability

| outcome | rule |
| --- | --- |
| Supported | Holding SV fixed, the decided-winner rate is non-increasing across ADS bands in the majority of eligible SV bands, **and** is strictly lower in the top ADS band than in the bottom, **and** at least one ADS band below 1.0 holds a non-trivial decidable region (resolution 6), **and** ADS is the stronger driver of decidability than SV (resolution 5), **and** this holds in the pooled non-inspire analysis. |
| Partial | The gradient holds pooled but not per-dataset; or the decidable region exists but the gradient is weak or non-monotone; or SV rivals ADS as a driver of decidability. |
| Not supported | The decided-winner rate does not decline with ADS, being flat or rising; or no ADS band holds a non-trivial decidable region, meaning the choice is never live, as in 2.2b. |
| Inconclusive | Fewer than 2 ADS bands and 2 SV bands with 30 or more blocks and a decided pooled verdict. |

### H3, surface stability directs the choice

| outcome | rule |
| --- | --- |
| Supported | Within at least one ADS band below 1.0 with 30 or more blocks per SV cell, two SV bands have decided pooled verdicts of opposite identity, a genuine reversal; **and** holding SV fixed, winner identity does not reverse across ADS bands, or all such verdicts are tie or undecided; **and** the reversal is present with SV_resid; **and** it holds with the Jaro-Winkler arm; **and** it generalizes past inspire. |
| Partial | A reversal with raw SV but not SV_resid, meaning the surface axis is forename initialization, Kim and Kim's variable; **or** a tie-crossing rather than a reversal; **or** an SV reversal that holds but ADS also reverses the winner at fixed SV, which is impure role separation; **or** a reversal that holds pooled but does not generalize; **or** one that holds with edit distance but not Jaro-Winkler; **or** one that is margin-dependent or k-dependent. |
| Not supported | **Gap compression only.** The magnitude of the gap varies with SV but no SV band pair is decided in opposite directions in any ADS band, in any qualifying analysis. This is an honest, publishable outcome and is reported in those words: a per-block, design-time, measured version of Kim and Kim's gap-compression finding, obtained with two simple mechanisms, together with the methodological point that single-nearest retrieval subsumes exact match. The two-signal dissociation claim is dropped and the paper retargets to this result. |
| Inconclusive | Fewer than 2 SV bands with 30 or more blocks and a decided pooled verdict inside any single ADS band. |

### Outcomes that are explicitly acceptable, not failures to hide

The original section 10 list carries over, with one entry updated and one added.

- **The gap only compresses, there is no reversal.** H3 not supported. Unchanged.
- **The co-signal does not help.** In 2.3, the SV-only selector matches or beats
  the two-signal selector out of sample, or neither beats the better fixed
  policy. Unchanged.
- **SV is forename initialization.** Effect present in SV, absent in SV_resid.
  Unchanged.
- **The choice is never live.** Updated from "the low-SV region is structurally
  tied". If no ADS band holds a non-trivial decidable region, H2 is Not supported
  and the paper reports that on this substrate the mechanism choice does not
  matter anywhere, which is itself a usable practitioner finding and is reported
  in those words.
- **Consistency directs as well as gates.** New. If ADS reverses the winner at
  fixed SV, the role separation is impure, H3 is Partial, and the paper reports a
  two-signal interaction without clean role assignment rather than claiming one.
- **ADS predicts gap magnitude.** Expected, consistent with Kim and Kim, and not
  a refutation of anything here. Unchanged.
- **The primary analysis population is too thin.** Inconclusive is a permitted
  verdict and will be used rather than reaching for a smaller threshold.
  Unchanged.

---

## Resolutions of ambiguity, fixed now

Six places where the revision as handed over was under-determined or drifted from
what 2.2c measured. Each is resolved here, before any number exists, rather than
being settled during the run. **All six are flagged for review.** Any of them can
be overruled before 2.2e starts; none can be changed after it.

**Resolution 1, what "k nearest" counts.** The revision says "retrieve the k
nearest training forms". Fixed here as the **signature-counted** version stated
in the section 4 amendment above: forms are added whole, nearest first, until the
pool holds at least k training signatures. The two readings differ whenever a
form carries more than one signature, which is the common case, and the k = 5
balance evidence in `reports/phase2c_pair_design.md` was produced under the
signature-counted reading. The form-counted reading has not been checked for
two-sidedness and is not adopted.

**Resolution 2, tie-breaking inside mechanism B.** The revision says "break ties
toward the nearest form". Not adopted, for two reasons: it is under-determined
when two forms are equidistant, and it would make the two mechanisms use
different tie-breaks, which turns part of the winner contest into a comparison of
tie-break rules. **The frozen original section 4 chain is used for both
mechanisms**: most frequent author inside the pooled evidence, then most frequent
author inside the block, then the lexicographically smallest author id. This is
what 2.2c measured.

**Resolution 3, the nesting limit is k = 1, not k = 2.** The revision calls k = 2
"the single-nearest limit". Under the signature-counted definition the exact
single-nearest-form retriever is k = 1. k = 2 is close to it but not identical,
and measured 181 rule wins against 736 on the calibration split, against 546
against 744 at k = 5. The substantive point stands unchanged: accuracy is
monotone toward the nesting limit, so accuracy-maximizing calibration would walk
the design back into 2.2b. k = 1 is not on the sensitivity curve, because it is
the known-degenerate case and its result is already reported in
`reports/phase2b_boundary.md`.

**Resolution 4, what "decided" means in H2.** Decidability is measured with the
**per-block** paired-bootstrap verdict of section 8, not the pooled band verdict.
The decided-winner rate of a cell is the share of that cell's blocks whose
per-block verdict is `rule wins` or `k-NN wins`. This is the quantity section 8
already requires under "Verdict distribution", so no new statistic is introduced.
H3's reversal test continues to use the **pooled** band verdict, as the original
section 9 specifies. The two hypotheses therefore read different rows of the same
frozen table, which is deliberate: decidability is a property of a population of
blocks, winner identity is a property of a band.

**Resolution 5, "ADS is the stronger driver of decidability".**
**Superseded by Addendum 1a, 2026-09-18, at the end of this file**, because the
range measure below is biased by the grid not being square. The text is kept for
the record. Operationalized
as a comparison of ranges over the frozen 5 by 4 grid. For each SV band with 30
or more blocks, take the range, maximum minus minimum, of the decided-winner rate
across its eligible ADS cells, and average those ranges over SV bands; do the
same with the axes swapped. **ADS is the stronger driver if its averaged range is
the larger.** Cells under 30 blocks are excluded, as everywhere else. Reported as
both numbers, never as the verdict alone.

**Resolution 6, "a non-trivial decidable region".** Fixed as: **at least one ADS
band below 1.0, holding 30 or more blocks, in which 30 or more blocks have a
decided per-block verdict.** An absolute count, not a rate, and it reuses the
section 3 minimum of 30 rather than introducing a new threshold. It is set as a
count because it is also exactly what H3 needs in order to have material to
analyse, so the two hypotheses share one floor.

---

## Reproducibility and invariant checks for 2.2e

The original section 12 carries over, with the mechanism names updated.

- All seeds stay at 20260918. The split of section 3 is unchanged, so the
  calibration and evaluation blocks of 2.2e are the same blocks as 2.2b's.
- No test signature reaches any signal, any band edge, or the choice of k. The
  k = 5 disclosure above concerns calibration-split blocks only. Per charter
  invariant 3.
- The winner is defined only by labelled accuracy. Neither ADS nor SV nor
  SV_resid appears in either mechanism definition. Per charter invariant 2.
- Two mechanisms only, neither trained. Per charter invariant 6.
- Offline, CPU-only, deterministic, no API key. Per charter invariant 7.
- Mechanism B gets an assert-based self-check in the module that defines it,
  including the case that fixes resolution 1 and the case that fixes
  resolution 2.
- The 2.2b numbers are not recomputed, not overwritten, and not withdrawn. They
  stay in `reports/phase2b_boundary.md` as the record of the nested pair and are
  reported in the paper beside the 2.2e numbers.

---

## Addendum 1a to Amendment 1, 2026-09-18: resolution 5 replaced

**Status: binding. Supersedes resolution 5 of Amendment 1 above.** Append-only,
in the same style as the amendment it revises: nothing above this line is edited
or removed, and resolution 5 carries a pointer here.

**Still before any measurement.** No mechanism B prediction on the evaluation
split exists anywhere under `phase2/`. Nothing in this addendum was informed by a
result, because no result for the amended design exists.

### Why resolution 5 had to change

Resolution 5 tested "ADS is the stronger driver of decidability than SV" by
comparing the averaged **range**, maximum minus minimum, of the decided-winner
rate across each axis of the frozen 5 by 4 grid. That measure is biased in favour
of the conclusion H2 needs. The range is an order statistic, so its expectation
grows with the number of values it is taken over, and the grid is not square: ADS
has 5 bands and SV has 4. ADS therefore enters the comparison with a built-in
edge that has nothing to do with the data. A hypothesis should not be handed a
measure that tilts toward supporting it.

### The replacement test, fixed now

**Primary measure: a one-way variance decomposition, eta-squared style.**

Let the observations be the **eligible cells** of the frozen 5 by 4 ADS-by-SV
grid, where eligible keeps the existing meaning of 30 or more blocks. Let `p_c`
be the decided-winner rate of cell `c`, defined as in resolution 4, and let
`p_bar` be the unweighted mean of `p_c` over eligible cells.

    SS_total    = sum over eligible cells of (p_c - p_bar)^2
    SS_ADS      = sum over ADS bands b of  m_b * (p_bar_b - p_bar)^2
    SS_SV       = sum over SV bands s of   m_s * (p_bar_s - p_bar)^2

where `m_b` is the number of eligible cells in ADS band `b` and `p_bar_b` their
unweighted mean, and likewise for SV. Then

    eta2_ADS = SS_ADS / SS_total        eta2_SV = SS_SV / SS_total

Each is an ordinary one-way effect size in [0, 1], computed over the same
observations, so the comparison is invariant to the number of bands on either
axis. **ADS is the stronger driver under the primary measure if
`eta2_ADS > eta2_SV`.**

**Secondary measure: the averaged-range test of the original resolution 5**, kept
verbatim and unchanged. It is no longer the test; it is the second of two
conditions.

**The combined rule, which is what section 10's H2 row now means by "ADS is the
stronger driver of decidability than SV".**

| both measures | H2 role-separation clause |
| --- | --- |
| ADS larger under the variance decomposition **and** under the averaged range | condition met, H2 may be Supported if its other clauses hold |
| ADS larger under one measure but not the other | **Partial**, never Supported, and the disagreement is reported with both pairs of numbers |
| ADS larger under neither | the clause fails; H2 falls to Partial under "SV rivals ADS as a driver of decidability", or lower if another clause also fails |

Both pairs of numbers, `eta2_ADS` against `eta2_SV` and the two averaged ranges,
are reported in every case. Neither is ever reported as a verdict alone.

### Fixed choices inside the primary measure

**Cells are unweighted.** Each eligible cell contributes one observation,
regardless of how many blocks it holds. The alternative, weighting each cell by
its block count, is **not** used to decide anything, for a stated reason: the
ADS = 1.0 row holds roughly three quarters of the primary analysis population,
and its low decidability is the part of H2 that Amendment 1 already concedes is
partly structural. Block-weighting would give that one row decisive leverage over
exactly the comparison H2 needs ADS to win, which is the same kind of tilt this
addendum exists to remove. The block-weighted decomposition is computed and
reported beside the unweighted one as a diagnostic, and **decides nothing**.

**Degenerate cases.** If `SS_total` is zero, that is every eligible cell has the
same decided-winner rate, the ratios are undefined and the role-separation clause
is **Inconclusive**, which under the Order of evaluation rule carries H2 to
Inconclusive. The same applies if fewer than two levels of either factor contain
an eligible cell, or if fewer than four eligible cells exist in total.

### What this does not fix, stated plainly

The ADS = 1.0 row still carries a partly structural decidability collapse, and it
is still one of the five rows entering the primary measure. Unweighting stops it
dominating, but it does not remove it, and no variant that removes it is
pre-registered here, because deleting the row would test a different hypothesis
from the one H2 states. The consequence is that a reader must take the H2 verdict
together with Amendment 1's own statement that the decline into the top ADS band
is guaranteed rather than discovered. Both go in the paper, adjacent, not one
without the other.
