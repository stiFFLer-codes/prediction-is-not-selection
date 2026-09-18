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
