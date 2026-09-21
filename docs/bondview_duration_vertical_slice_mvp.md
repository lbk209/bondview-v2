# Bondview Duration Vertical-Slice MVP

## Purpose

This MVP tests whether Bondview's core analytical approach can be implemented end to end and produce economically useful **Duration Evaluation Results across several bond ETFs**.

The objective is not to complete ETF selection or build reusable infrastructure. It is to validate one analytical dimension deeply enough to determine whether Bondview produces sensible cross-ETF differentiation and traceable explanations.

---

## Scope

The MVP covers:

```text
Raw Observations
        ↓
[Feature Calculation]
        ↓
Features
        ↓
[Component Calculation]
        ↓
Duration-related Canonical Components
        ↓
[Duration Core Evaluation] <──────── ETF Exposure Profile
        ↓
Core Duration Evaluation Result
        ↓
[Macro Adjustment] <────────────── Relevant Macro Components
        ↓
Duration Evaluation Result
```

The same market and macro Components are applied to several ETFs with meaningfully different duration exposures.

The ETF Exposure Profiles may be manually configured. Declared benchmarks or reference exposures may be used as the simplest practical basis.

The primary output is a comparable set of **Duration Evaluation Results across the selected ETFs**.

---

## Initial Duration Logic

The MVP should use the current Duration design as the starting point.

### Market Components

```text
Long-End Yield Trend
        +
Recent Long-End Yield Move
        ↓
Duration Core Evaluation
```

### Macro Components

```text
Inflation Trend
        +
Policy Direction
        ↓
Macro Adjustment
```

The exact Raw Observations, Features, horizons, thresholds, State Classification rules, Rule Cases, and mappings should be implemented only to the degree required to produce and inspect the Duration results.

---

## ETF Comparison

The ETF set should be small but intentionally span different duration exposures, for example:

```text
short duration
intermediate duration
long duration
very long duration
```

The MVP should make it possible to compare how the same market environment produces different Duration Evaluation Results across these ETFs.

Final ETF selection is not required.

---

## Diagnostics

Lineage-based Diagnostics are part of the MVP.

For each ETF Duration Evaluation Result, the implementation should allow backward inspection through the relevant analytical lineage:

```text
ETF Duration Evaluation Result
        ↑
Core Duration Evaluation / Macro Adjustment
        ↑
Relevant Component Values / States
        ↑
Features
        ↑
Raw Observations
```

Diagnostics should remain limited to the actual dependency lineage of the Duration result.

Historical inspection of the same lineage entities may be used to assess persistence, transitions, and economic plausibility.

---

## Explicitly Out of Scope

The MVP does not need to implement:

- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation unless later required to understand Duration viability;
- Evaluation Combination across constituent evaluations;
- Positioning Overlay;
- Instrument Quality;
- final ETF ranking or choice;
- generalized ETF metadata management;
- shared Capability extraction or reusable framework design;
- production-grade data ingestion;
- polished UI.

Code may remain local and Duration-specific where that is simpler.

---

## Validation

The MVP should be executable for historical `as_of` dates and expose enough intermediate information to inspect:

```text
Raw Observations
→ Features
→ Component Values / States
→ Core Duration Evaluation
→ Macro Adjustment
→ ETF-specific Duration Evaluation Results
```

The primary questions are:

1. Are the Component states economically interpretable?
2. Does the Duration evaluation change meaningfully across different rate regimes?
3. Does the same market environment produce sensible differentiation among ETFs with different duration exposures?
4. Can each ETF result be explained directly through its analytical lineage?
5. Does historical inspection suggest that the result contains useful information rather than merely reproducing an obvious yield observation?

Forward ETF returns may be added later as a simple validation aid, but they are not required for the first vertical slice.

---

## Decision Criterion

The MVP succeeds if real historical observations can produce **economically credible and meaningfully differentiated Duration Evaluation Results across several ETFs**, with each result traceable through its lineage.

The MVP should trigger redesign if reasonable model specifications produce unstable, arbitrary, or weakly differentiated ETF results.

If the Duration dimension cannot produce useful differentiation or explanation despite reasonable design choices, Bondview's broader analytical approach should be reconsidered before implementing additional dimensions.

---

## Next Step After MVP

Only after the Duration vertical slice is judged useful should Bondview proceed to additional constituent evaluations or extract shared implementation structures demonstrated by actual reuse.
