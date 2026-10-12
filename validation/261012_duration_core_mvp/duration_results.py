"""Completed Core result CSV/JSON persistence; no acquisition or calculation."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from duration_config import STATES, calculation_fingerprint, validate_config

DATE_COLUMNS = ("date", "trend_reference_date", "recent_reference_date")
INTEGER_COLUMNS = ("segment", "observation_index", "core_score")
STRING_COLUMNS = ("series_id", "availability", "trend_state", "recent_move_state",
                  "representative_tenor", "duration_exposure", "rule_case", "core_availability")
FLOAT_COLUMNS = ("raw_yield_pct", "yield_pct", "smoothed_yield_bp", "trend_reference_bp",
                 "recent_reference_bp", "trend_value_bp", "recent_move_value_bp")
REQUIRED_COLUMNS = (*DATE_COLUMNS, *INTEGER_COLUMNS, *STRING_COLUMNS, *FLOAT_COLUMNS)


def validate_results(results, config):
    """Check the persisted contract and ordinal semantics without producing results."""
    validate_config(config)
    if not set(REQUIRED_COLUMNS).issubset(results.columns) or results.empty:
        raise ValueError("Missing completed result columns or empty result file")
    if results["date"].isna().any() or results.duplicated(["date", "duration_exposure"]).any():
        raise ValueError("Missing or duplicate exposure observation dates")
    if set(results["duration_exposure"].dropna()) != set(config["exposures"]):
        raise ValueError("Saved results must contain all three exposures")
    for exposure, identity in config["exposures"].items():
        rows = results.loc[results["duration_exposure"].eq(exposure)]
        if (not rows["date"].is_monotonic_increasing
                or not rows["series_id"].eq(identity["series_id"]).all()
                or not rows["representative_tenor"].eq(identity["representative_tenor"]).all()):
            raise ValueError(f"Invalid identity or date ordering for {exposure}")
    if results[list(FLOAT_COLUMNS)].apply(lambda s: np.isinf(s.astype(float)).any()).any():
        raise ValueError("Infinite analytical values")
    for column in ("trend_state", "recent_move_state"):
        if not results[column].dropna().isin(STATES).all():
            raise ValueError(f"Invalid {column}")
    if not results["availability"].isin(("accepted", "missing", "structural_gap")).all():
        raise ValueError("Invalid source availability")
    if not results["core_availability"].isin(("available", "warmup", "missing", "structural_gap")).all():
        raise ValueError("Invalid Core availability")
    available = results["core_availability"].eq("available")
    calculable = results["trend_state"].notna() & results["recent_move_state"].notna()
    if (not available.eq(results["core_score"].notna()).all()
            or not available.eq(calculable).all()
            or not available.eq(results["rule_case"].notna()).all()):
        raise ValueError("Inconsistent completed Core availability")
    if not results.loc[available, "availability"].eq("accepted").all():
        raise ValueError("Unavailable yields cannot have Core results")
    for value_column, state_column in (("trend_value_bp", "trend_state"),
                                       ("recent_move_value_bp", "recent_move_state")):
        if not results[value_column].notna().eq(results[state_column].notna()).all():
            raise ValueError(f"Inconsistent {state_column} availability")
    scores = results.loc[available, "core_score"]
    if not scores.between(-3, 3).all() or not scores.eq(scores.astype(int)).all():
        raise ValueError("Core scores must be ordinal integers from -3 to +3")
    # Validate existing lineage and codes; never replace or recalculate any column.
    for case, mappings in config["rules"].items():
        rows = results.loc[results["rule_case"].eq(case)]
        trend, recent = case.split(" × ")
        if not rows["trend_state"].eq(trend).all() or not rows["recent_move_state"].eq(recent).all():
            raise ValueError("Rule Case does not match saved Component States")
        for exposure, score in mappings.items():
            if not rows.loc[rows["duration_exposure"].eq(exposure), "core_score"].eq(score).all():
                raise ValueError("Saved score does not match metadata Rule Table")
    if not results.loc[available, "rule_case"].isin(config["rules"]).all():
        raise ValueError("Unknown Rule Case")
    accepted = results["availability"].eq("accepted")
    if (not results["yield_pct"].notna().eq(accepted).all()
            or results.loc[accepted, ["segment", "observation_index"]].isna().any().any()):
        raise ValueError("Inconsistent accepted Raw Observation lineage")
    gap = results["series_id"].eq("DGS30") & results["date"].between("2002-02-18", "2006-02-08")
    if (not results.loc[gap, "availability"].eq("structural_gap").all()
            or results.loc[gap, ["yield_pct", "core_score", "segment"]].notna().any().any()):
        raise ValueError("DGS30 structural discontinuation was not excluded")


def save_results(results, source_snapshot, config, output_dir):
    """Save all exposure histories and sufficient metadata for independent display."""
    config = validate_config(config)
    validate_results(results, config)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "duration_core.csv"
    json_path = output_dir / "duration_core_metadata.json"
    coverage = {}
    for exposure in config["exposures"]:
        rows = results.loc[results["duration_exposure"].eq(exposure)]
        valid = rows.loc[rows["core_availability"].eq("available"), "date"]
        coverage[exposure] = {
            "source_start": str(rows["date"].min().date()),
            "source_end": str(rows["date"].max().date()), "rows": len(rows),
            "core_start": None if valid.empty else str(valid.min().date()),
            "core_end": None if valid.empty else str(valid.max().date()),
            "available_results": len(valid),
        }
    csv_tmp = csv_path.with_suffix(".csv.tmp")
    results.to_csv(csv_tmp, index=False, date_format="%Y-%m-%d")
    metadata = {
        "format_version": 1, "result_kind": "Core Duration Evaluation Result",
        "score_semantics": "Seven-level ordinal economic judgment, not a return estimate",
        "units": {"yield": "percent", "component_values": "basis_points"},
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "configuration": config, "calculation_fingerprint": calculation_fingerprint(config),
        "source_snapshot": source_snapshot, "coverage": coverage,
        "csv_sha256": hashlib.sha256(csv_tmp.read_bytes()).hexdigest(),
        "rows": len(results),
    }
    json_tmp = json_path.with_suffix(".json.tmp")
    json_tmp.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    csv_tmp.replace(csv_path)
    json_tmp.replace(json_path)
    return csv_path, json_path


def load_results(output_dir, expected_config=None):
    """Load saved results only; raise on corruption or analytical config mismatch.

    Omitting expected_config intentionally inspects the saved snapshot, regardless
    of subsequent YAML edits. Historical presets are stored in its metadata.
    """
    output_dir = Path(output_dir)
    csv_path = output_dir / "duration_core.csv"
    metadata = json.loads((output_dir / "duration_core_metadata.json").read_text(encoding="utf-8"))
    if metadata.get("format_version") != 1:
        raise ValueError("Unsupported result format")
    config = validate_config(metadata["configuration"])
    fingerprint = calculation_fingerprint(config)
    if metadata["calculation_fingerprint"] != fingerprint:
        raise ValueError("Metadata calculation fingerprint mismatch")
    if expected_config is not None and calculation_fingerprint(expected_config) != fingerprint:
        raise ValueError("Configuration mismatch: explicitly recalculate and save, "
                         "or omit expected_config to inspect the saved snapshot")
    if hashlib.sha256(csv_path.read_bytes()).hexdigest() != metadata["csv_sha256"]:
        raise ValueError("Saved CSV checksum mismatch")
    results = pd.read_csv(csv_path, parse_dates=list(DATE_COLUMNS), float_precision="round_trip",
                          dtype={**{c: "Int64" for c in INTEGER_COLUMNS},
                                 **{c: "string" for c in STRING_COLUMNS}})
    for column in DATE_COLUMNS:
        results[column] = pd.to_datetime(results[column]).astype("datetime64[ns]")
    if len(results) != metadata["rows"]:
        raise ValueError("Saved row count mismatch")
    validate_results(results, config)
    return results, metadata
