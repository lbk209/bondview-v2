# Bondview Vocabulary

## Purpose

This document defines the canonical vocabulary for **Bondview**.

Its purpose is to provide a consistent set of terms for describing how Bondview represents bond-market and macro conditions, interprets bond exposure, evaluates ETFs, and explains model behavior.

The definitions describe conceptual meaning and relationships rather than prescribing a particular implementation structure.

---

# 1. Vocabulary Map

```text
Bondview
│
├── System Responsibilities
│
├── Component Model
│   ├── Core Concepts
│   ├── Component Structure
│   └── Bond Exposure Concepts
│
├── Calculation Mechanics
│
├── ETF Evaluation
│   ├── Core Concepts
│   ├── Exposure Evaluation
│   ├── Positioning Overlay
│   └── Instrument Quality
│
├── Diagnostics
│
├── Model Definition and Interfaces
│
└── Naming Principles
```

---

# 2. System Responsibilities

| Term | Definition |
|---|---|
| **Bondview** | The complete bond-ETF analytical and decision-support system. |
| **Module** | A major system responsibility with a meaningful input/output boundary. |
| **Capability** | Reusable implementation behavior with defined semantics. |
| **Bond Analysis Module** | Produces canonical bond-relevant Components from accepted observations. |
| **ETF Evaluation Module** | Produces ETF-specific evaluation results by applying Components to ETF Exposure Profiles and implementation characteristics. |
| **Diagnostics Module** | Inspects and explains Components and evaluation results through historical analysis, interpretation, comparison, visualization, and sanity checking. |

```text
Bond Analysis
→ What bond-market and macro conditions exist?

ETF Evaluation
→ How suitable are ETFs under those conditions?

Diagnostics
→ Does the analytical and evaluation model behave plausibly and explainably?
```

---

# 3. Component Model

## 3.1 Core Concepts

| Term | Definition |
|---|---|
| **Raw Observation** | An accepted source observation used by Bondview, normally from historical time-series data. |
| **Feature** | A quantitative measure derived from Raw Observations for model use. |
| **Component** | A canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State. |
| **Component Value** | The calculated quantitative or structured representation of a Component before discrete classification. |
| **Component State** | A discrete economic condition assigned to a Component. |
| **State Classification** | The process that converts a Component Value into a Component State. |

A Feature is generally closer to calculation mechanics, while a Component represents an economically meaningful analytical concept.

Example:

```text
10Y yield change over a defined horizon
→ Feature

Long-End Yield Move
→ Component

Falling / Stable / Rising
→ Component State
```

## 3.2 Component Structure

Components carry Bondview's authoritative analytical information.

Typical Component examples include:

- Long-End Yield Trend;
- Long-End Yield Move;
- Curve Configuration;
- Curve Movement;
- Credit Spread Level;
- Credit Spread Direction;
- Inflation Trend;
- Policy Direction.

Conceptually:

```text
Raw Observations
        ↓
[Feature Calculation]
        ↓
Features
        ↓
[Component Calculation]
        ↓
Component Value
        ↓
[State Classification]
        ↓
Component State
```

A Component may also be calculated from other Components or their Values when the relationship is economically meaningful.

Example:

```text
Short-End Yield Move
        +
Long-End Yield Move
        ↓
[Curve Movement Calculation]
        ↓
Curve Movement
```

Two analytical concepts should normally be treated as the same Component only when their economic meaning, calculation, relevant horizon, and classification semantics are equivalent.

Some Components may partially overlap because they provide different economically meaningful views of the same underlying observations. This is acceptable when the distinction is analytically useful.

## 3.3 Bond Exposure Concepts

| Term | Definition |
|---|---|
| **Bond Exposure Dimension** | A principal bond-exposure dimension represented in Bondview. The current dimensions are Duration, Curve, and Credit. |
| **Bond Exposure View** | A high-level human-readable interpretation of one Bond Exposure Dimension, derived from selected Components. |
| **Duration View** | Interpretation of the Duration Dimension and current rate-sensitivity conditions. |
| **Curve View** | Interpretation of the Curve Dimension and current relative-maturity / term-structure conditions. |
| **Credit View** | Interpretation of the Credit Dimension and current credit-risk conditions. |

Bond Exposure Views are not authoritative ETF Evaluation inputs. ETF Evaluation consumes the underlying Components directly.

Views are primarily useful for explanation, historical inspection, expert sanity checking, and parameter validation.

---

# 4. Calculation Mechanics

Calculation Mechanics are reusable conceptual structures used across Components, ETF Evaluation, and Diagnostics.

**State Classification** converts a Component Value into a Component State.

```text
Credit Spread Level Value = 87th percentile
        ↓
[State Classification]
        ↓
Credit Spread Level State = Wide
```

**Rule Mapping** defines how a combination of Component States produces a model result.

| Term | Definition |
|---|---|
| **Rule Dimension** | A Component whose State participates in a particular Rule Case. |
| **Rule Case** | One concrete combination of Rule Dimension States. |
| **Rule Mapping** | The defined relationship that maps a Rule Case to a model result. |
| **Rule Table** | The configured set of Rule Mappings for one defined model purpose. |
| **Coverage Strategy** | The convention for handling the valid Rule Case space, such as explicit mapping, fallback, or justified interpolation. |

```text
Component States
        ↓
[Rule Case Construction]
        ↓
Rule Case
        ↓
[Rule Mapping]
        ↓
Mapped Result
```

The distinction is:

```text
State Classification
→ What State represents this Component Value?

Rule Mapping
→ What result follows from this combination of Component States?
```

---

# 5. ETF Evaluation

## 5.1 Core Concepts

| Term | Definition |
|---|---|
| **ETF Exposure Profile** | The economically relevant identity of an ETF's bond exposure, including properties such as maturity, duration, credit exposure, underlying market, portfolio construction, currency, and hedging where relevant. |
| **Exposure Evaluation** | The combined economic assessment of whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions. |
| **Positioning Overlay** | A post-Exposure-Evaluation adjustment reflecting crowding, sentiment, positioning, or similar implementation context. |
| **Instrument Quality** | The degree to which an ETF provides its intended Exposure Profile reliably, efficiently, and with acceptable implementation friction. |
| **Candidate Set** | The set of ETFs remaining eligible at a defined point in the evaluation flow. |

High-level flow:

```text
Canonical Components
        +
ETF Exposure Profile
        ↓
[Exposure Evaluation]
        ↓
Exposure Evaluation Result
        ↓
[Positioning Overlay]
        ↓
Positioning-Adjusted Exposure Evaluation
        ↓
[Instrument Quality]
        ↓
Evaluated Candidate Set
```

## 5.2 Exposure Evaluation

Exposure Evaluation combines several ETF-specific evaluations and related adjustment logic.

| Term | Definition |
|---|---|
| **Duration Evaluation** | ETF-specific evaluation of whether the ETF's interest-rate sensitivity is appropriate under current conditions. |
| **Curve Evaluation** | ETF-specific evaluation of whether the ETF's maturity / curve exposure is appropriate under current term-structure conditions. |
| **Credit Evaluation** | ETF-specific evaluation of whether the ETF's credit-risk exposure is appropriate under current credit conditions. |
| **Rates Valuation Evaluation** | ETF-specific evaluation of whether compensation for accepting the ETF's rates exposure is sufficiently attractive. |
| **Macro Adjustment** | A dimension-specific modification applied within an Evaluation when macroeconomic Components materially affect how strongly the exposure should be expressed. |

The four Evaluations—Duration, Curve, Credit, and Rates Valuation—operate in parallel and do not need to share identical output semantics or weighting.

**Macro Adjustment** is applied within the relevant Evaluation rather than as a separate peer Evaluation.

```text
Core Duration Evaluation Result
        +
Relevant Macro Components
        ↓
[Duration Macro Adjustment]
        ↓
Final Duration Evaluation Result
```

Possible adjustment semantics include pass-through, weaken, cap, or directional restriction.

The resulting dimension-level Evaluation results are then combined through Exposure Evaluation.

```text
Duration Evaluation Result
        +
Curve Evaluation Result
        +
Credit Evaluation Result
        +
Rates Valuation Evaluation Result
        ↓
[Exposure Evaluation]
        ↓
Exposure Evaluation Result
```

Additional inputs may include ETF-level Yield / Carry and Underlying Rate Volatility where relevant to the applicable Evaluation.

## 5.3 Positioning Overlay

**Positioning Overlay** modifies implementation willingness after Exposure Evaluation without redefining the underlying economic assessment.

Typical inputs may include crowding, sentiment, speculative positioning, unusual directional consensus, or exposure-level extension after a large market move. Possible effects include pass-through, weaker implementation preference, limits on aggressive expression, preference for less-extreme exposure, or reduced implementation intensity.

```text
Exposure Evaluation Result
        +
Positioning Inputs
        ↓
[Positioning Overlay]
        ↓
Positioning-Adjusted Exposure Evaluation
```

## 5.4 Instrument Quality

**Instrument Quality** evaluates whether an ETF is a sufficiently good vehicle after Exposure Evaluation and Positioning Overlay have been applied.

Typical inputs include expense ratio or implementation cost, liquidity, bid-ask spread, and tracking quality. Instrument Quality may serve as both a minimum-quality filter and a relative ranking criterion among acceptable ETFs.

```text
Positioning-Adjusted Exposure Evaluation
        +
Instrument Quality Inputs
        ↓
[Instrument Quality]
        ↓
Evaluated Candidate Set
```

Final ETF choice may be made from the Evaluated Candidate Set using simple ranking, weighting, thresholds, or other decision rules as appropriate.

---

# 6. Diagnostics

| Term | Definition |
|---|---|
| **Diagnostics** | Analysis that explains, validates, or inspects authoritative model behavior without changing the model's calculations or decisions. |
| **Historical Context** | Historical observations of authoritative calculated outputs used to interpret current or past model behavior. |
| **Diagnostic Comparison** | Comparison of Features, Components, Component States, Bond Exposure Views, Evaluation results, or related metadata for explanatory or validation purposes. |

Historical Context is diagnostic, not a second hidden decision model.

**Bond Exposure Views** can serve as sanity-check projections of Component behavior. Diagnostics may inspect their frequency, persistence, state transitions, historical episodes, Component-to-View traceability, and sensitivity to horizon or threshold choices.

For a selected date or period, Diagnostics should expose enough Component and supporting Feature / Raw Observation information for an expert to assess whether the interpretation is economically plausible.

---

# 7. Model Definition and Interfaces

| Term | Definition |
|---|---|
| **Model Configuration** | The declarative definition of model-specific structure and parameters used by Bondview calculations. |
| **Configuration Schema** | The contract that validates whether Model Configuration is structurally and semantically acceptable. |
| **Resolved Model Specification** | The validated, explicit runtime representation produced from Model Configuration before calculation. |

**Model Definition** describes how model structure and parameters are declared, validated, and resolved for runtime use.

```text
Model Configuration
        ↓
[Configuration Validation]
        ↓
Resolved Model Specification
```

| Term | Definition |
|---|---|
| **Result Boundary** | A formal interface through which one responsibility exposes authoritative outputs to downstream consumers. |
| **Result Contract** | The documented semantics and required contents of a particular Result Boundary. |

**Result Interfaces** define how authoritative outputs are exposed across responsibility boundaries. Concrete result objects should be defined individually when their contracts are designed rather than forcing all Modules into one generic result class.

---

# 8. Naming Principles

1. Prefer semantic names over numbered names.
2. Use **Module** only for major system responsibilities with meaningful boundaries.
3. Use **Capability** for implementation behavior.
4. Keep **Raw Observation**, **Feature**, and **Component** distinct.
5. Keep **Component Value** and **Component State** distinct where a discrete State exists.
6. Treat **Component** as the authoritative reusable analytical concept.
7. A Component may be derived from Features or from other Components / Component Values when economically meaningful.
8. Use **Bond Exposure Dimension** for Duration, Curve, and Credit.
9. Use **Bond Exposure View** for their high-level human-readable interpretations.
10. Use **Exposure Evaluation** for the combined economic assessment of an ETF's exposure.
11. Use **Macro Adjustment** for evaluator-specific macro modification.
12. Use **Positioning Overlay** for post-economic-evaluation crowding / sentiment / positioning adjustment.
13. Use **Instrument Quality** only for implementation quality, not for economic attractiveness.
14. Use **Candidate Set** as the general term for ETFs remaining eligible at a defined point in the evaluation flow.
15. Use **Rule Case**, **Rule Mapping**, **Rule Table**, and **Coverage Strategy** as general Calculation Mechanics.
16. Use **Result Boundary / Result Contract** as generic interface concepts while defining concrete results separately.
