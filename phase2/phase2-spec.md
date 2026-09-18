# Phase 2 spec, S2AND substrate

Method reference. The charter (CLAUDE.md) sets the boundaries; this fills them
with constructs, questions, and protocol. STATE.md says where we are; PLAN.md is
the arc. This revision replaces the earlier WDC-based spec.

## 1. Paper identity

A venue-neutral research paper reporting a pre-registered negative result:
**design-time mechanism selection for author name disambiguation has no signal a
designer can act on.** The question the paper asks is whether a designer can
measure a property of their own data before building anything and learn which
classification mechanism to build. On this substrate the answer is no, for two
separable reasons.

**Structural.** Exact match is a strict sub-case of single-nearest retrieval. A
test surface form present in the block's history sits at similarity exactly 1.0,
the maximum of any similarity function, so any single-nearest retriever takes the
same form and resolves the same author. The naive rules-versus-fuzzy comparison
cannot contest a winner, at any cutoff and in any metric family. Measured at 2.2b
as zero `exact wins` signatures out of 199,713 in both metric arms, then
generalized at 2.2c: for any pair of mechanisms that assigns an author from the
block's own history, a precision-first rule can never win where the history names
one author, and can never win where the history is written one way.

**Empirical.** With a genuinely two-sided pair, the exact-evidence rule against a
k-nearest vote at k = 5, the two mechanisms barely differ on real data: pooled
held-out accuracy 0.8244 against 0.8294 over 197,479 test signatures. The gap
compresses weakly with surface stability and changes sign marginally on both
axes, but no band clears the pre-registered margin, so H2 and H3 are both
Inconclusive. Neither consistency nor surface stability robustly predicts which
mechanism to use, and the one pre-registered clause that compared them found
surface stability the stronger driver of decidability under both required
measures.

Together these retroactively explain the Phase 1 synthetic result, whose winner
was a constant function of the lexical condition. A nested pair produces exactly
that shape by construction.

Sibling in framing to Tan (2026), "Beyond ROC-AUC," which shows a
signal-versus-selection gap for model choice under decision economics, and to Kim
and Kim (2020) on the surface axis. Distinct from both: Tan's blind axis is
economic and has no per-block unit; Kim and Kim manipulate one surface variable
at dataset level, report a gap magnitude, and never claim a winner change.

**Rewritten at Phase 2.5a, 2026-09-18.** The text here previously claimed a
two-signal role separation, consistency gating and surface stability directing.
2.2e tested it and returned Inconclusive on both hypotheses, with the one clause
that measured the role assignment failing under both required measures. That
identity is retired, not softened. `PREREG.md`, with Amendment 1 and Addendum 1a,
stays frozen and unedited as the record of what was fixed in advance.

## 2. Data: S2AND

S2AND (Semantic Scholar Author Name Disambiguation, Allen Institute for AI)
unifies eight prior author-disambiguation datasets into one format. Public,
offline, with a reference implementation. Its records are signatures: an author
mention on a paper, carrying the name string and context such as co-authors,
venue, title, affiliation, and year (exact fields to be confirmed at ingest).
Signatures are grouped into blocks by a normalized name string, and ground truth
assigns each signature to a real author (a cluster). S2AND explicitly
characterizes two block-level properties we use directly: homonymity (how many
distinct authors share a name, our inverse-consistency axis) and synonymity (how
many surface variants one author appears under, our inverse-surface-stability
axis).

The eight constituent datasets give cross-dataset generalization for free, which
is exactly the breadth Tan (2026) lacked. Access, license, and a scoped
not-scooped check are verified in Phase 2.1 before any building.

## 3. Construct mapping (the faithful port)

- key = name block, the normalized name string. The recurring key, like a product
  in the original invoice work.
- label = author identity. Like the account in the original.
- ADS(block) = purity of author assignments among the block's training
  signatures, that is the share belonging to the block's single most frequent
  author. High ADS means the name refers to essentially one person (low
  homonymity); low ADS means the name is shared (high homonymity). Computed
  train-only (design-time, history-only). This consistency signal is observed,
  not a coarsening knob, which is precisely what makes it legitimate here where
  the WDC blocking key was not.
- surface stability = the inverse of within-author or within-block surface-form
  variability, our synonymity-based axis. Low variability means the name is
  written consistently, so the exact-evidence rule survives; high variability
  means many variants, so the retriever's coverage is expected to pay. Measured,
  never set, and never defined using the winner (invariant 2). Which way it
  points was H3. Measured at 2.2e: the pooled gap does rise with SV and change
  sign marginally, -0.0388 / -0.0144 / -0.0115 / +0.0189 across the four bands,
  but no SV band pair is decided in opposite directions below ADS = 1.0 at any
  margin, so the shape is gap compression and not direction.
- unit of analysis = the block. Each block is a small classification problem with
  its own ADS and its own surface stability, so blocks are the natural analog of
  the synthetic experiment's conditions, and there are many of them.
- **winner = structurally unreachable in two regions, and empirically almost
  absent everywhere else** (rewritten at Phase 2.5a, after 2.2e). Two cells are
  zero by construction for any pair of mechanisms that assigns an author from the
  block's own history. A block whose train history names one author returns that
  author from any non-empty pool, so a precision-first rule can differ there only
  by abstaining, which scores as wrong. A block whose history carries one surface
  form gives every mechanism the same evidence. Where a contest is structurally
  possible, it is empirically small: at delta = 0.05 no ADS band and no SV band
  has a decided pooled verdict, and 500 of 13,902 blocks carry a decided
  per-block verdict. The winner is not a function of both axes in any actionable
  sense. Most of the time it is not there.

## 4. Mechanisms and winner

**Superseded by `PREREG.md` Amendment 1 (Phase 2.2d) for mechanism B and the
verdict names.** Mechanism B is now a k-nearest vote with k = 5 and no cutoff.
The text below is the draft this grew from and is kept for the record; where the
two differ, PREREG.md wins.

Two mechanisms assign a held-out signature to an author, using a historical
(train) knowledge base built per block:

- exact-match: assign the author of a training signature whose name string, and
  optionally a fixed exact context key, matches exactly; abstain on no match. No
  threshold to tune.
- fuzzy retrieval: retrieve the most similar training signature by a lexical
  similarity over the name, and optionally context, and assign its author; a
  similarity cutoff calibrated once, before the frozen run, on a disjoint split.

Primary metric: whole-set accuracy, abstention counts as incorrect, coverage
reported. The exact-abstains and fuzzy-does-not asymmetry is a first-class
result, not normalized away. Winner per block, or per ADS band, by paired
bootstrap on the accuracy difference with a fixed practical-equivalence margin;
ties are a distinct category. This is the Phase 1 rigor, carried over.

## 5. The two axes and independence

Phase 2.1 confirms, before anything is built: that ADS spans a real range across
blocks (expected, since homonymity varies widely in this data), that surface
stability spans a real range, and that the two are separable rather than the same
quantity measured twice. The separability check (a correlation and scatter of
block ADS against block surface variability) is what protects invariant 2. Where
S2AND ships its own homonymity and synonymity measures, cross-check our measures
against them.

## 6. Phases and gates

See PLAN.md for the full arc, which gained 2.2c, 2.2d and 2.2e after the 2.2b
result. The make-or-break gates are 2.1 (the two-axis sanity check), 2.2e (the
re-run against the amended pre-registration) and 2.3 (the co-signal). Nothing
runs past a gate without review.

## 7. Evaluation protocol

Thresholds and any selector are fit train-only. The selector is evaluated held
out and across the eight sub-datasets. Always report consistency-only,
stability-only, and two-signal baselines side by side; the dual-signal claim
survives only if the two-signal version beats both. If stability-only dominates,
say so plainly. No in-sample selector number is ever reported as a result.

## 8. Pre-registration draft

**Superseded by `phase2/PREREG.md`, frozen 2026-09-18 in Phase 2.2a.** That file
is the binding pre-registration; this section is kept as the draft it grew from.
Where the two differ, PREREG.md wins.

Fixed before the frozen run, following Phase 1 discipline.

- H1 (accuracy): block consistency (ADS) is positively associated with each
  mechanism's own accuracy.
- H2 (selection blindness): ADS does not predict which mechanism wins across its
  observed range.
- H3 (co-signal): a measured surface-stability co-signal predicts the winner where
  ADS cannot, and the two-signal selector beats both single-signal baselines
  out-of-sample by a pre-set margin.

Falsification table with four outcomes per hypothesis (supported, partial, not
supported, inconclusive), fixed in advance. "Co-signal does not help" is an
acceptable, publishable outcome. Freeze the blocking normalization, the
surface-stability measure, the fuzzy cutoff, the winner definition, the splits,
and the margins before measuring any accuracy.

## 9. Success, partial, failure

- Success: boundary finding holds across sub-datasets, and the two-signal selector
  beats both baselines out-of-sample.
- Partial: boundary holds; co-signal helps but only partially or on some
  sub-datasets. Still a strong, honest paper.
- Co-signal failure: boundary holds, co-signal adds nothing. Still publishable as
  a rigorous boundary result; the title leads with the boundary.
- Boundary failure: ADS has no range or the decomposition does not appear. Stop
  and reconsider before writing anything.

## 10. Paper skeleton and budget

> **Superseded by `reports/OUTLINE.md`, built at Phase 2.5a, 2026-09-18.** That
> file carries the section list, the spines and the budget for the paper as it
> now stands, adapted to a methodological-and-null result. The skeleton below is
> the draft it grew from. Where the two differ, OUTLINE.md wins. The
> related-work streams below are unchanged and still correct.

Abstract (~220), Introduction (~1200), Related work (~1500), Problem setting
(~900), Experimental design (~1400), Results (~1700), Discussion (~1100),
Limitations (~500), Conclusion (~400). References, tables, and captions sit
outside the body budget. Under 10k total.

Related-work streams, deliberately and not exhaustively: decision-focused
evaluation (Hand 2009, Hernandez-Orallo et al. 2012, Elmachtoub and Grigas 2022,
Vickers and Elkin 2006, Tan 2026 as sibling); author name disambiguation and
entity linking as the home domain (S2AND, WhoIsWho, an AND survey); the
algorithm-selection spine (Rice, Smith-Miles, Barbudo); representation and
surface-form robustness. Trim reject-option and learning-to-defer to a short
scoping paragraph.

## 11. arXiv posture

Venue-neutral LaTeX so journal retarget and arXiv upload are both cheap. The
content is author name disambiguation and entity resolution, so the honest
primary category is cs.DL (Digital Libraries) or cs.IR, cross-listing the other
and cs.LG rather than defaulting to cs.LG. Before any submission, run the
pre-submission gate: a moderation-risk audit (scope, scholarly framing,
references, category fit, TeX cleanliness, endorsement and eligibility verified at
that moment), an anti-AI-writing pass, and citation verification.
