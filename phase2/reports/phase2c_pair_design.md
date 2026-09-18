# Phase 2.2c: a two-sided mechanism pair, design and cheap check

Design-and-propose pass. Produced by `phase2/phase2c_probe.py`, which runs on the
**calibration blocks only**, the 15% of live blocks PREREG section 3 reserves for
choices of exactly this kind. No evaluation-split number was produced, no
hypothesis was evaluated, and `PREREG.md` was not amended. Every count below is a
design diagnostic, not a result, and none of it may be quoted as evidence for a
claim.

Scope of the calibration probe: 2,450 blocks with `n_train >= 2` and
`n_test >= 1`, 35,732 test signatures.

Tables: `reports/tables/phase2c_pair_twosidedness.csv`,
`reports/tables/phase2c_pair_regimes.csv`.

## Why the 2.2b pair failed, stated narrowly

2.2b found zero signatures on which exact match is right and the fuzzy arm is
wrong. The reason is narrower than "the mechanisms are similar", and the narrow
version is what rules out most repairs.

When the test signature's own surface form occurs in the train history, that form
sits at similarity exactly 1.0, which is the maximum of any similarity function.
**Any retriever that selects the single nearest train form therefore selects that
same form and resolves the same author.** Exact match is contained in every 1-NN
retriever, whatever the metric, whatever the cutoff, whatever the tie-break.
Swapping Levenshtein for Jaro-Winkler does not touch it, and 2.2b measured that:
both arms returned zero.

So the repair cannot be a different similarity. Mechanism B has to stop being a
1-NN retriever. There are two ways, and both are in the rules-versus-retrieval
family:

- **aggregate over a neighbourhood** rather than take the single nearest form, so
  that evidence from other forms can outvote the test form's own evidence;
- **match on a representation** under which the test form is no longer privileged,
  so that the retrieved set is a merge of several raw forms.

All three candidates below do one of those. All three are two-sided in the data.

## Mechanism A, shared by all three pairs

**The exact-evidence rule.** Unchanged from PREREG section 4 exact match: if the
test surface form occurs among the train surface forms, assign the most frequent
author carrying that exact form, with the frozen tie-break; otherwise abstain.

It is kept unchanged deliberately. The rule is the precision-first arm: it reads
only evidence that names the test form itself, it never merges across forms, and
it abstains rather than guess. Keeping it identical to 2.2b also means the
mechanism that carried the H1 accuracy finding is the same object in both passes.

## The three candidate pairs

### P1, rule versus radius vote

**B: pool every train signature whose form is within similarity r of the test
form, assign the most frequent author in the pool; abstain if the pool is empty.**

A radius vote is the honest small version of what production disambiguation
actually does. S2AND itself, and the AND literature generally, clusters mentions
by pairwise similarity rather than assigning each mention to its single nearest
neighbour. Merging everything inside a similarity ball is that procedure reduced
to one block and one decision, and its characteristic failure is the
characteristic failure of clustering: it over-merges two people whose names are
close, and then answers with whichever of them has the longer publication record.
The rule cannot make that mistake, because it never looks past the form it
matched. The rule cannot help when the form is absent, because it abstains.

### P2, rule versus normalized-key vote

**B: pool every train signature whose form carries the same ASCII-folded,
lowercased, letters-only key as the test form, assign the most frequent author in
the pool; abstain if the pool is empty.**

The cheapest possible relaxation, and the only candidate with no parameter at
all on either side. Case, diacritics, punctuation, hyphenation and internal
spacing collapse, so "Gell-Mann" and "Gellmann" merge, "Jurgen" and "Jürgen"
merge, and "W Wang" and "W. Wang" merge. Forename fullness deliberately does
**not** collapse: "J. Smith" keys to `jsmith` and "John Smith" to `johnsmith`.
That line is the whole point of the design. Initialization is Kim and Kim's
manipulated variable, so a mechanism that merged across it would encode their
axis into our definitions; what this key does merge is precisely the
non-initialization synonymy their paper names and excludes.

### P3, rule versus k-nearest vote

**B: pool the nearest train signatures by form similarity until at least k are
pooled, whole forms at a time, assign the most frequent author in the pool.**

The same over-merging idea as P1 but on a rank scale instead of an absolute one.
That matters here because every name in a block shares a surname, so raw
similarity has no natural zero and a fixed radius means different things in
different blocks. A rank rule is scale-free: it always consults a handful of
neighbours, however far apart the block's names happen to be. It also never
abstains, which makes the contrast with the rule exactly the precision-versus-
coverage contrast the paper is about, with abstention entirely on the rule's side.

## Two-sidedness on the calibration split

Per test signature, whether each mechanism's prediction equals the truth.
Abstention counts as wrong, as in PREREG section 4. `nn1` is the frozen 2.2b
fuzzy arm, scored as a self-check on the probe rather than as a candidate.

| pair | A right, B wrong | B right, A wrong | both right | both wrong | acc A | acc B | cov B |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| rule vs nn1 (2.2b pair) | **0** | 731 | 29,423 | 5,578 | 0.8234 | 0.8439 | 0.9990 |
| rule vs radius@0.70 | 1,461 | 635 | 27,962 | 5,674 | 0.8234 | 0.8003 | 0.9919 |
| rule vs radius@0.80 | 793 | 503 | 28,630 | 5,806 | 0.8234 | 0.8153 | 0.9852 |
| rule vs radius@0.85 | 456 | 346 | 28,967 | 5,963 | 0.8234 | 0.8204 | 0.9800 |
| rule vs radius@0.90 | 253 | 247 | 29,170 | 6,062 | 0.8234 | 0.8233 | 0.9762 |
| rule vs radius@0.95 | **0** | 16 | 29,423 | 6,293 | 0.8234 | 0.8239 | 0.9686 |
| rule vs mergekey | 158 | 437 | 29,265 | 5,872 | 0.8234 | 0.8312 | 0.9802 |
| rule vs knn@2 | 181 | 736 | 29,242 | 5,573 | 0.8234 | 0.8390 | 1.0000 |
| rule vs knn@3 | 314 | 740 | 29,109 | 5,569 | 0.8234 | 0.8354 | 1.0000 |
| **rule vs knn@5** | **546** | **744** | 28,877 | 5,565 | 0.8234 | 0.8290 | 1.0000 |
| rule vs knn@10 | 912 | 748 | 28,511 | 5,561 | 0.8234 | 0.8188 | 1.0000 |

The probe reproduces the 2.2b nesting exactly where it should: `rule vs nn1` is
zero on the A side. `radius@0.95` is also zero, which is the same degeneracy
reached from the other direction, and is the reason for the warning two sections
below.

**All three candidates are genuinely two-sided.** The weakest A-side count is
P2's 158 and the strongest is P1's 793 at r = 0.80; P3 at k = 5 is the most
balanced at 546 against 744, with the two mechanisms within 0.6 accuracy points
of each other. None of these is the structural zero that killed the 2.2b pair.

## Where each side wins, and the structural constraint the probe found

This is the part that matters more than the choice among the three. Counts of
"rule right, retriever wrong" by ADS band and SV band, for P3 at k = 5. The other
two pairs show the identical pattern of zeros.

| ADS band | SV=0 | SV low | SV mid | SV high |
| --- | ---: | ---: | ---: | ---: |
| [0,0.5) | **0** | 16 | 4 | 334 |
| [0.5,0.7) | **0** | 1 | 25 | 85 |
| [0.7,0.9) | **0** | 5 | 19 | 29 |
| [0.9,1.0) | **0** | 10 | 13 | 5 |
| 1.0 | **0** | **0** | **0** | **0** |

Two whole margins are exactly zero, and both are structurally necessary rather
than empirically small.

- **At SV = 0 the rule can never win.** SV = 0 means the block's train history
  carries one distinct surface form. Every mechanism here pools that one form, so
  all of them return the same author. No amount of redesign changes this.
- **At ADS = 1.0 the rule can never win.** ADS = 1.0 means the train history names
  one author. Any vote over any non-empty pool returns that author, and the rule
  returns the same author whenever it fires, so the rule's only possible
  difference is to abstain, which scores as wrong. This holds for **any** pair of
  mechanisms that assign an author from the block's own history, not just these.

So a contest between a precision-first rule and a coverage-first retriever exists
only where the history is **both** impure and surface-varied. On the calibration
split that region is 41% of test signatures, so it is not a corner case, but it
is gated by both signals at once.

**This contradicts H2 as PREREG section 2 words it.** H2 says train-only ADS does
not predict which mechanism wins. On any pair of this shape ADS does predict part
of it: at ADS = 1.0 the retriever wins or ties by construction. Equally, at fixed
ADS the sign of the gap still flips with SV, in all four ADS bands below 1.0, so ADS alone does not determine the winner either. Neither signal alone
does.

That is a different paper from the one PLAN.md currently describes, and a better
supported one: consistency says **whether the choice matters at all**, surface
stability says **which way to go when it does**, and the selector needs both. It
is also the shape charter invariant 4 already anticipates, since it requires an
ADS-only and an SV-only baseline beside the two-signal selector. But it is a
change to the paper's stated identity and it is review's to make, not this pass's.
Nothing here was measured on the evaluation split, so nothing here settles it;
what the probe establishes is that the old wording cannot survive contact with
any pair built this way, because two of its cells are zero by construction.

## The calibration trap, which the new pre-registration must avoid

Read the accuracy column of the table again. For P3, the retriever's accuracy
falls monotonically as k grows: 0.8390, 0.8354, 0.8290, 0.8188. For P1 it rises
monotonically as r grows, to 0.8239 at r = 0.95. In both families the
accuracy-maximizing parameter is the one closest to the 1-NN limit, and the 1-NN
limit is the degeneracy 2.2b reported.

PREREG section 7 calibrates the fuzzy cutoff by picking the value with the
highest pooled calibration accuracy. **Applied unchanged to either parameterized
pair, that protocol would select k = 2 or r = 0.95 and walk the design straight
back into nesting.** The parameter must be fixed by a definitional argument with
a pre-registered sensitivity curve beside it, not chosen to maximize the
retriever's accuracy. This is not a detail; it is the mechanism by which the same
failure would recur.

## Honest risks

**Closeness to Kim and Kim.** Lower than for the 2.2b pair, and deliberately so.
The two mechanisms differ in matching strategy, single-form evidence against a
pooled neighbourhood, and not at all in how much of the forename they read. Both
read the whole surface form. P2's merge key is built to keep initialization
distinct on purpose. The residual overlap is that SV still correlates with
initialization at Spearman 0.36 (2.2b), which is why the SV_resid control must be
carried over unchanged.

**Drift toward a trained-ML framing.** None of the three trains anything. Each is
a lookup over the block's own train signatures with a fixed decision rule, and
charter invariant 6's two-mechanism core is untouched. P3's k and P1's r are
single scalars fixed before the run, which is strictly less tuning than the 2.2b
pair had once the sensitivity curve is reported. No trained-ML arm is proposed
here and none is needed.

**The retriever may look like a strawman.** A reviewer can say nobody would
deploy a k-nearest vote. The answer is that the over-merging failure is not
invented for the paper: similarity-threshold merging is what clustering-based
disambiguation does, S2AND included, and over-merging is its named failure mode.
The mechanisms are small on purpose, as the 2.2b positioning already concedes in
`kim2020_positioning.md` item 5.

**The contested region is the minority of the corpus.** 41% of calibration test
signatures sit where a contest is possible at all, and within that, ADS = 1.0
blocks are excluded entirely. The per-block bootstrap will have less to work with
than 2.2b did, and 2.2b was already power-limited at delta = 0.05. Whatever pair
is chosen, the new pre-registration should expect to state the analysis
population as the contested region and to reconsider the margin, rather than
rediscovering the power floor after the fact.

**Two zero cells are structural, and the paper must say so before the numbers.**
SV = 0 and ADS = 1.0 cannot produce a rule win. If that is discovered in the
results it reads as a defect; if it is derived in the design section it is a
contribution, because it is the general statement of what went wrong in 2.2b.

**Nothing here is a result.** These are calibration-split diagnostics with no
bootstrap, no margin, and no verdict. The gap signs quoted above are raw means
over cells as small as 116 signatures. They are adequate for choosing a pair and
inadequate for anything else.

## Recommendation

**P3, the exact-evidence rule against a k-nearest vote, with k fixed at 5.**

Three reasons, in order of weight.

1. **It is the most balanced contest.** 546 against 744, with pooled accuracies
   0.8234 and 0.8290. P1 at r = 0.80 is more lopsided in the rule's favour and P2
   is thinner on the rule's side, with 101 of its 158 rule wins inside a single
   cell.
2. **Rank beats radius on this data.** Every name in a block shares a surname, so
   absolute similarity has no meaningful scale and a fixed radius means different
   things in different blocks. P1's behaviour confirms it: the A-side count moves
   from 1,461 to 0 across the radius grid, so the entire finding would be a
   function of r. Across the k grid it moves from 181 to 912, a real dependence
   but a graded one.
3. **The precision-versus-coverage contrast is clean.** The k-nearest vote never
   abstains, so abstention sits entirely on the rule's side and the two arms
   separate exactly along the axis the paper names.

k = 5 is proposed as an a priori choice, the ordinary default for a nearest-
neighbour vote, with the k in {2, 3, 5, 10} curve pre-registered as a mandatory
sensitivity report. It must not be calibrated by accuracy, for the reason in the
trap section above. Only 3.5% of calibration test signatures sit in blocks with
fewer than 5 train signatures, where the vote degenerates to a whole-block
majority, so the choice is not load-bearing on small blocks.

**P2 is the recommended fallback** if review prefers to remove parameters
entirely. It has no parameter on either side, which would also retire the "one
tuned parameter against none" asymmetry PREREG section 7 has to apologize for.
The cost is the thinner rule-side count and a merge behaviour that depends on how
each sub-dataset punctuates names, which is a per-dataset generalization risk P3
does not carry.

## What review has to decide, and what this pass did not do

- Which pair. P3 at k = 5 recommended, P2 as the parameter-free fallback.
- Whether H2 survives in any form, given that two of its cells are zero by
  construction for any pair of this shape. This is the larger of the two
  decisions.
- Whether the analysis population becomes the contested region, and what the
  margin should be in it.

`PREREG.md` was not amended, no evaluation-split number exists for any candidate,
and the 2.2b evidence base is untouched. A new pre-registration is the next
pass's work, not this one's.
