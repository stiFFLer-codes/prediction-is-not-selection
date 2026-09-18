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

**Status of that identity after 2.2b and 2.2c.** The first half survived and
generalizes: train-only ADS predicts each mechanism's own held-out accuracy
across seven datasets. The second half does not survive as written. 2.2b showed
the frozen mechanism pair is nested, so no winner exists to be blind to. 2.2c
found two-sided replacement pairs, which repairs that, but also showed that a
precision-first rule cannot win a block whose train history names one author, so
**ADS necessarily carries some winner information for any pair of this shape**.
The blindness claim is therefore not recoverable by changing mechanisms.

The identity the evidence supports is two-signal rather than blind: consistency
predicts each mechanism's accuracy and says whether the choice between them
matters at all, and surface stability says which way to go where it does.
Neither signal alone determines the winner. The identity above is kept as
written, marked, until review adopts it or something else, rather than quietly
rewritten to match the result.

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
- **2.2d New pre-registration, new. HARD GATE.** Only after review adopts a
  pair. A dated amendment section appended to PREREG.md per its own amendment
  rule, committed before any new accuracy exists. It has to settle three things
  the old one did not face: the replacement for H2, the analysis population
  (probably the contested region, ADS < 1 and SV > 0), and the margin inside it.
  It must also replace PREREG section 7's accuracy-maximizing calibration for
  the retriever's parameter, which points straight back at the nesting limit.
- **2.2e The boundary experiment, re-run. HARD GATE.** Executes 2.2d exactly, as
  2.2b executed 2.2a. The 2.2b numbers stay as the frozen record of the nested
  pair and are reported in the paper beside the new ones.
- 2.3 The co-signal. Measure surface stability, build the two-signal selector,
  evaluate it against consistency-only and stability-only baselines, held out and
  across S2AND's sub-datasets. Report the recovery number, whatever it is. HARD
  GATE. **Blocked on 2.2d and 2.2e.** A selector cannot choose between a
  mechanism and a strict superset of it, so this phase is not runnable until a
  two-sided pair is adopted and pre-registered. Charter invariant 4's ADS-only
  and SV-only baselines become load-bearing rather than defensive, since 2.2c
  indicates both signals carry part of the winner.
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

To merge with CC's suggestions at the writing phase, once results are in. All
three below presume both that a winner exists and that consistency is blind to
it. 2.2b removed the first for the current pair and 2.2c removed the second for
any pair of this shape, so **all three need replacing**. What the evidence points
at instead is a two-signal title: consistency says whether the choice matters,
surface stability says which way to go.

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
