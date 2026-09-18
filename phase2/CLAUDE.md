# Phase 2 charter, ADS-Cascade

This file governs all Phase 2 work. Read it at the start of every pass. It sets
hard boundaries and, inside them, gives you real freedom to explore. If any
instruction elsewhere conflicts with this file, this file wins. If something
here blocks a genuinely better path, stop and raise it rather than working
around it.

## Mission

Rebuild the ADS-Cascade paper as a clean, venue-neutral research paper on real
public benchmarks. The scientific core is a pre-registered negative result:
**design-time mechanism selection for author name disambiguation has no signal a
designer can act on.** It has a structural half and an empirical half, and the
two are separate contributions.

**Structural.** Exact match is a strict sub-case of single-nearest retrieval. A
test surface form that occurs in the block's history sits at similarity exactly
1.0, the maximum of any similarity function, so any retriever that takes the
single nearest form takes that form and resolves the same author. The naive
rules-versus-fuzzy comparison therefore cannot contest a winner, at any cutoff
and in any metric family. Measured at 2.2b: zero `exact wins` signatures out of
199,713, in both metric arms. Generalized at 2.2c: for any pair of mechanisms
that assigns an author from the block's own history, a precision-first rule can
never win a block whose history names one author, and can never win a block whose
history is written one way.

**Empirical.** With a genuinely two-sided pair, designed at 2.2c and run at 2.2e,
the two mechanisms barely differ: pooled held-out accuracy 0.8244 for the rule
against 0.8294 for the k-nearest vote. The gap compresses weakly with surface
stability and never reverses below ADS = 1.0 at the primary margin. Neither
consistency nor surface stability robustly predicts which mechanism to use. H2
and H3 both came out Inconclusive because the pre-registered margin is wider than
every effect on both axes.

Together these retroactively explain the Phase 1 synthetic result, where the
winner looked like a clean constant function of the surface condition. That is
what a nested pair returns by construction, on any data.

**Retired at Phase 2.5a, 2026-09-18.** The two-signal role separation is dead,
not weakened, and is not to be restated anywhere. The one pre-registered clause
that tested it, Addendum 1a's driver comparison, found SV the stronger driver of
decidability under both required measures, at every k and every margin. `PREREG.md`,
including Amendment 1 and Addendum 1a, stays frozen and untouched as the record
of what was fixed in advance and what was tested.

## Non-goals

- Do not overclaim a selector that "recovers 100%". Report whatever the data yields.
- Do not reintroduce the Romanian case study, confidential figures, or any
  non-reproducible motivation.
- Do not make the synthetic generator the primary evidence. It is a controlled
  probe only.

## Off-limits paths (read-only)

Do not modify, delete, move, or clean up any of these during Phase 2 passes:

- exp1 and the Phase 1 synthetic experiment code
- manuscript/, arxiv_build/, arxiv_submission/, and every main.tex copy
- anything outside phase2/
- the main branch and the v1.0.0 tag

All Phase 2 work happens on the phase-2 branch, inside phase2/. Reorganizing or
deprecating stale repo files happens only in the final dedicated cleanup pass,
and only after review.

## Hard invariants (non-negotiable)

1. Verify before you build. Measure the ADS distribution on the chosen data
   before building any mechanism or selector. If ADS does not span a usable
   range, stop and report the histogram. Do not proceed on a dead axis.
2. No tautology. The winner label and the representation-stability signal must
   never be the same variable measured twice. On real data, surface noise is
   measured per item, never set by us. Never define the winner using the
   stability signal.
3. Held-out only. Any selector is evaluated on held-out items or a different
   dataset than the one its thresholds were fit on. In-sample selector accuracy
   is never reported as a result.
4. Baselines always. Report an ADS-only selector and an RS-only selector beside
   any two-signal selector. The dual-signal claim survives only if the
   two-signal version beats both. If RS-only suffices, say so plainly.
5. No result before measurement. Never write a number, claim, or conclusion that
   was not produced by committed, re-runnable code. Verified numbers are a
   frozen evidence base; prose passes must not alter them.
6. Two-mechanism core. A precision-first exact-evidence rule versus a
   coverage-first k-nearest-vote retriever is the core comparison, as fixed by
   `PREREG.md` Amendment 1 (Phase 2.2d). It was exact match versus thresholded
   fuzzy retrieval until 2.2b measured that pair to be nested. Both mechanisms
   are untrained lookups over the block's own history. A third mechanism
   (semantic or LLM) may appear only if it is actually implemented and
   evaluated. Otherwise it is named as future scope, not shipped inside the
   selector.
7. Offline and reproducible. The pipeline stays public, offline, no API keys, no
   paid calls, CPU-runnable, and covered by tests. This is load-bearing for
   arXiv and for the paper's identity.
8. Honest framing. Lead with whatever the frozen falsification table returns,
   not with the framing that motivated the run. Present the selector as an
   honestly evaluated step. Never pre-commit to a recovery number. Two structural
   results already stand on their own whatever 2.2e finds: single-nearest
   retrieval subsumes exact match, and a precision-first rule cannot win where
   the history names one author.

## Freedom zone

Inside those boundaries you have real latitude. You choose implementation and
code structure within phase2/, which representation-stability signals to
prototype, which data subset to start with, the order of exploratory analyses,
and how to visualize results. Explore. Propose alternatives. Bring findings we
did not anticipate. The invariants above are the only hard limits; everything
else is yours to design.

## Pass protocol

Each pass ends with:

1. A commit on phase-2 with a clear message.
2. An entry appended to phase2/PASSLOG.md stating: what you did and why, the key
   numbers or plots produced with their file paths, which invariant checks you
   ran and their results, and your recommendation for the next pass.
3. STATE.md updated to reflect the new current status and the next step, and
   PLAN.md updated if the phase arc changed. STATE.md is the file a fresh session
   reads to orient, so after every pass it must describe reality as it now is,
   not as it was before the pass.

Then stop. Do not start the next pass. Wait for review. Work in gate-sized
passes (see phase2-spec.md). Do not run past a gate without sign-off. Gate 2,
the ADS-range check, is a hard stop.

## Writing invariants (for manuscript prose)

- Target about 8,000 words of body text, under 10,000 total. Leave headroom.
- Venue-neutral LaTeX, generic article class, no journal style file.
- Sentence-case headings. No em dashes.
- Avoid AI-tell vocabulary and constructions. Plain, direct prose.
- Every citation verified and resolvable. No fabricated or placeholder numbers.
