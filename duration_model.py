"""Provisional Duration Stage 1 calculations; no retrieval or ETF evaluation.

Boundaries are DataFrames of endpoint Features, Component Values / States,
and a human-facing View dict. Inputs are not mutated. Lags count observations.
"""
from pathlib import Path
import math

import numpy as np
import pandas as pd
import yaml


def load_config(path="duration_mvp.yaml"):
    """Load and validate the small MVP specification before calculations."""
    config = yaml.safe_load(Path(path).read_text())
    dates = pd.DatetimeIndex(config["as_of_dates"])
    if dates.empty or dates.has_duplicates or dates.hasnans:
        raise ValueError("as_of_dates must be nonempty, unique dates")
    if pd.Timestamp(config["history_start"]) >= dates.min():
        raise ValueError("history_start must precede every as_of date")
    if not config["series"] or not config["features"] or not config["components"]:
        raise ValueError("Series, Features and Components must be nonempty")
    for source in config["series"].values():
        if not source["id"] or source["frequency"] not in {"business_daily", "daily", "monthly"}:
            raise ValueError("Invalid series identifier or frequency")
        if type(source["max_age_days"]) is not int or source["max_age_days"] <= 0:
            raise ValueError("max_age_days must be a positive integer")
    for feature in config["features"].values():
        source = config["series"][feature["series"]]
        if feature["transform"] not in {"smoothed_level", "year_over_year"}:
            raise ValueError("Unsupported Feature transform")
        for key in ("smoothing", "lag"):
            if type(feature[key]) is not int or feature[key] <= 0:
                raise ValueError(f"{key} must be a positive integer")
        if feature["transform"] == "year_over_year":
            if source["frequency"] != "monthly" or feature["year_periods"] != 12:
                raise ValueError("Year-over-year Feature requires 12 monthly periods")
    view = config["view"]
    if list(view["contributions"]) != list(config["components"]):
        raise ValueError("View must reference all Components in declaration order")
    for name, component in config["components"].items():
        if component["feature"] not in config["features"]:
            raise ValueError(f"Unknown Feature for {name}")
        for key in ("scale", "threshold"):
            if not math.isfinite(component[key]) or component[key] <= 0:
                raise ValueError(f"{key} must be finite and positive")
        states = component["states"]
        if len(states) != 3 or len(set(states)) != 3:
            raise ValueError("Each Component requires three distinct ordered States")
        if set(view["contributions"][name]) != set(states):
            raise ValueError(f"Incomplete View mapping for {name}")
        if not all(math.isfinite(v) for v in view["contributions"][name].values()):
            raise ValueError("Nonfinite View contribution")
    if not math.isfinite(view["threshold"]) or view["threshold"] <= 0:
        raise ValueError("View threshold must be finite and positive")
    if len(view["labels"]) != 3 or len(set(view["labels"])) != 3:
        raise ValueError("View requires three distinct labels")
    return config


def calculate_features(raw, config, as_of):
    """Use date-indexed, as-of-vintage Raw Observations to form endpoint pairs.

    Each Series must carry attrs['vintage_date'] matching as_of. The notebook
    verifies the ALFRED vintage column before attaching this provenance.
    Trace dates delimit exact rolling windows; YoY denominator dates are
    retained separately. No forward filling or partial rolling windows.
    """
    as_of = pd.Timestamp(as_of)
    rows = []
    for name, spec in config["features"].items():
        source = config["series"][spec["series"]]
        observations = raw[spec["series"]]
        if pd.Timestamp(observations.attrs.get("vintage_date")) != as_of:
            raise ValueError(f"{name}: missing or mismatched as-of vintage")
        if not isinstance(observations.index, pd.DatetimeIndex):
            raise ValueError(f"{name}: expected date-indexed observations")
        if observations.index.has_duplicates or not observations.index.is_monotonic_increasing:
            raise ValueError(f"{name}: duplicate or unordered observation dates")
        series = observations.loc[:as_of].dropna().astype(float)
        if series.empty or not np.isfinite(series).all():
            raise ValueError(f"{name}: missing or nonfinite observations")
        if (as_of - series.index[-1]).days > source["max_age_days"]:
            raise ValueError(f"{name}: stale observations")
        if source["frequency"] == "monthly":
            expected = pd.period_range(series.index[0], series.index[-1], freq="M")
            if not series.index.to_period("M").equals(expected):
                raise ValueError(f"{name}: missing or duplicate monthly periods")
        elif source["frequency"] == "daily":
            if not series.index.equals(pd.date_range(series.index[0], series.index[-1])):
                raise ValueError(f"{name}: missing calendar-day observations")
        elif series.index.to_series().diff().dt.days.max() > 7:
            raise ValueError(f"{name}: excessive gap in business observations")
        year = spec.get("year_periods", 0) if spec["transform"] == "year_over_year" else 0
        required = spec["lag"] + spec["smoothing"] + year
        if len(series) < required:
            raise ValueError(f"{name}: needs {required} observations; has {len(series)}")
        transformed = series
        if year:
            if (series <= 0).any():
                raise ValueError("CPI index must be positive")
            transformed = (series / series.shift(year) - 1) * 100
        smoothed = transformed.rolling(spec["smoothing"], min_periods=spec["smoothing"]).mean()
        current_pos, base_pos = len(series) - 1, len(series) - 1 - spec["lag"]
        row = {"feature": name, "as_of": as_of, "series_id": source["id"],
               "vintage_date": as_of, "current": smoothed.iloc[current_pos],
               "base": smoothed.iloc[base_pos], "lag_observations": spec["lag"],
               "smoothing": spec["smoothing"], "transform": spec["transform"]}
        for endpoint, pos in (("current", current_pos), ("base", base_pos)):
            start = pos - spec["smoothing"] + 1
            row[f"{endpoint}_start"] = series.index[start]
            row[f"{endpoint}_end"] = series.index[pos]
            row[f"{endpoint}_denominator_start"] = series.index[start - year] if year else pd.NaT
            row[f"{endpoint}_denominator_end"] = series.index[pos - year] if year else pd.NaT
        rows.append(row)
    return pd.DataFrame(rows).set_index("feature")


def calculate_components(features, config):
    """Component Values are endpoint changes; States use inclusive neutral bands."""
    rows = []
    for name, spec in config["components"].items():
        feature = features.loc[spec["feature"]]
        value = float((feature["current"] - feature["base"]) * spec["scale"])
        if not math.isfinite(value):
            raise ValueError(f"{name}: nonfinite Component Value")
        threshold = spec["threshold"]
        state = spec["states"][0 if value < -threshold else 2 if value > threshold else 1]
        rows.append({"component": name, "as_of": feature["as_of"], "value": value,
                     "units": spec["units"], "state": state, "threshold": threshold,
                     "feature": spec["feature"]})
    return pd.DataFrame(rows).set_index("component")


def calculate_view(components, config):
    """Interpret only Component States; expose each contribution and Rule Case."""
    if components["as_of"].nunique() != 1:
        raise ValueError("View requires Components from exactly one as_of date")
    spec = config["view"]
    contributions = {name: spec["contributions"][name][components.loc[name, "state"]]
                     for name in spec["contributions"]}
    tally = sum(contributions.values())
    threshold = spec["threshold"]
    label = spec["labels"][0 if tally <= -threshold else 2 if tally >= threshold else 1]
    return {"as_of": components["as_of"].iloc[0], "view": label, "tally": tally,
            "rule_case": {name: components.loc[name, "state"] for name in contributions},
            "contributions": contributions}
