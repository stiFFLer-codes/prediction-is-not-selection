# Project status — ADS-Cascade

Living status for the project. Pointer-based on purpose: it links the canonical
docs, it does not copy them.

`Last updated: 2026-09-02`

**Current phase:** Phase 1 (data engineering) and Phase 2 (receipt cascade demo) are
complete. The repository is published and archived on Zenodo (v1.0.0, DOI
[10.5281/zenodo.21644208](https://doi.org/10.5281/zenodo.21644208)). The Experiment 1
manuscript (`manuscript/main.tex`) is finalized as a release candidate. The arXiv
submission has not yet happened.

---

## Where we are

Phase 1 (data engineering), Phase 2 (receipt-classification demo), and the Experiment 1
manuscript are all complete and committed. The interactive stakeholder demo is built
(`docs/demo/index.html`). No open implementation work remains for any of the three
tracks; what is left is publication logistics (arXiv submission) and optional
repository-hygiene polish.

## Done

- **Phase 1 — data-engineering pipeline.** 6 scripts (`scripts/`), standard-library only.
  296,648 invoice lines · 169 companies · weighted ADS 0.847 · 91.2% products
  deterministic · 76,843 product→account mappings.
  → `reports/phase1_final_report.md`
- **Phase 2 — solution architecture + cascade demo.** 17 docs (`architecture/`): scope,
  requirements, NFRs, domain model, services, event workflow, data schema, confidence
  cascade, AI orchestration, API contracts, sequences, security, observability, cost,
  plus 16 ADRs and 20 open questions. Cascade validated end to end: Tier-1 held-out
  accuracy 98.4% @ 42% coverage; full-cascade auto-apply 42.8% coverage @ 98.1% accuracy.
  → `architecture/00_SCOPE.md`, `docs/demo/index.html`
- **Public research export + synthetic reproduction.**
  `scripts/00_generate_synthetic.py` generates synthetic companies/products/invoice
  lines from documented target distributions (no real data read); the full pipeline
  reproduces the same qualitative structure on synthetic data, including one documented
  architecture-decision flip (R3) at smaller scale. Real data, real-derived intermediate
  files, and real-named worked examples were stripped or anonymized. → `METHODOLOGY.md`
- **GitHub + Zenodo publication.** Repo `stiFFLer-codes/ADS-Cascade`;
  `TECHNICAL_REPORT.md` written; `LICENSE` (MIT) and `CITATION.cff` (ORCID-linked) added;
  GitHub–Zenodo integration connected; `v1.0.0` release published; DOI
  `10.5281/zenodo.21644208` minted.
- **Experiment 1 — controlled mechanism-selection study, through manuscript
  finalization.** Research audit → literature verification → contribution lock
  (Formulation #2 adopted) → 240-condition frozen experiment
  (`data/outputs/experiments/exp1/final/`) → post-hoc analysis → first complete
  manuscript draft → independent adversarial audit → readability pass → citation/claim
  audit → public reproducibility audit → figure generation → final prose polish → final
  adversarial review → release-candidate hardening (author metadata, AI-assistance
  disclosure, bibliography corrections, release-boundary fixes, editorial refinement).
  The full phase-by-phase audit trail is retained in the project's development history.

## Next

**arXiv submission of `manuscript/main.tex`** — not yet started. Remaining items: pick an
arXiv category, assemble the source package, rebuild the compiled PDF from the current
`manuscript/` sources, confirm Google Scholar indexing once live, and cross-link the
Zenodo record / GitHub README / ORCID profile to the arXiv identifier. No further
scientific or drafting work is planned — the manuscript is content-frozen at the release
candidate.

## How to run

All offline except two cached API layers. Reproducible without keys (caches committed).

```
python scripts/phase2/p2_01_build_kb.py        # KB from Phase 1 mappings
python scripts/phase2/p2_02_classify_eval.py   # held-out cascade eval (Tier-1 98.4%)
python scripts/phase2/p2_03_extract.py         # Textract OCR (idempotent; 0 new calls if cached)
python scripts/phase2/p2_05_end_to_end.py      # 10 receipts -> per-line tier + candidates
python scripts/phase2/p2_06_llm_tail.py        # LLM re-rank on review tail (needs GROQ_API_KEY)
python scripts/phase2/test_cascade.py          # fast self-checks
python scripts/experiments/exp1/run_final.py   # Experiment 1 (single command, no keys)
python scripts/experiments/exp1/analyze_posthoc.py --demo   # fast self-check of Exp. 1 stats
```

- **Groq key:** put `GROQ_API_KEY=gsk_...` in `.env` at the repo root (gitignored). No
  key → `p2_06` skips cleanly.
- **Groq free-tier limits (llama-3.3-70b-versatile): 30 RPM / 12K TPM.** The adapter
  throttles to ~27 RPM with 429 backoff; cached calls don't count. To swap to Claude
  Haiku, edit `p2lib/ai/adapter.py` and set `ANTHROPIC_API_KEY`.
- **AWS:** IAM user `contai-textract`, region ap-south-1; Textract cached → $0 going
  forward.

## Open decisions / blockers

Headline items (full list → `architecture/OPEN_QUESTIONS.md`):

- **Production stack unconfirmed** — language, DB, hosting, how the live D406 pipeline is
  deployed. Design stays tech-agnostic until answered.
- **WhatsApp Business route** — direct Meta vs. BSP partner.
- **ERP export format** — the target accounting system's import XML schema.
- **Receipt volumes** — per company/month; drives the cost model and batching.
- Confidence thresholds (0.95 / 0.85) are Phase 1-derived starting points — a pilot must
  calibrate them.
- **arXiv category and submission logistics** — not yet decided (see "Next" above).

## Where things live

| What | Path |
|---|---|
| Pipeline scripts | `scripts/` |
| Pipeline outputs (ground truth) | `data/outputs/` |
| Phase 2 design (source of truth) | `architecture/` |
| Phase 1 reports + data-verification audit | `reports/` |
| Entry / navigation docs | `docs/` (start at `docs/INDEX.md`) |
| Repo map | `README.md` |
| Repository conventions | `AGENTS.md` |
| Experiment 1 manuscript | `manuscript/main.tex`, `manuscript/references.bib` |

## Keeping this file current

At the end of a work session, update only *Where we are*, *Next*, *Done*, and the
`Last updated` date. Keep it pointer-based — link the canonical docs, never copy their
prose here.
