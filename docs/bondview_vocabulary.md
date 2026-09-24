# Bondview Vocabulary

## Purpose

This document defines the canonical vocabulary for **Bondview**.

Its purpose is to provide a consistent set of terms for describing how Bondview represents bond-market and macroeconomic conditions, evaluates ETF exposures, and explains model behavior.

This document is the source of truth for **term meaning and naming**. `bondview_system_architecture.md` is the source of truth for **system structure, ownership, dependency direction, processing flow, and Result Boundaries**.

The definitions below may include compact conceptual relationships where those relationships are necessary to distinguish terms, but they do not prescribe detailed implementation structure.

---

# 1. System Responsibilities

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

# 2. Analytical Concepts

## 2.1 Component Model

| Term | Definition |
|---|---|
| **Raw Observation** | An accepted source observation used by Bondview. |
| **Feature** | A quantitative measure derived from Raw Observations for model use. |
| **Component** | A canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State. |
| **Component Value** | The calculated quantitative or structured representation of a Component before discrete classification. |
| **Component State** | A discrete economic condition assigned to a Component when discrete classification is useful. |
| **Bond Exposure Dimension** | A principal economically distinct aspect of bond exposure used to organize evaluation questions. Current examples include Duration, Curve, and Credit. |

A Feature is generally closer to calculation mechanics, while a Component represents an economically meaningful analytical concept intended for authoritative reuse.

The normal relationship is:

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
[State Classification, where applicable]
        ↓
Component State
```

A Component may be derived from Features or from other Components or Component Values when economically meaningful.

A Component's upstream representation is uniform across the architecture, but its downstream economic role is consumer-specific. For example, one evaluator may use selected Components for Core Evaluation and other Components for Macro Adjustment.

A Duration example illustrates the distinction among the terms:

| Example | Vocabulary role |
|---|---|
| observed 10Y Treasury yields | Raw Observations |
| yield change over a defined horizon | Feature |
| Long-End Yield Trend | Component |
| calculated trend measure | Component Value |
| Falling / Stable / Rising | Component State |
| Duration | Bond Exposure Dimension |

A Bond Exposure Dimension is descriptive vocabulary. It is not a separate calculated result and does not imply an ETF-independent Bond Exposure View.

Detailed Component construction, identity, consolidation, lineage, and Result Contract rules belong to the system architecture and more specific Component design documents.

## 2.2 Calculation Mechanics

Calculation Mechanics are reusable conceptual structures used across Components and ETF Evaluation and may also be inspected by Diagnostics.

| Term | Definition |
|---|---|
| **State Classification** | The process that converts a Component Value into a Component State. |
| **Rule Dimension** | A Component whose State participates in a particular Rule Case. |
| **Rule Case** | One concrete combination of Rule Dimension States. |
| **Rule Mapping** | The defined relationship that maps a Rule Case to a model result. |
| **Rule Table** | The configured set of Rule Mappings for one defined model purpose. |
| **Coverage Strategy** | The convention for handling the valid Rule Case space, such as explicit mapping, fallback, or justified interpolation. |

State Classification acts on one Component Value:

```text
Long-End Yield Trend Value = -45 bp
        ↓
[State Classification]
        ↓
Long-End Yield Trend State = Falling
```

Rule Mapping acts on a combination of Component States:

```text
Long-End Yield Trend State = Falling
        +
Recent Long-End Yield Move State = Falling
        ↓
Rule Case = Falling × Falling
        ↓
[Rule Mapping]
        ↓
Mapped Result = Very favorable for long-duration exposure
```

This is an illustrative mapping for a long-duration exposure, not an ETF-independent Duration judgment; the same Component States may map differently for materially different ETF duration profiles.

The distinction is:

```text
State Classification
→ What State represents this Component Value?

Rule Mapping
→ What result follows from this combination of Component States?
```

Reusable mechanics do not erase model semantics. Where a model assigns different roles such as Core Evaluation and Macro Adjustment, those roles remain distinct even if both stages use similar mechanics.

---

# 3. ETF Evaluation

## 3.1 Exposure Evaluation

| Term | Definition |
|---|---|
| **ETF Exposure Profile** | The economic identity of the bond exposure that an ETF is designed to provide. |
| **Exposure Evaluation** | The economic assessment process that determines whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions. |
| **Constituent Evaluation** | An ETF-specific evaluation of one economically distinct aspect of an ETF's Exposure Profile within Exposure Evaluation. |
| **Core Evaluation** | The exposure-specific economic assessment within a Constituent Evaluation before any applicable Macro Adjustment. It combines Components for Core Evaluation with the applicable ETF Exposure Profile. |
| **Core Evaluation Result** | The exposure-specific result of Core Evaluation before any applicable Macro Adjustment. |
| **Macro Adjustment** | An evaluator-specific modification of an already exposure-specific Core Evaluation Result using Macroeconomic Components when those conditions materially affect the evaluator's economic assessment. |
| **Constituent Evaluation Result** | The completed result of one Constituent Evaluation after any applicable Macro Adjustment. |
| **Exposure Evaluation Result** | The combined economic result produced from Constituent Evaluation Results before Positioning Overlay. |

The terms inside each Constituent Evaluation relate as follows:

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

Core Evaluation first interprets the ETF exposure under the Components used for that evaluator. Macro Adjustment then modifies that already exposure-specific result using applicable Macroeconomic Components.

For example, a Duration Evaluation may use `Long-End Yield Trend` and `Recent Long-End Yield Move` as Components for Core Evaluation together with duration characteristics from the ETF Exposure Profile. `Inflation Trend` and `Policy Direction` may then serve as Macroeconomic Components for Macro Adjustment. This example illustrates term roles rather than prescribing the Duration model's final rule mapping.

The current Constituent Evaluations are:

| Term | Definition |
|---|---|
| **Duration Evaluation** | ETF-specific evaluation of whether the ETF's interest-rate sensitivity is appropriate under current conditions. |
| **Curve Evaluation** | ETF-specific evaluation of whether the ETF's maturity / curve exposure is appropriate under current term-structure conditions. |
| **Credit Evaluation** | ETF-specific evaluation of whether the ETF's credit-risk exposure is appropriate under current credit conditions. |
| **Rates Valuation Evaluation** | ETF-specific evaluation of whether compensation for accepting the ETF's rates exposure is sufficiently attractive. |

The Constituent Evaluations are economically distinct assessments. They do not need to share identical output semantics, scales, weighting, State semantics, or Rule Mapping structures.

After the Constituent Evaluations are complete:

```text
Constituent Evaluation Results
        ↓
[Evaluation Combination]
        ↓
Exposure Evaluation Result
```

`Evaluation Combination` is an action in the evaluation flow rather than a separate canonical vocabulary term.

## 3.2 Positioning and Instrument Quality

| Term | Definition |
|---|---|
| **Positioning Overlay** | Adjusts implementation willingness or intensity based on positioning context after Exposure Evaluation. |
| **Instrument Quality** | Assesses whether an ETF is a suitable implementation vehicle for its exposure. |
| **ETF Evaluation Result** | The authoritative ETF-specific result exposed for downstream comparison or decision logic. |

The terms relate as follows:

```text
Exposure Evaluation Result
        ↓
[Positioning Overlay] <──────────── Positioning Inputs
        ↓
[Instrument Quality] <───────────── Instrument Quality Inputs
        ↓
ETF Evaluation Result
```

**Positioning Overlay** changes implementation willingness or intensity around the Exposure Evaluation Result rather than changing the underlying economic assessment. Typical positioning context may include crowding, sentiment, speculative positioning, unusual directional consensus, or exposure-level extension after a large market move. For example, an economically favorable very-long-duration exposure could still be implemented less aggressively when bullish duration positioning is unusually crowded.

**Instrument Quality** is distinct from economic attractiveness. It asks whether the ETF is a suitable vehicle for the evaluated exposure. Relevant characteristics may include expense ratio, tracking quality where tracking is an intended objective, and active-management effectiveness where applicable. For example, two ETFs with similar duration exposure may have similar economic evaluation but differ in Instrument Quality because of cost or tracking behavior.

The intermediate result after Positioning Overlay is intentionally unnamed because Bondview does not currently need to refer to it independently.

---

# 4. Diagnostics

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

# 5. Model Definition and Interfaces

| Term | Definition |
|---|---|
| **Model Configuration** | The declarative definition of model-specific structure and parameters used by Bondview calculations. |
| **Configuration Schema** | The contract that validates whether Model Configuration is structurally and semantically acceptable. |
| **Resolved Model Specification** | The validated, explicit runtime representation produced from Model Configuration before calculation. |
| **Result Boundary** | A formal interface through which one responsibility exposes authoritative outputs to downstream consumers. |
| **Result Contract** | The documented semantics and required contents of a particular Result Boundary or model-significant intermediate result. |

The configuration terms relate at a high level as:

```text
Model Configuration
        ↓
[Configuration Validation]
        ↓
Resolved Model Specification
```

Result Boundaries and Result Contracts define how authoritative outputs are exposed across responsibility boundaries and how model-significant intermediate results remain interpretable and traceable. Concrete result objects are defined individually when their contracts are designed.

---

# 6. Naming Principles

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
12. Use **Core Evaluation Result** for the exposure-specific result before any applicable Macro Adjustment.
13. Use **Macro Adjustment** for evaluator-specific macro modification of an already exposure-specific Core Evaluation Result.
14. Use **Constituent Evaluation Result** for the completed result of one Constituent Evaluation.
15. Use **Exposure Evaluation Result** for the combined economic result before Positioning Overlay.
16. Use **Positioning Overlay** for post-economic-evaluation positioning adjustment to implementation willingness or intensity.
17. Use **Instrument Quality** only for implementation quality, not for economic attractiveness.
18. Use **ETF Evaluation Result** for the authoritative ETF-specific output exposed by ETF Evaluation.
19. Use **Rule Case**, **Rule Mapping**, **Rule Table**, and **Coverage Strategy** as general Calculation Mechanics.
20. Use **Result Boundary / Result Contract** as generic interface concepts while defining concrete results separately.
