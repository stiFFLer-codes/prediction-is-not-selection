# Data licences

This repository's code is under MIT (`LICENSE`). The paper and the reports are under CC BY 4.0 (`LICENSE-TEXT`). The derived data files listed below are not covered by either. Each one carries the terms of its source, as set out here. Every source was read on 2026-11-12.

## S2AND

**Source.** S2AND, the Semantic Scholar Author Name Disambiguation benchmark, released by the Allen Institute for AI. The repository downloads it from AI2's public bucket, `s3://ai2-s2-research-public/s2and-release`, over its HTTPS endpoint `https://ai2-s2-research-public.s3.amazonaws.com/s2and-release/`. `data/MANIFEST_s2and.json` records the sha256 of every file taken. The raw release is not in this repository.

**Citation.** Shivashankar Subramanian, Daniel King, Doug Downey and Sergey Feldman. 2021. S2AND: A Benchmark and Evaluation System for Author Name Disambiguation. In *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (JCDL)*, 170-179. doi:10.1109/JCDL52503.2021.00029.

**Licence.** The S2AND README, section "Licensing", at https://github.com/allenai/S2AND (read 2026-11-12), says:

> Package metadata currently declares the Python package license as MIT, while the root `LICENSE` file is CC-BY-4.0. The released dataset is under ODC-BY. Some affiliation data comes directly from the Microsoft Academic Graph.

The release prefix ships its own `LICENSE.txt`, the text of the ODC Attribution License, whose first line is "# ODC Attribution License (ODC-By)". Its sha256 is in `data/MANIFEST_s2and.json`. The licence is at https://opendatacommons.org/licenses/by/1.0/.

**What this repository carries.** Six tables derived from the release. They are redistributed under ODC-BY with attribution to S2AND. Row counts were taken at commit `306557a`.

| File | Rows | Columns |
|---|---|---|
| `data/s2and_signatures.parquet` | 766,133 | `sid`, `dataset`, `signature_id`, `paper_id`, `block_key`, `author_label`, `surface_form`, `s2and_block`, `given_block`, `s2and_full_name`, `first`, `middle`, `last`, `suffix`, `position`, `n_affiliations`, `affiliation`, `has_email`, `s2_author_id` |
| `data/s2and_blocks.csv.gz` | 26,939 | `dataset`, `block`, `n_signatures`, `n_authors`, `n_surface_forms`, `ads`, `surface_variability`, `s2and_homonymity`, `s2and_synonymity` |
| `data/s2and_blocks_s2and_key.csv.gz` | 27,658 | the same nine columns as `s2and_blocks.csv.gz`, keyed by S2AND's shipped block |
| `data/phase2b_blocks.parquet` | 18,984 | `dataset`, `block_key`, `n_train`, `ads`, `sv`, `sv_resid`, `init`, `n_train_forms`, `n_train_authors`, `block_index`, `block_size`, `is_cal`, `n_test` |
| `reports/tables/phase2b_blocks_scored.csv.gz` | 13,902 | 54 columns: `dataset`, `block_key`, the block signals of `phase2b_blocks.parquet`, and per-block counts, accuracies, bootstrap intervals and verdicts for the 2.2b pair |
| `reports/tables/phase2e_blocks_scored.csv.gz` | 13,902 | 91 columns: `dataset`, `block_key`, the block signals of `phase2b_blocks.parquet`, and per-block counts, accuracies, bootstrap intervals and verdicts for the 2.2e pair at k = 2, 3, 5 and 10 |

The signature table holds one row per author mention, with the name fields, the block key, the author label and the affiliation string. The other five are per-block tables keyed by a normalized name (`block` or `block_key`). The paper's availability statement describes the same two kinds of table. Every other table under `reports/tables/` holds aggregates only, with no name or block key.

**Microsoft Academic Graph.** Some of the `affiliation` strings come from the Microsoft Academic Graph, as the S2AND README says. Microsoft documents the graph's schema in `academic-services/graph/reference-data-schema.md`, in the archived MicrosoftDocs repository at https://github.com/MicrosoftDocs/microsoft-academic-services/blob/live/academic-services/graph/reference-data-schema.md (read 2026-11-12). That page carries this heading and request:

> Open Data License: ODC-BY
>
> When using Microsoft Academic data (MAG, MAKES, etc.) in a product or service, or including data in a redistribution, please acknowledge Microsoft Academic using the URI https://aka.ms/msracad.

The page that the documentation used to be served from, https://microsoftdocs.github.io/MAG/Mag-ADLS-Schema, now redirects to a Microsoft Learn page that returns 404. The quote above comes from the documentation's source file in Microsoft's repository.

As that page asks: this repository includes data from Microsoft Academic, https://aka.ms/msracad.

Citation for the Microsoft Academic Graph: Arnab Sinha, Zhihong Shen, Yang Song, Hao Ma, Darrin Eide, Bo-June (Paul) Hsu and Kuansan Wang. 2015. An Overview of Microsoft Academic Service (MAS) and Applications. In *Proceedings of the 24th International Conference on World Wide Web* (WWW '15), 243-246. doi:10.1145/2740908.2742839.

## WDC LSPC 2017

**Source.** The WDC Training Dataset and Gold Standard for Large-Scale Product Matching, version 2.0 (LSPC 2017), from the Web Data Commons project. `data/MANIFEST.json` records the canonical host, https://webdatacommons.org/largescaleproductcorpus/v2/. The data was taken from the Web Data Commons group's Hugging Face repository `wdc/products-2017` (https://huggingface.co/datasets/wdc/products-2017) at revision `bee4f71ca1bcfc51eb8fc41d65720fb6f487df9d`. The manifest gives the sha256 of each of the twelve files taken.

**Citation.** Anna Primpeli, Ralph Peeters and Christian Bizer. 2019. The WDC Training Dataset and Gold Standard for Large-Scale Product Matching. In *Companion Proceedings of The 2019 World Wide Web Conference (WWW '19)*, 381-386. doi:10.1145/3308560.3316609.

**Licence.** No explicit licence is stated by the source.

- The LSPC v2 page, https://webdatacommons.org/largescaleproductcorpus/v2/ (read 2026-11-12), states no licence or terms of use. Its only instruction to users is "Please send questions and feedback to the Web Data Commons Google Group."
- The dataset card at that revision, https://huggingface.co/datasets/wdc/products-2017/raw/bee4f71ca1bcfc51eb8fc41d65720fb6f487df9d/README.md (read 2026-11-12), gives `license: unknown` in its metadata and has no licence section.

Neither source forbids redistribution, and neither grants it.

**What this repository carries.** One derived extract.

| File | Rows | Columns |
|---|---|---|
| `data/wdc_lspc2017_offers.csv.gz` | 15,179 | `offer_id`, `surface_string`, `key`, `label`, `slice`, `split` |

It is used only for the substrate check reported in section 1.2 of the paper, and nothing in the main analysis reads it. It will be removed on request.
