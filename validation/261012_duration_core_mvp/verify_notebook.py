"""Execute fresh acquisition and visualization-only isolation in separate kernels.

Run from the repository environment: poetry run python <path>/verify_notebook.py.
Only a concise execution record is persisted; large chart outputs stay in memory.
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import nbformat
from nbclient import NotebookClient


def inspect_notebook_outputs(notebook):
    """Include widget-captured outputs and reject errors suppressed by Output UI."""
    outputs = [out for cell in notebook.cells for out in cell.get('outputs', [])]
    widget_state = notebook.metadata.get('widgets', {}).get('application/vnd.jupyter.widget-state+json', {}).get('state', {})
    outputs += [out for widget in widget_state.values() for out in widget.get('state', {}).get('outputs', [])]
    errors = [out for out in outputs if out.get('output_type') == 'error']
    assert not errors, [(out.get('ename'), out.get('evalue')) for out in errors]
    return outputs


base = Path(__file__).resolve().parent
source = nbformat.read(base / 'duration_mvp.ipynb', as_version=4)
for cell in source.cells:
    if cell.cell_type == 'code':
        cell.source = cell.source.replace('REFRESH_FRED = False', 'REFRESH_FRED = True')
print('Executing complete notebook with REFRESH_FRED=True', flush=True)
executed = NotebookClient(source, on_cell_start=lambda cell, cell_index: print(f'Full notebook cell {cell_index}', flush=True), timeout=180, kernel_name='python3', resources={'metadata': {'path': str(base)}}).execute()
for cell in executed.cells:
    for output in cell.get('outputs', []):
        if output.output_type == 'stream':
            print(output.text.rstrip(), flush=True)
outputs = inspect_notebook_outputs(executed)
plots = sum('application/vnd.plotly.v1+json' in out.get('data', {}) for out in outputs)
print('Captured MIME outputs:', [list(out.get('data', {})) for out in outputs], flush=True)
assert plots == 1, f'Expected one primary Plotly output, got {plots}'

# A completely new kernel has no upstream imports/state. Any accidental runtime
# acquisition, calculation, or Core mapping import fails before it can execute.
visualization = nbformat.v4.new_notebook(metadata=source.metadata)
visualization.cells = [nbformat.v4.new_code_cell('''import sys
from importlib.abc import MetaPathFinder
class BlockUpstream(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in {"fred_data", "duration_components", "duration_core"}:
            raise AssertionError(f"Visualization attempted upstream import: {fullname}")
sys.meta_path.insert(0, BlockUpstream())''')]
visualization.cells += [cell for cell in source.cells if 'visualization' in cell.metadata.get('tags', [])]
visualization.cells += [nbformat.v4.new_code_cell('''from unittest.mock import patch
from datetime import date
with patch.object(controls, "render"):
    for exposure in saved_metadata["configuration"]["exposures"]:
        controls.exposure.value = exposure
        figure = controls.figure()
        assert exposure in figure.layout.title.text
        for event in saved_metadata["configuration"]["historical_events"]:
            controls.period.value = event
            figure = controls.figure()
    controls.period.value = "Custom period"
    controls.start.value, controls.end.value = date(2002, 2, 18), date(2006, 2, 8)
    controls.exposure.value = "Long"
    gap_figure = controls.figure()
    assert len(gap_figure.layout.annotations) > 0
assert not {"fred_data", "duration_components", "duration_core"} & set(sys.modules)
print("Visualization-only fresh kernel and all exposure/event controls passed; upstream imports blocked.")''')]
print('Executing visualization-only notebook in a fresh kernel', flush=True)
visual = NotebookClient(visualization, timeout=180, kernel_name='python3', resources={'metadata': {'path': str(base)}}).execute()
visual_outputs = inspect_notebook_outputs(visual)
visual_plots = sum('application/vnd.plotly.v1+json' in out.get('data', {}) for out in visual_outputs)
assert visual_plots == 1, f'Expected one saved-only Plotly output, got {visual_plots}'
for cell in visual.cells:
    for output in cell.get('outputs', []):
        if output.output_type == 'stream':
            print(output.text.rstrip(), flush=True)
summary = {
    'verified_at_utc': datetime.now(timezone.utc).isoformat(),
    'full_notebook': {'passed': True, 'forced_fresh_fred': True, 'code_cells_executed': sum(c.cell_type == 'code' for c in source.cells), 'primary_plotly_outputs': plots},
    'visualization_only': {'passed': True, 'fresh_kernel': True, 'primary_plotly_outputs': visual_plots, 'upstream_imports_blocked': ['fred_data', 'duration_components', 'duration_core'], 'all_exposure_event_combinations': True, 'dgs30_gap_window': True},
    'execution': 'Poetry Python 3.12, nbclient NotebookClient, notebook directory as kernel working directory; no Python path changes',
}
(base / 'output' / 'execution_validation.json').write_text(json.dumps(summary, indent=2) + '\n')
print('Both notebook executions passed; evidence saved.', flush=True)
