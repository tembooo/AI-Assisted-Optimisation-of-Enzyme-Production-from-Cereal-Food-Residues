from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fair_ssf_opt.data import (  # noqa: E402
    cohort_summary,
    load_records,
    profile_records,
    save_json,
    select_cross_study_case,
    select_within_study_case,
    write_records,
)
from fair_ssf_opt.modeling import (  # noqa: E402
    evaluate_models,
    feature_importance,
    out_of_fold_predictions,
    save_bundle,
    train_bootstrap_bundle,
    write_csv,
)
from fair_ssf_opt.reporting import (  # noqa: E402
    plot_feature_importance,
    plot_model_comparison,
    plot_predicted_vs_actual,
    plot_top_counts,
    plot_year_counts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the FAIR-SSF-Opt prototype pipeline.")
    parser.add_argument(
        "--data",
        default=str(PROJECT_ROOT / "data" / "raw" / "ssf_enzyme_production.csv"),
        help="Path to the harmonized CSV exported from the source workbook.",
    )
    parser.add_argument("--splits", type=int, default=10, help="Repeated group-aware validation splits.")
    parser.add_argument("--bootstrap", type=int, default=15, help="Number of group-bootstrap models.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    records = load_records(data_path)

    processed = PROJECT_ROOT / "data" / "processed"
    artifacts = PROJECT_ROOT / "artifacts"
    figures = PROJECT_ROOT / "reports" / "figures"
    processed.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    profile = profile_records(records)
    save_json(processed / "data_profile.json", profile)
    write_csv(processed / "cohort_summary.csv", cohort_summary(records))

    plot_top_counts(records, "Enzyme", figures / "top_enzymes.png")
    plot_top_counts(records, "Substrate", figures / "top_substrates.png")
    plot_year_counts(records, figures / "publication_years.png")

    configurations = [
        {
            "name": "within_study_reference_10",
            "records": select_within_study_case(records, reference_id=10),
            "group_field": "experiment_id",
            "description": "Reference 10 multi-enzyme case; grouped by experiment ID.",
        },
        {
            "name": "cross_study_xylanase_u_gds",
            "records": select_cross_study_case(records, enzyme="xylanase", unit="U/gds"),
            "group_field": "reference_id",
            "description": "Cross-study xylanase cohort; grouped by article reference.",
        },
    ]

    run_summary: dict[str, object] = {"data_profile": profile, "cohorts": {}}

    for config in configurations:
        name = config["name"]
        cohort_records = config["records"]
        group_field = config["group_field"]
        write_records(
            processed / f"{name}.csv",
            cohort_records,
            [
                "XP n°",
                "Substrate",
                "Organism",
                "Enzyme",
                "Yield",
                "Unit",
                "Incubation time (hrs)",
                "Pretreatment",
                "Nutritive or inducing supplement",
                "Enhancement or optimization method",
                "Parameters",
                "Notes",
                "Date of publication",
                "Reference",
                "yield_value",
                "incubation_hours",
                "experiment_id",
                "publication_year",
                "reference_id",
            ],
        )

        results, best = evaluate_models(
            cohort_records,
            group_field=group_field,
            n_splits=args.splits,
            test_size=0.25,
            seed=42,
        )
        write_csv(processed / f"{name}_validation.csv", results)
        plot_model_comparison(results, figures / f"{name}_model_comparison.png", name.replace("_", " ").title())

        best_model = str(best["model"])
        oof_rows, oof_metrics = out_of_fold_predictions(
            cohort_records,
            group_field=group_field,
            model_name=best_model,
            n_splits=5,
            seed=42,
        )
        write_csv(processed / f"{name}_oof_predictions.csv", oof_rows)
        plot_predicted_vs_actual(
            oof_rows,
            figures / f"{name}_predicted_vs_actual.png",
            name.replace("_", " ").title(),
        )

        bundle = train_bootstrap_bundle(
            cohort_records,
            group_field=group_field,
            model_name=best_model,
            n_bootstrap=args.bootstrap,
            seed=42,
        )
        save_bundle(artifacts / f"{name}_model_bundle.joblib", bundle)
        importance = feature_importance(bundle)
        write_csv(processed / f"{name}_feature_importance.csv", importance)
        if importance:
            plot_feature_importance(
                importance,
                figures / f"{name}_feature_importance.png",
                name.replace("_", " ").title(),
            )

        run_summary["cohorts"][name] = {
            "description": config["description"],
            "rows": len(cohort_records),
            "groups": len({record[group_field] for record in cohort_records}),
            "best_model": best_model,
            "repeated_group_validation": best,
            "group_kfold_oof_metrics": oof_metrics,
        }

    save_json(artifacts / "run_summary.json", run_summary)
    print(json.dumps(run_summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
