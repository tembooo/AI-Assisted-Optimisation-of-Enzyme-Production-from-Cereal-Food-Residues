from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def _save_current(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def plot_top_counts(records: list[dict[str, Any]], field: str, path: str | Path, top_n: int = 12) -> None:
    counts = Counter(str(record.get(field, "")) or "<missing>" for record in records).most_common(top_n)
    labels = [label for label, _ in reversed(counts)]
    values = [value for _, value in reversed(counts)]
    plt.figure(figsize=(9, 6))
    plt.barh(labels, values)
    plt.xlabel("Number of records")
    plt.title(f"Most frequent {field.lower()} labels")
    _save_current(Path(path))


def plot_year_counts(records: list[dict[str, Any]], path: str | Path) -> None:
    counts = Counter(record.get("publication_year") for record in records if record.get("publication_year") is not None)
    years = sorted(counts)
    plt.figure(figsize=(8, 5))
    plt.bar(years, [counts[year] for year in years])
    plt.xlabel("Publication year")
    plt.ylabel("Number of records")
    plt.title("Literature-derived records by publication year")
    _save_current(Path(path))


def plot_model_comparison(summary_rows: list[dict[str, Any]], path: str | Path, title: str) -> None:
    rows = [row for row in summary_rows if row.get("summary")]
    names = [row["model"] for row in rows]
    values = [row["median_mae"] for row in rows]
    plt.figure(figsize=(8, 5))
    plt.bar(names, values)
    plt.ylabel("Median group-aware MAE")
    plt.title(title)
    plt.xticks(rotation=20)
    _save_current(Path(path))


def plot_predicted_vs_actual(rows: list[dict[str, Any]], path: str | Path, title: str) -> None:
    actual = np.asarray([float(row["actual_yield"]) for row in rows])
    predicted = np.asarray([float(row["predicted_yield"]) for row in rows])
    low = min(float(actual.min()), float(predicted.min()))
    high = max(float(actual.max()), float(predicted.max()))
    plt.figure(figsize=(6, 6))
    plt.scatter(actual, predicted, alpha=0.75)
    plt.plot([low, high], [low, high], linestyle="--")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Observed yield")
    plt.ylabel("Group-aware out-of-fold prediction")
    plt.title(title)
    _save_current(Path(path))


def plot_feature_importance(rows: list[dict[str, Any]], path: str | Path, title: str, top_n: int = 15) -> None:
    selected = rows[:top_n]
    labels = [row["feature"] for row in reversed(selected)]
    values = [float(row["importance"]) for row in reversed(selected)]
    plt.figure(figsize=(10, 7))
    plt.barh(labels, values)
    plt.xlabel("Tree-based importance")
    plt.title(title)
    _save_current(Path(path))
