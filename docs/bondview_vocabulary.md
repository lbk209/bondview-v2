# Bondview Vocabulary

## Purpose

This document defines the current canonical working vocabulary for **Bondview v2**.

The objective is to keep conceptual design, documentation, configuration, labels, implementation discussions, and future file/API naming consistent. The vocabulary may evolve as the model is refined, but these terms should be preferred unless a later design decision explicitly replaces them.

Definitions and diagrams in this document describe conceptual meaning and terminology rather than prescribing implementation structure.

`bondview-v2` is the current project/repository name. Once it replaces the previous project, the intended system name is **Bondview**.


---

## 1. Vocabulary Map

```text
Bondview
│
├── Modules
│   ├── Stance Calculation Module
│   ├── ETF Selection Module
│   └── Diagnostics Module
│
├── Processing Structure
│   ├── Stage
│   └── Capability
│
├── Stance Model
│   ├── Raw Observations
│   ├── Feature
│   ├── Component
│   ├── Component Value
│   ├── State
│   ├── Rule Case
│   ├── Core Stance
│   ├── Macro Constraint
│   └── Final Stance
│
├── ETF Selection
│   ├── ETF Universe
│   ├── Exposure Profile
│   ├── Stance Fit
│   ├── Instrument Evaluation
│   └── ETF Selection
│
└── Model Definition / Interfaces
    ├── Model Configuration
    ├── Configuration Schema
    ├── Resolved Model Specification
    ├── Result Boundary
    └── Result Contract
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
| **ETF Selection Module** | Evaluates how the bond-exposure stance set maps to investable ETFs and whether specific instruments justify selection. | Does not recreate stance logic. |
| **Diagnostics Module** | Inspects and explains calculated model behavior through comparison, historical context, visualization, and reporting. | Must not alter authoritative model behavior. |

### Stage vs Capability

```text
Stage
= where an operation belongs in a conceptual flow

Capability
= implementation behavior that performs an operation
  and can be reused by multiple consumers
```

Example:

```text
State Classification Stage
        ↓
uses
        ↓
State Classification capability
        ↑
may also be reused elsewhere
```

---

## 3. Stance Model

### 3.1 Core hierarchy

| Term | Definition | Example |
|---|---|---|
| **Stance** | An analytical view about one dimension of bond exposure. | Credit stance |
| **Stance Type** | The exposure dimension analyzed by a stance. | Duration, Curve, Credit |
| **Feature** | A quantitative measure derived from raw observations for model use. | spread percentile, yield change |
| **Component** | An economically meaningful concept that a stance reasons about. | spread level, long-end yield trend |
| **Component Value** | The calculated quantitative or model-ready value representing a component before discrete classification. | spread percentile = 87 |
| **Component State** | A discrete economic condition assigned to a component or other classified concept. | wide, inverted, falling |
| **State Classification** | The process that converts a component value or other model-ready input into a discrete state used downstream. | 87th spread percentile → `wide` |
| **Rule Case** | A specific combination of component states whose joint condition has economic meaning. | `wide + tightening` |
| **Rule Mapping** | The mapping from a rule case to a core stance. | `wide + tightening → positive Credit` |
| **Core Stance** | The market-derived stance produced before macro constraints are applied. | positive Credit |
| **Macro Constraint** | Stance-specific macro logic that modifies how strongly or in what direction the core stance may be expressed. | weakening growth caps positive Credit |
| **Final Stance** | The authoritative stance after applicable macro constraints and required final processing. | constrained positive Credit |
| **Bond-Exposure Stance Set** | The combined final Duration, Curve, and Credit outputs consumed by ETF selection. | Preserves the three stances rather than collapsing them into one aggregate score. |

### 3.2 Raw Observations → Feature → Component → State

These terms should remain distinct because they answer different questions.

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
| Concept | Question it answers | Typical form |
|---|---|---|
| **Raw Observations** | What source data do we have? | Historical Treasury yields, CPI history, credit-spread history |
| **Feature** | What quantitative information did we derive from the data? | 60-day yield change, spread percentile |
| **Component** | What economic concept does the stance reason about? | spread level, yield trend |
| **Component State** | What condition is that concept currently in? | wide, falling, inverted |

Not every implementation path must physically contain every step. A feature may directly represent a component value when no additional calculation is required.

### 3.3 Raw Observations

**Raw Observations** means accepted source observations used by Bondview, normally historical time-series data rather than only a single current point.

```text
DGS10 historical series
CPI historical series
credit-spread historical series
```

An individual dated value is still an **observation**, but architectural flows should normally use the plural term **Raw Observations**.

---

## 4. Rule Mapping

```text
Component States
        ↓
[Rule-Case Construction]
        ↓
Rule Case
        ↓
[Rule Mapping]
        ↓
Core Stance
```

| Term | Definition |
|---|---|
| **Rule Dimension** | A component/state axis that participates in rule-case construction. |
| **Rule Case** | One concrete combination of rule-dimension states. |
| **Rule-Case Construction** | The process that assembles the relevant component states into a rule case. |
| **Rule Mapping** | The operation or defined relationship that maps a rule case to a core stance. |
| **Rule Table** | The configured set of rule mappings for a stance. |
| **Coverage Strategy** | The stance-specific convention for handling the valid rule space, such as complete explicit mapping, explicit cases plus fallback, or justified interpolation. |

Example:

```text
spread level       = wide
spread direction   = tightening
        ↓
Rule Case          = wide + tightening
        ↓
Rule Mapping
        ↓
Core Credit Stance = positive
```

---

## 5. Macro Constraint

```text
Macro Condition
        ↓
[State Classification]
        ↓
Macro State 
        + 
Core Stance
        ↓
[Macro Constraint]
        ↓
Final Stance
```

| Term | Definition |
|---|---|
| **Macro Condition** | A macroeconomic concept relevant to a particular stance. |
| **Macro State** | The classified current condition of a macro concept. |
| **Macro Constraint** | Stance-specific logic that modifies the expression of a core stance based on relevant macro states. |

Typical constraint effects may include leaving the core stance unchanged, strengthening or weakening it, capping magnitude, restricting direction, or applying a deliberately justified hard rejection.

Macro information is not assumed to have one universal bond implication. The same macro condition may affect Duration, Curve, and Credit differently.

---

## 6. ETF Selection

```text
Bond-Exposure Stance Set
          +
      ETF Universe
          ↓
Candidate Preparation
          ↓
Exposure Fit Evaluation
          ↓
Instrument Evaluation
          ↓
ETF Selection
```

| Term | Definition |
|---|---|
| **ETF Universe** | The investable ETFs eligible for evaluation. |
| **Candidate ETF** | An ETF currently under consideration in the selection process. |
| **Exposure Profile** | The bond exposure represented by an ETF, such as duration/maturity, curve segment, credit exposure, underlying market, and relevant currency/hedging characteristics. |
| **Stance Fit** | The degree to which an ETF's exposure profile expresses the Bond-Exposure Stance Set. |
| **Instrument Evaluation** | Evaluation of ETF-specific attractiveness after exposure fit, including relevant yield/carry, price behavior, fees, liquidity, tracking, hedging/currency structure, and alternatives. |
| **ETF Selection** | The process that determines which evaluated ETFs remain preferred candidates. |

---

## 7. Diagnostics

| Term | Definition |
|---|---|
| **Diagnostics** | Analysis that explains or inspects authoritative model behavior without changing the model's calculations or decisions. |
| **Historical Context** | Historical observations of authoritative calculated model outputs used to interpret current or past model behavior. |
| **Historical Context Preparation** | The capability that prepares reusable historical context from authoritative outputs or accepted historical inputs. |
| **Diagnostic Comparison** | Comparison of calculated features, components, states, stances, or related metadata for explanatory purposes. |

Historical Context is explanatory, not a second hidden model.

```text
Authoritative Calculated Outputs
        ↓
Historical Context Preparation
        ↓
Historical Context
        ↓
Diagnostics / Visualization / Reporting
```

---

## 8. Model Definition and Interface

| Term | Definition |
|---|---|
| **Model Configuration** | The declarative definition of model-specific structure and parameters consumed by Bondview calculation. |
| **YAML** | The current serialization/representation format for Model Configuration; not itself the architectural concept. |
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
7. Keep **Feature**, **Component**, and **State** distinct.
8. Use **Macro Constraint** for stance-specific macro effects rather than introducing a universal macro stance/score without a separate justification.
9. Treat **Bond-Exposure Stance Set** as the formal collection of final Duration, Curve, and Credit outputs.
10. Use **Result Boundary / Result Contract** as generic interface concepts, while defining concrete result structures separately.
