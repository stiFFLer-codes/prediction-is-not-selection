# Repository conventions

Working rules for anyone (human or AI assistant) changing code in this repository.
The guiding principle: **the best code is the code never written.** Prefer deletion
over addition, boring over clever, the fewest files that solve the problem.

## Before writing code

Understand the problem first — read the task and the code it touches, trace the real
flow end to end. Then stop at the first option that holds:

1. Does this need to be built at all? (YAGNI — skip speculative work.)
2. Does it already exist in this codebase? Reuse the helper, util, or pattern that
   is already here; don't re-implement it.
3. Does the standard library do it? Use it.
4. Does a native platform feature cover it? Use it.
5. Does an already-installed dependency solve it? Use it.
6. Can it be one line? Make it one line.
7. Only then: write the minimum code that works.

## Bug fixes

Fix the root cause, not the symptom. A report names one symptom; grep every caller of
the function you are about to touch. One guard in the shared function is a smaller diff
than one guard per caller — and patching only the path the report names leaves every
sibling caller still broken.

## Rules

- No abstractions that weren't asked for — no interface with one implementation, no
  config for a value that never changes.
- No new dependency for what a few lines can do.
- No boilerplate or scaffolding "for later."
- Shortest working diff wins — but only once you understand the problem. The smallest
  change in the wrong place is a second bug, not a fix.
- Given two standard-library approaches of the same size, take the one that is correct
  on edge cases.
- Mark a deliberate shortcut with a `# ponytail:` comment. If it has a known ceiling
  (global lock, O(n^2) scan, naive heuristic), the comment names the ceiling and the
  upgrade path.

## Never cut corners on

Understanding the problem, input validation at trust boundaries, error handling that
prevents data loss, security, accessibility, the calibration real-world inputs need
(a clock drifts, a sensor reads off, OCR is noisy), and anything explicitly requested.

## Tests

Non-trivial logic (a branch, a loop, a parser, a money or security path) leaves one
runnable check behind — the smallest thing that fails if the logic breaks: an
`assert`-based self-check under `if __name__ == "__main__"`, or one small `test_*.py`.
No frameworks, no fixtures unless asked. Trivial one-liners need no test.

## Repository-specific ground rules

Documented in `architecture/00_SCOPE.md` and `architecture/DECISIONS.md` (16 ADRs).
The locked calls — RULES_FIRST, hybrid retrieval, VAT as a secondary feature, no mass
reprocessing, OCR confidence is not classification confidence — are settled; revisit
them only with new evidence, not in passing.
