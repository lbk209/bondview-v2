# Bondview Duration Vertical-Slice MVP

## Purpose

This MVP validates Bondview's **Duration Constituent Evaluation** as a direct vertical slice of the authoritative ETF Evaluation path.

The MVP asks whether real historical bond-market and macroeconomic observations, combined with materially different ETF duration exposures, produce economically plausible, differentiated, and traceable **Duration Evaluation Results**.

The MVP does **not** create an ETF-independent Duration Bond Exposure View. Market and macroeconomic conditions remain represented by authoritative Components; exposure-specific interpretation begins inside Duration Evaluation.

---

## Scope

The MVP covers one Constituent Evaluation only:

```text
Accepted Raw Observations
        ↓
[Feature Calculation]
        ↓
Features
        ↓
[Component Calculation]
        ↓
Components
        ↓
[Duration Core Evaluation] <────── Duration-relevant ETF Exposure Profile
        ↓
Core Duration Evaluation Result
        ↓
[Macro Adjustment] <────────────── Relevant Macroeconomic Components
        ↓
Duration Evaluation Result
        ↓
[Diagnostics]
        ↓
Diagnostic Results
```

The MVP stops at the **Duration Evaluation Result**.

It does not implement:

- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation;
- Evaluation Combination;
- Positioning Overlay;
- Instrument Quality;
- complete ETF Evaluation Results;
- ETF ranking or final choice.

The Duration Evaluation Result is an intermediate authoritative ETF Evaluation result, not a Component and not a Diagnostic Result.

Diagnostics may inspect the Duration Evaluation Result and its dependency lineage but must not create an additional Duration market score or other parallel evaluation model.

---

## Core Architectural Contract

### Exposure enters before Macro Adjustment

The MVP must preserve the following ordering:

```text
Relevant rates Components
+
Duration-relevant ETF Exposure Profile
        ↓
Core Duration Evaluation
        ↓
Core Duration Evaluation Result

Core Duration Evaluation Result
+
Relevant macroeconomic Components
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

The Core Duration Evaluation Result is therefore already **exposure-specific**.

Macro Adjustment modifies that exposure-specific result. It must not be implemented as an ETF-independent macro-adjusted Duration View that is later applied to ETFs.

### Core and macro roles are not interchangeable

Components used by Core Duration Evaluation and Components used by Macro Adjustment have different model roles.

They must not be flattened into a single undifferentiated additive vote such as:

```text
rate Component
+ rate Component
+ inflation Component
+ policy Component
→ one peer-weighted score
```

unless a later approved Duration design explicitly changes the model to define those inputs as peers.

The MVP configuration and code should preserve explicit intermediate outputs for:

1. Core Duration Evaluation Result;
2. Macro Adjustment decision or action;
3. final Duration Evaluation Result.

---

## Initial Analytical Inputs

The following Components are the initial provisional inputs for the Duration MVP.

### Core Duration Evaluation Components

```text
Long-End Yield Trend
Recent Long-End Yield Move
```

These represent the rates-market conditions relevant to the Core Duration Evaluation.

### Macro Adjustment Components

```text
Inflation Trend
Policy Direction
```

These represent macroeconomic conditions that may modify the exposure-specific Core Duration Evaluation Result.

The named Components are provisional MVP inputs rather than permanent system-architecture requirements.

Their Raw Observations, Features, horizons, thresholds, State Classification, and exact mappings remain evaluator-specific model choices and should be explicit in the MVP configuration or Duration-specific design before being treated as settled model behavior.

---

## Duration Exposure Profiles

The MVP uses a small set of Korea-listed ETFs providing U.S. bond exposure and intentionally spans materially different duration profiles.

The ETFs are **test fixtures**, not an investment recommendation or permanent Bondview universe.

| Ticker | ETF | MVP duration role | Benchmark / reference exposure for MVP Profile | Inception |
|---|---|---|---|---|
| `329750` | TIGER 미국달러단기채권액티브 | Short | KIS U.S. Treasury Bond 0–1Y Index; benchmark duration approximately six months | 2019-07-22 |
| `305080` | TIGER 미국채10년선물 | Intermediate / 10-year | S&P 10-Year U.S. Treasury Note Futures (ER) Index | 2018-08-28 |
| `267440` | RISE 미국장기국채선물(H) | Long | S&P U.S. Treasury Bond Futures Excess Return Index | 2017-04-20 |
| `304660` | KODEX 미국30년국채울트라선물(H) | Very long / ultra-long | S&P Ultra T-Bond Futures Excess Return Index | 2018-09-12 |

For the MVP, ETF Exposure Profiles should contain only the duration-relevant information required by Core Duration Evaluation.

The declared benchmark or reference exposure should be the primary basis for the Profile. The MVP should not expand into a generalized ETF metadata or Profile framework.

Strict benchmark tracking is sufficient as the initial working assumption for treating the benchmark as a reliable proxy for the designed duration exposure. Products whose duration exposure cannot be represented clearly enough for the evaluator should remain unevaluated rather than forcing an approximate Profile.

No liquidity criterion is required because this MVP validates Duration Evaluation behavior rather than execution or final ETF selection.

---

## Core Duration Evaluation

Core Duration Evaluation answers:

> Given the current rates-market Components, how appropriate is this ETF's defined duration exposure?

It must jointly interpret:

```text
Long-End Yield Trend
Recent Long-End Yield Move
ETF Duration Exposure Profile
```

and produce an explicit **Core Duration Evaluation Result**.

The broader Long-End Yield Trend and the Recent Long-End Yield Move should not automatically be treated as equal independent votes. Their economic relationship and Rule Mapping must be explicit in the Duration-specific MVP model definition.

Likewise, ETF duration exposure must materially participate in the Core Evaluation. The MVP must not calculate a complete ETF-independent Duration judgment first and then merely attach the ETF Profile afterward.

### Rule Mapping requirement

Before an implementation is treated as model-complete, the MVP must expose the Core Duration Rule Mapping or equivalent explicit mapping logic sufficiently to answer:

- which Component States and Profile characteristics form the Rule Case;
- what Core Duration Evaluation Result follows from each covered case;
- how uncovered valid cases are handled;
- how materially different duration exposures can produce different Core results under the same rates environment.

The architecture does not prescribe the exact Duration Rule Table. A provisional MVP Rule Table is acceptable, but it must be explicit and reviewable rather than emerging implicitly from code.

---

## Macro Adjustment

Macro Adjustment answers:

> Given the exposure-specific Core Duration Evaluation Result, should current macroeconomic conditions modify that assessment?

Initial inputs are:

```text
Core Duration Evaluation Result
+
Inflation Trend
+
Policy Direction
```

Possible action semantics include:

```text
pass-through
weaken
magnitude cap
other explicitly justified evaluator-specific modification
```

The exact action set and Rule Mapping are provisional Duration-model choices.

### Exposure-specific effect

Macro Adjustment does not need to receive the full ETF Exposure Profile again when the Core Duration Evaluation Result already preserves sufficient exposure semantics or references.

The same macroeconomic condition may nevertheless have different final effects across ETFs because their different profiles may have produced different Core Duration Evaluation Results.

For example, an adverse macro condition might leave a moderate positive Core result unchanged while capping a stronger positive Core result associated with more aggressive duration exposure.

If a proposed macro rule directly requires exposure information that is not represented or referenced by the Core Duration Evaluation Result, that requirement should be made explicit rather than silently re-reading the Profile inside generic macro logic.

### No flat core/macro aggregation

The following structure is explicitly outside the intended MVP model:

```text
Long-End Yield Trend     → +1 / 0 / -1
Recent Yield Move        → +1 / 0 / -1
Inflation Trend          → +1 / 0 / -1
Policy Direction         → +1 / 0 / -1
                              ↓
                           sum
                              ↓
                    Duration Evaluation
```

because it erases the distinction between exposure-specific Core Evaluation and Macro Adjustment.

---

## Input Boundary and Historical Data

The analytical MVP begins from **accepted Raw Observations**.

For practical MVP execution, historical observations may be retrieved directly from FRED / ALFRED in the notebook or a small local helper. Such retrieval is an implementation convenience and is not a production ingestion architecture.

Historical evaluation should preserve `as_of` correctness. Revised macroeconomic series should use historical vintage information where necessary to avoid future-information leakage.

End-of-day archive availability is an acceptable temporal convention for this MVP. The MVP does not attempt to model intraday release timing or real-time trading execution.

---

## Historical Test Dates

The MVP should inspect Duration Evaluation Results across materially different historical environments.

The following dates remain candidate `as_of` dates:

| Candidate `as_of` | Intended regime coverage |
|---|---|
| 2019-08-30 | easing environment |
| 2020-03-31 | severe shock / aggressive easing environment |
| 2021-12-30 | inflation and policy-transition environment |
| 2022-10-31 | aggressive tightening environment |
| 2023-10-31 | high-yield / restrictive environment |
| 2024-09-30 | later easing-transition environment |

These dates are historical validation fixtures, not model parameters or training labels.

Before changing rules to improve the results, the MVP should document ex-ante directional plausibility expectations for the selected regimes. The purpose is to detect economically suspicious behavior, not to tune the model until every historical case matches a preferred categorical label.

The 2021 policy-transition case is particularly useful for identifying limitations in a purely realized `Policy Direction` Component and should be treated as a diagnostic stress case rather than automatically forcing a redesign of the Component.

---

## Cross-ETF and Historical Comparison

The MVP should evaluate the same historical environments across all evaluable Duration Profiles.

| Candidate `as_of` | Short `329750` | Intermediate `305080` | Long `267440` | Very long `304660` |
|---|---:|---:|---:|---:|
| 2019-08-30 | evaluate | evaluate | evaluate | evaluate |
| 2020-03-31 | evaluate | evaluate | evaluate | evaluate |
| 2021-12-30 | evaluate | evaluate | evaluate | evaluate |
| 2022-10-31 | evaluate | evaluate | evaluate | evaluate |
| 2023-10-31 | evaluate | evaluate | evaluate | evaluate |
| 2024-09-30 | evaluate | evaluate | evaluate | evaluate |

Reading across a row provides the **cross-sectional test**:

> Does the same market and macro environment produce sensible differentiation among materially different duration exposures?

Reading down a column provides the **longitudinal test**:

> Does the same duration exposure receive sensibly different evaluations across materially different historical environments?

Both comparisons are required for the MVP.

---

## Diagnostics

Diagnostics is applied to the actual Duration Evaluation path.

For each Duration Evaluation Result, the implementation should allow backward inspection through:

```text
Duration Evaluation Result
        ↑
Macro Adjustment
        ↑
Core Duration Evaluation Result
        ↑
Duration-relevant ETF Exposure Profile
+
Relevant Components
        ↑
Features
        ↑
Raw Observations
```

Diagnostics may inspect:

- Core versus final Duration Evaluation Result;
- the Macro Adjustment action and inputs;
- relevant ETF duration-profile characteristics;
- Component Values and States;
- Feature and Raw Observation lineage;
- historical frequency and persistence;
- transitions and historical episodes;
- parameter and threshold sensitivity;
- cross-ETF comparison at the same `as_of`;
- same-ETF comparison across historical `as_of` dates.

Diagnostics must not create an ETF-independent Duration score, Bond Exposure View, or other second evaluation model.

---

## Implementation Approach

The MVP should remain simple and inspection-oriented.

Preferred structure:

```text
duration_mvp.ipynb
duration_model.py
duration_mvp.yaml
```

### `duration_mvp.ipynb`

Responsibilities:

- retrieve or load accepted historical observations;
- orchestrate Feature and Component calculations;
- load minimal Duration Exposure Profiles;
- call Core Duration Evaluation;
- call Macro Adjustment;
- display Core and final Duration Evaluation Results;
- perform cross-ETF, historical, lineage, and sensitivity Diagnostics.

### `duration_model.py`

Responsibilities:

- Duration-specific Feature calculations;
- Component calculations and State Classification used by the MVP;
- Core Duration Evaluation;
- Macro Adjustment;
- small local calculation helpers where clearly useful.

The file should preserve conceptual boundaries even if several calculations live in the same module.

### `duration_mvp.yaml`

Responsibilities:

- provisional horizons and smoothing parameters;
- Component thresholds and classification parameters;
- minimal Duration Exposure Profile configuration;
- explicit Core Duration Rule Mapping or equivalent model parameters;
- explicit Macro Adjustment Rule Mapping or equivalent model parameters.

Behavior-sensitive configuration must remain reviewable. Changing a Rule Mapping, threshold, or exposure mapping is a model change, not merely a formatting or implementation change.

### Implementation simplicity

Use plain functions, DataFrames, dictionaries, and simple configuration structures where sufficient.

Do not create:

- a generic evaluator framework;
- a plugin registry;
- generalized ETF metadata infrastructure;
- reusable abstraction layers justified only by anticipated future Curve or Credit work.

Shared Capabilities should be extracted only after genuine repeated semantics are demonstrated.

---

## Explicitly Out of Scope

The MVP does not need to implement:

- an ETF-independent Bond Exposure View;
- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation;
- Evaluation Combination across Constituent Evaluations;
- Positioning Overlay;
- Instrument Quality;
- complete ETF Evaluation Results;
- final ETF ranking or choice;
- generalized ETF metadata management;
- generalized Profile construction;
- production-grade data ingestion;
- live execution data;
- intraday release-time modeling;
- polished UI;
- generic reusable evaluator infrastructure.

Forward ETF returns may be added as a secondary diagnostic later, but they are not required for initial MVP success.

---

## Validation Questions

The MVP should answer five questions.

### 1. Component plausibility

Are the Duration-relevant Component Values and States economically interpretable and traceable at each historical `as_of` date?

### 2. Exposure differentiation

Under the same rates environment, does Core Duration Evaluation produce sensible differences across short, intermediate, long, and very-long duration profiles?

### 3. Macro behavior

Does Macro Adjustment modify exposure-specific Core results in an economically interpretable way without behaving as an independent peer vote or recreating the Core evaluation?

### 4. Historical behavior

For the same Duration Profile, does the final Duration Evaluation Result change sensibly across materially different historical environments?

### 5. Explanatory traceability

Can each final Duration Evaluation Result be explained directly through:

```text
Raw Observations
→ Features
→ Components
→ ETF Duration Profile
→ Core Duration Evaluation Result
→ Macro Adjustment
→ Duration Evaluation Result
```

without introducing a second diagnostic decision model?

---

## Decision Criterion

The MVP succeeds if the Duration Constituent Evaluation produces results that are:

- economically credible across materially different historical environments;
- meaningfully differentiated across materially different duration exposures;
- explicit about the separate roles of Core Evaluation and Macro Adjustment;
- traceable through the authoritative analytical lineage;
- sufficiently stable under reasonable parameter sensitivity to support further model work.

The MVP should trigger redesign if:

- the ETF Exposure Profile has little or no effect on Core Duration Evaluation;
- Macro Adjustment behaves like an interchangeable peer contribution rather than a modification of an exposure-specific Core result;
- materially different duration exposures repeatedly collapse to indistinguishable results without economic justification;
- historical results are unstable, arbitrary, or economically implausible;
- Diagnostics requires a second hidden market-level model to explain the result.

---

## Next Step After MVP

If the Duration Constituent Evaluation is judged useful, the next step is to decide whether to:

- refine the Duration evaluator and its Profile contract;
- add Rates Valuation, Curve, or Credit Constituent Evaluations;
- test Evaluation Combination;
- or extract shared implementation mechanics that have now demonstrated real reuse.

The next step should follow observed model needs rather than pre-building the rest of the architecture.
