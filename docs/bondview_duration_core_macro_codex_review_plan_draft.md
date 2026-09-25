# Bondview Duration Core/Macro Review — Codex Work Plan (Draft)

## 1. Purpose

This document defines a temporary Codex work plan for reviewing the current Duration design before any further MVP redesign.

This is **not an MVP specification** and does not define a production implementation. Its purpose is to use the existing Duration prototype and current architecture to test one specific design question:

> How should an existing market-condition Rule Mapping become an exposure-specific Core Duration Evaluation Result, and how does the existing Macro Adjustment logic behave after that exposure-specific Core result has been produced?

The review is intended to make the missing relationship between:

```text
market Components
        ↓
market Rule Mapping
        ↓
Duration Exposure
        ↓
Core Duration Evaluation Result
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

concrete enough to inspect before making further formal design changes.

The work should favor exhaustive, transparent case analysis over framework design.

---

## 2. Reference Basis

Use the current `main` branch of `lbk209/bondview-v2` as the reference basis.

Primary references:

- `docs/bondview_system_architecture.md`
- `docs/bondview_vocabulary.md`
- `docs/bondview_stance_design_draft.md`
- `bondview_duration_horizon_rulecase_prototype.ipynb`

The current architecture is authoritative for the ordering and semantic boundaries:

```text
Components for Core Evaluation
        ↓
[Core Evaluation] <──────────────── ETF Exposure Profile
        ↓
Core Evaluation Result
        ↓
[Macro Adjustment, where applicable] <── Macroeconomic Components
        ↓
Constituent Evaluation Result
```

The current prototype notebook may be reused for the existing Duration market calculations.

---

## 3. What This Review Is Testing

The existing prototype already produces the two Duration market Components and their Rule Case:

```text
Long-End Yield Trend
        ×
Recent Long-End Yield Move
        ↓
market Rule Case
        ↓
existing 3 × 3 Rule Mapping
        ↓
market-mapping result
```

The current review does **not** need to reconsider the upstream market calculation unless a concrete problem is discovered during analysis.

The main missing design step is:

```text
market-mapping result
        +
Duration Exposure
        ↓
Core Duration Evaluation Result
```

After that step is made explicit, the existing provisional macro-cap logic can be applied:

```text
Core Duration Evaluation Result
        +
Inflation Trend
        +
Policy Direction
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

The review therefore has two main analytical stages:

1. **Exposure application review**
   - determine whether the same market condition produces economically sensible differences across duration exposures;

2. **Macro interaction review**
   - determine whether the existing Macro Adjustment remains economically sensible after the Core result has become exposure-specific.

---

## 4. Scope

### Included

The review should use:

- the existing `Long-End Yield Trend` Component;
- the existing `Recent Long-End Yield Move` Component;
- the existing 3 × 3 market Rule Table;
- four synthetic Duration Exposure classes;
- a provisional exposure-application rule;
- the existing provisional Inflation Trend × Policy Direction macro-cap logic;
- exhaustive case generation for Core Evaluation and Macro Adjustment;
- replay of selected historical dates for economic interpretation;
- descriptive summaries of how the mappings behave.

### Excluded

Do not expand the work into:

- a new MVP;
- real ETF Profile construction;
- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation;
- Evaluation Combination;
- Positioning Overlay;
- Instrument Quality;
- ETF ranking;
- new market Raw Observations;
- new Treasury maturities merely for case enumeration;
- optimization or tuning against historical outcomes;
- generic evaluator frameworks;
- production configuration architecture.

The four duration exposures are synthetic analytical fixtures, not actual ETF definitions.

---

## 5. Existing Market Rule Table

The existing Duration market Rule Table should remain fixed for the initial review.

```text
Long-End Yield Trend
        ×
Recent Long-End Yield Move
        ↓
9 market Rule Cases
        ↓
existing market mapping
        ↓
-3 ... +3 market-mapping result
```

The current prototype should be reused where practical rather than recreating the upstream calculations.

The market-mapping result should **not** be treated as the final Core Duration Evaluation Result. It is an internal market-condition interpretation that still has to be combined with Duration Exposure.

---

## 6. Synthetic Duration Exposures

Use four deliberately simple exposure classes:

```text
short
intermediate
long
very_long
```

These are categorical test fixtures.

Do not initially label them as exact `2Y`, `5Y`, `7Y`, or `30Y` effective durations unless a separate numeric exposure definition is explicitly approved. Maturity labels and effective duration are not interchangeable.

The purpose of the four classes is to answer:

> Under the same market Rule Case, should different levels of duration exposure receive different Core Evaluation Results, and if so, how?

---

## 7. Decisions Required Before Codex Runs the Full Batch

Most existing model choices can remain fixed. The following decisions should be made explicitly before the full batch comparison.

### 7.1 Exposure application rule — required

This is the main new design decision.

Define how:

```text
market-mapping result
        +
exposure class
        ↓
Core Duration Evaluation Result
```

works.

Possible mechanical forms include:

- scaling;
- caps;
- exposure-specific lookup tables;
- profile-conditioned Rule Mapping;
- another simple deterministic transformation.

Codex should **not invent or optimize** this logic.

The chosen rule should be simple enough that every one of the 36 Core cases can be inspected directly.

### 7.2 Core Evaluation Result scale — required

Decide the representation of the Core result.

A simple initial option is to preserve the existing seven-level directional scale:

```text
-3, -2, -1, 0, +1, +2, +3
```

If another representation is used, its semantics must be explicit before the batch run.

### 7.3 Core Result metadata — recommended

Even if Macro Adjustment operates only on the Core score, retain enough diagnostic fields to reconstruct the result:

```text
market_rule_case
market_mapping_result
exposure_class
core_evaluation_result
```

This avoids losing the distinction between cases that happen to collapse to the same Core score.

### 7.4 Macro Adjustment logic — initially fixed

For this review, reuse the existing provisional macro-cap logic as a **fixed test fixture** rather than redesigning it.

Current provisional actions include:

```text
pass-through
cap negative at -1
cap negative at -2
cap positive at +2
cap positive at +1
```

The purpose is to test how this existing macro behavior interacts with exposure-specific Core results.

If the interaction proves economically problematic, that becomes a later design finding rather than a reason for Codex to modify the macro rules during the run.

---

## 8. Review Sequence

### A. Existing Market Mapping

Use the existing:

```text
3 Trend States
×
3 Recent Move States
=
9 market Rule Cases
```

and retain the current market-mapping result for each case.

No additional Raw Observation dimension should be added for this exercise.

### B. Exposure-Specific Core Evaluation

Cross the 9 market Rule Cases with the 4 synthetic exposure classes:

```text
9 market cases
×
4 exposure classes
=
36 Core Evaluation cases
```

For every case, calculate and preserve:

```text
trend_state
recent_move_state
market_rule_case
market_mapping_result
exposure_class
core_evaluation_result
```

#### Required primary output

Produce a compact 9 × 4 matrix:

| Market Rule Case | Short | Intermediate | Long | Very Long |
|---|---:|---:|---:|---:|
| Falling × Falling | | | | |
| Falling × Stable | | | | |
| Falling × Rising | | | | |
| Stable × Falling | | | | |
| Stable × Stable | | | | |
| Stable × Rising | | | | |
| Rising × Falling | | | | |
| Rising × Stable | | | | |
| Rising × Rising | | | | |

#### Questions for B

Inspect whether:

- exposure differentiation is economically interpretable;
- stronger duration exposure changes the Core result in the intended direction;
- adjacent exposure classes collapse too often;
- the exposure rule is too weak or too aggressive;
- clipping or caps dominate the result space;
- increasing duration exposure ever creates an unintended reversal;
- neutral market cases remain sensible across exposure classes;
- the mapping is easy to explain case by case.

### C. Macro Adjustment

First determine the **distinct Core Evaluation Result representations** produced by B.

If Macro Adjustment depends only on the Core score, then cases sharing the same Core score may be tested together.

If Macro Adjustment needs exposure information beyond the Core score, that requirement must be explicit and the Core Result Contract is not sufficiently represented by score alone.

Cross the relevant distinct Core Results with the 9 macro Rule Cases:

```text
Core Evaluation Result
×
Inflation Trend
×
Policy Direction
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

For every tested case preserve:

```text
core_evaluation_result
inflation_state
policy_state
macro_rule_case
macro_action
duration_evaluation_result
```

#### Required macro review outputs

Produce:

1. a detailed case table;
2. a compact matrix where practical;
3. counts and summary statistics showing how strongly Macro Adjustment changes Core results.

#### Questions for C

Inspect whether Macro Adjustment:

- remains mostly a constraint rather than a second independent directional model;
- reverses sign anywhere;
- changes neutral Core results;
- compresses the Core result space excessively;
- collapses materially different Core results too often;
- preserves ordering where economically expected;
- behaves symmetrically only where symmetry is economically justified;
- has an economically acceptable maximum effect.

If all 36 Core cases must remain distinct for Macro Adjustment, then C may effectively cover all:

```text
36 Core cases × 9 macro cases = 324 cases
```

In that situation, no separate economic review stage after C is required; only implementation consistency checks remain.

---

## 9. Summary Diagnostics

In addition to case-by-case inspection, Codex should generate descriptive summaries.

These summaries are diagnostics, not optimization targets or model-quality scores.

### 9.1 Core Evaluation summaries

At minimum:

- number of distinct Core results;
- distribution of Core results by exposure class;
- average absolute Core score by exposure class;
- number and percentage of adjacent exposure classes with identical results;
- number of monotonicity violations, if monotonicity is expected by the chosen exposure rule;
- number and percentage of cases affected by clipping or caps;
- minimum and maximum Core result by exposure class.

### 9.2 Macro Adjustment summaries

At minimum:

- percentage of cases that are pass-through;
- percentage modified by macro;
- average absolute change from Core to final result;
- maximum absolute change;
- number of sign reversals;
- number of neutral Core results changed;
- number of distinct Core results collapsing to the same final result under each macro case;
- distribution of final Duration Evaluation Results.

The goal is to make excessive compression, excessive pass-through, or unexpectedly strong macro influence visible quickly.

---

## 10. Historical Replay

After the exhaustive synthetic case review, replay selected historical dates using the historical Component States produced by the existing logic.

Candidate dates from the prior Duration work may be reused:

```text
2019-08-30
2020-03-31
2021-12-30
2022-10-31
2023-10-31
2024-09-30
```

These dates are interpretation fixtures, not optimization labels.

For each date:

1. obtain the existing market Component States;
2. obtain the corresponding macro Component States;
3. apply the same market Rule Mapping;
4. evaluate all four synthetic exposures;
5. apply Macro Adjustment;
6. display Core and final results together.

### Required historical output

Produce a compact comparison table such as:

| `as_of` | Market Rule Case | Macro Rule Case | Short | Intermediate | Long | Very Long |
|---|---|---|---:|---:|---:|---:|
| 2019-08-30 | | | | | | |
| 2020-03-31 | | | | | | |
| 2021-12-30 | | | | | | |
| 2022-10-31 | | | | | | |
| 2023-10-31 | | | | | | |
| 2024-09-30 | | | | | | |

Each exposure result should remain traceable to:

```text
market Rule Case
→ market-mapping result
→ exposure application
→ Core Evaluation Result
→ macro action
→ Duration Evaluation Result
```

### Historical analysis questions

For each date, review:

- whether exposure ordering is economically plausible;
- whether Macro Adjustment changes the result in an understandable way;
- whether macro influence is excessive relative to the rates-market condition;
- whether important distinctions among duration exposures disappear;
- whether the final pattern across exposures matches the intended semantics of the model.

Do not collapse the historical dates into one overall model score.

---

## 11. Codex Deliverables

The initial Codex task should produce review artifacts, not a reusable architecture.

Preferred outputs:

```text
duration_core_macro_review.ipynb
duration_core_macro_review_results.csv
duration_core_macro_review_summary.md
```

### Notebook

Should contain:

- reuse or import of the existing market calculations;
- fixed existing market Rule Table;
- explicit synthetic exposure definitions;
- explicit provisional exposure-application logic;
- fixed existing macro-cap logic;
- exhaustive B case generation;
- exhaustive C case generation;
- summary diagnostics;
- historical replay;
- compact matrices and drill-down tables.

### Results

Preserve all case-level fields required to reproduce the analysis.

Where useful, use separate clearly named tables or files for:

```text
core_cases
macro_cases
historical_replay
```

rather than forcing unrelated row types into one ambiguous table.

### Summary Markdown

Should report:

- the exposure rule used;
- the Core Result representation;
- notable structural findings from the 36 Core cases;
- notable findings from Macro Adjustment;
- whether the macro layer appears too weak, appropriately bounded, or too dominant;
- whether repeated result collapse is economically justified;
- suspicious cases requiring manual review;
- historical replay observations;
- open design questions revealed by the run.

The summary should describe findings rather than automatically recommend a final model.

---

## 12. Constraints on Codex

Codex should treat the design choices supplied for the run as fixed inputs.

Do not:

- add new Raw Observations;
- add new Treasury maturities;
- redesign Trend or Recent Move Components;
- tune the model to improve historical examples;
- change the existing market Rule Table;
- change the existing macro-cap table during the run;
- invent a new exposure rule when one has not been explicitly supplied;
- create generalized evaluator abstractions;
- refactor unrelated project code;
- interpret historical replay as investment-performance validation.

If an inconsistency is found, surface it as a review finding.

---

## 13. Expected Review Outcome

This draft review is intended to answer four design questions:

### 1. Exposure application

Can the existing market Rule Mapping be transformed into exposure-specific Core Duration Evaluation Results through a simple, explainable rule?

### 2. Core Result representation

What information must the Core Duration Evaluation Result retain so that Macro Adjustment can operate correctly without re-reading the full ETF Exposure Profile?

### 3. Macro influence

Does the existing provisional macro-cap logic remain economically sensible after Core Evaluation becomes exposure-specific?

### 4. Interaction

Do exposure application and Macro Adjustment interact cleanly, or do they create excessive compression, lost differentiation, reversals, or other pathological cases?

The result of this review should inform the next Duration design revision.

It should not itself be treated as a finalized Duration model, MVP definition, or production contract.

---

## 14. Open Decisions for the Next Review

Before issuing the final Codex task, resolve:

1. the provisional exposure-application rule;
2. the exact Core Evaluation Result scale;
3. whether Macro Adjustment uses only the Core score or also needs retained exposure semantics;
4. whether the four exposure classes are sufficient for the first review;
5. whether any additional summary diagnostics are needed before implementation.

All other major inputs should remain fixed for the first batch run so that the resulting differences are attributable to exposure application and Macro Adjustment rather than simultaneous redesign of multiple model layers.
