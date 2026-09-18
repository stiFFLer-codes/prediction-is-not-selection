# Phase 2 plan

The full arc from here to a submission-ready paper. STATE.md says where we are
now; this says where we are going. The charter (CLAUDE.md) sets the boundaries;
the spec (phase2-spec.md) sets the method.

## Paper identity

A venue-neutral research paper showing that two design-time, label-free signals
play separable roles in mechanism choice. A consistency signal sets **whether**
the choice of classification mechanism matters at all, and a surface-stability
signal sets **which way** to choose where it does. Neither signal alone predicts
the winner, and that conjunction is the contribution. On top of it, an honestly
evaluated selector that uses both, reported beside a consistency-only and a
stability-only baseline.

Sibling in framing to Tan (2026), "Beyond ROC-AUC," which shows a
signal-versus-selection gap for model choice under decision economics, and to Kim
and Kim (2020), the nearest prior work on the surface axis. Distinct from both:
Tan's blind axis is economic and has no per-block unit; Kim and Kim manipulate a
single surface variable at dataset level and report a gap magnitude, with no
decidability axis and no design-time signal.

**How this identity was arrived at, and what is still untested.** It replaces an
earlier one-signal claim that consistency is blind to the winner. 2.2b showed the
frozen mechanism pair was nested, so no winner existed to be blind to, and 2.2c
showed that a precision-first rule cannot win a block whose train history names
one author, so consistency necessarily carries some winner information for any
pair in this family. The blindness claim was not recoverable by changing
mechanisms, so the claim was rebuilt rather than repaired, at Phase 2.2d.
`PREREG.md` Amendment 1 is the binding version.

What is established: train-only ADS predicts each mechanism's own held-out
accuracy across seven datasets (H1, 2.2b), and the two structural gates above.
**What is not yet measured: everything else.** The gating gradient, the SV
reversal, and the role separation between them are hypotheses with a frozen
falsification table, not results. 2.2e is the pass that tests them, and every
outcome in that table, including the ones that retire this identity, is
acceptable.

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
- **2.2e The mechanism experiment, re-run. HARD GATE.** Executes `PREREG.md`
  Amendment 1 exactly, as 2.2b executed 2.2a. Build mechanism B with its own
  self-check, freeze nothing new (the split, the band edges and the margins all
  carry over), then run calibration-free and report. The 2.2b numbers stay as the
  frozen record of the nested pair and are reported in the paper beside the new
  ones.
- 2.3 The co-signal. Measure surface stability, build the two-signal selector,
  evaluate it against consistency-only and stability-only baselines, held out and
  across S2AND's sub-datasets. Report the recovery number, whatever it is. HARD
  GATE. **Blocked on 2.2e.** The pair is now two-sided and pre-registered, but
  no evaluation-split number exists for it yet, so there is nothing to select
  over. Charter invariant 4's ADS-only and SV-only baselines are load-bearing
  rather than defensive here, since the amended hypotheses expect each signal to
  carry a different part of the winner.
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

## Working titles

To merge with CC's suggestions at the writing phase, once results are in.
Replaced at Phase 2.2d: the three earlier candidates all presumed consistency was
blind to the winner, which 2.2c ruled out.

- Consistency decides whether the matcher matters, surface stability decides
  which one: a two-signal design-time account.
- When does the matcher matter, and which one: a per-block, design-time selector
  for author name disambiguation.
- Two design-time signals, two roles: gating and directing mechanism choice in
  entity resolution.

## Output constraints (from the charter)

About 8,000 words of body, under 10,000 total. Venue-neutral LaTeX. Sentence-case
headings, no em dashes, no AI-tell constructions. Every citation verified.
Honest framing: lead with the boundary, present the selector with whatever
recovery number the data yields, never pre-commit to a number.
