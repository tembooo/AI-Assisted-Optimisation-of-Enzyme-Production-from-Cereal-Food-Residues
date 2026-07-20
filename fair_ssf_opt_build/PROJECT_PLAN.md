# Project Plan

## Phase 1 — Repository and provenance

- Create a public GitHub repository named `fair-ssf-opt`.
- Add the MIT software licence.
- Preserve the data licence and DOI separately.
- Keep raw, processed, metadata, model, and report folders distinct.

## Phase 2 — Data audit

- Verify row counts and workbook sheets.
- Profile categorical diversity, units, missing values, and publication years.
- Generate enzyme-unit cohort summaries.
- Document why raw yield values cannot be pooled across units.

## Phase 3 — FAIR harmonisation

- Keep source columns unchanged in the raw CSV.
- Add parsed identifiers and numeric fields.
- Define the data dictionary and provenance YAML.
- Parse only process parameters that can be extracted conservatively.
- Retain raw text alongside every derived field.

## Phase 4 — Within-study benchmark

- Use Reference 10 as a relatively standardised case study.
- Predict multi-enzyme activity on the log-transformed target.
- Group by experiment ID in every validation split.
- Compare a dummy baseline with random forest and extra trees.
- Report median and interquartile validation metrics.

## Phase 5 — Cross-study benchmark

- Select xylanase records measured in U/gds.
- Group by complete article reference.
- Compare performance with the within-study model.
- Treat weak generalisation as a data-infrastructure finding.

## Phase 6 — Uncertainty and interpretability

- Train group-bootstrap ensembles.
- Report point estimates and 5th–95th percentile ranges.
- Export tree-based feature importance with a non-causal warning.

## Phase 7 — Dashboard

- Provide within-study and cross-study modes.
- Allow scenario inputs from observed cohort values.
- Show model metrics and uncertainty intervals.
- Display the source cohort for transparent interpretation.

## Phase 8 — Portfolio presentation

- Add one overview figure, one model-comparison figure, one prediction figure,
  and one feature-importance figure to the GitHub README.
- Record a 60–90 second dashboard demonstration.
- Link the repository in the CV or motivation letter only after the code and
  README are public and tested.

## Phase 9 — Research extension

- Develop a controlled vocabulary for substrates and fungal organisms.
- Link activity outputs to energy, water, material, waste, and LCA indicators.
- Request or collect standardized partner data.
- Evaluate hybrid mechanistic–machine-learning models.
- Add external validation on a genuinely independent dataset.
