# Phase 2.2b calibration, frozen

Produced by `phase2/phase2b_build.py`. Everything on this page comes from the **calibration split only**: a random 15% of live blocks drawn at block level with seed 20260918, disjoint from every block that produces a reported result. PREREG sections 6 and 7 allow exactly these two calibrations and no others. The values are written to `phase2/phase2b_constants.py` and committed before any evaluation-split run.

## Split

| quantity | value |
| --- | ---: |
| live blocks | 18,984 |
| calibration blocks | 2,848 |
| evaluation blocks | 16,136 |
| calibration share | 15.0021% |
| calibration signatures (train + test) | 116,308 |
| calibration test signatures | 36,130 |

## SV and SV_resid band edges (PREREG section 6)

Band 0 is SV exactly 0 and is structural, never merged into a quantile. Bands 1 to 3 are the terciles of the **strictly positive** values, cut at the 33.33rd and 66.67th percentiles of the calibration blocks.

| signal | calibration blocks with the signal defined | strictly positive | 33.33rd pct | 66.67th pct |
| --- | ---: | ---: | ---: | ---: |
| SV | 2,450 | 1,673 | 0.102644 | 0.195066 |
| SV_resid | 2,450 | 733 | 0.036782 | 0.082418 |

## Fuzzy cutoff (PREREG section 7)

One global cutoff per metric family. Not one per dataset, not one per band. Selection rule, fixed in advance: highest pooled accuracy over all calibration test signatures, ties broken toward the **higher** cutoff because it abstains more.

### levenshtein

| cutoff | pooled fuzzy accuracy | fuzzy coverage |
| ---: | ---: | ---: |
| 0.50 | 0.8441 | 0.9987  **<- chosen** |
| 0.55 | 0.8434 | 0.9974 |
| 0.60 | 0.8425 | 0.9961 |
| 0.65 | 0.8407 | 0.9934 |
| 0.70 | 0.8394 | 0.9908 |
| 0.75 | 0.8378 | 0.9878 |
| 0.80 | 0.8355 | 0.9838 |
| 0.85 | 0.8318 | 0.9785 |
| 0.90 | 0.8291 | 0.9745 |
| 0.95 | 0.8228 | 0.9665 |

**Frozen cutoff for levenshtein: 0.50.** The curve is monotonically decreasing in the cutoff, so the selected value sits on the **lower boundary of the pre-registered grid**. The grid was fixed in advance in PREREG section 7 and is not widened here. What it means substantively is that on this data the fuzzy mechanism is never helped by abstaining: a nearest neighbour, however far, beats no answer at all, because an abstention is scored as wrong. The practical consequence is a fuzzy arm with near-total coverage, which is reported beside every accuracy number.

### jarowinkler

| cutoff | pooled fuzzy accuracy | fuzzy coverage |
| ---: | ---: | ---: |
| 0.50 | 0.8444 | 0.9999  **<- chosen** |
| 0.55 | 0.8442 | 0.9997 |
| 0.60 | 0.8440 | 0.9993 |
| 0.65 | 0.8440 | 0.9988 |
| 0.70 | 0.8431 | 0.9977 |
| 0.75 | 0.8425 | 0.9968 |
| 0.80 | 0.8408 | 0.9944 |
| 0.85 | 0.8394 | 0.9915 |
| 0.90 | 0.8373 | 0.9869 |
| 0.95 | 0.8323 | 0.9786 |

**Frozen cutoff for jarowinkler: 0.50.** The curve is monotonically decreasing in the cutoff, so the selected value sits on the **lower boundary of the pre-registered grid**. The grid was fixed in advance in PREREG section 7 and is not widened here. What it means substantively is that on this data the fuzzy mechanism is never helped by abstaining: a nearest neighbour, however far, beats no answer at all, because an abstention is scored as wrong. The practical consequence is a fuzzy arm with near-total coverage, which is reported beside every accuracy number.

## What is deliberately absent

No evaluation-split number appears above. No winner, no verdict, no ADS-band or SV-band result, no hypothesis outcome. Those exist only after this file and `phase2b_constants.py` are committed.
