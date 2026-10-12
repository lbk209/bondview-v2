"""Exposure-specific Core Rule Mapping, consuming completed Components."""

import pandas as pd


def evaluate_core(components, exposures, rules):
    """Produce all synthetic exposure histories without recalculating Components."""
    histories = []
    for exposure, identity in exposures.items():
        frame = components.loc[components["series_id"].eq(identity["series_id"])].copy(deep=True)
        if frame.empty:
            raise ValueError(f"Missing Components for {identity['series_id']}")
        frame["representative_tenor"] = identity["representative_tenor"]
        frame["duration_exposure"] = exposure
        frame["rule_case"] = frame["trend_state"] + " × " + frame["recent_move_state"]
        mapping = {case: scores[exposure] for case, scores in rules.items()}
        if not frame.loc[frame["rule_case"].notna(), "rule_case"].isin(mapping).all():
            raise ValueError("Unmapped Core Rule Case")
        frame["core_score"] = frame["rule_case"].map(mapping).astype("Int64")
        frame["core_availability"] = frame["availability"]
        frame.loc[frame["availability"].eq("accepted") & frame["core_score"].isna(),
                  "core_availability"] = "warmup"
        frame.loc[frame["core_score"].notna(), "core_availability"] = "available"
        histories.append(frame)
    return pd.concat(histories, ignore_index=True)
