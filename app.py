from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import joblib
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fair_ssf_opt.features import make_interactive_record  # noqa: E402
from fair_ssf_opt.modeling import predict_with_interval  # noqa: E402

st.set_page_config(page_title="FAIR-SSF-Opt", layout="wide")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


st.title("FAIR-SSF-Opt")
st.caption("FAIR-aligned AI benchmarking for enzyme production from cereal residues via solid-state fermentation")

summary_path = PROJECT_ROOT / "artifacts" / "run_summary.json"
if not summary_path.exists():
    st.error("Model artifacts are missing. Run `python scripts/run_pipeline.py` first.")
    st.stop()

summary = load_json(summary_path)
mode_labels = {
    "within_study_reference_10": "Within-study benchmark (Reference 10)",
    "cross_study_xylanase_u_gds": "Cross-study xylanase benchmark (U/gds)",
}
mode = st.sidebar.selectbox("Prototype mode", list(mode_labels), format_func=lambda key: mode_labels[key])

bundle_path = PROJECT_ROOT / "artifacts" / f"{mode}_model_bundle.joblib"
bundle = joblib.load(bundle_path)
cohort_path = PROJECT_ROOT / "data" / "processed" / f"{mode}.csv"
cohort = load_csv(cohort_path)

st.warning(
    "This is a literature-derived research prototype. Predictions are not validated industrial recommendations, "
    "and the interval reflects model resampling rather than complete scientific uncertainty."
)

col1, col2, col3, col4 = st.columns(4)
cohort_summary = summary["cohorts"][mode]
col1.metric("Rows", cohort_summary["rows"])
col2.metric("Independent groups", cohort_summary["groups"])
col3.metric("Selected model", cohort_summary["best_model"])
col4.metric("Group-KFold MAE", f"{cohort_summary['group_kfold_oof_metrics']['mae']:.2f}")

st.subheader("Scenario prediction")
values = bundle["categorical_values"]
left, right = st.columns(2)
with left:
    substrate = st.selectbox("Substrate", values["Substrate"])
    organism = st.selectbox("Organism", values["Organism"])
    enzyme = st.selectbox("Enzyme", values["Enzyme"])
    unit = st.selectbox("Unit", values["Unit"])
    incubation = st.number_input("Incubation time (hours)", min_value=0.0, max_value=1000.0, value=168.0, step=12.0)
with right:
    ph = st.number_input("Initial pH", min_value=0.0, max_value=14.0, value=5.0, step=0.1)
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=100.0, value=28.0, step=0.5)
    moisture = st.number_input("Moisture content (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    agitation = st.number_input("Agitation (rpm; use 0 for static SSF)", min_value=0.0, max_value=3000.0, value=0.0, step=25.0)
    pretreatment = st.selectbox("Pretreatment description", sorted({row["Pretreatment"] for row in cohort}))
    supplement = st.selectbox(
        "Supplement description",
        sorted({row["Nutritive or inducing supplement"] for row in cohort}),
    )
    optimization = st.selectbox(
        "Optimisation method",
        sorted({row["Enhancement or optimization method"] for row in cohort}),
    )

record = make_interactive_record(
    substrate=substrate,
    organism=organism,
    enzyme=enzyme,
    unit=unit,
    incubation_hours=incubation,
    ph=ph,
    temperature_c=temperature,
    moisture_content_pct=moisture,
    agitation_rpm=agitation,
    pretreatment=pretreatment,
    supplement=supplement,
    optimization_method=optimization,
)
result = predict_with_interval(bundle, record)

p1, p2, p3 = st.columns(3)
p1.metric("Point prediction", f"{result['prediction']:.2f} {unit}")
p2.metric("Bootstrap 5th percentile", f"{result['p05']:.2f} {unit}")
p3.metric("Bootstrap 95th percentile", f"{result['p95']:.2f} {unit}")

figure = go.Figure()
figure.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=result["prediction"],
        title={"text": f"Predicted enzyme activity ({unit})"},
        gauge={
            "axis": {"range": [0, max(bundle["training_yield_max"], result["p95"]) * 1.05]},
            "steps": [
                {"range": [result["p05"], result["p95"]]},
            ],
        },
    )
)
st.plotly_chart(figure, use_container_width=True)

st.subheader("Model validation")
st.json(cohort_summary)

st.subheader("Training cohort browser")
preview_fields = [
    "XP n°",
    "Substrate",
    "Organism",
    "Enzyme",
    "Yield",
    "Unit",
    "Incubation time (hrs)",
    "Date of publication",
    "Reference",
]
st.dataframe([{field: row.get(field, "") for field in preview_fields} for row in cohort], use_container_width=True)

st.subheader("Interpretation")
st.markdown(
    """
- The **within-study model** tests whether a relatively standardized experimental table is learnable when all enzyme outputs from the same experiment stay in the same validation fold.
- The **cross-study model** tests transportability across scientific articles by keeping complete references out of training folds.
- A weak cross-study result is scientifically informative: it indicates that harmonized metadata, comparable units, and consistent process measurements are prerequisites for reusable AI in consortium settings.
"""
)
