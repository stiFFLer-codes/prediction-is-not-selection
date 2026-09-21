# Phase 2.7b: re-analysis of the frozen records

Produced by `phase2/phase2_7b_reanalysis.py` on the committed per-block records of `reports/tables/phase2e_blocks_scored.csv.gz` and the S2AND signature table already ingested. It answers peer-review majors 1, 2, 3 and 8 of `reports/phase2_7_peer_review.md`.

**What this pass is.** Supplementary and sensitivity analysis on records that already exist, computed deterministically at the frozen seed. **What it is not.** It re-runs no experiment, re-draws no split, re-tunes nothing, and alters no frozen definition. `PREREG.md`, Amendment 1 and Addendum 1a are untouched. The frozen primary analysis population is unchanged at 13,902 blocks and 197,479 test signatures, and every frozen number it reports is re-derived here before anything is added to it.

Inputs: `reports/tables/phase2e_blocks_scored.csv.gz`, `data/phase2e_eval_sigs.parquet`, `data/s2and_signatures.parquet`. Seed 20260918 throughout, B = 2000, delta = 0.05 primary with 0.02 and 0.03 beside it, k = 5 primary.

## Headline: does anything change an H1, H2 or H3 conclusion?

**No hypothesis verdict moves. One general claim in the surrounding prose does, and it is the paper's headline sentence.**

H1 Supported, H2 Inconclusive, H3 Inconclusive at the primary margin and Partial at delta = 0.02, exactly as the frozen falsification table reports them. H2 and H3 were carried to Inconclusive by the pre-registered power floor, which counts decided pooled verdicts over **ADS and SV** bands, and nothing below gives an ADS band, an SV band or a grid cell a decided pooled verdict at delta = 0.05 in any population examined. Section 1b checks that against the restricted population rather than assuming it.

**Flagged, because it shapes the prose pass. Block size, a design-time signal the pre-registration did not carry, produces 2 decided pooled band verdicts at the primary margin:** blocks of 3-4 signatures give a pooled gap of -0.1145 [-0.1286, -0.1007], `k-NN wins`; blocks of 5-8 signatures give a pooled gap of -0.0712 [-0.0807, -0.0614], `k-NN wins`. Neither ADS nor SV produces a single decided marginal band. Taken alone this is a counter-example to "design-time mechanism selection has no signal a designer can act on" stated without qualification. Section 2 measures what it actually is: at fixed ADS the effect is gap compression with no sign change in either stratum, the marginal reversal is composition, and the decided cells are driven by the rule's abstentions rather than by how either mechanism resolves a name. The scoping decision that follows is the author's, and it is the same decision peer-review major 4 asks for.

Four further things change, all of them reporting rather than verdicts.

1. **The H2 decidability gradient is monotone once degenerate blocks are removed.** 2.2e reported that the decided-winner rate rises again in the top ADS band instead of approaching zero, against Amendment 1's prediction. On blocks with at least 3 test signatures it does not rise: the ADS = 1.0 rate falls from 0.0278 to 0.0070, below the band beneath it. The reported non-monotonicity is a small-block artifact and section 1 says so with the table.
2. **The decided-verdict count is composed differently than the manuscript implies and its direction is an artifact of the small end.** 278 of the 500 decided verdicts come from blocks with one or two test signatures. Restricted, the per-block margin flips from 191 rule wins against 309 k-NN wins to 167 against 55.
3. **The driver comparison now has an interval.** At k = 5 eta2_SV - eta2_ADS is +0.2088 [+0.0628, +0.3473], excluding zero before and after a size adjustment. At k = 2 it is +0.0474 [-0.2531, +0.3159], which does not. "Stable across k" is accurate for the verdict and not for the evidence behind it.
4. **There is a hard accuracy ceiling neither mechanism can pass, and it is not the reason the datasets differ.** 4.14% of held-out signatures name an author the block's training half never shows, so no mechanism in this family can exceed 0.9586. Per dataset the ceiling ranges from 0.8435 to 0.9964, and normalizing for it closes only about 13% of the aminer-to-inspire spread, against the natural guess that it explains most of it. The rule's precision where it fires, 0.8512, is above the vote's accuracy, 0.8294, which is the number the precision-first framing implies and the manuscript never prints.

Every item above is a table and a paragraph for the 2.7c prose pass. Only the flagged one is a claim change.

---

## 1. Small-test-block sensitivity (Major 1)

The paired per-block bootstrap of `PREREG.md` section 8 resamples a block's test signatures as a multinomial over the three per-signature outcomes {+1, 0, -1}. At one test signature that distribution is a point mass, so the interval is [0, 0], [+1, +1] or [-1, -1] and the block is recorded as a demonstrated tie or as a decided winner on the strength of one item. It can never be `undecided`. At two test signatures the interval takes three values and is still coarse.

This section recomputes everything the per-block verdict feeds on blocks with at least 3 test signatures, and prints it beside the frozen all-blocks version. **It is a sensitivity analysis. The frozen primary analysis is unchanged and is the all-blocks column.**

Population: 10,434 of 13,902 blocks survive the restriction (75.05%), carrying 191,852 of 197,479 test signatures (97.15%). The restriction removes small blocks, so it costs a quarter of the blocks and under 3% of the signatures.

### 1a. Four-verdict per-block distribution and the decided-winner rate

| population | blocks | rule wins | k-NN wins | tie | undecided | decided | decided_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all blocks (frozen primary) | 13,902 | 191 | 309 | 10,172 | 3,230 | 500 | 0.0360 |
| n_test >= 3 | 10,434 | 167 | 55 | 7,303 | 2,909 | 222 | 0.0213 |
| n_test = 1 only | 1,309 | 14 | 165 | 1,130 | 0 | 179 | 0.1367 |
| n_test = 2 only | 2,159 | 10 | 89 | 1,739 | 321 | 99 | 0.0459 |

| population | blocks | share_rule wins | share_k-NN wins | share_tie | share_undecided |
| --- | --- | --- | --- | --- | --- |
| all blocks (frozen primary) | 13,902 | 0.0137 | 0.0222 | 0.7317 | 0.2323 |
| n_test >= 3 | 10,434 | 0.0160 | 0.0053 | 0.6999 | 0.2788 |
| n_test = 1 only | 1,309 | 0.0107 | 0.1261 | 0.8633 | 0.0000 |
| n_test = 2 only | 2,159 | 0.0046 | 0.0412 | 0.8055 | 0.1487 |

Table: reports/tables/phase2_7b_verdict_distribution.csv

**The size-1 and size-2 strata explicitly.** The size-1 stratum holds 1,309 blocks: 14 `rule wins`, 165 `k-NN wins`, 1,130 `tie` and **0 `undecided`**, the last of which is zero by construction and not by evidence. The size-2 stratum holds 2,159 blocks: 10, 89, 1,739 and 321. Together the two strata supply **278 of the 500 decided verdicts (55.6%)** and **2,869 of the 10,172 demonstrated ties (28.2%)** in the frozen primary analysis.

**The decided-winner rate falls from 0.0360 to 0.0213 under the restriction**, and the direction of the per-block margin flips: all blocks give 191 `rule wins` against 309 `k-NN wins`, the restricted set gives 167 against 55. The tie share falls from 0.7317 to 0.6999 and the undecided share rises from 0.2323 to 0.2788, which is the degeneracy being removed rather than a change of evidence.

### 1b. The H2 decidability gradient across ADS bands

Marginal decided-winner rate by ADS band, delta = 0.05, k = 5.

| ads_band | blocks_all | decided_rate_all | blocks_n3 | decided_rate_n3 |
| --- | --- | --- | --- | --- |
| [0,0.5) | 1,071 | 0.1083 | 1,040 | 0.1096 |
| [0.5,0.7) | 1,101 | 0.0618 | 767 | 0.0443 |
| [0.7,0.9) | 743 | 0.0256 | 709 | 0.0254 |
| [0.9,1.0) | 450 | 0.0089 | 450 | 0.0089 |
| 1.0 | 10,537 | 0.0278 | 7,468 | 0.0070 |

Table: reports/tables/phase2_7b_gradient_ads.csv

The pooled band verdicts under the restriction, which is what the pre-registered power floor actually counts:

| ads_band | n_blocks | n_test | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [0,0.5) | 1,040 | 47,105 | 0.0332 | 0.0288 | 0.0380 | tie | undecided | rule wins |  | 0.1096 |
| [0.5,0.7) | 767 | 15,537 | 0.0211 | 0.0160 | 0.0267 | tie | tie | undecided |  | 0.0443 |
| [0.7,0.9) | 709 | 12,592 | 0.0124 | 0.0073 | 0.0179 | tie | tie | tie |  | 0.0254 |
| [0.9,1.0) | 450 | 12,683 | -0.0028 | -0.0062 | 0.0009 | tie | tie | tie |  | 0.0089 |
| 1.0 | 7,468 | 103,935 | -0.0235 | -0.0247 | -0.0224 | tie | tie | k-NN wins |  | 0.0070 |

| sv_band | n_blocks | n_test | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SV=0 | 2,071 | 14,064 | -0.0242 | -0.0278 | -0.0211 | tie | tie | k-NN wins |  | 0.0048 |
| SV low | 2,846 | 56,083 | -0.0136 | -0.0153 | -0.0121 | tie | tie | tie |  | 0.0091 |
| SV mid | 3,004 | 59,063 | -0.0107 | -0.0124 | -0.0090 | tie | tie | tie |  | 0.0113 |
| SV high | 2,513 | 62,642 | 0.0208 | 0.0173 | 0.0244 | tie | tie | undecided |  | 0.0605 |

Table: reports/tables/phase2_7b_restricted_marginals.csv

**0 ADS bands, 0 SV bands and 0 of the 20 grid cells carry a decided pooled verdict at delta = 0.05 under the restriction**, exactly as in the frozen analysis. The pre-registered power floor still bites first, so H2 and H3 stay Inconclusive whichever population is used.

Gradient clauses at fixed SV, all blocks (frozen):

| sv_band | eligible_ADS_cells | non_increasing | top_below_bottom | rates |
| --- | --- | --- | --- | --- |
| SV=0 | 5 |  |  | [0,0.5)=0.0000 / [0.5,0.7)=0.0072 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0000 / 1.0=0.0403 |
| SV low | 5 |  |  | [0,0.5)=0.0147 / [0.5,0.7)=0.0102 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0057 / 1.0=0.0156 |
| SV mid | 5 |  | yes | [0,0.5)=0.0330 / [0.5,0.7)=0.0573 / [0.7,0.9)=0.0417 / [0.9,1.0)=0.0076 / 1.0=0.0128 |
| SV high | 5 |  | yes | [0,0.5)=0.1971 / [0.5,0.7)=0.0986 / [0.7,0.9)=0.0319 / [0.9,1.0)=0.0198 / 1.0=0.0391 |

Non-increasing across ADS in 0 of 4 usable SV bands; strictly lower in the top ADS band than the bottom in 2 of 4. Marginal ADS reading, top below bottom: **True**.

Gradient clauses at fixed SV, n_test >= 3:

| sv_band | eligible_ADS_cells | non_increasing | top_below_bottom | rates |
| --- | --- | --- | --- | --- |
| SV=0 | 5 |  |  | [0,0.5)=0.0000 / [0.5,0.7)=0.0000 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0000 / 1.0=0.0060 |
| SV low | 5 |  | yes | [0,0.5)=0.0148 / [0.5,0.7)=0.0114 / [0.7,0.9)=0.0000 / [0.9,1.0)=0.0057 / 1.0=0.0091 |
| SV mid | 5 |  | yes | [0,0.5)=0.0333 / [0.5,0.7)=0.0368 / [0.7,0.9)=0.0425 / [0.9,1.0)=0.0076 / 1.0=0.0059 |
| SV high | 5 | yes | yes | [0,0.5)=0.2008 / [0.5,0.7)=0.0648 / [0.7,0.9)=0.0295 / [0.9,1.0)=0.0198 / 1.0=0.0066 |

Non-increasing across ADS in 1 of 4 usable SV bands; strictly lower in the top ADS band than the bottom in 3 of 4. Marginal ADS reading, top below bottom: **True**.

### 1c. The Addendum 1a driver comparison under the restriction

| label | delta | eligible_cells | SS_total | eta2_ADS | eta2_SV | avg_range_ADS | avg_range_SV | clause |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all blocks (frozen) | 0.0500 | 20 | 0.0401 | 0.1749 | 0.3837 | 0.0707 | 0.0755 | failed |
| all blocks (frozen) | 0.0300 | 20 | 0.0595 | 0.1664 | 0.3787 | 0.0800 | 0.0901 | failed |
| all blocks (frozen) | 0.0200 | 20 | 0.0687 | 0.1720 | 0.3783 | 0.0887 | 0.0953 | failed |
| n_test >= 3 | 0.0500 | 20 | 0.0384 | 0.2136 | 0.3113 | 0.0629 | 0.0662 | failed |
| n_test >= 3 | 0.0300 | 20 | 0.0600 | 0.2083 | 0.3173 | 0.0755 | 0.0823 | failed |
| n_test >= 3 | 0.0200 | 20 | 0.0695 | 0.2081 | 0.3262 | 0.0841 | 0.0876 | failed |

Table: reports/tables/phase2_7b_driver_restricted.csv

### 1d. Does anything change?

**The gradient changes shape, and this is the one substantive result of task 1.** The frozen marginal gradient runs 0.1083 / 0.0618 / 0.0256 / 0.0089 / 0.0278 and 2.2e reported, against Amendment 1's prediction, that it **rises again** in the top ADS band instead of approaching zero. Restricted to blocks with at least 3 test signatures it runs 0.1096 / 0.0443 / 0.0254 / 0.0089 / 0.0070, which is monotonically non-increasing: the ADS = 1.0 rate falls from 0.0278 to 0.0070 and now sits **below** the [0.9,1.0) band rather than above it. The rise Amendment 1 did not predict is carried by blocks with one or two test signatures inside the ADS = 1.0 band.

One of the two per-SV clause counts moves with it. Non-increasing across ADS in 1 of 4 usable SV bands restricted, against 0 of 4 frozen, which is still not a majority. Top ADS band strictly below the bottom in 3 of 4 against 2 of 4, which **is** a majority restricted and was not frozen. The marginal reading stays True in both. So the clause the frozen analysis reported as failing on a two-of-four split passes on the restricted population.

**This does not move H2.** The clause counts above are read only after the power floor, and the floor is unchanged: no marginal band and no cell is decided at delta = 0.05 under the restriction, as the tables in 1b show. H2 would still return Inconclusive on the first gate. What changes is the **narrative** the manuscript attaches to the gradient, and that is a prose matter for 2.7c: the reported non-monotonicity is a small-block artifact, and on blocks large enough for the interval to mean anything the gradient behaves the way Amendment 1 said it would.

**The driver comparison keeps its verdict and loses half its margin.** Restricted, eta2_ADS = 0.2136 against eta2_SV = 0.3113 at the primary margin, against 0.1749 and 0.3837 frozen: the difference narrows from +0.2088 to +0.0977. The averaged ranges are 0.0629 against 0.0662, against 0.0707 and 0.0755 frozen. ADS still loses under both measures at every margin in the table above, so Addendum 1a's clause comes out **failed** either way. The direction is robust to the restriction; the size of the gap is not, and section 3's interval says the same thing a different way.

## 2. Block size as a third design-time signal (Major 2)

Block size is the total number of signatures in a block. It is readable before anything is built, from the blocking pass alone, with no labels and no mechanism, so it satisfies the same design-time criterion as ADS and SV. It was **not** pre-registered and nothing below is a pre-registered test: this is a supplementary analysis of a signal the frozen regression named and the frozen design did not carry.

Bands are octaves on block size, the same shape as the frozen test-set-size strata, starting at 3 because the primary population rule n_train >= 2 admits no smaller block. They were chosen for balance and are not fitted to any outcome; every band holds well above the 30-block eligibility floor.

### Pooled gap by block-size band, full primary population

| bsize_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 | rule_cov | rule_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3-4 | 2,227 | 3,145 | 0.7892 | 0.9037 | -0.1145 | -0.1286 | -0.1007 | k-NN wins | k-NN wins | k-NN wins |  | 0.1055 | 0.8423 | 0.9370 |
| 5-8 | 2,188 | 5,323 | 0.8506 | 0.9218 | -0.0712 | -0.0807 | -0.0614 | k-NN wins | k-NN wins | k-NN wins |  | 0.0238 | 0.8927 | 0.9529 |
| 9-16 | 2,181 | 8,675 | 0.8656 | 0.9006 | -0.0350 | -0.0430 | -0.0271 | tie | undecided | k-NN wins |  | 0.0179 | 0.9217 | 0.9391 |
| 17-32 | 2,293 | 17,194 | 0.8972 | 0.9090 | -0.0118 | -0.0169 | -0.0065 | tie | tie | tie |  | 0.0305 | 0.9521 | 0.9424 |
| 33-64 | 2,204 | 32,059 | 0.9207 | 0.9276 | -0.0069 | -0.0101 | -0.0034 | tie | tie | tie |  | 0.0222 | 0.9631 | 0.9560 |
| 65-128 | 1,652 | 45,924 | 0.9394 | 0.9393 | 0.0001 | -0.0027 | 0.0031 | tie | tie | tie |  | 0.0188 | 0.9786 | 0.9599 |
| 129+ | 1,157 | 85,159 | 0.7069 | 0.7014 | 0.0056 | 0.0037 | 0.0077 | tie | tie | tie |  | 0.0207 | 0.9827 | 0.7194 |

### Pooled gap by block-size band, n_test >= 3 subset

| bsize_band | n_blocks | n_test | rule_acc | knn_acc | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.03 | verdict_0.02 | under_powered | decided_rate_0.05 | rule_cov | rule_precision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5-8 | 947 | 2,841 | 0.8589 | 0.9236 | -0.0648 | -0.0774 | -0.0514 | k-NN wins | k-NN wins | k-NN wins |  | 0.0095 | 0.9011 | 0.9531 |
| 9-16 | 2,181 | 8,675 | 0.8656 | 0.9006 | -0.0350 | -0.0424 | -0.0274 | tie | undecided | k-NN wins |  | 0.0179 | 0.9217 | 0.9391 |
| 17-32 | 2,293 | 17,194 | 0.8972 | 0.9090 | -0.0118 | -0.0171 | -0.0066 | tie | tie | tie |  | 0.0305 | 0.9521 | 0.9424 |
| 33-64 | 2,204 | 32,059 | 0.9207 | 0.9276 | -0.0069 | -0.0103 | -0.0035 | tie | tie | tie |  | 0.0222 | 0.9631 | 0.9560 |
| 65-128 | 1,652 | 45,924 | 0.9394 | 0.9393 | 0.0001 | -0.0027 | 0.0031 | tie | tie | tie |  | 0.0188 | 0.9786 | 0.9599 |
| 129+ | 1,157 | 85,159 | 0.7069 | 0.7014 | 0.0056 | 0.0036 | 0.0076 | tie | tie | tie |  | 0.0207 | 0.9827 | 0.7194 |

Table: reports/tables/phase2_7b_blocksize_pooled.csv

**Read the first two rows before anything else in this pass.** Block size is the only design-time signal examined anywhere in this project that produces a **decided pooled band verdict at the primary margin**. 2 of the seven bands are decided at delta = 0.05: 3-4 at -0.1145 [-0.1286, -0.1007], `k-NN wins`, 5-8 at -0.0712 [-0.0807, -0.0614], `k-NN wins`. Neither ADS nor SV has a single decided marginal band at delta = 0.05, which is the fact that carried H2 and H3 to Inconclusive. Section 2d below establishes what this does and does not mean, and it is not what it looks like on this table alone.

### Per-block winner distribution by block-size band, full primary population

| population | band | blocks | mean_block_size | mean_n_test | rule wins | k-NN wins | tie | undecided | decided | decided_rate | rule_share_of_decided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full primary population | 3-4 | 2,227 | 3.4122 | 1.4122 | 20 | 215 | 1,845 | 147 | 235 | 0.1055 | 0.0851 |
| full primary population | 5-8 | 2,188 | 6.3048 | 2.4328 | 4 | 48 | 1,768 | 368 | 52 | 0.0238 | 0.0769 |
| full primary population | 9-16 | 2,181 | 12.0587 | 3.9775 | 26 | 13 | 1,656 | 486 | 39 | 0.0179 | 0.6667 |
| full primary population | 17-32 | 2,293 | 23.4025 | 7.4985 | 48 | 22 | 1,636 | 587 | 70 | 0.0305 | 0.6857 |
| full primary population | 33-64 | 2,204 | 46.9868 | 14.5458 | 38 | 11 | 1,422 | 733 | 49 | 0.0222 | 0.7755 |
| full primary population | 65-128 | 1,652 | 91.0763 | 27.7990 | 31 | 0 | 1,045 | 576 | 31 | 0.0188 | 1.0000 |
| full primary population | 129+ | 1,157 | 243.7589 | 73.6033 | 24 | 0 | 800 | 333 | 24 | 0.0207 | 1.0000 |

### Per-block winner distribution by block-size band, n_test >= 3 subset

| population | band | blocks | mean_block_size | mean_n_test | rule wins | k-NN wins | tie | undecided | decided | decided_rate | rule_share_of_decided |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| n_test >= 3 subset | 5-8 | 947 | 7.4498 | 3.0000 | 0 | 9 | 744 | 194 | 9 | 0.0095 | 0.0000 |
| n_test >= 3 subset | 9-16 | 2,181 | 12.0587 | 3.9775 | 26 | 13 | 1,656 | 486 | 39 | 0.0179 | 0.6667 |
| n_test >= 3 subset | 17-32 | 2,293 | 23.4025 | 7.4985 | 48 | 22 | 1,636 | 587 | 70 | 0.0305 | 0.6857 |
| n_test >= 3 subset | 33-64 | 2,204 | 46.9868 | 14.5458 | 38 | 11 | 1,422 | 733 | 49 | 0.0222 | 0.7755 |
| n_test >= 3 subset | 65-128 | 1,652 | 91.0763 | 27.7990 | 31 | 0 | 1,045 | 576 | 31 | 0.0188 | 1.0000 |
| n_test >= 3 subset | 129+ | 1,157 | 243.7589 | 73.6033 | 24 | 0 | 800 | 333 | 24 | 0.0207 | 1.0000 |

Table: reports/tables/phase2_7b_blocksize_verdicts.csv

### Winner by block size: rule wins against k-NN wins

| population | band | blocks | rule wins | k-NN wins | decided | rule_share_of_decided |
| --- | --- | --- | --- | --- | --- | --- |
| full primary population | 3-4 | 2,227 | 20 | 215 | 235 | 0.0851 |
| full primary population | 5-8 | 2,188 | 4 | 48 | 52 | 0.0769 |
| full primary population | 9-16 | 2,181 | 26 | 13 | 39 | 0.6667 |
| full primary population | 17-32 | 2,293 | 48 | 22 | 70 | 0.6857 |
| full primary population | 33-64 | 2,204 | 38 | 11 | 49 | 0.7755 |
| full primary population | 65-128 | 1,652 | 31 | 0 | 31 | 1.0000 |
| full primary population | 129+ | 1,157 | 24 | 0 | 24 | 1.0000 |
| n_test >= 3 subset | 5-8 | 947 | 0 | 9 | 9 | 0.0000 |
| n_test >= 3 subset | 9-16 | 2,181 | 26 | 13 | 39 | 0.6667 |
| n_test >= 3 subset | 17-32 | 2,293 | 48 | 22 | 70 | 0.6857 |
| n_test >= 3 subset | 33-64 | 2,204 | 38 | 11 | 49 | 0.7755 |
| n_test >= 3 subset | 65-128 | 1,652 | 31 | 0 | 31 | 1.0000 |
| n_test >= 3 subset | 129+ | 1,157 | 24 | 0 | 24 | 1.0000 |

Figure: `reports/figs/phase2_7b_verdicts_by_blocksize.png`

### 2c. Block size at fixed ADS

The manuscript never shows one axis without holding the other, because the axes correlate. Block size correlates with both: Spearman -0.2515 with ADS and +0.3976 with SV over the primary population. The table above therefore has to be read at fixed ADS before it can be read as a statement about block size. The stratification below is the coarse one the report already uses for the structural top row, ADS = 1.0 against everything below it. It is a supplementary stratification and not a frozen band.

| ads_split | bsize_band | n_blocks | n_test | pooled_gap | ci_lo | ci_hi | verdict_0.05 | verdict_0.02 | under_powered | rule_cov |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADS < 1.0 | 3-4 | 223 | 320 | 0.0594 | 0.0064 | 0.1115 | undecided | undecided |  | 0.7719 |
| ADS < 1.0 | 5-8 | 320 | 784 | 0.0370 | 0.0077 | 0.0666 | undecided | undecided |  | 0.8278 |
| ADS < 1.0 | 9-16 | 442 | 1,780 | 0.0854 | 0.0634 | 0.1101 | rule wins | rule wins |  | 0.8921 |
| ADS < 1.0 | 17-32 | 572 | 4,324 | 0.0759 | 0.0608 | 0.0905 | rule wins | rule wins |  | 0.9348 |
| ADS < 1.0 | 33-64 | 639 | 9,267 | 0.0428 | 0.0335 | 0.0511 | undecided | rule wins |  | 0.9406 |
| ADS < 1.0 | 65-128 | 519 | 14,375 | 0.0302 | 0.0229 | 0.0382 | tie | rule wins |  | 0.9625 |
| ADS < 1.0 | 129+ | 650 | 57,739 | 0.0118 | 0.0091 | 0.0146 | tie | tie |  | 0.9782 |
| ADS = 1.0 | 3-4 | 2,004 | 2,825 | -0.1342 | -0.1482 | -0.1208 | k-NN wins | k-NN wins |  | 0.8503 |
| ADS = 1.0 | 5-8 | 1,868 | 4,539 | -0.0899 | -0.0995 | -0.0802 | k-NN wins | k-NN wins |  | 0.9039 |
| ADS = 1.0 | 9-16 | 1,739 | 6,895 | -0.0661 | -0.0731 | -0.0597 | k-NN wins | k-NN wins |  | 0.9294 |
| ADS = 1.0 | 17-32 | 1,721 | 12,870 | -0.0413 | -0.0455 | -0.0373 | tie | k-NN wins |  | 0.9579 |
| ADS = 1.0 | 33-64 | 1,565 | 22,792 | -0.0271 | -0.0296 | -0.0246 | tie | k-NN wins |  | 0.9722 |
| ADS = 1.0 | 65-128 | 1,133 | 31,549 | -0.0136 | -0.0151 | -0.0121 | tie | tie |  | 0.9860 |
| ADS = 1.0 | 129+ | 507 | 27,420 | -0.0076 | -0.0089 | -0.0064 | tie | tie |  | 0.9922 |

Table: reports/tables/phase2_7b_blocksize_by_ads.csv

**The sign change across block-size bands does not survive conditioning on ADS.** Inside ADS = 1.0 the pooled gap is negative in every band and runs 3-4=-0.1342 / 5-8=-0.0899 / 9-16=-0.0661 / 17-32=-0.0413 / 33-64=-0.0271 / 65-128=-0.0136 / 129+=-0.0076, shrinking monotonically toward zero. Inside ADS < 1.0 it is positive in every band and runs 3-4=+0.0594 / 5-8=+0.0370 / 9-16=+0.0854 / 17-32=+0.0759 / 33-64=+0.0428 / 65-128=+0.0302 / 129+=+0.0118, shrinking toward zero but not monotonically, the 9-16 band being the one out of order. Neither stratum changes sign anywhere. What changes across the marginal block-size bands is the **mix**: 90.0% of blocks in the smallest band are ADS = 1.0 against 43.8% in the largest. The marginal reversal is composition, not a winner reversal.

**Block size still decides bands inside a stratum, and it decides them the same way throughout the stratum.** Inside ADS = 1.0 the bands 3-4, 5-8, 9-16 are decided `k-NN wins` at delta = 0.05 and the rest are ties. Inside ADS < 1.0 the bands 9-16, 17-32 are decided `rule wins` and the rest are ties or undecided. That is a tie-crossing in each stratum, in the frozen vocabulary of `PREREG.md` section 9, and a winner reversal in neither.

### 2d. Reconciling the pooled headline with the per-block picture

Pooled over signatures the k-nearest vote is ahead by 0.0050. Per block the rule takes 191 wins against the vote's 309. Both are true and block size is what separates them.

- **The vote's per-block wins live in small blocks.** The two smallest bands (3-4, 5-8) hold 263 of the vote's 309 per-block wins (85.1%) and 24 of the rule's 191 (12.6%). Above 64 signatures the vote wins no block at all.
- **The signatures live in large blocks.** The two largest bands (65-128, 129+) are 2,809 of 13,902 blocks (20.2%) but 131,083 of 197,479 test signatures (66.4%). A one-block-one-vote tally and a one-signature-one-vote pool are therefore counting almost disjoint majorities.
- **The pooled gap is not carried by the bands that hold the signatures.** Summed over bands, the 5 bands with a negative gap contribute a net of -1,466 signatures' worth of rule deficit on 66,396 test signatures, and the 2 bands with a non-negative gap contribute +479 on 131,083. The total is -987 over 197,479, which is the pooled -0.0050. Two thirds of the signatures sit in bands whose own gap rounds to zero or favours the rule; the headline is negative because of the third that does not.

### 2e. Does block size predict the winner, and in which direction?

**Yes on the per-block winner, in the direction of the rule.** Across the seven bands the rule's share of decided per-block verdicts runs 3-4=0.0851 / 5-8=0.0769 / 9-16=0.6667 / 17-32=0.6857 / 33-64=0.7755 / 65-128=1.0000 / 129+=1.0000: it jumps between the 5-8 and 9-16 bands rather than climbing smoothly, and above 64 signatures it is 1.0 because the vote wins nothing there. The pooled gap, unlike that share, is monotone in band order, rank correlation +1.0000 over seven points. Read on its own this is the strongest design-time structure anywhere in the project.

**Yes on a pooled verdict too, which neither pre-registered signal managed.** At delta = 0.05 the bands 3-4, 5-8 are decided `k-NN wins`. The largest band gap is -0.1145, more than twice the primary margin. **This is the one place in the re-analysis where a design-time signal clears the bar the pre-registered signals could not, and the prose pass has to say so.**

**And it is not the finding it appears to be, for two measured reasons.**

1. **Conditioning on ADS removes the reversal.** Section 2c: inside ADS = 1.0 every band favours the vote, inside ADS < 1.0 every band favours the rule, and the marginal sign change across bands is the changing mix of the two. At fixed ADS block size still decides bands, but it decides every one of them the same way, so it is a **gap-compression** signal, the shape Amendment 1 pre-registered for ADS itself, and not a winner-direction signal. Which mechanism to build is still set by ADS; block size only says how much the choice is worth.
2. **The decided small-block cells are an abstention effect, not a resolution effect.** The rule's coverage climbs monotonically with block size, 3-4=0.8423 / 5-8=0.8927 / 9-16=0.9217 / 17-32=0.9521 / 33-64=0.9631 / 65-128=0.9786 / 129+=0.9827, and it is the abstentions, scored as errors, that produce the deficit. The rule's precision where it fires **exceeds the vote's accuracy in all seven bands**, including both decided ones: 0.9370 against 0.9037 in the smallest. A designer told "use the vote on small blocks" is being told to prefer the mechanism that is less often right when it commits, because the other one declines to commit on a sixth of the items.

**The scoped statement the evidence supports.** Block size predicts which mechanism has the higher whole-set accuracy on small blocks, at the primary margin, and that mechanism is the one that never abstains. It does not predict which mechanism resolves a name better, and at fixed ADS it never points to a different winner than ADS already points to. Whether an abstention-driven, composition-dependent effect counts as a design-time signal a practitioner can act on is a claim the manuscript now has to make explicitly rather than leave to the reader. It is the one place where "no design-time signal is actionable", stated without qualification, is too strong.

The same tables on the n_test >= 3 subset are printed above. The pattern is unchanged: the 3-4 band disappears with the restriction, because those blocks hold one or two test signatures by construction, and the 5-8 band stays decided `k-NN wins` at -0.0648.

## 3. Uncertainty for the driver comparison (Major 3)

Addendum 1a's primary measure is an unweighted one-way variance decomposition of the decided-winner rate over the eligible cells of the frozen 5 x 4 grid. 2.2e reported it as two point statistics with no interval. This section bootstraps the difference **eta2_SV - eta2_ADS** by resampling blocks with replacement, B = 2,000, at the frozen seed scheme of `phase2b_core.band_seed`. The per-block verdicts are the frozen ones; what is resampled is which blocks enter the grid, which is the sampling model `PREREG.md` section 8 already uses for every pooled band.

**This adds an interval to a pre-registered statistic. It does not change the statistic, the clause, or the verdict Addendum 1a returned.**

### 3a. Bootstrap interval on eta2_SV - eta2_ADS

| k | delta | eta2_ADS | eta2_SV | diff | diff_lo | diff_hi | share_SV_larger | draws_with_an_ineligible_cell |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 0.0500 | 0.1749 | 0.3837 | 0.2088 | 0.0628 | 0.3473 | 0.9985 | 30 |
| 2 | 0.0500 | 0.3277 | 0.3751 | 0.0474 | -0.2531 | 0.3159 | 0.5700 | 30 |

Table: reports/tables/phase2_7b_driver_bootstrap.csv

At k = 5 the difference is **+0.2088, 95% interval [+0.0628, +0.3473]**, and SV is the larger of the two in 99.9% of the 2,000 usable draws. The interval excludes zero, so the direction Addendum 1a's clause turned on survives being given an error bar. Its width, 0.2846, is about 136% of the point estimate, which is the honest way to state how sharp the measurement is.

### 3b. Size-adjusted variant (labelled diagnostic, decides nothing)

The cells are not balanced on test-set size and decidability rises with test-set size, so part of what eta-squared attributes to SV could be attributable to how large the blocks in each SV band are. The diagnostic below partials log cell-mean test-set size out of the cell decided rates by ordinary least squares across the eligible cells, then runs the same decomposition on the residuals. It is **not** pre-registered, it is not a variant Addendum 1a admits, and it decides nothing.

| k | delta | adj_eta2_ADS | adj_eta2_SV | adj_diff | adj_diff_lo | adj_diff_hi | adj_share_SV_larger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 0.0500 | 0.1824 | 0.3664 | 0.1840 | 0.0299 | 0.3277 | 0.9950 |
| 2 | 0.0500 | 0.2119 | 0.4844 | 0.2725 | 0.0093 | 0.4691 | 0.9775 |

After the adjustment the k = 5 pair is eta2_ADS = 0.1824 against eta2_SV = 0.3664, difference +0.1840 with 95% interval [+0.0299, +0.3277]. SV stays the larger driver. The confound the reviewer named is therefore present but not load bearing: adjusting for it moves the difference from +0.2088 to +0.1840 and does not cross zero.

### 3c. The pair at k = 2 beside k = 5, so "stable across k" can be stated accurately

At k = 2 the pair is eta2_ADS = 0.3277 against eta2_SV = 0.3751, difference **+0.0474, 95% interval [-0.2531, +0.3159]**, against +0.2088 [+0.0628, +0.3473] at k = 5.

**The k = 2 interval straddles zero**, and SV is the larger of the two in only 57.0% of draws there against 99.9% at k = 5. The k = 2 point difference is 23% of the k = 5 one. So the accurate statement is narrower than "stable across k":

- **The point estimate points the same way at every k on the curve**, which is what the k-curve table reports and what makes the clause outcome stable.
- **The evidence for the direction is not the same at every k.** At k = 5 it is decisive by this interval; at k = 2 it is not distinguishable from zero. That is consistent with, and is the quantitative content of, Addendum 1a's own clause coming out `split` at k = 2 and `failed` at k = 3, 5 and 10.
- **The manuscript's "stable across k" should therefore be scoped to the verdict, not the magnitude, and k = 2 should be named as the weak end.** Section 5.6's phrase "the sharpest single measurement in the run" is defensible at k = 5 with the interval above and is not defensible as a statement about the whole curve.

The size-adjusted diagnostic moves k = 2 the other way, to +0.2725 [+0.0093, +0.4691], which excludes zero. Two diagnostics disagreeing at k = 2 is itself the honest summary: k = 2 is the unstable end of the curve and nothing should be rested on it.

Figure: `reports/figs/phase2_7b_driver_bootstrap.png`

**Nothing here changes an H2 conclusion.** H2 was carried to Inconclusive by the power floor, which is evaluated before the driver clause. At the primary k = 5 the clause was `failed` and stays `failed`, and it now has an interval saying the failure was not a coin flip. At k = 2, where the clause was already reported as `split`, the interval says the evidence there is close to a coin flip, which is a sharper statement of the same thing rather than a new outcome.

## 4. Accuracy accounting (Major 8)

### 4a. The out-of-history share, an accuracy ceiling for both mechanisms

Both mechanisms assign an author drawn from the block's own training half. Neither can assign an author it has never seen. A test signature whose true author does not occur in the training half is therefore an **automatic error for both arms**, and 1 minus the share of such signatures is a hard accuracy ceiling for the whole comparison.

This quantity is in no committed table, so it is derived here from the frozen split and the labels, which is all it needs: a block's training half is `is_train` under `phase2b_core.assign_splits` at seed 20260918, and a test signature is out of history when its `author_label` is not among that half's labels. No mechanism is re-run and no split is redrawn. The derivation is checked rather than asserted: the code verifies that **no** out-of-history signature is scored correct by either arm in the committed per-signature scores.

Check passed: 8,168 out-of-history test signatures in the primary population, and the committed scores mark every one of them wrong for the rule and wrong for the k-nearest vote.

| population | blocks | test signatures | out_of_history | out_of_history_share | accuracy_ceiling | rule_acc | knn_acc | rule_acc_over_ceiling | knn_acc_over_ceiling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 13,902 | 197,479 | 8,168 | 0.0414 | 0.9586 | 0.8244 | 0.8294 | 0.8600 | 0.8652 |
| aminer | 842 | 40,006 | 6,259 | 0.1565 | 0.8435 | 0.4076 | 0.4038 | 0.4832 | 0.4787 |
| arnetminer | 82 | 1,620 | 245 | 0.1512 | 0.8488 | 0.5093 | 0.5099 | 0.6000 | 0.6007 |
| inspire | 11,110 | 139,369 | 498 | 0.0036 | 0.9964 | 0.9482 | 0.9645 | 0.9516 | 0.9680 |
| kisti | 711 | 10,147 | 965 | 0.0951 | 0.9049 | 0.8466 | 0.7334 | 0.9355 | 0.8105 |
| pubmed | 34 | 803 | 9 | 0.0112 | 0.9888 | 0.8020 | 0.5554 | 0.8111 | 0.5617 |
| qian | 276 | 1,696 | 82 | 0.0483 | 0.9517 | 0.6079 | 0.5896 | 0.6388 | 0.6196 |
| zbmath | 847 | 3,838 | 110 | 0.0287 | 0.9713 | 0.8494 | 0.9125 | 0.8745 | 0.9394 |
| inspire alone | 11,110 | 139,369 | 498 | 0.0036 | 0.9964 | 0.9482 | 0.9645 | 0.9516 | 0.9680 |
| pooled non-inspire | 2,792 | 58,110 | 7,670 | 0.1320 | 0.8680 | 0.5276 | 0.5054 | 0.6078 | 0.5823 |

Table: reports/tables/phase2_7b_accuracy_accounting.csv

Pooled, **4.14% of held-out signatures name an author the block's training half never shows**, so no mechanism in this family can exceed 0.9586 on this population. Against that ceiling the rule reaches 0.8600 and the vote 0.8652. The pooled gap between the mechanisms, -0.0050, is unchanged in kind by the ceiling: it is a shared floor, subtracted from both arms, so it moves each accuracy and barely moves their difference.

**The ceiling is real and it is not the main reason the datasets differ, which is worth stating because the obvious guess is that it is.** Ordered by out-of-history share: aminer=0.1565 / arnetminer=0.1512 / kisti=0.0951 / qian=0.0483 / zbmath=0.0287 / pubmed=0.0112 / inspire=0.0036. aminer's ceiling is 0.8435 against inspire's 0.9964, a difference of 0.1529, while their rule accuracies differ by 0.5406. Normalized to their own ceilings the two still sit 0.4684 apart, so the ceiling accounts for only about 13% of the spread between them. The rest is the blocks themselves being harder, not more of them being impossible. A reader who is handed the ceiling column and no caveat will draw the opposite conclusion, so the caveat belongs beside the column.

### 4b. The rule's conditional precision, its accuracy where it fires

The manuscript scores an abstention as an error, which is the right primary metric for a comparison of deployable mechanisms, and it is not the number a precision-first framing invites. Below, `rule_conditional_precision` is the rule's accuracy restricted to the signatures on which it fires, `rule_correct / rule_fires`. Both are computed from the same committed per-block records; neither replaces the other.

| population | test signatures | rule_fires | rule_coverage | rule_acc | rule_conditional_precision | knn_acc |
| --- | --- | --- | --- | --- | --- | --- |
| all (primary population) | 197,479 | 191,270 | 0.9686 | 0.8244 | 0.8512 | 0.8294 |
| aminer | 40,006 | 39,205 | 0.9800 | 0.4076 | 0.4159 | 0.4038 |
| arnetminer | 1,620 | 1,587 | 0.9796 | 0.5093 | 0.5198 | 0.5099 |
| inspire | 139,369 | 135,252 | 0.9705 | 0.9482 | 0.9771 | 0.9645 |
| kisti | 10,147 | 9,353 | 0.9218 | 0.8466 | 0.9184 | 0.7334 |
| pubmed | 803 | 762 | 0.9489 | 0.8020 | 0.8451 | 0.5554 |
| qian | 1,696 | 1,675 | 0.9876 | 0.6079 | 0.6155 | 0.5896 |
| zbmath | 3,838 | 3,436 | 0.8953 | 0.8494 | 0.9488 | 0.9125 |
| inspire alone | 139,369 | 135,252 | 0.9705 | 0.9482 | 0.9771 | 0.9645 |
| pooled non-inspire | 58,110 | 56,018 | 0.9640 | 0.5276 | 0.5473 | 0.5054 |

Pooled, the rule fires on 96.86% of held-out signatures and is right on **0.8512** of those, against the vote's 0.8294 over everything. The precision-first characterization is therefore accurate: where the rule commits, it is the more accurate arm by +0.0218, and it pays for that with 3.14% abstention. This is the cleanest one-line statement of what the two mechanisms actually trade, and it belongs beside the pooled accuracy rather than instead of it.

**Nothing here changes an H1, H2 or H3 conclusion.** The ceiling and the conditional precision are accounting that was missing, not a re-scoring. Every verdict in the frozen falsification table is computed from the same per-signature correctness the manuscript already used.

## What 2.7c has to carry, in priority order

1. **The scoping decision on the general claim, which is the author's.** Block size is a design-time signal with two decided pooled bands at the primary margin (section 2). The abstract, the title and section 8.1 currently generalize past what that allows. Either scope every general sentence to the two pre-registered signals, or state the block-size result and its two qualifications in the main text and let the general sentence stand with them attached. This is the same decision peer-review major 4 asks for, and taking it first is what 2.7's own handover recommended.
2. **Section 5.4 and Figure 2 need the size-1 and size-2 rows and the degeneracy note** (section 1a), because 278 of the 500 decided verdicts come from blocks whose interval cannot produce an undecided.
3. **The gradient paragraph needs its sensitivity result** (section 1d). The reported rise at ADS = 1.0 is a small-block artifact and the restricted gradient is monotone. Reporting that makes the H2 discussion stronger, not weaker.
4. **Table 4 needs the bootstrap interval, and section 5.6's "stable across k" needs scoping to the verdict** (section 3).
5. **Table 3 or the population table needs the ceiling column, section 5.3 needs the rule's conditional precision** (section 4), with the caveat that the ceiling is not what separates the datasets.

None of the five changes a verdict. The first changes a claim.

## Reproducing this report

`python phase2/phase2_7b_reanalysis.py`. It runs its own assert-based self-check first, then re-derives the frozen per-block verdict counts (191 / 309 / 10,172 / 3,230) and refuses to continue if they do not match, then writes this file and the `reports/tables/phase2_7b_*.csv` tables and the two figures. Two consecutive runs produce a byte-identical report.
