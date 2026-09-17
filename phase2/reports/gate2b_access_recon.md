# Gate 2b step 0 — access recon: STOP

**Verdict: stop after step 0.** No feasible first-party public WDC source
carries per-offer (per-shop) raw `schema.org/category` values joinable to
product clusters. Steps 1 to 6 were not run. No data was pulled and nothing was
measured.

Two independent reasons, either of which is sufficient:

1. **The premise does not hold for the WDC LSPC distribution.** The corpus does
   not retain each shop's own `schema.org/category`. The WDC extraction and
   cleansing pipeline keeps identifiers plus title, description, brand, price
   and specification-table content, and nothing else. Its `category` field is
   the output of a single classifier that WDC trained and applied, assigned per
   product, not per shop.
2. **The WDC data hosts are down.** Both `webdatacommons.org` and
   `data.dws.informatik.uni-mannheim.de` refuse connections, as they did during
   gate 1 and gate 2.

Reason 1 is the load-bearing one. Reason 2 alone would justify retrying later;
reason 1 means the retry would not help for LSPC-derived data.

Re-verify both with `python phase2/gate2b_access_recon.py`.

## Host status

| Host | Status |
| --- | --- |
| `webdatacommons.org` | unreachable, connection refused at origin `134.155.98.56:443` |
| `data.dws.informatik.uni-mannheim.de` | unreachable, connection refused (ports 80 and 443) |
| `dws.informatik.uni-mannheim.de` | 200, redirects to `www.uni-mannheim.de/dws/` — group homepage only, hosts no data |
| `huggingface.co` org `wdc` | 200 — exactly one dataset, `wdc/products-2017`, the one already ingested |
| `ir-ischool-uos.github.io/mwpd/` | 200 |
| `github.com/wbsg-uni-mannheim` | 200 — first-party code, no corpus data |

The unreachability is at the origin, not a local network block: an independent
fetcher returns `ECONNREFUSED 134.155.98.56:443` for the same host, while
unrelated hosts resolve and serve normally from here.

## Sources checked

Checked in the order of preference the task set.

### 1. WDC product-categorization datasets — carries no per-shop category

The WDC-25 Gold Standard for Product Categorization is documented on the WDC
group's own website source repo (`wbsg-uni-mannheim/wdc-page`, path
`categorization/index.html`), which is reachable even though the data host is
not.

Two findings kill this source:

**The labels are assigned per cluster by construction.** The gold standard's own
methodology section states that for each category, "the offers assigned to that
category by the transfer learning approach, as well as the offers in the same
cluster, were reviewed and, if they were correctly classified, **all offers in
the cluster were annotated with the class label**." So a single label is stamped
onto every offer in a cluster. This is the authors' own description of the
procedure, and it independently confirms the structural explanation gate 2 gave
for why Framing A is degenerate.

**The offer records carry no category property.** The WDC group commits sample
files for each downloadable artifact to its website repo. Scanning all four for
any category-like schema.org property:

| Sample file | schema.org properties present | category-like property |
| --- | --- | --- |
| `categories_gold_standard_offers_sample.json` | `/availability`, `/brand`, `/description`, `/image`, `/manufacturer`, `/name`, `/price`, `/priceCurrency`, `/title` | **NONE** |
| `categories_clusters_training_sample.json` | flat record, no raw properties | **NONE** |
| `categories_clusters_testing_sample.json` | flat record, no raw properties | **NONE** |
| `amazon_training_sample.json` | flat record, no raw properties | **NONE** |

The gold-standard offer records do preserve raw per-offer
`schema.org_properties` with the actual terms each shop used, which is exactly
where a per-shop `/category` would appear if WDC had extracted one. It does not
appear. The two `categories_clusters_*` files are one row per *cluster* with a
single `categoryLabel`, confirming the cluster-level design again. The
downloadable `categories_offers_en_clusters.csv` is just
`(predictedLabel, cluster_id)` — classifier output at cluster granularity.

Sample sizes are 10 records each, so this is corroborating rather than
conclusive on its own. It agrees with the corpus schema documentation below,
which is conclusive.

### 2. Full raw Product Data Corpus (LSPC v2, 2017 — matches our clusters) — carries no per-shop category

The authoritative field list, from the WDC group's own corpus documentation
(`largescaleproductcorpus/v2/index.html`, section 2.2 "Schema of the Corpus"),
is complete and short:

```
id, cluster_id, identifiers, category, title, description, brand, price, specTableContent
```

The `category` field is documented verbatim as "One of 25 product categories the
product was assigned to, NaN if not part of the English subset", and section 2.1
states plainly: "**We learn a classifier** for assigning each offer to one of 25
top-level product categories."

So `category` in every LSPC v2 artifact — full corpus, English subset, gold
standards, training and validation sets — is a machine label from one model,
attached to the product. It is not the shop's annotation, and there is no second
field holding the shop's annotation. This is the same coarse, cluster-constant
field already present in the ingested `wdc/products-2017` table, and it is why
Framing A was dead.

Independent confirmation that our ingest reconstructed the right universe: the
corpus documentation states the gold standard "consists of offers for **2485
products (ID-clusters)**", which matches the 2,485 clusters gate 1 recovered
exactly.

All download URLs for this corpus point at `data.dws.informatik.uni-mannheim.de`
and are therefore dead as well.

### 3. WDC Products 2022 benchmark — same fields, same dead host

`github.com/wbsg-uni-mannheim/wdcproducts` is reachable but contains only code;
its `download_datasets.py` and README point exclusively at
`webdatacommons.org/largescaleproductcorpus/wdc-products/`. Derived from the
same corpus, so the same field set applies. Not usable.

### 4. MWPD challenge Task 2 — has per-shop category, but cannot be joined

This is the one WDC-derived source that does carry the signal. Its Task 2
(product classification) records include a **`CategoryText`** field, documented
as the "website-specific product category, or breadcrum" — genuinely the shop's
own raw category or breadcrumb text. The site is reachable.

It still fails, for a reason unrelated to host status:

- **No cluster ids.** Records carry `ID`, `Name`, `Description`, `CategoryText`,
  `URL` and the GS1 targets `lvl1`/`lvl2`/`lvl3`, with no cluster or product
  identifier linking offers of the same product.
- **One record per product.** Roughly 16k instances across train, validation and
  test, each a single offer. Even with a join, there would be no second shop's
  category for the same product to disagree with.

Within-cluster category disagreement is therefore not measurable here, at any
normalization strength. The data shape forbids the measurement, so steps 3 to 6
would have nothing to compute.

It is also distributed via Google Drive and a `bit.ly` link rather than
first-party WDC hosting, and it is derived from WDC's 2014 classification
dataset rather than the 2017 corpus our clusters come from.

### 5. Language-modelling product corpora — best candidate, host dead

The `productCategorization` repo README points at a third artifact whose paper
abstract describes "large numbers of related product offers together with **the
heterogeneous categorization information from the original web shops**". That
phrasing is the closest match to what gate 2b needs of anything found.

It is hosted at
`data.dws.informatik.uni-mannheim.de/largescaleproductcorpus/data/languagemodelling/`
— unreachable. Because the host is down, its actual field list could not be
confirmed, and the corpus documentation above gives reason to doubt that a
per-shop category column survives the same extraction pipeline. This is the one
source worth re-checking when the host returns, but it should be treated as
unverified, not as a known-good fallback.

## Zenodo and other first-party routes

A Zenodo search for Web Data Commons returns 11 records, all third-party
analyses by unrelated authors (property and datatype usage datasets, characteristic
sets, embedding repositories). The WDC group publishes no product corpus on
Zenodo. No first-party alternative host exists.

Per instruction, no third-party mirrors were used or considered.

## What would change this verdict

In priority order, when `webdatacommons.org` or
`data.dws.informatik.uni-mannheim.de` becomes reachable:

1. Check the language-modelling product corpora for a per-shop category column.
   This is the only untested candidate that could carry both the signal and a
   cluster join.
2. Download the LSPC v2 corpus sample files
   (`data/v2/samples/offers_corpus_english_v2_sample.json`) and confirm against
   real records that no per-shop category property exists, rather than relying on
   the schema documentation plus 10-record website samples.

Neither is worth waiting on before deciding the framing question, because both
are contingent on a host that has been down across three consecutive passes.

## Recommendation

Gate 2b cannot answer its question on WDC data. The label-disagreement axis this
pass was meant to recover does not exist in the WDC LSPC distribution as
published, so no amount of host availability or normalization design will
produce it.

That leaves the gate 2 recommendation standing unchanged: **Framing B with a
frozen, principled blocking key** is the only measured route to a live ADS axis
on this corpus. Gate 2b's failure removes the main alternative to it rather than
weakening it.

If a genuine per-item label-inconsistency axis is judged essential to the paper,
the honest conclusion is that it has to come from a different dataset, and that
decision belongs with the spec's data section rather than with a normalization
choice. The spec's secondary dataset — a Magellan "Dirty" benchmark from
HuggingFace or Zenodo record 8164151 — is reachable and is the natural place to
look next, but evaluating it is a scope question for review, not something this
pass should decide.

**Stopping for review as instructed.**
