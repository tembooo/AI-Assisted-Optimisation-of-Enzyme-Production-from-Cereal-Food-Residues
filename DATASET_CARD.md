# Dataset Card

## Source

**Production of enzymes via solid state fermentation from cereals — Version 2**  
Bourgine, J.; Teigiserova, D.; Thomsen, M.  
Mendeley Data DOI: `10.17632/k2xv3yss8m.2`  
Licence: **CC BY 4.0**

## Observed structure

The supplied workbook contains:

- **487** enzyme-output records;
- **209** experiment identifiers;
- **69** scientific references;
- **45** substrate labels;
- **111** organism or co-culture labels;
- **34** enzyme labels;
- **6** reported activity units;
- publication years from **2010 to 2019**.

There are **485 numeric yield records** and **458 numeric incubation-time records**.

## Important heterogeneity

Raw yield values cannot be pooled indiscriminately. Enzyme type and activity
unit define the measurement context. The most common comparable cohorts are:

- xylanase, U/gds: 60 records;
- CMCase, U/gds: 60 records;
- beta-glucosidase, U/gds: 51 records;
- FPase, U/gds: 35 records.

The semi-structured process fields contain pH, moisture, temperature,
inoculum, agitation, pretreatment, and supplementation information, but not
all variables are consistently reported.

## Intended use

This repository uses the data for:

1. a FAIR-oriented data audit;
2. leakage-aware modelling benchmarks;
3. uncertainty-aware demonstration predictions;
4. analysis of barriers to cross-study reuse.

## Out-of-scope uses

The data and prototype must not be used as validated industrial operating
instructions, safety-critical control logic, or a substitute for experiments.
