from __future__ import annotations

import csv
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import joblib
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline

from .features import build_feature_dict


@dataclass(frozen=True)
class ModelSpec:
    name: str
    factory: Callable[[int], Any]


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec("dummy_median", lambda seed: DummyRegressor(strategy="median")),
        ModelSpec(
            "random_forest",
            lambda seed: RandomForestRegressor(
                n_estimators=100,
                min_samples_leaf=1,
                max_features=0.8,
                random_state=seed,
                n_jobs=1,
            ),
        ),
        ModelSpec(
            "extra_trees",
            lambda seed: ExtraTreesRegressor(
                n_estimators=100,
                min_samples_leaf=1,
                max_features=1.0,
                random_state=seed,
                n_jobs=1,
            ),
        ),
    ]


def build_pipeline(spec: ModelSpec, seed: int) -> Pipeline:
    return Pipeline(
        [
            ("vectorizer", DictVectorizer(sparse=False)),
            ("model", spec.factory(seed)),
        ]
    )


def _metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(actual, predicted)),
        "median_ae": float(median_absolute_error(actual, predicted)),
        "rmse": float(mean_squared_error(actual, predicted) ** 0.5),
        "r2": float(r2_score(actual, predicted)),
    }


def prepare_xyg(records: list[dict[str, Any]], group_field: str) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    features = [build_feature_dict(record) for record in records]
    target = np.asarray([float(record["yield_value"]) for record in records], dtype=float)
    groups = np.asarray([int(record[group_field]) for record in records], dtype=int)
    return features, target, groups


def evaluate_models(
    records: list[dict[str, Any]],
    *,
    group_field: str,
    n_splits: int = 25,
    test_size: float = 0.25,
    seed: int = 42,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    features, target, groups = prepare_xyg(records, group_field)
    splitter = GroupShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=seed)
    split_indices = list(splitter.split(features, target, groups))
    all_results: list[dict[str, Any]] = []

    for spec in model_specs():
        split_metrics: list[dict[str, float]] = []
        for split_number, (train_idx, test_idx) in enumerate(split_indices, start=1):
            model = build_pipeline(spec, seed + split_number)
            train_features = [features[i] for i in train_idx]
            test_features = [features[i] for i in test_idx]
            model.fit(train_features, np.log1p(target[train_idx]))
            prediction = np.expm1(model.predict(test_features))
            prediction = np.clip(prediction, 0, None)
            result = _metrics(target[test_idx], prediction)
            result.update({"model": spec.name, "split": split_number, "test_rows": len(test_idx)})
            split_metrics.append(result)
            all_results.append(result)

        summary: dict[str, Any] = {"model": spec.name, "splits": len(split_metrics)}
        for metric in ["mae", "median_ae", "rmse", "r2"]:
            values = np.asarray([row[metric] for row in split_metrics], dtype=float)
            summary[f"median_{metric}"] = float(np.median(values))
            summary[f"mean_{metric}"] = float(np.mean(values))
            summary[f"q25_{metric}"] = float(np.quantile(values, 0.25))
            summary[f"q75_{metric}"] = float(np.quantile(values, 0.75))
        all_results.append({"summary": True, **summary})

    summaries = [row for row in all_results if row.get("summary")]
    best = min(summaries, key=lambda row: row["median_mae"])
    return all_results, best


def out_of_fold_predictions(
    records: list[dict[str, Any]],
    *,
    group_field: str,
    model_name: str,
    n_splits: int = 5,
    seed: int = 42,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    features, target, groups = prepare_xyg(records, group_field)
    unique_groups = np.unique(groups)
    folds = min(n_splits, len(unique_groups))
    splitter = GroupKFold(n_splits=folds)
    spec = next(spec for spec in model_specs() if spec.name == model_name)
    predictions = np.full_like(target, fill_value=np.nan, dtype=float)

    for fold, (train_idx, test_idx) in enumerate(splitter.split(features, target, groups), start=1):
        model = build_pipeline(spec, seed + fold)
        model.fit([features[i] for i in train_idx], np.log1p(target[train_idx]))
        prediction = np.expm1(model.predict([features[i] for i in test_idx]))
        predictions[test_idx] = np.clip(prediction, 0, None)

    rows: list[dict[str, Any]] = []
    for idx, (record, actual, predicted) in enumerate(zip(records, target, predictions)):
        rows.append(
            {
                "row_index": idx,
                "experiment_id": record.get("experiment_id"),
                "reference_id": record.get("reference_id"),
                "enzyme": record.get("Enzyme"),
                "unit": record.get("Unit"),
                "actual_yield": float(actual),
                "predicted_yield": float(predicted),
                "absolute_error": float(abs(actual - predicted)),
            }
        )
    return rows, _metrics(target, predictions)


def train_bootstrap_bundle(
    records: list[dict[str, Any]],
    *,
    group_field: str,
    model_name: str,
    n_bootstrap: int = 40,
    seed: int = 42,
) -> dict[str, Any]:
    features, target, groups = prepare_xyg(records, group_field)
    spec = next(spec for spec in model_specs() if spec.name == model_name)
    final_model = build_pipeline(spec, seed)
    final_model.fit(features, np.log1p(target))

    rng = np.random.default_rng(seed)
    unique_groups = np.unique(groups)
    group_to_indices = {group: np.where(groups == group)[0] for group in unique_groups}
    bootstrap_models: list[Pipeline] = []

    for bootstrap_index in range(n_bootstrap):
        sampled_groups = rng.choice(unique_groups, size=len(unique_groups), replace=True)
        sampled_indices = np.concatenate([group_to_indices[group] for group in sampled_groups])
        model = build_pipeline(spec, seed + bootstrap_index + 1)
        model.fit([features[i] for i in sampled_indices], np.log1p(target[sampled_indices]))
        bootstrap_models.append(model)

    categorical_values = {
        field: sorted({str(record.get(field, "")) for record in records})
        for field in ["Substrate", "Organism", "Enzyme", "Unit"]
    }

    return {
        "model_name": model_name,
        "group_field": group_field,
        "final_model": final_model,
        "bootstrap_models": bootstrap_models,
        "target_transform": "log1p",
        "training_rows": len(records),
        "unique_groups": len(unique_groups),
        "categorical_values": categorical_values,
        "training_yield_min": float(np.min(target)),
        "training_yield_median": float(np.median(target)),
        "training_yield_max": float(np.max(target)),
    }


def predict_with_interval(bundle: dict[str, Any], feature_record: dict[str, Any]) -> dict[str, float]:
    features = [build_feature_dict(feature_record)]
    point = float(np.expm1(bundle["final_model"].predict(features)[0]))
    bootstrap = np.asarray(
        [float(np.expm1(model.predict(features)[0])) for model in bundle["bootstrap_models"]],
        dtype=float,
    )
    bootstrap = np.clip(bootstrap, 0, None)
    return {
        "prediction": max(point, 0.0),
        "p05": float(np.quantile(bootstrap, 0.05)),
        "p50": float(np.quantile(bootstrap, 0.50)),
        "p95": float(np.quantile(bootstrap, 0.95)),
    }


def feature_importance(bundle: dict[str, Any], top_n: int = 30) -> list[dict[str, Any]]:
    pipeline: Pipeline = bundle["final_model"]
    vectorizer: DictVectorizer = pipeline.named_steps["vectorizer"]
    model = pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        return []
    names = vectorizer.get_feature_names_out()
    values = np.asarray(model.feature_importances_, dtype=float)
    order = np.argsort(values)[::-1][:top_n]
    return [
        {"feature": str(names[index]), "importance": float(values[index])}
        for index in order
    ]


def save_bundle(path: str | Path, bundle: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path)


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
