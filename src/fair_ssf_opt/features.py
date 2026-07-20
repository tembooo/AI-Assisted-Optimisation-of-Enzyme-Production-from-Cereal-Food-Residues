from __future__ import annotations

import re
from typing import Any

from .data import clean_text


def _decimalize(text: str) -> str:
    return text.replace(",", ".")


def _first_float(text: str, patterns: list[str], lower: float | None = None, upper: float | None = None) -> float | None:
    normalized = _decimalize(clean_text(text))
    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if not match:
            continue
        try:
            value = float(match.group(1))
        except (TypeError, ValueError):
            continue
        if lower is not None and value < lower:
            continue
        if upper is not None and value > upper:
            continue
        return value
    return None


def parse_process_parameters(text: str) -> dict[str, float | None]:
    """Extract selected process parameters from semi-structured text.

    The parser is intentionally conservative. Missing or ambiguous values remain None.
    """
    return {
        "ph": _first_float(text, [r"\bpH\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)"], 0, 14),
        "temperature_c": _first_float(
            text,
            [
                r"\bT(?:°|o)?C?\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)",
                r"([0-9]+(?:\.[0-9]+)?)\s*°\s*C",
            ],
            0,
            100,
        ),
        "moisture_content_pct": _first_float(
            text,
            [r"\bMC\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)\s*%"],
            0,
            100,
        ),
        "agitation_rpm": _first_float(
            text,
            [r"\bAgitation\s*[=:]\s*([0-9]+(?:\.[0-9]+)?)\s*rpm"],
            0,
            5000,
        ),
    }


def optimization_category(text: str) -> str:
    value = clean_text(text).casefold()
    if value in {"", "none", "na", "n/a"}:
        return value or "missing"
    if any(token in value for token in ["rsm", "response surface", "box-behnken", "central composite", "plackett"]):
        return "RSM"
    if any(token in value for token in ["ofat", "one factor"]):
        return "OFAT"
    if "taguchi" in value:
        return "Taguchi"
    if any(token in value for token in ["simplex", "mixture design"]):
        return "MixtureDesign"
    return "Other"


def substrate_family(text: str) -> str:
    value = clean_text(text).casefold()
    families = [
        cereal
        for cereal in ["wheat", "rice", "corn", "oat", "sorghum", "millet", "barley", "rye"]
        if cereal in value
    ]
    return "+".join(sorted(set(families))) if families else "other"


def organism_genus(text: str) -> str:
    value = clean_text(text)
    if value.casefold().startswith("co-culture"):
        return "Co-culture"
    return value.split()[0] if value else "unknown"


def _flag(text: str, tokens: list[str]) -> int:
    value = clean_text(text).casefold()
    return int(any(token in value for token in tokens))


def build_feature_dict(record: dict[str, Any]) -> dict[str, Any]:
    substrate = clean_text(record.get("Substrate"))
    organism = clean_text(record.get("Organism"))
    enzyme = clean_text(record.get("Enzyme"))
    unit = clean_text(record.get("Unit"))
    pretreatment = clean_text(record.get("Pretreatment"))
    supplement = clean_text(record.get("Nutritive or inducing supplement"))
    parameters = clean_text(record.get("Parameters"))
    parsed = parse_process_parameters(parameters)

    pretreatment_folded = pretreatment.casefold()
    supplement_folded = supplement.casefold()

    return {
        "substrate": substrate,
        "substrate_family": substrate_family(substrate),
        "organism": organism,
        "organism_genus": organism_genus(organism),
        "enzyme": enzyme,
        "unit": unit,
        "incubation_hours": record.get("incubation_hours") if record.get("incubation_hours") is not None else -1.0,
        "ph": parsed["ph"] if parsed["ph"] is not None else -1.0,
        "temperature_c": parsed["temperature_c"] if parsed["temperature_c"] is not None else -1.0,
        "moisture_content_pct": parsed["moisture_content_pct"] if parsed["moisture_content_pct"] is not None else -1.0,
        "agitation_rpm": parsed["agitation_rpm"] if parsed["agitation_rpm"] is not None else -1.0,
        "substrate_is_mixture": int(substrate.casefold().startswith("mixture")),
        "organism_is_coculture": int(organism.casefold().startswith("co-culture")),
        "pretreatment_missing_or_none": int(pretreatment_folded in {"", "none", "na", "n/a"}),
        "pretreatment_autoclave_or_sterilize": _flag(pretreatment, ["autoclav", "sterilis"]),
        "pretreatment_dried": _flag(pretreatment, ["dried", "air-dried", "oven-dried"]),
        "pretreatment_ground_or_milled": _flag(pretreatment, ["ground", "milled", "grinded"]),
        "pretreatment_chemical": _flag(pretreatment, ["acid", "alkali", "ammonia", "naoh", "hcl", "peroxide"]),
        "supplement_missing_or_none": int(supplement_folded in {"", "none", "na", "n/a"}),
        "supplement_yeast_extract": _flag(supplement, ["yeast extract", " ye ", "ye+"]),
        "supplement_nitrogen_source": _flag(supplement, ["nh4", "nitrate", "peptone", "urea", "ammonium"]),
        "optimization_category": optimization_category(record.get("Enhancement or optimization method", "")),
        "publication_year": float(record.get("publication_year") or -1),
    }


def make_interactive_record(
    *,
    substrate: str,
    organism: str,
    enzyme: str,
    unit: str,
    incubation_hours: float,
    ph: float | None,
    temperature_c: float | None,
    moisture_content_pct: float | None,
    agitation_rpm: float | None,
    pretreatment: str,
    supplement: str,
    optimization_method: str,
    publication_year: int = 2018,
) -> dict[str, Any]:
    parameter_parts: list[str] = []
    if ph is not None:
        parameter_parts.append(f"pH={ph}")
    if moisture_content_pct is not None:
        parameter_parts.append(f"MC={moisture_content_pct}%")
    if temperature_c is not None:
        parameter_parts.append(f"T°={temperature_c}°C")
    if agitation_rpm is not None:
        parameter_parts.append(f"Agitation={agitation_rpm}rpm")

    return {
        "Substrate": substrate,
        "Organism": organism,
        "Enzyme": enzyme,
        "Unit": unit,
        "Incubation time (hrs)": str(incubation_hours),
        "incubation_hours": float(incubation_hours),
        "Pretreatment": pretreatment,
        "Nutritive or inducing supplement": supplement,
        "Enhancement or optimization method": optimization_method,
        "Parameters": " ; ".join(parameter_parts),
        "Date of publication": str(publication_year),
        "publication_year": int(publication_year),
    }
