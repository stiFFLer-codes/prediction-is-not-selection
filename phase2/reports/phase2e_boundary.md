# Phase 2.2e: the amended boundary experiment

Produced by `phase2/phase2e_run.py`, executing `phase2/PREREG.md` as amended by **Amendment 1** and **Addendum 1a**, both frozen on 2026-09-18 at Phase 2.2d before any number on this page existed. Mechanism B is the k-nearest vote of `phase2/phase2e_mech.py`, whose regression check reproduces the 2.2c calibration-split two-sidedness counts exactly (see the next section). Nothing below re-tunes, re-bands or redefines anything the pre-registration fixed: section 7 is void, k is fixed by definition at 5, and the split, the ADS bands, the SV and SV_resid band edges, the margins and the seeds all carry over from the 2.2a freeze and `phase2b_constants.py`.

Frozen inputs used here: SV band edges 0.102644 / 0.195066; SV_resid band edges 0.036782 / 0.082418; seed 20260918; B = 2000; delta = 0.05 primary with 0.02 and 0.03 as the robustness curve.

The 2.2b numbers are not recomputed, not overwritten and not withdrawn. They stay in `reports/phase2b_boundary.md` as the record of the nested pair.

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

Both exclusions are counted and reported, never silently dropped. ADS = 1.0 blocks are **not** excluded: Amendment 1 keeps them because the decline of decidability into that band is what H2 is about.

Every reported number below comes from the 13,902 blocks and 197,479 test signatures of the primary analysis population.

## What this pass found, in short

**H1 Supported. H2 Inconclusive. H3 Inconclusive.** The rules behind those three words are in the amended falsification table at the end of this report; nothing was decided by inspection.

1. **The mechanism pair is two-sided on the evaluation split.** `rule wins` was structurally unreachable in 2.2b and measured zero on 199,713 signatures. Here the rule is right and the k-nearest vote wrong on **3,025** test signatures, against **4,012** the other way, at k = 5. A winner exists to be predicted.

2. **Pooled, the two mechanisms are close.** Rule accuracy 0.8244 against k-NN 0.8294, a pooled gap of -0.0050, with the rule abstaining on 3.14% of test signatures and the vote never abstaining.

3. **Decidability and its drivers.** The decided-winner rate over the primary population is 0.0360 at delta = 0.05. Over the eligible cells of the frozen grid, eta2_ADS = 0.1749 against eta2_SV = 0.3837, and the averaged ranges are 0.0707 against 0.0755. Addendum 1a requires ADS to win under both; the clause comes out **failed**.

Nothing here was re-tuned, re-banded or redefined. Section 7 is void, k is fixed by definition, and the band edges and margins are the ones committed before 2.2b ran.

## Regression check: mechanism B reproduces the 2.2c design diagnostics

Mandatory first step, run before any evaluation-split signature was read. `phase2/phase2e_mech.py` is written independently of `phase2c_probe.py`, so this is a check rather than a restatement. It reruns the 2.2c two-sidedness counts on the **calibration split only** and asserts them against `reports/tables/phase2c_pair_twosidedness.csv`. If it fails, the bug is in the mechanism and no evaluation number may be produced.

| k | A_right_B_wrong | B_right_A_wrong | both_right | both_wrong | acc_A | acc_B |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 181 | 736 | 29,242 | 5,573 | 0.8234 | 0.8390 |
| 3 | 314 | 740 | 29,109 | 5,569 | 0.8234 | 0.8354 |
| 5 | 546 | 744 | 28,877 | 5,565 | 0.8234 | 0.8290 |
| 10 | 912 | 748 | 28,511 | 5,561 | 0.8234 | 0.8188 |

All four k values reproduce the frozen counts exactly, including the k = 5 pair **546 rule wins against 744 k-NN wins**, and mechanism A's accuracy 0.8234 is identical across k as it must be, since A does not depend on k. The monotone fall of B's accuracy from k = 2 to k = 10 is the calibration trap Amendment 1 voided section 7 over: maximizing accuracy would walk the design back to the k = 1 nesting limit.

Table: reports/tables/phase2e_regression_check.csv

## Held-out accuracy and coverage

| population | blocks | test signatures | rule accuracy | k-NN accuracy | gap (rule - k-NN) | rule coverage | k-NN coverage | agreement | qualifies (>=100 blocks) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 13,902 | 197,479 | 0.8244 | 0.8294 | -0.0050 | 0.9686 | 1.0000 | 0.9493 | yes |
| aminer | 842 | 40,006 | 0.4076 | 0.4038 | 0.0038 | 0.9800 | 1.0000 | 0.9620 | yes |
| arnetminer | 82 | 1,620 | 0.5093 | 0.5099 | -0.0006 | 0.9796 | 1.0000 | 0.9716 |  |
| inspire | 11,110 | 139,369 | 0.9482 | 0.9645 | -0.0163 | 0.9705 | 1.0000 | 0.9612 | yes |
| kisti | 711 | 10,147 | 0.8466 | 0.7334 | 0.1131 | 0.9218 | 1.0000 | 0.7826 | yes |
| pubmed | 34 | 803 | 0.8020 | 0.5554 | 0.2466 | 0.9489 | 1.0000 | 0.6650 |  |
| qian | 276 | 1,696 | 0.6079 | 0.5896 | 0.0183 | 0.9876 | 1.0000 | 0.9629 | yes |
| zbmath | 847 | 3,838 | 0.8494 | 0.9125 | -0.0631 | 0.8953 | 1.0000 | 0.8682 | yes |
| inspire alone | 11,110 | 139,369 | 0.9482 | 0.9645 | -0.0163 | 0.9705 | 1.0000 | 0.9612 | yes |
| pooled non-inspire | 2,792 | 58,110 | 0.5276 | 0.5054 | 0.0221 | 0.9640 | 1.0000 | 0.9206 | yes |

Abstention sits entirely on the rule's side, as Amendment 1 says it must: the rule abstains on 3.14% of test signatures and the k-nearest vote never abstains. Abstention is scored as incorrect throughout.

**Block-size-2 stratum, reported not interpreted.** 2,234 blocks, 2,234 test signatures. Rule accuracy 0.6893, k-NN accuracy 0.8648, rule coverage 0.7739. These blocks are excluded from every hypothesis test.

Table: reports/tables/phase2e_accuracy_by_population.csv

### Two-sidedness on the evaluation split

The single quantity 2.2b could not produce. `rule wins` measured **zero** for the retired pair on 199,713 signatures; for the amended pair it is a positive count at every k on the mandatory curve, so the winner construct is reachable in both directions before any band is cut.

| arm | k | A right, B wrong | B right, A wrong | rule acc | k-NN acc | pooled gap |
| --- | --- | --- | --- | --- | --- | --- |
| levenshtein | 2 | 987 | 3,990 | 0.8244 | 0.8396 | -0.0152 |
| levenshtein | 3 | 1,724 | 4,004 | 0.8244 | 0.8360 | -0.0115 |
| levenshtein | 5 | 3,025 | 4,012 | 0.8244 | 0.8294 | -0.0050 |
| levenshtein | 10 | 5,176 | 4,040 | 0.8244 | 0.8187 | 0.0058 |
| jarowinkler | 5 | 2,946 | 4,002 | 0.8244 | 0.8298 | -0.0053 |

Table: reports/tables/phase2e_twosidedness_eval.csv

## H1, accuracy: does train-only ADS track each mechanism's own accuracy?

Amendment 1 keeps H1 as a construct-validity check, not a contribution. Spearman correlation between train-only ADS and the block's held-out accuracy, with a 95% block-bootstrap interval, for the exact-evidence rule and for the k-nearest vote at k = 5.

| population | blocks | qualifies | rho rule | lo rule | hi rule | rho k-NN | lo k-NN | hi k-NN | both positive, interval excludes 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 13,902 | yes | 0.5069 | 0.4919 | 0.5224 | 0.8298 | 0.8190 | 0.8401 | yes |
| aminer | 842 | yes | 0.6275 | 0.5726 | 0.6770 | 0.6487 | 0.5978 | 0.6974 | yes |
| arnetminer | 82 |  | 0.8464 | 0.7641 | 0.8966 | 0.8553 | 0.7715 | 0.9048 | yes |
| inspire | 11,110 | yes | 0.3361 | 0.3169 | 0.3556 | 0.7570 | 0.7393 | 0.7747 | yes |
| kisti | 711 | yes | 0.4352 | 0.3702 | 0.4931 | 0.5658 | 0.5070 | 0.6205 | yes |
| pubmed | 34 |  | 0.5382 | 0.1822 | 0.7774 | 0.6029 | 0.2919 | 0.8253 | yes |
| qian | 276 | yes | 0.6595 | 0.5617 | 0.7370 | 0.7291 | 0.6461 | 0.7978 | yes |
| zbmath | 847 | yes | 0.2269 | 0.1576 | 0.2978 | 0.6039 | 0.5387 | 0.6638 | yes |
| inspire alone | 11,110 | yes | 0.3361 | 0.3164 | 0.3556 | 0.7570 | 0.7400 | 0.7741 | yes |
| pooled non-inspire | 2,792 | yes | 0.5632 | 0.5344 | 0.5916 | 0.7659 | 0.7451 | 0.7861 | yes |

Table: reports/tables/phase2e_h1_spearman.csv

Mean per-block accuracy by ADS band:

| ads_band | blocks | rule | knn | rule_cov |
| --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 0.4991 | 0.4088 | 0.9218 |
| [0.5,0.7) | 1,101 | 0.6758 | 0.6296 | 0.8931 |
| [0.7,0.9) | 743 | 0.8389 | 0.8165 | 0.9325 |
| [0.9,1.0) | 450 | 0.9418 | 0.9465 | 0.9703 |
| 1.0 | 10,537 | 0.9234 | 0.9889 | 0.9291 |

Figure: `reports/figs/phase2e_h1_ads_accuracy.png`

Qualifying non-inspire datasets (4): aminer, kisti, qian, zbmath. H1 holds in 4 of them: aminer, kisti, qian, zbmath.

## The winner (PREREG section 8, verdicts renamed by Amendment 1)

Per block: paired bootstrap on the accuracy difference, B = 2000, seed 20260918 + block index, 95% percentile interval, four mutually exclusive verdicts `rule wins`, `k-NN wins`, `tie`, `undecided`. Per band and per cell: the pooled gap with an interval from resampling **blocks** with replacement. delta = 0.05 is primary, 0.02 and 0.03 the robustness curve.

Overall per-block verdict distribution, delta = 0.05, k = 5:

| verdict | blocks | share |
| --- | --- | --- |
| rule wins | 191 | 0.0137 |
| k-NN wins | 309 | 0.0222 |
| tie | 10,172 | 0.7317 |
| undecided | 3,230 | 0.2323 |

### Pooled verdict by ADS band (marginal)

| ads_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 47,167 | 0.4490 | 0.4156 | 0.0334 | 0.0289 | 0.0383 | tie | undecided | rule wins |  | 0.1083 |
| [0.5,0.7) | 1,101 | 16,079 | 0.7981 | 0.7767 | 0.0215 | 0.0159 | 0.0272 | tie | tie | undecided |  | 0.0618 |
| [0.7,0.9) | 743 | 12,660 | 0.8777 | 0.8654 | 0.0123 | 0.0068 | 0.0178 | tie | tie | tie |  | 0.0256 |
| [0.9,1.0) | 450 | 12,683 | 0.9563 | 0.9591 | -0.0028 | -0.0064 | 0.0009 | tie | tie | tie |  | 0.0089 |
| 1.0 | 10,537 | 108,890 | 0.9694 | 0.9972 | -0.0278 | -0.0292 | -0.0265 | tie | tie | k-NN wins |  | 0.0278 |

### Pooled verdict by SV band (marginal)

| sv_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.8102 | 0.8490 | -0.0388 | -0.0426 | -0.0352 | tie | k-NN wins | k-NN wins |  | 0.0354 |
| SV low | 3,032 | 56,408 | 0.7864 | 0.8008 | -0.0144 | -0.0160 | -0.0127 | tie | tie | tie |  | 0.0142 |
| SV mid | 3,218 | 59,433 | 0.9041 | 0.9156 | -0.0115 | -0.0133 | -0.0097 | tie | tie | tie |  | 0.0177 |
| SV high | 3,135 | 63,678 | 0.7878 | 0.7689 | 0.0189 | 0.0155 | 0.0226 | tie | tie | undecided |  | 0.0766 |

### Pooled verdict by SV_resid band (marginal)

| svr_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 9,636 | 94,171 | 0.8350 | 0.8474 | -0.0124 | -0.0140 | -0.0107 | tie | tie | tie |  |
| SV low | 1,383 | 45,378 | 0.7835 | 0.7860 | -0.0025 | -0.0053 | 0.0003 | tie | tie | tie |  |
| SV mid | 1,375 | 29,732 | 0.8380 | 0.8405 | -0.0025 | -0.0064 | 0.0014 | tie | tie | tie |  |
| SV high | 1,508 | 28,198 | 0.8409 | 0.8279 | 0.0130 | 0.0077 | 0.0181 | tie | tie | tie |  |

### The 5 x 4 ADS-by-SV grid (PREREG section 9)

The SV effect is only ever shown at fixed ADS and the ADS effect only at fixed SV, because the two axes correlate (Phase 2.1: Pearson -0.2988). Cells under 30 blocks are marked under-powered and decide nothing.

| ads_band | sv_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 | agreement | rule_cov |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | SV=0 | 155 | 2,383 | 0.2509 | 0.2522 | -0.0013 | -0.0028 | 0.0000 | tie | tie | tie |  | 0.0000 | 0.9874 | 0.9874 |
| [0,0.5) | SV low | 272 | 13,131 | 0.2579 | 0.2549 | 0.0030 | 0.0007 | 0.0055 | tie | tie | tie |  | 0.0147 | 0.9762 | 0.9889 |
| [0,0.5) | SV mid | 91 | 5,652 | 0.3850 | 0.3776 | 0.0074 | 0.0031 | 0.0133 | tie | tie | tie |  | 0.0330 | 0.9657 | 0.9867 |
| [0,0.5) | SV high | 553 | 26,001 | 0.5776 | 0.5200 | 0.0576 | 0.0490 | 0.0689 | undecided | rule wins | rule wins |  | 0.1971 | 0.8637 | 0.9469 |
| [0.5,0.7) | SV=0 | 278 | 1,167 | 0.4996 | 0.5124 | -0.0129 | -0.0214 | -0.0063 | tie | tie | undecided |  | 0.0072 | 0.9597 | 0.9597 |
| [0.5,0.7) | SV low | 98 | 1,876 | 0.6210 | 0.6189 | 0.0021 | -0.0062 | 0.0110 | tie | tie | tie |  | 0.0102 | 0.9568 | 0.9771 |
| [0.5,0.7) | SV mid | 157 | 3,527 | 0.7939 | 0.7791 | 0.0147 | 0.0055 | 0.0246 | tie | tie | undecided |  | 0.0573 | 0.9410 | 0.9742 |
| [0.5,0.7) | SV high | 568 | 9,509 | 0.8713 | 0.8393 | 0.0320 | 0.0241 | 0.0408 | tie | undecided | rule wins |  | 0.0986 | 0.8865 | 0.9468 |
| [0.7,0.9) | SV=0 | 119 | 756 | 0.7884 | 0.7976 | -0.0093 | -0.0173 | -0.0032 | tie | tie | tie |  | 0.0000 | 0.9828 | 0.9828 |
| [0.7,0.9) | SV low | 109 | 2,410 | 0.8120 | 0.8075 | 0.0046 | -0.0051 | 0.0148 | tie | tie | tie |  | 0.0000 | 0.9440 | 0.9689 |
| [0.7,0.9) | SV mid | 264 | 4,420 | 0.9045 | 0.8819 | 0.0226 | 0.0128 | 0.0334 | tie | undecided | undecided |  | 0.0417 | 0.9161 | 0.9604 |
| [0.7,0.9) | SV high | 251 | 5,074 | 0.8989 | 0.8886 | 0.0102 | 0.0013 | 0.0198 | tie | tie | tie |  | 0.0319 | 0.9198 | 0.9586 |
| [0.9,1.0) | SV=0 | 43 | 882 | 0.9467 | 0.9524 | -0.0057 | -0.0138 | -0.0011 | tie | tie | tie |  | 0.0000 | 0.9921 | 0.9921 |
| [0.9,1.0) | SV low | 174 | 5,013 | 0.9523 | 0.9531 | -0.0008 | -0.0062 | 0.0050 | tie | tie | tie |  | 0.0057 | 0.9687 | 0.9840 |
| [0.9,1.0) | SV mid | 132 | 3,797 | 0.9602 | 0.9602 | 0.0000 | -0.0060 | 0.0070 | tie | tie | tie |  | 0.0076 | 0.9658 | 0.9800 |
| [0.9,1.0) | SV high | 101 | 2,991 | 0.9609 | 0.9696 | -0.0087 | -0.0179 | 0.0000 | tie | tie | tie |  | 0.0198 | 0.9595 | 0.9749 |
| 1.0 | SV=0 | 3,922 | 12,772 | 0.9349 | 0.9870 | -0.0521 | -0.0567 | -0.0476 | undecided | k-NN wins | k-NN wins |  | 0.0403 | 0.9422 | 0.9422 |
| 1.0 | SV low | 2,379 | 33,978 | 0.9735 | 0.9989 | -0.0254 | -0.0276 | -0.0232 | tie | tie | k-NN wins |  | 0.0156 | 0.9740 | 0.9740 |
| 1.0 | SV mid | 2,574 | 42,037 | 0.9780 | 0.9988 | -0.0209 | -0.0226 | -0.0191 | tie | tie | undecided |  | 0.0128 | 0.9785 | 0.9785 |
| 1.0 | SV high | 1,662 | 20,103 | 0.9665 | 0.9975 | -0.0310 | -0.0342 | -0.0279 | tie | undecided | k-NN wins |  | 0.0391 | 0.9676 | 0.9676 |

Table: reports/tables/phase2e_pooled_cells_sv.csv

Figures: `reports/figs/phase2e_grid_gap_sv.png`, `reports/figs/phase2e_grid_gap_svresid.png`, `reports/figs/phase2e_grid_decided_sv.png`

Figures: `reports/figs/phase2e_verdicts_by_ads.png`, `reports/figs/phase2e_verdicts_by_sv.png`

### Compact regression summary

Per-block gap (rule minus k-NN) on ADS and SV together, with test-set size as a covariate and heteroskedasticity-robust standard errors, for the reason `phase2b_core.ols_robust` states. A summary of the grid, not a substitute for it; no hypothesis is decided from it.

| term | coef | se | t |
| --- | --- | --- | --- |
| intercept | 0.0866 | 0.0088 | 9.8950 |
| ADS | -0.1889 | 0.0076 | -24.7363 |
| SV | 0.0548 | 0.0212 | 2.5822 |
| log(test-set size) | 0.0208 | 0.0018 | 11.8754 |

## Decidability: the gradient and its drivers (Amendment 1 H2, Addendum 1a)

The decided-winner rate of a cell is the share of that cell's blocks whose **per-block** verdict is `rule wins` or `k-NN wins` (resolution 4). H2 says it declines as ADS rises, approaching zero in the top ADS band while staying non-trivially positive below it, and that ADS is the stronger driver of it than SV.

The decline into the ADS = 1.0 band is **partly structural** and Amendment 1 says so in its own text: a block whose train history names one author returns that author from any non-empty pool, so only abstention can differ there. The load-bearing empirical content is the gradient below 1.0 and the existence of a decidable region. Both statements belong in the paper together.

### Decided-winner rate over the frozen 5 x 4 grid

| ads_band | sv_band | n_blocks | decided_rate_0.05 | decided_rate_0.03 | decided_rate_0.02 | n_decided_0.05 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | SV=0 | 155 | 0.0000 | 0.0000 | 0.0000 | 0 |  |
| [0,0.5) | SV low | 272 | 0.0147 | 0.0147 | 0.0184 | 4 |  |
| [0,0.5) | SV mid | 91 | 0.0330 | 0.0440 | 0.0440 | 3 |  |
| [0,0.5) | SV high | 553 | 0.1971 | 0.2477 | 0.2640 | 109 |  |
| [0.5,0.7) | SV=0 | 278 | 0.0072 | 0.0072 | 0.0072 | 2 |  |
| [0.5,0.7) | SV low | 98 | 0.0102 | 0.0102 | 0.0102 | 1 |  |
| [0.5,0.7) | SV mid | 157 | 0.0573 | 0.0637 | 0.0828 | 9 |  |
| [0.5,0.7) | SV high | 568 | 0.0986 | 0.1092 | 0.1162 | 56 |  |
| [0.7,0.9) | SV=0 | 119 | 0.0000 | 0.0000 | 0.0000 | 0 |  |
| [0.7,0.9) | SV low | 109 | 0.0000 | 0.0183 | 0.0183 | 0 |  |
| [0.7,0.9) | SV mid | 264 | 0.0417 | 0.0455 | 0.0455 | 11 |  |
| [0.7,0.9) | SV high | 251 | 0.0319 | 0.0398 | 0.0478 | 8 |  |
| [0.9,1.0) | SV=0 | 43 | 0.0000 | 0.0000 | 0.0000 | 0 |  |
| [0.9,1.0) | SV low | 174 | 0.0057 | 0.0057 | 0.0057 | 1 |  |
| [0.9,1.0) | SV mid | 132 | 0.0076 | 0.0152 | 0.0152 | 1 |  |
| [0.9,1.0) | SV high | 101 | 0.0198 | 0.0297 | 0.0297 | 2 |  |
| 1.0 | SV=0 | 3,922 | 0.0403 | 0.0403 | 0.0403 | 158 |  |
| 1.0 | SV low | 2,379 | 0.0156 | 0.0160 | 0.0164 | 37 |  |
| 1.0 | SV mid | 2,574 | 0.0128 | 0.0148 | 0.0155 | 33 |  |
| 1.0 | SV high | 1,662 | 0.0391 | 0.0403 | 0.0415 | 65 |  |

Table: reports/tables/phase2e_decided_rate_cells.csv

Marginal decided-winner rate by ADS band:

| ads_band | n_blocks | decided_rate_0.05 | decided_rate_0.03 | decided_rate_0.02 | n_decided_0.05 | under_powered |
| --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 0.1083 | 0.1354 | 0.1447 | 116 |  |
| [0.5,0.7) | 1,101 | 0.0618 | 0.0681 | 0.0745 | 68 |  |
| [0.7,0.9) | 743 | 0.0256 | 0.0323 | 0.0350 | 19 |  |
| [0.9,1.0) | 450 | 0.0089 | 0.0133 | 0.0133 | 4 |  |
| 1.0 | 10,537 | 0.0278 | 0.0286 | 0.0290 | 293 |  |

### The gradient at fixed SV (delta = 0.05)

Within each eligible SV band, the decided-winner rate across the eligible ADS cells, in ADS order.

| sv_band | eligible_ADS_cells | non_increasing | top_below_bottom | rates |
| --- | --- | --- | --- | --- |
| SV=0 | 5 |  |  | [0,0.5)=0.0000 / [0.5,0.7)=0.0072 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0000 / 1.0=0.0403 |
| SV low | 5 |  |  | [0,0.5)=0.0147 / [0.5,0.7)=0.0102 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0057 / 1.0=0.0156 |
| SV mid | 5 |  | yes | [0,0.5)=0.0330 / [0.5,0.7)=0.0573 / [0.7,0.9)=0.0417 / [0.9,1.0)=0.0076 / 1.0=0.0128 |
| SV high | 5 |  | yes | [0,0.5)=0.1971 / [0.5,0.7)=0.0986 / [0.7,0.9)=0.0319 / [0.9,1.0)=0.0198 / 1.0=0.0391 |

Non-increasing across ADS in 0 of 4 usable SV bands; strictly lower in the top ADS band than the bottom in 2 of 4. The marginal ADS reading, which is the other available construction of the same clause, gives top below bottom: **True**.

Both readings of the clause are reported because the frozen sentence admits both; the falsification table below requires them to agree and says so if they do not.

Figure: `reports/figs/phase2e_decidability_gradient.png`

### Which signal drives decidability (Addendum 1a)

Primary measure: the one-way, eta-squared style variance decomposition over the eligible cells of the frozen 5 x 4 grid, each cell one unweighted observation. Second required condition: the averaged-range test of the original resolution 5, kept verbatim. **ADS is the stronger driver only if it is larger under both.** A split makes the clause Partial and is reported with both pairs of numbers.

| label | delta | eligible_cells | ADS levels | SV levels | SS_total | eta2_ADS | eta2_SV | avg_range_ADS | avg_range_SV | eta2_ADS_blockweighted | eta2_SV_blockweighted | clause |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full grid | 0.0500 | 20 | 5 | 4 | 0.0401 | 0.1749 | 0.3837 | 0.0707 | 0.0755 | 0.3653 | 0.3765 | failed |
| full grid | 0.0300 | 20 | 5 | 4 | 0.0595 | 0.1664 | 0.3787 | 0.0800 | 0.0901 | 0.3972 | 0.3443 | failed |
| full grid | 0.0200 | 20 | 5 | 4 | 0.0687 | 0.1720 | 0.3783 | 0.0887 | 0.0953 | 0.4114 | 0.3418 | failed |
| ADS < 1.0 only (diagnostic) | 0.0500 | 16 | 4 | 4 | 0.0393 | 0.1755 | 0.4594 | 0.0622 | 0.0875 | 0.2892 | 0.5728 | failed |

Table: reports/tables/phase2e_driver_comparison.csv

The block-weighted decomposition is printed above beside the unweighted one and **decides nothing**, for the reason Addendum 1a gives: the ADS = 1.0 row holds most of the population and its low decidability is the part of H2 that is conceded to be structural, so block-weighting would hand that one row decisive leverage over exactly the comparison H2 needs ADS to win.

The last row restricts the same computation to the four ADS bands below 1.0. It is a **labeled diagnostic and decides nothing**: deleting the top row tests a different hypothesis from the one H2 states, and Addendum 1a pre-registers no such variant. It is reported because a reader is entitled to see how much of the comparison rests on the structural row.

Per-band ranges, full grid: ADS ranges within each SV band SV high=0.1773, SV low=0.0156, SV mid=0.0497, SV=0=0.0403; SV ranges within each ADS band 1.0=0.0275, [0,0.5)=0.1971, [0.5,0.7)=0.0914, [0.7,0.9)=0.0417, [0.9,1.0)=0.0198.

Per-band ranges, ADS < 1.0 diagnostic: ADS ranges within each SV band SV high=0.1773, SV low=0.0147, SV mid=0.0497, SV=0=0.0072; SV ranges within each ADS band [0,0.5)=0.1971, [0.5,0.7)=0.0914, [0.7,0.9)=0.0417, [0.9,1.0)=0.0198.

### A non-trivial decidable region (resolution 6)

At least one ADS band below 1.0 with 30 or more blocks in which 30 or more blocks carry a decided per-block verdict. Bands meeting it at delta = 0.05: **[0,0.5), [0.5,0.7)**.

## The k sensitivity curve (Amendment 1, mandatory)

k is fixed by definition at 5 and is never calibrated by maximizing accuracy, because B's accuracy is monotone toward the single-nearest limit, which is the 2.2b nesting. Every H2 and H3 outcome is recomputed across the curve; an outcome that holds at k = 5 and flips elsewhere is k-dependent and is treated as Partial, not Supported. k = 1 is off the curve as the known-degenerate case (resolution 3).

| k | rule acc | k-NN acc | pooled gap | A right B wrong | B right A wrong | decided rate | decidable region | gradient non-increasing (majority) | eta2_ADS | eta2_SV | driver clause | SV reversal below ADS 1.0 | tie-crossing below ADS 1.0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.8244 | 0.8396 | -0.0152 | 987 | 3,990 | 0.0252 | yes |  | 0.3277 | 0.3751 | split |  |  |
| 3 | 0.8244 | 0.8360 | -0.0115 | 1,724 | 4,004 | 0.0285 | yes |  | 0.1969 | 0.4480 | failed |  |  |
| 5 | 0.8244 | 0.8294 | -0.0050 | 3,025 | 4,012 | 0.0360 | yes |  | 0.1749 | 0.3837 | failed |  |  |
| 10 | 0.8244 | 0.8187 | 0.0058 | 5,176 | 4,040 | 0.0501 | yes |  | 0.1984 | 0.3525 | failed |  | yes |

Table: reports/tables/phase2e_k_curve.csv

Figure: `reports/figs/phase2e_k_curve.png`

## Power report (PREREG section 8, mandatory)

Verdict share as a function of test-set size, so a reader can see how much of any no-winner region is demonstrated equivalence and how much is a small test set. Tie and undecided are never merged.

| test-set size | blocks | rule wins | k-NN wins | tie | undecided |
| --- | --- | --- | --- | --- | --- |
| 1 | 1,309 | 0.0107 | 0.1261 | 0.8633 | 0.0000 |
| 2 | 2,159 | 0.0046 | 0.0412 | 0.8055 | 0.1487 |
| 3-4 | 2,466 | 0.0057 | 0.0069 | 0.7762 | 0.2113 |
| 5-8 | 2,316 | 0.0181 | 0.0099 | 0.7258 | 0.2461 |
| 9-16 | 2,214 | 0.0190 | 0.0045 | 0.6608 | 0.3157 |
| 17-32 | 1,903 | 0.0205 | 0.0026 | 0.6332 | 0.3437 |
| 33-64 | 1,113 | 0.0234 | 0.0000 | 0.6280 | 0.3486 |
| 65-+ | 422 | 0.0095 | 0.0000 | 0.8081 | 0.1825 |

Full curve across all three margins: reports/tables/phase2e_power_by_size.csv

Figure: `reports/figs/phase2e_power_by_size.png`

## Winner structure: reversal, tie-crossing, or compression only (PREREG section 9)

A **winner reversal** is two bands with decided pooled verdicts of opposite identity. A **tie-crossing** is one band decided and another a demonstrated tie, with no band decided the opposite way. **Gap compression only** is a change of magnitude with neither. H3's direction-by-SV clause is scoped to ADS bands below 1.0 by Amendment 1's own wording; the full grid is printed too.

### H3, direction by SV: across SV bands at fixed ADS

**signal/metric: sv**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=tie / SV high=tie | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=tie / SV mid=tie / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 1 | SV=0=k-NN wins / SV low=tie / SV mid=tie / SV high=undecided | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=tie / SV mid=tie / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 1 | SV=0=undecided / SV low=tie / SV mid=undecided / SV high=rule wins | tie-crossing |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 3 | SV=0=k-NN wins / SV low=k-NN wins / SV mid=undecided / SV high=k-NN wins | gap compression only |

**signal/metric: svr**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=undecided / SV mid=undecided / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 1 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=k-NN wins | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 2 | SV=0=undecided / SV low=undecided / SV mid=rule wins / SV high=rule wins | gap compression only |
| [0.5,0.7) | 4 | 1 | SV=0=rule wins / SV low=undecided / SV mid=undecided / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| 1.0 | 4 | 3 | SV=0=k-NN wins / SV low=undecided / SV mid=k-NN wins / SV high=k-NN wins | gap compression only |

**signal/metric: sv_jw**

delta = 0.05

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 0 | SV=0=undecided / SV low=tie / SV mid=tie / SV high=tie | gap compression only |

delta = 0.03

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=tie / SV mid=tie / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=tie | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 1 | SV=0=k-NN wins / SV low=tie / SV mid=tie / SV high=undecided | tie-crossing |

delta = 0.02

| ads_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| [0,0.5) | 4 | 1 | SV=0=tie / SV low=tie / SV mid=tie / SV high=rule wins | tie-crossing |
| [0.5,0.7) | 4 | 1 | SV=0=undecided / SV low=tie / SV mid=undecided / SV high=rule wins | tie-crossing |
| [0.7,0.9) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=undecided | gap compression only |
| [0.9,1.0) | 4 | 0 | SV=0=tie / SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| 1.0 | 4 | 3 | SV=0=k-NN wins / SV low=k-NN wins / SV mid=undecided / SV high=k-NN wins | gap compression only |

### H3, non-direction by ADS: across ADS bands at fixed SV

**signal/metric: sv**

delta = 0.05

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=undecided | gap compression only |
| SV low | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV high | 5 | 0 | [0,0.5)=undecided / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |

delta = 0.03

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=k-NN wins | tie-crossing |
| SV low | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=undecided / [0.9,1.0)=tie / 1.0=tie | gap compression only |
| SV high | 5 | 1 | [0,0.5)=rule wins / [0.5,0.7)=undecided / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=undecided | tie-crossing |

delta = 0.02

| sv_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| SV=0 | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=undecided / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=k-NN wins | tie-crossing |
| SV low | 5 | 1 | [0,0.5)=tie / [0.5,0.7)=tie / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=k-NN wins | tie-crossing |
| SV mid | 5 | 0 | [0,0.5)=tie / [0.5,0.7)=undecided / [0.7,0.9)=undecided / [0.9,1.0)=tie / 1.0=undecided | gap compression only |
| SV high | 5 | 3 | [0,0.5)=rule wins / [0.5,0.7)=rule wins / [0.7,0.9)=tie / [0.9,1.0)=tie / 1.0=k-NN wins | winner reversal |

### Per-dataset generalization (PREREG section 11)

inspire is the great majority of live blocks, so a pooled number is mostly an inspire number. A finding generalizes only if it holds pooled non-inspire **and** in a majority of qualifying non-inspire datasets (100 or more blocks in the primary analysis population).

| population | blocks | qualifies (>=100 blocks) | ADS bands (<1.0) with 2+ eligible SV bands | ADS bands (<1.0) with 2+ decided SV bands | winner reversal | tie-crossing | decidable region | gradient non-increasing (majority) | gradient top<bottom (marginal) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aminer | 842 | yes | 2 | 0 |  |  |  |  |  |
| arnetminer | 82 |  | 0 | 0 |  |  |  |  | None |
| inspire | 11,110 | yes | 3 | 0 |  |  | yes |  | yes |
| kisti | 711 | yes | 0 | 0 |  |  | yes | yes | yes |
| pubmed | 34 |  | 0 | 0 |  |  |  |  | None |
| qian | 276 | yes | 0 | 0 |  |  |  | yes | yes |
| zbmath | 847 | yes | 0 | 0 |  |  |  | yes | yes |
| inspire alone | 11,110 | yes | 3 | 0 |  |  | yes |  | yes |
| pooled non-inspire | 2,792 | yes | 4 | 0 |  | yes | yes |  | yes |

Table: reports/tables/phase2e_generalization.csv

## Diagnostics required by the pre-registration

### Mechanism agreement rate per SV band (PREREG section 4)

The share of test signatures on which the two mechanisms return the identical prediction. B never abstains, so a rule abstention counts as a disagreement. Under the retired 2.2b pair this diagnostic collapsed to the identity `exact coverage + fuzzy abstention rate`; under the amended pair it is an observation again, because the two mechanisms can disagree while both firing.

| sv_band | n_blocks | n_test | agreement | rule_cov | rule_acc | knn_acc | median_n_test | mean_n_test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.9535 | 0.9535 | 0.8102 | 0.8490 | 2.0000 | 3.9761 |
| SV low | 3,032 | 56,408 | 0.9721 | 0.9782 | 0.7864 | 0.8008 | 11.0000 | 18.6042 |
| SV mid | 3,218 | 59,433 | 0.9696 | 0.9778 | 0.9041 | 0.9156 | 11.0000 | 18.4689 |
| SV high | 3,135 | 63,678 | 0.9089 | 0.9557 | 0.7878 | 0.7689 | 9.0000 | 20.3120 |

### Jaro-Winkler robustness arm (PREREG section 9, restated by Amendment 1)

The same k-nearest vote with Jaro-Winkler similarity in place of normalized Levenshtein. It calibrates nothing, because there is no cutoff to calibrate.

| sv_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | decided_rate_0.05 | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 4,517 | 17,960 | 0.8102 | 0.8490 | -0.0388 | -0.0426 | -0.0351 | tie | 0.0354 |  |
| SV low | 3,032 | 56,408 | 0.7864 | 0.8010 | -0.0146 | -0.0162 | -0.0130 | tie | 0.0135 |  |
| SV mid | 3,218 | 59,433 | 0.9041 | 0.9157 | -0.0116 | -0.0135 | -0.0098 | tie | 0.0177 |  |
| SV high | 3,135 | 63,678 | 0.7878 | 0.7697 | 0.0181 | 0.0147 | 0.0215 | tie | 0.0775 |  |

### INIT stratification (PREREG section 9, secondary control)

INIT is the train-only share of signatures whose given-name field is an initial only. The SV-to-winner relationship is shown inside each INIT band, which asks whether the effect exists among blocks homogeneous in initialization style.

| init_band | sv_band | n_blocks | n_test | pooled_gap | ci_lo | ci_hi | verdict_0.05 | decided_rate_0.05 | agreement | under_powered |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INIT=0 | SV=0 | 3,743 | 15,253 | -0.0266 | -0.0300 | -0.0234 | tie | 0.0190 | 0.9656 |  |
| INIT=0 | SV low | 684 | 9,373 | -0.0106 | -0.0153 | -0.0059 | tie | 0.0234 | 0.9515 |  |
| INIT=0 | SV mid | 277 | 2,385 | 0.0289 | 0.0143 | 0.0445 | tie | 0.0722 | 0.8876 |  |
| INIT=0 | SV high | 508 | 4,746 | 0.1363 | 0.1182 | 0.1557 | rule wins | 0.1693 | 0.7141 |  |
| 0<INIT<0.5 | SV low | 1,047 | 26,947 | -0.0078 | -0.0096 | -0.0061 | tie | 0.0029 | 0.9810 |  |
| 0<INIT<0.5 | SV mid | 1,325 | 27,865 | -0.0092 | -0.0117 | -0.0067 | tie | 0.0113 | 0.9746 |  |
| 0<INIT<0.5 | SV high | 1,249 | 36,481 | 0.0172 | 0.0126 | 0.0224 | tie | 0.0641 | 0.9181 |  |
| INIT>=0.5 | SV=0 | 774 | 2,707 | -0.1071 | -0.1237 | -0.0912 | k-NN wins | 0.1150 | 0.8851 |  |
| INIT>=0.5 | SV low | 1,301 | 20,088 | -0.0249 | -0.0282 | -0.0220 | tie | 0.0184 | 0.9700 |  |
| INIT>=0.5 | SV mid | 1,616 | 29,183 | -0.0170 | -0.0194 | -0.0148 | tie | 0.0136 | 0.9715 |  |
| INIT>=0.5 | SV high | 1,378 | 22,451 | -0.0033 | -0.0075 | 0.0009 | tie | 0.0537 | 0.9350 |  |

Structure across SV within each INIT band, delta = 0.05:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 1 | SV=0=tie / SV low=tie / SV mid=tie / SV high=rule wins | tie-crossing |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| INIT>=0.5 | 4 | 1 | SV=0=k-NN wins / SV low=tie / SV mid=tie / SV high=tie | tie-crossing |

Structure across SV within each INIT band, delta = 0.03:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 1 | SV=0=tie / SV low=tie / SV mid=undecided / SV high=rule wins | tie-crossing |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=tie | gap compression only |
| INIT>=0.5 | 4 | 1 | SV=0=k-NN wins / SV low=tie / SV mid=tie / SV high=tie | tie-crossing |

Structure across SV within each INIT band, delta = 0.02:

| init_band | eligible_bands | decided_bands | verdicts | outcome |
| --- | --- | --- | --- | --- |
| INIT=0 | 4 | 2 | SV=0=k-NN wins / SV low=tie / SV mid=undecided / SV high=rule wins | winner reversal |
| 0<INIT<0.5 | 3 | 0 | SV low=tie / SV mid=tie / SV high=undecided | gap compression only |
| INIT>=0.5 | 4 | 2 | SV=0=k-NN wins / SV low=k-NN wins / SV mid=tie / SV high=tie | tie-crossing |

### How much of SV is forename initialization?

Spearman correlations among the design-time signals on the primary analysis population. Unchanged from 2.2b, since the signals are unchanged; reprinted because the SV_resid control is load-bearing for H3.

|  | ads | sv | sv_resid | init |
| --- | --- | --- | --- | --- |
| ads | 1.0000 | -0.2704 | -0.2744 | 0.1794 |
| sv | -0.2704 | 1.0000 | 0.5125 | 0.3627 |
| sv_resid | -0.2744 | 0.5125 | 1.0000 | 0.2025 |
| init | 0.1794 | 0.3627 | 0.2025 | 1.0000 |

## The amended falsification table, evaluated (Amendment 1 section 10)

Outcomes are read off the rules frozen at Phase 2.2d, in the order the pre-registration fixes: **Inconclusive is evaluated first** and takes precedence over every other row. An outcome that holds at one margin or one k and flips elsewhere is margin-dependent or k-dependent and is treated as Partial, not Supported.

### H1, accuracy (validity check, not a contribution)

**Outcome: Supported**

- primary analysis population blocks: 13,902
- qualifying non-inspire datasets: 4 (aminer, kisti, qian, zbmath)
- Spearman rho, rule: 0.5069, 95% CI [0.4919, 0.5224]
- Spearman rho, k-NN: 0.8298, 95% CI [0.8190, 0.8401]
- generalizes: True

### H2, consistency gates decidability

**Outcome: Inconclusive**

- decided ADS bands (30+ blocks, pooled verdict): []
- decided SV bands (30+ blocks, pooled verdict): []
- gradient non-increasing across ADS in a majority of eligible SV bands: False (0 of 4 usable SV bands)
- top ADS band strictly below the bottom, per SV band (majority): False (2 of 4)
- top ADS band strictly below the bottom, marginal reading: True
- non-trivial decidable region below ADS = 1.0 (resolution 6): True ([0,0.5), [0.5,0.7))
- eta2_ADS vs eta2_SV (Addendum 1a primary): 0.1749 vs 0.3837
- averaged range ADS vs SV (Addendum 1a second condition): 0.0707 vs 0.0755
- ADS is the stronger driver: failed
- block-weighted eta2 (diagnostic, decides nothing): 0.3653 vs 0.3765
- holds in the pooled non-inspire analysis: False

### H3, surface stability directs the choice

**Outcome: Inconclusive**

- ADS bands with 2+ eligible SV bands (any ADS): 5
- ADS bands with 2+ decided SV bands (any ADS): 0
- ADS bands below 1.0 with 2+ decided SV bands: 0
- SV reversal below ADS = 1.0: False
- tie-crossing below ADS = 1.0: False
- no ADS-driven reversal at fixed SV (non-direction by ADS): True
- SV_resid reversal below ADS = 1.0: False
- Jaro-Winkler reversal below ADS = 1.0: False
- generalizes: None

### Margin sensitivity (PREREG section 8)

| delta | H2 | H3 |
| --- | --- | --- |
| 0.0500 | Inconclusive | Inconclusive |
| 0.0300 | Inconclusive | Inconclusive |
| 0.0200 | Inconclusive | Partial |

H2 constant across margins: yes. H3 constant across margins: **no, margin-dependent**.

### k sensitivity (Amendment 1, mandatory)

The clauses each hypothesis rests on, recomputed across k in {2, 3, 5, 10} at the primary margin.

| k | decidable region | gradient non-increasing (majority) | driver clause |
| --- | --- | --- | --- |
| 2 | yes |  | split |
| 3 | yes |  | failed |
| 5 | yes |  | failed |
| 10 | yes |  | failed |

| k | SV reversal below ADS 1.0 | tie-crossing below ADS 1.0 |
| --- | --- | --- |
| 2 |  |  |
| 3 |  |  |
| 5 |  |  |
| 10 |  | yes |

H2's clauses constant across k: **no, k-dependent**. H3's clauses constant across k: **no, k-dependent**.

Figure: `reports/figs/phase2e_margin_sensitivity.png`

## What these outcomes do and do not say

**Why H2 and H3 are Inconclusive.** The Order of evaluation rule puts the power floor first and it is not met at the primary margin. Every marginal pooled verdict at delta = 0.05 is a demonstrated tie, because every marginal pooled gap is smaller than 0.05 in absolute value: +0.0334, +0.0215, +0.0123, -0.0028, -0.0278 across ADS bands, -0.0388, -0.0144, -0.0115, +0.0189 across SV bands. H2 needs two decided ADS bands and two decided SV bands and has none of either; H3 needs two decided SV bands inside a single ADS band and has none. This is the same floor that bit in 2.2b, for a different reason. In 2.2b no winner was reachable at all. Here the pair is two-sided, the gap changes sign on both axes, and the margin is simply wider than the effect.

Four things stand beside the verdict. None is a hypothesis outcome and none is offered in place of one.

**1. The pooled gap changes sign on both axes.** Across ADS bands it runs +0.0334 -> +0.0215 -> +0.0123 -> -0.0028 -> -0.0278, from the rule ahead at low consistency to the k-nearest vote ahead at ADS = 1.0. Across SV bands it runs -0.0388 -> -0.0144 -> -0.0115 -> +0.0189, from the vote ahead where the history is written one way to the rule ahead where it is most varied. At delta = 0.02 the ADS ordering becomes a decided marginal reversal, `rule wins` in [0,0.5) against `k-NN wins` at 1.0. Both design-time signals therefore carry winner-identity information, which is more than H3's SV clause claims and more than the retired selection-blindness claim allowed for ADS.

**2. The decidability gradient is not monotone and does not approach zero at ADS = 1.0.** The marginal decided-winner rate runs [0,0.5)=0.1083 / [0.5,0.7)=0.0618 / [0.7,0.9)=0.0256 / [0.9,1.0)=0.0089 / 1.0=0.0278. It falls through the first four bands and then **rises** in the top band, from 0.0089 in [0.9,1.0) to 0.0278 at ADS = 1.0. Amendment 1 predicted it would approach zero there. It does not, and the reason is the structural argument the amendment itself makes: at ADS = 1.0 the only move the rule can make is to abstain, and in the blocks where it abstains often the vote wins by a wide and decidable margin. The collapse Amendment 1 conceded is real in the pooled gap but not in the decided-winner rate, and the top ADS band holds 10,537 of the 13,902 blocks in the primary analysis population.

**3. SV, not ADS, is the stronger driver of decidability.** Addendum 1a's clause fails, and it fails under **both** required measures rather than splitting: eta2_ADS 0.1749 against eta2_SV 0.3837, averaged ranges 0.0707 against 0.0755. It fails at every margin on the robustness curve and at every k on the mandatory curve, so it is neither margin-dependent nor k-dependent. Dropping the structural ADS = 1.0 row widens the gap rather than closing it, 0.1755 against 0.4594, so the failure is not an artifact of the row Amendment 1 conceded. This is the clause H2 needed ADS to win. It does not decide H2, because the power floor is evaluated first, but it is the sharpest measurement in this pass and it points against the role assignment the 2.2d reframe adopted.

**4. There is no SV-driven winner reversal anywhere below ADS = 1.0, at any margin.** The strongest structure the frozen rules find below the top band is a tie-crossing at delta = 0.02. Substantively the shape is the pre-registered **gap compression** one: at fixed ADS the gap rises with SV and changes sign, but only the high-SV side ever clears a margin. Under the frozen rules that reading is a hypothesis outcome only above the power floor, which the primary margin does not clear, so it is reported here as substance and not as H3 Not supported.

**One pre-registration ambiguity, found at run time and handled by reporting both readings.** Amendment 1's H2 Supported row reads: holding SV fixed, the decided-winner rate is non-increasing across ADS bands in the majority of eligible SV bands, **and** is strictly lower in the top ADS band than in the bottom. The second clause admits two constructions, within each eligible SV band or on the marginal ADS bands, and they disagree here. Per SV band it holds in 2 of 4 usable bands, so not a majority; marginally it holds. Both are printed in the H2 facts above and neither was picked after seeing which way it fell. The disagreement changes no outcome, because H2 is Inconclusive on the power floor, which is evaluated first. It is recorded so that the construction is fixed before it can matter.

**What this leaves for Phase 2.3.** The blocking issue of 2.2b is gone: the pair is two-sided, `rule wins` is reachable, and 500 blocks carry a decided per-block verdict at the primary margin, so a selector has something to select over. What the pass does not supply is a measured basis for the two-signal role assignment, because the one pre-registered clause that tested it came out against ADS. Whether 2.3 proceeds on the amended framing, and what charter invariant 4's ADS-only and SV-only baselines should now be expected to show, is a decision for review and not for this pass.
