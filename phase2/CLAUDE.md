# Phase 2 charter, ADS-Cascade

This file governs all Phase 2 work. Read it at the start of every pass. It sets
hard boundaries and, inside them, gives you real freedom to explore. If any
instruction elsewhere conflicts with this file, this file wins. If something
here blocks a genuinely better path, stop and raise it rather than working
around it.

## Mission

Rebuild the ADS-Cascade paper as a clean, venue-neutral research paper on real
public benchmarks. The scientific core is a two-part finding: a standard
historical-consistency statistic (cluster purity, which we call ADS) predicts
each classification mechanism's own accuracy but is blind to which mechanism
wins, because the winner is governed by surface-form stability, an axis the
consistency signal cannot see. On top of that boundary finding we test one
constructive step: whether a measured surface-stability co-signal carries the
information ADS lacks.

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
6. Two-mechanism core. Exact-match versus fuzzy retrieval is the core
   comparison. A third mechanism (semantic or LLM) may appear only if it is
   actually implemented and evaluated. Otherwise it is named as future scope,
   not shipped inside the selector.
7. Offline and reproducible. The pipeline stays public, offline, no API keys, no
   paid calls, CPU-runnable, and covered by tests. This is load-bearing for
   arXiv and for the paper's identity.
8. Honest framing. Lead with the boundary finding, which stands on its own.
   Present the selector as an honestly evaluated step. Never pre-commit to a
   recovery number.

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

Then stop. Do not start the next pass. Wait for review. Work in gate-sized
passes (see phase2-spec.md). Do not run past a gate without sign-off. Gate 2,
the ADS-range check, is a hard stop.

## Writing invariants (for manuscript prose)

- Target about 8,000 words of body text, under 10,000 total. Leave headroom.
- Venue-neutral LaTeX, generic article class, no journal style file.
- Sentence-case headings. No em dashes.
- Avoid AI-tell vocabulary and constructions. Plain, direct prose.
- Every citation verified and resolvable. No fabricated or placeholder numbers.
