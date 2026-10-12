# Duration Core research MVP

This provisional workflow inspects the accepted Duration Core definition in
`docs/bondview_exposure_evaluation_design.md`, Section 3. It evaluates synthetic
Short / 6M, Intermediate / 10Y, and Long / 30Y exposures. Scores are seven-level
ordinal judgments, not expected returns, ETF rankings, or completed Duration
Evaluation Results. Defaults reproduce the accepted 2026-10-10 Core definition.

## Run the notebook

From the repository root, install the locked environment if necessary:

```bash
poetry install --no-root
cd validation/261012_duration_core_mvp
poetry run jupyter lab duration_mvp.ipynb
```

Use the Poetry environment's Python kernel. Jupyter starts this notebook's kernel
in its directory, where the local modules and YAML live; no Python path edits or
API key are needed. Run all calculation cells before the visualization cells.
The notebook explicitly exposes Raw Observations (`observations`), Features and
Components (`components`), all Core histories (`core_results`), and the loaded
saved snapshot (`loaded_results`).

## Acquire, calculate, and save

`REFRESH_FRED = False` reuses each valid local cache. Missing or invalid caches are
downloaded directly from FRED's public full-history CSV endpoint. Set
`REFRESH_FRED = True` and rerun the calculation section to replace the raw caches
with fresh observations. A failed retrieval raises an error; a failed refresh
preserves the old cache but requires explicitly setting refresh to False to reuse
it. No stale fallback is disguised as a fresh download.

The calculation cells then calculate Components for all three tenors, apply the
configured exposure-specific Rule Table, and save all three histories to:

- `output/duration_core.csv`: yields, M5 Features and reference endpoints,
  Component Values and States, Rule Cases, scores, and availability/segment lineage.
- `output/duration_core_metadata.json`: source snapshot hashes and coverage,
  retrieval times, units, complete configuration and presets, calculation
  fingerprint, generation time, result coverage, and CSV checksum.

The untracked `cache/` directory contains original per-series FRED CSVs and their
provenance sidecars. Calculated results are separate and committed for immediate
saved-snapshot inspection. Regenerating replaces the consolidated CSV/JSON pair;
checksum validation catches an interrupted or inconsistent pair.

FRED percent yields are converted to basis points for calculation. M5 smoothing
and 126/21 lookbacks use accepted valid observation indices within a structural
segment. Missing days are preserved as unavailable rows and never forward-filled.
DGS30 observations from 2002-02-18 through 2006-02-08 are excluded even when
numerical source entries exist. Both Features and Trend classification restart
after that discontinuation. Component warmup requires a full smoothing window
and the applicable observation offset.

## Visualization from saved results only

Restart the kernel and run only the **Visualization** section. It imports the
result loader and plotting module and reads the saved CSV/JSON; it does not read
raw caches, download FRED data, or calculate Components or Core mappings.

Intermediate / 10Y is the default exposure. Custom period initially uses the
first and last dates with completed results shared across all three exposures.
Earlier exposure-specific history remains in the loaded data; extend Custom
dates to view it. Historical presets use their saved dates in disabled controls.
Returning to Custom restores the previous manually entered dates. Empty windows,
warmup, and unavailable periods display a chart annotation; reversed or missing
custom dates display a short instruction. Changing controls only filters saved
results. Hover values also come directly from the saved results.

## Change model parameters explicitly

Edit `duration_config.yaml`, then rerun the entire calculation/save section.
Non-default parameters or Rule Tables are experimental variants. Turning off
Trend stabilization preserves Trend Values and uses plain threshold States.
Recent Move always uses plain classification. No controls change model settings.

Visualization intentionally loads the configuration of the saved snapshot.
To detect a mismatch against the current YAML instead, use:

```python
from duration_config import load_config
from duration_results import load_results

loaded_results, metadata = load_results("output", expected_config=load_config())
```

Analytical changes raise a clear mismatch error. Historical-event dates are
presentation settings and do not affect the calculation fingerprint; saved
presets are used until a new save. Omitting `expected_config` explicitly inspects
the saved snapshot even if YAML has changed.

## Verify

From the repository root:

```bash
poetry check
poetry run python -m py_compile validation/261012_duration_core_mvp/*.py
poetry run python -m unittest discover -s validation/261012_duration_core_mvp -p 'test_duration_core.py' -v
```

For a complete headless notebook execution, from this directory:

```bash
poetry run jupyter nbconvert --to notebook --execute duration_mvp.ipynb --output /tmp/duration_core_executed.ipynb --ExecutePreprocessor.timeout=180
```

Set `REFRESH_FRED = True` before execution when fresh retrieval is required.
For a headless visualization-only run in a new kernel:

```bash
poetry run python - <<'PY'
from pathlib import Path
import nbformat
from nbclient import NotebookClient

notebook = nbformat.read('duration_mvp.ipynb', as_version=4)
notebook.cells = [cell for cell in notebook.cells
                  if 'visualization' in cell.metadata.get('tags', [])]
NotebookClient(notebook, timeout=180, kernel_name='python3',
               resources={'metadata': {'path': str(Path.cwd())}}).execute()
print('Visualization-only execution passed.')
PY
```

Tests use explicitly synthetic fixtures and mocked downloads; they never use
previous validation outputs. Actual fresh retrieval and two independent notebook
executions are recorded in `report.md` and `output/execution_validation.json`.

To repeat the recorded fresh retrieval and both kernel executions, including
blocked upstream imports during visualization and checking widget-captured chart
outputs for errors, run from the repository root:

```bash
poetry run python validation/261012_duration_core_mvp/verify_notebook.py
```

This command explicitly refreshes FRED observations and overwrites the completed
CSV/JSON snapshot and concise execution record. The source notebook keeps its
cache-reuse default.
