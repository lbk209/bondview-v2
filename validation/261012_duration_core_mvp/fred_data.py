"""Public FRED observations, auditable raw caches, and source acceptance policy."""

import hashlib
import io
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

# FRED DGS30 notes: discontinued 2002-02-18; reintroduced 2006-02-09.
GAP_START = pd.Timestamp("2002-02-18")
GAP_END = pd.Timestamp("2006-02-08")
SERIES = ("DGS6MO", "DGS10", "DGS30")


def parse_fred_csv(payload, series_id):
    """Reject malformed extracts; retain explicitly missing observations."""
    frame = pd.read_csv(io.BytesIO(payload), na_values=["."], float_precision="round_trip")
    if frame.columns.tolist() not in (["observation_date", series_id], ["DATE", series_id]):
        raise ValueError(f"Unexpected FRED columns for {series_id}")
    frame.columns = ["date", "raw_yield_pct"]
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    frame["raw_yield_pct"] = pd.to_numeric(frame["raw_yield_pct"], errors="raise").astype(float)
    if (frame.empty or frame["date"].isna().any() or frame["date"].duplicated().any()
            or not frame["date"].is_monotonic_increasing
            or not frame["date"].eq(frame["date"].dt.normalize()).all()
            or not frame["raw_yield_pct"].notna().any()
            or np.isinf(frame["raw_yield_pct"]).any()):
        raise ValueError(f"Invalid FRED observations for {series_id}")
    return frame


def prepare_observations(raw, series_id):
    """Expose Raw Observations with accepted yields and explicit structural segments.

    Routine missing days remain unavailable and do not increment the accepted
    observation index. DGS30's documented discontinuation is always excluded,
    including numerical entries, and splits the history even if gap rows vanish.
    """
    frame = raw.copy(deep=True)
    frame["date"] = pd.to_datetime(frame["date"]).astype("datetime64[ns]")
    frame["series_id"] = series_id
    frame["yield_pct"] = frame["raw_yield_pct"]
    frame["segment"] = pd.Series(1, index=frame.index, dtype="Int64")
    frame["availability"] = np.where(frame["yield_pct"].notna(), "accepted", "missing")
    if series_id == "DGS30":
        gap = frame["date"].between(GAP_START, GAP_END)
        frame.loc[gap, "yield_pct"] = np.nan
        frame.loc[gap, "segment"] = pd.NA
        frame.loc[gap, "availability"] = "structural_gap"
        frame.loc[frame["date"] > GAP_END, "segment"] = 2
    frame["observation_index"] = pd.Series(pd.NA, index=frame.index, dtype="Int64")
    accepted = frame["availability"].eq("accepted")
    frame.loc[accepted, "observation_index"] = frame.loc[accepted].groupby("segment", sort=False).cumcount()
    return frame


def acquire_fred(cache_dir, refresh=False):
    """Return accepted observations for all tenors plus raw snapshot provenance.

    Each cache has its original FRED CSV and a hash-checked JSON sidecar. Invalid
    caches are downloaded again. A failed explicit refresh raises, preserving
    the previous cache rather than silently substituting stale observations.
    """
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    observations, provenance = [], {}
    for series_id in SERIES:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode(
            {"id": series_id, "cosd": "1900-01-01"})
        csv_path = cache_dir / f"{series_id}.csv"
        meta_path = cache_dir / f"{series_id}.json"
        raw = None
        if not refresh and csv_path.exists() and meta_path.exists():
            try:
                payload = csv_path.read_bytes()
                metadata = json.loads(meta_path.read_text())
                raw = parse_fred_csv(payload, series_id)
                if (metadata["series_id"] != series_id or metadata["units"] != "percent"
                        or metadata["sha256"] != hashlib.sha256(payload).hexdigest()
                        or metadata["url"] != url
                        or metadata["source_start"] != str(raw["date"].min().date())
                        or metadata["source_end"] != str(raw["date"].max().date())):
                    raise ValueError("Cache provenance mismatch")
                datetime.fromisoformat(metadata["retrieved_at_utc"])
            except (OSError, ValueError, KeyError, TypeError) as exc:
                warnings.warn(f"Invalid {series_id} cache; downloading again: {exc}", stacklevel=2)
                raw = None
        if raw is None:
            try:
                request = Request(url, headers={"User-Agent": "Bondview-Duration-MVP/1.0"})
                with urlopen(request, timeout=60) as response:
                    payload = response.read()
                raw = parse_fred_csv(payload, series_id)
            except (OSError, ValueError) as exc:
                raise RuntimeError(f"FRED retrieval failed for {series_id}; no fresh result. "
                                   "A valid prior cache, if present, is preserved; "
                                   "set refresh=False explicitly to reuse it.") from exc
            metadata = {
                "series_id": series_id, "url": url, "units": "percent",
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "source_start": str(raw["date"].min().date()),
                "source_end": str(raw["date"].max().date()),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
            # A mismatched pair after interruption is detected on the next read.
            csv_path.with_suffix(".csv.tmp").write_bytes(payload)
            meta_path.with_suffix(".json.tmp").write_text(json.dumps(metadata, indent=2) + "\n")
            csv_path.with_suffix(".csv.tmp").replace(csv_path)
            meta_path.with_suffix(".json.tmp").replace(meta_path)
        accepted = prepare_observations(raw, series_id)
        valid = accepted.loc[accepted["availability"].eq("accepted"), "date"]
        provenance[series_id] = {
            **metadata, "accepted_start": str(valid.min().date()),
            "accepted_end": str(valid.max().date()), "accepted_observations": len(valid),
        }
        observations.append(accepted)
    return pd.concat(observations, ignore_index=True), {
        "series": provenance,
        "acceptance_policy": "Routine missing observations skipped, never filled; "
                             "DGS30 2002-02-18 through 2006-02-08 excluded; "
                             "lookbacks and state reset per structural segment.",
    }
