# Bondview Duration Vertical-Slice MVP

## Purpose

This MVP tests whether Bondview's core analytical approach can be implemented end to end and produce an economically useful **Duration Bond Exposure View** from real historical bond-market and macroeconomic observations.

The initial objective is to validate the Duration analytical interpretation independently of ETF-specific exposure. The MVP should determine whether the underlying Components and the resulting Duration Bond Exposure View are economically plausible, regime-sensitive, and traceable.

ETF-specific **Duration Evaluation** is a possible second-stage extension. It should be considered only after the Stage 1 Duration Bond Exposure View is judged useful.

---

## Scope

### Stage 1 — Duration Bond Exposure View

The initial MVP covers:

```text
Raw Observations
        ↓
[Feature Calculation]
        ↓
Features
        ↓
[Component Calculation]
        ↓
Duration-related Components
        ↓
[Duration Bond Exposure View Calculation]
        ↓
Duration Bond Exposure View
```

Stage 1 intentionally excludes ETF Exposure Profiles and ETF-specific Duration Evaluation.

The primary output is a **Duration Bond Exposure View** for selected historical `as_of` dates, with enough analytical lineage to inspect how the result was produced.

### Stage 2 — Candidate Extension

Only after Stage 1 is judged useful should the MVP consider applying the same authoritative Components to ETF-specific duration exposures:

```text
Relevant Components
        ↓
[Duration Core Evaluation] <──────── Duration-relevant ETF Exposure Profile
        ↓
Core Duration Evaluation Result
        ↓
[Macro Adjustment] <────────────── Relevant Macroeconomic Components
        ↓
Duration Evaluation Result
```

Stage 2 would test whether the Component interpretation validated in Stage 1 can be applied sensibly to ETFs with meaningfully different duration exposures.

The primary Stage 2 output is a comparable set of **Duration Evaluation Results across the selected ETFs**. Stage 2 stops at this Constituent Evaluation output and does not attempt to produce a complete ETF Evaluation Result.

The Stage 1 Bond Exposure View must not become an input to Stage 2 ETF Evaluation. Both Stage 1 and Stage 2 consume authoritative Components directly for their own purposes.

---

## Initial Duration Logic

The MVP should use the current Duration design as the starting point.

### Initial Duration-Related Components

The following Components are provisional analytical inputs for Stage 1:

```text
Long-End Yield Trend
Recent Long-End Yield Move
Inflation Trend
Policy Direction
```

`Long-End Yield Trend` and `Recent Long-End Yield Move` provide the initial rates-side interpretation. `Inflation Trend` and `Policy Direction` provide relevant macroeconomic context.

The exact View mapping, Raw Observations, Features, horizons, thresholds, State Classification rules, Rule Cases, and mappings should be implemented only to the degree required to produce and inspect the Duration Bond Exposure View.

The named Components are provisional MVP inputs rather than system-architecture requirements. Their exact definitions may change during implementation if the resulting Duration interpretation remains economically coherent.

If Stage 2 is reached, the current candidate structure is:

### Components for Core Evaluation

```text
Long-End Yield Trend
        +
Recent Long-End Yield Move
        ↓
Core Evaluation
```

### Macroeconomic Components for Macro Adjustment

```text
Inflation Trend
        +
Policy Direction
        ↓
Macro Adjustment
```

---

## Input Boundary

The MVP begins from **accepted Raw Observations**. Data downloading, source-specific retrieval, and production-grade ingestion are not part of what this MVP is intended to validate.

---

## Historical Test Dates

Stage 1 should inspect the Duration Bond Exposure View across a small number of materially different historical rate environments.

The following dates are initial **candidate `as_of` dates**, not fixed model parameters. If a date is not suitable for the required analytical inputs, it may be shifted to the nearest suitable date while preserving the intended regime.

| Candidate `as_of` | Intended regime coverage | Stage 1 output |
|---|---|---|
| 2019-08-30 | easing environment | Duration Bond Exposure View |
| 2020-03-31 | severe shock / aggressive easing environment | Duration Bond Exposure View |
| 2021-12-30 | inflation and policy-transition environment | Duration Bond Exposure View |
| 2022-10-31 | aggressive tightening environment | Duration Bond Exposure View |
| 2023-10-31 | high-yield / restrictive environment | Duration Bond Exposure View |
| 2024-09-30 | later easing-transition environment | Duration Bond Exposure View |

These dates should provide enough variation to determine whether the Duration interpretation changes meaningfully across regimes rather than merely restating one current-market observation.

---

## Stage 2 Candidate ETF Test Set

The following ETF configuration is retained as a candidate Stage 2 test set and should be used only if Stage 1 succeeds.

The test set uses a small number of **Korea-listed ETFs providing U.S. bond exposure** and intentionally spans meaningfully different duration exposures:

```text
short duration
        ↓
intermediate / 10-year exposure
        ↓
long duration
        ↓
very long / ultra-long duration
```

The selected ETFs are test fixtures for validating Duration Evaluation behavior. They are not a recommended investment universe or a permanent Bondview ETF universe.

| Ticker | ETF | MVP duration role | Benchmark / reference exposure for MVP Profile | Inception |
|---|---|---|---|---|
| `329750` | TIGER 미국달러단기채권액티브 | Short | KIS U.S. Treasury Bond 0–1Y Index; benchmark duration is approximately six months | 2019-07-22 |
| `305080` | TIGER 미국채10년선물 | Intermediate / 10-year | S&P 10-Year U.S. Treasury Note Futures (ER) Index | 2018-08-28 |
| `267440` | RISE 미국장기국채선물(H) | Long | S&P U.S. Treasury Bond Futures Excess Return Index | 2017-04-20 |
| `304660` | KODEX 미국30년국채울트라선물(H) | Very long / ultra-long | S&P Ultra T-Bond Futures Excess Return Index | 2018-09-12 |

For Stage 2, ETF Exposure Profiles may be manually configured and should contain only the information required by Duration Evaluation. The declared benchmark or reference exposure should be the primary basis for the duration-relevant Profile. Product implementation details beyond what Duration Evaluation requires should not be expanded into a generalized Profile model.

Because `329750` is the latest-inception product in the candidate set, the common ETF-history window cannot begin earlier than July 2019.

No liquidity criterion is required because Stage 2 would validate Duration Evaluation behavior rather than select an ETF for execution.

### Candidate Stage 2 Cross-ETF Matrix

If Stage 2 is reached, the same historical environments may be used for cross-sectional and longitudinal ETF comparison:

| Candidate `as_of` | Short `329750` | Intermediate `305080` | Long `267440` | Very long `304660` |
|---|---:|---:|---:|---:|
| 2019-08-30 | evaluate | evaluate | evaluate | evaluate |
| 2020-03-31 | evaluate | evaluate | evaluate | evaluate |
| 2021-12-30 | evaluate | evaluate | evaluate | evaluate |
| 2022-10-31 | evaluate | evaluate | evaluate | evaluate |
| 2023-10-31 | evaluate | evaluate | evaluate | evaluate |
| 2024-09-30 | evaluate | evaluate | evaluate | evaluate |

Reading across a row provides the **cross-sectional test**: how the same market environment is interpreted for different duration exposures.

Reading down a column provides the **longitudinal test**: how the same duration exposure is evaluated across different historical rate environments.

---

## Implementation Approach

The MVP should be implemented primarily in a **Jupyter notebook** so that calculation boundaries, intermediate results, historical comparisons, and diagnostic inspection remain visible.

A minimal supporting structure is preferred:

```text
duration_mvp.ipynb
duration_model.py
duration_mvp.yaml
```

The intended responsibilities are:

- `duration_mvp.ipynb`
  - orchestrates the MVP flow;
  - loads accepted observations and configuration;
  - calls Feature and Component calculations;
  - displays intermediate inputs and outputs;
  - produces and inspects Stage 1 Duration Bond Exposure Views;
  - performs historical comparison and diagnostics;
  - implements Stage 2 only if Stage 1 succeeds.

- `duration_model.py`
  - contains Duration-specific Feature calculations;
  - contains Component calculations and State Classification;
  - may contain small, clearly reusable calculation helpers such as moving averages or rolling changes where useful;
  - should keep Feature and Component outputs conceptually distinguishable even when implemented in the same file.

- `duration_mvp.yaml`
  - contains provisional model parameters such as horizons, smoothing windows, thresholds, or other values that are useful to inspect and adjust separately from code.

The Python and YAML artifacts are **MVP implementation aids**, not final reusable architecture. They may later serve as evidence for what should be generalized, extracted, or formalized, but the MVP should not create reusable infrastructure merely in anticipation of future use.

Inputs and outputs at each analytical boundary should remain explicit enough to inspect the progression:

```text
Accepted Raw Observations
→ Features
→ Component Values / States
→ Duration Bond Exposure View
```

If Stage 2 is reached:

```text
Component Values / States
+ Duration-relevant ETF Exposure Profile
→ Core Duration Evaluation Result
→ Duration Evaluation Result
```

---

## Diagnostics

Lineage-based Diagnostics are part of Stage 1.

For each Duration Bond Exposure View, the implementation should allow backward inspection through the relevant analytical lineage:

```text
Duration Bond Exposure View
        ↑
Relevant Component Values / States
        ↑
Features
        ↑
Raw Observations
```

Diagnostics should remain limited to the actual dependency lineage of the Duration result.

Historical inspection of the same lineage entities may be used to assess persistence, transitions, and economic plausibility.

If Stage 2 is reached, equivalent lineage inspection should extend through the Duration Evaluation path without making the Stage 1 Bond Exposure View an authoritative input.

---

## Explicitly Out of Scope

Stage 1 does not need to implement:

- ETF Exposure Profiles;
- ETF-specific Duration Evaluation;
- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation;
- Evaluation Combination across constituent evaluations;
- Positioning Overlay;
- Instrument Quality;
- final ETF ranking or choice;
- generalized ETF metadata management;
- shared Capability extraction or reusable framework design;
- production-grade data ingestion;
- polished UI.

Stage 2 ETF-specific Duration Evaluation should be considered only after Stage 1 succeeds. If Stage 2 is reached, it still stops at the Duration Constituent Evaluation Result; complete ETF Evaluation, Evaluation Combination, other Constituent Evaluations, Positioning Overlay, Instrument Quality, and final ETF choice remain outside this MVP.

Code may remain local and Duration-specific where that is simpler.

---

## Validation

Stage 1 should be executable for historical `as_of` dates and expose enough intermediate information to inspect:

```text
Accepted Raw Observations
→ Features
→ Component Values / States
→ Duration Bond Exposure View
```

The primary Stage 1 questions are:

1. Are the Component States economically interpretable?
2. Does the Duration Bond Exposure View change meaningfully across different rate regimes?
3. Is the resulting Duration interpretation economically plausible for each selected historical `as_of` date?
4. Can each View be explained directly through its analytical lineage?
5. Does historical inspection suggest that the View contains useful interpretation rather than merely reproducing an obvious yield observation?

Forward ETF returns are not required for Stage 1.

If Stage 1 succeeds, Stage 2 should validate the ETF-specific application in both cross-sectional and longitudinal directions.

The primary Stage 2 questions are:

1. Does the same market environment produce sensible differentiation among ETFs with different duration exposures when the validated Components are applied to their duration-relevant ETF Exposure Profiles?
2. For the same ETF Exposure Profile, does the Duration Evaluation Result change sensibly across materially different historical rate regimes?
3. Can each Duration Evaluation Result be explained directly through its analytical lineage?

Forward ETF returns may be added in Stage 2 as a simple secondary validation aid, but they are not required for Stage 2 success.

---

## Decision Criterion

### Stage 1

Stage 1 succeeds if real historical observations produce a **credible, regime-sensitive, and explainable Duration Bond Exposure View**, with each result traceable through its analytical lineage.

Stage 1 should trigger redesign if reasonable model specifications produce unstable, arbitrary, weakly interpretable, or economically implausible Duration Views.

If the Duration interpretation itself is not useful, Bondview should reconsider the Duration analytical design before implementing ETF-specific Duration Evaluation.

### Stage 2

Stage 2 should be considered only after Stage 1 succeeds.

Stage 2 succeeds if the same authoritative Components produce **economically credible and meaningfully differentiated Duration Evaluation Results across ETFs with different duration exposures**, with each result traceable through its analytical lineage and behaving sensibly across historical regimes.

Stage 2 should trigger redesign if reasonable model specifications produce unstable, arbitrary, weakly differentiated, or poorly explainable ETF-specific Duration Evaluation Results.

---

## Next Step After MVP

If Stage 1 is judged useful, the next step is to decide whether to proceed with the Stage 2 ETF-specific Duration Evaluation using the candidate ETF test set above.

Only after the relevant Duration slice is validated should Bondview proceed to additional constituent evaluations or extract shared implementation structures demonstrated by actual reuse.
