from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

MISSING_TOKENS = {"", "na", "n/a", "none available", "not available"}


def clean_text(value: Any) -> str:
    """Return normalized text while preserving scientific symbols."""
    if value is None:
        return ""
    text = str(value).replace("\u00a0", " ").replace("\r", " ").replace("\n", " ")
    return " ".join(text.split()).strip()


def parse_float(value: Any) -> float | None:
    """Parse numeric values, including decimal commas, and return None for NA."""
    text = clean_text(value)
    if not text or text.lower() in MISSING_TOKENS:
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def parse_int(value: Any) -> int | None:
    number = parse_float(value)
    if number is None:
        return None
    return int(number)


def load_records(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        records: list[dict[str, Any]] = []
        for row in reader:
            normalized = {key: clean_text(value) for key, value in row.items()}
            normalized["yield_value"] = parse_float(normalized.get("Yield"))
            normalized["incubation_hours"] = parse_float(normalized.get("Incubation time (hrs)"))
            normalized["experiment_id"] = parse_int(normalized.get("XP n°"))
            normalized["publication_year"] = parse_int(normalized.get("Date of publication"))
            normalized["reference_id"] = parse_int(normalized.get("Reference"))
            records.append(normalized)
    return records


def write_records(path: str | Path, records: Iterable[dict[str, Any]], fields: list[str]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def profile_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    numeric_yields = [r["yield_value"] for r in records if r["yield_value"] is not None]
    numeric_incubation = [r["incubation_hours"] for r in records if r["incubation_hours"] is not None]

    def count(field: str) -> Counter[str]:
        return Counter(clean_text(r.get(field)) or "<missing>" for r in records)

    experiment_ids = {r["experiment_id"] for r in records if r["experiment_id"] is not None}
    references = {r["reference_id"] for r in records if r["reference_id"] is not None}
    years = sorted({r["publication_year"] for r in records if r["publication_year"] is not None})

    cohort_counts: Counter[tuple[str, str]] = Counter(
        (r.get("Enzyme", ""), r.get("Unit", ""))
        for r in records
        if r["yield_value"] is not None
    )

    return {
        "rows": len(records),
        "numeric_yield_rows": len(numeric_yields),
        "missing_or_nonnumeric_yield_rows": len(records) - len(numeric_yields),
        "experiments": len(experiment_ids),
        "references": len(references),
        "publication_year_min": min(years) if years else None,
        "publication_year_max": max(years) if years else None,
        "unique_substrates": len(count("Substrate")),
        "unique_organisms": len(count("Organism")),
        "unique_enzymes": len(count("Enzyme")),
        "unique_units": len(count("Unit")),
        "numeric_incubation_rows": len(numeric_incubation),
        "top_substrates": count("Substrate").most_common(10),
        "top_organisms": count("Organism").most_common(10),
        "top_enzymes": count("Enzyme").most_common(10),
        "unit_counts": count("Unit").most_common(),
        "top_enzyme_unit_cohorts": [
            {"enzyme": enzyme, "unit": unit, "rows": n}
            for (enzyme, unit), n in cohort_counts.most_common(20)
        ],
    }


def cohort_summary(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["yield_value"] is None:
            continue
        grouped[(record.get("Enzyme", ""), record.get("Unit", ""))].append(record)

    output: list[dict[str, Any]] = []
    for (enzyme, unit), rows in grouped.items():
        yields = sorted(float(r["yield_value"]) for r in rows)
        n = len(yields)
        median = yields[n // 2] if n % 2 else (yields[n // 2 - 1] + yields[n // 2]) / 2
        output.append(
            {
                "enzyme": enzyme,
                "unit": unit,
                "rows": n,
                "experiments": len({r["experiment_id"] for r in rows}),
                "references": len({r["reference_id"] for r in rows}),
                "yield_min": min(yields),
                "yield_median": median,
                "yield_max": max(yields),
            }
        )
    return sorted(output, key=lambda row: (-int(row["rows"]), row["enzyme"], row["unit"]))


def select_within_study_case(records: list[dict[str, Any]], reference_id: int = 10) -> list[dict[str, Any]]:
    """Structured multi-enzyme case study from a single reference."""
    return [
        r
        for r in records
        if r["reference_id"] == reference_id
        and r["yield_value"] is not None
        and r["experiment_id"] is not None
    ]


def select_cross_study_case(
    records: list[dict[str, Any]], enzyme: str = "xylanase", unit: str = "U/gds"
) -> list[dict[str, Any]]:
    """Cross-study cohort with comparable enzyme and unit labels."""
    return [
        r
        for r in records
        if r.get("Enzyme", "").casefold() == enzyme.casefold()
        and r.get("Unit", "").casefold() == unit.casefold()
        and r["yield_value"] is not None
        and r["reference_id"] is not None
    ]


def save_json(path: str | Path, payload: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
