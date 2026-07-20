# Model Card: FAIR-SSF-Opt

## Purpose

The prototype tests whether literature-derived solid-state fermentation data
can support reproducible AI modelling while respecting experimental and
article-level grouping.

## Models

- median dummy regressor;
- random forest regressor;
- extra-trees regressor.

The target is transformed with `log1p` during training and converted back to
the original activity scale for evaluation.

## Benchmark 1: within-study multi-enzyme model

- Source cohort: Reference 10 in the workbook;
- Records: 119 numeric enzyme outputs;
- Experiments: 30;
- Enzymes: CMCase, beta-glucosidase, xylanase, beta-xylosidase;
- Validation grouping: experiment ID.

Keeping all outputs from one experiment in the same fold prevents leakage
between enzyme measurements sharing identical process conditions.

Preliminary local run with 8 repeated group splits selected random forest:

- median MAE: approximately 41.9 activity units;
- median absolute error: approximately 10.0;
- median RMSE: approximately 94.4;
- median R-squared: approximately 0.32;
- five-fold grouped out-of-fold R-squared: approximately 0.29.

These values are illustrative and are recomputed by the pipeline.

## Benchmark 2: cross-study xylanase model

- Cohort: xylanase measured in U/gds;
- Records: 60;
- Scientific references: 16;
- Validation grouping: complete article reference.

Preliminary grouped results were weak, with negative out-of-fold R-squared.
This is not hidden: it demonstrates that article-specific protocols,
incomplete metadata, unit conventions, and dataset imbalance limit model
transportability.

## Uncertainty

The dashboard interval is derived from group-bootstrap model predictions. It
reflects sensitivity to the sampled experimental or article groups, not total
scientific uncertainty.

## Intended interpretation

- Within-study performance shows the potential of standardized data capture.
- Cross-study degradation shows why FAIR metadata and common process schemas
  are prerequisites for consortium-scale reusable AI.
- A prediction is a research demonstration, not an operating recommendation.

## Ethical and scientific limitations

- No causal effect is established.
- Missing metadata can create hidden confounding.
- High-cardinality organism and substrate labels create sparse combinations.
- The data are literature-derived rather than generated under one protocol.
- Experimental validation is required before process decisions.
