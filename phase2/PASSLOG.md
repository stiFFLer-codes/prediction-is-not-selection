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

## Pass 1 — Gate 1: scaffold and WDC ingest

**What and why:** Gate 1 per spec §6.1: get a manageable, public, offline WDC
subset into a clean `(surface_string, key, label)` table. No mechanisms, no
ADS, no selector, no experiments — none were built.

**Subset chosen and why:** the four category-restricted slices (cameras,
computers, shoes, watches) of the **WDC Training Dataset and Gold Standard for
Large-Scale Product Matching, v2.0** (LSPC 2017), splits `train_xlarge`,
`valid_xlarge`, `test`. Chosen over the full 26M/98M-offer dump (unmanageable)
and over the 24-category categorization gold standard (too small, and its
cluster-to-category mapping only feeds the Framing A axis the spec already
expects to be dead). This slice is the one that carries all three properties
spec §2 requires at once: clusters give **repeated keys** (88.7% of clusters
occur 3+ times), cross-vendor titles give **real un-engineered surface noise**
(93.6% of clusters carry more than one distinct surface form), and both a
product-identity key and a WDC category label are present — so it serves
Framing A and Framing B from one table without re-ingesting.

**Provenance (exact):**
- Source: Web Data Commons, Training Dataset and Gold Standard for Large-Scale
  Product Matching, v2.0. Primpeli, Peeters, Bizer, WWW '19 Companion, 381–386.
- Canonical host `https://webdatacommons.org/largescaleproductcorpus/v2/` was
  **down globally** during this pass (`ECONNREFUSED 134.155.98.56:443`,
  reproduced from local curl and from an independent fetcher).
- Obtained instead from the **Web Data Commons group's own HuggingFace org
  account**, `https://huggingface.co/datasets/wdc/products-2017`, pinned to
  immutable revision `bee4f71ca1bcfc51eb8fc41d65720fb6f487df9d`. This is
  first-party WDC distribution, not a third-party mirror and not a synthetic
  stand-in: the repo is owned by the `wdc` org, carries the Primpeli et al.
  citation as its own dataset card, and the records are raw schema.org
  serialisations complete with `"..."@en` language tags and `"Null"` literals —
  artifacts no synthetic generator produces.
- 12 files, sha256 of every downloaded byte recorded in
  `phase2/data/MANIFEST.json`; all 12 verified equal to the LFS oids HuggingFace
  publishes for that revision.
- Genuineness caveat, stated plainly: this is first-party-account distribution
  verified by checksum, but it is **not** a checksum published by
  webdatacommons.org itself (WDC publishes none). Re-verify against the
  canonical host once it is reachable.

**Table produced:** `phase2/data/wdc_lspc2017_offers.csv.gz` (706 KB, committed).
The distributed files are labelled offer *pairs* carrying both full offers, so
`phase2/ingest_wdc.py` explodes both sides and deduplicates on offer id:
438,270 offer sides → **15,179 distinct offers**. Raw downloads (100 MB) are
gitignored and re-fetchable by re-running the script.

**Key numbers** (full report: `phase2/reports/gate1_data_shape.md`):
- 15,179 rows; 2,485 distinct keys (clusters); 14,033 distinct surface strings.
- Key recurrence: 50 keys once (2.0%), 232 twice (9.3%), 2,203 three-plus (88.7%).
- Surface forms per key: min 1, median 5, max 140; 93.6% of keys have >1 form.
- Label cardinality: 15 WDC categories, dominated by Computers_and_Accessories
  (4,518), Jewelry (3,936), Camera_and_Photo (3,394), Shoes (2,760); a 53-row
  `not found` category exists and must be handled at gate 2.

**Invariant checks run:** #7 (offline/reproducible) — public download, no API
key, no paid call, CPU-only, deterministic given the pinned revision;
script self-checks on every run (`offer_id` unique after dedup, no empty
surface strings, recurring keys present) and all three passed. Off-limits
paths (`exp1/`, `manuscript/`, `arxiv_build/`, `arxiv_submission/`, main,
v1.0.0) untouched; all new files are under `phase2/`. Invariants #1–#6 and #8
are not yet applicable — nothing was measured, modelled or claimed.

**Observations for gate 2, not acted on:**
- Titles carry raw serialisation noise (leading spaces, embedded quotes,
  `"..."@en` tags, `"Null"`, retailer boilerplate such as `- Prijzen Tweakers`).
  Deliberately left uncleaned — it is genuine surface variation, and how much
  of it to normalise is a Framing B design decision that belongs to gate 2.
- The corpus is multilingual in practice (NL, FR titles appear) despite the
  `language: en` tag.
- 15,179 offers is modest. If gate 2 finds the ADS histograms too thin, the
  upgrade path is the per-category offers corpus rather than a different
  dataset.

**Recommendation for next pass:** gate 2 (hard gate) — compute and plot ADS
histograms under Framing A (key=cluster, label=category) and Framing B
(key=normalised surface, label=cluster id) on this table, report both, and
stop for review before committing to a framing. Decide the title-normalisation
scheme there, since Framing B's ADS range depends on it directly; consider
reporting Framing B under two or three normalisation strengths so the framing
choice is not confounded with a normalisation choice.

## Pass 2 — Gate 2: ADS-range check (hard gate)

**What and why:** Gate 2 per spec §6.2 and charter invariant 1: measure the ADS
distribution before building anything, and stop. ADS distributions only — no
mechanisms, no accuracy, no thresholds, no selector, no cutoff were computed.
Code: `phase2/gate2_ads_range.py`. Report with all histograms embedded:
`phase2/reports/gate2_ads_range.md`.

**Scope note, as instructed:** ADS is computed over the full ingested subset,
not the train split. This pass asks whether the axis has usable range at all,
which is a corpus property. The charter's design-time, history-only train-split
ADS is a gate 3 concern and is stated as such in the report header.

**Step 1 verdict — Framing A is dead.** Of 2,485 clusters, **0 (0.000%)** carry
more than one distinct category; the distinct-categories-per-cluster
distribution is a single row, 1 category for 100.0% of clusters. This is
structural rather than a sampling artifact: WDC assigns category at the cluster
level and stamps it onto each offer, so `category` is a function of
`cluster_id`. ADS_A is a point mass at 1.0 with zero variance — nothing to
correlate against, and no normalisation or subsetting can change it. Spec §3
predicted exactly this. Framing A is not carried forward.

**Step 2 — Framing A numbers** (reported for completeness, degenerate as
expected). With `not found`: 2,485 keys, spike at ADS=1.0 is 100.000%,
min=median=mean=max=1.000, all four sub-bands empty. Without `not found`: 2,474
keys, identical degenerate result. The `not found` category is 53 offers in 11
clusters; because category is cluster-constant it is a whole-cluster label, so
excluding it drops those clusters wholesale rather than splitting any cluster.
Neither view changes the verdict. Figure: `reports/figs/gate2_ads_a.png` — one
bar at 1.0.

**Step 3 — Framing B, three normalisation strengths** (defined and documented in
the script; `raw` = as distributed, `light` = strip `"@lang` tags / `Null` /
punctuation + lowercase, `aggressive` = light + keep only the first quoted
segment + token sort/dedupe). The `aggressive` rule is data-driven: every title
is a sequence of quoted segments whose first element is the offer title proper
and whose later elements are page-title/retailer boilerplate.

| strength | normkeys | recurring | impure (all) | impure (recurring) | spike@1.0 (recurring) | mean (recurring) |
| --- | --- | --- | --- | --- | --- | --- |
| `raw` | 14,033 | 979 | 0.35% | 5.01% | 95.0% | 0.974 |
| `light` | 13,905 | 1,074 | 0.35% | 4.56% | 95.4% | 0.976 |
| `aggressive` | 9,202 | 2,248 | 2.27% | 9.30% | 90.7% | 0.953 |

Figures: `reports/figs/gate2_ads_b_{raw,light,aggressive}.png`. Full sub-band
tables for both the all-normkeys and recurring-normkeys views are in the report.

**Framing B as literally specified is also effectively dead.** Keying on the
whole normalised title makes the key nearly as unique as the offer. Even at
`aggressive`, only 8,139 of 15,093 offers (53.9%) sit under a normkey that
recurs at all, and among recurring normkeys 90.7% still sit at exactly 1.0.
Worse, the non-spike mass is not spread: it concentrates on a few
small-denominator values (0.5 dominates with 130 keys, then 0.667 with 17),
because a recurring normkey has a median of 2 offers. That is a near-binary
pure/ambiguous flag with a ~9% base rate, not a continuous axis with usable
range. Invariant 1 says do not proceed on a dead axis, and at this key
granularity the axis is dead.

**Step 3b — the axis is dead at this granularity, not in principle (diagnostic,
nothing committed).** Spec §3 defines Framing B's key as "a normalized surface
**or blocking key**", and steps 1–3 only tested the first option. Keying on the
first k tokens of the `aggressive` normkey:

| k | recurring keys | impure | spike@1.0 | mean | mass in (0.5, 1.0) |
| --- | --- | --- | --- | --- | --- |
| 2 | 2,282 | 40.1% | 59.9% | 0.784 | 9.6% |
| 3 | 2,615 | 29.9% | 70.1% | 0.850 | 7.3% |
| 4 | 2,548 | 22.7% | 77.3% | 0.890 | 5.8% |
| 5 | 2,450 | 16.7% | 83.3% | 0.919 | 4.0% |

Figure: `reports/figs/gate2_ads_b_blocking.png`. ADS responds strongly and
monotonically to key granularity; at k=2 the histogram has genuine interior mass
(bars at ~0.15, 0.2, 0.3, 0.33, 0.4, 0.5, 0.6, 0.67, 0.8) alongside the spike.
This is the only view in the pass that looks like a distribution. Flagged
honestly in the report: because `aggressive` token-sorts, "first k tokens" means
the alphabetically-first k, which is deterministic but not a principled blocking
function. It is evidence about granularity, not a proposed key.

**Step 4 — surface noise (light heuristics).** Language read off the `"@lang`
tags the serialisation already carries. 59.4% of titles carry an explicit
language tag; **26.1% carry a non-English tag** (lower bound; 44.0% of tagged
titles); 16.1% contain non-ASCII characters. **55.4% carry a page-title/retailer
segment** after the offer title and **50.7%** match an observed
retailer-boilerplate marker; 5.8% contain a `Null` literal. Top tags: en 7,941,
es 2,008, en-US 1,374, de 967, fr 921, NL 746, it 718, pl 655.

**Step 5 — recommendation (not committed, for review).** Take forward **Framing
B with a blocking key**, not a whole-title normkey: a principled blocking
function — brand token plus model-number token is the obvious candidate here,
with step 3b's first-k keys as a crude fallback — designed and frozen before
gate 3 measures anything. Reasons: it is the only variant measured here that
yields a real distribution rather than a point mass (invariant 1); it preserves
the intended mechanism, since a blocking key resolving to one versus several
clusters is exactly spec §3's "generic or ambiguous strings resolve to multiple
clusters", and it keeps ADS and surface stability as separate axes so invariant
2 is not at risk; and it costs nothing already spent, since only the key
derivation changes. Caveats for the reviewer: the blocking key must be frozen
before gate 3 or the ADS range becomes a tuned quantity (invariant 5);
coarsening trades range for meaning, and a k=2 key is close to a brand bucket,
so brand+model must be checked to confirm it keeps range without collapsing into
brand frequency; 15,179 offers may be thin once split for held-out evaluation
(invariant 3); and with about half of titles carrying boilerplate and at least
26% non-English, normalisation choices move the numbers materially and must be
frozen and reported rather than tuned.

**Invariant checks run:** #1 — this pass *is* the invariant 1 check; result is
reported honestly as a dead axis under both specified framings, and no
downstream work was started on it. #5 — every number above is produced by
committed, re-runnable code (`phase2/gate2_ads_range.py`), including the prose
in the report, which interpolates computed values rather than restating them by
hand. #7 — offline, CPU-only, no API key, deterministic; script self-checks pass
on every run (ADS lies in (0,1]; single-label keys score exactly 1.0; the band
table matches the band definition). #2, #3, #4, #6, #8 — not yet applicable, no
mechanism, winner, selector or claim exists. Off-limits paths untouched; all
changes are under `phase2/`.

**Note on this pass:** a `sed` invocation of mine corrupted
`phase2/gate2_ads_range.py` mid-pass (a too-loose pattern matched trailing
quotes throughout the file). Caught immediately at the syntax error, the file
was rewritten correctly, and the committed version is the one whose output is
reported here. No data or committed artifact was affected.

**Recommendation for next pass:** do not start gate 3. The hard gate's answer is
that both specified framings have a dead ADS axis, so the framing decision is
now a human call. If the blocking-key direction is approved, the next pass
should be scoped to designing and freezing a principled blocking function and
re-running this same characterisation against it, still with no mechanisms
built — effectively a gate 2b — before gate 3 is unlocked.

## Pass 3 — Gate 2b: salvage check, stopped at step 0 (access recon)

**What and why:** Gate 2b asked whether raw WDC schema.org data carries genuine
cross-shop category disagreement for the same product, which would give a real
ADS axis independent of surface variation. Step 0 was the gated access recon,
with instruction to stop if no feasible first-party source exists. It does not
exist. **Stopped at step 0.** Steps 1–6 were not run: no data pulled, no
normalization frozen, no disagreement measured, no ADS computed, no independence
diagnostic. Report: `phase2/reports/gate2b_access_recon.md`. Re-runnable probe:
`phase2/gate2b_access_recon.py`.

**Step 0 verdict — STOP, for two independent reasons.**

*Reason 1, the load-bearing one: the premise does not hold for the WDC LSPC
distribution.* The corpus does not retain each shop's own `schema.org/category`.
The authoritative first-party field list (WDC website source repo
`wbsg-uni-mannheim/wdc-page`, `largescaleproductcorpus/v2/index.html` §2.2
"Schema of the Corpus") is complete and short: `id, cluster_id, identifiers,
category, title, description, brand, price, specTableContent`. The `category`
field is documented verbatim as "One of 25 product categories the product was
assigned to", and §2.1 states "**We learn a classifier** for assigning each offer
to one of 25 top-level product categories." So `category` in every LSPC v2
artifact is one model's output attached to the product, not the shop's
annotation, and no second field holds the shop's annotation. The WDC extraction
pipeline kept identifiers plus title/description/brand/price/specTable and
discarded the rest. This is the same coarse cluster-constant field we already
have, and it is the root cause of gate 2's dead Framing A.

*Reason 2: the WDC data hosts remain down.* `webdatacommons.org` and
`data.dws.informatik.uni-mannheim.de` both refuse connections (origin
`134.155.98.56`, ports 80 and 443), now across three consecutive passes. This is
at the origin, not a local block — an independent fetcher returns the same
`ECONNREFUSED` while unrelated hosts serve normally.

Reason 2 alone would only justify retrying later. Reason 1 means retrying would
not help for any LSPC-derived data.

**Sources checked, what each carries, join-ability, size, host status:**

| Source | Per-shop raw category? | Joins to our 2,485 clusters? | Host |
| --- | --- | --- | --- |
| WDC-25 categorization gold standard | **No** | cluster_id present | data host DOWN |
| LSPC v2 full corpus (2017, our clusters) | **No** — `category` is classifier output | yes, `cluster_id` | data host DOWN |
| WDC Products 2022 benchmark | No, same fields | yes | webdatacommons.org DOWN |
| MWPD challenge Task 2 | **Yes** — `CategoryText` field | **No cluster ids, one record per product** | reachable (Google Drive / bit.ly) |
| Language-modelling product corpora | Unknown, plausible | unknown | data host DOWN |
| WDC HuggingFace org | No — only `wdc/products-2017`, already ingested | n/a | reachable |
| Zenodo | No WDC product corpus; 11 hits all third-party analyses | n/a | reachable |

**The near-miss worth recording:** MWPD Task 2 is the one WDC-derived source
that genuinely carries the signal — its `CategoryText` field is documented as
the "website-specific product category, or breadcrum", i.e. the shop's own raw
category. It fails for a reason unrelated to host status: records carry no
cluster or product identifier, and there is one record per product (~16k
instances). Even with a join there would be no second shop's category for the
same product to disagree with. The data shape forbids the measurement, so steps
3–6 would have had nothing to compute at any normalization strength.

**Corroborating empirical check (committed in the recon script):** the WDC group
commits sample files for each downloadable artifact to its website repo, which
stayed reachable while the data host did not. Scanning all four for any
category-like schema.org property found **none**. The gold-standard offer records
do preserve raw per-offer `schema.org_properties` with the actual terms each shop
used — `/availability`, `/brand`, `/description`, `/image`, `/manufacturer`,
`/name`, `/price`, `/priceCurrency`, `/title` — which is exactly where a
`/category` would appear if WDC had extracted one. It does not. Samples are 10
records each, so this corroborates rather than proves; the corpus schema
documentation above is the conclusive evidence.

**Independent confirmation of gate 1 and gate 2:** the corpus documentation
states the gold standard "consists of offers for **2485 products (ID-clusters)**",
matching exactly the 2,485 clusters gate 1 recovered. And the gold standard's own
methodology — "all offers in the cluster were annotated with the class label" —
is the authors' own confirmation of gate 2's structural explanation for why
per-cluster category purity is identically 1.0. Gate 2's Framing A verdict is now
backed by WDC's documented procedure, not only by our measurement.

**Invariant checks run:** #5 — no number or claim here is unmeasured; the two
load-bearing claims (hosts down, no per-shop category property) are re-verifiable
by `python phase2/gate2b_access_recon.py`, which self-checks and fails loudly if
a category property ever appears, so the verdict cannot silently go stale. #7 —
offline-compatible, CPU-only, no API key, no paid call; the recon makes only
public unauthenticated HTTP requests. No third-party mirrors used or considered,
per instruction. #1–#4, #6, #8 — not applicable; nothing was measured, built or
claimed. Off-limits paths untouched; all changes under `phase2/`.

**Interpretation.** Gate 2b cannot answer its question on WDC data. The
label-disagreement axis this pass was meant to recover does not exist in the WDC
LSPC distribution as published, so neither host availability nor normalization
design would produce it. This does not weaken the gate 2 recommendation, it
removes the main alternative to it: **Framing B with a frozen, principled
blocking key** remains the only measured route to a live ADS axis on this corpus.

**Recommendation for next pass:** a human decision is needed between two paths,
and neither should be started unprompted.

1. *Proceed on WDC with the blocking key* (gate 2 recommendation, unchanged).
   ADS becomes key-ambiguity rather than label-inconsistency. Honest and
   measured, but the consistency axis means something weaker than the paper
   originally framed, and that shift must be stated openly in the paper.
2. *Reconsider the dataset*, which is a spec §2 decision rather than a
   normalization choice. If a genuine per-item label-inconsistency axis is
   essential, it has to come from elsewhere. The spec's secondary dataset — a
   Magellan "Dirty" benchmark via HuggingFace or Zenodo record 8164151 — is
   reachable and is the natural place to look, but evaluating it is a scope
   question for review.

Two things to re-check if `webdatacommons.org` returns, neither worth waiting
on: the language-modelling product corpora, whose paper abstract describes "the
heterogeneous categorization information from the original web shops" and which
is the only untested candidate that could carry both the signal and a cluster
join; and the LSPC v2 corpus sample files, to confirm against real records rather
than schema documentation that no per-shop category property exists.

## Pass 4 — Phase 2.1: S2AND data foundation (hard gate, PASSED)

**What and why:** the first pass on the new substrate. Steps 0 through 4 of
Phase 2.1: access and license recon plus a scoped not-scooped check; ingest;
freeze the blocking normalization; the two-axis sanity check; interpret and
recommend. Measurement and ingest only. No mechanism, no accuracy, no
similarity cutoff, no winner definition, no selector was built, and none exists
anywhere under `phase2/` after this pass.

Code: `phase2/fetch_s2and.py` (download + checksums),
`phase2/s2and_blocking.py` (the frozen definitions, with a runnable
self-check), `phase2/ingest_s2and.py` (table + shape report),
`phase2/gate21_two_axes.py` (the gate). Reports:
`reports/gate21_access_recon.md`, `reports/gate21_data_shape.md`,
`reports/gate21_two_axes.md`. Figures: `reports/figs/gate21_*.png`.

### Step 0 — access, license, not-scooped: all pass

S2AND is obtainable as first-party public data. AI2's own public research
bucket, `s3://ai2-s2-research-public/s2and-release`, which is the location the
`allenai/S2AND` README documents under "Download Data or Model". Pulled over
plain unauthenticated HTTPS at the S3 REST endpoint: no AWS credentials, no
CLI, no API key, no paid call. Not a mirror, not HuggingFace, not Zenodo. The
host was reachable on every request, in contrast to three passes of WDC.

Which release matters. The current README steers new users to an Arrow release
whose smoke-eval example names only `pubmed qian zbmath`. The paper-era JSON
release the README keeps published is the one that carries **all eight**
constituent datasets, and is what we use.

License: **ODC-BY** for the data, stated in the README and shipped inside the
release prefix as `LICENSE.txt` (downloaded and checksummed). ODC-BY permits
our use and permits committing a processed subset as a derivative database,
subject to attribution. Repo code is CC-BY-4.0 (package metadata says MIT); we
use no S2AND code, only two attributed reimplementations for the cross-check.
One caveat recorded rather than buried: the README notes some affiliation data
comes from the Microsoft Academic Graph. `affiliation` is a droppable context
column; flagged for the 2.6 pre-submission gate, not acted on.

Provenance: `phase2/data/MANIFEST_s2and.json`, 19 files, sha256 of every
downloaded byte, 260 MB. One 404 reported rather than hidden:
`medline/medline_clusters.json` does not exist. The three files first fetched
by hand during recon were deleted and re-downloaded by the committed script;
all three checksums were byte-identical.

**Not-scooped: not scooped, but one real flag.** No published work makes the
claim that a design-time consistency signal predicts AND accuracy but not which
matching mechanism to select. The flag is **Kim and Kim 2020 (JASIST 71(7),
839-855; arXiv:2102.03250), "Effect of forename string on author name
disambiguation."** Their abstract states that "performance gains by algorithmic
disambiguation are pronounced when many forenames are initialized or homonym is
prevalent" and that as full-forename ratios rise those gains "become marginal
compared to the performances by string matching." That is a mechanism gap moving
with both a surface quantity and a consistency quantity. It does not scoop us:
their surface axis is a synthetic manipulation rather than a measurement, their
unit is the dataset not the block, they report no winner flip (string matching
"cannot defeat" the ML arm), and they build no selector. It is nonetheless a
live risk to **H2**, since it reports homonymity modulating the gap, and it must
be read in full before 2.2 freezes hypotheses. It also belongs in related work,
where it was not.

### Step 1 — ingest

**Datasets used: seven of eight.** aminer, arnetminer, inspire, kisti, pubmed,
qian, zbmath. **Medline excluded**, for a structural reason, not a size one: the
release ships no `medline_clusters.json` (HTTP 404, confirmed against the bucket
listing), because medline is distributed as labelled *pairs*
(`train_pairs.csv` / `test_pairs.csv`), not clusters. With no cluster file there
is no author label, so there is no ADS to compute. Its `given_block` field is
also 0% populated, where the other seven are 100%. Nothing else was too small or
malformed; every other dataset had 100% cluster coverage and zero rows dropped.

Result: **766,133 signatures**, 26,939 blocks, 59,119 distinct authors, in
`phase2/data/s2and_signatures.parquet` (16 MB, committed; the 260 MB of raw
downloads is gitignored and re-fetchable).

**Exact fields S2AND carries**, identical across all eight: the signature record
is `signature_id`, `paper_id`, `author_id`, and an `author_info` object with
`first`, `middle`, `last`, `suffix`, `position`, `block`, `given_block`,
`affiliations`, `email`. Nothing else. The paper record is `paper_id`, `title`,
`abstract`, `authors` (position + author_name), `venue`, `journal_name`, `year`,
`references`.

Two findings here that change how the data must be used:

- **`author_id` is not the label.** It is a Semantic Scholar author id that
  disagrees with the gold clustering: in zbmath, 796 of 2,334 gold clusters
  contain more than one distinct `author_id`, and 201 `author_id`s span more
  than one cluster. The label of record is the cluster id from
  `*_clusters.json`. Carried in the table so the disagreement stays visible.
- **The surface form is the raw printed name, not a reconstruction.** Joining
  the signature's own `first middle last suffix` reproduces
  `papers[paper_id].authors[position].author_name` **byte-identically** for
  15,181 of 15,181 zbmath signatures, and for 100% of the several hundred
  signatures checkable in the head sniff of each other papers file. This is what
  makes the surface axis legitimate; it is a committed, re-runnable check.

Papers and SPECTER pickles (~6.5 GiB) were deliberately not ingested: they carry
paper-level context 2.2 may want and nothing 2.1 needs. Context-field coverage
varies sharply by dataset and is tabulated in the shape report (affiliations 34%
to 94%, middle names 3% to 43%, email 0% to 47%).

### Step 2 — frozen blocking normalization

Committed in `phase2/s2and_blocking.py` with an assert-based self-check, before
any measurement existed (charter invariant 5). The rule in full: **block key =
first initial + " " + last name, after transliterating to ASCII, lowercasing,
and deleting every character that is not an ASCII letter.** The surface form is
frozen in the same file: the signature's own name parts joined by single spaces,
whitespace collapsed, case and punctuation and diacritics kept, because those
*are* the variation being measured.

We did not simply adopt S2AND's shipped `author_info.block`, for two measured
reasons. It is not a function of the name: 406 of 69,077 distinct
(dataset, first, middle, last) tuples map to more than one shipped block,
affecting 4,247 signatures (0.55%), because hyphens were handled two ways in
preprocessing, so "Murray Gell-Mann" appears under both `m gell-mann` and
`m gellmann`. And it keeps internal spaces and hyphens, so `Gell-Mann` and
`Gellmann` land in different blocks. Our key agrees with it on 98.79% of
signatures and yields 26,939 blocks against its 27,658. Because coarsening a key
raises measured ambiguity and could in principle buy ADS range, **every ADS
number is reported under both keys**, and they agree (see below).

**Block structure.** 26,939 blocks. Signatures per block: min 1, p25 1, median 5,
p75 26, p90 79, p99 284, max 2,339, mean 28.44. Distinct authors per block: min
1, median 1, p90 2, p99 45, max 684, mean 2.74. Distinct surface forms per
block: min 1, median 1, p90 5, p99 15, max 126, mean 2.53. 18,984 blocks (70.5%)
carry 2+ signatures and define both axes; those cover 99.0% of all signatures.

### Step 3 — the two-axis check (the hard gate)

**Consistency axis, ADS: alive.** Over the 18,984 blocks with 2+ signatures, the
spike at exactly 1.0 is **75.77%**; min 0.0377, median 1.0000, mean 0.9017. The
remaining 4,600 blocks are spread across the whole interval, not piled on a few
small-denominator values: 1,385 in [0, 0.5), 1,566 in [0.5, 0.7), 983 in
[0.7, 0.9), 666 in [0.9, 1.0). Fifth percentile 0.3750. Figure:
`reports/figs/gate21_ads.png`. Recomputed on S2AND's own shipped block instead
of ours: 19,227 blocks, spike 75.71%, mean 0.9012, min 0.0410. The axis does not
depend on our key.

**Surface axis, SV: alive, compressed by construction.** Defined as the expected
normalized Levenshtein distance between two signatures drawn at random without
replacement from the block, computed on the raw printed name and
signature-weighted. 34.36% of blocks sit at exactly 0; median 0.0752, mean
0.1048, p90 0.2637, p95 0.3226, p99 0.4502, max 1.0. Bands: 2.83% in (0, 0.02),
7.07% in [0.02, 0.05), 11.77% in [0.05, 0.10), 24.00% in [0.10, 0.20), 13.35% in
[0.20, 0.30), 5.94% in [0.30, 0.50), 0.69% at 0.50 or above. Figure:
`reports/figs/gate21_sv.png` — a spike at 0 followed by a broad, smoothly
decaying body, not a second spike. Its ceiling is well under 1 because every
signature in a block shares a surname; for calibration, "Jane Smith" against
"J. Smith" scores 0.30, against "Jane A. Smith" 0.23 and against "Jane Smyth"
0.10, so the 0.1 to 0.3 range already means most pairs differ in form.

**Independence: genuinely separable.** Over the 18,984 blocks where both are
defined, Pearson r = **-0.2988**, Spearman rho = **-0.2612**, around 7% of rank
variance shared. The sign is the expected one. Within block-size strata the
Spearman association stays between -0.098 and -0.319, so it is not a block-size
artifact. Scatter: `reports/figs/gate21_independence.png`, and the cloud fills
the plane rather than tracing a line. Median-split quadrants hold 1,593 / 3,007 /
7,899 / 6,485 blocks, so every combination of the two conditions is represented.
These are not the same quantity measured twice.

**Cross-check against S2AND's own facets.** S2AND defines block-level
*homonymity* ("the fraction of records in the block with the same names that are
in different clusters") and *synonymity* ("the fraction of records in the same
cluster that have different names"). Both were reimplemented from their
reference implementation (`s2and/eval.py`), on their normalized full name.
Spearman: ADS vs homonymity **-0.818**; SV vs synonymity **+0.743**; ADS vs
synonymity +0.180; SV vs homonymity +0.055; their homonymity vs their synonymity
-0.158. Convergent high, divergent low, on both axes, and their own two facets
are themselves only weakly related. One asymmetry recorded plainly: S2AND's
synonymity is label-conditioned and therefore not computable at design time; our
SV is label-free. The correlation is a validity check, not an equivalence claim.

### Step 4 — verdict

Both axes have real range on real data, and they are separable. Charter
invariant 1 is satisfied, which it was not on WDC, and invariant 2 is not at
risk from these two variables. **Recommendation: proceed to Phase 2.2.** Nothing
in this pass licenses any claim about accuracy or about which mechanism wins.

Carry-forward, not acted on: ADS must be recomputed train-only in 2.2, these are
corpus-level numbers; inspire is 15,077 of 18,984 live blocks, so per-dataset
reporting is not optional; 29.5% of blocks are singletons that drop out of both
axes and will have no history to match against, which is a design decision for
2.2 and not a silent exclusion; SV thresholds must come from its observed
distribution, not from the [0, 1] scale; and Kim and Kim 2020 must be read before
H2 is frozen.

**Invariant checks run:** #1 — this pass *is* the invariant 1 check, and unlike
gate 2 on WDC the answer is that both axes are live; histograms and the
independence numbers are the evidence, and no downstream work was started. #2 —
protected in advance: the surface signal is measured per block from the printed
name and is never set by us, no winner exists yet to define anything from, and
the independence numbers plus the discriminant cross-check confirm the two axes
are not one variable. #5 — every number in the reports, PASSLOG and STATE is
produced by committed re-runnable code; the reports interpolate computed values
rather than restating them by hand. Two hand-typed values caught in draft, a
singleton percentage and a set of calibration edit distances, were replaced by
computed ones; the calibration figures had in fact been wrong. #7 — offline, CPU-only, no API key, no paid
call, deterministic; `s2and_blocking.py` self-checks on every run,
`ingest_s2and.py` asserts id uniqueness, non-empty keys and forms, label
presence and label-dataset containment, and `gate21_two_axes.py` asserts ADS in
(0, 1], exact 1.0 for single-author blocks, exact 0 for single-form blocks, SV
defined on every 2+ block, and that the bands partition. All passed. #3, #4, #6,
#8 — not yet applicable; no split, mechanism, baseline, selector or claim exists.
Off-limits paths untouched; all changes are under `phase2/` plus one `.gitignore`
line.

**Recommendation for next pass:** Phase 2.2, the boundary finding, in a fresh
session after review. Freeze the fuzzy cutoff, the winner definition, the splits
and the practical-equivalence margin at its start, before any accuracy is
measured. Read Kim and Kim 2020 first.

## Pass 5 — Phase 2.2a: freeze the pre-registration (no measurement)

**What and why:** the charter's invariant 5 requires the pre-registration to be
committed before the measurement it governs, and the 2.1 carry-forward required
Kim and Kim 2020 to be read in full before H2 was frozen. This pass does those
two things and nothing else. No mechanism, no accuracy, no similarity cutoff, no
winner, no selector was built, and none exists anywhere under `phase2/` after
this pass. No new number was computed; every figure quoted in the new files is
an already-committed Phase 2.1 measurement, cited as design context.

New files: `phase2/PREREG.md` (the frozen pre-registration),
`phase2/reports/kim2020_positioning.md` (the sibling read and the positioning).
Edited: `phase2/phase2-spec.md` section 8 now points at PREREG.md as its
successor, `phase2/PLAN.md` splits 2.2 into 2.2a and 2.2b, `phase2/STATE.md`,
`.gitignore`.

### Step 1 — Kim and Kim 2020, read in full

Read from the author preprint the human placed at `phase2/Kim and Mim paper for
review.pdf`, 25 pages, all body text plus appendices A and B plus the reference
list. Title, authors, and journal reference checked against the arXiv abstract
page for 2102.03250 and they match: JASIST 71(7), 839-855 (2020), DOI
10.1002/asi.24298, categories cs.DL, cs.IR, cs.LG.

**What they did.** Four labelled AND datasets (PENN, KISTI, AMINER, GESIS).
Surface variation is *manufactured*, twice: the full-forename ratio is set from
0% to 100% in steps of 10 with 10 random repetitions, and forenames are truncated
to 1 through 10 characters. Blocking is surname plus first initial, the same
family as ours, so the manipulation stays inside blocks. Heuristic arm is string
matching on all available name strings; algorithmic arm is five classifiers over
four pairwise features feeding hierarchical agglomerative clustering. Metric is
B-cubed P/R/F1 at **dataset level**, averaged over 10 iterations.

**What they found, stated precisely because the precision is the whole point.**
The result is **gap compression, not a winner reversal**. The margin by which ML
beats string matching shrinks as full forenames get more common, and their
conclusion says string matching "cannot defeat feature-based machine learning."
On B-cubed F1, against the best algorithmic arm, string matching **never wins**,
in any of the four datasets, at any setting. Two component-metric crossings exist
and are recorded in the report rather than smoothed over: heuristic precision
overtakes Naive Bayes, their weakest classifier, above the 60% ratio in PENN, and
heuristic recall exceeds the algorithms below the 50% ratio in PENN, which is
degenerate because at 0% the heuristic puts nearly everything in one cluster for
recall 0.99 at precision below 0.1. Neither survives into F1. In the two
homonym-centric datasets (AMINER, GESIS) everything is flat and the algorithmic
arms stay above the heuristic across the whole range.

**One protocol detail worth carrying.** Their clustering threshold is chosen per
block by trying values and keeping the one that maximises that block's B-cubed
F1, that is a per-block oracle tuned on the evaluated outcome, while the
heuristic has no parameter at all. "String matching cannot defeat ML" is
therefore a zero-tuning arm against a per-block-oracle arm.

**A limitation they state that opens our door.** They address only the
initialization form of synonymy and explicitly exclude edit-distance variants and
flipped token order, noting the effect may matter for German, Hispanic and Slavic
names. That is exactly where our measured SV lives.

**Point-by-point differences** are tabulated in the report across nine axes:
manipulated vs measured surface axis, design-time availability, consistency axis
(their dataset-level homonym characterization vs our per-block train-only ADS),
unit (dataset vs block), mechanisms (string vs ML against exact vs fuzzy), task
(clustering scored by B-cubed against assignment scored by accuracy with
abstention), winner as a construct (absent there, pre-registered here), selector
(none there), and generalization breadth.

**Seven honest collapse risks, flagged rather than buried.** The sharpest: if our
SV is mostly forename initialization, H3 is their manipulated variable observed
instead of set, and the novelty reduces to unit of analysis plus framing. Also:
gap compression without reversal *is* their result; H1 is close to already known
and is demoted to a construct-validity check; H2 must be about the winner's sign
and identity, not gap magnitude, because ADS predicting magnitude is their
finding and is not a refutation; exact vs fuzzy is a smaller comparison than
string vs ML; exact and fuzzy may *coincide* on a single-surface-form history, so
the low-SV half of H3 may be structural ties rather than exact-match wins; and SV
and the fuzzy mechanism share an edit-distance metric family. Every one of these
is written into the pre-registration as a pre-listed reportable outcome or a
pre-registered control.

### Step 2 — `phase2/PREREG.md`, frozen

Committed before any accuracy exists. Supersedes `phase2-spec.md` section 8.
Carries an amendment rule: changes are appended as dated amendments in the same
commit as the code that needs them and before the affected numbers exist; the
original text is never edited away.

**Hypotheses**, phrased for the specific design-time, per-block, measured
dissociation rather than the general "surface affects the gap" that Kim and Kim
already showed. H1 is labelled in the document itself as construct validity, not
a contribution. H2 is explicitly about the *identity* of the decided winner at
fixed SV, with the ADS-to-gap-magnitude relationship reported beside it as a
previously known effect reproduced at block level. H3 requires a winner reversal
at fixed ADS *and* survival of the initialization control.

**Falsification table**, four outcomes per hypothesis, each with a concrete
decision rule. Plus a separate list of six outcomes named as acceptable and
honestly reportable, so none of them can later read as something to avoid. Two of
them are the ones review asked for by name: "the gap only compresses, no
reversal" is H3 not supported, reported in those words as a per-block,
design-time, measured version of Kim and Kim's finding with the dissociation
claim dropped; and "co-signal does not help" is listed for 2.3 under invariant 4,
including the case where neither selector beats the better fixed policy. The
other four: SV turns out to be initialization; the low-SV region is structurally
tied; ADS predicts gap magnitude; the population is too thin and inconclusive is
used rather than lowering a threshold.

**Signals and thresholds.** ADS train-only, five fixed purity bands. SV is the
gate-2.1 `surface_variability` function unchanged, applied train-only; the
document states that train-only is a choice for SV rather than a necessity, since
SV needs no labels, and gives the reason. Thresholds come from the observed
distribution, not the [0,1] scale: band 0 is SV exactly 0 as a structural band of
its own, bands 1 to 3 are terciles of the strictly positive values with cut
points taken from the **calibration split**, so not even the band edges see
evaluation data.

**Winner definition.** Per block, paired bootstrap on the accuracy difference,
B = 2000, both mechanisms scored on the same resample, 95% percentile interval,
practical-equivalence margin delta = 0.05 fixed now. Four verdicts: exact wins,
fuzzy wins, tie, undecided. Tie (equivalence shown) and undecided (no power) are
kept apart deliberately, and verdict share is reported as a function of test-set
size so no-winner regions cannot pass as equivalence. Per ADS band the summary is
two things, both required: the four-way verdict distribution over blocks, and a
pooled band verdict that resamples **blocks** rather than signatures because the
block is the independent unit.

**Winner-structure analysis, stated up front.** 2.2b will report whether the
pattern is a genuine winner change or only gap compression, using three
definitions fixed now: winner reversal, tie-crossing, and gap compression only.
The exact-minus-fuzzy gap is reported as a function of both axes in a 5x4
ADS-by-SV grid, so SV's effect is always shown at fixed ADS and ADS's at fixed
SV; this is required, not optional, precisely because the axes correlate at
Pearson -0.2988 / Spearman -0.2612. Cells under 30 blocks are printed with their
counts, marked under-powered, and excluded from every decision rule.

**Kim and Kim overlap control.** Primary: SV_resid, the same frozen SV function
applied to an initialization-canonical surface form (first name and each middle
token reduced to an initial, surname and suffix kept), under which "John Smith"
and "J. Smith" are identical, so forename initialization contributes exactly
zero. The whole grid is rerun with it and H3 requires the reversal in both.
Secondary: stratification by INIT, the train-only share of initial-only given
names, in three fixed bands. A third arm reruns fuzzy with Jaro-Winkler, against
the fair objection that SV and the fuzzy mechanism share a metric family.

**Per-dataset reporting made binding**, section 11, since inspire is 15,077 of
18,984 live blocks. Every headline table and every hypothesis decision is
reported per dataset, for inspire alone, and pooled non-inspire. A finding is
called generalizing only if it holds pooled non-inspire *and* in a majority of
qualifying non-inspire datasets, qualifying at 100 or more blocks; otherwise it is
reported as an inspire finding in those words.

**Split and ADS recomputation.** 15% of live blocks form the calibration split,
seed 20260918, used once for the fuzzy cutoff and the band edges and never for a
reported number. The other 85% is the evaluation split, with a within-block
train/test rule of `n_train = max(1, min(n-1, floor(0.7n)))`. ADS is recomputed
train-only. The primary analysis population is blocks with `n_train >= 2` and
`n_test >= 1`; blocks of exactly 2 are a named, counted, separately reported
exclusion rather than a silent drop, because ADS on one train signature is 1.0 by
construction and SV is undefined.

**Fuzzy-cutoff calibration protocol**, specified and not executed: calibration
blocks only, fixed grid 0.50 to 0.95 in steps of 0.05, pick the highest pooled
accuracy, break ties toward the higher (more abstaining) cutoff, commit the value
and the full curve, then frozen. One global cutoff, not one per dataset or band,
because a per-stratum cutoff would give fuzzy a tuning budget exact cannot have.
The residual asymmetry, one tuned parameter against none, is to be stated in the
paper.

**Key numbers / plots:** none produced. This pass deliberately computed nothing.
The two new documents are at `phase2/PREREG.md` and
`phase2/reports/kim2020_positioning.md`.

**Invariant checks run:** #5 — this pass *is* an invariant 5 action: the
pre-registration is committed before the measurement it governs, and the
positioning report is committed before the hypotheses it informed were frozen. No
number in either file is new; each quoted figure is an already-committed 2.1
measurement used as design context, and I verified that by re-reading
`reports/gate21_two_axes.md` rather than recalling. #2 — protected in the design:
PREREG.md section 12 records that the winner is defined only by labelled accuracy
and that neither ADS nor SV nor SV_resid appears in its definition; the
shared-metric objection between SV and the fuzzy mechanism is acknowledged as a
fair criticism rather than dismissed, and a Jaro-Winkler arm is pre-registered
against it. #3 — the calibration split is disjoint from the evaluation split at
block level and is burned on the cutoff and the band edges; no test signature
reaches any signal, cutoff, or band edge. #4 — the 2.3 baselines are restated in
PREREG.md section 2 with the explicit outcome that if SV-only suffices, the paper
says SV-only suffices. #6 — two mechanisms only; no semantic or LLM arm is
specified. #7 — nothing was run, and the protocol as written stays offline,
CPU-only, seeded and deterministic. #1 and #8 — 1 was satisfied at 2.1 and is
untouched; 8 is what the falsification table and the acceptable-outcomes list
exist to enforce. Off-limits paths untouched; all changes are under `phase2/`
plus one `.gitignore` block.

**One licensing note, acted on.** `phase2/Kim and Mim paper for review.pdf` is a
publisher preprint with no redistribution licence, so it is gitignored and stays
untracked rather than entering a repo that becomes public. The file is read from
disk; the citation is what the paper carries.

**Recommendation for next pass:** Phase 2.2b in a fresh session after review.
Execute PREREG.md exactly and do not re-decide any of it; if something in it is
unrunnable, append a dated amendment to that file in the same commit as the code
that needs it, before the affected numbers exist. Order of work: build the split
and the two mechanisms with their self-checks, calibrate the fuzzy cutoff once on
the calibration split and commit the frozen value with its curve, compute the
calibration-split band edges and commit those, and only then touch the evaluation
split. The one thing to watch early is the mechanism agreement rate at low SV; if
exact and fuzzy turn out to be the same procedure on most single-surface-form
histories, that shapes the finding and should be surfaced at review rather than
discovered in the writing phase.

### Pass 5, addendum — two reviewer rules folded into PREREG.md

Applied at review of the 2.2a freeze, still before any measurement and before
2.2b starts. Both were supplied by the reviewer and are inserted verbatim.

- **Section 8, margin sensitivity.** delta = 0.05 is the primary margin, and
  every band-level and cell-level verdict plus the H2 and H3 outcomes are also
  recomputed at delta = 0.02 and 0.03 and reported as a robustness curve. An
  outcome that holds at one margin and flips at another is margin-dependent and
  is treated as Partial, not Supported. This closes a hole I left: delta was
  fixed but nothing stopped 2.2b from reporting a single margin's result as if
  the choice of margin were immaterial.
- **Section 10, order of evaluation.** Inconclusive is evaluated first and takes
  precedence over every other row. In particular, an all-tie-or-undecided band
  set is not H2 Supported unless at least two ADS bands and two SV bands each
  have 30 or more blocks and a decided pooled verdict. This closes a real
  loophole in the H2 Supported row as I wrote it: "or all such verdicts are tie
  or undecided" would have let a completely underpowered run read as support for
  selection blindness, which is the hypothesis most flattered by having no
  evidence at all.

Both rules tighten the falsification table; neither relaxes it. A revision
history note was added at the top of PREREG.md recording the change and its
timing, so the document's authority as a pre-registration is auditable rather
than asserted.

---

## Pass 6 — Phase 2.2b, the boundary experiment (2026-09-18)

**What I did and why.** Executed `PREREG.md` as frozen, in the order it
prescribes: build the split and the train-only signals, calibrate the fuzzy
cutoff once on the calibration split and commit it, then and only then touch the
evaluation split. Two commits, deliberately: `5e13e38` freezes the calibration
before any evaluation number exists, `3d86959` carries the results. Nothing in
PREREG.md was re-tuned, re-banded or redefined, and no amendment was needed,
because nothing in it turned out unrunnable.

**The headline is methodological, and it was measured rather than deduced.**
Under PREREG section 4 as frozen, **exact match is a strict sub-case of fuzzy
retrieval**. When a test surface form occurs among the train forms it sits at
similarity exactly 1.0, which is the maximum, so the fuzzy arm selects that same
form at any cutoff at or below 1.0 and resolves the author with the same frozen
tie-break. Across all 16,136 evaluation blocks and 199,713 test signatures there
are **zero** signatures on which exact is right and fuzzy is wrong, in either
metric arm. Three consequences:

- `exact wins` is an unreachable verdict. The four-verdict rule can only return
  fuzzy wins, tie, or undecided, so a winner reversal, which H3 requires and H2
  forbids, cannot occur for either signal at any margin. The design could not
  have produced the alternative outcome.
- The pooled gap is exactly one quantity: minus the share of test signatures
  where exact abstains and fuzzy is correct. The whole exact-minus-fuzzy story
  is the 3.2-point coverage difference, 0.9686 against 0.9988.
- The mechanism agreement rate, which PREREG section 4 added specifically to
  separate genuine equivalence from structural coincidence, turns out to be the
  identity exact coverage plus fuzzy abstention rate: 0.9664 + 0.0015 = 0.9679,
  to every digit. The diagnostic measures the structural coincidence exactly.

`reports/kim2020_positioning.md` item 6 anticipated this risk, but as a low-SV
effect. Measured, it is total and holds at every SV level. **Reported, not
repaired.** Changing the mechanism pair, the cutoff or the tie-break to make the
comparison two-sided is a change to a frozen definition after the affected
numbers exist, which the amendment rule reserves for review.

**Outcomes against the frozen falsification table**, Inconclusive evaluated
first per the 2.2a reviewer rule:

- **H1 Supported.** Spearman of train-only ADS with held-out accuracy is 0.5069
  [0.4916, 0.5224] for exact and 0.7436 [0.7305, 0.7568] for fuzzy, both
  block-bootstrap intervals clear of zero, positive in pooled non-inspire and in
  all four qualifying non-inspire datasets (aminer, kisti, qian, zbmath), so it
  generalizes. Stated in PREREG as a construct-validity check, not a
  contribution, and reported as one.
- **H2 Inconclusive.** The power floor is not met: at delta = 0.05 no ADS band
  and no SV band has a decided pooled verdict. This is the reviewer rule added
  at the 2.2a freeze doing exactly its job, since the all-tie band set would
  otherwise have read as support for the hypothesis most flattered by an absence
  of evidence.
- **H3 Inconclusive at delta = 0.05, Partial at 0.02, so margin-dependent.**
  At 0.02 the ADS = 1.0 row clears the floor with three decided SV bands and one
  ADS band shows a tie-crossing, which is the Partial row.

**Substance beside the verdict, reported separately rather than substituted for
it.** The pattern is gap compression: at fixed ADS the pooled gap grows with SV
monotonically in four of the five ADS bands and never changes sign. Under the
frozen rules that reading is only available above the power floor, which is not
cleared at the primary margin, so the verdict stays Inconclusive and the
substance is stated next to it.

**Key numbers and where they live.**

- Report: `reports/phase2b_boundary.md`. Calibration: `reports/phase2b_calibration.md`.
- Frozen constants: `phase2/phase2b_constants.py`. Cutoff 0.50 for both metric
  families, on the lower boundary of the pre-registered grid because both
  accuracy-versus-cutoff curves are monotonically decreasing: with abstention
  scored as wrong, the fuzzy arm is never helped by abstaining. SV band edges
  0.102644 / 0.195066, SV_resid 0.036782 / 0.082418, all from calibration blocks.
- Population: 13,902 primary-population blocks, 197,479 test signatures. Named
  exclusions reported not dropped: 7,955 singleton blocks (1.04% of signatures)
  and 2,234 block-size-2 blocks (0.58%).
- Pooled accuracy exact 0.8244, fuzzy 0.8441, gap -0.0196.
- Per-block verdicts at delta 0.05: 0 exact wins, 302 fuzzy wins, 11,117 tie,
  2,483 undecided.
- Regression of the per-block gap: ADS -0.0495 (se 0.0043), SV -0.1443 (se
  0.0172), log test-set size +0.0308 (se 0.0015).
- Signals: SV to SV_resid Spearman 0.51, SV to INIT 0.36, ADS to SV -0.27. SV is
  correlated with forename initialization but is not it.
- Figures: `reports/figs/phase2b_h1_ads_accuracy.png`, `phase2b_grid_gap_sv.png`,
  `phase2b_grid_gap_svresid.png`, `phase2b_verdicts_by_sv.png`,
  `phase2b_verdicts_by_ads.png`, `phase2b_power_by_size.png`,
  `phase2b_margin_sensitivity.png`. Tables: `reports/tables/phase2b_*.csv`.

**Two readings I had to fix, both recorded in the report rather than resolved
silently.** First, PREREG section 9 gates the structural classification at two
bands of 30 or more blocks while section 10 sets the Inconclusive floor at two
bands that are also decided; the Order of evaluation rule makes the latter a
hypothesis-level test, so both counts are printed per row and either reading can
be checked against the same numbers. Second, section 9 asks for block-clustered
standard errors on a regression whose unit of observation is the block, where
each cluster holds one observation and the estimator reduces algebraically to
the heteroskedasticity-robust one; that is what is computed and the report says
so instead of printing a label that would imply more.

**Invariant checks run.** #2 — the winner is defined only by labelled accuracy;
neither ADS nor SV nor SV_resid appears in its definition, and the shared-metric
objection is answered by the Jaro-Winkler arm, which reproduces the same picture
(pooled gaps -0.0379, -0.0177, -0.0181, -0.0192 across SV bands, all ties at
delta 0.05). #3 — `verify_no_leakage` runs on every execution and asserts the
calibration and evaluation block sets are disjoint and partition the 18,984 live
blocks, that the frozen n_train rule holds for every live block, and that ADS
and SV recompute train-only on a 300-block sample. It passes. The cutoff and the
band edges were committed before the evaluation split was read. #5 — every
number above is produced by committed, re-runnable code; re-running
`phase2b_build.py` reproduces `phase2b_constants.py` byte for byte, verified
before the freeze commit. #6 — two mechanisms only. #7 — offline, CPU-only,
seeded, deterministic, no API call. #1 and #8 — 1 was satisfied at 2.1; 8 is why
the degeneracy leads the report instead of sitting in a limitations paragraph.
Off-limits paths untouched; every change is under `phase2/` plus one `.gitignore`
line.

**One bug found and fixed before the final run.** The per-block paired bootstrap
was seeded with the block index alone rather than 20260918 offset by it, as
PREREG section 8 specifies. Fixed and re-run; no outcome changed.

**One disclosure.** The calibration run printed exact-match accuracy on the
calibration split (0.8223) alongside the fuzzy curve, as console context. It
entered no frozen choice: the cutoff rule selects on pooled fuzzy accuracy
alone and both it and the band rules are mechanical. Recorded here because the
value was observed before the evaluation split was read.

**Recommendation for the next pass.** Do not start 2.3 as planned. The selector
question 2.3 exists to ask cannot be asked of this mechanism pair: a selector
choosing between a mechanism and a strict superset of it has nothing to choose,
and an SV-only or two-signal selector would be scored against a comparison whose
winner is fixed in advance. Review needs to decide one of:

1. Amend PREREG section 4 to a genuinely two-sided mechanism pair, dated and
   agreed before any new accuracy exists. The obvious candidate is to make the
   fuzzy arm exclude exact matches, or to give exact an advantage fuzzy lacks,
   but any such change is a new pre-registration and its numbers are new numbers.
2. Keep the pair and retarget the paper on what this run does establish: the
   design-time consistency signal predicts each mechanism's accuracy and
   generalizes across datasets, while the winner between a mechanism and its own
   relaxation is a coverage question with no selection content. That is a
   smaller paper and the title would have to change.
3. Replace the second mechanism with one that is not nested, which reopens
   charter invariant 6 and is a larger scope change.

Whichever is chosen, the 2.2b numbers stand as the frozen evidence base for it,
and the degeneracy is a result to report in the paper rather than a mistake to
erase, because it is a property of a mechanism pair that a reader might
reasonably have proposed themselves.

---

## Pass 7, Phase 2.2c: mechanism redesign, design-and-propose

**Date:** 2026-09-18. **Branch:** phase-2.

**What this pass did and why.** 2.2b found the frozen mechanism pair nested, so
the selection question 2.3 exists to ask is unanswerable against it. This pass
designs a replacement: a mechanism pair where each side can win in some regime.
It proposes, checks the proposals cheaply on the calibration split, and stops.
No evaluation-split number was produced, `PREREG.md` was not amended, and the
2.2b evidence base is untouched.

**The narrow reason the old pair failed, which rules out most repairs.** When the
test surface form occurs in the train history it sits at similarity exactly 1.0,
the maximum of any similarity function, so any retriever that takes the single
nearest form takes that form and resolves the same author. Exact match is
contained in *every* 1-NN retriever, whatever the metric, cutoff or tie-break.
A different similarity cannot fix it; mechanism B has to stop being 1-NN, either
by aggregating over a neighbourhood or by matching on a representation under
which the test form is not privileged.

**What was built.** `phase2/phase2c_probe.py`, calibration blocks only, with an
assert-based self-check. Mechanism A is the PREREG section 4 exact-evidence rule,
unchanged. Three candidate B arms, all label-free at prediction time, all
untrained, none using forename fullness as the axis: a radius vote (P1), a
normalized-key vote (P2, no parameter, and built so initialization does *not*
collapse), and a k-nearest vote (P3). The frozen 2.2b fuzzy arm is scored beside
them as a probe self-check and returns 0 on the A side, reproducing the nesting.

**Two-sidedness on the calibration split**, 2,450 blocks, 35,732 test signatures,
as (A right and B wrong) / (B right and A wrong):

- rule vs nn1, the 2.2b pair: **0** / 731. Dead, as in 2.2b.
- P1 radius: 1,461/635 at r=0.70, 793/503 at 0.80, 253/247 at 0.90, **0**/16 at 0.95.
- P2 mergekey: 158/437, no parameter on either side.
- P3 knn: 181/736 at k=2, 314/740 at k=3, **546/744 at k=5**, 912/748 at k=10.

All three candidates are genuinely two-sided. Accuracies at the recommended
setting are 0.8234 for the rule and 0.8290 for knn@5, so it is a real contest.

**The structural constraint the probe found, which is the pass's main result.**
The rule wins zero signatures in every SV=0 cell and zero in every ADS=1.0 cell,
for all three pairs, and both zeros are necessary rather than small. At SV=0 the
history carries one distinct form, so every mechanism pools the same evidence. At
ADS=1.0 the history names one author, so any non-empty pool returns it and the
rule's only possible difference is to abstain. **The second holds for any pair of
mechanisms that assign an author from the block's own history, not just these.**
A contest therefore exists only where the history is both impure and
surface-varied, which is 41% of calibration test signatures.

**This contradicts H2 as PREREG section 2 words it**, and no redesign inside this
family can rescue that wording: ADS does predict part of the winner, because at
ADS=1.0 the retriever wins or ties by construction. Equally, at fixed ADS the
sign of the gap still flips with SV in all four ADS bands below 1.0, so ADS alone
does not determine the winner either. The supportable shape is a two-signal one:
consistency says whether the choice matters, surface stability says which way to
go when it does. That is a change to the paper's identity and it is review's to
make.

**The calibration trap, flagged for the new pre-registration.** For both
parameterized pairs the retriever's pooled accuracy is monotone toward the 1-NN
limit: knn falls 0.8390, 0.8354, 0.8290, 0.8188 as k grows, radius rises to
0.8239 at r=0.95. PREREG section 7 calibrates by maximizing pooled accuracy, so
applied unchanged it would select k=2 or r=0.95 and walk the design straight back
into nesting. The parameter must be fixed by a definitional argument with a
pre-registered sensitivity curve, never chosen to maximize the retriever.

**Ruled out cheaply.** A context-based mechanism (co-authors, venue, title) was
considered and dropped without building it: the ingested table carries `paper_id`
but only 18.7% of its papers hold 2 or more signatures, so co-authorship is too
thin to found a mechanism on, and the papers files that carry the rest are the
3.4 GiB S2AND payload Phase 2.1 deliberately did not ingest. The pair stays in
the name-string family, which is also where charter invariant 6 wants it.

**Invariant checks run.** Invariant 2, no tautology: the winner would still be
defined by labelled accuracy alone and neither ADS nor SV appears in any
mechanism definition. Invariant 3, held-out only: the probe touches calibration
blocks only, which are disjoint at block level from every block that has ever
produced a reported number. Invariant 5, no result before measurement: nothing
here is a result and the report says so twice; `PREREG.md` is byte-unchanged.
Invariant 6, two-mechanism core: two mechanisms, neither trained. Invariant 7,
offline and CPU-only, with an assert-based self-check that fails loudly if any
mechanism drifts.

**Artifacts.** `phase2/phase2c_probe.py`,
`phase2/reports/phase2c_pair_design.md`,
`phase2/reports/tables/phase2c_pair_twosidedness.csv`,
`phase2/reports/tables/phase2c_pair_regimes.csv`.

**Recommendation for the next pass.** Adopt P3, the exact-evidence rule against a
k-nearest vote with k fixed a priori at 5 and the k in {2,3,5,10} curve reported
as mandatory sensitivity. P2 is the fallback if review prefers zero parameters on
both sides. Then, and only then, write a new pre-registration as a dated
amendment section appended to `PREREG.md`, before any new accuracy exists. That
new pre-registration has three things to settle that the old one did not face:
the replacement for H2, given that two of its cells are zero by construction; the
analysis population, which should probably become the contested region; and the
margin inside that region, since 2.2b was already power-limited at delta = 0.05
on a larger population. Do not run the evaluation until that document is frozen
and committed.

---

## Pass 8, Phase 2.2d: pre-registration revision, the two-signal reframe

**Date:** 2026-09-18. **Branch:** phase-2.

**What this pass did and why.** Applied the handed-over revision that rebuilds
the paper's claim from a one-signal blindness statement into a two-signal role
separation. Nothing was run, measured, or computed. The pass is entirely
documents.

**Why the claim had to be rebuilt rather than repaired.** Two measured structural
findings, one per preceding pass. 2.2b: a test form present in the train history
sits at similarity exactly 1.0, so any single-nearest retriever contains exact
match, and `exact wins` measured zero on 199,713 test signatures in both metric
arms. 2.2c: a precision-first rule cannot win a block whose train history names
one author, because any non-empty pool returns that author and the rule's only
possible difference is to abstain, which holds for any pair of mechanisms that
assign an author from the block's own history. The second one is what kills the
old H2: consistency necessarily carries some winner information, so "ADS does not
predict which mechanism wins" is not true of any pair in this family and is not
recoverable by changing mechanisms.

**How the amendment was applied, and one deviation from the instruction.** The
revision said to replace sections 2, 4, 7 and 10 of `PREREG.md` in place.
PREREG's own amendment rule says the opposite: a change is made by appending a
dated amendment section, and the original text is never edited away. Applied as
an appended **Amendment 1** carrying the full replacement text and marked
binding, with a superseded banner inserted at the head of each of sections 2, 4,
7 and 10 pointing to it, and a new first entry in the revision history. Same
binding effect, and the 2.2a text and the conditions 2.2b was run under stay
readable in full. Flagged here because it is a deviation in form from the
instruction, taken to satisfy the document's own rule.

**What Amendment 1 fixes.**

- **Section 2, replaced.** H1 unchanged in substance, still a validity check. H2
  is now a gating hypothesis: holding SV fixed, the share of blocks with a
  decided winner declines as ADS rises, approaching zero in the top band, while
  staying non-trivially positive lower down. H3 is now two required parts,
  direction by SV (a genuine reversal at fixed ADS below 1.0) and non-direction
  by ADS (the old blindness claim, correctly scoped to decidable blocks at fixed
  surface stability, which is where it can be true). The contribution is the
  conjunction.
- **Section 4, amended.** Mechanism A is untouched. Mechanism B is the
  k-nearest-vote retriever: pool nearest training signatures, whole forms at a
  time, until at least k are pooled, then a signature-weighted author vote. It
  does not abstain, so abstention sits entirely on the rule's side.
- **Section 7, void for 2.2e.** B has no cutoff to calibrate. k = 5 is fixed by
  definition, never by maximizing accuracy, because accuracy is monotone toward
  the single-nearest limit and that limit is the 2.2b nesting. The k in
  {2, 3, 5, 10} curve is mandatory and a k-dependent outcome is Partial. Section
  6's SV and SV_resid band edges, calibrated under the same protocol at
  `5e13e38`, carry over unchanged and are not recomputed.
- **Section 8, renamed only.** `exact wins` to `rule wins`, `fuzzy wins` to
  `k-NN wins`. Bootstrap, seeds, margins, four-verdict rule all as frozen.
- **Section 10, replaced.** New falsification table. Inconclusive still evaluated
  first. Two acceptable outcomes added: the choice is never live, and consistency
  directs as well as gates.
- **Section 3 unchanged.** ADS = 1.0 blocks stay in the primary population,
  because H2 needs them. H3 scopes itself to ADS below 1.0 in its own wording,
  which is the right place for that restriction. This settles the open question
  2.2c raised about moving to a contested-region population: the answer is no.

**Six resolutions, all flagged for review.** The revision was under-determined or
drifted from what 2.2c measured in six places, each resolved in the amendment
before any number exists. (1) "k nearest" counts signatures, not forms, because
that is what 2.2c measured and the form-counted reading is untested. (2)
Mechanism B uses the frozen section 4 tie-break chain, not "toward the nearest
form", which is under-determined for equidistant forms and would give the two
mechanisms different tie-breaks, turning part of the winner contest into a
comparison of tie-break rules. (3) The nesting limit is k = 1, not k = 2 as the
revision states; k = 2 measured 181 rule wins against 736, so it is close to the
limit but not at it, and k = 1 stays off the curve as the known-degenerate case.
(4) "Decided" in H2 means the per-block verdict; H3's reversal keeps the pooled
band verdict. (5) "ADS is the stronger driver of decidability" means the larger
averaged range of the decided-winner rate across its axis of the frozen 5 by 4
grid. (6) "A non-trivial decidable region" means at least one ADS band below 1.0
with 30 or more blocks holding 30 or more decided per-block verdicts, an absolute
count reusing the existing minimum rather than a new threshold.

Resolutions 5 and 6 are the two that set a bar where none was given, so they are
the two most worth review's attention. They can be overruled before 2.2e starts
and not after.

**Identity reframed in the governing documents.** `phase2/CLAUDE.md` mission,
`phase2/PLAN.md` paper identity, and `phase2/phase2-spec.md` section 1 and the
section 3 construct note, all per the instruction. Three further lines were stale
after the reframe and would have left the charter contradicting the amendment, so
they were updated too and are listed here rather than made silently: charter
invariant 6, which named exact match versus fuzzy retrieval as the core
comparison; charter invariant 8, which told future passes to lead with "the
boundary finding", a thing that no longer exists under that name; and spec
section 3's surface-stability bullet, which asserted "so fuzzy wins" as though it
were settled rather than being H3. Spec section 4 gained a superseded pointer and
spec section 6's gate list was brought up to date. PLAN.md's working titles were
replaced with the three supplied.

**Numbers produced:** none. **Invariant checks run.** Invariant 5, no result
before measurement: no mechanism B prediction on the evaluation split has been
computed anywhere, the amendment says so in its own header, and the only
measurements cited in it are the 2.2c calibration diagnostics, disclosed as such.
Invariant 2, no tautology: neither ADS nor SV nor SV_resid appears in either
mechanism definition. Invariant 3, held-out only: the split is unchanged, so
2.2e's evaluation blocks are 2.2b's evaluation blocks, and the k = 5 choice used
calibration blocks only. Invariant 6, two-mechanism core: two mechanisms, neither
trained; the charter's wording of this invariant was updated to name the new
pair. Invariant 7: nothing added that is not offline and CPU-only. The three
existing module self-checks still pass and were re-run.

**The honest risk this pass creates.** The hypotheses were rewritten after two
passes returned results. That is post hoc, and a reviewer will say so. The
defence is procedural and has to be visible in the paper rather than only in the
repository: the amendment is dated and appended instead of edited in, the
superseded text and the 2.2b numbers stay where they are, what forced each change
is a measured structural fact rather than a disappointing number, and no accuracy
for the new mechanism existed anywhere when the amendment was written. It is also
worth stating plainly that the new H2 has a partly structural component, the
guaranteed decline into the ADS = 1.0 band, which the amendment flags in its own
text and which the load-bearing content deliberately sits below.

**Artifacts.** `phase2/PREREG.md` (Amendment 1, plus four banners and a revision
history entry), `phase2/CLAUDE.md`, `phase2/PLAN.md`, `phase2/phase2-spec.md`,
`phase2/STATE.md`.

**Recommendation for the next pass.** Review verifies Amendment 1 end to end,
and the six resolutions in particular, before anything runs. Then 2.2e: implement
mechanism B in a module with its own assert-based self-check, confirm it
reproduces the 2.2c calibration-split counts of 546 rule wins against 744 at
k = 5 as a regression check on the implementation, then re-run the frozen
analysis with the renamed verdicts and report against the amended falsification
table plus both mandatory curves, k and delta. Nothing new is calibrated in
2.2e. Expect the primary-margin power floor from 2.2b to still bite, since the
margin and the bootstrap are unchanged and the decidable region is a subset of
the population; if it does, Inconclusive is a permitted verdict and is used
rather than reached around.

---

## Pass 9, Phase 2.2d continued: Addendum 1a, and one deliverable outstanding

**Date:** 2026-09-18. **Branch:** phase-2. Nothing run, nothing measured.

**Two edits were requested. One is applied, one is blocked on missing input.**

### Edit A, applied: resolution 5 replaced by Addendum 1a

Resolution 5 of Amendment 1 tested "ADS is the stronger driver of decidability
than SV" by comparing the averaged range of the decided-winner rate across each
axis of the frozen 5 by 4 grid. That measure is biased toward the conclusion H2
needs. Range is an order statistic, so its expectation grows with the number of
values it is taken over, and the grid is not square: 5 ADS bands against 4 SV
bands. ADS entered the comparison with an edge that came from the grid shape
rather than from the data.

Replaced by a one-way variance decomposition over the eligible cells of the same
grid: `eta2_ADS = SS_ADS / SS_total` against `eta2_SV = SS_SV / SS_total`, both
ordinary one-way effect sizes over the same observations, so the comparison is
invariant to band count. The averaged-range test is kept verbatim as a **second
required condition**. ADS counts as the stronger driver only if it wins under
both. A split between the two measures makes the H2 role-separation clause
**Partial**, never Supported, and both pairs of numbers are reported in every
case.

Two choices inside the new measure were not specified and are fixed in the
addendum, with reasons.

- **Cells are unweighted**, one observation each. Block-weighting is computed and
  reported beside it but decides nothing, because the ADS = 1.0 row holds roughly
  three quarters of the primary analysis population and its low decidability is
  the part of H2 that Amendment 1 already concedes is partly structural.
  Weighting by blocks would give that single row decisive leverage over exactly
  the comparison H2 needs ADS to win, which is the same kind of tilt this
  addendum exists to remove.
- **Degenerate cases are Inconclusive**: zero total sum of squares, fewer than
  two levels of either factor holding an eligible cell, or fewer than four
  eligible cells in total.

The addendum also states what it does not fix. The ADS = 1.0 row still carries a
partly structural collapse and is still one of the five rows entering the
measure. Unweighting stops it dominating but does not remove it, and no variant
that deletes the row is pre-registered, because deleting it would test a
different hypothesis from the one H2 states. The H2 verdict and Amendment 1's own
statement that the top-band decline is guaranteed rather than discovered go in
the paper adjacent to each other.

Applied append-only, as instructed: Addendum 1a sits after Amendment 1, nothing
prior is overwritten, resolution 5 carries a one-line pointer, and the file's
revision history gained a dated entry.

### Edit B, not applied: the pre-registration-integrity subsection

**Blocked, and deliberately left undone.** The instruction was to add a required
Phase 2.5 deliverable to PLAN.md carrying supplied drafted text verbatim. The
paste came through as the literal placeholder
`[Paste the contents of posthoc-defense-deliverable.md here.]`, and no file of
that name exists anywhere in the repository; the only `posthoc` hits are Phase 1
archive artifacts under `data/outputs/experiments/exp1/`, unrelated and
read-only.

Not substituted with drafted text, because the point of the deliverable is that
it was written by the author blind to the 2.2e result. Text composed here, after
two passes of reading the results that motivate the defence, would be the exact
thing the deliverable exists to rule out, and calling it verbatim would be false.
It is recorded here as outstanding rather than silently dropped.

It does not gate 2.2e. It is a Phase 2.5 writing deliverable and can be added at
any point before the writing pass.

**Numbers produced:** none. **Invariant checks.** Invariant 5: no measurement,
and the addendum states in its own text that no mechanism B prediction on the
evaluation split exists. Invariants 2, 3, 6, 7: untouched by this pass. The three
module self-checks were re-run and pass.

**Artifacts.** `phase2/PREREG.md` (Addendum 1a, one pointer at resolution 5, one
revision-history entry).

**Recommendation for the next pass.** Supply the Edit B text, which can be folded
into any later commit, then run 2.2e. 2.2e is unchanged by this pass except that
it must now compute and report both decidability measures rather than one, and
must implement the unweighted decomposition as the deciding one with the
block-weighted variant beside it as a reported diagnostic.

---

## Pass 10, Phase 2.2d closed: the pre-registration-integrity deliverable locked

**Date:** 2026-09-18. **Branch:** phase-2. Nothing run, nothing measured.

**What this pass did.** Applied Edit B, the one item Pass 9 left outstanding for
want of its supplied text. `phase2/PLAN.md` gains a new section, "Required Phase
2.5 deliverable: pre-registration-integrity subsection", carrying the
author-supplied draft verbatim between explicit BEGIN and END markers, and the
2.5 bullet in the phase list now points at it. Phase 2.2d is closed.

**Provenance, which is the point of the deliverable.** The text was drafted by
the author during Phase 2.2d, blind to the 2.2e result, and locked on 2026-09-18
before 2.2e ran. It is marked in PLAN.md as not to be softened or strengthened by
what 2.2e returns. The lock cuts both ways and the section says so: a later pass
that finds the defence inconvenient does not get to soften it, and a later pass
that finds the result flattering does not get to strengthen it. Reproduced
without reflowing, editing or paraphrasing; drafting changes belong in the
manuscript pass, worked against this as the source.

**Why a locked defence is worth more than a written-later one.** The hypotheses
were amended after two passes returned results, which is post hoc and a reader is
entitled to say so. A defence of an amendment composed after seeing the outcome
it defends is worth less than one composed before. This one was composed before,
and the repository timestamps show it: the deliverable is committed on the same
branch as, and before, any 2.2e artifact exists.

**Two wording checks recorded beside the text, and deliberately not applied to
it.** Both are questions against the repository record rather than disagreements
with the argument, and both are noted in PLAN.md under the deliverable as
additions to its own fill-at-writing checklist.

- **"amended once."** `PREREG.md` carries two dated appends, Amendment 1 and
  Addendum 1a, both made during 2.2d and both before any 2.2e number exists. They
  are one amendment event in two documents, so "once" is defensible, but a reader
  who finds the second append should not have to reconstruct that for themselves.
- **"two exploratory runs."** 2.2b was the pre-registered run executing the 2.2a
  freeze, not an exploratory one. 2.2c was the exploratory calibration-split
  probe. The phrase may not say what it intends.

Neither was edited into the text, because the text is locked and because
resolving them is a writing-pass job against committed history. Recording them
rather than silently fixing them is the same discipline the deliverable itself
argues for.

**Numbers produced:** none. **Invariant checks.** Invariant 5: nothing measured,
and no 2.2e artifact exists. Invariants 2, 3, 6, 7: untouched. The three module
self-checks were re-run and pass.

**Artifacts.** `phase2/PLAN.md` (new required-deliverable section, amended 2.5
bullet).

**Recommendation for the next pass.** Phase 2.2d is closed with nothing
outstanding. Run 2.2e against `PREREG.md` Amendment 1 as revised by Addendum 1a:
implement mechanism B with its own assert-based self-check, confirm it reproduces
the 2.2c calibration counts of 546 rule wins against 744 at k = 5 as a regression
check on the implementation, then re-run the frozen analysis with the renamed
verdicts and report against the amended falsification table plus both mandatory
curves, k and delta, and both decidability measures. Nothing new is calibrated.

---

## Pass 11 — Phase 2.2e, the amended boundary experiment (2026-09-18)

**What I did and why.** Executed `PREREG.md` as amended by Amendment 1 and
Addendum 1a, on the primary population, exactly as frozen. Nothing was
re-tuned, re-banded or redefined: section 7 stays void, k is fixed by definition
at 5, the split and the SV and SV_resid band edges are the ones committed in
`phase2b_constants.py` at `5e13e38`, and the margins, the seeds and the
four-verdict rule come straight from the 2.2a freeze. Two new modules:
`phase2e_mech.py` for the mechanisms and `phase2e_run.py` for the analysis. The
2.2b code and its numbers are untouched.

**The regression check came first and cleared.** `phase2e_mech.py` implements
mechanism B independently of `phase2c_probe.py`, so that checking it against
2.2c is a check and not a restatement. Run on the calibration split alone, it
reproduces the frozen 2.2c counts exactly at every k on the curve: 181/736 at
k = 2, 314/740 at k = 3, **546/744 at k = 5**, 912/748 at k = 10, with rule
accuracy 0.8234 identical across k and B's accuracy matching to four decimals.
`main()` asserts all of it, so no evaluation-split signature can be read until it
passes. It is also the first thing `phase2e_run.py` does.

**The pair is two-sided on the evaluation split, which is the thing 2.2b could
not produce.** `rule wins` measured **zero** for the retired pair on 199,713
signatures. For the amended pair, at k = 5, the rule is right and the vote wrong
on **3,025** test signatures against **4,012** the other way. Rule accuracy
0.8244 against k-NN 0.8294, pooled gap -0.0050. The rule's accuracy is identical
to 2.2b's exact-match accuracy to every digit, as it must be, since mechanism A
was not amended. Abstention sits entirely on the rule's side, 3.14% against the
vote's zero.

**Outcomes against the amended falsification table**, Inconclusive evaluated
first:

- **H1 Supported.** Spearman of train-only ADS with held-out accuracy 0.5069
  [0.4919, 0.5224] for the rule and 0.8298 [0.8190, 0.8401] for the k-nearest
  vote, both intervals clear of zero, positive in pooled non-inspire and in all
  four qualifying non-inspire datasets, so it generalizes. Still a
  construct-validity check, not a contribution.
- **H2 Inconclusive at all three margins.** The power floor is evaluated first
  and is not met: at delta = 0.05 no ADS band and no SV band has a decided
  pooled verdict, because every marginal pooled gap is smaller than the margin.
- **H3 Inconclusive at delta = 0.05 and 0.03, Partial at 0.02, so
  margin-dependent.** At 0.02 the ADS = 1.0 band clears the floor with three
  decided SV bands, and two ADS bands below 1.0 show a tie-crossing rather than a
  reversal.

**The sharpest measurement in the pass is a clause H2 lost.** Addendum 1a's
role-separation test says ADS must be the stronger driver of decidability under
**both** its measures. It is the stronger driver under **neither**: eta2_ADS
0.1749 against eta2_SV 0.3837, and averaged ranges 0.0707 against 0.0755. That
is not a split, it is a clean failure, and it holds at every margin on the
robustness curve and at every k on the mandatory curve. Dropping the structural
ADS = 1.0 row widens the gap rather than closing it, 0.1755 against 0.4594, so
it is not an artifact of the row Amendment 1 already conceded. The block-weighted
diagnostic, which decides nothing by pre-registration, is 0.3653 against 0.3765
and points the same way. H2's verdict is Inconclusive on the power floor, which
is evaluated first, so this does not decide the hypothesis. It does point against
the role assignment the 2.2d reframe adopted, and it is reported in those words.

**Three more things beside the verdict, none offered in place of one.**

- **The pooled gap changes sign on both axes.** Across ADS bands: +0.0334,
  +0.0215, +0.0123, -0.0028, -0.0278. Across SV bands: -0.0388, -0.0144, -0.0115,
  +0.0189. At delta = 0.02 the ADS ordering becomes a decided marginal reversal,
  `rule wins` in [0, 0.5) against `k-NN wins` at ADS = 1.0. Both design-time
  signals carry winner-identity information.
- **The decidability gradient is not monotone and does not approach zero at
  ADS = 1.0.** The marginal decided-winner rate runs 0.1083, 0.0618, 0.0256,
  0.0089, then **rises** to 0.0278 in the top band, which holds 10,537 of the
  13,902 primary-population blocks. Amendment 1 predicted it would approach zero
  there. The reason it does not is the amendment's own structural argument: at
  ADS = 1.0 the rule can only differ by abstaining, and where it abstains often
  the vote wins by a decidable margin.
- **No SV-driven winner reversal anywhere below ADS = 1.0, at any margin.** The
  strongest structure below the top band is a tie-crossing at delta = 0.02.
  Substantively the shape is the pre-registered gap-compression one. The frozen
  rules make that a hypothesis outcome only above the power floor, which the
  primary margin does not clear, so it is reported as substance.

**One pre-registration ambiguity, found at run time, reported rather than
improvised.** Amendment 1's H2 Supported row requires the decided-winner rate to
be "strictly lower in the top ADS band than in the bottom". That admits two
constructions, within each eligible SV band or on the marginal ADS bands, and
here they disagree: 2 of 4 usable SV bands, so no majority, against True
marginally. Both are computed and printed in the H2 facts, neither was picked
after seeing which way it fell, and the disagreement changes no outcome because
H2 is Inconclusive on the power floor. Recorded so the construction can be fixed
before it can matter.

**Robustness and diagnostics, all pre-registered, all run.** The Jaro-Winkler
arm reproduces the same picture, pooled gaps -0.0388, -0.0146, -0.0116, +0.0181
across SV bands with the same verdicts. SV_resid shows the same shape at smaller
magnitude, -0.0124, -0.0025, -0.0025, +0.0130, and no reversal. The k curve, the
delta curve, the mechanism agreement rate per SV band, the INIT stratification,
the power-by-test-set-size report and the per-dataset and pooled non-inspire
tables are all in the report. H1 holds in all seven datasets.

**Numbers produced.** 13,902 primary-population blocks, 197,479 test signatures,
unchanged from 2.2b because the split is unchanged. Key files:
`reports/phase2e_boundary.md` (the report), `reports/tables/phase2e_*.csv` (26
tables), `reports/figs/phase2e_*.png` (10 figures). The regression check is
`reports/tables/phase2e_regression_check.csv`.

**Invariant checks.** Invariant 2: the winner is defined only by labelled
accuracy; neither ADS nor SV nor SV_resid appears in either mechanism, verified
by inspection of `phase2e_mech.py`, which takes only forms and labels.
Invariant 3: `verify_no_leakage` ran and passed, confirming the calibration and
evaluation block sets are disjoint and partition the 18,984 live blocks, the
frozen `n_train` rule is applied to every live block, and ADS and SV recompute
train-only on a 300-block sample. Invariant 5: every number in the report is
produced by the committed scripts; the report is regenerated end to end from
them. Invariant 6: two mechanisms, neither trained. Invariant 7: offline,
CPU-only, deterministic, no API call. Both new modules carry assert-based
self-checks that pass (`phase2e_mech.demo`, `phase2e_run.demo`), and
`phase2e_run.demo` pins the eta-squared decomposition against hand-computed
answers, including the band-count invariance that is the whole reason Addendum 1a
replaced the range test.

**Two implementation notes worth keeping.** The Addendum 1a degenerate case is
"SS_total is zero", and on a perfectly flat grid floating point leaves it at
about 6e-32 rather than 0, which would have read as a decided clause with
eta2 = 1.0 on both axes. It is compared against a tolerance of 1e-18, which sits
far below the roughly 1e-8 that the smallest real between-cell difference can
produce. Separately, `structural` and `gradient_clauses` build their frames with
explicit columns, because a small per-dataset population can have no eligible
band at all and an empty frame with no columns broke the first run.

**Recommendation for the next pass.** Do not start 2.3 yet. This pass returns
Inconclusive on both substantive hypotheses at the primary margin, and the one
clause that directly tested the two-signal role assignment came out against ADS
under both of its required measures, stably across k and delta. Three things
belong to review, in this order. First, whether the primary margin is the right
one, given that the pair is now two-sided and every marginal pooled gap falls
below it; the delta = 0.02 column is where this data has structure, and moving
the primary margin after seeing that is exactly the move the pre-registration
exists to prevent, so it is a decision to take explicitly and to record, not to
slide into. Second, whether the paper identity survives result 3 above, since
PLAN.md's identity paragraph and the charter mission both assert a role
separation that this pass measured pointing the other way. Third, only after
those, whether 2.3 proceeds, and with which baselines. The locked Phase 2.5
pre-registration-integrity subsection needs no change: it was drafted blind and
its argument is unaffected by an Inconclusive result.

---

## Pass 12 — Phase 2.5a, writing setup and outline (2026-09-18)

**What I did and why.** Rewrote the paper identity in the working documents to
the result 2.2e actually returned, then built the manuscript outline. No
manuscript body text was drafted and nothing was measured. `PREREG.md` was not
opened for editing: it stays frozen with Amendment 1 and Addendum 1a intact, as
the record of what was fixed in advance.

**The identity that was retired.** The two-signal role separation, consistency
gating whether the mechanism choice is live and surface stability directing it
where it is. It was removed from all four places it lived, not softened and not
kept as a secondary claim: `phase2/CLAUDE.md` mission, `PLAN.md` paper identity,
`PLAN.md` working titles, and `phase2-spec.md` sections 1 and 3. The reason is
the one clause that tested it. Addendum 1a required ADS to be the stronger
driver of decidability under both its measures, and 2.2e found it the stronger
driver under neither, at every k and every margin.

**The identity that replaces it.** A pre-registered negative result:
design-time mechanism selection for author name disambiguation has no signal a
designer can act on. Two halves, and the structural half is the sharper
contribution.

- **Structural.** Exact match is a strict sub-case of single-nearest retrieval,
  so the naive rules-versus-fuzzy comparison cannot contest a winner at any
  cutoff, in any metric family. Measured at 2.2b as zero `exact wins` out of
  199,713 test signatures in both metric arms, then generalized at 2.2c to any
  pair of mechanisms that assigns an author from the block's own history: no
  precision-first rule can win where the history names one author, and none can
  win where the history is written one way.
- **Empirical.** With the two-sided pair, the mechanisms barely differ (pooled
  0.8244 against 0.8294), the gap compresses weakly with surface stability and
  never reverses below ADS = 1.0 at the primary margin, and neither signal
  robustly predicts which mechanism to use. H2 and H3 Inconclusive because the
  pre-registered margin is wider than every effect on both axes.
- **What it retroactively explains.** The Phase 1 synthetic result reported a
  winner that was a constant function of the lexical condition and a consistency
  signal blind to it. That is the shape a nested pair returns by construction.
  The outline carries this as an interpretation of our own published result in
  discussion section 8.3, explicitly not as a new measurement.

**The outline.** `phase2/reports/OUTLINE.md`. Ten sections, each with a
one-sentence spine and a word budget, subsection budgets for the five largest,
and a total of **8,100 body words plus a 250-word abstract**, leaving about
1,600 words of headroom under the 10,000 total for captions and references. It
adapts `phase2-spec.md` section 10 to a methodological-and-null paper, and that
section now carries a banner pointing here. The structural result gets its own
section (4, 650 words) rather than sitting inside related work or results, which
is the main structural change from the old skeleton. Section 6.4 reproduces the
locked pre-registration-integrity subsection from PLAN.md and is marked "not
drafted, reproduced", with its own fill-at-writing checklist plus the two
wording checks recorded at lock time.

**The figure and table plan.** Six tables and five figures out of the 26 analysis
tables and 10 figures that 2.2b, 2.2c and 2.2e produced. Tables: population
accounting; two-sidedness across k with the 2.2b zero beside it; per-dataset
accuracy and coverage; marginal pooled gap and verdict by ADS and by SV; the
Addendum 1a driver comparison; the falsification table evaluated with margin and
k sensitivity. Figures: H1 accuracy against ADS, the 5 by 4 gap grid, the
decidability gradient, verdict share by test-set size, and the k curve. H1 keeps
a main-text figure deliberately: without it the null reads as a dead experiment
rather than as prediction working and selection failing. Everything else is named
as a supplementary pointer to its committed file, including the SV_resid,
Jaro-Winkler and INIT arms, which are reported as numbers in section 7.5 instead.

**Title candidates.** Six, sentence case, in PLAN.md and OUTLINE.md with merging
notes. Anything containing "cascade", "selector", "gating", "role" or
"two-signal" was deliberately avoided, since all of them name the retired
framing.

**Writing constraints recorded in OUTLINE.md**, per instruction, so they govern
every 2.5 session and not just this one: plain English and short concrete
sentences, sentence-case headings, no em dashes, venue-neutral LaTeX, honest
framing with no overclaim, every number traceable to a committed table, and the
`/anti-ai` pass held back as a dedicated 2.5c session rather than applied during
drafting.

**Invariant checks run, and their results.**

- **Invariant 5, no result before measurement: pass.** Nothing was computed this
  pass. Every number written into the rewritten identity and into OUTLINE.md was
  copied from a committed report or table. Spot-verified three of them directly
  against the CSVs rather than against the prose: `phase2e_twosidedness_eval.csv`
  gives 3,025 / 4,012 at k = 5 Levenshtein, `phase2e_driver_comparison.csv` gives
  eta2_ADS 0.17489 against eta2_SV 0.38373 with averaged ranges 0.07072 against
  0.07549, and `phase2e_accuracy_by_population.csv` gives 0.82444 against 0.82944
  over 13,902 blocks and 197,479 test signatures.
- **`PREREG.md` frozen: pass.** Not in the diff. Amendment 1 and Addendum 1a
  unedited.
- **The locked Phase 2.5 deliverable untouched: pass.** No line of the PLAN.md
  deliverable block appears in the diff.
- **Read-only paths respected: pass.** `git status` shows four modified files,
  all under `phase2/`, plus the new `phase2/reports/OUTLINE.md`. `phase1-archive/`
  and `manuscript/` were read for the retroactive-explanation paragraph and not
  modified.
- **No em dashes: pass.** Zero in all five touched files.
- **Budget arithmetic: pass.** Section budgets sum to 8,100 and every subsection
  list sums to its section total.

**What I did not do, and why.** `phase2-spec.md` sections 7 and 9 still describe
the selector protocol and the old success-partial-failure criteria. They were
outside the instruction's scope for this pass, so they are flagged in OUTLINE.md
open input 3 and in STATE.md rather than rewritten. Charter invariants 4 and 6
also still assume a selector may be built; that depends on whether 2.3 runs at
all, which is review's call. The primary margin was left at delta = 0.05,
because moving it after seeing that delta = 0.02 is where the structure lives is
exactly the move the pre-registration exists to prevent.

**Recommendation for the next pass.** Review `reports/OUTLINE.md` and the
rewritten identity, and settle the four open inputs OUTLINE.md lists, in
particular whether delta = 0.05 stays primary and whether 2.3 and 2.4 happen at
all. Then Phase 2.5b, drafting, in the order OUTLINE.md's last section gives:
sections 4, 5 and 6 first, then 7, then 3, 8 and 9, then 1 and 2, then the
abstract. The one thing worth deciding early is whether section 4 can be made to
land as a contribution in its own right. If it cannot, the paper is thinner than
this outline assumes, and that is better known before 8,000 words exist.

---

## Pass 13 — Phase 2.5b, drafting the manuscript body (2026-09-18)

**What and why.** The drafting pass. `reports/OUTLINE.md` was executed as
written, in the order its last section fixes: sections 4, 5 and 6 first, then
7, then 3, 8, 9 and 10, then 1 and 2, then the abstract, then one budget trim
over the whole draft. Venue-neutral LaTeX, generic `article` class, no journal
style file. The `/anti-ai` pass was deliberately not run; that is 2.5c and is a
separate session by design. Nothing was measured this pass.

**Where the manuscript lives.** `phase2/paper/main.tex` and
`phase2/paper/references.bib`. Built with pdflatex and bibtex into the session
scratchpad, not into the repository. 24 pages, no undefined citations or
references, no em dashes anywhere.

**Seven commits, one per drafting block plus the banners:**

- `cb06770` sections 4, 5 and 6, plus `references.bib`
- `dfa3831` section 7, results
- `672839e` sections 3, 8, 9 and 10
- `4a10f00` sections 1 and 2
- `9ebc341` the abstract
- `925bcb7` the budget trim over the whole draft
- `8dc3c14` the four superseded-selector banners, not manuscript

**The eight drafting instructions, and what each produced.**

1. **Section 4 states that the degeneracy was found by running a full
   pre-registered analysis before it was understood.** Section 4.2 opens on it
   and closes on it: it was found by looking at an empty cell in the output of
   the full frozen analysis, and it survived a pre-registration careful enough
   to fix a deterministic tie-break chain for both mechanisms. The general form
   is 4.3 and is framed as a trap with a one-count check, not as a theorem.
2. **Section 1 carries a page-one practitioner statement.** End of 1.3, three
   sentences: check the pair is not nested by counting the items where each is
   right and the other wrong, expect the choice not to matter and decide on
   cost where it does not, and measure your data to learn how hard it is rather
   than what to build. Repeated as the closing paragraph of section 10.
3. **Section 3 justifies the two untrained lookups as a scoping choice.**
   Section 3.1, third paragraph, with three reasons: the design-time budget
   question, the need for the pair to sit inside the rules-versus-retrieval
   family the structural result is about, and holding training budget and model
   class fixed so a winner difference cannot be a spending difference. Kim and
   Kim's per-block oracle-tuned comparison is named as carrying exactly that
   confound. Section 9 still carries the scope as a limitation, pointing back
   at 3.1.
4. **Section 8.3 reinterprets the Phase 1 result with care.** Zenodo concept
   DOI `10.5281/zenodo.21644207` cited as `adscascade2026`. Three labelled
   paragraphs separate what was an artifact of the pair (the constancy of the
   winner), what stands (the accuracy prediction, reproduced here as H1), and
   what is intact but narrower (the widening margin). Framed as a limitation
   the near-nested design imposed, stated as an interpretation of a published
   result rather than a new measurement, and explicit that the containment
   there is close rather than exact, because the two-stage company-then-global
   fallback and tie-breaking are the two ways the rules arm could differ in its
   own favour.
5. **The logical negative control is section 7.7.** No cell of the frozen 5 by
   4 grid carries a decided pooled verdict at the primary margin, eighteen of
   twenty being demonstrated ties and two undecided, so a selector reading ADS
   and SV routes only inside demonstrated ties. No selector experiment is run
   and none is reported. Stated as a claim about the pre-registered margin and
   not about the underlying gaps.
6. **Every count traces to a committed 2.2e table.** The 2.2b numbers appear in
   exactly two places, section 4.2 and the retired-pair row of table 2, both
   labelled with their own population. 2.2b's per-block verdict counts are not
   in the paper at all.
7. **Section 6.4 reproduces the locked deliverable.** Verbatim, inside a
   `quote` block, its argument untouched. Its fill-at-writing checklist is
   worked through after it as three labelled points of record.
8. **Verdicts come from the frozen table.** Section 7's preamble says so, and
   7.5 and 7.6 open by labelling their contents as substance. "Inconclusive
   means the frozen rules declined to decide; it is not a finding that the
   effects below the margin are absent" is stated in 7.4 in those words.

**The fill-at-writing checklist, worked against the committed repository.**

- **Commit ids confirmed.** `8869b82` freezes `PREREG.md`; `5e13e38` freezes
  the calibration constants; `3d86959` is the 2.2b run; `c20239a` is the 2.2c
  probe; `5f452ad` and `3e79a48` are Amendment 1 and Addendum 1a; `9e3d921` is
  the 2.2e run. All seven are in the footnote to section 6.4.
- **The amendment-predates-run claim confirmed against timestamps.** Amendment
  1 at 12:36:16 and Addendum 1a at 13:04:42, against the 2.2e run commit at
  14:25:07. Just under two hours and about eighty minutes respectively, all on
  2026-09-18. `5e13e38` at 10:46:50 precedes the 2.2b run at 11:43:11.
- **"Amended once" resolved.** The paper says the repository holds two dated
  appends, names what each did, states that both precede the run they govern
  and were committed within half an hour of each other, and calls them one
  amendment event in two documents.
- **"Two exploratory runs" resolved.** The paper says the first was not
  exploratory but the pre-registered run executing the frozen text, and the
  second was the calibration-split design probe. The locked text is unchanged;
  the correction sits beside it.

**Invariant checks run, and their results.**

- **Invariant 5, no result before measurement: pass.** Nothing was computed
  into the manuscript. Every number was copied from a committed report or
  table. Two were re-verified directly against the committed data rather than
  against prose, by reading `phase2e_blocks_scored.csv.gz` and
  `phase2b_blocks_scored.csv.gz`: the 2.2e per-block verdicts at k = 5 and
  delta = 0.05 are 191 rule wins, 309 k-NN wins, 10,172 tie and 3,230
  undecided, giving 500 decided, exactly as the paper states; the 2.2b
  distribution is 0 / 298 / 11,117 / 2,487.
- **A transcription error found and fixed in STATE.md.** STATE.md recorded
  2.2b's per-block verdicts as "302 fuzzy wins ... 2,483 undecided". The
  generated report and the committed blocks table both give 298 and 2,487.
  STATE.md was the hand-written copy and was wrong; it is corrected this pass.
  No report, table or paper number changes, because the paper never carried
  2.2b's per-block counts.
- **`PREREG.md` frozen: pass.** Not in any diff this pass.
- **The locked PLAN.md deliverable untouched: pass.** Not in any diff. It is
  quoted into the manuscript, not edited in place.
- **Read-only paths respected: pass.** `manuscript/main.tex` and
  `manuscript/references.bib` were read for section 8.3 and for the
  carried-over bibliography entries, and not modified. Everything written is
  under `phase2/`.
- **No em dashes: pass.** Zero in `main.tex` and zero in the two files given
  supersession banners.
- **Builds: pass.** pdflatex, bibtex, then two more pdflatex passes. 24 pages,
  zero undefined citation or reference warnings.

**Budget, and the one thing that is off target.** The body is 9,181 words
against the outline's 8,100, with the abstract at about 290 and captions at
about 400, so roughly 9,900 against the charter's 10,000 ceiling. Under the
ceiling, but with less headroom than the charter asks for. The trim pass
already removed 492 words of genuine duplication between sections 3 and 6 and
inside section 1. What remains is spread across section 6, where the locked
deliverable alone is 400 words that cannot be cut, section 4, which the
instructions asked to expand, and section 7, which gained 7.7. Flagged rather
than fixed by further shaving, because 2.5c is a tightening pass and can take
it down properly.

**Citations, stated plainly.** `references.bib` carries three verification
tiers as comments. Block A is carried over from the Experiment 1 citation
audit. Block B, Kim and Kim 2020, was verified at 2.2a against the source
itself. Block C is not verified and every entry says so in its own `note`
field: S2AND, WhoIsWho, the AND survey, Backes 2018, Hand 2009,
Hernandez-Orallo et al. 2012, Vickers and Elkin 2006, Elmachtoub and Grigas
2022. **Tan (2026) is a placeholder with no bibliographic details anywhere in
the repository**, so the sibling-framing paragraph that PLAN.md and the spec
both describe was not drafted; a TeX comment in section 2.1 says why and what
to do. Either verify it in full at 2.5c or drop the framing.

**The superseded-selector banners.** Four places still described the retired
selector as live and now carry dated banners with their original text kept:
`phase2-spec.md` sections 7 and 9, charter invariant 4, and the last clause of
charter invariant 6. All four become live again unchanged if review decides
2.3 runs. OUTLINE.md open input 3 is closed by this.

**What I did not do, and why.** No `/anti-ai` pass, by instruction; that is
2.5c. No citation verification sweep, which the charter requires and 2.6
schedules; the unverified entries are flagged per entry instead. The primary
margin was left at delta = 0.05 and the paper is drafted against it, with the
delta = 0.02 structure reported as the robustness curve and named in section
8.1 as the caveat that changes a reader's takeaway. Open inputs 1, 2 and 4 in
OUTLINE.md are still open; only 3 is closed.

**Recommendation for the next pass.** Review the drafted sections against the
committed reports, not against this narrative. The three places most worth an
independent read are section 4, because the whole paper rests on it landing as
a contribution; section 6.4 and its three points of record, because that is
the integrity argument and it has to survive a hostile read; and section 8.3,
because it reinterprets published work of the author's own and the line
between artifact and standing result has to be exactly right. Then settle
OUTLINE.md's remaining open inputs, in particular whether Tan (2026) stays.
After that, 2.5c: the anti-AI pass, the citation verification sweep, and the
trim from 9,181 body words toward 8,500.

## Pass 14 — Phase 2.5c, two correctness fixes and the /anti-ai pass (2026-09-18)

**What I did and why.** Two targeted fixes first, then `/anti-ai` over the
manuscript prose, then the budget trim OUTLINE.md prescribes. Nothing was
measured, no analysis code ran, and `PREREG.md` was not touched. The only
file changed is `phase2/paper/main.tex`.

**Fix 1, the population attribution of the pooled gap.** Section 4.2 said the
gap of `-0.0196` was "over the primary analysis population", then supported it
with coverage figures (0.9664, 0.9985) and an agreement rate (0.9679) taken
from the whole evaluation split, and the Table 2 caption said the retired
pair's whole row covered the full evaluation split. Checked against the
committed tables:

- `reports/tables/phase2b_accuracy_by_population.csv` row
  `all (primary population)`, 13,902 blocks and 197,479 test signatures:
  exact 0.8244420925769322, fuzzy 0.8440694959970427, gap
  -0.019627403420110493, exact coverage 0.9685586821889922, fuzzy coverage
  0.998794808561923, agreement 0.9697638736270692. So **-0.0196 is a
  primary-analysis-population number**, and the coverage and agreement
  figures that belong beside it are 0.9686, 0.9988 and 0.9698.
- The 0.9664 / 0.9985 / 0.9679 triple comes from `section_domination` in
  `phase2b_run.py`, which runs over `bk_all`, the **whole evaluation split**
  of 16,136 blocks and 199,713 signatures. That is also the population the
  zero `exact wins` count is measured on.

Section 4.2 now opens by naming both populations, gives the zero on the
evaluation split, and gives the gap, the accuracies, the coverages and the
agreement rate together on the primary analysis population. The
agreement identity still holds to every printed digit there:
0.9686 + 0.0012 = 0.9698. The Table 2 caption now says the retired pair's
zero was counted over the whole evaluation split and that every accuracy and
gap in the table, the retired pair's included, is on the primary analysis
population. No number was altered; two were swapped for the same quantity on
the population the sentence is about.

**Fix 2, section 8.3.** "The two-stage company-then-global fallback the arms
shared" now sits in its own sentence and is scoped in one clause as an
invoice-domain lookup that tries the issuing company's own history before the
whole corpus. A reader of an author-name paper no longer meets an unexplained
company.

**The `/anti-ai` pass, 22 prose edits.** Use case is academic manuscript, so
formal register, passive voice in methods and justified statistical hedging
were left alone. What the audit actually found, and what was done:

- **"rather than" 31 times**, roughly one per 300 words and the draft's
  dominant construction. It is the academic register's negative parallelism.
  Cut to 20, of which 2 are inside the locked quote and untouchable and the
  rest carry real contrasts ("measured rather than manipulated", "close
  rather than exact", "failed rather than splitting").
- **A self-congratulating honesty refrain**: "we say so rather than letting a
  seven-dataset label stand for it", "we say so plainly rather than treating
  Inconclusive as evidence of absence", "reported rather than worked around",
  "reported rather than improvised", "checked against the committed
  repository rather than against memory", "we state the consequence in the
  plainest available words", "reasons rather than excuses". All rewritten to
  the direct statement. The paper still says every one of these things; it
  stops narrating its own virtue while saying them.
- **Rule of three.** Dropped "for three reasons in order of weight" in 5.1
  and the "the message fits in three lines" triad in 1.3, which was a
  near-verbatim duplicate of the closing triad in section 10.
- **Compulsive summary.** Section 10 opened "Four things are on the record"
  and then restated all four claims chronologically, the fourth of them
  already stated in the same section's first paragraph. Replaced with a
  synthesis that separates the structural half from the empirical one.
- **Duplicated paragraphs.** 3.1's "A designer stands after the history"
  restated 1.1 almost sentence for sentence; 4.3 ended with the
  report-it-in-the-design-section advice that 8.2 gives again. Both cut once.
- One intensifier, "Crucially we measure it rather than set it", replaced.
- Zero em dashes in prose, unchanged. The only `---` are two "not
  applicable" table cells, which are table cells and out of scope for this
  pass. Sentence-case headings unchanged.

Burstiness was already fine and was not manufactured: 458 sentences, mean
20.0 words, sd 11.2, 84 sentences under ten words and one over sixty.

**The budget trim, per OUTLINE.md's order.** Section 2.3, algorithm
selection, is cut entirely. Its three citations survive in 1.1 and 8.2, which
both use the combined `\citep{rice1976, smithmiles2009, barbudo2023}`; the
portfolio assumption it set up is stated in 8.2 and the structural
consequence in 4.3; nothing `\ref`s `sec:algsel`. Section 7.3's prose is cut
to what Table 3 cannot say for itself; the table, its caption and every
number in it stay, so the mandatory per-dataset reporting is intact. Five
numbers lost a second appearance in 7.3's prose (0.1131, 0.2466, 34, 0.0163,
0.0631) and all five are still in Table 3.

**Word count, stated against my own counter so the delta is honest.** My
counter reads about 190 words higher than 2.5b's on the same file, so absolute
numbers here are not comparable to the 9,181 in Pass 13.

| | before this pass | after |
| --- | ---: | ---: |
| body | 9,374 | 9,157 |
| abstract | 290 | 290 |
| captions | 434 | 462 |
| prose total | 10,098 | 9,909 |

Body is down 217 words and the prose total is under 10,000, but **the body is
still around 9,150 against the 8,500 target and OUTLINE.md's 8,100 budget**.
The overrun now lives in section 6 (1,738 against 1,100, of which 400 is the
locked deliverable), section 7 (1,769 against 1,600), section 8 (1,250
against 950) and section 4 (1,021 against 650). Those are the three sections
STATE.md sends to review as the ones whose landing has to be judged first, so
this pass did not cut into them. That is a decision for review, not for a
prose pass.

**Invariant checks.**

- **The locked 6.4 quote block: byte-identical, verified.** 1,985 bytes,
  compared programmatically against the pass baseline, not by eye. It is not
  in any replacement string.
- **No number, table cell, figure file, label, citation key or verdict word
  changed: verified programmatically.** Bag-of-tokens comparison against the
  baseline. Figure files unchanged, all 5. Verdict words unchanged, all 7.
  The only diffs are the five 7.3 restatements above, the three `\citet` keys
  and the `sec:algsel` label that went with section 2.3, and the three `\ref`
  counts that moved with it.
- **No result before measurement: pass.** Nothing measured, no analysis code
  run, no report or table touched.
- **`PREREG.md` untouched: pass.** Not in the diff.
- **Read-only paths respected: pass.** Only `phase2/paper/main.tex` changed.
- **Builds: pass.** pdflatex, bibtex, three further pdflatex passes. **23
  pages, zero LaTeX warnings, zero undefined citations, zero undefined
  references.** Down from 24 pages.

**Four items flagged for 2.6, not fixed here, per instruction.**

1. **The Zenodo DOI.** `references.bib` gives `adscascade2026` the DOI
   `10.5281/zenodo.21644207` with a note that version 1.0.0 is at
   `10.5281/zenodo.21644208`. Which of the two is the concept DOI and which
   is the version DOI is unverified against Zenodo. Section 8.3 is the only
   place it is cited.
2. **Section 6.4's commit hashes: checked this pass, and they hold.** All
   seven resolve on `phase-2` and their subject lines match the roles 6.4
   assigns them, in the stated order. The timing claims check too:
   `5f452ad` 12:36:16, `3e79a48` 13:04:42, `9e3d921` 14:25:07 on 2026-09-18,
   so the amendment is 1h49m before the run ("just under two hours"), the
   addendum 1h20m before it ("about eighty minutes"), and the two appends
   28 minutes apart ("within half an hour"). What is left for 2.6 is to
   re-check them if the branch is ever rebased, since they are short hashes
   in published text.
3. **Tan (2026): verify or drop.** Unchanged from 2.5b. Still a placeholder
   with no bibliographic details anywhere in the repository, still named as
   the paper's sibling in framing by PLAN.md and `phase2-spec.md` section 1,
   still absent from section 2.1 with a TeX comment saying why.
4. **The author affiliation line.** `\author{Maitreya Sapariya\thanks{ORCID
   0009-0003-9346-3775.}}` carries an ORCID and no affiliation. Needs a
   decision before submission.

**Recommendation for the next pass.** Review the prose changes against the
diff, particularly section 4.2, where the two populations now have to read as
a clarification and not as hedging, and section 10, where the recap became a
synthesis. Then decide the body-length question, because it is the one thing
2.5c could not settle alone: either accept about 9,150 body words, or say
which of sections 4, 6, 7 and 8 may be cut into, since all four are over
budget and three of them are the sections review was asked to judge. Then
2.6: the citation verification sweep over `references.bib` block C, the four
items above, and the `affiliation` column question the S2AND README raises.

## Pass 15 — Phase 2.6, the pre-submission gate (2026-09-21)

**What I did and why.** Housekeeping, the verified bibliography, one prose fix
for a scope risk the final title opens, and a moderation audit reported rather
than acted on. Nothing was measured, no analysis code ran, `PREREG.md` was not
touched, and no number or verdict in the manuscript changed. Files changed:
`paper/main.tex`, `paper/references.bib`, `PLAN.md`, `phase2-spec.md`,
`reports/OUTLINE.md`, `.gitignore`, this file and `STATE.md`. One file added:
`reports/phase2_6_moderation_audit.md`.

**Housekeeping, five items, all now closed.**

1. *The author affiliation.* `\author{}` carried an ORCID and no affiliation.
   Set to `Independent researcher. ORCID 0009-0003-9346-3775.` No affiliation
   for the author exists anywhere in the repository, including `CITATION.cff`,
   which also carries only the ORCID. **This is a default I chose, not a fact I
   verified, and the author should confirm or replace it.** No email was added;
   arXiv does not require one in the PDF.
2. *Tan (2026) sibling framing removed* from `PLAN.md` (the paper-identity
   section) and `phase2-spec.md` (sections 1, 2 and 10). Each removal leaves a
   dated one-line note saying what was cut and why, per the project's
   keep-the-record convention. `phase2d-prereg-revision.md` and `PREREG.md`
   mention it too and were deliberately not touched: they are frozen records.
   The manuscript never cited it; the TeX comment in section 2.1 holding its
   place is gone.
3. *Em-dash "not applicable" table cells.* Three cells, `---` to `n/a`: one in
   Table 2 (the retired pair's absent B-right-A-wrong count) and two in Table 6
   (the block-weighted diagnostic's absent ranges). These were the last two
   em dashes in the manuscript; the charter forbids them and a bare rule in a
   numeric column reads as a missing value rather than as an inapplicable one.
4. *Trailing period dropped from `\title{}`*, and from the final title as
   PLAN.md records it, so the two match byte for byte. arXiv's title field takes
   the string verbatim.
5. *Superseded banner on the candidate-title list* in `reports/OUTLINE.md`,
   above the six 2.5a candidates, carrying the final title and pointing at
   PLAN.md. The six are kept. OUTLINE.md open input 4 ("citations are
   unverified") is also closed, since this pass is the sweep it was waiting for.

**The verified bibliography.** `paper/references.bib` replaced with the file the
author delivered. Block C's eight entries now carry a DOI each, except
`hernandezorallo2012`, which carries the JMLR publisher URL, and four gained
page ranges. `whoiswho2023` changed title and venue, to the KDD 2023 paper
actually published. The header's three verification tiers are rewritten as
verified. `adscascade2026`'s note now names v1.1.0 at
`10.5281/zenodo.22258609` beside the concept DOI, which matches `CITATION.cff`.

**`tan2026` is gone**, replaced in the bib by a comment recording why: no
indexed citable record of it exists and the source carried "DOI pending, pages
pending". The placeholder entry, the section 2.1 TeX comment and the sibling
framing in PLAN.md and the spec all went with it. **No `\cite{tan2026}` ever
existed in the manuscript**, so nothing in the prose needed repair.

**Key check, cite keys against the bib.** 17 keys cited, 17 keys defined, exact
set equality: every cited key resolves and no entry is orphaned. Verified by
set difference in both directions before the build.

**The build.** `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`, `pdflatex` from a
clean directory. Zero undefined citations, zero undefined references, zero
`LaTeX Warning` lines. 24 pages, `paper/main.pdf`, 635 KB. Four typographic box
warnings carried over unchanged from `4416798`; a fifth is new and is in
`main.bbl`, an underfull line in the `adscascade2026` entry whose note the new
bib lengthened. Cosmetic, in the bibliography, not chased.

**The scope fix, sections 1.2 and 1.4.** The final title says entity
resolution; the empirical work is seven author name disambiguation datasets.
2.5d flagged those two subsections as where the scoping has to hold. It now
holds explicitly in both, and in the same terms.

- Section 1.2 opens with the split before the substrate is named: the
  structural half uses no property of names, so it is stated at entity
  resolution width; the empirical half is a measurement and is the author name
  disambiguation instance. The substrate paragraph then follows as what *that
  half* needs.
- Section 1.4 stops presenting the four claims as one list. Two are proven from
  the mechanisms alone and are entity resolution contributions, with the
  measured zero named as the instance that found them rather than as their
  support. Two are measurements on seven author name disambiguation datasets
  with one pair of untrained lookups, offered as evidence about that substrate
  and explicitly not as facts about entity resolution. The pre-existing
  boundaries paragraph follows and now says "the empirical claim is scoped to
  these two mechanisms and this margin".

Section 10's second paragraph already carried the same split and was left
alone; the three places now agree. Prose only, no new experiments, no number
touched.

**Cost of the scope fix: +198 body words**, measured on one counter across both
versions, so the delta is sound even though the absolute reads lower than the
Pass 14 counter. Prose total 9,770 on that counter, under the charter's 10,000
ceiling. The page count went 23 to 24. **The body-length decision 2.5c handed
up is still open and this pass made it slightly worse, deliberately, because
the fix was instructed and "unmissable" was the requirement.**

**The moderation audit ran, but not as a skill.** `arxiv-moderation-check` is
not installed and is not in this session's skill list; the plugin cache and
both skill directories were checked. The audit was done directly against
arXiv's own moderation criteria over the seven dimensions asked for, and its
findings are in `reports/phase2_6_moderation_audit.md`: ten findings, ranked,
plus an eighth section on endorsement that nobody asked for and that has the
longest lead time on the list. **Nothing it flagged was fixed, by
instruction.** Its two blocking findings, restated in STATE.md: the manuscript
cites seven short commit hashes and fifteen repository artifact paths and gives
no repository URL, while branch `phase-2` is not pushed to `origin`, so none of
it resolves for a reader; and `\graphicspath{{../reports/figs/}}` escapes the
submission directory and will not build under arXiv's AutoTeX.

**Invariant checks.** Invariant 5, no result before measurement: held, nothing
measured and no number altered. Invariant 7, offline and reproducible: held,
no network call and no new dependency. Invariant 8, honest framing: the scope
fix tightens it, and the affiliation is flagged as a chosen default rather
than presented as verified. The writing invariants: em dashes now zero in the
manuscript, headings still sentence case, and the body grew against a budget
that was already over, which is the one invariant this pass moved the wrong
way.

**What I did not do, and why.** Did not act on any moderation finding, by
instruction. Did not touch `PREREG.md`, `phase2d-prereg-revision.md` or the
Phase 1 archive. Did not resolve the body-length decision, the delta question,
the Zenodo concept-versus-version DOI check, or the S2AND `affiliation` column
question; the last two stay flagged. Did not push `phase-2`.

**Recommendation for the next pass.** Take the moderation findings in the order
the report ranks them. The two blocking ones are cheap and both have to land
before a first upload: push `phase-2` and put its URL in the manuscript, or cut
the hashes and paths; and flatten the figure paths for the arXiv tarball. Then
decide the affiliation, the generative-AI disclosure, and whether the body
length is accepted. Endorsement is the item with the longest lead time and is
worth checking before anything else is polished.

## Pass 16 — Phase 2.6b, submission-content edits (2026-09-21)

**What I did and why.** Acted on five of the ten findings Pass 15 surfaced,
using text the author supplied for the two that needed an author's words.
Content edits only. No commit history was rebased, squashed or altered, so the
seven short hashes in section 6.4's footnote are untouched and still resolve.
Nothing was measured, no analysis code ran, and `PREREG.md` was not touched.
Files changed: `paper/main.tex`, `.gitignore`,
`reports/phase2_6_moderation_audit.md`, this file and `STATE.md`. Files added:
`paper/figs/` with five PNGs, and `paper/main.bbl`.

**1. The affiliation, corrected.** Pass 15's "Independent researcher" was a
wrong default and is gone. `\author{}` now carries the Department of
Information Technology, A. D. Patel Institute of Technology (ADIT), Charutar
Vidya Mandal (CVM) University, New Vallabh Vidyanagar, Anand, Gujarat, India,
with `maitreyasapariya@gmail.com` as the corresponding address and the ORCID.
Checked against the supplied string word for word. The only typographic liberty
is `A.~D.~Patel`, which is the LaTeX idiom for initials: it renders as
"A. D. Patel" and stops the pair breaking across a line.

**2. The generative-AI disclosure**, as `\section*{Generative-AI disclosure}`
after the conclusion. The author's text is reproduced **verbatim**, verified
character for character by a script that normalizes whitespace and compares
against the supplied string: exact match, no paraphrase, nothing added.

**3. The data and code availability statement**, as
`\section*{Data and code availability}` before the disclosure. It names the
GitHub repository and states that the Phase 2 code and pre-registration will be
public there at release; it ties that repository to the commit history section
6.4 depends on; it gives the Zenodo concept DOI `10.5281/zenodo.21644207` as a
resolvable link; and it names S2AND, cites it, states the ODC-BY licence, and
says explicitly that nothing is redistributed and that the repository holds
only the download code and the manifest.

**4. The build is now self-contained, and this was verified the way arXiv will
test it.** The five PNGs are copied to `paper/figs/` and confirmed
sha256-identical to their sources under `reports/figs/`. `\graphicspath` is
`{{figs/}}`. `main.tex` contains no `../` anywhere.

**The verification that matters:** `main.tex`, `main.bbl` and `figs/` were
copied alone into an empty directory with no access to the repository, and
built there. All five `\includegraphics` resolved from `figs/`; zero undefined
citations, zero undefined references, zero LaTeX warnings after the third pass,
25 pages. That is an AutoTeX simulation, not an inference from the source.

**`main.bbl` is committed and explicitly not ignored.** Pass 15 was wrong to
gitignore it. `.gitignore` now carries a comment saying why it is exempt:
AutoTeX does not run BibTeX, so the `.bbl` has to ship. `main.aux`, `.blg`,
`.log`, `.out` and `.pdf` stay ignored.

**The figures now exist twice in the repository**, in `reports/figs/` and in
`paper/figs/`. Deliberate: `paper/` is now a self-contained submission
directory, which is worth 356 KB of duplication. `reports/figs/` stays the
generated output of `phase2e_run.py` and is the copy to regenerate.

**Post-edit checks, all run.** Zero undefined citations. Zero undefined
references. Zero LaTeX warnings. **Zero em dashes**, both the TeX `---` form
and U+2014. Source still pure ASCII, zero non-ASCII bytes and zero stray
control characters. Cite-key parity holds unchanged at 17 against 17, and all
22 `\texttt{}` artifact references still resolve locally. 25 pages, up from 24.

**Length, and a ceiling that is now effectively touched.** The body is
unchanged at 9,076 words on this pass's counter; the two back-matter sections
add 215. Back matter is conventionally outside a body budget, like references
and captions, which puts prose at 9,770. **Counted the other way, with back
matter inside, the prose total is 9,985 against the charter's 10,000 ceiling:
fifteen words of headroom.** Whichever convention review adopts, the practical
consequence is the same. Nothing further can be added to this manuscript
without cutting something, and the body-length decision 2.5c handed up is now
the binding constraint rather than a tidiness question.

**The audit report was updated rather than superseded.**
`reports/phase2_6_moderation_audit.md` keeps every finding's original text and
adds a dated 2.6b note to each one that moved, plus a status column. Five
closed (2, 3, 4, 7, and the endorsement position improved), one reduced but not
closed (1), four unchanged (5, 6, 8, 10) and one whose fix shape changed (9).

**The finding that did not close, and why it gates the upload.** Finding 1 is
reduced, not closed. The paper now names the repository, but `phase-2` is still
unpushed, so the seven hashes in section 6.4 and the availability statement's
promise both point at a repository that does not yet contain what the paper
says it contains. A reader following the URL today lands on `main`, which is
the Phase 1 project. **The manuscript must not be uploaded before that push
happens.** Adding the URL without the push moved the problem from silent to
stated, which is an improvement and is not a fix.

**New finding, from the affiliation itself.** The corresponding address is a
personal Gmail account, which is what the author asked for and is fine in
print. It matters only for the arXiv account: automatic endorsement keys off a
registered institutional email domain plus publication history, so a personal
address forecloses the automatic route and leaves the manual request.
Registering an `adit.ac.in` or `cvmu.edu.in` address with arXiv, independently
of what the paper prints, is now the cheapest item on the list. Recorded in the
audit report.

**Invariant checks.** Invariant 5, no result before measurement: held, nothing
measured and no number, verdict or table altered. Invariant 7, offline and
reproducible: held, no network call and no new dependency; the figure copies
are local. Invariant 8, honest framing: the availability statement's future
tense is deliberate and is flagged above rather than being allowed to read as a
present-tense promise. Writing invariants: em dashes zero, headings sentence
case, and the prose ceiling is now effectively reached, which is on the record.

**What I did not do, and why.** Did not push `phase-2`, tag it, or touch any
remote: out of scope and the author's call. Did not rebase, squash or amend
anything, by instruction. Did not act on findings 5, 6, 8 or 10, which are
metadata and licence decisions taken at submission time, not manuscript edits.
Did not cut anything to make room for the 215 new words; that is the
body-length decision and it is review's.

**Recommendation for the next pass.** 2.7, the peer-review dry run, can proceed
on the manuscript as it stands: nothing outstanding blocks a review read. Two
things are worth doing in parallel because they are slow and are not writing.
Push `phase-2` and tag the state section 6.4 describes, which closes finding 1
without touching a hash. And register an institutional email with arXiv, then
start the endorsement request for cs.DL, which has the longest lead time of
anything left.

---

## Pass 17 — Phase 2.7, the peer-review dry run (2026-09-21)

**What I did and why.** Ran the manuscript through a simulated external peer
review at Reviewer 2 severity, calibrated to a mid-tier (Q2 or Q3) information
science, information retrieval or scientometrics journal rather than to a named
venue, which is the realistic target class. This is a review pass only: the
manuscript was not touched, and no number, verdict, table or figure was
altered. The review treated `phase2/paper/main.tex` as an external artifact and
checked every number and claim it states against the committed reports, tables
and code rather than against the PASSLOG narrative, per the instruction held
over from 2.5c.

**Key output.** `reports/phase2_7_peer_review.md`, with the same content built
as `reports/phase2_7_peer_review.docx` for the skill's deliverable contract
(29 headings, 5 tables, validated with the skill's own validator). Eight major
comments, twenty minor, a general-rigor compliance table, a literature audit, a
venue-class assessment and a recommendation of **major revision needed**, with
no fatal flaw found.

**The eight majors, in one line each.**

1. The per-block winner construct is degenerate on small test sets. At one test
   signature the paired bootstrap is a point mass, so such a block can never be
   `undecided`: 278 of the 500 decided verdicts (55.6%) and 1,130 of the 10,172
   demonstrated ties come from blocks with one or two test signatures. This is
   the quantity H2's whole apparatus is built on.
2. Test-set size is the design-time signal that was never registered. It
   carries +0.0208 per log unit in the paper's own regression, it is readable
   from the history, and it splits the result: above 32 test signatures the
   vote wins **no** block and the rule wins 30, while pooled the vote is ahead.
3. The driver comparison, called the sharpest measurement in the run, is two
   point statistics over twenty unweighted cells with no interval, no size
   adjustment, and SS_total of 0.0401.
4. "Entity resolution" in the title is carried by an argument stated entirely in
   author-block vocabulary, and the reference list contains no entity resolution
   literature at all. Recommends either a retitle to the substrate or one
   non-AND demonstration of the zero count.
5. Section 6.4's locked quote says no k-nearest accuracy figure existed when the
   amendment was written. `phase2c_pair_twosidedness.csv` and
   `phase2c_pair_regimes.csv` were committed in `c20239a` 27 minutes earlier and
   contain exactly that, on the calibration split, including the per-cell grid
   whose shape the amended hypotheses go on to predict. `PREREG.md` states the
   properly scoped version; the manuscript quote drops the qualifier.
6. The pre-registration record is author-controlled, the whole cycle is thirteen
   hours of one day, and `phase-2` is still unpushed, so none of the seven
   hashes resolves for a reader.
7. Two winner reversals present in `phase2e_boundary.md` at delta = 0.02 are
   absent from the manuscript: across ADS at fixed SV high (line 455), and
   across SV inside INIT = 0 (line 537). The paper uses delta = 0.02 elsewhere
   when it supports the reading.
8. Accuracy accounting is incomplete: no ceiling for test signatures whose true
   author is absent from the history, no conditional precision for the rule
   (0.851 where it fires against the vote's 0.8294), and no justification for
   using accuracy rather than B-cubed or pairwise F.

**Verification done, with results.** Every headline number in the manuscript was
re-derived from the committed CSVs and reconciles: Table 1's arithmetic and all
six shares; the pooled and pooled-non-inspire accuracies rebuilt from the
per-dataset rows; the agreement identity in 4.2; the verdict sum
191 + 309 + 10,172 + 3,230 = 13,902; the H1 coefficients and intervals; every
band gap, verdict and decided rate on both axes; the twenty-cell distribution as
18 tie and 2 undecided; the driver table at all three margins plus both
diagnostics; the regression; the k curve; the 41% contested region as
14,680 / 35,732; the two lines of zeros in the calibration probe for all three
candidate pairs; the H1 per-band means against `phase2e_boundary.md` 110-113;
and all three section 6.4 commit intervals (1h48m51s, 1h20m25s, 28m26s).
**One claim the artifacts do not support as written**: the unqualified sentence
in the 6.4 quote, major 5 above. **Two omissions found**: majors 7 and 8. No
transcription error was found anywhere.

**Measured for the record.** Abstract 288 words; body 9,488 words excluding
float contents; per-section body counts Introduction ~1,010, Related work 774,
Problem setting 750, section 4 1,032, section 5 517, section 6 1,733, section 7
1,759, Discussion 1,286, Limitations 380, Conclusion 247; 6 tables, 5 figures,
11 captions, 17 bibliography entries.

**Invariant checks.** Invariant 5, no result before measurement: held, nothing
was measured and nothing in the evidence base was altered; the review reads the
frozen artifacts and writes only a report. Invariant 7, offline and
reproducible: held for the repository; the review itself made four general web
searches for the literature audit, all recorded in the report's audit log with
their URLs, and added no dependency and no code to `phase2/`. Invariant 8,
honest framing: the report is the hostile read the charter asks for and its
findings are recorded here unsoftened. Writing invariants: the manuscript was
not edited, so they are untouched.

**What I did not do, and why.** Did not fix anything in the manuscript, by
instruction: 2.7 produces the report and 2.7b decides what to accept. Did not
push `phase-2`, tag, or touch a remote. Did not re-execute any analysis code, so
the review verifies manuscript-against-artifact consistency and not the
correctness of the artifacts, except where code was read directly
(`phase2b_core.py:246`, which is where major 1 was confirmed). Consensus was
unavailable, so the literature audit used general web search and is indicative
rather than systematic; it is flagged as such in the report.

**Recommendation for the next pass.** 2.7b, apply the accepted review fixes.
The eight majors split cleanly into three kinds and the author decides which to
accept. **Re-analysis on existing records, no new data**: majors 1, 2, 3 and 8.
**Disclosure and reporting, prose only**: majors 5, 6 and 7. **A scope
decision**: major 4, retitle to author name disambiguation or earn the wider
word with one non-AND count. Take major 4 first, because a retitle changes what
the abstract and conclusion have to say and majors 2 and 5 both touch the same
paragraphs. Note the standing constraint: the prose total is at 9,985 against
the charter's 10,000 ceiling, so every accepted fix has to be paid for with a
cut, and the four over-budget sections are still 4, 6, 7 and 8. The two slow
non-writing items from 2.6b are unchanged and still worth starting in parallel:
push and tag `phase-2`, which major 6 now makes a review finding rather than a
tidiness item, and register an institutional email with arXiv for the cs.DL
endorsement request.

---

## Pass 18 — Phase 2.7b, the re-analysis of the frozen records (2026-09-21)

**What I did and why.** 2.7 produced eight majors and changed nothing. Four of
them, majors 1, 2, 3 and 8, are re-analyses on records that already exist, and
2.7's own handover said to run them together because three of them touch the
decided-winner rate. This pass runs all four in one module and reports them in
one place. No experiment was re-run, no split re-drawn, no constant re-tuned and
no frozen definition altered. `PREREG.md`, Amendment 1 and Addendum 1a are
untouched. The manuscript was not edited: prose is 2.7c.

New code `phase2/phase2_7b_reanalysis.py`, new report
`phase2/reports/phase2_7b_reanalysis.md`, eight new tables
`reports/tables/phase2_7b_*.csv`, two new figures
`reports/figs/phase2_7b_verdicts_by_blocksize.png` and
`phase2_7b_driver_bootstrap.png`. The module imports the frozen band, verdict,
pooled-bootstrap and eta-squared functions from `phase2b_core` and
`phase2e_run` rather than restating them, so a drift in any frozen definition
breaks this pass rather than silently producing a different number.

**The one result that changes a claim, flagged as the task asked.** Block size
produces **two decided pooled band verdicts at the primary margin**: blocks of
3 to 4 signatures at -0.1145 [-0.1286, -0.1007] and blocks of 5 to 8 at
-0.0712 [-0.0807, -0.0614], both `k-NN wins` at delta = 0.05. Neither ADS nor
SV produces a single decided marginal band, which is the fact that carried H2
and H3 to Inconclusive. Read alone this is a counter-example to "design-time
mechanism selection has no signal a designer can act on" stated without
qualification. Two measured qualifications sit beside it and both are in the
report. At fixed ADS the effect never changes sign: inside ADS = 1.0 every band
favours the vote, inside ADS < 1.0 every band favours the rule, and the
marginal reversal is composition, since 90.0% of the smallest band is ADS = 1.0
against 43.8% of the largest. And the decided small-block cells are an
abstention effect: the rule's coverage climbs from 0.8423 to 0.9827 across the
bands, and its precision where it fires exceeds the vote's accuracy in all seven
bands, 0.9370 against 0.9037 in the smallest. The scoping decision is the
author's and it is the same one major 4 asks for.

**No H1, H2 or H3 verdict moves.** H1 Supported, H2 Inconclusive, H3
Inconclusive at the primary margin. The power floor counts decided pooled
verdicts over ADS and SV bands, and this was checked rather than assumed on the
restricted population: 0 ADS bands, 0 SV bands and 0 of 20 grid cells are
decided at delta = 0.05 with blocks under 3 test signatures removed. The check
is an assertion in the code, so the prose cannot drift from it.

**Key numbers, by task.**

1. *Major 1, small-test-block sensitivity.* Restricting to n_test >= 3 keeps
   10,434 of 13,902 blocks (75.05%) and 191,852 of 197,479 signatures (97.15%).
   Size-1 stratum: 1,309 blocks, 14 / 165 / 1,130 / **0 undecided**, the zero by
   construction. Size-2: 2,159 blocks, 10 / 89 / 1,739 / 321. The two strata
   supply 278 of the 500 decided verdicts (55.6%) and 2,869 of the 10,172 ties
   (28.2%). Restricted, the per-block margin flips from 191 rule wins against
   309 to **167 against 55**, and the decided rate falls 0.0360 to 0.0213.
   **The gradient changes shape and this is the substantive finding of task 1.**
   The marginal decided rate runs 0.1083 / 0.0618 / 0.0256 / 0.0089 / 0.0278
   frozen, which 2.2e reported as rising again at ADS = 1.0 against Amendment
   1's prediction, and 0.1096 / 0.0443 / 0.0254 / 0.0089 / **0.0070**
   restricted, which is monotone. The rise is a small-block artifact. The
   per-SV top-below-bottom count goes 2 of 4 to 3 of 4, which is a majority
   restricted and was not frozen; non-increasing goes 0 of 4 to 1 of 4, still
   not a majority. The driver clause keeps its verdict and loses half its
   margin: eta2_ADS 0.1749 / eta2_SV 0.3837 frozen against 0.2136 / 0.3113
   restricted, `failed` at all three margins either way.
2. *Major 2, block size.* Seven octave bands, 1,157 to 2,293 blocks each.
   Pooled gaps -0.1145 / -0.0712 / -0.0350 / -0.0118 / -0.0069 / +0.0001 /
   +0.0056, rank correlation with band order +1.0000. Per-block winners
   20/215, 4/48, 26/13, 48/22, 38/11, 31/0, 24/0 as rule/k-NN. At fixed ADS the
   gaps are -0.1342 to -0.0076 inside ADS = 1.0 and +0.0594 to +0.0118 inside
   ADS < 1.0, decided in each stratum but never changing sign, which is a
   tie-crossing and not a reversal. Pooled-headline reconciliation: the five
   negative bands carry -1,466 net on 66,396 signatures, the two non-negative
   bands +479 on 131,083, total -987 over 197,479 = the pooled -0.0050.
3. *Major 3, uncertainty.* eta2_SV - eta2_ADS bootstrapped by resampling
   blocks, B = 2000, seed from the frozen `band_seed` scheme. **k = 5: +0.2088
   [+0.0628, +0.3473]**, SV larger in 99.9% of draws. Size-adjusted diagnostic,
   log cell-mean test size partialled out: +0.1840 [+0.0299, +0.3277], still
   excluding zero, so the confound the reviewer named is present and not load
   bearing. **k = 2: +0.0474 [-0.2531, +0.3159]**, which straddles zero, SV
   larger in only 57.0% of draws. So "stable across k" is accurate for the
   verdict and not for the evidence; k = 2 is the weak end and is also where
   the clause was already `split`.
4. *Major 8, accounting.* Out-of-history share pooled **0.0414**, ceiling
   **0.9586**. Per dataset: aminer 0.1565, arnetminer 0.1512, kisti 0.0951,
   qian 0.0483, zbmath 0.0287, pubmed 0.0112, inspire 0.0036. **The ceiling is
   not the main reason the datasets differ**, against the reviewer's
   expectation: normalizing for it closes only about 13% of the aminer to
   inspire spread. Rule conditional precision pooled **0.8512** on 96.86%
   coverage, against the vote's 0.8294.

**Invariant checks, run and passed.** Invariant 2, no tautology: nothing new is
defined here; block size is a count of signatures and is never derived from a
winner. Invariant 3, held-out only: every number is on the evaluation split's
primary population; no selector was fitted and none exists to fit. Invariant 5,
no result before measurement: every number in the report, including every
number in its headline, is emitted by `phase2_7b_reanalysis.py` and none is
retyped; the header is built by substitution from the tables. Invariant 7,
offline and reproducible: no network, no new dependency, CPU only, and
`demo()` is an assert-based self-check that pins `eta2_fast` against the frozen
`eta2_decomposition`. The run re-derives the frozen verdict counts
191 / 309 / 10,172 / 3,230 and aborts if they differ, asserts the restricted
power floor is unchanged, asserts the per-block test-set sizes agree with the
frozen split, and asserts that no out-of-history signature is scored correct by
either mechanism in the committed per-signature scores (8,168 of them).
**Determinism verified**: two consecutive runs produce a byte-identical report.

**What I did not do, and why.** Did not touch `main.tex`, by instruction: the
prose is 2.7c. Did not touch `PREREG.md` or any frozen constant. Did not
re-run the experiment or re-draw the split. Did not act on majors 4, 5, 6 or 7,
which are a scope decision and prose. Did not change the primary analysis: the
n_test >= 3 population is reported as a sensitivity analysis beside the frozen
all-blocks column and never in place of it. Did not push or tag.

**Recommendation for the next pass.** 2.7c, the prose pass, in the priority
order the report's closing section sets out. Take the block-size scoping
decision first, because it is the author's and it changes the abstract, the
title question and section 8.1, and majors 2, 4 and 5 all touch the same
paragraphs. Then the four reporting fixes: the size-1 and size-2 rows plus the
degeneracy note in 5.4 and Figure 2, the gradient sensitivity in the H2
discussion, the bootstrap interval in Table 4 with "stable across k" scoped to
the verdict, and the ceiling column plus conditional precision in 5.3 with the
caveat that the ceiling is not what separates the datasets. The body-length
constraint is unchanged and binding: 9,985 against the 10,000 ceiling, so every
addition has to be paid for. The two slow non-writing items are still open:
push and tag `phase-2`, and register an institutional email with arXiv.

## Pass 19 — Phase 2.7c, the prose pass (2026-09-21)

**What I did and why.** 2.7b produced every number the prose needed and touched
no prose. This pass wrote it. The manuscript was rewritten against the committed
2.7b numbers, citing that report's figures exactly. Nothing was measured, no
frozen definition was altered, `PREREG.md` was not opened, and no H1, H2 or H3
verdict moved. Every number added to the prose comes from
`reports/phase2_7b_reanalysis.md`, `reports/phase2e_boundary.md` or the
committed tables, and each was checked against its source table before it was
typed.

**1. The title, and the scope decision it rides on.** `\title{}` is now
"Prediction is not selection: a pre-registered study of design-time mechanism
choice in author name disambiguation". PLAN.md and STATE.md updated, with the
2.5d title kept beside it as the record of what it was. This is peer-review
major 4 closed by the reviewer's own first option: the entity resolution width
came out of the title and stayed in the paper, since sections 1.2 and 1.4 still
state the structural containment at entity resolution width and scope the
empirical null to the author name disambiguation instance.

**2. The scoping decision, taken first as 2.7b asked.** Every flat "no
design-time signal is actionable" sentence is gone, from the abstract, section
1.4, section 8.1, the limitations and the conclusion. What stands in its place
is the statement the evidence supports: **neither pre-registered signal is
actionable at the margin, and no design-time signal we examined tells a designer
which mechanism resolves a name better**. "Prediction is not selection" is
unchanged as the thesis.

**3. The abstract.** Rebuilt as one paragraph of 260 words, down from 288 in
three. "Signature" is gone, replaced by "held-out author mentions". It leads
with the structural containment, then the two pre-registered signals, then block
size and its deflation, then H1 as the contrast.

**4. Block size, the new section 7.7 with Table 7.** This is the subsection the
whole pass turns on, and it is written in the order the report established:
the decided verdict in full first (3-4 at $-0.1145$ [$-0.1286$, $-0.1007$], 5-8
at $-0.0712$ [$-0.0807$, $-0.0614$], both `k-NN wins`, and the statement that
neither pre-registered signal produces one decided marginal band), then the two
measured deflations, then the reconciliation, then the distinction the whole
subsection exists to land.
- *Composition.* At fixed ADS the sign never changes: inside ADS = 1.0 every
  band is negative, $-0.1342$ down to $-0.0076$; inside ADS < 1.0 every band is
  positive, $+0.0594$ to $+0.0118$. 90.0% of the smallest band is ADS = 1.0
  against 43.8% of the largest. So block size says how much the choice is worth,
  not which choice to make, and at fixed consistency it never points anywhere
  consistency does not already point.
- *Abstention.* Rule coverage climbs 0.8423 to 0.9827 across the bands, and the
  rule's precision where it fires exceeds the vote's accuracy in all seven,
  0.9370 against 0.9037 in the smallest. Table 7 carries both columns and the
  vote's accuracies beneath them. The prose says plainly that telling a designer
  to use the vote on small blocks is telling them to prefer the mechanism that
  is less often right where it commits, because the other declines to commit on
  about a sixth of the items.
- *Reconciliation.* Pooled the vote is ahead 0.0050; per block the rule takes
  191 against 309. The two smallest bands hold 263 of the vote's 309 wins and 24
  of the rule's 191; the two largest bands are 2,809 of 13,902 blocks but
  131,083 of 197,479 signatures; the five negative bands contribute $-1,466$ on
  66,396 and the two non-negative $+479$ on 131,083, totalling $-987$ over
  197,479, which is the pooled $-0.0050$. On the restricted population the
  per-block margin is 167 against 55, the rule taking the larger blocks.
- *The closing claim.* Two things get called a winner. Block size predicts which
  mechanism has the higher whole-set accuracy on small blocks, and that
  mechanism is the one that never abstains. It does not predict which mechanism
  resolves a name better. The edge is a mechanical consequence of coverage
  against abstention, which is fixed by the two definitions and needed no
  measurement.

Section 7.8, the no-selector subsection, now also answers the block-size version
of the selector question rather than only the ADS-and-SV version.

**5. Small-block sensitivity (major 1).** Reported as a sensitivity analysis
with the frozen primary unchanged. Section 7.4 gains the size-1 stratum
(1,309 blocks: 14 / 165 / 1,130 / 0 undecided, the zero by construction), the
size-2 stratum (2,159: 10 / 89 / 1,739 / 321), the fact that the two together
supply 278 of the 500 decided verdicts and 2,869 of the 10,172 ties, and the
restriction's result: 0 ADS bands, 0 SV bands, 0 of 20 cells decided at
delta = 0.05, so no verdict moves. Section 7.6 gains the gradient result: the
restricted marginal gradient 0.1096 / 0.0443 / 0.0254 / 0.0089 / 0.0070 is
monotone, the rise at ADS = 1.0 is a small-block artifact, and the per-SV
top-below-bottom count goes 2 of 4 to 3 of 4. The Figure 2 caption now says the
size-1 stratum cannot produce an undecided verdict by construction.

**6. Driver uncertainty (major 3).** Table 5 gains a bootstrap panel:
k = 5 $+0.2088$ [$+0.0628$, $+0.3473$], 99.9% of draws; size-adjusted $+0.1840$
[$+0.0299$, $+0.3277$], 99.5%; k = 2 $+0.0474$ [$-0.2531$, $+0.3159$], 57.0%.
Section 7.6's prose now separates the verdict from the evidence: the point
estimate points the same way at every k, which is what makes the clause outcome
stable, and the direction is decisive at k = 5 and not distinguishable from zero
at k = 2. "The sharpest single measurement in the run" is now scoped to k = 5
rather than to the whole curve.

**7. Accuracy accounting (major 8).** Table 3 gains a Ceiling column
(pooled 0.9586, aminer 0.8435, inspire 0.9964, and the rest), with the caveat
stated in text that normalizing for it closes only about 13% of the
aminer-to-inspire spread, so it does not explain the dataset differences.
Section 7.3 gains the rule's conditional precision, 0.8512 on 96.86% coverage
against the vote's 0.8294. Section 6.3 gains three sentences justifying
whole-set accuracy over B-cubed for an assignment task and naming the
comparability cost.

**8. The three integrity disclosures (majors 5, 6, 7).**
- *Major 5.* The locked 6.4 quote is unchanged and was verified byte-identical
  to `HEAD` and to the PLAN.md deliverable after every edit. A fourth point of
  record below it states exactly what existed at `c20239a` (12:09:23): the
  calibration-split k-NN accuracies 0.8390 / 0.8354 / 0.8290 / 0.8188, the
  two-sidedness counts, and the per-cell ADS-by-SV grid whose gaps already carry
  the compression-and-sign-change shape, $+0.0576$ in [0, 0.5) x SV-high against
  $-0.0526$ at ADS = 1.0 x SV = 0. It says the amended hypotheses were written
  with that grid in view, that what makes it legitimate is the original
  pre-registration reserving the calibration split for design choices, and that
  the evaluation split was untouched. The correction is by disclosure, not by
  editing locked text.
- *Major 6.* A fifth point of record says the ordering evidence is
  author-controlled git metadata, names the regression check against frozen
  calibration-split counts as the one control that is not, and says the
  repository will be pushed and tagged at release.
- *Major 7.* The two delta = 0.02 reversals are in section 7.5 in two sentences,
  and Appendix A (new, Table 8) gives the winner structure for the
  direction-by-SV, fixed-SV and INIT grids at all three margins, with the
  outcome vocabulary defined there.

**9. Substantive minors taken.** ADS expanded at first use as the
author-dominance share; Table 2's "n/a" replaced by 3,876 with a caption note
saying the containment fixes it; a paragraph on kisti and one on inspire's
out-of-history share; the Table 4 caption's conflation of the two power floors
fixed; the two undecided cells named; `adscascade2026` stated in text as a
Zenodo-archived artifact rather than a peer-reviewed paper.

**Key artifacts.** `phase2/paper/main.tex` only. No table, figure, report or
code file was written or changed. No new figure was added; the new floats are
Table 7 (block size) and Table 8 (Appendix A), both built from committed CSVs.

**Invariant checks, run and passed.** Invariant 2, no tautology: nothing was
defined this pass; block size is a count of signatures and appears nowhere in
any winner definition. Invariant 3, held-out only: every number in the prose is
on the evaluation split's primary population or on the labelled sensitivity
subset; no selector exists or was fitted. Invariant 5, no result before
measurement: nothing was measured and nothing was invented. Every added number
was checked against its committed source before typing, including 3,876 against
`phase2b_accuracy_by_population.csv` (0.019627403420110493 x 197,479 = 3876.0
exactly), the calibration accuracies and per-cell gaps against
`phase2c_pair_twosidedness.csv` and `phase2c_pair_regimes.csv`, the commit
timestamps against `git log`, and the whole block-size, sensitivity, driver and
accounting sets against `reports/phase2_7b_reanalysis.md`. Invariant 7, offline
and reproducible: no network, no dependency, no code. Invariant 8, honest
framing: this pass exists to make the framing more honest, not less; the one
claim 2.7b found unsupported was rescoped rather than dropped, and the
counter-example is reported in full before it is deflated. The locked 6.4 quote
was verified byte-identical to `HEAD`.

**Build.** `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`. Zero undefined
citations, zero undefined references, zero LaTeX warnings, zero em dashes. Six
underfull hboxes, the same six the pre-pass build had, in the author footnote,
the Figure 1 caption, a falsification-table cell and a bibliography entry. The
one overfull hbox the pre-pass build had, in the driver table, is gone.
`main.bbl` is unchanged because no citation was added. 30 pages, up from 25.

**What I did not do, and why.** Did not touch `PREREG.md`, any frozen constant,
any committed table or any report. Did not re-run or re-analyse anything. Did
not add a reference or a citation, by instruction: the reference expansion is
2.7d. Did not add keywords, funding, competing-interests or contributions
declarations, also 2.7d. Did not run `/anti-ai` over the new prose, also 2.7d.
Did not trim, by instruction. Did not push or tag.

**The length, stated plainly.** `texcount -inc` reads 13,263 text words against
the pre-pass 9,537, so this pass added about 3,700 words against a charter
ceiling of 10,000 for the prose total. That was the instruction and it makes the
trim the binding constraint on 2.7d rather than a tidiness item.

**Recommendation for the next pass.** 2.7d, in this order: the trim, the
reference expansion, the front and back matter, the remaining minors, then
`/anti-ai` and a final rebuild. STATE.md names five trim candidates and one
non-candidate. **Section 7.7 and both of its deflations are not a trim target**:
reporting the block-size verdict without the composition and abstention results
is worse than not reporting it, because it reads as a buried selection signal,
which is the single most damaging thing a reviewer could say about a paper whose
contribution is a null result. The two slow non-writing items are unchanged and
one of them the manuscript now promises in text: push and tag `phase-2`, and
deposit the frozen pre-registration somewhere with a timestamp the author does
not control.

---

## Pass 20 — Phase 2.7d, citations, declarations, trim and polish (2026-09-21)

**What I did and why.** 2.7c added about 3,700 words and deferred five things.
This pass pays for them and closes the deferred set: eight new citations, the
four standard declarations, the length trim, the remaining peer-review minors,
and an `/anti-ai` pass over what was written or revised. Nothing was measured.
`PREREG.md` was not opened, no frozen constant or committed table moved, and no
H1, H2 or H3 verdict changed. The locked 6.4 quote is byte-identical to its
pre-pass state, verified by sha256 (`dcaa1bc…f8f4`) before and after.

### 1. The eight citations, all flagged unverified

`references.bib` grows from 17 entries to 25, in a new Block E whose header and
whose every `note` field says **"Unverified, verify at review"**. That is the
instruction and it is the honest state: none of the eight was checked against a
DOI or venue record this pass, unlike Block C at 2.6. They are to be held to the
2.6 standard before submission.

| Key | Placed at | Doing what |
|---|---|---|
| `fellegisunter1969` | 1.2 | the record-linkage foundation under the entity resolution width |
| `christen2012` | 1.2 | the entity resolution reference work |
| `papadakis2020` | 1.2 | the blocking literature |
| `autoblock2020` | 4.3 | the prior statement of the containment intuition |
| `mudgal2018` | 2.4 | the learned line the two untrained mechanisms are deliberately not |
| `armstrong2009` | 2.1 | the lineage of comparisons that cannot inform |
| `lakens2017` | 3.3 | the four-verdict winner construct as equivalence testing |
| `kim2019` | 2.2, 6.3 | AND evaluation methodology, beside `amigo2009` |

Two placements carry an explicit concession rather than a name-drop. Section
4.3 now says the containment intuition is not new, cites AutoBlock for
key-based blocking as a special case of nearest-neighbour blocking under a
binary similarity metric, and states that **what we add is the consequence
drawn from it**, the unreachable verdict, not the containment observation.
Section 2.1 says this paper belongs to the Armstrong lineage of comparisons
that cannot inform and that its structural version is sharper, because there
the baseline could have been beaten and was chosen badly, and here one of the
two verdicts cannot occur at all. Section 3.3 names the winner construct as
equivalence testing and carries the margin-choice caveat from that literature.
The related-work expansion is three paragraphs and four sentences, not a
survey.

### 2. Declarations

Keywords after the abstract, six of them: author name disambiguation;
pre-registration; mechanism selection; equivalence testing; entity resolution;
negative results. Three new starred back-matter sections before the availability
statement: **Funding** (none, stated as none, with no paid compute or data
access), **Competing interests** (none, plus the one disclosure that matters,
that section 8.3 reinterprets an archived artifact of the author's own), and
**Author contributions** (sole author, with the AI-assistance role pointed at
the existing disclosure rather than restated). Peer-review minor 2 closed.

### 3. The trim, and how it was actually achieved

**30 pages to 26, and 13,263 text words to 12,079.** The page target is met.
The charter's 10,000-word prose ceiling is not, and that is stated plainly
below rather than buried.

Taken as instructed:
- **Section 6.4's points of record compressed.** All seven commit ids survive in
  the footnote, both corrections survive as their own labelled points, and the
  locked quote was not touched. The subsection is 983 words of which about 385
  are the quote.
- **Sections 8.3 and 2.3 shrunk**, 8.3 by folding the three labelled findings
  into one paragraph and tightening the fallback description, 2.3 by compressing
  the manipulation detail and the four-differences list.
- **Section 7.3's two minor paragraphs removed as paragraphs.** They are not
  deleted outright: kisti and inspire each keep one sentence carrying the
  numbers the review asked for, because deleting them would reopen minors 8 and
  9 that 2.7c closed. This is the one place the instruction was read in effect
  rather than literally, and it is flagged here for review.
- **Figure 5 and Table 6's overlap cut, Figure 5 going.** Table 6 is the frozen
  falsification table and cannot go; its $k$ rows carry the sensitivity curve,
  and Table 2 carries the accuracy and two-sidedness curve, so the figure was
  the duplicate. Its caption now says why nothing repeats it.
- **Section 7.7 and both deflations kept.** Tightened for concision by about 90
  words; every number, both qualifications and the licensing paragraph stand.

**Beyond the instruction, and the part that needs sign-off.** The named cuts
plus a full prose pass reached 29 pages, not 26. Four further changes closed the
gap, and three of them are not prose:
1. **Two more floats removed.** Figure 1 (the H1 scatter) and Figure 4 (the
   decidability gradient). Both were pure plots of numbers the text already
   states in full, both PNGs stay in the repository and are named in the text at
   the point they were used, and H1 is labelled in the paper as a
   construct-validity check rather than a contribution. Restoring either costs
   about one page. **This is the judgement call of the pass.**
2. `\parskip` set to 0pt, from `0.25\baselineskip`. The class already indents
   paragraphs, so the document was using both devices. Worth one page.
3. `\bibsep` set to `0.4ex plus 0.2ex`. The bibliography was spilling nine lines
   onto a page of its own. Worth one page.
4. Float placement fractions loosened (`topfraction` 0.9, `bottomfraction` 0.8,
   `textfraction` 0.07, `floatpagefraction` 0.8, `topnumber` 3, `totalnumber`
   4), so large tables stop claiming a page each.

Five tables gained `\small` and the two surviving figures dropped from
`0.8\linewidth` to `0.7`. Six float captions were tightened; captions fell from
831 words to 636.

**The length, stated plainly.** Text 12,079 words, headers 229, captions 636,
prose total 12,944 against the charter's 10,000. Prose came down by about 1,200
words this pass; the other four pages came from three floats and from
typography. **The charter ceiling is not met and cannot be met by tightening
alone.** Reaching 10,000 needs about 2,000 more words out, which means removing
argument, not wording, after four editing passes over the same text. The
candidates, if review wants them: Appendix A and Table 8 (about one page, and
the review's major 7 was satisfied by the two sentences now in 7.5, so the
appendix is above requirement), the 6.4 points of record beyond the two
corrections, and section 8.3 as a whole.

### 4. Remaining minors

- **Minor 3, bare acronyms.** A scan of every uppercase token in the body found
  only one left unglossed: ROC, now "the receiver operating characteristic (ROC)
  curve". `k-NN` is now defined where the verdicts are defined, in 6.3. ADS, SV,
  SV\_resid and INIT were already expanded at first use.
- **Minor 13, the Table 5 caption power-floor conflation.** Already fixed at
  2.7c and verified still correct; the caption separates H2's floor from H3's.
- **Minor 15, the two undecided cells.** Already named at 2.7c and still named:
  $[0, 0.5)$ crossed with SV-high at a decided rate of 0.1971 over 553 blocks,
  and ADS = 1.0 crossed with SV = 0 at 3,922 blocks.
- **Minor 6, the Spearman population in 3.2.** Now says the $-0.2612$ is across
  the 18,984 live blocks, "a wider population than the 13,902 every reported
  result uses".
- **Minor 5, "to every printed digit" in 4.2.** Now "to four decimal places".
- **Minor 14, six-decimal band edges.** Printed to four decimals (0.1026,
  0.1951, 0.0368, 0.0824) with a pointer to `phase2b_constants.py` as the frozen
  record at full precision.
- **Minor 16, runtime and hardware.** One sentence added to the availability
  statement: offline and CPU-only, no network call after the one-time S2AND
  download, no GPU and no paid service, about twenty minutes for a full
  mechanism pass, one consumer laptop, the seed of section 6.1. The twenty
  minutes is the figure STATE.md records for the cached mechanism re-run; no
  machine specification exists in the repository and none is asserted.
- **Minor 17, the Zenodo concept DOI. VERIFIED and closed.** Queried the Zenodo
  REST API this pass. `10.5281/zenodo.21644207` is the concept DOI
  (`conceptrecid` 21644207) and currently resolves to v1.1.0 at
  `10.5281/zenodo.22258609`; `10.5281/zenodo.21644208` is v1.0.0. Both
  `references.bib` and the availability statement already said exactly that, so
  nothing changed in the text and the verification is recorded as a comment in
  the bib.
- **Minor 1, abstract length.** 260 words to 246, inside the 200-250 band.
- **Minor 19, the Figure 5 / Table 6 overlap.** Closed, see the trim above.

### 5. The `/anti-ai` pass

Run over the prose written or revised this pass, which after four rewrites is
most of the body. Audited mechanically first: zero occurrences of delve,
underscore, pivotal, crucial, seamless, comprehensive, intricate, nuanced,
holistic, transformative, Moreover, Furthermore, Additionally, Consequently,
"it is important to note", "shed light", "paves the way", "testament", "in
conclusion" or "further research is needed". Five hits on "robust" are all
"robustness curve", the pre-registered term, and "Surface-form robustness", a
real section topic. Sentence length runs mean 24.7, sd 13.0, from 3 to 71 words,
with 32% in the 15-25 band and 17% under 12, which is high burstiness rather
than the flat AI rhythm. Paragraph openers are varied; no paragraph opens with a
formulaic connective.

Six rewrites followed. The entity-resolution citation sentence stopped being a
"runs from X through Y and Z" tour. The Armstrong paragraph lost an
unattributed "the concern has been restated for each wave of new methods since".
The AutoBlock sentence lost its "what we add is X and not Y" negative
parallelism while keeping the distinction the instruction requires. The learned
entity-matching clause was rewritten out of an awkward tail. The design-time
definition lost a "not only" construction. The runtime sentence was made plainer.
Every number, every citation key and every verdict word was preserved; no em
dash was introduced, asserted in the edit script itself.

### 6. The numeric audit, and three restorations

Because four rewriting passes went over the same text, the multiset of every
numeric token in the body was diffed against the pre-pass file. Everything that
left is accounted for: the four six-decimal band edges, replaced by their
four-decimal forms (minor 14); `0.25` and three `0.8`s, which are `\parskip`
and the figure widths; `0.9184`, `92.18`, `0.94` and one of the two `0.7334`s,
which are the kisti and inspire sentences the instruction said to remove, with
the surviving `0.7334` still in Table 3; and duplicate mentions of `13{,}902`,
`197{,}479`, `0.02` and small integers, each of which still appears elsewhere
(`0.02` 34 times, `13{,}902` 13 times, `197{,}479` 5 times). Everything that
arrived is a citation year, a rounded band edge, or a preamble length.

Three specifics the trim had dropped were put back after that audit, because
they are precision rather than padding: the `12:09:23 on 2026-09-18` timestamp
on `c20239a` in the 6.4 correction, the `0.1529` aminer-to-inspire ceiling
difference in 7.3, and the explicit 95\% level on the driver bootstrap in 7.6.

### Invariant checks

Invariant 1, verify before you build: nothing built. Invariant 2, no tautology:
no construct touched. Invariant 3, held-out only: no new number. Invariant 4,
superseded, and no selector exists to report baselines beside. Invariant 5, no
result before measurement: **nothing was measured and no number changed**,
verified by diffing every numeric token in the body against the pre-pass file
(see below). Invariant 6, two mechanisms, both untrained, no third arm: the new
`mudgal2018` citation is explicitly named as the line this paper is not on.
Invariant 7, offline and reproducible: no code, no dependency; the one network
call this pass was a read-only Zenodo API query for minor 17, recorded above.
Invariant 8, honest framing: the trim did not touch section 7.7's deflations,
the locked quote or either correction under it, and the part of the page
reduction that came from typography and float cuts rather than from prose is
stated above rather than presented as tightening.

**Build.** `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`, `pdflatex`, from a
clean tree with the aux files removed. **26 pages. Zero undefined citations,
zero undefined references, zero LaTeX warnings, zero em dashes in the source and
zero in the rendered PDF.** 25 `\bibitem`s in `main.bbl`, which is regenerated
and committed because AutoTeX does not run BibTeX. Ten floats, down from
thirteen.

**Commit hashes.** All seven of section 6.4's short hashes resolve on `phase-2`
and their subject lines still match the roles 6.4 assigns them, in order:
`8869b82` 01:32:56, `5e13e38` 10:46:50, `3d86959` 11:43:11, `c20239a` 12:09:23,
`5f452ad` 12:36:16, `3e79a48` 13:04:42, `9e3d921` 14:25:07, all on 2026-09-18.
No history was rebased, squashed or amended.

**What I did not do.** Did not touch `PREREG.md`, any frozen constant, any
committed table, any report or any figure file. Did not re-run or re-analyse
anything. Did not verify the eight new citations, by instruction. Did not push
or tag. Did not delete `figs/phase2e_h1_ads_accuracy.png`,
`figs/phase2e_decidability_gradient.png` or `figs/phase2e_k_curve.png`, which
are now unused by the build but are sha256-identical to the `reports/figs/`
originals and are named in the text; removing them from the upload bundle is a
2.8 item.

**Recommendation for the next pass.** 2.8, release and submission prep. Three
things gate a first upload and none of them is writing. Push and tag `phase-2`,
which is the only thing that makes section 6.4's seven hashes and the
availability statement true for a reader. Deposit the frozen `PREREG.md`,
Amendment 1 and Addendum 1a somewhere with a timestamp the author does not
control, which is peer-review major 6. And register an institutional address
with arXiv, then open the cs.DL endorsement request, which is the only item
measured in weeks. Before submission, and separately from the upload: **verify
all eight Block E citations** against DOI and venue records to the 2.6 standard.
Two decisions are for review at the top of 2.8: whether the three extra float
and typography changes stand, and whether the charter's 10,000-word ceiling is
enforced or formally relaxed to the page count.

## Pass 21 — Phase 2.8a, citation lock, figure restore, and a contribution-and-moderation scan (2026-09-23)

**What I did and why.** Three items, all content edits: lock the eight Block E
citations to the values the author verified externally, restore the H1 figure
2.7d cut, and read the manuscript as an arXiv moderator would, sharpening the
framing wherever a real contribution was undersold. Then the moderation audit
re-run over its seven dimensions. Nothing was measured, `PREREG.md` was not
opened, no committed table, report or figure file moved, no verdict changed.
Not pushed, tagged or released, by instruction.

### 1. The citations, locked

Every `note = {Unverified, verify at review}` is removed and the fields set to
the author's confirmed values; the only field value that changed is Armstrong
et al.'s "Ad-hoc" to "Ad-Hoc", everything else already matched. Each of the
eight DOIs was also resolved against the Crossref REST API, read-only, which
agrees with the confirmed values and supplied the two multi-author expansions:
AutoBlock has six authors (Zhang, Wei, Sisman, Dong, Faloutsos, Page) and
Mudgal et al. nine, both as already in the bib. Two departures from raw
Crossref, recorded in the bib header: Crossref spells the last AutoBlock author
"Davd", a typo for David Page, and gives Lakens's forename as Daniël, which the
bib keeps as `Dani{\"e}l` although the confirmed list wrote it in ASCII.
AutoBlock's arXiv preprint pointer lived in the same note field and went with
it. The bib's header now reads all 25 entries verified.

### 2. The H1 figure, restored

Back as Figure 1 in section 7.2 at `0.7\linewidth`, matching the other two;
the decidability gradient stays cut, per the instruction. The PNG is
sha256-identical to `reports/figs/`. Two corrections came with it, both to
existing text rather than new claims. The old pointer called the plot "the
per-block scatter"; it is a line plot of mean per-block accuracy by ADS band
(`reports/phase2e_boundary.md`, "Mean per-block accuracy by ADS band"), and the
caption now says so. And the plot shows a fifth point the text does not quote,
ADS = 1.0, where the rule sits below the vote (0.9234 against 0.9889 in the
report). The caption explains it by pointing at section 4.3's argument, that a
history naming one author leaves the rule no departure from the vote but
abstention, rather than by printing the report's numbers. An earlier draft
said "which is why it falls there", which implies a cause for the band-to-band
drop that the paper does not establish; it now says "why it sits below the vote
there", which section 4.3 entails.

### 3. The contribution-and-moderation scan

The paper read as original research before the pass. What a skimming moderator
could misread: every positive result was stated as a reason the answer is no,
nothing said in one place what the paper adds, the calibration trap first
appeared in section 5.2, and two sentences undersold the structural result.
Six framing edits:

- **New section 1.4, "Contributions"**, four items on page 3, each a restatement
  of a claim already made with a pointer to where: the structural result and
  its unreachable-verdict consequence, with the AutoBlock precedent conceded
  inside the item; the pre-registered study, with both hypotheses named
  Inconclusive; the block-size deflation, with "did not pre-register" inside
  the item; the cautions for portfolio and benchmark design. The calibration
  trap is worded as "moves its parameter toward the limit", which both tunable
  families support, and not as section 5.2 words it (see F1).
- **Abstract and 1.3, "avoids both problems"** became "in which neither
  mechanism contains the other". Traced through history, the two problems were
  always the nesting and the general form's empty regions, and no pair avoids
  the second.
- **Abstract, "Against that, the same statistic predicts"** became "The
  consistency statistic, by contrast, predicts". Since 2.7c the preceding
  sentences are about block size, so it read as block size predicting accuracy
  at 0.51 and 0.83.
- **4.3, "a trap practitioners fall into rather than a theorem anyone needs"**
  became "The result is practical rather than deep, and the trap is easy to
  fall into".
- **8.1, "most of what this paper has to offer"** became "the paper's central
  contribution".

**Five flags for human review, not acted on**, each because it needs new
analysis or changes a claim; full text in the audit report.
- **F1, the one that matters.** Section 5.2 says the accuracy-maximizing
  protocol "selects the degenerate parameter and walks the design straight back
  into a comparison that cannot have a winner" in either family. Exact for the
  radius vote; on the k grid it selects k = 2, which is two-sided at 181/736 on
  calibration and 987/3,990 on evaluation, in the paper's own Table 2.
  Inherited from `reports/phase2c_pair_design.md`.
- F2, the 41% contested-region figure is calibration-split only. F3, the
  one-count check on a non-AND benchmark would make the entity resolution width
  a demonstration. F4, the calibration trap is not in the abstract, because the
  shortest accurate clause puts it at about 263 words. F5, section 4 could be
  set as a proposition with a proof.

### 4. The moderation audit, re-run

`reports/phase2_8a_moderation_audit.md`, over the same seven dimensions as
2.6. **No desk-reject risk on content.** Self-containment is still the top
finding and still the release pass's: `phase-2` unpushed, the availability
statement future-tense, the locked quote's "public repository" true only after
the push. Category: cs.DB is now a better-supported cross-list than cs.LG,
since the paper cites the entity resolution literature. Overlap with
`manuscript/main.tex`: 8 shared 8-grams of 14,277, all in section 8.3 and all
from two attributed phrases describing the earlier study. An AutoTeX-style
isolated build with `main.tex`, `main.bbl` and only the three used PNGs came
out clean, so `phase2e_decidability_gradient.png` and `phase2e_k_curve.png` can
be left out of the tarball. Submission-time items reported and left alone: the
one `{,}` in the metadata abstract, the cross-list, the licence, the ORCID on
the account, the institutional address and cs.DL endorsement.

### Numbers

**27 pages**, up one for the restored figure. `texcount -inc`: 12,375 text
words, 230 in headers, 692 in captions, **prose total 13,297** against the
charter's 10,000 and 12,944 at 2.7d; about 270 of the 353 are the contributions
list and 56 the restored caption. Abstract 249 words, 1,565 characters with
the separator retyped, against arXiv's 1,920. Eleven floats.

### Invariant checks

Invariant 1, verify before you build: nothing built. Invariant 2, no tautology:
no construct touched. Invariant 3, held-out only: no new number. Invariant 4,
superseded, no selector. Invariant 5, no result before measurement: **nothing
measured, and every numeric token in the body diffed against the pre-pass
file: none removed, and the only additions are `199{,}713` and `197{,}479`
restated in the contributions list, the figure width, and digits in the
figure's filename.** No number new to the paper. Invariant 6, two untrained
mechanisms, no third arm: untouched. Invariant 7, offline and reproducible: no
code or dependency changed; the pass's network calls were eight read-only
Crossref lookups. Invariant 8, honest framing: the contributions list carries
"did not pre-register", "Inconclusive" and the AutoBlock concession inside its
own items; section 7.7's deflations, the locked quote, both corrections under
it and the limitations section are untouched; the one existing overstatement
found, F1, is flagged rather than repeated or silently changed.

**Build.** From a clean tree, `pdflatex`, `bibtex`, `pdflatex` x3: zero
undefined citations, zero undefined references, zero LaTeX warnings, 25
`\bibitem`s, no "Unverified" in `main.bbl` or the PDF, zero em dashes in the
source and the PDF, `main.tex` and `references.bib` pure ASCII. Four cosmetic
underfull-box notices, no overfull boxes. **Locked 6.4 quote byte-identical**,
sha256 `dcaa1bc…f8f4` over `\begin{quote}` through `\end{quote}` plus the
trailing newline, before and after. **All seven 6.4 hashes resolve** on
`phase-2` as ancestors of the tip with matching subjects: `8869b82` 01:32:56,
`5e13e38` 10:46:50, `3d86959` 11:43:11, `c20239a` 12:09:23, `5f452ad` 12:36:16,
`3e79a48` 13:04:42, `9e3d921` 14:25:07, all 2026-09-18. No history rewritten.

**What I did not do.** Did not push, tag, release or cut Zenodo v2; the
availability statement stays future-tense. Did not touch `PREREG.md`, any frozen
constant, table, report or figure file. Did not act on F1 to F5 or on any
submission-time item. Did not revisit the 2.7d typographic settings, which were
not in the instruction. Did not delete the two unused PNGs.

**Recommendation for the next pass.** Decide F1 first, since it is a sentence a
reviewer can falsify from the paper's own Table 2. Then the release pass: push
and tag `phase-2`, cut Zenodo v2 from the tag, move the availability statement
to the present tense, deposit the frozen pre-registration with an independent
timestamp, and package the tarball with `main.bbl` and the three used figures.
The venue-specific trim follows once a venue is chosen and carries the word
ceiling, the typography and F4. Start the institutional arXiv address and the
cs.DL endorsement request now, in parallel; nothing else here takes weeks.

---

## Pass 22 — Phase 2.9a, release-pass facts and the like-for-like precision comparison (2026-11-12)

**What I did and why.** This is the first pass of the release. The goal is
to declare the paper complete and make it public on GitHub plus a new Zenodo
record, with no journal and no arXiv. The orchestrating chat read the recon
(`../RECON_ads_cascade_2026-11-12.md`) and will write the manuscript edits
itself at 2.9b. This pass gathered the facts those edits need, read-only
(Part A, seven items), and committed one analysis script (Part B, new files
only). Two release-pass overrides apply, both from the 2.9 brief: arXiv and
venue items are moot, and the word ceiling is not enforced. Nothing in
`paper/`, `PREREG.md` or any existing report, table or figure was touched.
Everything is in `reports/phase2_9a_report.md`.

### Key numbers

The script is `phase2_9a_matched.py`. It halts unless 13,902 / 197,479 /
0.824442 / 0.829440 reproduce, then checks six per-block counts against
`phase2e_blocks_scored.csv.gz`. Both checks passed.

- **Matched precision** (`reports/tables/phase2_9a_matched_precision.csv`). The
  rule's precision where it fires is 0.8512. The vote's accuracy on the same
  fired items is 0.8359, against 0.8294 on all items. The matched margin is
  **+0.0153 [+0.0142, +0.0165]**, so the paper's +0.0218 overstates it by
  0.0064. It is positive in all seven block-size bands (+0.0118 to +0.0261) and
  all seven datasets (+0.0044 to +0.2703), and every lower bound is above zero.
- **Region counts** (`reports/tables/phase2_9a_region_counts.csv`). In the
  SV = 0 band (17,960 test signatures):
  - rule right and vote wrong: **0**;
  - vote right and rule wrong: **696**, all of them rule abstentions;
  - test forms absent from the training half: 835.

  ADS = 1.0 shows the same pattern: 0 against 3,029, all abstentions. Section
  4.3's "no mechanism can win where the history is written one way" is
  therefore false. The rule cannot win there; the vote can. That is Table 4's
  SV = 0 `k-NN wins` at delta 0.03 and 0.02.
- **Contested share, evaluation split**
  (`reports/tables/phase2_9a_contested_share.csv`): **0.4223**, 83,401 of
  197,479 signatures in 2,770 of 13,902 blocks. The calibration figure is
  0.4108. This closes the factual half of F2.
- **Max-score collisions.** 0 of 210,537 distinct-form pairs inside primary
  blocks score 1.0 under Levenshtein or Jaro-Winkler, as the mechanisms compute
  it (float32, no processor).

### Part A in brief

- **a41a67a.** It added the revision note, "Margin sensitivity" and "Order of
  evaluation" to `PREREG.md`. No file, git object or temp file was written
  between 01:33:00 and 10:27:06. The first post-freeze pipeline import was at
  10:33:08. No calibration or evaluation number came before it. The "reviewer"
  was the between-pass reviewer of the 2.2a freeze; whether that was the human
  or an orchestrating chat is not recorded, and no September transcript
  survives. It was not the simulated 2.7 review.
- **Section 8.3.** Eleven of twelve claims hold against `manuscript/main.tex`
  and its committed outputs. (j) does not: zero defined comparisons is not
  equivalence, and 5 of the 120 clean intervals cross +0.02. That 115/120 count
  came from a one-line command over a Phase 1 CSV, not committed code. The
  Experiment 1 design commit (3c6b581) was pushed 41 s after it was made and
  about 11 h before the run.
- **Containment.** It is valid for the two functions used. The wording needs
  "the maximum is attained only at identity". rapidfuzz's token and partial
  ratios and any case-folding processor break it. main.tex:722 is inside the
  locked quote.
- **Sources.** 0.36 is `phase2e_signal_correlations.csv`. −0.818 / +0.743 /
  +0.18 / +0.06 are `gate21_two_axes.md:122-125`.
- **main.tex:112-115** rests on one benchmark, WDC LSPC 2017, which is exact or
  near-exact on both framings.
- **Crossref.** The Primpeli and Sinha DOIs were found and BibTeX drafted. For
  Sinha, Crossref gives the venue as "Proceedings of the 24th International
  Conference on World Wide Web", not "Companion". Pages were found for
  hendrickx2024 (113(5):3073-3110), s2and2021 (170-179) and backes2018
  (803-812).
- **Environment.** CPython 3.14.2 is the only interpreter on the machine with
  the packages. Its bytecode is cpython-314. The seven scientific packages are
  unchanged since 2026-09-18; only statsmodels, seaborn and their dependencies
  were installed after (2026-10-01).

### Invariant checks

- **Invariant 1** (verify before you build): nothing built on a new axis.
- **Invariant 2** (no tautology): no construct touched.
- **Invariant 3** (held-out only): every number is evaluation-split, from the
  frozen held-out scores.
- **Invariant 4:** superseded; no selector.
- **Invariant 5** (no result before measurement): every Part B number comes
  from committed, re-runnable code with halting checks, and two runs were
  byte-identical. The report flags the one Part A count that does not yet come
  from committed code (Experiment 1's 115/120).
- **Invariant 6** (two untrained mechanisms, no third arm): untouched.
- **Invariant 7** (offline and reproducible): the script is offline. The
  pass's only network calls were seven read-only Crossref GETs, sent with a
  generic user agent.
- **Invariant 8** (honest framing): three paper sentences are found to
  overstate (4.3 region 2, the 0.0218, 8.3 (j)) and one to overgeneralise
  (containment). All are reported for 2.9b, not edited here.
- **History:** none rewritten. Hard rule 2 was respected.
- **One side effect.** The run recompiled the gitignored, stale
  `__pycache__/phase2_7b_reanalysis.cpython-314.pyc`. Its prior mtime,
  2026-09-21 14:17:09, was recorded before the run.

**Recommendation for the next pass.** 2.9b, the manuscript edits, in this
priority order:

1. 4.3 region 2 (main.tex:136-137, 475-478), to the narrow version in A3.
2. The matched margin (main.tex:158, 209-210, 911-913, 1297-1302, 1359-1360),
   from `phase2_9a_matched_precision.csv`.
3. The `a41a67a` disclosure in 6.4 and its footnote, and "external read"
   (main.tex:745).
4. The containment condition (main.tex:50-51, 130, 420-421, 509-510), with
   main.tex:722 handled by disclosure.
5. 8.3 (j).
6. 42.2% beside 41%.
7. Then the release.

## Pass 23 — Phase 2.9b step 1, per-population verdicts, the INIT control cells, and the Experiment 1 interval count (2026-11-12)

**What I did and why.** I executed work order WO-1 of the release-pass master
plan (`../FABLE_MASTER_PLAN.md`), with the orchestrator's three amendments. The
goal is to put every number the manuscript edits (WO-2) need into committed
tables before any prose moves. Findings W1, W2 and W8 needed new computation.
O3 needed the local file times on record. The work is one new script,
`phase2_9b_supplement.py`, in the conventions of `phase2_9a_matched.py`. It
imports and does not restate: `phase2_9a_matched.load` for the frozen
population check, `phase2e_run.pooled_table` and `structural` at `PRIMARY`,
and `phase2b_run.populations`. No existing script, report, table, figure,
`PREREG.md` or `paper/` file was touched. Everything is in
`reports/phase2_9b_report.md`.

### Key numbers

The script halts unless 13,902 / 197,479 / 0.824442 / 0.829440 reproduce.
They did. Sub-population intervals use new seeds tagged
`p29b|<population>|<axis>`. The `all` rows match `phase2e_pooled_ads.csv`,
`_sv.csv` and `_cells_sv.csv` to 1e-12 on the point gap, and every frozen
population matches `phase2e_accuracy_by_population.csv`. Under the new seeds
none of the 87 `all`-row verdicts (29 groups, three margins) differs from the
committed one. All numbers below are at delta = 0.05 unless stated.

- **Whole populations** (`reports/tables/phase2_9b_population_verdicts.csv`):
  - kisti: **+0.1131 [+0.1015, +0.1250], `rule wins`** at every margin;
  - zbmath: **-0.0631 [-0.0761, -0.0512], `k-NN wins`** at every margin, with
    the upper bound 0.0012 inside the margin;
  - pubmed (34 blocks, not qualifying): +0.2466, `rule wins`;
  - pooled non-inspire: +0.0221, tie;
  - non-inspire without kisti: +0.0029, tie;
  - inspire, aminer, arnetminer and qian are ties at 0.05.
- **Bands** (`phase2_9b_bands_by_population.csv`). Inside kisti, `rule wins`
  for SV high (+0.1654, 443 blocks), SV mid (+0.0806), ADS [0, 0.5) (+0.1762)
  and [0.5, 0.7) (+0.1100). In pooled non-inspire, SV high is `rule wins`
  (+0.0600, lower bound 0.0501, so by 0.0001) and ADS = 1.0 is undecided.
  In non-inspire without kisti, every ADS band below 1.0 and every SV band is
  a tie at 0.05 and 0.03. At 0.02, SV = 0 and SV high are undecided.
- **Grid and structure** (`phase2_9b_cells_by_population.csv`,
  `phase2_9b_structure_by_population.csv`). In pooled non-inspire at fixed SV
  high, [0, 0.5) +0.0629 and [0.5, 0.7) +0.1024 are `rule wins` and ADS = 1.0
  -0.1130 is `k-NN wins`. That is a **winner reversal** across ADS at the
  primary margin. Across SV at fixed ADS, pooled non-inspire has no reversal:
  tie-crossings at [0, 0.5), [0.5, 0.7) and 1.0, and gap compression only at
  the other two levels.
- **INIT** (`phase2_9b_init.csv`). The INIT bands on their own are all ties at
  0.05: INIT = 0 +0.0066, 0 < INIT < 0.5 +0.0018, INIT >= 0.5 -0.0183. The two
  cells of `phase2e_pooled_init_sv.csv` decided at 0.05 were asserted to be
  exactly INIT = 0 x SV high (`rule wins`) and INIT >= 0.5 x SV = 0
  (`k-NN wins`):
  - INIT = 0 x SV high: kisti supplies 3,781 of 4,746 test signatures, at
    +0.1698. Without kisti the cell is +0.0052, a tie. Leaving out any other
    dataset keeps it `rule wins`. Disagreements: 724 rule-right-vote-wrong,
    77 vote-right-rule-wrong.
  - INIT >= 0.5 x SV = 0: 0 rule-right-vote-wrong, 290 vote-right-rule-wrong.
    It stays `k-NN wins` with any one dataset left out.
- **Experiment 1** (`phase2_9b_exp1_clean_intervals.csv`, read with
  `git show v1.1.0:...`). There are 240 rows and 120 clean ones. **115 of 120**
  have the interval inside +-0.02. Outside are seeds 31001, 31016, 31009, 31014
  and 31005, and every one crosses +0.02 on the high side.
- **File times (O3).** These are times on the author's machine, not repository
  evidence. The evaluation-split prediction cache `phase2e_eval_sigs.parquet`
  was born at 13:27:30.05, 22 min 48 s after `3e79a48`. `phase2e_mech.py` was
  born at 13:19:17 and `phase2e_run.py` at 13:21:53, and both were first
  imported at 13:22:07. No trace puts an evaluation prediction of the amended
  pair before the addendum, so the amendment's stop condition was not hit. No
  temp folder, transcript or file-history snapshot from 2026-09-18 survives.
  The limits of birth times are spelled out in the report.

### Invariant checks

- **Invariant 3** (held-out only): every number is evaluation-split, from the
  frozen held-out per-block record.
- **Invariant 5** (no result before measurement): every number comes from
  committed code with halting checks. Two consecutive runs gave identical
  hashes for all six CSVs and the report. A rerun keeps the hand-written section
  byte for byte. The 115/120 count, flagged at 2.9a as not yet from committed
  code, now is.
- **Invariants 2, 4, 6, 7:** untouched. The script is offline. Its one
  subprocess is a local `git show`.
- **Invariant 8** (honest framing): no hypothesis outcome moves. The W2 and W1
  findings are one-dataset findings under `PREREG.md:531-535`, reported for
  WO-2 and not edited into the paper here.
- **Confidentiality:** all new and changed text was checked case-insensitively
  against the private name-scan list, with zero hits. One phase-2 reflog line
  matched a term and is withheld. Only the count is recorded.
- **Side effects:** `../scan_terms.txt.txt` was renamed to `../scan_terms.txt`,
  outside the repository, with the author's approval. The 2.2e `.pyc` times
  were checked before and after the runs and are unchanged.

**Recommendation for the next pass.** WO-2, the manuscript corrections, once
the author has ruled on N3 and N4. Three results are firmer than the plan's
PREVIEW expected, and the WO-2 wording should use the committed verdicts. The
zbmath whole-population result is decided (`k-NN wins`), not "near the
boundary". In pooled non-inspire, [0, 0.5) x SV high and the marginal SV-high
band are `rule wins` at 0.05, not boundary cases. The marginal band clears the
margin by 0.0001, so it should be reported with its lower bound, not as a
robust win.

## Pass 24 — Phase 2.9b step 2, the manuscript corrected against the 2.9a and 2.9b records (2026-11-12)

**What I did and why.** I executed work order WO-2 of the release-pass master
plan (`../FABLE_MASTER_PLAN.md`) with the orchestrator's overrides, then the
orchestrator's review fixes (WO-2b). The goal is a `main.tex` that says only
what the committed records support. Decisions N3 and N4 were approved, both
option (a). Questions Q1 and Q2 have no answer, so the plan's either-way wording
is used. Files changed: `paper/main.tex`, `paper/references.bib` and the
regenerated `paper/main.bbl`. No script, `PREREG.md`, report, table or figure
changed, and the locked 6.4 quote is untouched.

### Edits applied

- **E1 to E20**, as written in the plan, except where an override replaced a
  passage. In brief: abstract (E1); the WDC sentence (E2); section 1.3 and the
  contributions (E3, E4); the winning construct (E5); section 4, now "A
  comparison only one side can win", with the identity condition stated and
  the second region narrowed to surface-only mechanisms (E6, E7); sections 5.1
  and 5.2 (E8); sections 6.1 and 6.3, the calibration-split uses and the power
  floor wording (E9); section 6.4, now eight points of record with three new
  corrections (`a41a67a`, the calibration split, "any similarity function") and
  the run timing (E10); results corrections (E11 a to h); block size and the
  INIT control (E12); the new subsection 7.8 "Two datasets are not like the
  pool", label `sec:per-dataset` (E13); sections 7.9 and 8.1 (E14); the 42.2%
  share (E15); section 8.3 and the bibliography (E16); Appendix A (E17); the
  S2AND redistribution sentence (E18); the conclusion (E19); the generative-AI
  disclosure (E20).
- **Overrides O-E1 to O-E20** from the WO-2 prompt: O-E1, O-E2, O-E3 (a, b),
  O-E4 (items 1, 2), O-E6 (section 5 retitled "A pair either side can win"),
  O-E10 (a, b), O-E11a, O-E11h, O-E12, O-E13 (the whole new subsection, plus
  the section 9 pointer), O-E14 (a, b), O-E16, O-E19 (a, b), O-E20.
- **One placement change in E8, reported at WO-2.** Applied literally, the
  `:511-513` replacement would have left ", with mechanism A unchanged in all
  three pairs" hanging on the new cross-reference sentence. The clause was moved
  to the end of the preceding sentence. No word was added or removed.
- **Review fixes R1 to R14** (WO-2b). R1 removes the repeated identity condition
  in 1.3. R2, R3, R4 (four places, including the 7.7 title), R6 and R7 (two
  places) scope every "only signal" and "no design-time signal" claim to the
  seven-dataset pool. R5 shortens the INIT sentence. R8 brings the 8.2
  calibration warning in line with E4. R9 says "reserved for a single use". R10
  removes the repeated rule-side count in 5.2. R11 says the third point of
  record was extended at release, and names the reported run. R12 rewords the
  7.8 sentence whose 8.1 and conclusion targets were removed. R13 spells out
  "five". R14 gives `adscascade2026` a `\doi` in its note, because plainnat
  prints no DOI for `@misc`. All 18 passages matched exactly once, by words,
  and none lies inside the locked quote.
- **Bibliography.** 27 entries. `adscascade2026` cites v1.1.0
  (`10.5281/zenodo.22258609`) and is marked deprecated. `primpeli2019wdc` and
  `sinha2015mas` are added as Block F from the Crossref records in
  `reports/phase2_9a_report.md` A5. Sinha's booktitle is Crossref's container
  title, without "Companion". Pages were added for `hendrickx2024`, `s2and2021`
  and `backes2018`.

### Every number added, with its source

Every value was checked against its table before use. None differed.

| Value | File | Row |
|---|---|---|
| 0.1131 [+0.1015, +0.1250], 1,219 / 71 | `reports/tables/phase2_9b_population_verdicts.csv` | kisti |
| -0.0631 [-0.0761, -0.0512], `k-NN wins` | same | zbmath |
| pubmed `rule wins`, 34 blocks | same | pubmed |
| +0.1762, +0.1100, +0.0806, +0.1654; tie at ADS 1.0 and SV = 0 | `phase2_9b_bands_by_population.csv` | kisti, ADS [0,0.5) and [0.5,0.7); SV mid and SV high |
| -0.0976, -0.1137 | same | zbmath, ADS 1.0 and SV = 0 |
| SV-high lower bound 0.0501 ("by 0.0001") | same | pooled non-inspire, SV high |
| ADS bands below 1.0 and every SV band tie; ADS 1.0 `k-NN wins` with 0 rule-right | same | non-inspire without kisti |
| +0.0629, +0.1024, -0.1130 | `phase2_9b_cells_by_population.csv` | pooled non-inspire, [0,0.5), [0.5,0.7) and 1.0 x SV high |
| winner reversal at 0.05; in the seven-dataset pool only at 0.02 | `phase2_9b_structure_by_population.csv` | pooled non-inspire and all, across ADS at fixed SV high |
| 0.1299, 0.0221 | `phase2_9a_matched_precision.csv` | kisti, zbmath (`matched_diff`) |
| 0.8359, 0.0153 [+0.0142, +0.0165]; 0.9230, 0.9388, 0.9130, 0.9172, 0.9375, 0.9456, 0.7076 | same | pooled; the seven size bands (`knn_acc_fired`) |
| +0.0066, +0.0018, -0.0183 | `phase2_9b_init.csv` | INIT band alone |
| 3,781; +0.0052, tie; 0 rule-right | same | INIT=0 x SV high, kisti alone and kisti left out; INIT>=0.5 x SV=0 |
| -0.1071 [-0.1237, -0.0912]; +0.1363 [+0.1182, +0.1557] | `phase2e_pooled_init_sv.csv` | INIT>=0.5 x SV=0; INIT=0 x SV high |
| 115 / 5 | `phase2_9b_exp1_clean_intervals.csv` | `inside_margin_0.02` count; `paired_diff` is rules minus retrieval (`v1.1.0:scripts/experiments/exp1/stats.py`) |
| 0 / 3,029; 0 / 696; 835 | `phase2_9a_region_counts.csv` | ADS 1.0; SV = 0 |
| 42.2% | `phase2_9a_contested_share.csv` | evaluation |
| r = 0.95; k = 2 at 181 / 736 | `phase2c_pair_twosidedness.csv` | radius@0.95, knn@2 |
| +0.2725 [+0.0093, +0.4691], 97.8% | `phase2_7b_driver_bootstrap.csv` | k = 2, `adj_*` (share 0.9775) |
| 0.3972 / 0.3443, 0.4114 / 0.3418 | `reports/phase2e_boundary.md:272-273` | block-weighted, delta 0.03 and 0.02 |
| 0.9889, 0.9234 | `reports/phase2e_boundary.md:114` | ADS 1.0 |
| 90.7% | `reports/gate2_ads_range.md:178` | 1.0 exactly |
| 210,537 | `reports/phase2_9a_report.md:192` (B4) | distinct-form pairs |
| 0.8441; 0.0147 (0.8441 - 0.8294) | Table 2 in `main.tex` (`phase2e_twosidedness_eval.csv`) | retired pair |
| 0.8953, 0.7826, 11,110 of 13,902 | Table 3 in `main.tex` (`phase2e_accuracy_by_population.csv`) | zbmath coverage, kisti agreement, inspire blocks |
| about 17, 23 and 40 minutes (13:22:07, 13:27:30, 14:07:22) | `reports/phase2_9b_report.md`, "Local file times" | launch proxy, cache birth, last edit; crash fix and tolerance per `PASSLOG.md:1460-1468` |

The O-E10(b) sentence was checked against the frozen H2 Supported row
(`git show 8869b82:phase2/PREREG.md`), which reads "or all such verdicts are
tie or undecided".

### Anti-ai passes

The project skill `.claude/skills/anti-ai` was run on added and replaced
passages only.
- WO-2: two changes.
  - 7.8, last paragraph: "Three things follow. The sentence that the choice
    barely matters..." became "The sentence that the choice barely matters...".
  - O-E11h: "carries one more comparison worth reading here." became
    "carries one more comparison."
- WO-2b: no change.

### Checks

- **Build** (pdflatex, bibtex, pdflatex, pdflatex): zero LaTeX warnings, zero
  undefined references and citations, and bibtex reports no warnings. That is
  the same as a clean build of `f2f3add`. The paper is 31 pages, against 27 at
  `f2f3add`.
- **Locked quote:** sha256 `dcaa1bc…f8f4`, unchanged. STATE records it at
  line 77, not line 50 as the prompt said.
- **R14:** the built reference reads "Zenodo, doi: 10.5281/zenodo.22258609".
- **Leftover phrases:** every PDF line with "no design-time signal", "only
  signal", "carry a decided" and the rest was read. Each is either scoped to
  the pool, or is a per-block count, or is the "stated flat" sentence it
  qualifies.
- **Zero hits** in `main.tex` outside comments: `0.0218`, `external read`,
  `redistribute none`, `41\%`, `used once`, `cannot have a winner`, `A pair
  that can`, `one dataset departs`, `the metric family or the tie-break`, the
  token bracket, the em dash, `---`.
- **Scripts:** `git diff --stat f2f3add -- 'phase2/*.py'` is empty.
- **Invariants.** 5: every new number is from a committed table. 8: no
  hypothesis outcome moved. H1 is Supported, H2 and H3 are Inconclusive, and
  the per-dataset results are reported as one-dataset findings under
  `PREREG.md:531-535`.
- **Confidentiality:** every added line in the four committed files was checked
  against the private name-scan list, case-insensitively. There are zero
  whole-word hits. The nine substring hits all sit inside ordinary English
  words, the same ones that already match 20 times in the `f2f3add`
  manuscript. Neither "production engagement" nor "production deployment"
  appears.

**Recommendation for the next pass.** WO-3, the release files, the errata and
the Phase 1 tip deletion. Two small items for the author first. The
section 6.4 sentence on the repository being pushed, and the tense of the
availability paragraph, belong to WO-6, as planned. And the per-dataset
subsection says "We do not know what makes kisti different"; Q3 is the place
to replace it if the author has a reason the data supports.

## Pass 25: Phase 2.9c, release files, licences, errata and the tip removal (2026-11-12)

**What I did and why.** I executed work order WO-3 of the release-pass master
plan in two steps. WO-3a prepared everything and committed nothing, so the
orchestrator could review it first. WO-3b applied four review fixes and made the
two gate 2.9c commits. The goal is a tip that a stranger can reproduce and
cite, with none of the deprecated earlier tree in it. No script,
`PREREG.md`, report, table, figure or paper file changed.

### What WO-3a prepared

- **New files.** `README.md` (what the paper is, the three outcomes, the build,
  the CPython 3.14.2 environment, the run order with outputs, the self-check
  statement, the record, the project log, a three-line deprecation section,
  the licences), `requirements-lock.txt` (seven exact pins, confirmed with
  `importlib.metadata`), `DATA_LICENSES.md`, `ERRATA.md`, and `LICENSE-TEXT`
  at the root (CC BY 4.0 for `phase2/paper/` and `phase2/reports/`, with a
  carve-out for the derived data files, including the two
  `reports/tables/*_blocks_scored.csv.gz` tables).
- **DATA_LICENSES.md.** S2AND: the README's licensing lines quoted from
  https://github.com/allenai/S2AND, ODC-BY, and the six derived files with
  their columns and row counts, which agree with the paper's availability
  paragraph. Microsoft Academic Graph: "Open Data License: ODC-BY" and the
  https://aka.ms/msracad request, quoted from Microsoft's archived docs
  repository, because the hosted page now returns 404. WDC LSPC 2017: the
  source states no licence (the v2 page has no terms, and the Hugging Face card
  says `license: unknown`), so the file is kept under decision N2, described
  as used only for the section 1.2 substrate check and removable on request.
  All sources were read on 2026-11-12.
- **ERRATA.md.** Six entries: the four O9 statements ("at every k", "written
  one way" for any pair, "nothing is redistributed", the calibration split
  "reserved"), the per-dataset form that `reports/phase2e_boundary.md` lacks,
  and Q2, who drafted the locked 6.4 text (`PLAN.md:164`). The author does not
  recall. The assistant drafted most text, as the paper's disclosure says, and
  the paper's own passive sentence stands.
- **Dated notes.** `CLAUDE.md`: the mission paragraph's two narrowed statements,
  and the non-goal line reworded so that it names no earlier engagement.
  `PLAN.md`: the same two statements, and the Q2 note at the 6.4 status line.
  `STATE.md`: "at every k".
- **Commit 2 drafts**, outside the repository: root `README.md`,
  `CITATION.cff` (the Phase 2 paper as `preferred-citation`, `type: article`,
  DOI placeholder), `.gitignore` (Phase 1 stanzas dropped) and a two-line
  `CLAUDE.md`, plus the `git rm` list checked against `git ls-tree`.

### Review fixes (WO-3b)

Each one replaced a single exact passage that matched once.

- **F1.** `README.md`, the H2 and H3 bullets, now worded as the paper's outcome
  table has them.
- **F2.** `README.md`, the structural sentence, now with its condition: the
  similarity gives its maximum only to identical strings and the two
  mechanisms share a tie-break.
- **F3.** `README.md`, "Earlier work, deprecated", now one line. It says section
  8.3 of the paper discusses the earlier study and cites `v1.1.0`. The 8.3 is
  `sec:earlier-synthetic` as printed in `paper/main.aux`.
- **F4.** `DATA_LICENSES.md`, the Sinha et al. venue, now as in
  `references.bib` ("WWW '15", no "Companion"). The Microsoft quote is
  unchanged.

### Anti-ai passes

WO-3a, over the new prose and the dated notes: no listed vocabulary, connective
or em dash was found. Six changes were made, all to sentence shape. The README's
tests sentence was split. The optional raw-data chain became a numbered list.
Two long DATA_LICENSES sentences (the MAG source, the WDC source) were split.
ERRATA entry 6 was reordered so that "is passive" comes before the quote. "Two
statements ... are narrower on the record" in the `CLAUDE.md` and `PLAN.md`
notes became "The record narrows two statements". The before and after texts are
in the WO-3a review bundle, section 6. WO-3b ran the same pass over F1 to F4,
this entry and the STATE updates. F1 to F4 were left verbatim, and the two
changes to this entry are listed in the WO-3b reply.

### Checks

Run on the prepared state at WO-3a, and again here before commit 1.

- **Name scan**, whole words, against the term file outside the repository: no
  hit in any new or changed file, in any root draft, or in the post-removal
  tip. As a control, it finds the 8 files of the confidentiality audit's 7f.3
  among the files being removed.
- **Leftover wording**, the four-term check of the WO-3 acceptance list: no
  hit in any new file, draft or dated note. One line
  at the tip still matches, `PASSLOG.md:3333`. It is an earlier pass's own scan
  result, which states that the terms do not appear. It is kept as written,
  like the rest of the record, and it names no client and makes no production
  claim. The charter's non-goal line no longer matches.
- **Scripts.** `git diff --stat 306557a -- 'phase2/*.py'` is empty.
- **Pins.** All seven match `importlib.metadata` on CPython 3.14.2.
- **`.gitignore` dry run.** Against a listing of the 403 files in the
  repository folder, 90 are ignored under the old file and the same 90 under
  the new one. Nothing becomes untracked, and no path kept after the removal is
  ignored.
- **Phase 2 only.** From a `git archive HEAD phase2` copy, all 17 modules
  import, and `phase2e_mech.py` passes its self-check and the calibration-split
  regression check (546 against 744 at k = 5).
- **Tables.** No tracked table under `reports/tables/` other than the two
  `*_blocks_scored.csv.gz` holds a block-key value (64 tables, 20,275 keys).

**Recommendation for the next pass.** The removal commit, then WO-4, the cold
run from a fresh clone. WO-4 fills the `<cold run>` times in `README.md`, and
WO-6 fills `<DOI>`.

### Addendum: commit 2, the tip removal

Commit 1 is `47c6cb3`. Commit 2 removes the deprecated earlier tree from the
tip: 137 files deleted, all outside `phase2/`, with the four root files
`README.md`, `CITATION.cff`, `.gitignore` and `CLAUDE.md` replaced
by the reviewed drafts, byte for byte. History keeps every removed file. The
dangling-path search ran before the commit, over `README.md`,
`DATA_LICENSES.md`, `ERRATA.md`, `paper/main.tex`, the four root files and
every `phase2/*.py`, 25 files in all. It looked for a `../` path to a removed
directory, a removed root file name, a Python parent join into a removed
directory, and a top-level removed path in a root file. It found no hit. The
checks after the commit are in the WO-3b reply and go into WO-4's entry.
Both 2.9c commits were re-made before any push, without the co-author trailer,
at Markie's direction; their content is otherwise unchanged.

## Pass 26: Phase 2.9c, cold reproduction from a fresh clone (2026-11-12)

**What I did and why.** I executed work order WO-4 of the release-pass master
plan, then WO-4b. WO-4 ran the README's run order from a fresh clone, with no
cache, to test B3: does the tip reproduce for a stranger who has only the
README? It ran and prepared, and committed nothing. The orchestrator reviewed
the bundle, ruled on the one open call, and asked for all five README findings
to be fixed. WO-4b applied that and made this commit. No script, `PREREG.md`,
existing report, table, figure or paper file changed.

### WO-4, the cold run

- **Source.** H = `1ef28d2` on `phase-2`, cloned with `git clone
  --no-hardlinks --branch phase-2` outside the working repository. The clone
  had both tags and neither mechanism cache.
- **Environment.** A new venv made with the README's commands: CPython 3.14.2,
  64-bit, Windows; the seven pins from `requirements-lock.txt` and nine
  unpinned dependencies (the full `pip freeze` is in the report). Windows 11
  Home 24H2, Intel Core i5-6200U (2 cores, 4 threads), 16 GB RAM.
- **Times.** Steps 1 to 9: 1 s, 3 min, 10 min, 15 s, 12 s, 4 min, 40 s,
  22 s, 24 s, 19 minutes in all. Steps 3 and 6 built their caches. Paper
  build 12 s. Raw path: fetch 3 min, ingest 50 s, `gate21_two_axes.py`
  4 min.
- **Self-checks.** All passed. The frozen record re-derives: 199,713 test
  signatures, 546 against 744 at k = 5, per-block verdicts
  191 / 309 / 10,172 / 3,230, and H1 Supported, H2 and H3 Inconclusive.
- **Comparison.** 108 of 108 output files match in content: 94 from the main
  run (including the two gitignored caches, compared with the reported run's
  local copies), 13 from the raw path, and `main.bbl`. No file differs in
  content, and none differs only as PNG bytes. All 26 PNGs are
  byte-identical. Below content level, on Windows the scripts write CRLF
  where the checkout has LF, so `git status` lists 78 rewritten files with
  no diff, and the four `.csv.gz` files differ in their gzip header time.
- **Raw path.** The manifest totals 260,176,690 bytes, under the 1 GB limit,
  so it ran. All 19 downloads match the committed sha256 and size, and the
  one 404 entry is still a 404. The rebuilt manifest, signature table, block
  tables, gate 2.1 reports and figures all match.
- **Paper.** Built in the clone: 31 pages, no undefined reference or
  citation.
- **Report.** `reports/phase2_9c_cold_run.md`: environment, commands, times,
  the 108-row comparison table, the differences below content level, and
  the README findings.

### Rulings (WO-4b)

- **R1.** The constants check is a pass. The regenerated
  `phase2b_constants.py` has CRLF line endings on Windows. `git diff
  --exit-code` is clean and `git hash-object --path` gives the committed blob
  `7440cef`. R4 asks whether the frozen constants reproduce, and git's blob is
  the record. The report's sentence leaving the call open was replaced.
- **R2.** All five README findings are fixed in this commit, and the report
  says so.

### README fixes (WO-4b)

Each one replaced a single exact passage that matched once.

- **F1.** The run-order lead now says to run `python phase2/<script>` from
  the root, and that script names and output paths are relative to `phase2/`.
- **F2.** Step 4's row no longer lists `reports/phase2c_pair_probe.md`, which
  `phase2c_probe.py` never writes. The note about one new untracked file is
  gone. A search of `README.md`, `DATA_LICENSES.md`, `ERRATA.md` and
  `paper/main.tex` found the file named only in those two README places.
- **F3.** The constants note now names `git diff --exit-code` as the check.
  A new note says Windows writes CRLF, so `git status` lists files with no
  diff, and the `.csv.gz` files are compared decompressed.
- **F4 and F5.** After the venv commands, a paragraph says to confirm 3.14.2
  with `python -VV`, and gives the PowerShell execution-policy command and
  the `cmd` form of activation.

WO-4's own README change, kept: the nine Time cells from this run and one line
naming the machine.

### Anti-ai passes

WO-4, over the report and the new README line: no listed vocabulary or em dash.
Four changes to wording. A sentence restating the opening was cut, and the
two sentences on byte-level differences were joined. The constants judgment
was recast as a plain clause after a colon. The README's earlier "about 20
min" became its own sentence. "From one cold run from a fresh clone" became
"of a fresh clone". The texts before and after are in the WO-4 review bundle.
WO-4b, over R1, R2 and F1 to F5: nothing to change, so they went in verbatim.
The same pass over this entry and the STATE line changed nothing either.

### Checks

Before the commit, on the prepared state.

- **Name scan**, whole words, against the term file outside the repository:
  no hit in the report or the README change.
- **Personal paths.** No user name, application-data folder or home-folder path in the
  report or the README.
- **Changed files.** Only `README.md` (modified) and the report (new) at
  WO-4, then these two plus `PASSLOG.md` and `STATE.md` here.
- **Paper in the clone.** 31 pages, 0 undefined references or citations.

The checks after the commit are in the WO-4b reply and go into WO-5's entry.

**Recommendation for the next pass.** WO-5, the independent verifier, in a
session that wrote none of the release-pass work. Then WO-6 fills `<DOI>`.
