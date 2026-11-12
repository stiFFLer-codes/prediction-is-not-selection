# Errata

The governance files (`CLAUDE.md`, `PLAN.md`, `STATE.md`, `PASSLOG.md`) and the reports under `reports/` are working records. They were written pass by pass and are kept as written, so a reader can see what was believed when. Several of them state things that the later record contradicts. This file lists each one: where it is, what it says, what the record shows, and which file shows it. The paper (`paper/main.tex`) has been corrected for all of these, and nothing here changes a reported number or a hypothesis outcome. Line numbers are at commit `306557a`, before the dated notes that point here were added to `CLAUDE.md`, `PLAN.md` and `STATE.md`. Entries added 2026-11-12.

## 1. "At every k" for the driver comparison

- **Where.** `CLAUDE.md:43`; `PLAN.md:41-42`; `STATE.md:228-229`; `reports/phase2e_boundary.md:638`; `PASSLOG.md:1394` and `:1503`.
- **What it says.** Addendum 1a's driver clause, which required ADS to be the stronger driver of decidability, failed "at every k" on the mandatory k curve.
- **What the record shows.** The clause failed at k = 3, 5 and 10. At k = 2 it was `split`, which the report defines as the two required measures disagreeing (`reports/phase2e_boundary.md:267`). On the primary measure at k = 2, eta2_ADS was 0.3277 against eta2_SV 0.3751. ADS wins both measures at no k, so the retirement of the role separation stands.
- **Shown by.** `reports/phase2e_boundary.md:296`, the k sensitivity table, and `:612`. Section 7.6 of the paper says "splits at $k = 2$" (`paper/main.tex:1214-1217`).

## 2. "Can never win a block whose history is written one way," for any pair

- **Where.** `CLAUDE.md:23-26`; `PLAN.md:26-29`.
- **What it says.** For any pair of mechanisms that assigns an author from the block's own history, a precision-first rule can never win a block whose history names one author, and can never win a block whose history is written one way.
- **What the record shows.** The first half holds for any such pair. The second half holds only for mechanisms that read surface forms alone and share a tie-break. A mechanism that also reads co-authors, venues or other context can tell apart mentions that share one form. On the data, in the SV = 0 band the rule is right where the vote is wrong on 0 signatures. The vote is right where the rule is wrong on 696, and every one of those is a rule abstention on a test form the training half never shows. The rule cannot win there and the vote can, which is the source of the `k-NN wins` verdicts in that band at delta = 0.03 and 0.02.
- **Shown by.** `reports/phase2_9a_report.md`, finding 4 (`:32-37`) and section A3 (`:426` onward); `reports/tables/phase2_9a_region_counts.csv`. Section 4.3 of the paper now states the narrower form.

## 3. "Nothing is redistributed"

- **Where.** `reports/phase2_6_moderation_audit.md:284-296`.
- **What it says.** The availability statement says none of the data is redistributed, the repository holds only the download code and the manifest, and "nothing is redistributed".
- **What the record shows.** The repository carries derived S2AND tables: the signature table `data/s2and_signatures.parquet`, which holds names and affiliation strings, and five per-block tables keyed by a normalized name. It also carries one derived WDC extract. The signature table has been tracked since commit `4399fe1`. The audit checked only the gitignored `data/raw_s2and/`.
- **Shown by.** `DATA_LICENSES.md`, which lists every derived file with its columns and row count; `git log --diff-filter=A` on those paths. The paper's availability statement now says what is carried and under which licence.

## 4. The calibration split "reserved for choices of exactly this kind"

- **Where.** `reports/phase2c_pair_design.md:4-5`. The same words are in the docstring of `phase2c_probe.py:4`, which is left unchanged like every analysis script.
- **What it says.** The 2.2c probe ran on "the 15% of live blocks PREREG section 3 reserves for choices of exactly this kind".
- **What the record shows.** The frozen section 3 says the calibration split is "Used exactly once, for the fuzzy cutoff (section 7) and for the SV and SV_resid band edges (section 6)" (`PREREG.md:135-138`). It reserves the split for nothing else. The split was used a second time at 2.2c, to choose the replacement pair and k, and a third time for the 2.2e regression check. Amendment 1 discloses the k choice (`PREREG.md:700-703`), and it also calls it a choice "of exactly the kind the calibration split exists for", which the frozen section 3 does not say. No reported hypothesis number comes from the calibration split.
- **Shown by.** `PREREG.md:135-138`; section 6.4 of the paper, fourth correction (`paper/main.tex:869-876`).

## 5. Section 11's per-dataset form is missing from the 2.2e report

- **Where.** `reports/phase2e_boundary.md`.
- **What it says.** The report gives the per-dataset, inspire-alone and pooled non-inspire forms for accuracy, for H1 and as a summary table (`:459-471`).
- **What the record shows.** `PREREG.md` section 11 (`:523-529`) requires "Every headline table and every hypothesis decision" in all three forms. The report does not give them for the pooled-verdict-by-band tables or the ADS-by-SV grid, which are the headline tables behind H2 and H3. Once produced, those tables show kisti `rule wins` and zbmath `k-NN wins` as whole datasets at delta = 0.05. They do not move a hypothesis outcome.
- **Shown by.** `reports/phase2_9b_report.md`; `reports/tables/phase2_9b_population_verdicts.csv`, `phase2_9b_bands_by_population.csv` and `phase2_9b_cells_by_population.csv`. Section 7.8 of the paper reports them.

## 6. Who drafted the locked section 6.4 text

- **Where.** `PLAN.md:164`.
- **What it says.** "**Status: required. Drafted by the author during Phase 2.2d, blind to the 2.2e result, and locked here on 2026-09-18 before 2.2e ran.**"
- **What the record shows.** The author does not recall who drafted it. The project's AI assistant drafted most of the project's text, as the paper's generative-AI disclosure now states (`paper/main.tex:1845-1851`). "Drafted by the author" is therefore not supported by the record. The timing in the same line, written during 2.2d and locked before 2.2e ran, is a separate matter, and section 6.4 of the paper sets out its evidence.
- **The paper.** The paper's own sentence about the text is passive: "The text of this subsection was written during the amendment pass, before the run it defends was executed, and locked in the project plan at that point" (`paper/main.tex:738-740`). It names no drafter, and it stands.
