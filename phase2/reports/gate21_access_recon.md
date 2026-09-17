# Phase 2.1 step 0: S2AND access, license, and not-scooped recon

Gate: stop and report if access, license, feasibility, or novelty fails.
**Verdict: all four pass. One substantive literature flag, recorded below, that
bears on hypothesis H2 and must be read before Phase 2.2 freezes its hypotheses.**

## Access

| question | answer |
| --- | --- |
| Is it first-party? | Yes. Allen Institute for AI's own public research bucket, `s3://ai2-s2-research-public/s2and-release`, which is the download location documented in the `allenai/S2AND` README under "Download Data or Model". Not a third-party mirror, not HuggingFace, not Zenodo. |
| Offline? | Yes. Plain unauthenticated HTTPS against the S3 REST endpoint `https://ai2-s2-research-public.s3.amazonaws.com/`. No AWS credentials, no AWS CLI, no API key, no paid call. The README's own command is `aws s3 sync --no-sign-request`, that is, explicitly credential-free. |
| Complete? | Yes. All eight constituent datasets are present as their own prefixes: `aminer`, `arnetminer`, `inspire`, `kisti`, `medline`, `pubmed`, `qian`, `zbmath`. |
| Host reachable? | Yes, on every request made during this pass. |

Note on which release. The repo's current README steers new users to an Arrow
release, `s3://ai2-s2-research-public/s2and-release-arrow`, about 10.1 GiB, and
its smoke-eval example names only `pubmed qian zbmath`. The **paper-era JSON
release** the README keeps published, `s2and-release`, is the one that carries
all eight datasets in the format the S2AND paper describes, and is what we use.
The README says it "is still available ... but it is only needed for paper-era
`ANDData` workflows", which is exactly our workflow.

What we pulled, and what we skipped:

- Pulled: `*_signatures.json` and `*_clusters.json` for all eight, plus
  `LICENSE.txt`, medline's `train_pairs.csv` / `test_pairs.csv`, and
  `zbmath_papers.json`. 260 MB, 19 files, every byte sha256'd.
- Skipped: `*_papers.json` (~3.4 GiB) and `*_specter.pickle` (~3.0 GiB). Not
  needed for the two-axis check. The first 200 KB of each papers file was
  range-read instead, enough to confirm the schema.
- One 404, expected and reported rather than hidden:
  `medline/medline_clusters.json` does not exist. Medline ships as labelled
  *pairs*, not clusters, so it carries no author labels and is excluded.

Provenance and checksums: `phase2/data/MANIFEST_s2and.json`. Re-runnable with
`python phase2/fetch_s2and.py`, which skips files already on disk and re-hashes
them either way.

## License

- **Data: ODC-BY.** Stated in the README ("The released dataset is under
  ODC-BY") and shipped inside the release prefix itself as
  `s2and-release/LICENSE.txt`, which we downloaded and checksummed. ODC-BY
  grants the right to use, modify, and share the database and to produce and
  share derivative databases, subject to attribution.
- **Code: CC-BY-4.0** in the repo's root `LICENSE`; package metadata declares
  MIT. We use no S2AND code in the pipeline. Two S2AND functions are
  *reimplemented* in `phase2/s2and_blocking.py` for the cross-check, and both
  are attributed in place.
- **Committing a processed subset: permitted.** A derived table is a derivative
  database under ODC-BY section 4.4; the obligation is attribution and a notice
  of the license, which the manifest, this report, and the paper's citation all
  carry.
- **One caveat, stated because the README states it:** "Some affiliation data
  comes directly from the Microsoft Academic Graph." Affiliation strings are
  carried in our table as a context field. If MAG's own terms matter for
  redistribution, the affordable answer is to drop the `affiliation` column
  before any public release; it is not load-bearing for either axis. Flagged for
  the 2.6 pre-submission gate, not acted on now.

## Feasibility

Confirmed by doing it, not by reading about it: 766,133 signatures ingested,
26,939 blocks, 59,119 distinct authors, offline, CPU-only, deterministic. See
`gate21_data_shape.md`.

## Not-scooped check (scoped, not a full related-work pass)

A handful of targeted searches for the exact claim: a design-time consistency or
homonymity signal that predicts author-disambiguation accuracy but not which
matching mechanism to select. Nothing found that makes that claim. Two things
are close enough to record now.

### The real flag: Kim and Kim 2020

*Effect of forename string on author name disambiguation.* Jinseok Kim and Jenna
Kim, JASIST 71(7), 839-855. arXiv:2102.03250.

They vary the ratio and length of full forenames across labelled AND datasets and
measure heuristic string matching against feature-based machine learning. From
the abstract, verbatim:

> "Performance gains by algorithmic disambiguation are pronounced when many
> forenames are initialized or homonym is prevalent. As the ratios of full
> forenames increase, however, they become marginal compared to the performances
> by string matching."

This is a *gap between two mechanisms* that moves with both a surface-form
quantity (forename initialization) and a consistency quantity (homonymity). It
is the nearest prior work to our H2 and H3 and it is not currently in our
related-work list. It must be.

Why it does not scoop the claim:

- Their surface axis is a **manipulation**, not a measurement: they synthetically
  initialize forenames at set ratios. Ours is measured per block and never set.
- Their unit is the **dataset**; ours is the block. They report no per-block
  signal and no design-time signal.
- They report **no winner flip**. A follow-up summary of the same work puts it as
  string matching producing "decent performances although they cannot defeat
  feature-based machine learning". One mechanism always wins, so there is no
  selection problem to have.
- They build **no selector** and frame nothing as algorithm selection.

Why it is nonetheless a live risk to H2, and should be treated as one: their
result says the mechanism gap widens "when ... homonym is prevalent". H2 says a
consistency signal does *not* predict which mechanism wins. Those are not
formally contradictory, since a gap in magnitude is not a flip in sign, and their
homonymity is dataset-level while ours is per block. But if H2 fails in Phase
2.2, this paper predicted it, and the honest move is to have said so beforehand.
Read it in full before the 2.2 hypotheses are frozen.

### The weaker neighbour

Work that bounds AND accuracy by the combined ratio of ambiguous pairs, homonyms
plus synonyms, is adjacent. It sets a ceiling on achievable accuracy. It says
nothing about which of two mechanisms to pick, which is the whole content of the
claim here.

### What was searched

Block homonymity as a predictor of AND accuracy versus method choice; algorithm
selection and meta-learning for entity resolution per block; exact versus fuzzy
matching governed by surface variability rather than label ambiguity; cluster and
block purity predicting accuracy but not the winner; per-instance algorithm
selection in AND; and S2AND's own homonymity and synonymity facets against
disambiguation performance. This is a quick check, deliberately not the full
related-work pass, which belongs to the writing phase.

## What this pass did not do

No mechanism, no accuracy, no similarity cutoff, no winner definition, no
selector. None of those exists anywhere in `phase2/` after this pass.
