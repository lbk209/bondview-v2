# Duration Stage 1 MVP implementation review

## Scope and outcome

Implemented the Stage 1 contract in `docs/bondview_duration_vertical_slice_mvp.md`.
All six original candidate dates execute with actual FRED historical vintages;
none was shifted. The notebook exposes Raw Observations, Feature endpoints,
Component Values / States, and Duration Bond Exposure Views as separate results.
No Stage 2 or ETF-specific calculation was added. Architecture and vocabulary
sources are unchanged.

This separate report preserves the provisional economic choices, historical
results, behavior validation, and review questions needed before Stage 2.
Execution and descriptive regime variation are demonstrated; economic usefulness
beyond yield momentum has not been established.

## Files

- `duration_mvp.ipynb`: executed orchestration, notebook-local retrieval/cache,
  raw coverage/provenance, all calculation boundaries, backward lineage inspection,
  historical comparison and diagnostic threshold sensitivity.
- `duration_model.py`: config validation, Feature Calculation, Component Value
  calculation / State Classification, and separate View calculation.
- `duration_mvp.yaml`: provisional series, dates, horizons, thresholds, states,
  and complete per-state View contribution mapping.
- `test_duration_model.py`: six focused synthetic contract tests.
- `pyproject.toml`, `poetry.lock`: declare already-locked PyYAML as a direct
  dependency; no dependency versions changed.
- This report: durable review record.

## Sources, availability, and reproducibility

The notebook downloads CSV data directly from FRED's ALFRED archive, without
credentials, using one request per series and candidate `as_of` (18 requests).
The download starts at 2017-01-01, enough for all windows including CPI's
12-month denominator and three-month comparison. Every response's dated column
must match the requested vintage. No latest-data fallback is allowed.

The availability contract is end-of-day ALFRED vintage availability, not an
intraday execution time. As-of slicing additionally excludes future observation
dates. Missing market holidays are not forward-filled. Monthly gaps, daily
policy gaps, excessive market gaps, stale series and insufficient history fail.
ALFRED can lag source publication; for example DGS10's last observation in the
2024-09-30 vintage is 2024-09-27. CPI's last observation for that vintage is
2024-08-01 (the August reference month), not September CPI.

Source observations are normalized into date-indexed pandas Series. The notebook
preserves the CSV URL, FRED series ID, source, units, vintage date, UTC retrieval
time and SHA-256. Original CSVs and manifests are automatically cached under
ignored `_private/duration_mvp/`; users need not prepare files. Cache reads verify
URL and content hash. Set `refresh=True` on the download call or remove that cache
to fetch again. Source archive corrections can change future downloads; hashes
and committed notebook provenance make such changes detectable. The cache is
local, not a committed data distribution. New environments need internet access.

Sources:
- [ALFRED availability and vintage semantics](https://alfred.stlouisfed.org/help)
- [DGS10](https://fred.stlouisfed.org/series/DGS10): 10Y constant-maturity Treasury
  yield, a provisional long-end proxy. DGS30 could materially change ultra-long
  interpretation.
- [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL): seasonally adjusted
  headline CPI, representing broad consumer inflation. Vintage selection avoids
  subsequently revised seasonal history. Core CPI or PCE could change the signal.
- [DFEDTARU](https://fred.stlouisfed.org/series/DFEDTARU): upper policy target,
  measuring implemented changes. Futures or 2Y yields could detect expected
  transitions earlier but would change the Component's meaning.

All three series choices are provisional MVP assumptions, not project-level
analytical definitions.

## Provisional formulas and behavior

Yield Features are five-valid-observation average endpoints, compared 63 and
21 valid business observations apart. Inflation Features are CPI year-over-year
rates compared three monthly observations apart. Policy Features are target
levels compared 90 daily observations apart. Component Values are current minus
base, scaled to bp for yield/policy and percentage points for inflation.

Component neutral bands include their boundaries: ±25 bp for Long-End Yield
Trend, ±15 bp for Recent Long-End Yield Move, ±0.25 pp for Inflation Trend,
±12.5 bp for Policy Direction. Outside the bands, signs determine directional
States. Actual dates of endpoint windows and CPI denominator windows are retained.

The View maps falling/cooling/easing to +1, rising/heating/tightening to -1,
and neutral States to zero. Tally >=2 is `duration_supportive`, <=-2 is
`duration_headwind`, otherwise `mixed`. This defines all 81 State cases. The tally
is an explanatory View mapping, not a new Component or an ETF evaluation score.

The YAML intentionally creates new Stage 1 model outputs. Its series, horizons,
thresholds and mappings affect those outputs. Existing prototype outputs and
public interfaces are unchanged. No permanent API or generalized framework is
introduced.

## Historical results

Values below are changes; yield/policy units are bp, inflation units are pp.

| as_of | Long-End Yield Trend | Recent Long-End Yield Move | Inflation Trend | Policy Direction | Tally | Duration Bond Exposure View |
|---|---|---|---|---|---:|---|
| 2019-08-30 | -73.40 / falling | -55.60 / falling | -0.19 / stable | -25.00 / easing | 3 | duration_supportive |
| 2020-03-31 | -111.20 / falling | -50.00 / falling | +0.28 / heating | -150.00 / easing | 2 | duration_supportive |
| 2021-12-30 | +9.40 / stable | -9.20 / stable | +1.68 / heating | 0.00 / unchanged | -1 | mixed |
| 2022-10-31 | +132.40 / rising | +28.20 / rising | -0.77 / cooling | +75.00 / tightening | -2 | duration_headwind |
| 2023-10-31 | +93.00 / rising | +32.20 / rising | +0.60 / heating | 0.00 / unchanged | -3 | duration_headwind |
| 2024-09-30 | -52.60 / falling | -6.80 / stable | -0.66 / cooling | -50.00 / easing | 3 | duration_supportive |

- 2019: both yield horizons and policy support the easing interpretation.
- 2020: strong yield falls and aggressive easing outweigh the lagged inflation
  signal. The available CPI reference month is February, so the heating State
  does not imply observation of March inflation during the shock.
- 2021: rising inflation meets neutral rates-side and realized-policy States.
  The resulting mixed View highlights the absence of anticipatory policy data.
- 2022: rising yields and tightening dominate cooling inflation. Cooling is a
  decline in YoY inflation, not a claim that inflation was low.
- 2023: rising yield momentum and renewed inflation acceleration produce a
  headwind even with unchanged recent policy targets.
- 2024: medium-horizon falling yields, cooling inflation and policy easing
  produce support despite a neutral recent yield move.

All six Views remain unchanged when every Component threshold is multiplied by
0.8 or 1.2. Some Component States can change without crossing a View boundary.
This narrow sensitivity check does not establish robustness to different series,
horizons, smoothing, or View weights.

## Validation

Run from the repository root with the Poetry environment:

```bash
poetry run python -m py_compile duration_model.py test_duration_model.py
poetry run python -m unittest -v test_duration_model
poetry check
git diff --check
poetry run python - <<'PY'
import nbformat
from nbclient import NotebookClient
first = nbformat.read('duration_mvp.ipynb', as_version=4)
second = nbformat.read('duration_mvp.ipynb', as_version=4)
NotebookClient(second, timeout=180, kernel_name='python3').execute()
for before, after in zip(first.cells, second.cells):
    if before.cell_type == 'code':
        assert before.outputs == after.outputs
nbformat.validate(second)
PY
```

Results on 2026-09-23:

- Python syntax checks passed for both new Python files.
- All six tests passed: independent formula/lineage expectations, future-date
  exclusion and input immutability, mismatched vintage rejection, missing/stale/
  short/nonfinite data rejection, inclusive State thresholds, all 81 View cases,
  mixed-date rejection, and invalid configuration checks.
- First full notebook execution downloaded all 18 real historical series
  vintages and produced every Feature, Component and View.
- Second full notebook execution used the verified cache and produced exactly
  identical outputs in every code cell, including provenance and diagnostics.
- Notebook format validation, Poetry consistency and whitespace checks passed.
- The initial immutability test compared a pre-append synthetic index frequency
  against an index modified by the test itself; the fixture snapshot was corrected
  to compare the full input immediately before/after calculation. All final checks
  passed. This was a test-fixture issue, not a model-output change.

The bare system Python lacks pandas; use `poetry run`. The default tool sandbox
failed to start (`mountinfo path is not absolute`); authorized commands ran outside
that malfunctioning sandbox. This did not prevent FRED access or full execution.

## Before Stage 2

Economic review is still required. The four equal State contributions give two
correlated yield Components half of the possible vote; momentum may dominate.
Inflation acceleration differs from inflation level, and implemented policy
changes omit forward guidance. Falling yields after a shock do not establish
attractive valuation, future returns, or implementation liquidity. Thresholds and
horizons have not been calibrated and should not be judged solely on six selected
dates. These are limitations of the provisional interpretation, not architectural
issues requiring changes to the standing design.

Stage 2 remains deferred. If approved later, its ETF-specific Duration Evaluation
must consume Components directly and must not consume the Stage 1 View.
