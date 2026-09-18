# Phase 2.2d, pre-registration revision (two-signal reframe)

Apply these edits exactly. They reframe the paper from a one-signal blindness
claim to a two-signal role-separation claim, forced by the 2.2b and 2.2c
findings: any mechanism drawn from this family returns the sole author at ADS =
1.0, so consistency necessarily gates whether the choice is live; and a
single-nearest retriever contains exact match, so the second mechanism must vote
over a neighbourhood. Nothing here is run or measured. After applying, stop for
review of the re-frozen PREREG.md before Phase 2.2e.

The frozen calibration constants (commit 5e13e38: SV band edges, SV_resid band
edges, the delta curve) carry over unchanged. Do not recompute them.

---

## Edit 1. Replace PREREG.md section 2 (the hypotheses) with this

H1, accuracy (validity check, not a contribution).

Across evaluation blocks, train-only ADS is positively associated with each
mechanism's own held-out accuracy, separately for the exact-evidence rule (A) and
the k-nearest-vote retriever (B, k = 5). Stated as a validity check: it confirms
per-block ADS behaves like the established dataset-level homonymity effect
reported by Kim and Kim and in the S2AND paper. Reported as such, not as a
finding.

H2, consistency gates whether the choice is live.

Train-only ADS governs whether the mechanism choice is decidable at all. Holding
SV fixed, the share of blocks with a decided pooled winner (rule wins or k-NN
wins, as opposed to tie or undecided) declines as ADS rises, approaching zero in
the top ADS band, while remaining non-trivially positive in the lower ADS bands.
In words: high consistency means it does not matter which mechanism you use, low
consistency means the choice is live. The decline toward zero at ADS = 1.0 is
partly structural, since a block naming one author returns that author from any
non-empty pool so only abstention can differ, and is reported as such. The
load-bearing empirical content is the gradient across the range and the existence
of a non-trivial decidable region at low ADS. Role-separation check: ADS's
association with decidability is reported alongside SV's, and H2 expects ADS to be
the stronger driver of decidability.

H3, surface stability directs the choice, consistency does not.

Among blocks where the choice is decidable, train-only surface stability governs
which mechanism wins, and consistency does not. Two parts, both required:
- Direction by SV: holding ADS fixed within a band below 1.0, the decided pooled
  winner's identity changes across SV bands, and the change is a genuine reversal
  as defined in section 8 (two SV bands with decided pooled verdicts of opposite
  identity), not only a change in gap magnitude.
- Non-direction by ADS: holding SV fixed, the decided pooled winner's identity
  does not change across ADS bands. This is the original selection-blindness
  claim, now correctly scoped to decidable blocks at fixed surface stability,
  where it can be true.
H3 additionally requires the SV reversal to survive the initialization control of
section 9 (present with SV_resid, not only with raw SV), to hold with the
Jaro-Winkler metric arm, and to generalize beyond inspire.

Contribution. The paper's contribution is the conjunction H2 and H3: two
design-time, label-free signals play separable roles, consistency setting whether
the choice matters and surface stability setting which way to choose, and neither
signal alone predicts the winner. This is distinct from Kim and Kim, who report a
single dataset-level gap magnitude modulated by a manipulated surface variable,
with no decidability axis, no per-block interaction, and no design-time signal.

---

## Edit 2. Amend PREREG.md sections 4 and 7 (mechanism B and its parameter)

Mechanism A (the exact-evidence rule) is unchanged.

Mechanism B is now the k-nearest-vote retriever, replacing the thresholded fuzzy
arm. For a test signature, retrieve the k nearest training forms in the block by
the similarity metric, vote their authors, and break ties toward the nearest
form. For a block with fewer than k training forms, use all available. B does not
abstain when the block has at least one training form, so abstention sits entirely
on the rule's side and coverage is reported.

k is fixed by definition at k = 5. It is not calibrated by maximizing accuracy.
This supersedes section 7's accuracy-maximizing cutoff calibration, which no
longer applies, because B has no similarity cutoff and because accuracy is
monotone toward the k = 2 (single-nearest) limit, which would rebuild the
exact-is-a-subset-of-fuzzy nesting that killed 2.2b. k = 5 was chosen on the
calibration split for contest balance, disclosed as such, and the sensitivity
curve k in {2, 3, 5, 10} is mandatory: every H2 and H3 outcome is recomputed
across it and reported, and an outcome that holds at k = 5 but flips elsewhere on
the curve is reported as k-dependent and treated as Partial.

The margin sensitivity curve (delta in {0.02, 0.03, 0.05}, primary 0.05) and the
four-verdict winner definition (exact wins, k-NN wins, tie, undecided) from
section 8 are unchanged.

---

## Edit 3. Replace PREREG.md section 10 (the falsification table) with this

Inconclusive is evaluated first for every hypothesis. If the Inconclusive power
floor is met, the outcome is Inconclusive regardless of the other rows. An
all-tie or all-undecided set of bands is never read as support for H2 or H3.

H1, accuracy.
- Supported: Spearman of train-only ADS with held-out accuracy is positive with a
  95% block-bootstrap interval excluding 0, for both mechanisms, and generalizes
  (holds pooled non-inspire and in at least 2 qualifying non-inspire datasets).
- Partial: positive and interval-excluding-0 for one mechanism but not both, or
  pooled but not generalizing.
- Not supported: interval includes 0 for both mechanisms, or the correlation is
  negative with an interval excluding 0 for either.
- Inconclusive: fewer than 500 blocks in the primary population, or fewer than 2
  qualifying non-inspire datasets.

H2, consistency gates decidability.
- Supported: holding SV fixed, the decided-winner rate is non-increasing across
  ADS bands in the majority of eligible SV bands and strictly lower in the top
  ADS band than the bottom, at least one low-ADS band has a decided-winner rate
  materially above zero (a real decidable region exists), ADS is the stronger
  driver of decidability than SV, and this holds pooled non-inspire.
- Partial: the gradient holds pooled but not per-dataset, or the decidable region
  exists but the gradient is weak or non-monotone, or SV rivals ADS as a driver
  of decidability.
- Not supported: the decided-winner rate does not decline with ADS (flat or
  rising), or no ADS band has a non-trivial decidable region (the choice is never
  live, as in 2.2b).
- Inconclusive: fewer than 2 ADS bands and 2 SV bands with 30 or more blocks and
  a decided pooled verdict.

H3, surface stability directs the choice.
- Supported: within at least one ADS band below 1.0 with 30 or more blocks per SV
  cell, two SV bands have decided pooled verdicts of opposite identity (a genuine
  reversal); holding SV fixed, winner identity does not reverse across ADS bands
  (or all such verdicts are tie or undecided); the reversal is present with
  SV_resid; it holds with the Jaro-Winkler arm; and it generalizes past inspire.
- Partial: a reversal with raw SV but not SV_resid (the surface axis is forename
  initialization, Kim and Kim's variable); or a tie-crossing rather than a
  reversal; or an SV reversal that holds but ADS also reverses the winner at fixed
  SV (impure role separation); or a reversal that holds pooled but does not
  generalize; or holds with edit distance but not Jaro-Winkler; or margin- or
  k-dependent.
- Not supported: gap compression only. The magnitude of the gap varies with SV
  but no SV band pair is decided in opposite directions in any ADS band, in any
  qualifying analysis. This is an honest, publishable outcome and is reported in
  those words: a per-block, design-time, measured version of Kim and Kim's
  gap-compression finding, obtained with two simple mechanisms, together with the
  methodological point that single-nearest retrieval subsumes exact match. The
  two-signal dissociation claim is dropped and the paper retargets to this result.
- Inconclusive: fewer than 2 SV bands with 30 or more blocks and a decided pooled
  verdict inside any single ADS band.

---

## Edit 4. Identity reframe in the three governing docs

Replace the one-signal framing wherever it appears with the two-signal framing.
The specific lines:

phase2/CLAUDE.md, Mission paragraph. Replace the sentence describing the finding
with: "The scientific core is a two-signal role separation: a design-time
consistency signal (cluster purity, ADS) governs whether the choice of
classification mechanism is live at all, and a design-time surface-stability
signal governs which mechanism to choose when it is. Neither signal alone predicts
the winner. On top of that, a selector that uses both."

phase2/PLAN.md, Paper identity paragraph. Same reframe: consistency sets whether
the mechanism choice matters, surface stability sets which way, neither alone
predicts the winner, sibling in framing to Tan (2026) on the economic axis and to
Kim and Kim (2020) on the surface axis, distinct from both.

phase2/phase2-spec.md, section 1 and the section 3 construct note. State that the
winner is a function of both axes in interaction, not blind to consistency;
consistency gates decidability, surface stability directs the decidable cases.

phase2/PLAN.md, working titles. Replace with:
- Consistency decides whether the matcher matters, surface stability decides
  which one: a two-signal design-time account.
- When does the matcher matter, and which one: a per-block, design-time selector
  for author name disambiguation.
- Two design-time signals, two roles: gating and directing mechanism choice in
  entity resolution.

---

## After applying

Commit on phase-2, append a PASSLOG entry, and update STATE.md and PLAN.md to
reflect the reframe and that 2.2e (the re-run) is next. Then stop for review.
Surface the re-frozen PREREG.md sections 2, 4, 7, and 10 for verification before
2.2e runs.
