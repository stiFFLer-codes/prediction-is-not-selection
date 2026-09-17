# Phase 2 spec, ADS-Cascade

Reference document for Phase 2. The charter (CLAUDE.md) sets the boundaries;
this fills them with the questions to answer and the method. Read both.

## 1. Paper identity

A venue-neutral research paper. The unattackable core is a decomposition shown
on real data: historical decision consistency (cluster purity, equivalently
majority-vote agreement, here called ADS) strongly predicts each classification
mechanism's own accuracy, but does not predict which mechanism wins a
head-to-head comparison, because the winner is governed by surface-form
(representation) stability, which the consistency signal is blind to. The
constructive half tests whether a measured surface-stability co-signal recovers
the selection the consistency signal cannot. Sibling in framing to Tan (2026),
"Beyond ROC-AUC," which shows the same signal-versus-selection gap for model
choice under decision economics; our blind axis is representational rather than
economic.

## 2. Data (finalized)

Primary: WDC Product Data Corpus (Web Data Commons), the public product-offer
corpus extracted from Common Crawl and grouped into clusters by GTIN and MPN
identifiers. Offers of the same product from different shops give repeated entity
keys with natural, un-engineered surface variation in their titles. Category
labels are available via the WDC product-categorization gold standard (24
categories, cluster-to-category mapping) and the cleansed PDC2020-C corpus. Start
from a manageable public subset (a category-restricted slice, or the WDC
Products benchmark variants and categorization gold standard), not the full
98M-offer dump. Everything is a public offline download from webdatacommons.org.

Why this one: it is the only genuinely public source that carries all three
properties we need at once, repeated keys, real cross-vendor surface noise, and
labels. It replaces both the synthetic generator and the Romanian case study.

Secondary (breadth and contrast): one Magellan "Dirty" benchmark (Dirty
Walmart-Amazon or Dirty DBLP-ACM), available from HuggingFace
(lighteval/EntityMatching) or Zenodo record 8164151. The clean-versus-dirty pair
is the real-data analog of the old CLEAN and VARIED contrast, and a second
domain guards against a single-dataset result, which is Tan's main weakness.

Rejected: public financial-transaction and payee categorization data.
Conceptually the perfect fit, but the public versions are overwhelmingly
synthetic (the popular Kaggle banking-transaction sets are explicitly
simulated), and the one genuinely real labeled corpus is gated behind an email
request. Using synthetic transaction data would reintroduce the exact toy-
benchmark criticism we are escaping. Keep the "AMZN MKTPLACE PMTS" example only
as narrative motivation in the introduction, never as evidence.

Demoted: the Phase 1 synthetic generator survives as a controlled causal-
isolation probe (one secondary section), used to turn the surface-noise knob in
a way real data cannot, which is a capability Tan lacks. It is never primary
evidence.

## 3. The task-definition problem (resolve this first)

For the paper to work, both axes must be alive on the real data, and that
depends entirely on how we define the label and the key. This is the single
highest-risk design decision. Two candidate framings:

Framing A, label = category, key = cluster. Each cluster (one product) maps to
one gold category, so per-cluster category purity is near 1.0 everywhere and ADS
has almost no range. The "ADS predicts accuracy" axis dies. Do not assume this
framing works; it probably does not.

Framing B, label = entity identity, key = a normalized surface or blocking key.
ADS = for a normalized key, how consistently it resolves to one cluster. Generic
or ambiguous strings resolve to multiple clusters (low ADS); distinctive strings
resolve to one (high ADS). This yields a real ADS range, and the raw surface
variation within a cluster drives the exact-versus-fuzzy outcome. This is the
intended primary framing.

Gate 2 measures the ADS distribution under both framings on a subset and reports
the histograms before anything downstream is built. Commit to a framing only
after seeing real numbers. If neither yields usable ADS range, stop and rethink
the data, not the paper.

## 4. The two axes

ADS (axis 1): per-key label purity computed on the training split only
(design-time, history-only, as in Phase 1). Report its distribution first.

Representation stability, RS (axis 2): a per-item, measured signal of surface-
form stability, computed at design time from the historical strings for a key.
Candidate signals to prototype (you choose and may add): normalized edit
distance or Jaro-Winkler dispersion among a key's historical surface forms,
token-set variability, character n-gram divergence, length variance. RS must be
measured, never set, and never defined using the winner.

## 5. Mechanisms and winner definition

Two mechanisms, carried over in spirit from Phase 1: exact-match lookup (context-
scoped then global, abstain on miss) versus fuzzy retrieval (rapidfuzz-style
lexical similarity, cutoff calibrated once on a disjoint split, never abstains at
the cutoff). Primary metric is whole-set accuracy with abstention counted as
incorrect, and coverage reported (the rules-abstain versus retrieval-never-
abstain asymmetry is a first-class result, not normalized away). Winner per
condition by paired bootstrap on the accuracy difference with a practical-
equivalence margin, ties a distinct category, exactly the Phase 1 rigor.

## 6. Experiments and gates

1. Scaffold and WDC ingest. Load a manageable subset into (surface_string, key,
   label) form. No experiments.
2. ADS-range sanity check (hard gate). Report ADS histograms under Framing A and
   Framing B. Commit to a framing. Stop for review.
3. Boundary finding on real natural noise. Show ADS predicts each mechanism's
   accuracy (axis 1) but not the winner (axis 2). This is the keel; it must
   stand alone.
4. Co-signal. Measure RS. Build the two-signal selector. Evaluate against
   ADS-only and RS-only baselines, held-out and cross-dataset. Report the
   recovery number, whatever it is.
5. Synthetic causal probe (demoted). Apply controlled perturbation on real
   records to isolate the direction of the effect.
6. Repo reorganization and release. Only after review: reorganize, deprecate
   stale files, tag a new release, archive a new Zenodo version (additive, never
   a history rewrite).

Review with the human after every gate. Gates 2 and 4 are the make-or-break
checks.

## 7. Evaluation protocol

Thresholds fit on train only. Selector evaluated on held-out items and,
separately, on the second dataset. Always report ADS-only, RS-only, and
two-signal side by side. Complementarity (two-signal beats both) is the claim;
if RS-only dominates, report that honestly. No in-sample selector number is a
result.

## 8. Pre-registration draft

Fix before the frozen run, following Phase 1 discipline.

Hypotheses:
- H1 (accuracy): realized ADS is positively associated with each mechanism's own
  accuracy on real benchmarks.
- H2 (selection blindness): ADS does not predict the winner across its observed
  range.
- H3 (co-signal): a measured RS co-signal predicts the winner where ADS cannot,
  and the two-signal selector beats both single-signal baselines out-of-sample
  by a pre-set margin.

Falsification table with four outcomes per hypothesis (supported, partial, not
supported, inconclusive), fixed in advance. "Co-signal does not help" is an
acceptable, publishable outcome. Freeze the winner definition, splits, cutoff,
thresholds, and margins before the run; do not re-tune after seeing results.

## 9. What success, partial, and failure look like

- Success: boundary finding holds on two datasets, and the two-signal selector
  beats both baselines out-of-sample.
- Partial: boundary holds; co-signal helps but only partially or on one dataset.
  Still a strong, honest paper.
- Co-signal failure: boundary holds, co-signal adds nothing. Still publishable as
  a rigorous boundary result; the title leads with the boundary, not the
  selector.
- Boundary failure: ADS has no range or the decomposition does not appear. Stop
  and rethink the data before writing anything.

## 10. Paper skeleton and budget

Abstract (~220), Introduction (~1200), Related work (~1500), Problem setting
(~900), Experimental design (~1400), Results (~1700), Discussion (~1100),
Limitations (~500), Conclusion (~400). References, tables, and captions sit
outside the body budget. Under 10k total.

Related work streams to add, deliberately and not exhaustively: decision-focused
evaluation (Hand 2009, Hernandez-Orallo et al. 2012, Elmachtoub and Grigas 2022,
Vickers and Elkin 2006, Tan 2026 as sibling); entity resolution and the
exact-versus-fuzzy dichotomy (WDC Products, one entity-matching survey, the
Magellan and DeepMatcher lineage); representation stability and surface-form
robustness. Keep the algorithm-selection spine (Rice, Smith-Miles, Barbudo) and
trim the reject-option and learning-to-defer material to a short scoping
paragraph.

## 11. arXiv posture

Write venue-neutral LaTeX so journal retarget and arXiv upload are both cheap.
The new content is entity resolution, product matching, and record linkage, so
the honest primary category is cs.IR or cs.DB, with cs.LG as a cross-list rather
than the default. Before any submission, run the pre-submission gate: an
arXiv-moderation-risk audit (scope, scholarly framing, references, category fit,
TeX cleanliness, endorsement and eligibility verified at that moment), an
AI-writing-tells pass, and citation verification. Endorsement and eligibility
are checked at submission time, not assumed.
