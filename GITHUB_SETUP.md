# GitHub Setup

## Repository form

**Owner**

```text
tembooo
```

**Repository name**

```text
fair-ssf-opt
```

**Description**

```text
FAIR-aligned, uncertainty-aware AI benchmarking for enzyme production from cereal residues via solid-state fermentation.
```

**Visibility**

```text
Public
```

Because this package already contains a README, `.gitignore`, and licence, do
not ask GitHub to create additional versions when importing the folder.

## Suggested topics

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
```

## Upload using Git

```bash
cd fair-ssf-opt
git init
git add .
git commit -m "Initialize FAIR-SSF-Opt research prototype"
git branch -M main
git remote add origin https://github.com/tembooo/fair-ssf-opt.git
git push -u origin main
```

## Recommended second commit

After running the pipeline and reviewing the figures:

```bash
git add README.md MODEL_CARD.md DATASET_CARD.md reports/figures data/processed artifacts/run_summary.json
git commit -m "Add group-aware modelling results and figures"
git push
```

The `.gitignore` currently excludes model binaries and generated figures/data
by default. Remove the relevant ignore lines only after you decide which
results should be tracked. Do not commit confidential data or credentials.
