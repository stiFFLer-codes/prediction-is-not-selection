# Phase 2.2b: the boundary experiment

Produced by `phase2/phase2b_run.py`, executing `phase2/PREREG.md` as frozen on 2026-09-18. The fuzzy cutoff and the SV band edges were fixed on the calibration split and committed in `phase2/phase2b_constants.py` before this script was run; see `reports/phase2b_calibration.md`. Nothing below re-tunes, re-bands or redefines anything the pre-registration fixed.

Frozen inputs used here: fuzzy cutoff 0.50 (Levenshtein) and 0.50 (Jaro-Winkler); SV band edges 0.102644 / 0.195066; SV_resid band edges 0.036782 / 0.082418.

## Population accounting (PREREG section 3)

| stratum | blocks | signatures | share of signatures |
| --- | ---: | ---: | ---: |
| all signatures | 26,939 | 766,133 | 100.00% |
| singleton blocks, outside the live set | 7,955 | 7,955 | 1.04% |
| live blocks (2+ signatures) | 18,984 | 758,178 | 98.96% |
| - calibration split (15%) | 2,848 | 116,308 | 15.18% |
| - evaluation split (85%) | 16,136 | 641,870 | 83.78% |
| - - **primary analysis population** (n_train >= 2) | 13,902 | 637,402 | 83.20% |
| - - block-size-2 stratum, named exclusion | 2,234 | 4,468 | 0.58% |

Both exclusions are counted and reported, never silently dropped. Singleton blocks have no second signature, so they have neither a history to match against nor a signal; blocks of exactly 2 give a one-signature history, where ADS is 1.0 by construction and SV is undefined. Their accuracy is reported below as its own stratum but they decide nothing.

Every reported number below comes from the 13,902 blocks and 197,479 test signatures of the primary analysis population.

## What this pass found, in short

**H1 Supported. H2 Inconclusive. H3 Inconclusive.** The rules behind those three words are in the falsification table at the end of this report; nothing was decided by inspection.

Three things a reader should take from the rest of the page.

1. **ADS works as a difficulty signal and generalizes.** Train-only ADS correlates with each mechanism own held-out accuracy, with block-bootstrap intervals well clear of zero for both mechanisms, and it holds in every qualifying non-inspire dataset. That is the construct-validity check H1 was written to be.

2. **The two mechanisms as PREREG section 4 defines them are not independent: exact match is a strict sub-case of fuzzy retrieval.** This is the headline methodological result of the pass and it is a property of the design, not of the data. It is quantified in the next section. Its consequence is that the winner construct is one-sided by construction: exact match cannot win a block, so no ADS-driven or SV-driven winner reversal is reachable, whatever the data say. The risk was anticipated in `reports/kim2020_positioning.md` item 6, but as a low-SV effect; measured, it is total and holds at every SV level.

3. **At the primary margin the gap is small everywhere, so nothing is decided.** The pooled exact-minus-fuzzy gap is -0.0196 overall. At delta = 0.05 the pooled verdict is a demonstrated tie in 5 of 5 ADS bands, 4 of 4 SV bands and 19 of 20 grid cells, with the rest undecided and none decided either way. Under the Order of evaluation rule the power floor is therefore hit first and both H2 and H3 are Inconclusive at delta = 0.05. At the smaller robustness margins some bands do decide, always toward fuzzy, never toward exact.

Nothing here was re-tuned, re-banded or redefined. The degeneracy in point 2 is reported rather than repaired, because repairing it means changing a frozen definition and that is a pre-registration amendment, not an implementation choice.

## The mechanism pair is degenerate: exact match is a sub-case of fuzzy retrieval

This was measured, not deduced. Across all 16,136 evaluation blocks and 199,713 test signatures, the number of signatures on which exact match is right and fuzzy retrieval is wrong is **0** for the Levenshtein arm and **0** for the Jaro-Winkler arm.

The reason is in the frozen definitions themselves. PREREG section 4 has exact match fire only when the test surface form occurs among the train surface forms. When it does, that form sits at similarity exactly 1.0, which is the maximum, so the fuzzy arm selects the same form at any cutoff at or below 1.0 and resolves the author with the same tie-break. Exact match is therefore fuzzy retrieval restricted to similarity 1.0. The relation is independent of the calibrated cutoff: no value on the frozen grid changes it.

Three consequences, all of which shape how the rest of this report should be read.

- **The winner is one-sided by construction.** `exact wins` is unreachable. The four-verdict rule can only return fuzzy wins, tie, or undecided, so a winner reversal, which H3 requires and H2 forbids, cannot occur for either signal at any margin. The H2 and H3 outcomes below are produced by the frozen rules and are reported as such, but the design could not have produced the alternative.
- **The gap is exactly one quantity.** Since every signature exact gets right fuzzy also gets right, the pooled gap equals minus the share of test signatures where exact abstains and fuzzy is correct. Exact coverage is 0.9664, fuzzy coverage 0.9985, and the whole exact-minus-fuzzy story lives in that 3.21 point coverage difference.
- **The agreement rate is an identity, not an observation.** Agreement is 0.9679, which equals exact coverage plus the fuzzy abstention rate, 0.9664 + 0.0015, to every digit. The diagnostic PREREG section 4 asked for to separate genuine equivalence from structural coincidence turns out to measure the structural coincidence exactly.

This is reported, not repaired. Changing the mechanism pair, the cutoff, or the tie-break to make the comparison two-sided would be a change to a frozen definition, which PREREG amendment rule reserves for a dated amendment agreed before the affected numbers exist. The numbers already exist, so the decision belongs to review.

## Held-out accuracy and coverage

| population | blocks | test signatures | exact accuracy | fuzzy accuracy | gap (exact - fuzzy) | exact coverage | fuzzy coverage | agreement | qualifies (>=100 blocks) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 13,902 | 197,479 | 0.8244 | 0.8441 | -0.0196 | 0.9686 | 0.9988 | 0.9698 | yes |
| aminer | 842 | 40,006 | 0.4076 | 0.4106 | -0.0030 | 0.9800 | 0.9992 | 0.9808 | yes |
| arnetminer | 82 | 1,620 | 0.5093 | 0.5142 | -0.0049 | 0.9796 | 1.0000 | 0.9796 |  |
| inspire | 11,110 | 139,369 | 0.9482 | 0.9724 | -0.0241 | 0.9705 | 0.9988 | 0.9716 | yes |
| kisti | 711 | 10,147 | 0.8466 | 0.8528 | -0.0062 | 0.9218 | 0.9970 | 0.9247 | yes |
| pubmed | 34 | 803 | 0.8020 | 0.8182 | -0.0162 | 0.9489 | 1.0000 | 0.9489 |  |
| qian | 276 | 1,696 | 0.6079 | 0.6103 | -0.0024 | 0.9876 | 0.9988 | 0.9888 | yes |
| zbmath | 847 | 3,838 | 0.8494 | 0.9286 | -0.0792 | 0.8953 | 0.9971 | 0.8981 | yes |
| inspire alone | 11,110 | 139,369 | 0.9482 | 0.9724 | -0.0241 | 0.9705 | 0.9988 | 0.9716 | yes |
| pooled non-inspire | 2,792 | 58,110 | 0.5276 | 0.5364 | -0.0088 | 0.9640 | 0.9987 | 0.9653 | yes |

The abstention asymmetry PREREG section 4 asks to keep visible: exact match abstains on 3.1% of test signatures, the fuzzy arm on 0.1%. Abstention is scored as incorrect throughout.

**Block-size-2 stratum, reported not interpreted.** 2,234 blocks, 2,234 test signatures. Exact accuracy 0.6893, fuzzy accuracy 0.8532, exact coverage 0.7739, fuzzy coverage 0.9745. These blocks are excluded from every hypothesis test.

## H1, accuracy: does train-only ADS track each mechanism own accuracy?

PREREG section 2 states H1 as a construct-validity check, not a contribution. Spearman correlation between train-only ADS and the block held-out accuracy, with a 95% block-bootstrap interval.

| population | blocks | qualifies | rho exact | lo exact | hi exact | rho fuzzy | lo fuzzy | hi fuzzy | both positive, interval excludes 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 13,902 | yes | 0.5069 | 0.4916 | 0.5224 | 0.7436 | 0.7305 | 0.7568 | yes |
| aminer | 842 | yes | 0.6275 | 0.5745 | 0.6789 | 0.6497 | 0.5971 | 0.6957 | yes |
| arnetminer | 82 |  | 0.8464 | 0.7594 | 0.8977 | 0.8545 | 0.7701 | 0.9054 | yes |
| inspire | 11,110 | yes | 0.3361 | 0.3148 | 0.3552 | 0.6183 | 0.5951 | 0.6399 | yes |
| kisti | 711 | yes | 0.4352 | 0.3737 | 0.4950 | 0.4446 | 0.3809 | 0.5062 | yes |
| pubmed | 34 |  | 0.5382 | 0.1640 | 0.7823 | 0.5185 | 0.1887 | 0.7480 | yes |
| qian | 276 | yes | 0.6595 | 0.5681 | 0.7408 | 0.6782 | 0.5955 | 0.7589 | yes |
| zbmath | 847 | yes | 0.2269 | 0.1595 | 0.2966 | 0.4673 | 0.3931 | 0.5355 | yes |
| inspire alone | 11,110 | yes | 0.3361 | 0.3164 | 0.3559 | 0.6183 | 0.5958 | 0.6405 | yes |
| pooled non-inspire | 2,792 | yes | 0.5632 | 0.5337 | 0.5916 | 0.6971 | 0.6735 | 0.7206 | yes |

Table: reports/tables/phase2b_h1_spearman.csv

Mean per-block accuracy by ADS band:

| ads_band | blocks | exact | fuzzy | exact_cov | fuzzy_cov |
| --- | --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 0.4991 | 0.5093 | 0.9218 | 0.9945 |
| [0.5,0.7) | 1,101 | 0.6758 | 0.7127 | 0.8931 | 0.9855 |
| [0.7,0.9) | 743 | 0.8389 | 0.8757 | 0.9325 | 0.9964 |
| [0.9,1.0) | 450 | 0.9418 | 0.9627 | 0.9703 | 0.9984 |
| 1.0 | 10,537 | 0.9234 | 0.9866 | 0.9291 | 0.9966 |

Figure: `reports/figs/phase2b_h1_ads_accuracy.png`

Qualifying non-inspire datasets (4): aminer, kisti, qian, zbmath. H1 holds in 4 of them: aminer, kisti, qian, zbmath.

## The winner (PREREG section 8)

Per block: paired bootstrap on the accuracy difference, B = 2000, seed 20260918 + block index, 95% percentile interval, four mutually exclusive verdicts. Per band and per cell: the pooled gap with an interval obtained by resampling **blocks** with replacement, because the block is the independent unit. delta = 0.05 is primary; 0.02 and 0.03 are the pre-registered robustness curve.

Overall per-block verdict distribution, delta = 0.05:

| verdict | blocks | share |
| --- | --- | --- |
| exact wins | 0 | 0.0000 |
| fuzzy wins | 298 | 0.0214 |
| tie | 11,117 | 0.7997 |
| undecided | 2,487 | 0.1789 |

### Pooled verdict by ADS band (marginal)

| ads_band | n_blocks | n_test | exact_acc | fuzzy_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 47,167 | 0.4490 | 0.4537 | -0.0047 | -0.0055 | -0.0039 | tie | tie | tie |  |
| [0.5,0.7) | 1,101 | 16,079 | 0.7981 | 0.8152 | -0.0171 | -0.0199 | -0.0147 | tie | tie | tie |  |
| [0.7,0.9) | 743 | 12,660 | 0.8777 | 0.8988 | -0.0211 | -0.0243 | -0.0182 | tie | tie | undecided |  |
| [0.9,1.0) | 450 | 12,683 | 0.9563 | 0.9698 | -0.0135 | -0.0161 | -0.0112 | tie | tie | tie |  |
| 1.0 | 10,537 | 108,890 | 0.9694 | 0.9964 | -0.0270 | -0.0283 | -0.0257 | tie | tie | fuzzy wins |  |

### Pooled verdict by SV band (marginal)

| sv_band | n_blocks | n_test | exact_acc | fuzzy_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.8102 | 0.8468 | -0.0366 | -0.0402 | -0.0332 | tie | fuzzy wins | fuzzy wins |  |
| SV low | 3,032 | 56,408 | 0.7864 | 0.8036 | -0.0172 | -0.0188 | -0.0158 | tie | tie | tie |  |
| SV mid | 3,218 | 59,433 | 0.9041 | 0.9217 | -0.0177 | -0.0191 | -0.0163 | tie | tie | tie |  |
| SV high | 3,135 | 63,678 | 0.7878 | 0.8066 | -0.0188 | -0.0204 | -0.0172 | tie | tie | undecided |  |

### Pooled verdict by SV_resid band (marginal)

| svr_band | n_blocks | n_test | exact_acc | fuzzy_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 9,636 | 94,171 | 0.8350 | 0.8543 | -0.0194 | -0.0206 | -0.0182 | tie | tie | undecided |  |
| SV low | 1,383 | 45,378 | 0.7835 | 0.7973 | -0.0138 | -0.0154 | -0.0123 | tie | tie | tie |  |
| SV mid | 1,375 | 29,732 | 0.8380 | 0.8599 | -0.0219 | -0.0246 | -0.0194 | tie | tie | undecided |  |
| SV high | 1,508 | 28,198 | 0.8409 | 0.8684 | -0.0275 | -0.0304 | -0.0248 | tie | undecided | fuzzy wins |  |

### The 5 x 4 ADS-by-SV grid (PREREG section 9)

SV effect is only ever shown at fixed ADS and ADS effect only at fixed SV, because the two axes correlate (Phase 2.1: Pearson -0.2988). Cells under 30 blocks are marked under-powered and decide nothing.

| ads_band | sv_band | n_blocks | n_test | exact_acc | fuzzy_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | agreement | exact_cov | fuzzy_cov |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | SV=0 | 155 | 2,383 | 0.2509 | 0.2522 | -0.0013 | -0.0028 | 0.0000 | tie | tie | tie |  | 0.9878 | 0.9874 | 0.9996 |
| [0,0.5) | SV low | 272 | 13,131 | 0.2579 | 0.2598 | -0.0019 | -0.0027 | -0.0012 | tie | tie | tie |  | 0.9899 | 0.9889 | 0.9989 |
| [0,0.5) | SV mid | 91 | 5,652 | 0.3850 | 0.3877 | -0.0027 | -0.0048 | -0.0012 | tie | tie | tie |  | 0.9871 | 0.9867 | 0.9996 |
| [0,0.5) | SV high | 553 | 26,001 | 0.5776 | 0.5844 | -0.0069 | -0.0083 | -0.0056 | tie | tie | tie |  | 0.9484 | 0.9469 | 0.9985 |
| [0.5,0.7) | SV=0 | 278 | 1,167 | 0.4996 | 0.5099 | -0.0103 | -0.0177 | -0.0044 | tie | tie | tie |  | 0.9657 | 0.9597 | 0.9940 |
| [0.5,0.7) | SV low | 98 | 1,876 | 0.6210 | 0.6279 | -0.0069 | -0.0125 | -0.0029 | tie | tie | tie |  | 0.9781 | 0.9771 | 0.9989 |
| [0.5,0.7) | SV mid | 157 | 3,527 | 0.7939 | 0.8049 | -0.0111 | -0.0160 | -0.0072 | tie | tie | tie |  | 0.9748 | 0.9742 | 0.9994 |
| [0.5,0.7) | SV high | 568 | 9,509 | 0.8713 | 0.8935 | -0.0222 | -0.0259 | -0.0188 | tie | tie | undecided |  | 0.9504 | 0.9468 | 0.9964 |
| [0.7,0.9) | SV=0 | 119 | 756 | 0.7884 | 0.7963 | -0.0079 | -0.0155 | -0.0023 | tie | tie | tie |  | 0.9868 | 0.9828 | 0.9960 |
| [0.7,0.9) | SV low | 109 | 2,410 | 0.8120 | 0.8282 | -0.0162 | -0.0234 | -0.0105 | tie | tie | undecided |  | 0.9697 | 0.9689 | 0.9992 |
| [0.7,0.9) | SV mid | 264 | 4,420 | 0.9045 | 0.9251 | -0.0206 | -0.0261 | -0.0157 | tie | tie | undecided |  | 0.9606 | 0.9604 | 0.9998 |
| [0.7,0.9) | SV high | 251 | 5,074 | 0.8989 | 0.9247 | -0.0258 | -0.0313 | -0.0210 | tie | undecided | fuzzy wins |  | 0.9602 | 0.9586 | 0.9984 |
| [0.9,1.0) | SV=0 | 43 | 882 | 0.9467 | 0.9512 | -0.0045 | -0.0116 | 0.0000 | tie | tie | tie |  | 0.9932 | 0.9921 | 0.9989 |
| [0.9,1.0) | SV low | 174 | 5,013 | 0.9523 | 0.9637 | -0.0114 | -0.0151 | -0.0081 | tie | tie | tie |  | 0.9848 | 0.9840 | 0.9992 |
| [0.9,1.0) | SV mid | 132 | 3,797 | 0.9602 | 0.9737 | -0.0134 | -0.0178 | -0.0096 | tie | tie | tie |  | 0.9808 | 0.9800 | 0.9992 |
| [0.9,1.0) | SV high | 101 | 2,991 | 0.9609 | 0.9806 | -0.0197 | -0.0264 | -0.0142 | tie | tie | undecided |  | 0.9756 | 0.9749 | 0.9993 |
| 1.0 | SV=0 | 3,922 | 12,772 | 0.9349 | 0.9843 | -0.0495 | -0.0538 | -0.0451 | undecided | fuzzy wins | fuzzy wins |  | 0.9458 | 0.9422 | 0.9964 |
| 1.0 | SV low | 2,379 | 33,978 | 0.9735 | 0.9981 | -0.0246 | -0.0268 | -0.0226 | tie | tie | fuzzy wins |  | 0.9747 | 0.9740 | 0.9992 |
| 1.0 | SV mid | 2,574 | 42,037 | 0.9780 | 0.9983 | -0.0203 | -0.0220 | -0.0186 | tie | tie | undecided |  | 0.9792 | 0.9785 | 0.9993 |
| 1.0 | SV high | 1,662 | 20,103 | 0.9665 | 0.9972 | -0.0307 | -0.0339 | -0.0277 | tie | undecided | fuzzy wins |  | 0.9682 | 0.9676 | 0.9994 |

Table: reports/tables/phase2b_pooled_cells_sv.csv

Figures: `reports/figs/phase2b_grid_gap_sv.png`, `reports/figs/phase2b_grid_gap_svresid.png`

Figures: `reports/figs/phase2b_verdicts_by_sv.png`, `reports/figs/phase2b_verdicts_by_ads.png`

### Compact regression summary

Per-block gap (exact - fuzzy) on ADS and SV together, with test-set size as a covariate. PREREG section 9 asks for block-clustered standard errors on a regression whose unit of observation is the block; each cluster then holds one observation, so the cluster-robust estimator reduces algebraically to the heteroskedasticity-robust one, and that is what is reported. It is a summary of the grid, not a substitute for it, and no hypothesis is decided from it.

| term | coef | se | t |
| --- | --- | --- | --- |
| intercept | -0.0519 | 0.0056 | -9.3362 |
| ADS | -0.0495 | 0.0043 | -11.3884 |
| SV | -0.1443 | 0.0172 | -8.3902 |
| log(test-set size) | 0.0308 | 0.0015 | 21.2261 |

## Power report (PREREG section 8, mandatory)

Verdict share as a function of test-set size, so that a reader can see how much of any no-winner region is demonstrated equivalence and how much is a small test set. Tie means equivalence was shown; undecided means there was not enough evidence to decide. They are never merged.

| test-set size | blocks | exact wins | fuzzy wins | tie | undecided |
| --- | --- | --- | --- | --- | --- |
| 1 | 1,309 | 0.0000 | 0.1215 | 0.8785 | 0.0000 |
| 2 | 2,159 | 0.0000 | 0.0394 | 0.8319 | 0.1288 |
| 3-4 | 2,466 | 0.0000 | 0.0073 | 0.8183 | 0.1744 |
| 5-8 | 2,316 | 0.0000 | 0.0104 | 0.8009 | 0.1887 |
| 9-16 | 2,214 | 0.0000 | 0.0041 | 0.7602 | 0.2358 |
| 17-32 | 1,903 | 0.0000 | 0.0016 | 0.7362 | 0.2622 |
| 33-64 | 1,113 | 0.0000 | 0.0000 | 0.7358 | 0.2642 |
| 65-+ | 422 | 0.0000 | 0.0000 | 0.9360 | 0.0640 |

Full curve across all three margins: reports/tables/phase2b_power_by_size.csv

Figure: `reports/figs/phase2b_power_by_size.png`

## Winner structure: reversal, tie-crossing, or compression only (PREREG section 9)

Three outcomes defined in advance. A **winner reversal** is two bands with decided pooled verdicts of opposite identity. A **tie-crossing** is one band decided and another a demonstrated tie, with no band decided the opposite way. **Gap compression only** is a change of magnitude with neither of those.

Reading note. Section 9 gates the classification at two bands of 30 or more blocks; section 10 separately sets the Inconclusive power floor at two bands with 30 or more blocks **and** a decided pooled verdict, and the Order of evaluation rule makes that floor a hypothesis-level test evaluated first. The two are reported separately below (`eligible_bands` and `decided_bands`) so either reading can be checked against the same numbers.

### H2: across ADS bands at fixed SV

**signal/metric: sv**

delta = 0.05

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=undecided | gap compression only |
| SV low | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV high | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |

delta = 0.03

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=fuzzy wins | tie-crossing |
| SV low | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV high | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=undecided / [0.9,1.0)=tie / 1.0=undecided | gap compression only |

delta = 0.02

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=fuzzy wins | tie-crossing |
| SV low | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=undecided / [0.9,1.0)=tie / 1.0=fuzzy wins | tie-crossing |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=undecided / [0.9,1.0)=tie / 1.0=undecided | gap compression only |
| SV high | 5 | 2 | [0,0.5)=tie / [0.5,0.7)=undecided / [0.7,0.9)=fuzzy wins / [0.9,1.0)=undecided / 1.0=fuzzy wins | tie-crossing |

### H3: across SV bands at fixed ADS

**signal/metric: sv**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=tie / SV high=tie | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 1 | SV=0=fuzzy wins / SV low=tie / SV mid=tie / SV high=undecided | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 1 | SV=0=tie / SV low=undecided / SV mid=undecided / SV high=fuzzy wins | tie-crossing |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| 1.0 | 4 | 3 | SV=0=fuzzy wins / SV low=fuzzy wins / SV mid=undecided / SV high=fuzzy wins | gap compression only |

**signal/metric: svr**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| 1.0 | 4 | 1 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=fuzzy wins | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 1 | SV=0=undecided / SV low=undecided / SV mid=undecided / SV high=fuzzy wins | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| 1.0 | 4 | 3 | SV=0=fuzzy wins / SV low=undecided / SV mid=fuzzy wins / SV high=fuzzy wins | gap compression only |

**signal/metric: sv_jw**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=tie / SV high=tie | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 1 | SV=0=fuzzy wins / SV low=tie / SV mid=tie / SV high=undecided | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 1 | SV=0=tie / SV low=undecided / SV mid=undecided / SV high=fuzzy wins | tie-crossing |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| 1.0 | 4 | 3 | SV=0=fuzzy wins / SV low=fuzzy wins / SV mid=undecided / SV high=fuzzy wins | gap compression only |

### Per-dataset generalization of the H3 structure (PREREG section 11)

inspire is the great majority of live blocks, so a pooled number is mostly an inspire number. A finding generalizes only if it holds pooled non-inspire **and** in a majority of qualifying non-inspire datasets (100 or more blocks in the primary analysis population).

| population | blocks | qualifies (>=100 blocks) | ADS bands with 2+ eligible SV bands | ADS bands with 2+ decided SV bands | winner reversal | tie-crossing | outcomes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| aminer | 842 | yes | 2 | 0 |  |  | gap compression only / not eligible |
| arnetminer | 82 |  | 0 | 0 |  |  | not eligible |
| inspire | 11,110 | yes | 4 | 0 |  |  | gap compression only / not eligible |
| kisti | 711 | yes | 0 | 0 |  |  | not eligible |
| pubmed | 34 |  | 0 | 0 |  |  | not eligible |
| qian | 276 | yes | 0 | 0 |  |  | not eligible |
| zbmath | 847 | yes | 1 | 1 |  |  | gap compression only / not eligible |
| inspire alone | 11,110 | yes | 4 | 0 |  |  | gap compression only / not eligible |
| pooled non-inspire | 2,792 | yes | 5 | 0 |  | yes | gap compression only / tie-crossing |

Table: reports/tables/phase2b_generalization.csv

## Diagnostics required by the pre-registration

### Mechanism agreement rate per SV band (PREREG section 4)

The share of test signatures on which the two mechanisms return the identical prediction, counting identical abstentions as agreement. This separates demonstrated practical equivalence from the structural case where a single-surface-form history makes the two mechanisms the same procedure.

| sv_band | n_blocks | n_test | agreement | exact_cov | fuzzy_cov | exact_acc | fuzzy_acc | median_n_test | mean_n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.9567 | 0.9535 | 0.9968 | 0.8102 | 0.8468 | 2.0000 | 3.9761 |
| SV low | 3,032 | 56,408 | 0.9791 | 0.9782 | 0.9991 | 0.7864 | 0.8036 | 11.0000 | 18.6042 |
| SV mid | 3,218 | 59,433 | 0.9784 | 0.9778 | 0.9994 | 0.9041 | 0.9217 | 11.0000 | 18.4689 |
| SV high | 3,135 | 63,678 | 0.9571 | 0.9557 | 0.9985 | 0.7878 | 0.8066 | 9.0000 | 20.3120 |

Test-set size is printed beside it because the SV bands are not comparable in size: an SV = 0 block has a single-surface-form history, which on this data is mostly a small block. The marginal SV ordering and the SV coefficient in the regression above therefore say different things, and the regression, which holds ADS and log test-set size fixed, is the one that isolates SV. Neither is used to decide a hypothesis; the decisions come from the grid, where ADS is held fixed by construction.

### Jaro-Winkler robustness arm (PREREG section 9)

SV and the fuzzy mechanism are both built on normalized edit distance. The winner is defined by labelled accuracy, so this is not the tautology charter invariant 2 forbids, but the shared metric is a fair objection. The fuzzy arm is rerun with Jaro-Winkler, its own cutoff calibrated on the calibration split by the same protocol.

| sv_band | n_blocks | n_test | exact_acc | fuzzy_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.8102 | 0.8481 | -0.0379 | -0.0417 | -0.0343 | tie |  |
| SV low | 3,032 | 56,408 | 0.7864 | 0.8041 | -0.0177 | -0.0192 | -0.0163 | tie |  |
| SV mid | 3,218 | 59,433 | 0.9041 | 0.9221 | -0.0181 | -0.0197 | -0.0167 | tie |  |
| SV high | 3,135 | 63,678 | 0.7878 | 0.8070 | -0.0192 | -0.0209 | -0.0176 | tie |  |

### INIT stratification (PREREG section 9, secondary control)

INIT is the train-only share of signatures whose given-name field is an initial only. The SV-to-winner relationship is shown inside each INIT band, which asks whether the effect exists among blocks that are homogeneous in initialization style.

| init_band | sv_band | n_blocks | n_test | pooled_gap | ci_lo | ci_hi | verdict_0.05 | agreement | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INIT=0 | SV=0 | 3,743 | 15,253 | -0.0252 | -0.0284 | -0.0221 | tie | 0.9681 |  |
| INIT=0 | SV low | 684 | 9,373 | -0.0192 | -0.0229 | -0.0157 | tie | 0.9694 |  |
| INIT=0 | SV mid | 277 | 2,385 | -0.0222 | -0.0309 | -0.0152 | tie | 0.9543 |  |
| INIT=0 | SV high | 508 | 4,746 | -0.0164 | -0.0210 | -0.0126 | tie | 0.8978 |  |
| 0<INIT<0.5 | SV low | 1,047 | 26,947 | -0.0101 | -0.0116 | -0.0086 | tie | 0.9870 |  |
| 0<INIT<0.5 | SV mid | 1,325 | 27,865 | -0.0138 | -0.0157 | -0.0119 | tie | 0.9823 |  |
| 0<INIT<0.5 | SV high | 1,249 | 36,481 | -0.0158 | -0.0180 | -0.0139 | tie | 0.9622 |  |
| INIT>=0.5 | SV=0 | 774 | 2,707 | -0.1008 | -0.1173 | -0.0857 | fuzzy wins | 0.8925 |  |
| INIT>=0.5 | SV low | 1,301 | 20,088 | -0.0259 | -0.0289 | -0.0230 | tie | 0.9729 |  |
| INIT>=0.5 | SV mid | 1,616 | 29,183 | -0.0210 | -0.0231 | -0.0190 | tie | 0.9766 |  |
| INIT>=0.5 | SV high | 1,378 | 22,451 | -0.0242 | -0.0270 | -0.0216 | tie | 0.9615 |  |

Structure across SV within each INIT band, delta = 0.05:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| INIT>=0.5 | 4 | 1 | SV=0=fuzzy wins / SV low=tie / SV mid=tie / SV high=tie | tie-crossing |

Structure across SV within each INIT band, delta = 0.03:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=tie | gap compression only |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| INIT>=0.5 | 4 | 1 | SV=0=fuzzy wins / SV low=tie / SV mid=tie / SV high=tie | tie-crossing |

Structure across SV within each INIT band, delta = 0.02:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 1 | SV=0=fuzzy wins / SV low=undecided / SV mid=undecided / SV high=undecided | gap compression only |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| INIT>=0.5 | 4 | 3 | SV=0=fuzzy wins / SV low=fuzzy wins / SV mid=undecided / SV high=fuzzy wins | gap compression only |

### How much of SV is forename initialization?

Spearman correlations among the design-time signals on the primary analysis population. If SV were essentially INIT, the SV_resid control would be the whole answer to the Kim and Kim overlap.

|  | ads | sv | sv_resid | init |
| --- | --- | --- | --- | --- |
| ads | 1.0000 | -0.2704 | -0.2744 | 0.1794 |
| sv | -0.2704 | 1.0000 | 0.5125 | 0.3627 |
| sv_resid | -0.2744 | 0.5125 | 1.0000 | 0.2025 |
| init | 0.1794 | 0.3627 | 0.2025 | 1.0000 |

## The falsification table, evaluated (PREREG section 10)

Outcomes are read off the rules frozen on 2026-09-18, in the order the pre-registration fixes: **Inconclusive is evaluated first** and takes precedence over every other row. An outcome that holds at one margin and flips at another is margin-dependent and is treated as Partial, not Supported.

### H1, accuracy (validity check, not a contribution)

**Outcome: Supported**

- primary analysis population blocks: 13,902
- qualifying non-inspire datasets: 4 (aminer, kisti, qian, zbmath)
- Spearman rho, exact: 0.5069, 95% CI [0.4916, 0.5224]
- Spearman rho, fuzzy: 0.7436, 95% CI [0.7305, 0.7568]
- generalizes: True

### H2, selection blindness

**Outcome: Inconclusive**

- decided ADS bands (30+ blocks): []
- decided SV bands (30+ blocks): []

### H3, co-signal

**Outcome: Inconclusive**

- ADS bands with 2+ eligible SV bands: 5
- ADS bands with 2+ decided SV bands: 0
- winner reversal with SV: False
- tie-crossing with SV: False
- winner reversal with SV_resid: False
- winner reversal with Jaro-Winkler: False
- generalizes (non-inspire pooled + majority of qualifying datasets): None

### Margin sensitivity (PREREG section 8)

delta = 0.05 is the primary margin; 0.02 and 0.03 are the pre-registered robustness curve.

| delta | H2 | H3 |
| --- | --- | --- |
| 0.0500 | Inconclusive | Inconclusive |
| 0.0300 | Inconclusive | Inconclusive |
| 0.0200 | Inconclusive | Partial |

H2 outcome constant across margins: yes. H3 outcome constant across margins: **no, margin-dependent**.

Figure: `reports/figs/phase2b_margin_sensitivity.png`

### What these outcomes do and do not say

H2 and H3 are Inconclusive because the pre-registered power floor is evaluated first and is not met: at delta = 0.05 no ADS band and no SV band has a decided pooled verdict, so there is nothing for the constancy test in H2 or the reversal test in H3 to operate on. PREREG section 10 lists exactly this situation, the primary analysis population being too thin to decide, as a permitted verdict to be used rather than worked around, and the reviewer rule added at the 2.2a freeze exists to stop an all-tie band set reading as support for H2. It is doing its job here.

Two things should not be read into it.

- **Inconclusive is not evidence for selection blindness.** H2 says ADS does not predict the winner. On this run ADS does not predict the winner, but neither does anything else, because there is no winner to predict: the mechanism pair cannot produce one. That is a weaker statement than H2 and the falsification table correctly declines to call it support.

- **Inconclusive is not the same as the pre-registered gap-compression outcome.** Substantively the pattern is compression: the pooled gap varies with SV at fixed ADS, monotonically in four of the five ADS bands, and never changes sign. Under the frozen rules that reading is available only once the power floor is cleared, which it is not at the primary margin. The substance and the pre-registered verdict are reported separately here rather than the more favourable one being chosen.

The single blocking issue for Phase 2.3 is the degeneracy reported at the top of this page. A selector that chooses between a mechanism and a strict superset of it has nothing to choose, so the 2.3 selector question cannot be asked of this mechanism pair as PREREG section 4 defines it. That is a pre-registration matter and is left for review.
