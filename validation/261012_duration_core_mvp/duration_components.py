"""Tenor-local Features, Component Values, and States, independent of exposure."""

import numpy as np
import pandas as pd


def classify_plain(values, threshold_bp):
    """Threshold equality is Stable; missing values have no State."""
    states = pd.Series(pd.NA, index=values.index, dtype="string")
    states.loc[values.notna()] = "Stable"
    states.loc[values > threshold_bp] = "Rising"
    states.loc[values < -threshold_bp] = "Falling"
    return states


def classify_trend(values, parameters):
    """Hybrid persistence/hysteresis within one accepted structural segment.

    The first calculable value initializes plainly. Missing observations neither
    increment nor reset pending entry; callers start a fresh classifier per segment.
    A directional exit does not count as an already-Stable entry observation.
    """
    plain = classify_plain(values, parameters["entry_threshold_bp"])
    if not parameters["stabilization_enabled"]:
        return plain
    states = pd.Series(pd.NA, index=values.index, dtype="string")
    state, pending, count = None, None, 0
    entry = parameters["entry_threshold_bp"]
    exit_threshold = entry - parameters["hysteresis_bp"]
    for index, value in values.items():
        if pd.isna(value):
            continue
        candidate = plain.loc[index]
        if state is None:
            state = candidate
        elif state != "Stable":
            opposite = "Falling" if state == "Rising" else "Rising"
            if parameters["direct_reversal"] and candidate == opposite:
                state = opposite
            elif ((state == "Rising" and value <= exit_threshold)
                  or (state == "Falling" and value >= -exit_threshold)):
                state = "Stable"
            pending, count = None, 0
        elif candidate == "Stable":
            pending, count = None, 0
        else:
            count = count + 1 if pending == candidate else 1
            pending = candidate
            if count >= parameters["persistence"]:
                state = candidate
                pending, count = None, 0
        states.loc[index] = state
    return states


def calculate_components(observations, trend, recent_move):
    """Return explicit Raw Observation lineage, M5 Features, Values, and States.

    Parameters contain no downstream exposure identity or Rule Mapping. Rolling
    means and shifts operate only on accepted observations within each segment.
    Invalid source rows are preserved with unavailable Features/Components.
    """
    frame = observations.copy(deep=True)
    for column in ("smoothed_yield_bp", "trend_reference_bp", "recent_reference_bp",
                   "trend_value_bp", "recent_move_value_bp"):
        frame[column] = np.nan
    for column in ("trend_reference_date", "recent_reference_date"):
        frame[column] = pd.NaT
    for column in ("trend_state", "recent_move_state"):
        frame[column] = pd.Series(pd.NA, index=frame.index, dtype="string")
    for _, group in frame.loc[frame["availability"].eq("accepted")].groupby(
            ["series_id", "segment"], sort=False):
        if not group["date"].is_monotonic_increasing or group["date"].duplicated().any():
            raise ValueError("Accepted observations must be ordered and unique per segment")
        endpoints = (group["yield_pct"] * 100).rolling(
            trend["smoothing_observations"], min_periods=trend["smoothing_observations"]).mean()
        trend_reference = endpoints.shift(trend["lookback_observations"])
        recent_reference = endpoints.shift(recent_move["lookback_observations"])
        # Remove binary floating-point dust at the strict bp thresholds.
        trend_values = (endpoints - trend_reference).round(10)
        recent_values = (endpoints - recent_reference).round(10)
        frame.loc[group.index, "smoothed_yield_bp"] = endpoints
        frame.loc[group.index, "trend_reference_bp"] = trend_reference
        frame.loc[group.index, "recent_reference_bp"] = recent_reference
        frame.loc[group.index, "trend_reference_date"] = group["date"].shift(trend["lookback_observations"])
        frame.loc[group.index, "recent_reference_date"] = group["date"].shift(recent_move["lookback_observations"])
        frame.loc[group.index, "trend_value_bp"] = trend_values
        frame.loc[group.index, "recent_move_value_bp"] = recent_values
        frame.loc[group.index, "trend_state"] = classify_trend(trend_values, trend)
        frame.loc[group.index, "recent_move_state"] = classify_plain(recent_values, recent_move["threshold_bp"])
    return frame
