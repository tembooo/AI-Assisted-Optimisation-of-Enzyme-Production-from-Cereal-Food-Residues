# AI-Assisted Optimisation of Enzyme Production from Cereal Food Residues

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Software License: MIT](https://img.shields.io/badge/Software%20License-MIT-green.svg)](LICENSE)
[![Dataset License: CC BY 4.0](https://img.shields.io/badge/Dataset%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE_DATA.md)
[![Dataset DOI](https://img.shields.io/badge/DOI-10.17632%2Fk2xv3yss8m.2-blue.svg)](https://doi.org/10.17632/k2xv3yss8m.2)
[![Project Status](https://img.shields.io/badge/status-functional%20research%20prototype-orange.svg)](#project-status)

## FAIR-Aligned, Uncertainty-Aware Machine Learning for Circular Enzyme Production via Solid-State Fermentation

> **Research question:**  
> Can FAIR-aligned machine-learning models predict enzyme production from cereal food residues and identify promising solid-state fermentation conditions for circular bioprocessing?

FAIR-SSF-Opt is a research-oriented machine-learning prototype for studying enzyme production from cereal residues, food-waste-derived substrates, and agro-industrial side streams through fungal solid-state fermentation.

The repository demonstrates an end-to-end workflow that begins with a real literature-derived Excel database and continues through data preservation, data cleaning, FAIR-oriented documentation, cohort construction, feature engineering, leakage-aware validation, model comparison, uncertainty estimation, result reporting, and an interactive Streamlit dashboard.

The project was designed as a portfolio prototype for research at the intersection of:

- artificial intelligence and machine learning;
- FAIR research data management;
- circular food production;
- food and bioprocess systems;
- solid-state fermentation;
- agricultural and food-waste valorisation;
- uncertainty-aware modelling;
- process-data harmonisation;
- scientific reproducibility;
- decision-support and future process optimisation.

The main scientific lesson of the prototype is not simply that a Random Forest can be trained. The more important finding is that model quality depends strongly on how experimental data are structured, documented, grouped, and validated. A model may appear accurate when records from the same experiment or scientific article are split randomly between training and test sets. FAIR-SSF-Opt therefore uses group-aware validation to test whether the model transfers to unseen experiments and unseen scientific articles.

---

# Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Status](#project-status)
3. [What the Project Does](#what-the-project-does)
4. [What the Project Does Not Yet Do](#what-the-project-does-not-yet-do)
5. [Why This Project Matters](#why-this-project-matters)
6. [Relationship to Circular Food and Bioprocess Research](#relationship-to-circular-food-and-bioprocess-research)
7. [Research Questions and Hypotheses](#research-questions-and-hypotheses)
8. [Source Dataset](#source-dataset)
9. [Dataset Citation and Licence](#dataset-citation-and-licence)
10. [Dataset Structure](#dataset-structure)
11. [Initial Data Audit](#initial-data-audit)
12. [Why All 487 Records Are Not Pooled into One Regression Problem](#why-all-487-records-are-not-pooled-into-one-regression-problem)
13. [Experimental Design](#experimental-design)
14. [Experiment 1: Within-Study Multi-Enzyme Benchmark](#experiment-1-within-study-multi-enzyme-benchmark)
15. [Experiment 2: Cross-Study Xylanase Benchmark](#experiment-2-cross-study-xylanase-benchmark)
16. [Complete End-to-End Pipeline](#complete-end-to-end-pipeline)
17. [Data Cleaning and Normalisation](#data-cleaning-and-normalisation)
18. [Feature Engineering](#feature-engineering)
19. [Target Transformation](#target-transformation)
20. [Candidate Models](#candidate-models)
21. [Group-Aware Validation](#group-aware-validation)
22. [Model Selection](#model-selection)
23. [Out-of-Fold Evaluation](#out-of-fold-evaluation)
24. [Uncertainty Estimation](#uncertainty-estimation)
25. [Evaluation Metrics](#evaluation-metrics)
26. [Tested Results](#tested-results)
27. [Interpretation of Results](#interpretation-of-results)
28. [Feature Importance](#feature-importance)
29. [Interactive Streamlit Dashboard](#interactive-streamlit-dashboard)
30. [FAIR Data Implementation](#fair-data-implementation)
31. [Repository Structure](#repository-structure)
32. [File-by-File Explanation](#file-by-file-explanation)
33. [Installation](#installation)
34. [Quick Start](#quick-start)
35. [Full Reproducible Run](#full-reproducible-run)
36. [Command-Line Options](#command-line-options)
37. [Running the Dashboard](#running-the-dashboard)
38. [Running the Tests](#running-the-tests)
39. [Generated Outputs](#generated-outputs)
40. [Reproducibility](#reproducibility)
41. [Responsible AI and Scientific Use](#responsible-ai-and-scientific-use)
42. [Limitations](#limitations)
43. [Troubleshooting](#troubleshooting)
44. [Future Development and Optimisation Roadmap](#future-development-and-optimisation-roadmap)
45. [Suggested GitHub Repository Settings](#suggested-github-repository-settings)
46. [Suggested Interview Answer](#suggested-interview-answer)
47. [How to Cite This Project](#how-to-cite-this-project)
48. [Author](#author)
49. [Acknowledgements](#acknowledgements)

---

# Executive Summary

The source database contains **487 quantified enzyme-production records** obtained from **209 solid-state-fermentation experiments** reported in scientific publications. The substrates include single cereals and mixtures of cereal residues with other food-waste or agro-industrial materials. The records contain information about substrate, microorganism, enzyme, reported yield, activity unit, incubation time, pretreatment, supplementation, optimisation method, selected process parameters, publication year, and scientific reference.

The database is highly relevant to circular food and bioprocess research because it describes the valorisation of cereal residues and related side streams into higher-value enzymes. It is also a useful example of a real consortium-style data problem: data originate from multiple publications, laboratories, organisms, substrates, activity assays, units, and process descriptions.

The prototype performs four main tasks:

1. **FAIR-oriented data preparation**  
   The original workbook is preserved, exported into machine-readable CSV files, documented with metadata, and accompanied by provenance and data-dictionary files.

2. **Within-study prediction**  
   A relatively structured subset from one scientific reference is used to test whether machine learning can predict multiple enzyme activities while keeping all outputs from the same experiment in the same validation fold.

3. **Cross-study prediction**  
   A xylanase cohort with the same reported unit is used to test whether a model trained on some scientific articles can predict records from completely unseen articles.

4. **Uncertainty-aware scenario exploration**  
   The selected model is refitted through group bootstrap resampling. The Streamlit dashboard reports a point prediction together with the 5th and 95th percentiles of bootstrap predictions.

The current implementation shows moderate predictive signal in the within-study benchmark but weak generalisation across scientific articles. This is a scientifically meaningful result. It indicates that AI alone cannot repair inconsistent metadata, incompatible protocols, hidden laboratory effects, sparse categorical combinations, and missing process variables. Reusable AI for circular food systems therefore requires FAIR data capture and modelling to be designed together.

---

# Project Status

**Current release:** `v0.1.0`  
**Status:** Functional research prototype  
**Language:** Python 3.10+  
**Interface:** Command-line pipeline and Streamlit dashboard  
**Data type:** Literature-derived experimental data  
**Primary modelling task:** Regression  
**Validation strategy:** Group-aware validation  
**Uncertainty strategy:** Group bootstrap ensemble

The full pipeline has been executed on the included dataset. The repository contains:

- the preserved source workbook;
- harmonised CSV exports;
- processed modelling cohorts;
- data profiles and cohort summaries;
- repeated group-aware validation results;
- grouped out-of-fold predictions;
- trained model bundles;
- bootstrap models for uncertainty estimation;
- feature-importance tables;
- reproducible figures;
- a machine-readable run summary;
- an interactive dashboard;
- unit tests;
- a dataset card;
- a model card;
- FAIR metadata;
- software and data licence documentation;
- citation metadata.

---

# What the Project Does

The current implementation:

- reads the harmonised CSV exported from the original Excel workbook;
- normalises text while preserving scientific symbols;
- parses numeric values, including decimal commas;
- creates explicit numeric fields for yield, incubation time, experiment ID, publication year, and reference ID;
- profiles the complete database;
- counts substrates, organisms, enzymes, units, experiments, and references;
- identifies comparable enzyme-unit cohorts;
- creates one within-study modelling cohort;
- creates one cross-study modelling cohort;
- extracts selected process parameters from semi-structured text;
- derives interpretable categorical and binary features;
- compares a median baseline, Random Forest, and Extra Trees model;
- trains models on `log(1 + yield)`;
- converts predictions back to the original activity scale;
- prevents experiment-level and article-level leakage;
- evaluates models through repeated grouped train/test splits;
- selects the model with the lowest median grouped MAE;
- creates five-fold grouped out-of-fold predictions;
- computes MAE, median absolute error, RMSE, and R-squared;
- trains group-bootstrap models;
- reports 5th, 50th, and 95th percentile bootstrap predictions;
- exports tree-based feature importance;
- creates exploratory and model-evaluation plots;
- saves trained models with Joblib;
- exposes the results through a Streamlit dashboard.

---

# What the Project Does Not Yet Do

The project title refers to AI-assisted optimisation, but the present release should be understood as the **data-readiness, prediction, uncertainty, and scenario-screening foundation** for a future optimisation system.

The current code does **not** yet:

- implement a validated mathematical optimiser;
- claim that the predicted conditions are globally optimal;
- perform laboratory validation;
- model microbial kinetics mechanistically;
- calculate mass and energy balances;
- perform a complete ISO-compliant Life Cycle Assessment;
- estimate causal effects;
- replace food-process or bioprocess experts;
- provide industrial operating recommendations;
- guarantee safe combinations of substrate, organism, process conditions, or reactor settings;
- correct for all differences between analytical assays and laboratories;
- convert incompatible enzyme-activity units into a common unit;
- claim external validity beyond the analysed literature database.

A direct multi-objective optimiser should only be added after the predictive model has demonstrated acceptable transportability and the process variables required for optimisation are documented consistently.

---

# Why This Project Matters

Circular food production aims to reduce waste and retain the value of biological materials. Cereal processing, agriculture, and food manufacturing generate residues such as bran, straw, stover, cobs, husks, and mixed lignocellulosic side streams. These materials can potentially serve as substrates for microbial processes that produce enzymes and other value-added products.

However, building reusable AI models from such data is difficult because:

- the data may come from many organisations and laboratories;
- each partner may use different naming conventions;
- units may differ;
- metadata may be incomplete;
- experimental protocols may not be reported consistently;
- multiple enzyme outputs may originate from the same experiment;
- several rows may refer to one scientific article;
- categorical combinations may be rare;
- process settings may be embedded in free text;
- some variables may be missing systematically;
- a random row split may cause serious data leakage.

FAIR-SSF-Opt treats these data-quality and interoperability issues as part of the modelling problem rather than as an afterthought.

---

# Relationship to Circular Food and Bioprocess Research

The project connects directly to several research themes.

## Circular economy

Cereal residues and agro-industrial side streams are treated as potential feedstocks rather than waste.

## Food and bioprocess systems

The database describes fungal solid-state fermentation and enzyme production, including substrates, organisms, incubation time, pretreatment, supplements, and process parameters.

## Artificial intelligence

Machine-learning models are trained to estimate reported enzyme activity from heterogeneous process and biological features.

## FAIR data

The project records provenance, DOI, licence, variable definitions, units, derived fields, transformations, access conditions, and modelling assumptions.

## Process modelling

The prototype uses process-related variables such as incubation time, pH, temperature, moisture content, agitation, pretreatment, supplementation, and optimisation method.

## Sustainability

The valorisation of food and agricultural residues can contribute to resource efficiency, reduced waste, circular bioeconomy, and cleaner production.

## Consortium data infrastructure

The cross-study benchmark simulates an important consortium question: can a model trained on data from some providers transfer to a provider or publication that was not included in training?

---

# Research Questions and Hypotheses

## Main research question

Can FAIR-aligned machine-learning models predict enzyme production from cereal food residues and identify promising solid-state fermentation conditions for circular bioprocessing?

## Sub-question 1: Data readiness

Can the literature-derived workbook be transformed into a documented, machine-readable, reproducible dataset without losing the original scientific fields?

## Sub-question 2: Within-study modelability

Can a model learn a useful relationship between substrate, organism, enzyme, process descriptors, and reported activity when evaluated on experiments that were excluded from training?

## Sub-question 3: Cross-study transportability

Can a model trained on xylanase records from selected publications generalise to scientific articles that were completely excluded from training?

## Sub-question 4: Uncertainty

How sensitive are predictions to the groups used for model training?

## Hypothesis

A relatively standardised within-study dataset should be more learnable than a heterogeneous cross-study literature dataset. Weak cross-study performance would indicate that harmonised metadata, comparable units, common schemas, and explicit process variables are prerequisites for reusable consortium AI.

---

# Source Dataset

## Official dataset

**Title:** Production of enzymes via solid state fermentation from cereals  
**Version:** 2  
**Published:** 26 January 2021  
**DOI:** `10.17632/k2xv3yss8m.2`  
**Repository:** Mendeley Data  
**Dataset page:** https://data.mendeley.com/datasets/k2xv3yss8m/2  
**Contributors:** Joseph Bourgine, Dominika Teigiserova, Marianne Thomsen  
**Licence:** Creative Commons Attribution 4.0 International, CC BY 4.0

The dataset was produced as part of research associated with the review of enzyme production from cereal residues through fungal solid-state fermentation. The work was connected to the Horizon 2020 DECISIVE project on decentralised biowaste valorisation and was further supported by Aarhus University research environments.

The original database was designed to support filtering by variables such as substrate, enzyme, unit, yield, organism, incubation time, pretreatment, supplementation, optimisation method, and scientific reference.

---

# Dataset Citation and Licence

Please cite the source dataset as:

> Bourgine, Joseph; Teigiserova, Dominika; Thomsen, Marianne (2021),  
> “Production of enzymes via solid state fermentation from cereals”,  
> Mendeley Data, Version 2.  
> DOI: https://doi.org/10.17632/k2xv3yss8m.2

The source data are licensed under **CC BY 4.0**. Reuse therefore requires appropriate attribution.

The project code is licensed separately under the **MIT License**. The MIT licence applies to the software in this repository and does not replace or override the licence of the source dataset.

See:

- `LICENSE`
- `LICENSE_DATA.md`
- `CITATION.cff`

---

# Dataset Structure

The original workbook contains:

- an introduction sheet describing columns and abbreviations;
- the main enzyme-production database;
- a reference sheet containing full bibliographic information.

The processed repository preserves these components as:

```text
data/raw/source_workbook.xlsx
data/raw/introduction.csv
data/raw/ssf_enzyme_production.csv
data/raw/references.csv
```

The main table includes fields such as:

| Field | Meaning |
|---|---|
| `XP n°` | Experiment identifier |
| `Substrate` | Cereal residue or mixed substrate |
| `Organism` | Fungal organism, strain, or co-culture |
| `Enzyme` | Reported enzyme |
| `Yield` | Reported enzyme activity or production value |
| `Unit` | Unit associated with the reported value |
| `Incubation time (hrs)` | Incubation duration |
| `Pretreatment` | Substrate pretreatment description |
| `Nutritive or inducing supplement` | Supplementation information |
| `Enhancement or optimization method` | Reported optimisation method |
| `Parameters` | Semi-structured process parameters |
| `Notes` | Additional scientific notes |
| `Date of publication` | Publication year |
| `Reference` | Reference identifier linked to the bibliography sheet |

Derived fields created by the code include:

| Derived field | Purpose |
|---|---|
| `yield_value` | Numeric representation of `Yield` |
| `incubation_hours` | Numeric incubation time |
| `experiment_id` | Integer experiment identifier |
| `publication_year` | Integer publication year |
| `reference_id` | Integer reference identifier |

---

# Initial Data Audit

The uploaded workbook was examined before model development. The resulting profile is saved in:

```text
data/processed/data_profile.json
```

## Overall profile

| Property | Observed value |
|---|---:|
| Total records | 487 |
| Numeric yield records | 485 |
| Missing or nonnumeric yield records | 2 |
| Independent experiment IDs | 209 |
| Scientific references | 69 |
| Publication period | 2010–2019 |
| Unique substrate labels | 45 |
| Unique organism or co-culture labels | 111 |
| Unique enzyme labels | 34 |
| Unique activity units | 6 |
| Records with numeric incubation time | 458 |

## Most frequent substrates

| Substrate | Records |
|---|---:|
| Wheat bran | 103 |
| Mixture of wheat bran and sugarcane bagasse | 56 |
| Mixture of wheat bran and cottonseed meal | 41 |
| Rice straw | 36 |
| Corn stover | 32 |
| Mixture of oat and sugarcane bagasse | 32 |
| Wheat straw | 28 |
| Mixture of wheat bran and sphagnum peat | 28 |
| Corn cob | 24 |
| Mixture of rice straw and wheat bran | 12 |

## Most frequent enzymes

| Enzyme | Records |
|---|---:|
| Xylanase | 92 |
| CMCase | 83 |
| β-glucosidase | 74 |
| FPase | 61 |
| β-xylosidase | 34 |
| Laccase | 19 |
| Phytase | 18 |
| Protease | 15 |
| Mn-peroxidase | 13 |
| Lignin peroxidase | 12 |

## Activity-unit distribution

| Unit | Records |
|---|---:|
| U/gds | 278 |
| U/g | 88 |
| U/mL | 87 |
| U/g protein | 21 |
| nmol [Glu]/ml/min | 7 |
| U/cm² | 6 |

## Largest comparable enzyme-unit cohorts

| Enzyme | Unit | Records |
|---|---|---:|
| Xylanase | U/gds | 60 |
| CMCase | U/gds | 60 |
| β-glucosidase | U/gds | 51 |
| FPase | U/gds | 35 |
| β-xylosidase | U/gds | 30 |
| Xylanase | U/g | 26 |
| FPase | U/g | 19 |
| Phytase | U/g protein | 17 |

These statistics are generated by the pipeline and are not manually hard-coded into the modelling logic.

---

# Why All 487 Records Are Not Pooled into One Regression Problem

Pooling all rows into a single target would be scientifically misleading because:

1. **Different enzymes are being measured.**  
   Xylanase, CMCase, FPase, β-glucosidase, laccase, phytase, and other enzymes do not represent the same response.

2. **Different units are used.**  
   Values reported in `U/gds`, `U/g`, `U/mL`, `U/g protein`, `U/cm²`, and other units are not directly interchangeable.

3. **Assay methods may differ.**  
   Even identical labels may reflect different analytical protocols.

4. **Records are clustered.**  
   Several outputs may originate from the same experiment, and multiple experiments may originate from the same publication.

5. **The feature space is sparse.**  
   Many organism–substrate–enzyme combinations appear only a few times.

6. **Important variables may be unreported.**  
   Reactor scale, inoculum, moisture, temperature, pH, particle size, aeration, and analytical method are not consistently available.

The project therefore creates focused cohorts and uses group-aware validation.

---

# Experimental Design

Two complementary modelling experiments are implemented.

```text
Complete database
        |
        +--> Data profile and cohort summary
        |
        +--> Experiment 1:
        |    Reference 10
        |    Multiple enzyme outputs
        |    Grouped by experiment ID
        |
        +--> Experiment 2:
             Xylanase + U/gds
             Multiple scientific articles
             Grouped by reference ID
```

The first experiment asks whether a relatively structured study can support prediction. The second asks whether the model transports across publications.

---

# Experiment 1: Within-Study Multi-Enzyme Benchmark

## Cohort definition

The within-study cohort selects records satisfying:

```text
Reference ID = 10
Yield is numeric
Experiment ID is available
```

## Cohort size

| Property | Value |
|---|---:|
| Records | 119 |
| Independent experiments | 30 |
| Validation group | Experiment ID |
| Response | Reported enzyme activity |
| Units | Preserved as a feature |
| Enzymes | Multiple enzyme outputs |

## Why group by experiment ID?

Some experiments report several enzyme activities under the same substrate, organism, and process conditions. If rows were split randomly, one enzyme output from an experiment could enter training while another output from the same experiment entered testing. This would provide the model with almost identical experimental conditions and produce an optimistic estimate.

The group-aware design ensures:

```text
All rows from one experiment -> train
or
All rows from one experiment -> test
```

No experiment appears in both sets within a split.

---

# Experiment 2: Cross-Study Xylanase Benchmark

## Cohort definition

The cross-study cohort selects records satisfying:

```text
Enzyme = xylanase
Unit = U/gds
Yield is numeric
Reference ID is available
```

## Cohort size

| Property | Value |
|---|---:|
| Records | 60 |
| Independent references | 16 |
| Validation group | Scientific reference |
| Response | Xylanase activity in U/gds |

## Why group by scientific reference?

Rows from the same article often share:

- laboratory procedures;
- analytical methods;
- equipment;
- strains;
- reporting conventions;
- experimental design;
- unreported contextual variables.

A random row split can therefore allow article-specific information to leak into both training and testing.

The cross-study design ensures:

```text
All rows from one article -> train
or
All rows from one article -> test
```

This is a stronger test of transportability to unseen data sources.

---

# Complete End-to-End Pipeline

Running:

```bash
python scripts/run_pipeline.py
```

executes the following sequence.

## Step 1 — Load the harmonised raw CSV

The pipeline reads:

```text
data/raw/ssf_enzyme_production.csv
```

using Python's standard CSV module with UTF-8 support.

## Step 2 — Normalise text

The function `clean_text()`:

- converts `None` to an empty string;
- replaces non-breaking spaces;
- removes carriage returns and line breaks;
- collapses repeated whitespace;
- preserves scientific characters such as `β`, degree symbols, and superscripts where possible.

## Step 3 — Parse numeric fields

The functions `parse_float()` and `parse_int()`:

- treat empty values and known missing tokens as missing;
- support decimal commas by replacing commas with decimal points;
- return `None` for values that cannot be parsed safely;
- create numeric yield, incubation, experiment, year, and reference fields.

## Step 4 — Profile the complete dataset

The code calculates:

- row counts;
- usable yield counts;
- experiment counts;
- reference counts;
- year range;
- unique substrates;
- unique organisms;
- unique enzymes;
- unique units;
- unit distribution;
- most frequent variables;
- enzyme-unit cohort sizes.

## Step 5 — Export the data profile

The profile is saved to:

```text
data/processed/data_profile.json
```

## Step 6 — Build the cohort summary

Each enzyme-unit combination is summarised with:

- record count;
- experiment count;
- reference count;
- minimum yield;
- median yield;
- maximum yield.

The result is saved to:

```text
data/processed/cohort_summary.csv
```

## Step 7 — Generate exploratory figures

The pipeline generates:

- most frequent enzymes;
- most frequent substrates;
- records by publication year.

## Step 8 — Select the two modelling cohorts

The code creates:

```text
data/processed/within_study_reference_10.csv
data/processed/cross_study_xylanase_u_gds.csv
```

## Step 9 — Convert each record into a feature dictionary

Categorical, numeric, and binary features are derived through `build_feature_dict()`.

## Step 10 — Compare candidate models

Each model is tested on the same repeated group-aware splits.

## Step 11 — Select the best model

The model with the lowest median grouped MAE is selected.

## Step 12 — Create grouped out-of-fold predictions

Five-fold GroupKFold predictions are created so each row receives a prediction from a model that did not train on its group.

## Step 13 — Train the final model

The selected model is trained on the full cohort after evaluation.

## Step 14 — Train group-bootstrap models

Groups are sampled with replacement and multiple models are fitted for prediction-interval estimation.

## Step 15 — Calculate feature importance

Tree-based importance is extracted from the selected model.

## Step 16 — Save model bundles

The fitted final model, bootstrap models, category values, target transformation, and training ranges are stored with Joblib.

## Step 17 — Generate model figures

The pipeline produces:

- model-comparison charts;
- observed-versus-predicted plots;
- feature-importance charts.

## Step 18 — Save a machine-readable run summary

The final profile and model results are saved to:

```text
artifacts/run_summary.json
```

## Step 19 — Print the summary

The same JSON summary is printed to the terminal for immediate inspection.

---

# Data Cleaning and Normalisation

## Missing values

The following tokens are treated as missing:

```text
""
"na"
"n/a"
"none available"
"not available"
```

The parser is conservative. Values that cannot be parsed safely remain missing instead of being guessed.

## Decimal commas

Scientific data may use commas as decimal separators. For example:

```text
5,5
```

is parsed as:

```text
5.5
```

## Text preservation

The project avoids aggressive lowercasing of the raw scientific fields. Original labels are retained in processed cohort exports. Case-insensitive comparison is used only where needed for cohort selection and feature rules.

## Source preservation

The original workbook is kept unchanged as:

```text
data/raw/source_workbook.xlsx
```

Derived CSV and processed files are stored separately, so the raw source remains traceable.

---

# Feature Engineering

The prototype uses a transparent feature-engineering approach rather than a black-box text model.

## Raw categorical features

- substrate;
- organism;
- enzyme;
- unit;
- pretreatment;
- supplement;
- optimisation method.

## Derived categorical features

### Substrate family

The substrate label is searched for cereal families:

- wheat;
- rice;
- corn;
- oat;
- sorghum;
- millet;
- barley;
- rye.

Mixed cereal families are combined, for example:

```text
wheat+rice
```

Unrecognised labels are mapped to:

```text
other
```

### Organism genus

For a single organism, the first token is used as a genus-level label.

Example:

```text
Aspergillus niger -> Aspergillus
```

Co-culture labels are assigned:

```text
Co-culture
```

### Optimisation category

Semi-structured optimisation descriptions are grouped into:

- `RSM`
- `OFAT`
- `Taguchi`
- `MixtureDesign`
- `Other`
- `none`
- `na`
- `missing`

Rules recognise terms such as response surface methodology, Box–Behnken, central composite design, Plackett–Burman, one-factor-at-a-time, Taguchi, simplex, and mixture design.

## Numeric features

- incubation time in hours;
- pH;
- temperature in degrees Celsius;
- moisture content percentage;
- agitation speed in rpm;
- publication year.

## Conservative process-parameter parsing

The `Parameters` field is semi-structured. Regular expressions search for explicit patterns such as:

```text
pH=5.0
T°=30°C
MC=70%
Agitation=150rpm
```

The parser intentionally does not infer ambiguous numbers.

## Binary features

### Substrate and organism

- substrate is a mixture;
- organism is a co-culture.

### Pretreatment

- missing or none;
- autoclaved or sterilised;
- dried;
- ground or milled;
- chemical treatment.

### Supplementation

- missing or none;
- yeast extract;
- nitrogen-source terms such as ammonium, nitrate, peptone, or urea.

## Missing numeric sentinels

When a selected numeric process variable is unavailable, the feature value is represented by `-1.0`. This enables the tree models to distinguish missing values from realistic positive process settings. The limitation of this approach is documented, and future versions should consider explicit missingness indicators for each numeric variable.

---

# Target Transformation

The raw enzyme-activity distributions are strongly skewed and include very large values.

The models are trained on:

```math
z = \log(1 + y)
```

where:

- `y` is the reported enzyme activity;
- `z` is the transformed target.

Predictions are converted back through:

```math
\hat{y} = \exp(\hat{z}) - 1
```

Negative back-transformed predictions are clipped to zero.

This transformation:

- reduces the influence of extreme values;
- supports non-negative predictions;
- allows tree models to focus on relative differences;
- does not make incompatible enzyme units comparable.

All reported evaluation metrics are calculated on the original activity scale after inverse transformation.

---

# Candidate Models

Three models are compared.

## 1. Dummy median regressor

```text
DummyRegressor(strategy="median")
```

Purpose:

- provides a non-informative baseline;
- predicts the median transformed target;
- establishes whether the machine-learning models improve on a simple reference.

## 2. Random Forest regressor

```text
RandomForestRegressor(
    n_estimators=100,
    min_samples_leaf=1,
    max_features=0.8,
    random_state=seed,
    n_jobs=1
)
```

Purpose:

- captures nonlinear relationships;
- handles interactions;
- works with mixed tabular features after vectorisation;
- provides tree-based feature importance.

## 3. Extra Trees regressor

```text
ExtraTreesRegressor(
    n_estimators=100,
    min_samples_leaf=1,
    max_features=1.0,
    random_state=seed,
    n_jobs=1
)
```

Purpose:

- offers a more randomised ensemble comparison;
- can reduce variance in some tabular problems;
- provides a second nonlinear tree baseline.

## Feature vectorisation

`DictVectorizer(sparse=False)` converts feature dictionaries into a numeric matrix.

Categorical variables become one-hot-style indicator columns. Numeric variables remain numeric.

The full modelling object is an scikit-learn `Pipeline`:

```text
DictVectorizer -> Regressor
```

This keeps feature transformation and model fitting together.

---

# Group-Aware Validation

## Repeated grouped train/test splits

Model comparison uses:

```text
GroupShuffleSplit
```

with:

```text
test_size = 0.25
random_state = 42
```

The default pipeline uses 10 repeated splits. A more stable portfolio run can use 25 splits.

## Group definition

| Experiment | Group field |
|---|---|
| Within-study | `experiment_id` |
| Cross-study | `reference_id` |

## Why this matters

Random row splitting would violate the independence assumptions of evaluation because records from the same experiment or publication can be strongly related.

Group-aware validation asks a harder and more realistic question:

> Can the model predict a group that it did not observe during training?

---

# Model Selection

For every model and every repeated split, the pipeline calculates:

- MAE;
- median absolute error;
- RMSE;
- R-squared;
- test-set row count.

For each model, the pipeline then calculates:

- median metric;
- mean metric;
- 25th percentile;
- 75th percentile.

The selected model is the model with the lowest:

```text
median group-aware MAE
```

This is implemented directly in the code:

```python
best = min(summaries, key=lambda row: row["median_mae"])
```

The same candidate models and split indices are used for fair comparison.

---

# Out-of-Fold Evaluation

After model selection, the chosen model is evaluated through:

```text
GroupKFold(n_splits=5)
```

The number of folds is reduced automatically if fewer than five independent groups are available.

Each row receives an out-of-fold prediction generated by a model that did not train on that row's group.

The exported file includes:

- row index;
- experiment ID;
- reference ID;
- enzyme;
- unit;
- observed yield;
- predicted yield;
- absolute error.

Files:

```text
data/processed/within_study_reference_10_oof_predictions.csv
data/processed/cross_study_xylanase_u_gds_oof_predictions.csv
```

---

# Uncertainty Estimation

The project uses a group-bootstrap ensemble.

## Procedure

1. Identify all unique validation groups.
2. Sample the groups with replacement.
3. Include every row belonging to each sampled group.
4. Fit one model on the resampled grouped dataset.
5. Repeat the procedure multiple times.
6. Predict the requested scenario with every bootstrap model.
7. calculate prediction percentiles.

## Reported values

The dashboard reports:

- final-model point prediction;
- 5th percentile of bootstrap predictions;
- 50th percentile of bootstrap predictions;
- 95th percentile of bootstrap predictions.

## Important interpretation

The 5th–95th percentile interval is **not** a complete scientific confidence interval. It reflects sensitivity to group resampling under the current model and dataset.

It does not include all uncertainty arising from:

- experimental measurement;
- analytical assays;
- omitted variables;
- laboratory differences;
- unknown scale effects;
- model misspecification;
- extrapolation beyond training support.

---

# Evaluation Metrics

## Mean Absolute Error

```math
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
```

MAE measures the average absolute prediction error in the original activity unit.

## Median Absolute Error

```math
MedAE = \operatorname{median}(|y_i-\hat{y}_i|)
```

Median absolute error is more resistant to extreme errors than MAE.

## Root Mean Squared Error

```math
RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
```

RMSE penalises large errors more strongly.

## Coefficient of Determination

```math
R^2 = 1 - \frac{\sum_i(y_i-\hat{y}_i)^2}{\sum_i(y_i-\bar{y})^2}
```

Interpretation:

- `R² = 1`: perfect prediction;
- `R² = 0`: comparable to predicting the mean;
- `R² < 0`: worse than a mean-based reference for that evaluation set.

Because the target distributions are skewed and groups differ substantially, all metrics should be interpreted together.

---

# Tested Results

The values below were produced by the included pipeline with:

```text
10 repeated grouped splits
5-fold grouped out-of-fold evaluation
15 group-bootstrap models
random seed 42
```

Small numerical differences may appear with different package versions or different command-line settings.

## Experiment 1 — Within-study Reference 10

### Cohort

| Property | Value |
|---|---:|
| Rows | 119 |
| Independent experiment groups | 30 |
| Selected model | Random Forest |

### Repeated group-aware validation

| Metric | Result |
|---|---:|
| Median MAE | 41.93 |
| Mean MAE | 44.57 |
| Median median absolute error | 8.91 |
| Median RMSE | 94.74 |
| Median R² | 0.316 |
| Mean R² | 0.208 |

### Five-fold grouped out-of-fold evaluation

| Metric | Result |
|---|---:|
| MAE | 42.14 |
| Median absolute error | 10.06 |
| RMSE | 98.83 |
| R² | 0.289 |

### Model comparison by median grouped MAE

| Model | Median MAE |
|---|---:|
| Random Forest | 41.93 |
| Dummy median | 56.16 |
| Extra Trees | 58.47 |

The Random Forest improved on the dummy baseline for this cohort and showed some predictive signal under experiment-level validation.

## Experiment 2 — Cross-study Xylanase in U/gds

### Cohort

| Property | Value |
|---|---:|
| Rows | 60 |
| Independent publication groups | 16 |
| Selected model | Random Forest |

### Repeated group-aware validation

| Metric | Result |
|---|---:|
| Median MAE | 1478.03 U/gds |
| Mean MAE | 1869.85 U/gds |
| Median median absolute error | 1172.16 U/gds |
| Median RMSE | 1903.63 U/gds |
| Median R² | -0.450 |
| Mean R² | -1.422 |

### Five-fold grouped out-of-fold evaluation

| Metric | Result |
|---|---:|
| MAE | 1186.93 U/gds |
| Median absolute error | 626.74 U/gds |
| RMSE | 1910.67 U/gds |
| R² | -0.281 |

### Model comparison by median grouped MAE

| Model | Median MAE |
|---|---:|
| Random Forest | 1478.03 U/gds |
| Dummy median | 1597.93 U/gds |
| Extra Trees | 2037.40 U/gds |

The Random Forest was the least inaccurate candidate according to median grouped MAE, but its cross-study generalisation remained weak.

---

# Interpretation of Results

## Within-study result

The within-study model performs better than the simple median baseline and obtains positive grouped out-of-fold R². This suggests that the structured study contains learnable relationships among:

- enzyme identity;
- organism;
- substrate;
- incubation time;
- pretreatment;
- optimisation category;
- available process variables.

However, the result is not strong enough for industrial decision-making. It demonstrates prototype feasibility rather than process validation.

## Cross-study result

The xylanase model has negative grouped R² on unseen scientific articles. This means that the model does not transfer reliably across publications.

Possible reasons include:

- different analytical assays;
- laboratory-specific procedures;
- unreported strain and cultivation details;
- inconsistent moisture definitions;
- different inoculum conditions;
- hidden scale differences;
- article-specific substrate preparation;
- sparse organism–substrate combinations;
- severe target skew;
- incomplete process variables;
- source imbalance;
- limited sample size.

## Main research conclusion

The result supports the following principle:

> FAIR data infrastructure is not separate from AI performance. Comparable units, explicit metadata, provenance, controlled vocabularies, quality flags, and common process variables are necessary for reusable consortium models.

A negative cross-study result is therefore informative. It reveals where data infrastructure must improve before optimisation claims can be justified.

---

# Feature Importance

Feature importance is exported for the selected tree model.

## Within-study examples

The highest-ranked features in the tested run included:

- enzyme identity, especially β-xylosidase and xylanase;
- selected substrate labels;
- organism and genus;
- incubation time;
- grinding or milling pretreatment;
- optimisation category;
- moisture content.

## Cross-study examples

The highest-ranked features included:

- autoclaving or sterilisation indicator;
- incubation time;
- corn substrate family;
- temperature;
- optimisation category;
- publication year;
- mixture indicator;
- selected organism and genus labels;
- moisture content;
- pH.

## Warning

Tree-based importance:

- is not a causal effect;
- may favour high-cardinality features;
- may reflect source-specific patterns;
- may be unstable in small datasets;
- should be interpreted alongside grouped validation.

Files:

```text
data/processed/within_study_reference_10_feature_importance.csv
data/processed/cross_study_xylanase_u_gds_feature_importance.csv
```

Figures:

```text
reports/figures/within_study_reference_10_feature_importance.png
reports/figures/cross_study_xylanase_u_gds_feature_importance.png
```

---

# Interactive Streamlit Dashboard

The dashboard is implemented in:

```text
app.py
```

## Available modes

1. **Within-study benchmark — Reference 10**
2. **Cross-study xylanase benchmark — U/gds**

## Dashboard summary cards

The dashboard displays:

- cohort rows;
- independent groups;
- selected model;
- grouped out-of-fold MAE.

## User inputs

The scenario interface allows selection or entry of:

- substrate;
- organism;
- enzyme;
- unit;
- incubation time;
- initial pH;
- temperature;
- moisture content;
- agitation speed;
- pretreatment description;
- supplement description;
- optimisation method.

## Prediction outputs

The dashboard displays:

- point prediction;
- bootstrap 5th percentile;
- bootstrap 95th percentile;
- a gauge representation of the predicted activity.

## Cohort browser

The user can inspect the training cohort, including:

- experiment;
- substrate;
- organism;
- enzyme;
- yield;
- unit;
- incubation time;
- year;
- reference.

## Dashboard safety warning

The interface states that:

- the data are literature-derived;
- predictions are not validated industrial recommendations;
- the bootstrap interval is not complete scientific uncertainty;
- weak cross-study performance is an important data-readiness finding.

---

# FAIR Data Implementation

FAIR-SSF-Opt applies the FAIR principles at a practical prototype level.

## Findable

- dataset DOI is documented;
- source citation is provided;
- stable filenames are used;
- dataset and model cards are included;
- a variable-level data dictionary is provided;
- outputs use descriptive cohort names;
- machine-readable JSON summaries are generated;
- citation metadata are stored in `CITATION.cff`.

## Accessible

- the original public dataset source is linked;
- the dataset licence is documented;
- source and processed data are separated;
- access conditions are explicit;
- the pipeline can be run locally without a proprietary platform.

## Interoperable

- CSV is used for tabular data;
- JSON is used for profiles and run summaries;
- YAML is used for provenance;
- UTF-8 encoding is used;
- units are preserved explicitly;
- reference and experiment identifiers are maintained;
- derived variables are documented;
- raw labels are retained.

## Reusable

- transformation code is versionable;
- source provenance is recorded;
- assumptions and limitations are documented;
- validation groups are explicit;
- model cards and dataset cards are included;
- software and data licences are separated;
- tests are included;
- commands are documented;
- output files are reproducible.

## FAIR files

```text
metadata/data_dictionary.csv
metadata/dataset_description.json
metadata/provenance.yaml
DATASET_CARD.md
MODEL_CARD.md
CITATION.cff
LICENSE_DATA.md
```

---

# Repository Structure

```text
fair-ssf-opt/
├── README.md
├── README_FA.md
├── PROJECT_PLAN.md
├── GITHUB_SETUP.md
├── DATASET_CARD.md
├── MODEL_CARD.md
├── INTERVIEW_NOTES.md
├── LICENSE
├── LICENSE_DATA.md
├── CITATION.cff
├── requirements.txt
├── pyproject.toml
├── app.py
│
├── scripts/
│   └── run_pipeline.py
│
├── src/
│   └── fair_ssf_opt/
│       ├── __init__.py
│       ├── data.py
│       ├── features.py
│       ├── modeling.py
│       └── reporting.py
│
├── data/
│   ├── raw/
│   │   ├── source_workbook.xlsx
│   │   ├── ssf_enzyme_production.csv
│   │   ├── introduction.csv
│   │   └── references.csv
│   └── processed/
│       ├── data_profile.json
│       ├── cohort_summary.csv
│       ├── within_study_reference_10.csv
│       ├── within_study_reference_10_validation.csv
│       ├── within_study_reference_10_oof_predictions.csv
│       ├── within_study_reference_10_feature_importance.csv
│       ├── cross_study_xylanase_u_gds.csv
│       ├── cross_study_xylanase_u_gds_validation.csv
│       ├── cross_study_xylanase_u_gds_oof_predictions.csv
│       └── cross_study_xylanase_u_gds_feature_importance.csv
│
├── metadata/
│   ├── data_dictionary.csv
│   ├── dataset_description.json
│   └── provenance.yaml
│
├── artifacts/
│   ├── run_summary.json
│   ├── within_study_reference_10_model_bundle.joblib
│   └── cross_study_xylanase_u_gds_model_bundle.joblib
│
├── reports/
│   └── figures/
│       ├── top_enzymes.png
│       ├── top_substrates.png
│       ├── publication_years.png
│       ├── within_study_reference_10_model_comparison.png
│       ├── within_study_reference_10_predicted_vs_actual.png
│       ├── within_study_reference_10_feature_importance.png
│       ├── cross_study_xylanase_u_gds_model_comparison.png
│       ├── cross_study_xylanase_u_gds_predicted_vs_actual.png
│       └── cross_study_xylanase_u_gds_feature_importance.png
│
└── tests/
    └── test_features.py
```

---

# File-by-File Explanation

## `README.md`

Complete English documentation for the project.

## `README_FA.md`

Persian-language project overview.

## `PROJECT_PLAN.md`

Research objectives, implementation stages, and planned extensions.

## `GITHUB_SETUP.md`

Instructions for creating and publishing the GitHub repository.

## `DATASET_CARD.md`

Documents:

- source;
- DOI;
- licence;
- contents;
- intended use;
- known limitations;
- processing decisions.

## `MODEL_CARD.md`

Documents:

- model purpose;
- candidate models;
- validation design;
- metrics;
- uncertainty method;
- limitations;
- responsible use.

## `INTERVIEW_NOTES.md`

Contains a concise explanation of the project for a doctoral interview.

## `LICENSE`

MIT licence for the software.

## `LICENSE_DATA.md`

Explains the CC BY 4.0 source-data licence and attribution requirements.

## `CITATION.cff`

Machine-readable citation metadata for GitHub.

## `requirements.txt`

Python dependencies required to run the project.

## `pyproject.toml`

Package metadata, dependencies, package-discovery configuration, and pytest settings.

## `app.py`

Streamlit dashboard.

## `scripts/run_pipeline.py`

Main orchestration script. It runs profiling, cohort construction, model evaluation, out-of-fold prediction, bootstrapping, importance export, figure generation, model saving, and summary creation.

## `src/fair_ssf_opt/data.py`

Responsible for:

- text cleaning;
- numeric parsing;
- CSV loading;
- record writing;
- data profiling;
- cohort summaries;
- within-study selection;
- cross-study selection;
- JSON writing.

## `src/fair_ssf_opt/features.py`

Responsible for:

- process-parameter parsing;
- optimisation-method classification;
- substrate-family extraction;
- organism-genus extraction;
- pretreatment flags;
- supplement flags;
- model feature dictionaries;
- dashboard scenario-record construction.

## `src/fair_ssf_opt/modeling.py`

Responsible for:

- candidate model definitions;
- scikit-learn pipelines;
- grouped validation;
- model summaries;
- model selection;
- grouped out-of-fold predictions;
- group bootstrap training;
- prediction intervals;
- feature importance;
- Joblib model saving;
- CSV result writing.

## `src/fair_ssf_opt/reporting.py`

Responsible for:

- top-category plots;
- publication-year plots;
- model-comparison plots;
- observed-versus-predicted plots;
- feature-importance plots.

## `data/raw/`

Contains the preserved workbook and raw CSV exports.

## `data/processed/`

Contains derived cohorts and result tables. These files can be regenerated.

## `metadata/`

Contains FAIR-oriented structured metadata.

## `artifacts/`

Contains model bundles and the machine-readable run summary.

## `reports/figures/`

Contains reproducible visual outputs.

## `tests/test_features.py`

Tests selected feature-processing rules.

---

# Installation

Python 3.10 or newer is recommended.

## Option 1 — Clone from GitHub

```bash
git clone https://github.com/tembooo/fair-ssf-opt.git
cd fair-ssf-opt
```

## Option 2 — Use the downloaded ZIP

1. Download the project ZIP.
2. Extract it.
3. Rename the folder to:

```text
fair-ssf-opt
```

4. Open a terminal inside the folder.

---

## Create a virtual environment

### Windows Command Prompt

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If script execution is blocked, run PowerShell as the current user and use:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Upgrade pip

```bash
python -m pip install --upgrade pip
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Optional editable installation

```bash
pip install -e .
```

Editable installation allows the package under `src/` to be imported while you modify the source code.

---

# Quick Start

Run the tests:

```bash
pytest
```

Run a fast pipeline check:

```bash
python scripts/run_pipeline.py --splits 5 --bootstrap 5
```

Launch the dashboard:

```bash
streamlit run app.py
```

---

# Full Reproducible Run

The default run uses 10 repeated grouped splits and 15 bootstrap models:

```bash
python scripts/run_pipeline.py
```

A more stable portfolio run can use:

```bash
python scripts/run_pipeline.py --splits 25 --bootstrap 40
```

A lighter run for a slow computer can use:

```bash
python scripts/run_pipeline.py --splits 3 --bootstrap 3
```

The script prints the complete JSON summary to the terminal and writes the results to disk.

---

# Command-Line Options

View help:

```bash
python scripts/run_pipeline.py --help
```

## `--data`

Path to the harmonised input CSV.

Default:

```text
data/raw/ssf_enzyme_production.csv
```

Example:

```bash
python scripts/run_pipeline.py --data data/raw/ssf_enzyme_production.csv
```

## `--splits`

Number of repeated GroupShuffleSplit evaluations.

Default:

```text
10
```

Example:

```bash
python scripts/run_pipeline.py --splits 25
```

## `--bootstrap`

Number of group-bootstrap models.

Default:

```text
15
```

Example:

```bash
python scripts/run_pipeline.py --bootstrap 40
```

Combined example:

```bash
python scripts/run_pipeline.py --splits 25 --bootstrap 40
```

---

# Running the Dashboard

The model artifacts must exist before the dashboard is launched.

First run:

```bash
python scripts/run_pipeline.py
```

Then run:

```bash
streamlit run app.py
```

Streamlit normally opens:

```text
http://localhost:8501
```

To stop the server, press:

```text
Ctrl + C
```

---

# Running the Tests

Run:

```bash
pytest
```

The current tests verify:

- decimal-comma process parsing;
- optimisation-method classification;
- substrate-family extraction.

A successful result should look similar to:

```text
3 passed
```

Future tests should cover:

- missing-value parsing;
- cohort selection;
- group separation;
- target transformation;
- prediction non-negativity;
- artifact schema;
- dashboard record construction.

---

# Generated Outputs

## Data profile

```text
data/processed/data_profile.json
```

Contains complete-dataset statistics.

## Cohort summary

```text
data/processed/cohort_summary.csv
```

Contains enzyme-unit cohort sizes and yield ranges.

## Modelling cohorts

```text
data/processed/within_study_reference_10.csv
data/processed/cross_study_xylanase_u_gds.csv
```

## Validation results

```text
data/processed/within_study_reference_10_validation.csv
data/processed/cross_study_xylanase_u_gds_validation.csv
```

Each file contains split-level metrics and model-level summaries.

## Out-of-fold predictions

```text
data/processed/within_study_reference_10_oof_predictions.csv
data/processed/cross_study_xylanase_u_gds_oof_predictions.csv
```

## Feature importance

```text
data/processed/within_study_reference_10_feature_importance.csv
data/processed/cross_study_xylanase_u_gds_feature_importance.csv
```

## Trained model bundles

```text
artifacts/within_study_reference_10_model_bundle.joblib
artifacts/cross_study_xylanase_u_gds_model_bundle.joblib
```

Each bundle contains:

- selected model name;
- grouping field;
- final fitted model;
- bootstrap models;
- target transformation;
- training-row count;
- unique-group count;
- allowed categorical values;
- minimum, median, and maximum training yield.

## Run summary

```text
artifacts/run_summary.json
```

## Figures

```text
reports/figures/top_enzymes.png
reports/figures/top_substrates.png
reports/figures/publication_years.png
reports/figures/within_study_reference_10_model_comparison.png
reports/figures/within_study_reference_10_predicted_vs_actual.png
reports/figures/within_study_reference_10_feature_importance.png
reports/figures/cross_study_xylanase_u_gds_model_comparison.png
reports/figures/cross_study_xylanase_u_gds_predicted_vs_actual.png
reports/figures/cross_study_xylanase_u_gds_feature_importance.png
```

---

# Reproducibility

## Random seeds

The main seed is:

```text
42
```

Model-specific seeds are derived from the split, fold, or bootstrap index.

## Deterministic configuration

The tree models use:

```text
n_jobs=1
```

This reduces platform-dependent parallel variation.

## Regeneration

Processed datasets, figures, validation tables, and artifacts can be regenerated by rerunning the pipeline.

## Environment differences

Small differences may occur because of:

- Python version;
- NumPy version;
- scikit-learn version;
- operating system;
- floating-point implementation.

For exact archival reproducibility, create a frozen environment after successful execution:

```bash
pip freeze > requirements-lock.txt
```

---

# Responsible AI and Scientific Use

This repository is intended for:

- research prototyping;
- method demonstration;
- data-readiness analysis;
- FAIR workflow development;
- educational use;
- portfolio presentation;
- hypothesis generation.

It is not intended for:

- unsupervised industrial process control;
- safety-critical decisions;
- regulatory decisions;
- commercial yield guarantees;
- biological safety decisions;
- replacing experimental validation;
- selecting organisms or conditions without expert review.

Any operational use would require:

- domain-expert review;
- laboratory validation;
- independent external validation;
- assay harmonisation;
- process-safety assessment;
- uncertainty calibration;
- clear responsibility and governance.

---

# Limitations

## Dataset limitations

- literature-derived rather than prospectively collected;
- heterogeneous analytical methods;
- incomplete metadata;
- inconsistent process descriptions;
- multiple units;
- uneven source representation;
- sparse categorical combinations;
- possible publication bias;
- values extracted from studies with different objectives;
- limited control over data quality.

## Modelling limitations

- small cohorts;
- high-cardinality categorical features;
- no causal interpretation;
- no mechanistic mass-balance constraints;
- no kinetic equations;
- no external experimental validation;
- no hyperparameter optimisation;
- limited candidate-model set;
- feature importance may be unstable;
- missing numeric values use sentinel values;
- bootstrap intervals are incomplete uncertainty estimates.

## Dashboard limitations

- users can create combinations not present in the data;
- the interface does not currently block extrapolation;
- predictions may be unreliable for rare categories;
- numerical outputs are not operating recommendations;
- the gauge range is based on training yield and current interval;
- scenario input does not represent a full fermentation recipe.

## Optimisation limitation

The current version does not implement a validated optimiser. The dashboard supports scenario exploration, which can help identify candidate conditions for further study, but it must not be described as confirmed optimisation.

---

# Troubleshooting

## `python` is not recognised

Try:

```bash
py --version
```

Then replace `python` with `py`:

```bash
py -m venv .venv
py scripts/run_pipeline.py
```

## Virtual environment does not activate in PowerShell

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Module import error

Install the project in editable mode:

```bash
pip install -e .
```

Or verify that you are running commands from the repository root.

## Missing package

Run:

```bash
pip install -r requirements.txt
```

## Dashboard says model artifacts are missing

Run:

```bash
python scripts/run_pipeline.py
```

before:

```bash
streamlit run app.py
```

## Input file not found

Verify that this file exists:

```text
data/raw/ssf_enzyme_production.csv
```

Or specify the path:

```bash
python scripts/run_pipeline.py --data path/to/file.csv
```

## Joblib model cannot be loaded

Delete and regenerate the artifacts using the same software environment:

```bash
python scripts/run_pipeline.py
```

Serialized scikit-learn models may not remain compatible across substantially different package versions.

## Log-scale plotting error

Observed and predicted values must be positive for logarithmic axes. The code clips negative predictions to zero, but exact zeros can still require attention in future datasets.

## Streamlit port is busy

Use another port:

```bash
streamlit run app.py --server.port 8502
```

## Pipeline is slow

Reduce the number of splits and bootstrap models:

```bash
python scripts/run_pipeline.py --splits 3 --bootstrap 3
```

---

# Future Development and Optimisation Roadmap

## Phase 1 — Data infrastructure

- controlled vocabularies for substrates;
- controlled vocabularies for organisms and strains;
- enzyme ontology mapping;
- standard unit definitions;
- explicit analytical-assay metadata;
- partner and laboratory identifiers;
- data-quality flags;
- measurement uncertainty;
- missingness reasons;
- machine-actionable metadata.

## Phase 2 — Improved feature engineering

- particle size;
- inoculum concentration;
- substrate ratio;
- moisture basis;
- initial and final pH;
- reactor or vessel scale;
- oxygen-transfer descriptors;
- aeration;
- humidity;
- sterilisation conditions;
- enzyme-assay method;
- strain taxonomy;
- substrate chemical composition.

## Phase 3 — Stronger models

- regularised linear models;
- CatBoost;
- histogram gradient boosting;
- quantile regression;
- conformal prediction;
- Bayesian hierarchical models;
- mixed-effects models;
- domain adaptation;
- partner-aware calibration.

## Phase 4 — Hybrid modelling

Combine machine learning with:

- microbial-growth kinetics;
- substrate-consumption models;
- product-formation equations;
- moisture and heat-transfer relations;
- mass balances;
- known process constraints.

## Phase 5 — External validation

- hold out a partner;
- hold out a laboratory;
- hold out a time period;
- test on new experiments;
- compare predicted and measured activity;
- recalibrate uncertainty.

## Phase 6 — Multi-objective optimisation

After predictive validity is established, optimise:

- enzyme yield;
- productivity;
- incubation time;
- energy demand;
- water demand;
- residue utilisation;
- environmental impact;
- economic cost;
- robustness under uncertainty.

Potential methods:

- constrained random search;
- Bayesian optimisation;
- NSGA-II;
- Pareto-front analysis;
- robust multi-objective optimisation.

## Phase 7 — Sustainability integration

Link process predictions to:

- energy inventories;
- water inventories;
- material inputs;
- waste outputs;
- greenhouse-gas indicators;
- LCA datasets;
- circularity indicators;
- techno-economic analysis.

## Phase 8 — Consortium decision-support platform

- role-based data access;
- partner-level metadata validation;
- model registry;
- dataset versioning;
- provenance tracking;
- dashboard deployment;
- API access;
- audit logs;
- uncertainty communication;
- human-in-the-loop approval.

---

# Suggested GitHub Repository Settings

## Repository name

```text
fair-ssf-opt
```

## Description

```text
FAIR-aligned, uncertainty-aware AI benchmarking for enzyme production from cereal residues via solid-state fermentation.
```

## Visibility

```text
Public
```

Only public, non-confidential data and code should be included.

## README

When creating the repository from this existing project:

```text
Add README: Off
```

## `.gitignore`

```text
Add .gitignore: None
```

The project already includes one.

## Licence

```text
Add licence: None
```

The project already contains the MIT licence and separate data-licence documentation.

## Suggested GitHub topics

```text
artificial-intelligence
machine-learning
fair-data
solid-state-fermentation
bioprocess-modelling
circular-economy
food-waste
agricultural-waste
enzyme-production
uncertainty-quantification
grouped-cross-validation
random-forest
streamlit
python
research-data-management
circular-food-systems
```

## Initial Git commands

```bash
git init
git add .
git commit -m "Initialize FAIR-SSF-Opt research prototype"
git branch -M main
git remote add origin https://github.com/tembooo/fair-ssf-opt.git
git push -u origin main
```

---

# Suggested Interview Answer

> My first proposed AI model for CIRC4FOOD would be a FAIR-aligned, uncertainty-aware surrogate model for a focused circular food-bioprocess use case.
>
> As a proof of concept, I developed a pipeline using a real literature-derived dataset on enzyme production from cereal and agro-industrial residues through fungal solid-state fermentation. The workflow preserves provenance and units, structures the data, extracts process variables, compares interpretable ensemble models, and evaluates them using group-aware validation.
>
> I designed two benchmarks. In the within-study benchmark, all outputs from the same experiment remain in one fold. In the cross-study xylanase benchmark, complete scientific articles are excluded from training folds. This prevents optimistic leakage and tests whether the model transfers to unseen data providers.
>
> The within-study model shows some predictive signal, while the cross-study model generalises poorly. I consider that an important result rather than something to hide. It demonstrates that reusable consortium AI requires comparable units, controlled vocabularies, explicit metadata, provenance, common process variables, and quality indicators.
>
> With better partner data, the same architecture could be extended to hybrid process modelling, calibrated uncertainty, and multi-objective optimisation of yield, energy use, water use, waste, cost, and environmental impact.

---

# How to Cite This Project

## Source dataset

```text
Bourgine, J.; Teigiserova, D.; Thomsen, M. (2021).
Production of enzymes via solid state fermentation from cereals.
Mendeley Data, Version 2.
https://doi.org/10.17632/k2xv3yss8m.2
```

## Software project

A suggested citation is available in:

```text
CITATION.cff
```

Example:

```text
Golbidi, Arman. FAIR-SSF-Opt: FAIR-Aligned AI Benchmarking for
Circular Enzyme Production from Cereal Residues.
Research prototype, 2026.
```

---

# Author

**Arman Golbidi**

MSc in Data-Centric Engineering  
Major: Computer Vision and Pattern Recognition  
LUT University, Finland

Research interests:

- artificial intelligence;
- machine learning;
- uncertainty-aware modelling;
- FAIR research data;
- sustainable food systems;
- circular production;
- process modelling;
- surrogate modelling;
- optimisation;
- data-driven decision support.

---

# Acknowledgements

The project uses the public dataset:

> Production of enzymes via solid state fermentation from cereals

created by Joseph Bourgine, Dominika Teigiserova, and Marianne Thomsen.

The source research was associated with work on cereal-residue enzyme production and circular bioeconomy, including the Horizon 2020 DECISIVE context described by the dataset authors.

This repository is an independent research and portfolio prototype. It is not an official project of Mendeley Data, Aarhus University, the DECISIVE consortium, LUT University, CIRC4FOOD, FAO, Ecochain, or any industrial organisation.

---

# Final Scientific Statement

FAIR-SSF-Opt demonstrates a central principle for data-driven circular food research:

> A machine-learning model is only as reusable as the data infrastructure, metadata, units, provenance, validation design, and uncertainty reporting that support it.

The prototype therefore treats data harmonisation, FAIR documentation, leakage prevention, and uncertainty estimation as core parts of the AI system. Its current results support further development toward partner-level data integration, hybrid process models, and carefully validated multi-objective optimisation.
