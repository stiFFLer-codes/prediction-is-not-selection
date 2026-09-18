# Phase 2 plan

The full arc from here to a submission-ready paper. STATE.md says where we are
now; this says where we are going. The charter (CLAUDE.md) sets the boundaries;
the spec (phase2-spec.md) sets the method.

## Paper identity

**Rewritten at Phase 2.5a, 2026-09-18, to the result 2.2e returned.** The
two-signal role-separation identity that stood here is retired. It is not
softened and not carried as a secondary claim; it is gone. What replaces it is
what the frozen rules actually produced.

A venue-neutral research paper reporting a pre-registered negative result:
**design-time mechanism selection for author name disambiguation has no signal a
designer can act on.** The result has two halves, and the structural half is the
sharper contribution.

**The structural half: the comparison most people would run cannot have a
winner.** Exact match is a strict sub-case of single-nearest retrieval, because a
test surface form present in the block's history sits at similarity exactly 1.0,
the maximum of any similarity function. The naive rules-versus-fuzzy comparison
therefore cannot contest a winner at any cutoff, in any metric family, under any
tie-break. This was measured before it was understood: 2.2b found zero `exact
wins` signatures out of 199,713, in both metric arms. 2.2c then generalized it.
For **any** pair of mechanisms that assigns an author from the block's own
history, a precision-first rule can never win a block whose history names one
author, and can never win a block whose history is written one way. Two cells of
the design space are zero by construction, not by measurement.

**The empirical half: where a contest is possible, there is almost nothing to
select.** 2.2c built a genuinely two-sided pair, the exact-evidence rule against a
k-nearest vote at k = 5, and 2.2e ran the frozen analysis on it. The pair is
two-sided on held-out data: 3,025 signatures where the rule is right and the vote
wrong, against 4,012 the other way. But the two mechanisms barely differ, pooled
0.8244 against 0.8294. The gap compresses weakly along both axes and changes sign
marginally, yet no ADS band and no SV band clears the pre-registered margin, so
H2 and H3 are both Inconclusive. Neither consistency nor surface stability
robustly predicts which mechanism to use, and the one pre-registered clause that
tested the role assignment found surface stability, not consistency, the stronger
driver of decidability, under both required measures, at every k and every
margin.

**What this retroactively explains.** The Phase 1 synthetic study reported a
winner that was a constant function of the lexical condition and a consistency
signal blind to it. That is what a nested mechanism pair returns by construction:
the contained mechanism cannot win, so the winner cannot vary, and whatever
tracks the margin then looks like it predicts the choice. The positive-looking
shape of that result was a property of the mechanism pair, not of the data. The
paper says this about its own prior work, as an interpretation of a published
result and not as a new measurement.

What stands on its own, whatever else review decides: the two structural facts
above, H1 (train-only ADS predicts each mechanism's own held-out accuracy across
seven datasets, Supported at both 2.2b and 2.2e), and the pre-registration record
itself.

Sibling in framing to Tan (2026), "Beyond ROC-AUC," which shows a
signal-versus-selection gap for model choice under decision economics, and to Kim
and Kim (2020), the nearest prior work on the surface axis. The distinction
survives the retirement of the old identity and gets sharper. Tan's blind axis is
economic and has no per-block unit. Kim and Kim manipulate a single surface
variable at dataset level, report a gap magnitude, and never claim a winner
change. Our gap-compression shape reproduces theirs at block level with measured
rather than manipulated surface variation, and our null is about selection, which
neither paper attempts.

**What this identity does not include.** No selector, and no claim about one. The
constructive half of the old arc is not part of this paper unless review decides
2.3 runs anyway, and on this result an honestly evaluated selector would have
almost nothing to select over.

## Dataset

S2AND (author name disambiguation). See STATE.md for the one-paragraph rationale
and phase2-spec.md for the construct mapping.

## Phases

Each phase is one fresh Claude Code session, so context never rots. Hard gates
are where we slow down and review most carefully.

- 2.1 Data foundation. Access and license recon, a scoped not-scooped check,
  ingest, and the two-axis sanity check (consistency range, surface-stability
  range, independence). HARD GATE.
- 2.2a Pre-registration. Read the nearest prior work (Kim and Kim 2020) in full,
  position against it, then freeze PREREG.md: hypotheses, falsification table,
  thresholds, split, winner definition, calibration protocol, controls, and
  reporting rules. Committed before any accuracy exists, per invariant 5. No
  measurement.
- 2.2b The boundary finding. Two mechanisms, a paired-bootstrap winner, then the
  dissociation: consistency predicts each mechanism's accuracy but not the
  winner; surface stability does. Executes PREREG.md exactly. This is the keel
  and it must stand alone. **Done. The keel did not come out as drafted:
  consistency predicts accuracy and generalizes, but the two mechanisms turned
  out to be nested, so no winner exists to be predicted or to be blind to. See
  STATE.md and `reports/phase2b_boundary.md`.**
- **2.2c Mechanism redesign, new, inserted by the 2.2b result. HARD GATE.**
  Design-and-propose only: candidate mechanism pairs, a cheap two-sidedness
  check on the calibration split, and a recommendation. No evaluation, no
  amendment to PREREG.md. **Done.** Three two-sided pairs found, P3 (the
  exact-evidence rule against a k-nearest vote, k = 5) recommended, and two
  winner cells found to be zero by construction, which is what forces the change
  to the paper identity above. See `reports/phase2c_pair_design.md`.
- **2.2d Pre-registration revision, the two-signal reframe. HARD GATE. Done.**
  `PREREG.md` Amendment 1, appended and dated 2026-09-18 under the file's own
  amendment rule, superseding sections 2, 4, 7 and 10 and renaming the section 8
  verdicts. H2 becomes consistency gates whether the choice is live; H3 becomes
  surface stability directs it where it is, and consistency does not. Mechanism B
  becomes the k-nearest vote at k = 5, fixed by definition rather than calibrated,
  with a mandatory k curve. Section 7's accuracy-maximizing calibration is void,
  because it pointed straight back at the nesting limit. Nothing measured. Six
  under-determined points in the revision are resolved in the amendment and
  flagged for review.
- **2.2e The mechanism experiment, re-run. HARD GATE. Done.** Executed
  `PREREG.md` Amendment 1 and Addendum 1a exactly, as 2.2b executed 2.2a.
  Mechanism B built with its own self-check and regression-checked against the
  2.2c calibration counts before any evaluation signature was read; nothing new
  frozen. **The pair is two-sided on held-out data, which is what 2.2b lacked,
  but H2 and H3 both come out Inconclusive at the primary margin because every
  marginal pooled gap falls below delta = 0.05.** H1 Supported. H3 is Partial at
  delta = 0.02, so margin-dependent. The one clause that directly tested the
  two-signal role assignment, Addendum 1a's driver comparison, found SV the
  stronger driver of decidability under both required measures. See STATE.md and
  `reports/phase2e_boundary.md`. The 2.2b numbers stay as the frozen record of
  the nested pair and are reported in the paper beside the new ones.
- 2.3 The co-signal. Measure surface stability, build the two-signal selector,
  evaluate it against consistency-only and stability-only baselines, held out and
  across S2AND's sub-datasets. Report the recovery number, whatever it is. HARD
  GATE. **Still blocked, now on review rather than on 2.2e.** The mechanical
  blocker is gone: the pair is two-sided and 500 blocks carry a decided per-block
  verdict at the primary margin, so there is something to select over. What is
  missing is a settled premise. 2.2e supported neither H2 nor H3 and measured the
  role-separation clause pointing the other way, so review has to decide whether
  the two-signal framing stands before a two-signal selector is built. Charter
  invariant 4's ADS-only and SV-only baselines are now the interesting part of
  2.3 rather than the defensive part.
- 2.4 Robustness and causal probe. Controlled perturbation on real records to pin
  the direction of the effect, plus robustness slices.
- 2.5 Writing. Venue-neutral LaTeX, about 8,000 words of body, per the skeleton.
  Likely two or three sessions: draft, tighten, then anti-AI and
  citation-verification passes. **Carries one required deliverable fixed in
  advance: the pre-registration-integrity subsection, drafted blind during 2.2d
  and reproduced verbatim below. It ships whatever 2.2e returns.**
- 2.6 Pre-submission gate and release. arXiv-moderation audit, citation
  verification, repo reorganization, new Zenodo version, category selection.

## Required Phase 2.5 deliverable: pre-registration-integrity subsection

**Status: required. Drafted by the author during Phase 2.2d, blind to the 2.2e
result, and locked here on 2026-09-18 before 2.2e ran.** It is not to be softened
or strengthened by what 2.2e returns. The writing pass reproduces it, works
through its own fill-at-writing checklist, and does not rewrite its argument.

Why it is fixed in advance. The paper's hypotheses were amended after two passes
returned results, which is post hoc, and a reader is entitled to say so. A
defence of that amendment written after seeing the outcome it defends is worth
less than one written before, so this one was written before and pinned here. The
lock is the point: a later pass that finds the defence inconvenient does not get
to soften it, and a later pass that finds the result flattering does not get to
strengthen it.

The text below is verbatim as supplied. Do not reflow, edit, or paraphrase it
here; drafting changes belong in the manuscript pass, against this as the source.

--- BEGIN DELIVERABLE ---

Draft subsection: pre-registration and its amendment

We pre-registered the hypotheses, the winner definition, the analysis bands, and the falsification table before computing any evaluation metric, and we froze the calibration constants in a separate commit before any evaluation number existed. The pre-registration and every subsequent amendment are in the public repository with full history.

We amended the pre-registration once, after two exploratory runs, and we state that plainly rather than presenting the amended version as the original. The amendment was forced by two structural facts about the mechanisms, not by an unwelcome effect size. First, when a test name is present in a block's history it sits at the maximum of any similarity function, so a single-nearest retriever returns whatever exact match returns; exact match is therefore a strict sub-case of single-nearest retrieval, and the two cannot contest a winner. Second, a block whose history names one author returns that author from any non-empty candidate pool, so at maximum consistency the only move a mechanism can make is to abstain. The first fact required replacing the second mechanism with a k-nearest vote that does not reduce to exact match. The second required scoping the consistency hypothesis to whether the choice is decidable at all, rather than which mechanism wins at every consistency level.

Three properties keep the amendment honest. The original hypotheses and the conditions of the runs that motivated the change remain in the pre-registration, unedited and dated. No accuracy figure for the k-nearest mechanism existed at the time the amended hypotheses were written; the amendment predates the run it governs. And the one component of the amended consistency hypothesis that is guaranteed by construction, the decline in decided winners as consistency approaches its maximum, is labeled as structural wherever it appears; the empirical content we test lies below that maximum, in the region where the outcome is not fixed in advance.

Fill-at-writing checklist: confirm every reference and commit id against the committed repo; confirm the amendment-predates-run claim against actual commit timestamps and order; if 2.2e lands H3 as gap-compression-only, this subsection stays essentially unchanged and only the surrounding framing shifts.

--- END DELIVERABLE ---

### Two checks to add to its own checklist, noted at lock time, text unchanged

Both are wording questions against the repository record, not disagreements with
the argument. They are recorded here rather than applied, because the text is
locked and because resolving them is a writing-pass job against the committed
history.

- **"amended once."** The repository shows two dated appends to `PREREG.md`, both
  made during 2.2d and both before any 2.2e number: Amendment 1, the reframe, and
  Addendum 1a, which replaced resolution 5's decidability measure. They are one
  amendment event in two documents, so "once" is defensible, but the writing pass
  should say which it means rather than leave a reader to find a second dated
  append and wonder.
- **"two exploratory runs."** 2.2b was the pre-registered run executing the 2.2a
  freeze, not an exploratory one; 2.2c was the exploratory calibration-split
  probe. The writing pass should check that this phrase says what it intends.

## How each phase runs (the loop)

1. Start a fresh Claude Code session pointed at the repo. It reads the bootstrap
   chain in STATE.md and is caught up.
2. It executes the phase, stopping at the phase's gate. It commits and updates
   STATE.md and PASSLOG.md.
3. The human surfaces the real artifacts, the actual diff and report and key
   scripts, not the PASSLOG narrative, for independent review.
4. Review verifies the work against the claims and the invariants, then plans the
   next phase.
5. Only then does the next fresh session start.

## Title

**Final, set by the author at Phase 2.5d, 2026-09-18.** This is the title, not
a working candidate, and it is the string in `paper/main.tex`:

> Prediction is not selection: a pre-registered study of design-time mechanism
> selection in entity resolution.

It names entity resolution, which is broader than the substrate. The empirical
work is on seven author name disambiguation datasets, and the abstract says so
in its second sentence. The structural result is the part that earns the wider
scope: it holds for any pair of mechanisms assigning from the record's own
history, so it is a statement about entity resolution generally rather than
about author names.

The six candidates carried here from Phase 2.5a are superseded by the line
above and are kept only as the record of what was considered. Rationale and
the discarded directions are in `reports/OUTLINE.md`.

- Nothing to select: a pre-registered null result for design-time mechanism
  choice in author name disambiguation.
- Exact match is a sub-case of nearest-neighbour retrieval, and what that costs a
  mechanism comparison.
- Two design-time signals, no decision: measuring before you build does not tell
  you what to build.
- A comparison that cannot have a winner, and one that barely does: limits on
  design-time mechanism selection.
- When the choice does not matter: rules against retrieval on seven real
  disambiguation datasets.
- Measure your data first, then build what you like: a negative result on
  design-time mechanism selection.

## Output constraints (from the charter)

About 8,000 words of body, under 10,000 total. Venue-neutral LaTeX. Sentence-case
headings, no em dashes, no AI-tell constructions. Every citation verified.
Honest framing: lead with the boundary, present the selector with whatever
recovery number the data yields, never pre-commit to a number.
