# Prediction is not selection

A pre-registered study of design-time mechanism choice in author name disambiguation.

By Maitreya Sapariya ([ORCID 0009-0003-9346-3775](https://orcid.org/0009-0003-9346-3775)).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24184394.svg)](https://doi.org/10.5281/zenodo.24184394)

On seven public author name disambiguation datasets, the study compares a precision-first exact-evidence rule with a coverage-first k-nearest vote, both untrained lookups over a name block's own history. Structurally, a rule that assigns on an exact surface match cannot beat a retriever that takes the single nearest surface form, at any cutoff, whenever the similarity function gives its maximum only to identical strings. Empirically, the rule and the vote score 0.8244 and 0.8294 when the datasets are pooled, and neither pre-registered signal is actionable at the margin fixed in advance; two datasets are decided in opposite directions, kisti for the rule and zbmath for the vote. The consistency statistic still predicts each mechanism's own accuracy. Prediction is not selection.

## Read the paper

The PDF is [`phase2/paper/main.pdf`](phase2/paper/main.pdf), and the archived record is at [doi:10.5281/zenodo.24184394](https://doi.org/10.5281/zenodo.24184394). Preprint, not peer reviewed.

## Reproduce

[`phase2/README.md`](phase2/README.md) gives the environment, the data and the run order. The whole run takes about twenty minutes on a laptop.

## Cite

Use [`CITATION.cff`](CITATION.cff), or cite the DOI [10.5281/zenodo.24184394](https://doi.org/10.5281/zenodo.24184394).

## Licences

- Code: MIT (`LICENSE`).
- Paper, reports and documentation: CC BY 4.0 (`LICENSE-TEXT`).
- Derived data: the terms of each source, set out in `phase2/DATA_LICENSES.md`.

## Earlier work

This repository was earlier named ADS-Cascade. The tags `v1.0.0` and `v1.1.0` hold that work, which is deprecated and kept for the record only.
