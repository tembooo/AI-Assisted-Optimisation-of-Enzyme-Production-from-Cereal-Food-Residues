# Interview Notes

## Question

**What would be your first proposed AI model for CIRC4FOOD?**

## 90-second answer

My first model would be a FAIR-aligned, uncertainty-aware surrogate model for
circular food-bioprocess data. I would start with a focused and measurable use
case rather than a complex deep network. In this prototype, I use literature
data on enzyme production from cereal and agro-industrial residues through
fungal solid-state fermentation.

The workflow first harmonises substrate, organism, enzyme, activity unit,
incubation time, pretreatment, supplementation, optimisation method, and
available process parameters. I then benchmark interpretable ensemble models
using group-aware validation. Outputs from the same experiment are kept in the
same fold, and the cross-study test holds out complete scientific articles.
This prevents optimistic leakage and measures whether a model transfers to
unseen data sources.

The preliminary result is scientifically useful: a relatively standardised
within-study cohort is partly learnable, while cross-study xylanase prediction
is weak. This suggests that the main first contribution for CIRC4FOOD should
combine AI with a FAIR consortium data schema, common units, provenance,
quality flags, and uncertainty reporting. As partner data improve, the same
pipeline can evolve into hybrid process models and multi-objective decision
support for yield, energy, water, waste, and environmental impact.

## Key message

The prototype does not claim that an algorithm can compensate for poor data.
It demonstrates how FAIR infrastructure and leakage-aware AI must be designed
together.
