# Phase 2 plan

The full arc from here to a submission-ready paper. STATE.md says where we are
now; this says where we are going. The charter (CLAUDE.md) sets the boundaries;
the spec (phase2-spec.md) sets the method.

## Paper identity

A venue-neutral research paper showing that a design-time consistency signal
predicts each classification mechanism's accuracy but not which mechanism to
select, because the winner is governed by surface-form stability, an axis the
consistency signal cannot see. On top of that boundary finding, an honestly
evaluated co-signal that recovers the selection. Sibling in framing to Tan
(2026), "Beyond ROC-AUC," which shows the same signal-versus-selection gap for
model choice under decision economics; our blind axis is representational.

## Dataset

S2AND (author name disambiguation). See STATE.md for the one-paragraph rationale
and phase2-spec.md for the construct mapping.

## Phases

Each phase is one fresh Claude Code session, so context never rots. Hard gates
are where we slow down and review most carefully.

- 2.1 Data foundation. Access and license recon, a scoped not-scooped check,
  ingest, and the two-axis sanity check (consistency range, surface-stability
  range, independence). HARD GATE.
- 2.2 The boundary finding. Two mechanisms, a paired-bootstrap winner, then the
  dissociation: consistency predicts each mechanism's accuracy but not the
  winner; surface stability does. This is the keel and it must stand alone.
- 2.3 The co-signal. Measure surface stability, build the two-signal selector,
  evaluate it against consistency-only and stability-only baselines, held out and
  across S2AND's sub-datasets. Report the recovery number, whatever it is. HARD
  GATE.
- 2.4 Robustness and causal probe. Controlled perturbation on real records to pin
  the direction of the effect, plus robustness slices.
- 2.5 Writing. Venue-neutral LaTeX, about 8,000 words of body, per the skeleton.
  Likely two or three sessions: draft, tighten, then anti-AI and
  citation-verification passes.
- 2.6 Pre-submission gate and release. arXiv-moderation audit, citation
  verification, repo reorganization, new Zenodo version, category selection.

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

To merge with CC's suggestions at the writing phase, once results are in:

- Historical consistency predicts accuracy, not method choice: a design-time
  blind spot in entity resolution.
- The selection signal that is most confident where it is most wrong:
  consistency, surface stability, and mechanism choice.
- Two axes, one signal: consistency predicts difficulty, surface stability
  decides the winner.

## Output constraints (from the charter)

About 8,000 words of body, under 10,000 total. Venue-neutral LaTeX. Sentence-case
headings, no em dashes, no AI-tell constructions. Every citation verified.
Honest framing: lead with the boundary, present the selector with whatever
recovery number the data yields, never pre-commit to a number.
