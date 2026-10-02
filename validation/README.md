# Bondview validation artifacts

`validation/` holds empirical and historical evidence, diagnostics, executable scripts, results, and reports used to validate Bondview design decisions. It is a project directory, not a Codex-specific directory.

- `docs/` → authoritative / accepted design documentation, subject to the repository's designated design authorities.
- `validation/` → validation evidence, diagnostics, scripts, results, and reports.

Validation artifacts do not become design authority merely because they are committed. Recommendations require explicit acceptance into the applicable design documentation.

Organize validation efforts into dated work-package directories named `YYMMDD_<short-work-package-name>`, with task subdirectories where needed. The date identifies when the work package began.

## Duration validation

[`261002_duration/task1_core/`](261002_duration/task1_core/) contains the completed Task-1 Core Duration validation for the Duration validation effort beginning on 2026-10-02:

- [`analysis.py`](261002_duration/task1_core/analysis.py): reproducible analysis script.
- [`results.csv`](261002_duration/task1_core/results.csv): committed observation-level results and source snapshot.
- [`report.md`](261002_duration/task1_core/report.md): analysis, conclusions, limitations, and offline replay commands.
