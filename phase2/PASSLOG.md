# Phase 2 pass log

## Pass 0 — archive Phase 1 root context (pre-gate, admin)

**What and why:** Root `CLAUDE.md` and `STATE.md` were auto-loading into every
session as Phase 1 framing/status, competing with `phase2/CLAUDE.md` as the
authoritative charter. User granted a one-time authorized exception to the
charter's off-limits rule (root files are normally read-only until the final
cleanup pass) to move them out of the auto-load path. `git mv`'d both into
`phase1-archive/` as `CLAUDE.phase1.md` and `STATE.phase1.md` (no
hard-delete). Root `CLAUDE.md` contained no repo-wide operational content
(no build/test commands, no latexmk/pdflatex invocations, no git/LF
conventions, no main.tex sync steps — pure Phase 1 framing and doc pointers),
so no replacement root `CLAUDE.md` was created.

**Key numbers / plots:** None — administrative file move, no code or data
touched.

**Invariant checks run:** None applicable — no code, data, or selector
changes in this pass. Confirmed off-limits paths otherwise untouched
(`exp1/`, `manuscript/`, `arxiv_build/`, `arxiv_submission/`, main branch,
v1.0.0 tag all unaffected).

**Side effect noted:** `.claude/hooks/check-state-modified.ps1` hardcodes a
check against root `STATE.md`; with that file archived, the hook now exits
silently (file not found) instead of reminding about state updates. Not
fixed in this pass — out of scope (hooks weren't part of the authorized
exception) — flagging for the eventual final cleanup pass.

**Recommendation for next pass:** None — this was an administrative
exception pass, not part of the gated sequence. Gate 1 has not been started
per instruction; awaiting review/sign-off before any gate work begins.
