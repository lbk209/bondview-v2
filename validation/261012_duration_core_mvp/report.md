# Duration Core MVP implementation report

Date: 2026-10-12 (Asia/Seoul). Baseline: `main` at `b67d1e0`.

## Implementation and boundaries

Implemented a provisional historical Duration Core research workflow under this
directory. It calculates all three exposure histories, persists their completed
results, and presents one interactive Plotly chart from the saved snapshot.
Authoritative design documents and production analytical modules are unchanged.

| File | Responsibility |
|---|---|
| `duration_mvp.ipynb` | Explicit acquisition → Components → Core → save → independent load → controls workflow |
| `duration_config.yaml` | Accepted defaults, configurable experimental parameters, complete Rule Table, event dates |
| `duration_config.py` | MVP-local validation and analytical configuration fingerprint |
| `fred_data.py` | Public FRED retrieval, hash-checked raw caches, source acceptance and structural segments |
| `duration_components.py` | M5 Features, endpoint-change Component Values, plain and Hybrid Trend States |
| `duration_core.py` | Exposure/tenor selection and Core Rule Mapping from completed Components |
| `duration_results.py` | Consolidated CSV/JSON save/load, integrity and result-contract validation |
| `duration_plot.py` | One dual-axis Plotly chart, exposure/period controls, retained custom dates |
| `test_duration_core.py` | Synthetic calculation, persistence, cache, configuration, and UI contract tests |
| `verify_notebook.py` | Fresh full-notebook and separate visualization-only kernel execution checks |
| `README.md` | Environment, notebook, cache, saved-only visualization, regeneration, and verification instructions |
| `output/duration_core.csv` | All three source histories, intermediate lineage, Core judgments, and unavailable rows |
| `output/duration_core_metadata.json` | Raw source provenance, calculation configuration, coverage, generation time, checksum |
| `output/execution_validation.json` | Concise notebook execution evidence |
| `.gitignore` | Keep original raw `cache/` files local |

Repository-level changes are limited to declaring Plotly directly in
`pyproject.toml` and updating `poetry.lock`. Plotly was already in the lock as a
transitive dependency; the direct declaration locks 6.9.0. Existing Jupyter,
ipywidgets, pandas, NumPy, and YAML dependencies are reused.

## Fresh source snapshot and analytical results

The implementation retrieved its own histories from FRED's public
`https://fred.stlouisfed.org/graph/fredgraph.csv` endpoint, requesting coverage from
1900-01-01 with no end cutoff or API key. Source hashes, URLs, actual retrieval
times, and units are preserved in the saved JSON. No earlier repository CSV,
Component result, or notebook output was used as an analytical input.

| Exposure | Source start | Latest source observation | Source rows | Completed Core judgments |
|---|---|---|---:|---:|
| Short / 6M | 1981-09-01 | 2026-10-08 | 11,768 | 11,146 |
| Intermediate / 10Y | 1962-01-02 | 2026-10-08 | 16,898 | 16,048 |
| Long / 30Y | 1977-02-15 | 2026-10-08 | 12,953 | 11,154 |

Total: 41,619 source rows and 38,348 completed Core judgments. All nine Rule Cases
occur in each exposure's history. Default Custom dates are 1982-03-16 through
2026-10-08. All earlier exposure-specific observations remain saved and loadable.

The [FRED DGS30 notes](https://fred.stlouisfed.org/series/DGS30) document the
discontinuation on 2002-02-18 and reintroduction on 2006-02-09. The fresh extract
contained 994 numeric entries in the excluded interval; all were preserved as raw
values but rejected as accepted yields. No calculation bridges this interval.
After reintroduction, the first completed Long Core judgment is 2006-08-16,
following the required smoothing and lookback warmup.

## Material implementation decisions

1. **Source acceptance owns structural segmentation.** DGS30's known source
   discontinuation is source-specific policy in acquisition/preparation, rather
   than a configurable economic threshold. Raw values and accepted yields remain
   separate. Every downstream stage receives the accepted segment identity.
   This preserves the architectural acquisition/Bond Analysis boundary.
2. **Routine missing observations are unavailable, without resetting State.**
   They neither increment nor reset directional confirmation. Calculations use
   the sequence of accepted observations within a structural segment, as required
   by Section 3.3. No yield or Component is assigned to a missing source date.
   Structural boundaries reset smoothing, lookbacks, State, and pending entries.
3. **A directional exit is not an entry from an already Stable State.** With
   direct reversal disabled experimentally, an opposite threshold crossing first
   exits the established direction; persistence starts on the next accepted
   observation. With accepted defaults, a direct opposite crossing wins before
   exit logic and clears pending confirmation. These choices follow Section 3.3's
   ordered rules and its “already Stable” condition.
4. **Numerical precision at strict thresholds.** Endpoint-change values are
   rounded to ten decimal places in basis points, removing floating-point dust
   that could otherwise turn mathematically exact +25 or +10 into strict entry
   crossings. This is a numerical convention, not an intentional economic-rule
   deviation. Features retain their underlying floating-point values.
5. **Unavailable and warmup rows are retained.** Core availability distinguishes
   available, warmup, routine missing, and structural gaps. Scores are nullable
   integers; unavailable scores are never replaced with neutral zero. M5,
   reference endpoint values/dates, and accepted observation indices support
   traceability without downstream analytical reconstruction.
   The endpoint Feature is named `smoothed_yield_bp`, so its name remains accurate
   when experimental smoothing lengths differ from five observations.
6. **A failed refresh is explicit.** Valid caches are reused only when refresh is
   disabled. Failed downloads preserve existing caches and raise; the caller must
   explicitly choose reuse. Cache/result pairs are hash checked to detect partial
   writes and corruption. This prevents stale data from being labeled fresh.
7. **Saved configuration is authoritative for snapshot inspection.** Loading can
   optionally require the current configuration's analytical fingerprint to match.
   Date presets are excluded from this fingerprint because they do not affect
   Components or Rule Mapping. The saved full configuration supplies visualization
   presets, so the visualization section runs independently after kernel restart.
8. **Shared dates define defaults only.** Custom defaults are the minimum and
   maximum exact dates with completed results shared by all exposures. The chart
   filters only the selected exposure and requested period. It never truncates
   the loaded histories to that intersection.
9. **Plotting preserves discontinuities explicitly.** Missing yields/scores break
   traces. A null separator is additionally inserted when segment identity changes,
   protecting extracts that omit structural-gap rows. The score trace uses `hv`
   steps and fixed integer categories −3 through +3. The JupyterLab-compatible
   interactive MIME renderer is selected explicitly; hover consumes saved fields.
10. **Validation remains MVP-local.** A small configuration-validation module
    avoids embedding validation in runtime Components or visualization. A UI class
    owns callback state and custom-date restoration; it imports no acquisition,
    Feature, Component, or Core mapping code. No permanent configuration framework,
    generalized engine, new project Module, or production Result Boundary is added.

Historical-event presets copy date windows from
`validation/261002_duration/task1_core/analysis.py` (`EVENTS`), including all six
requested episodes. Only date definitions were reused. Volcker's early Short
coverage is partially unavailable, and DGS30's structural interval is unavailable;
these conditions are handled by annotations and gaps.

## Verification

Commands run from the repository environment:

```bash
poetry add 'plotly>=6,<7'
poetry check
poetry run python -m py_compile validation/261012_duration_core_mvp/*.py
poetry run python -m unittest discover -s validation/261012_duration_core_mvp -p 'test_duration_core.py' -v
poetry run python validation/261012_duration_core_mvp/verify_notebook.py
git diff --check
```

- **Configuration/environment:** Poetry consistency and syntax checks passed for
  all eight Python files. The verifier uses the Poetry Python 3.12 Jupyter kernel
  and the notebook directory as its working directory; no Python path changes.
- **Focused tests:** all 33 passed. They cover fresh/reused/invalid caches,
  forced refresh and explicit failures, missing data, structural-gap boundaries,
  source parsing, configurable formulas, accepted-observation offsets, strict
  threshold equalities, initialization, persistence, neutral/opposing pending
  resets, both hysteresis exits, direct reversals and their priority, reversal
  behavior after exit, structural resets, and disabled stabilization. Synthetic
  reversals cover accepted semantics that historical observations need not exhibit.
- **Core/persistence:** all 27 accepted mappings passed against independently
  listed expected scores. Core selection/mapping leaves upstream Components
  unchanged. CSV/JSON round trips preserve dates, floating-point values, States,
  and nullable integer scores exactly. Config mismatches, checksum corruption,
  incomplete exposure sets, and invalid ordinal scores are rejected.
- **Visualization contracts:** tests verify the exposure/tenor title, two axes,
  integer score categories, zero reference, step shape, hover values from saved
  rows, exact shared-date defaults, retained exposure-specific history, custom
  date restoration, disabled event date controls, unavailable/reversed/partial
  periods, and separators when structural-gap rows are absent.
- **Full live notebook:** all seven code cells executed with fresh FRED retrieval.
  The final saved snapshot was generated at 2026-10-12T03:40:49.702689+00:00.
  The verifier confirmed one interactive Plotly MIME output, including output
  captured by the widget, and rejected any captured errors.
- **Independent visualization:** a completely new kernel executed only the
  visualization cells and additional control checks. A meta-path import guard
  rejected acquisition, Component, and Core mapping modules. All three exposures
  and all nine historical presets were exercised from saved results, including a
  wholly unavailable DGS30 gap window. One interactive chart output was confirmed;
  no upstream import occurred.

The repeatable verifier records these notebook checks in
`output/execution_validation.json`. The source notebook is intentionally saved
without execution outputs; large chart payloads remain in memory during
verification. Early implementation checks caught nullable plotting conversion
and pandas datetime-resolution issues; both were corrected before the final
passing checks. No requested automated or network-dependent check remains unrun.
Browser appearance was not manually inspected: chart data/contracts, interactive
MIME output, widget callbacks, and kernel isolation were verified headlessly.

## Behavior impact and limitations

The new YAML defaults and calculations reproduce the accepted Duration Core
definition without intentional deviations. The workflow creates new research
outputs; existing production model outputs, public APIs, and configuration
interpretation are unchanged. Editing analytical YAML parameters or Rule Table
scores intentionally creates experimental results on the next explicit
calculation/save; changing chart controls does not change model outputs.

These are current FRED histories and may be revised, not historical real-time
vintages. Source retrieval times/hashes identify the snapshot; no future data
revision is silently treated as the same snapshot. Ordinary missing source dates
are distinct from the documented structural discontinuation. No speculative
calendar-gap threshold was introduced to redefine accepted observation segments.

No Macro Adjustment, completed Constituent Evaluation, ETF data/selection,
Evaluation Combination, Positioning Overlay, or return backtesting is implemented.
No accepted economic rule or architectural boundary required revision.
