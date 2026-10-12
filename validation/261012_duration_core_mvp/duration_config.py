"""Small, MVP-local configuration contract; no application framework."""

import hashlib
import json
import math
from copy import deepcopy
from datetime import date
from pathlib import Path

import yaml

STATES = ("Falling", "Stable", "Rising")
EXPOSURES = {
    "Short": {"representative_tenor": "6M", "series_id": "DGS6MO"},
    "Intermediate": {"representative_tenor": "10Y", "series_id": "DGS10"},
    "Long": {"representative_tenor": "30Y", "series_id": "DGS30"},
}


def validate_config(config):
    """Validate all required keys and economic domains; return an owned copy."""
    def keys(value, expected, context):
        if not isinstance(value, dict) or set(value) != set(expected):
            raise ValueError(f"{context}: expected keys {list(expected)}")

    keys(config, ("trend", "recent_move", "exposures", "rules", "historical_events"), "config")
    keys(config["trend"], ("lookback_observations", "smoothing_observations",
         "entry_threshold_bp", "stabilization_enabled", "persistence",
         "hysteresis_bp", "direct_reversal"), "trend")
    keys(config["recent_move"], ("lookback_observations", "threshold_bp"), "recent_move")
    for section, names in (("trend", ("lookback_observations", "smoothing_observations", "persistence")),
                           ("recent_move", ("lookback_observations",))):
        for name in names:
            value = config[section][name]
            if type(value) is not int or value < 1:
                raise ValueError(f"{section}.{name} must be a positive integer")
    for section, name in (("trend", "entry_threshold_bp"), ("trend", "hysteresis_bp"),
                           ("recent_move", "threshold_bp")):
        value = config[section][name]
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{section}.{name} must be finite and nonnegative")
    if config["trend"]["entry_threshold_bp"] <= config["trend"]["hysteresis_bp"]:
        raise ValueError("Trend entry threshold must exceed hysteresis")
    for name in ("stabilization_enabled", "direct_reversal"):
        if type(config["trend"][name]) is not bool:
            raise ValueError(f"trend.{name} must be boolean")
    if config["exposures"] != EXPOSURES:
        raise ValueError("This MVP requires the accepted three exposure/tenor/series identities")
    cases = [f"{a} × {b}" for a in STATES for b in STATES]
    keys(config["rules"], cases, "rules")
    for case, scores in config["rules"].items():
        keys(scores, EXPOSURES, case)
        if any(type(score) is not int or not -3 <= score <= 3 for score in scores.values()):
            raise ValueError(f"{case}: scores must be ordinal integers from -3 to +3")
    if not isinstance(config["historical_events"], dict):
        raise ValueError("historical_events must be a mapping")
    for name, window in config["historical_events"].items():
        if not isinstance(name, str) or not name or name == "Custom period":
            raise ValueError("Event names must be nonempty and distinct from Custom period")
        keys(window, ("start", "end"), name)
        try:
            start, end = (date.fromisoformat(window[k]) for k in ("start", "end"))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name}: use quoted ISO dates") from exc
        if start > end:
            raise ValueError(f"{name}: start is after end")
    return deepcopy(config)


def load_config(path=Path(__file__).with_name("duration_config.yaml")):
    with Path(path).open(encoding="utf-8") as stream:
        return validate_config(yaml.safe_load(stream))


def calculation_fingerprint(config):
    """Presentation date presets do not affect the analytical configuration."""
    analytical = {k: v for k, v in validate_config(config).items() if k != "historical_events"}
    return hashlib.sha256(json.dumps(analytical, sort_keys=True).encode()).hexdigest()
