# Kim and Kim 2020: what they did, and how our study differs

Phase 2.2a, step 1. Written before the Phase 2.2 pre-registration was frozen, as
the Phase 2.1 access recon required. Nothing in this pass measured anything; this
is a reading of prior work and a positioning statement.

## What was read, and its provenance

Jinseok Kim and Jenna Kim, "Effect of forename string on author name
disambiguation." *Journal of the Association for Information Science and
Technology* 71(7), 839-855 (2020). DOI 10.1002/asi.24298. Preprint
arXiv:2102.03250, submitted 5 February 2021, categories cs.DL, cs.IR, cs.LG.

Read from the author preprint held locally at `phase2/Kim and Mim paper for
review.pdf`, 25 pages, which carries the header "This is a pre-print of a paper
published in the Journal of the Association for Information Science and
Technology" with the full JASIST citation. Title, authors, and journal reference
were checked against the arXiv abstract page and match. The full body, appendices
A and B, and the reference list were read, not the abstract alone.

The preprint says "three labeled datasets" once, on its page 4, where the Methods
section, the results, and the conclusion all use four. That is a transcription
slip in the preprint, not a substantive ambiguity.

## What they did

**Question.** How much do author forenames contribute to author name
disambiguation, for a simple string-matching heuristic and for feature-based
machine learning, and how does that contribution change as forenames get more or
less complete?

**Data.** Four labelled author-disambiguation datasets: PENN (5,018 name
instances), KISTI (41,673), AMINER (7,528), GESIS (29,965 instances of 2,580
authors from its Evaluation Set). In every one of them 95.7% to 98.9% of
instances already carry at least one full forename, so the datasets as shipped
sit at the clean end of the surface axis.

**The manipulation, which is the core of the design.** They do not measure
surface variation as they find it. They create it. Two manipulations:

1. *Full-forename ratio.* In each dataset they choose a random p percent of name
   instances to keep their full forenames and initialize the forenames of the
   rest, for p from 0 to 100 in steps of 10, repeating the random selection and
   the data split 10 times per value of p. At p = 0 every forename in the corpus
   is an initial.
2. *Forename truncation.* Every forename string is truncated to its first n
   characters, for n from 1 to 10, plus an untruncated "ALL" setting.

**Blocking.** Full surname plus first forename initial. This is the same blocking
family we use, and it means the manipulation operates strictly inside blocks:
initializing a forename never moves an instance to a different block.

**Mechanisms compared.**

- *Heuristic (String).* Test-set instances that match on all available name
  strings, surname plus forename, are assumed to be the same author. No training,
  no threshold.
- *Algorithmic.* Pairwise similarity over four features, forename, coauthor,
  title, and venue, each as a TF cosine over character 2 to 4-grams. Five
  classifiers: Random Forest, Naive Bayes, Logistic Regression, SVM, and Gradient
  Boosting. Classifier match probabilities feed hierarchical agglomerative
  clustering. Data split 50/50 into train and test.

**One detail of their protocol matters for how their headline comparison should
be read.** The clustering threshold is chosen "by trying various distance values
between 0 and 1 in each block and choosing one that produces the best clustering
result (measured by B-Cubed F1) for the block." That is a per-block threshold
selected against the evaluated outcome, so the algorithmic arm is given per-block
oracle tuning while the heuristic arm has no parameter at all. Their statement
that string matching cannot defeat machine learning is therefore a statement
about a heuristic with zero tuning against an ML arm tuned per block on the thing
being scored.

**Metric and unit.** B-cubed precision, recall, and F1, computed over a whole
test set, averaged over 10 iterations per setting. The reported unit of analysis
is the dataset crossed with the manipulation setting. Blocks appear only as an
internal computational device and as the level at which the oracle threshold is
picked. No block-level result is reported.

**Also reported.** Random Forest impurity-based feature importance for the four
features at each setting; the pairwise composition of four ambiguity types,
homonym, synonym, SN-SA, DN-DA, at each setting; and in Appendix A a record
linkage demonstration on 3,188 MEDLINE-ORCID instances restoring initialized
forenames to full ones.

## What they found

**Both mechanisms improve as forenames get fuller, in the two datasets that have
room to improve.** In PENN, heuristic precision rises from below 0.1 at 0% full
forenames to 0.94 at 100%, and the algorithmic arms rise from roughly 0.6 to 0.7
up to 0.94. KISTI behaves the same way. Heuristic recall traces a U shape,
because at intermediate ratios an author's instances split into one initialized
cluster and one full-forename cluster.

**The headline is gap compression, not a winner reversal.** Their result is that
the *margin* by which machine learning beats string matching shrinks as full
forenames become more common. Their own summary sentence: performance gains by
algorithmic disambiguation "are pronounced when many forenames are initialized or
homonym is prevalent" and "as the ratios of full forenames increase, however,
they become marginal compared to the performances by string matching." The
conclusion states the ordering that holds throughout: for datasets where authors
are distinguishable by full forenames, "sophisticated string-matching techniques
may produce decent performances although they cannot defeat feature-based machine
learning."

**String matching never beats the machine-learning arm on the summary metric, in
any of their four datasets, at any setting.** On B-cubed F1, against the best
algorithmic arm, the heuristic is below the algorithms everywhere. Two local
crossings exist on the component metrics and should be stated rather than
smoothed over, because they are the closest thing in their data to a reversal:

- In PENN, on *precision only*, the heuristic overtakes Naive Bayes above the 60%
  full-forename ratio. Naive Bayes is the weakest of their five classifiers, and
  the crossing does not occur against Logistic Regression or Random Forest.
- In PENN, on *recall only*, the algorithmic arms surpass the heuristic only above
  the 50% ratio, so below 50% the heuristic has the higher recall. That crossing
  is degenerate: at 0% full forenames the heuristic puts nearly everything in one
  cluster, which buys recall near 0.99 at precision below 0.1.

Neither crossing survives into F1, and neither is presented by the authors as a
change of winner.

**The two homonym-centric datasets are flat.** In AMINER and GESIS, where most
instances in a block share the same name string, increasing full forenames barely
moves the heuristic at all, the algorithmic arms are close to flat, and the two
never converge. The algorithmic arms sit above the heuristic across the whole
range. This is their consistency-axis result: where homonymity is high, the gap
is large and stays large.

**Feature importance tracks the manipulation.** In PENN, forename importance is
exactly zero at 0% full forenames, which is mechanically necessary since every
forename in a block is then the same string, and rises to overtake venue, title,
and coauthor at the 70%, 80%, and 90% settings. In AMINER it peaks around 0.25 at
the 50 to 60% setting and stays small throughout.

**Truncation saturates early.** Performance stops improving after about 5
characters of forename for KISTI and 6 for PENN.

**What they conclude practically.** Restore initialized forenames to full strings
by record linkage; evaluate any new method under both initialized and full
forename settings before claiming an improvement from algorithmic sophistication;
use string matching as a baseline; and characterize the name ambiguity in a
dataset before choosing a method. That last recommendation is the closest they
come to our territory, and it is offered as advice to a human reader, not as a
measurable signal or a procedure.

**A limitation they state, which is directly relevant to us.** They address only
the initialization form of synonymy and explicitly exclude other kinds, naming
"different by edit-distance, flipped ordering of forename tokens" and noting the
effect may not be negligible for German, Hispanic, and Slavic names.

## How our study differs, point by point

| | Kim and Kim 2020 | This study |
| --- | --- | --- |
| Surface axis | Synthetically manipulated. They set the full-forename ratio and truncate strings. | Measured as found. SV is the expected normalized edit distance between two signatures of a block, computed on the printed name, never set by us. Frozen in `phase2/s2and_blocking.py` before any measurement existed. |
| Is the surface axis available at design time | No. The ratio is a property of their experimental arm, not something a practitioner can read off their own data. | Yes, and this is the point. SV is label-free and computed from history only, so it is available before any decision is made. |
| Consistency axis | Homonymity appears as an outcome they describe, at dataset level, via a pairwise ambiguity-type composition and via which datasets are "homonym-centric". | ADS is a per-block purity statistic computed train-only, with a measured distribution across 18,984 blocks, cross-checked against S2AND's own homonymity facet at Spearman -0.818. |
| Unit of analysis | The dataset, crossed with the manipulation setting. Four datasets, eleven ratio settings. | The block. Roughly 19,000 small classification problems, each with its own ADS, its own SV, and its own held-out test. |
| Mechanisms compared | String matching against feature-based machine learning, on four features with five classifiers and per-block oracle-tuned clustering. | Exact match against fuzzy retrieval. Two simple mechanisms in the same family, one global calibrated cutoff for fuzzy and no parameter for exact. |
| Task formulation | Clustering, scored by B-cubed against truth clusters. | Assignment of a held-out signature to an author, against a per-block historical knowledge base, scored by accuracy with abstention counted as incorrect and coverage reported separately. |
| Winner | Not a construct in their paper. They report gap magnitudes. No statistical winner test, no equivalence margin, no tie category. | A pre-registered construct: per-block paired bootstrap on the accuracy difference, a fixed practical-equivalence margin, and four verdicts including a distinct tie and a distinct undecided. |
| Selector | None, and selection is not framed as a problem. | A design-time selector is the constructive half of the claim, evaluated held out against ADS-only and SV-only baselines. Phase 2.3, not 2.2. |
| Generalization | Four datasets, each analysed separately. | Seven S2AND sub-datasets in one format, with mandatory per-dataset reporting and a pooled non-inspire row. |

The one-sentence version: they show that if you degrade forenames on purpose, the
margin between a heuristic and machine learning widens, at dataset level, with no
change of winner and no selector. We ask whether a label-free measurement you can
take at design time, per block, tells you which of two mechanisms to use, and
whether the consistency statistic that predicts each mechanism's own accuracy is
blind to that choice.

## Where our claim risks collapsing into a per-block replication of theirs

These are the honest failure modes. Each one is written into the falsification
table in `phase2/PREREG.md` as a pre-registered, reportable outcome rather than
something to be discovered and quietly reframed later.

**1. SV may be mostly forename initialization.** Our SV is a general edit distance
over the printed name, but the largest single source of within-block name
variation in bibliographic data is exactly the thing they manipulated, "J. Smith"
against "John Smith". If SV turns out to be a proxy for the per-block
full-forename ratio, then "SV predicts the winner" is a finer-grained,
observational restatement of their Figures 2 and 3, and the only novelty left is
the unit of analysis and the design-time framing. This is the sharpest risk.
Pre-registered control: the whole SV analysis is repeated with SV_resid, an SV
computed after mapping every surface form to its fully initialized canonical
form, so that initialization contributes exactly zero to it and only spelling,
diacritic, hyphenation, middle-name and suffix variation remain. If the effect
lives only in SV and not in SV_resid, we report that the surface axis is
initialization, and we say so in the paper.

**2. Gap compression without reversal is their result, not a new one.** If the
exact-minus-fuzzy gap shrinks as SV rises but never crosses zero, we have
reproduced gap compression at block level with two different mechanisms. That is
a real but modest contribution and must not be written as a dissociation.
Pre-registered: gap compression, tie-crossing, and winner reversal are three
separately defined outcomes, decided by a fixed rule, and "compression only" is
listed as H3 not supported.

**3. H1 is close to already known.** That accuracy falls as homonymity rises is
visible in their AMINER and GESIS results and in the S2AND paper itself. H1 is a
construct-validity check for us, not a finding, and the pre-registration says so
in those words.

**4. H2 must be about sign, not magnitude.** Their result that the gap widens when
homonymity is prevalent is a statement about gap magnitude. Ours is a statement
about which mechanism wins. Those are compatible, and we could easily find that
ADS predicts the magnitude of our gap too. If we phrase H2 loosely as "ADS says
nothing about the comparison" and then find a magnitude relationship, the claim
looks refuted when it is not, and if we phrase it after seeing the data it looks
rescued. Pre-registered: H2 is about the identity of the decided winner at fixed
SV, and the ADS-magnitude relationship is reported alongside it as an expected,
previously reported effect.

**5. Exact against fuzzy is a smaller comparison than string against machine
learning.** Both of our mechanisms are string-based. A reviewer can fairly say
that a winner change between exact and fuzzy is a narrower phenomenon than a
winner change between a heuristic and a learned model, and that Kim and Kim
tested the harder version and found no reversal. We accept that framing: the
contribution is the design-time selection signal and its dissociation from the
consistency signal, demonstrated on the simplest honest pair of mechanisms, not a
claim that simple methods beat learned ones.

**6. Exact against fuzzy risks being definitionally linked to SV.** If a block's
history contains a single surface form, exact match fires on any test signature
carrying that form and fuzzy retrieves the same neighbour, so the two mechanisms
may return identical predictions and produce a structural tie rather than a win
for exact. The interesting half of H3 may therefore be one-sided: fuzzy wins at
high SV, ties at low SV. Pre-registered: the rate at which the two mechanisms
produce identical predictions is reported per SV band, so a reader can see how
much of the low-SV region is genuine equivalence rather than a measurement
artifact.

**7. Our stability signal and our fuzzy mechanism share a metric.** SV is built
from normalized edit distance and the fuzzy mechanism retrieves by the same
distance family. The winner is defined by labelled accuracy, so this is not the
tautology invariant 2 forbids, but it is a fair criticism. Pre-registered
robustness arm: rerun the fuzzy mechanism with Jaro-Winkler similarity and report
whether the SV-to-winner relationship survives a change of metric family.

## Consequences for related work

Kim and Kim 2020 belongs in the related-work section, in the representation and
surface-form robustness stream, cited as the nearest prior result on the surface
axis and as the source of the gap-compression finding we are distinguishing
ourselves from. It was not in the spec's related-work list. The Phase 2.5 writing
pass must place it there and must state the distinction in the body, not only in
a citation. Their Backes (2018) point, that string-based matching results should
be baselines in author name disambiguation evaluation, is also worth carrying,
since our exact-match arm is exactly such a baseline.
