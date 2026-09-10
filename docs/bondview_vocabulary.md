# Bondview Vocabulary

## Purpose

This document defines the current canonical working vocabulary for **Bondview v2**.

The objective is to keep conceptual design, documentation, configuration, labels, implementation discussions, and future file/API naming consistent. The vocabulary may evolve as the model is refined, but these terms should be preferred unless a later design decision explicitly replaces them.

Definitions and diagrams in this document describe conceptual meaning and terminology rather than prescribing implementation structure.

`bondview-v2` is the current project/repository name. Once it replaces the previous project, the intended system name is **Bondview**.

---

## 1. Vocabulary Map

The map is a compact guide to the major vocabulary areas defined in this document.

```text
Bondview
│
├── System and Architecture
│   ├── Modules
│   └── Processing Structure
│
├── Component-State Structure
│   ├── Market Component
│   └── Macro Component
│
├── Rule Mapping
│   ├── Stance Rule Case → Core Stance
│   └── Constraint Rule Case → Constraint Action
│
├── Stance and Constraint Integration
│
├── ETF Selection
│
├── Diagnostics
│
└── Model Definition / Interfaces
```

---

## 2. System and Architecture Terms

| Term | Definition | Notes |
|---|---|---|
| **Bondview** | The complete bond-ETF decision-support system. | Current development project: `bondview-v2`. |
| **Module** | A major system responsibility with a meaningful input/output boundary. | Prefer semantic names rather than numbered names such as `Module 1`. |
| **Stage** | A semantic processing step within a module flow. | A stage does not imply a separate Python file/class. |
| **Capability** | A defined implementation behavior that performs an operation and may be reused wherever the same semantics are required. | Reuse does not require the word `shared` in the capability name. |
| **Stance Calculation Module** | Produces Duration, Curve, and Credit stances from market-derived conditions and stance-specific macro constraints. | Owns stance logic. |
| **ETF Selection Module** | Evaluates how the Bond-Exposure Stance Set maps to investable ETFs and whether specific instruments justify selection. | Does not recreate stance logic. |
| **Diagnostics Module** | Inspects and explains calculated model behavior through comparison, historical context, visualization, and reporting. | Must not alter authoritative model behavior. |

### Stage vs Capability

```text
Stage
= where an operation belongs in a conceptual flow

Capability
= implementation behavior that performs an operation
  and can be reused by multiple consumers
```

---

## 3. Component-State Structure

### 3.1 Core Concepts

The Component / Value / State vocabulary applies to both the market-derived side of stance calculation and the macro side of constraint calculation.

| Term | Definition | Example |
|---|---|---|
| **Raw Observations** | Accepted source observations used by Bondview, normally historical time-series data. | Treasury-yield history, CPI history, credit-spread history |
| **Feature** | A quantitative measure derived from Raw Observations for model use. | spread percentile, yield change, inflation-trend measure |
| **Component** | An economically meaningful model concept represented by a model-ready value and, where required, classified into a discrete state. | spread level, long-end yield trend, inflation trend |
| **Market Component** | A bond-market-derived Component whose state may contribute to stance calculation. | spread level, recent long-end yield move |
| **Macro Component** | A macroeconomic Component whose state may contribute to stance-specific constraint logic. | inflation trend, policy direction, growth |
| **Component Value** | The calculated quantitative or model-ready representation of a Component before discrete classification. | spread percentile = 87 |
| **Component State** | The discrete economic condition assigned to a Component. | wide, tightening, rising, easing |
| **State Classification** | The process that converts a Component Value or other model-ready representation into a Component State. | spread percentile 87 → `wide` |

### 3.2 Component-State Derivation Flow

```text
Raw Observations
        ↓
[Feature Calculation]
        ↓
Feature
        ↓
[Component Calculation]
        ↓
Component Value
        ↓
[State Classification]
        ↓
Component State
```

The same vocabulary applies whether the resulting Component State belongs to a Market Component or a Macro Component.

```text
Component
├── Market Component
└── Macro Component
```

Not every model path must physically contain every conceptual step. A Feature may directly represent a Component Value when no additional Component Calculation is required.

---

## 4. Rule Mapping

Rule-case construction is a general model structure. Market and Macro Components may independently contribute states to Rule Cases. Each Rule Case should represent a joint state with an economically meaningful interpretation.

### 4.1 General rule-case structure

```text
Component States
        ↓
[Rule-Case Construction]
        ↓
Rule Case
        ↓
[Rule Mapping]
        ↓
Mapped Result
```

| Term | Definition |
|---|---|
| **Rule Dimension** | A Component whose State participatesin a Rule Case |
| **Rule Case** | One concrete combination of Rule-Dimension states. |
| **Rule Mapping** | The operation or defined relationship that maps a Rule Case to a model result. |
| **Rule Table** | The configured set of Rule Mappings for a defined model purpose. |
| **Coverage Strategy** | The convention for handling the valid rule space, such as complete explicit mapping, explicit cases plus fallback, or justified interpolation. |

### 4.2 Stance and Constraint Rule Cases

A **Stance Rule Case** is constructed from **Market Component States**, and **Stance Rule Mapping** maps that Rule Case to a **Core Stance**.

A **Constraint Rule Case** is constructed from **Macro Component States**, and **Constraint Rule Mapping** maps that Rule Case to a **Constraint Action**.

The existence of a Constraint Rule Case does not imply that every stance must have a macro Rule Table. A stance may have no Macro Constraint, and a constraint model may use explicit cases plus a pass-through fallback rather than a complete Cartesian table.

---

## 5. Stance and Constraint Integration

This section defines how the Core Stance and Constraint Action combine through Constraint Application to produce the authoritative Final Stance.

| Term | Definition | Example |
|---|---|---|
| **Stance** | An analytical view about one dimension of bond exposure. | Duration stance, Curve stance, Credit stance |
| **Core Stance** | The market-derived Stance produced from Stance Rule Mapping before Macro Constraint application. | positive Credit |
| **Constraint Action** | The stance-specific action selected from macro rules for application to a Core Stance. | pass-through, weaken, cap positive magnitude |
| **Macro Constraint** | The umbrella concept for stance-specific macro-based constraint logic and its application to a Core Stance. | rising inflation + tightening policy caps positive Duration |
| **Bond-Exposure Stance Set** | The combined final Duration, Curve, and Credit outputs consumed by ETF Selection. | Preserves the three Stances rather than collapsing them into one aggregate score. |

### 5.1 Integration Flow

```text
Core Stance
     +
Constraint Action
        ↓
[Constraint Application]
        ↓
Final Stance
```

`Macro Constraint` is the umbrella concept for stance-specific constraint logic based on Macro Components and its application to the Core Stance.

Typical Constraint Actions may include:

```text
pass-through
strengthen
weaken
magnitude cap
directional restriction
hard rejection
```

### 5.2 Constraint Rules vs Constraint Application

Constraint Rule Mapping answers:

```text
Which Constraint Action applies under this Constraint Rule Case?
```

Constraint Application answers:

```text
How is that action applied to the supplied Core Stance?
```

One Constraint Rule Case does not require a separate table entry for every possible Core Stance when the selected Constraint Action has well-defined application semantics.


---

## 6. ETF Selection

| Term | Definition |
|---|---|
| **ETF Universe** | The set of ETFs eligible for exposure-fit evaluation. |
| **Exposure Profile** | The bond exposure represented by an ETF, such as duration/maturity, curve segment, credit exposure, underlying market, and relevant currency/hedging characteristics. |
| **Exposure Fit** | The degree to which an ETF's Exposure Profile expresses the Bond-Exposure Stance Set. |
| **Instrument Evaluation** | Evaluation of ETF-specific attractiveness after Exposure Fit, including relevant yield/carry, price behavior, fees, liquidity, tracking, hedging/currency structure, and alternatives. |
| **ETF Selection** | The process that determines which evaluated ETFs remain preferred. |

```text
ETF Universe
        +
Bond-Exposure Stance Set
        ↓
[Exposure Fit Evaluation]
        ↓
[Instrument Evaluation]
        ↓
[ETF Selection]
```
---

## 7. Diagnostics

| Term | Definition |
|---|---|
| **Diagnostics** | Analysis that explains or inspects authoritative model behavior without changing the model's calculations or decisions. |
| **Historical Context** | Historical observations of authoritative calculated model outputs used to interpret current or past model behavior. |
| **Diagnostic Comparison** | Comparison of calculated Features, Components, Component States, Stances, or related metadata for explanatory purposes. |

Historical Context is explanatory, not a second hidden model.

```text
Authoritative Calculated Outputs
        ↓
[Historical Context Preparation]
        ↓
Historical Context
        ↓
Diagnostics / Visualization / Reporting
```

---

## 8. Model Definition and Interface

| Term | Definition |
|---|---|
| **Model Configuration** | The declarative definition of model-specific structure and parameters consumed by Bondview calculation, currently represented in YAML. |
| **Configuration Schema** | The contract that validates whether Model Configuration is structurally and semantically acceptable. |
| **Resolved Model Specification** | The validated, explicit runtime representation produced from Model Configuration before calculation. |
| **Result Boundary** | A formal interface through which one responsibility exposes authoritative outputs to downstream consumers. |
| **Result Contract** | The documented semantics and required contents of a particular Result Boundary. |

Conceptually:

```text
Model Configuration (YAML)
        ↓
Configuration Schema
        ↓
Resolved Model Specification
        ↓
Runtime Calculation
        ↓
Result Boundary
```

Concrete result objects should be defined individually when their contracts are designed rather than forcing all modules into one generic result class.

---

## 9. Naming Principles

1. Prefer semantic names over numbered names.
2. Use **Module** for major system responsibilities.
3. Use **Stage** for semantic positions in a processing flow.
4. Use **Capability** for implementation behavior.
5. Do not add `shared` to a capability name merely because it has multiple consumers.
6. Reuse authoritative capabilities and outputs when equivalent semantics already exist.
7. Keep **Feature**, **Component**, **Component Value**, and **Component State** distinct.
8. Use **Market Component** and **Macro Component** for the two input domains, and use **Component Value** and **Component State** consistently for both.
10. Use **Rule Case** as the general concept; use **Stance Rule Case** or **Constraint Rule Case** when the processing role matters.
11. Use **Macro Constraint** as the umbrella concept for stance-specific macro rule interpretation and Constraint Application rather than introducing a universal macro stance/score.
12. Keep **Constraint Rule Mapping** conceptually separate from **Constraint Application**: economic rules choose the action; application mechanics execute it against the Core Stance.
13. Treat **Bond-Exposure Stance Set** as the formal collection of final Duration, Curve, and Credit outputs.
14. Use **Result Boundary / Result Contract** as generic interface concepts, while defining concrete result structures separately.
