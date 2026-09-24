# Bondview Vocabulary

## Purpose

This document defines the canonical vocabulary for **Bondview**.

Its purpose is to provide a consistent set of terms for describing how Bondview represents bond-market and macroeconomic conditions, evaluates ETF exposures, and explains model behavior.

This document is the source of truth for **term meaning and naming**. `bondview_system_architecture.md` is the source of truth for **system structure, ownership, dependency direction, processing flow, and Result Boundaries**.

The definitions below may include compact conceptual relationships where those relationships are necessary to distinguish terms, but they do not prescribe detailed implementation structure.

---

# 1. Vocabulary Map

```text
Bondview
│
├── System Responsibilities
│
├── Component Model
│   ├── Core Concepts
│   ├── Component Relationships
│   └── Exposure Dimensions
│
├── Calculation Mechanics
│
├── ETF Evaluation
│   ├── Core Concepts
│   ├── Constituent Evaluations
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
| **Bond Analysis Module** | Produces authoritative bond-relevant Components from accepted Raw Observations. |
| **ETF Evaluation Module** | Produces ETF-specific evaluation results by applying Components to ETF Exposure Profiles and supported implementation characteristics. |
| **Diagnostics Module** | Inspects and explains Components and ETF Evaluation results through historical analysis, comparison, visualization, traceability, and sanity checking without creating a separate authoritative analytical model. |

```text
Bond Analysis
→ What bond-market and macroeconomic conditions exist?

ETF Evaluation
→ How appropriate are defined ETF exposures under those conditions?

Diagnostics
→ Does the analytical and evaluation model behave plausibly and explainably?
```

---

# 3. Component Model

## 3.1 Core Concepts

| Term | Definition |
|---|---|
| **Raw Observation** | An accepted source observation used by Bondview. |
| **Feature** | A quantitative measure derived from Raw Observations for model use. |
| **Component** | A canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State. |
| **Component Value** | The calculated quantitative or structured representation of a Component before discrete classification. |
| **Component State** | A discrete economic condition assigned to a Component when discrete classification is useful. |
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

## 3.2 Component Relationships

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

At a high level:

```text
Raw Observation
        ↓
Feature
        ↓
Component Value
        ↓
Component State, where applicable
```

A Component may be derived from Features or from other Components or Component Values when economically meaningful.

A Component's upstream representation is uniform across the architecture, but its downstream economic role is consumer-specific. For example, one evaluator may use selected Components for Core Evaluation and other Components for Macro Adjustment.

Detailed Component construction, identity, consolidation, lineage, and Result Contract rules belong to the system architecture and more specific Component design documents.

## 3.3 Exposure Dimensions

| Term | Definition |
|---|---|
| **Bond Exposure Dimension** | A principal economically distinct aspect of bond exposure used to organize evaluation questions. Current examples include Duration, Curve, and Credit. |

A Bond Exposure Dimension is descriptive vocabulary. It is not a separate calculated result and does not imply an ETF-independent Bond Exposure View.

---

# 4. Calculation Mechanics

Calculation Mechanics are reusable conceptual structures used across Components and ETF Evaluation and may also be inspected by Diagnostics.

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

Reusable mechanics do not erase model semantics. Where a model assigns different roles such as Core Evaluation and Macro Adjustment, those roles remain distinct even if both stages use similar mechanics.

---

# 5. ETF Evaluation

## 5.1 Core Concepts

| Term | Definition |
|---|---|
| **ETF Exposure Profile** | The economic identity of the bond exposure that an ETF is designed to provide. |
| **Exposure Evaluation** | The combined economic assessment of whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions. |
| **Constituent Evaluation** | An ETF-specific evaluation of one economically distinct aspect of an ETF's Exposure Profile within Exposure Evaluation. |
| **Core Evaluation** | The exposure-specific economic assessment within a Constituent Evaluation before any applicable Macro Adjustment. It jointly interprets the relevant non-macro Components and the relevant ETF Exposure Profile. |
| **Core Evaluation Result** | The intermediate exposure-specific result produced by Core Evaluation and supplied to any applicable Macro Adjustment. |
| **Macro Adjustment** | An evaluator-specific modification of an already exposure-specific Core Evaluation Result using relevant macroeconomic Components when those conditions materially affect the evaluator's economic assessment. |
| **Constituent Evaluation Result** | The completed result of one Constituent Evaluation after any applicable Macro Adjustment. |
| **Positioning Overlay** | A post-Exposure-Evaluation adjustment to implementation willingness or intensity based on positioning context, without redefining the underlying economic assessment. |
| **Instrument Quality** | Evaluation of whether an ETF is a sufficiently good implementation vehicle for its exposure using instrument-specific characteristics supported by defined data and rules. |
| **ETF Evaluation Result** | The authoritative ETF-specific result exposed by the ETF Evaluation Module for downstream comparison or decision logic. |

A compact relationship among the major ETF Evaluation concepts is:

```text
Relevant Components
+ ETF Exposure Profile
        ↓
Core Evaluation
        ↓
Core Evaluation Result
        ↓
Macro Adjustment, where applicable
        ↓
Constituent Evaluation Result
        ↓
Evaluation Combination
        ↓
Exposure Evaluation Result
        ↓
Positioning Overlay
        ↓
Instrument Quality
        ↓
ETF Evaluation Result
```

Macro Adjustment acts on an exposure-specific Core Evaluation Result. It is not an ETF-independent market assessment performed before exposure is known.

The detailed Component sets, mappings, scales, inputs, and Result Contract semantics are defined by the relevant evaluator design and the system architecture.

## 5.2 Constituent Evaluations

| Term | Definition |
|---|---|
| **Duration Evaluation** | ETF-specific evaluation of whether the ETF's interest-rate sensitivity is appropriate under current conditions. |
| **Curve Evaluation** | ETF-specific evaluation of whether the ETF's maturity / curve exposure is appropriate under current term-structure conditions. |
| **Credit Evaluation** | ETF-specific evaluation of whether the ETF's credit-risk exposure is appropriate under current credit conditions. |
| **Rates Valuation Evaluation** | ETF-specific evaluation of whether compensation for accepting the ETF's rates exposure is sufficiently attractive. |

The current Constituent Evaluations operate as economically distinct assessments. They do not need to share identical output semantics, scales, weighting, State semantics, or Rule Mapping structures.

Macro Adjustment belongs within an applicable Constituent Evaluation rather than forming a separate peer Evaluation.

## 5.3 Positioning Overlay

Typical positioning context may include crowding, sentiment, speculative positioning, unusual directional consensus, or exposure-level extension after a large market move.

Positioning Overlay changes implementation willingness or intensity around an Exposure Evaluation Result; it does not redefine the underlying economic assessment.

## 5.4 Instrument Quality

Instrument Quality is distinct from economic attractiveness.

Examples of instrument-specific characteristics that may be evaluated when supported by defined data and rules include:

- expense ratio or implementation cost;
- tracking quality where tracking is an intended objective;
- active-management effectiveness where applicable.

Execution-specific conditions that are not modeled by Bondview are not implied to be Instrument Quality inputs merely because they affect trading in practice.

---

# 6. Diagnostics

| Term | Definition |
|---|---|
| **Diagnostics** | Analysis that explains, validates, or inspects authoritative model behavior and its dependency lineage without changing calculations, decisions, or creating a parallel analytical model. |
| **Diagnostic Result** | A non-authoritative explanatory, comparative, historical, sensitivity, traceability, visualization, or sanity-check output produced by Diagnostics. |
| **Historical Context** | Historical realizations of authoritative calculated outputs or their supporting analytical inputs used to interpret current or past model behavior. |
| **Diagnostic Comparison** | Comparison of Features, Components, Component States, ETF Exposure Profile characteristics, Core Evaluation Results, Constituent Evaluation Results, ETF Evaluation Results, or related metadata for explanatory or validation purposes. |

Historical Context is diagnostic, not a second hidden decision model.

Human-readable summaries produced by Diagnostics explain authoritative Components or evaluation results. They do not constitute a separate Bond Exposure View or other authoritative market-level assessment.

The detailed diagnostic boundary, dependency-lineage requirements, and permissible historical inspection are defined by the system architecture.

---

# 7. Model Definition and Interfaces

| Term | Definition |
|---|---|
| **Model Configuration** | The declarative definition of model-specific structure and parameters used by Bondview calculations. |
| **Configuration Schema** | The contract that validates whether Model Configuration is structurally and semantically acceptable. |
| **Resolved Model Specification** | The validated, explicit runtime representation produced from Model Configuration before calculation. |

The terms relate at a high level as:

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
| **Result Contract** | The documented semantics and required contents of a particular Result Boundary or model-significant intermediate result. |

Result Boundaries and Result Contracts define how authoritative outputs are exposed across responsibility boundaries and how model-significant intermediate results remain interpretable and traceable. Concrete result objects are defined individually when their contracts are designed.

---

# 8. Naming Principles

1. Prefer semantic names over numbered names.
2. Use **Module** only for major system responsibilities with meaningful boundaries.
3. Use **Capability** for reusable implementation behavior.
4. Keep **Raw Observation**, **Feature**, and **Component** distinct.
5. Keep **Component Value** and **Component State** distinct where a discrete State exists.
6. Treat **Component** as the authoritative reusable analytical concept.
7. A Component may be derived from Features or from other Components / Component Values when economically meaningful.
8. Use **Bond Exposure Dimension** only as descriptive vocabulary for economically distinct exposure dimensions such as Duration, Curve, and Credit.
9. Do not use **Bond Exposure View**, **Duration View**, **Curve View**, or **Credit View** as model-result terms.
10. Use **Constituent Evaluation** for one economically distinct ETF-specific evaluation within Exposure Evaluation.
11. Use **Core Evaluation** for the exposure-specific pre-Macro-Adjustment assessment within a Constituent Evaluation.
12. Use **Core Evaluation Result** for the explicit intermediate result produced by Core Evaluation.
13. Use **Macro Adjustment** for evaluator-specific macro modification of an already exposure-specific Core Evaluation Result.
14. Use **Constituent Evaluation Result** for the completed result of one Constituent Evaluation.
15. Use **Exposure Evaluation** for the combined economic assessment of an ETF's exposure.
16. Use **Positioning Overlay** for post-economic-evaluation positioning adjustment to implementation willingness or intensity.
17. Use **Instrument Quality** only for implementation quality, not for economic attractiveness.
18. Use **ETF Evaluation Result** for the authoritative ETF-specific output exposed by ETF Evaluation.
19. Use **Rule Case**, **Rule Mapping**, **Rule Table**, and **Coverage Strategy** as general Calculation Mechanics.
20. Use **Result Boundary / Result Contract** as generic interface concepts while defining concrete results separately.
