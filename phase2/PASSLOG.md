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
