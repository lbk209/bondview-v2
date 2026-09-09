# Working Architecture Concepts for Bondview v2

> **Status: Working document.**
>
> This document captures the current architectural direction derived during terminology design. It is not an authoritative replacement for `docs/bondview_system_architecture.md`. The system architecture remains foundational, and more specific v2 design documents take precedence where applicable.

## 1. Purpose

This document organizes the current working architecture around three concepts:

- **Module** — major system responsibility;
- **Stage** — semantic processing step inside a module;
- **Capability** — implementation behavior that may be reused wherever equivalent semantics are required.

The goal is to make conceptual architecture clear without prematurely forcing each stage into a separate Python class, file, package, or abstraction layer.

---

## 2. Module Structure

The current working module set is:

```text
Bondview
│
├── Stance Calculation Module
│
├── ETF Selection Module
│
└── Diagnostics Module
```

### 2.1 Stance Calculation Module

Responsibility:

> Produce Duration, Curve, and Credit stances from market-derived components, then apply the macro constraints relevant to each stance.

It owns:

- stance-specific components;
- component/state interpretation;
- rule-case construction;
- rule mapping;
- core stance calculation;
- stance-specific macro constraints;
- final stance outputs;
- construction of the Bond-Exposure Stance Set.

It does **not** own ETF-specific instrument evaluation.

### 2.2 ETF Selection Module

Responsibility:

> Map the Bond-Exposure Stance Set to investable ETFs and determine whether specific instruments express the desired exposure appropriately and are attractive enough to select.

It owns:

- ETF universe/candidate handling;
- exposure-profile interpretation;
- stance-fit evaluation;
- instrument-level evaluation;
- final ETF selection.

It consumes stance outputs rather than recreating Duration, Curve, or Credit logic.

### 2.3 Diagnostics Module

Responsibility:

> Explain and inspect authoritative Bondview model behavior through comparison, historical context, visualization, and reporting.

It may consume:

- features;
- component values;
- component states;
- rule cases;
- core stances;
- macro-constraint effects;
- final stances;
- stance scores/labels where applicable;
- result metadata.

Diagnostics must remain explanatory rather than decision-changing.

---

## 3. Stage vs Capability

### Stage

A **Stage** is a semantic position in a module's processing flow.

Examples:

```text
Feature Calculation Stage
Component Calculation Stage
State Classification Stage
Rule Mapping Stage
Instrument Evaluation Stage
```

### Capability

A **Capability** is an implementation behavior with a defined semantic contract.

Examples:

```text
Feature Calculation capability
Component Calculation capability
State Classification capability
State Stabilization capability
Historical Context Preparation capability
```

A capability may be used by several stages or consumers.

```text
                     ┌── Duration path
                     │
Classification capability
                     │
                     ├── Credit path
                     │
                     └── Macro condition preparation
```

The capability name describes **what it does**, not whether it is shared.

### Architectural rule

```text
Stage
≠ necessarily one Python file/class

Capability
≠ necessarily one consumer

Reuse
≠ reason to add "shared" to the name
```

---

## 4. Stance Calculation Module — Working Stage Flow

The following is a semantic flow, not a requirement that every model path physically implement every box.

```text
Raw Observations
        ↓
Feature Calculation
        ↓
Features
        ↓
Component Calculation
        ↓
Component Values
        ↓
State Classification
        ↓
Component States
        ↓
Rule-Case Construction
        ↓
Rule Mapping
        ↓
Core Stance
        ↓
Macro Constraint
        ↓
Final Stance
```

A feature may directly represent a component value where no distinct component-calculation operation is needed.

### Stance structure

```text
┌─────────────────────────────────────┐
│ Stance                              │
│                                     │
│ Type: Duration / Curve / Credit     │
│                                     │
│ Components                          │
│      ↓                              │
│ Component States                    │
│      ↓                              │
│ Rule Case                           │
│      ↓                              │
│ Rule Mapping                        │
│      ↓                              │
│ Core Stance                         │
│      ↓                              │
│ Macro Constraint                    │
│      ↓                              │
│ Final Stance                        │
└─────────────────────────────────────┘
```

Curve may legitimately have no applicable macro constraint; in that case the no-constraint path should be treated as normal pass-through behavior rather than an exceptional workaround.

### Combined stance output

```text
Duration Final Stance
        +
Curve Final Stance
        +
Credit Final Stance
        ↓
Bond-Exposure Stance Set
```

The set preserves the three stances as separate analytical outputs.

---

## 5. ETF Selection Module — Working Stage Flow

A compact four-stage structure is sufficient for the current design.

```text
Bond-Exposure Stance Set
          +
      ETF Universe
          ↓
1. Candidate Preparation
          ↓
2. Exposure Fit Evaluation
          ↓
3. Instrument Evaluation
          ↓
4. Selection
          ↓
ETF Selection Result
```

### 5.1 Candidate Preparation

Purpose:

> Establish which ETFs are eligible and resolve the exposure characteristics required for evaluation.

Likely concepts:

- ETF Universe;
- Candidate ETF;
- Exposure Profile;
- underlying market identity;
- maturity/duration exposure;
- curve segment;
- credit exposure;
- investor-currency or hedging characteristics where relevant.

### 5.2 Exposure Fit Evaluation

Purpose:

> Determine whether an ETF expresses the exposure favored by the Bond-Exposure Stance Set.

Primary output concept:

- **Stance Fit**

This stage answers:

```text
"What bond exposure is favored?"
        ↓
"Does this ETF actually express it?"
```

### 5.3 Instrument Evaluation

Purpose:

> Determine whether the particular ETF is attractive enough after exposure fit is established.

Potential evaluation inputs include:

- yield or carry;
- price behavior;
- fees;
- liquidity;
- tracking/index characteristics;
- currency/hedging effects;
- relevant low-risk or risk-free alternatives.

Price behavior belongs here initially rather than requiring a separate top-level module or stage.

### 5.4 Selection

Purpose:

> Apply the ETF-selection contract to the evaluated candidates and produce the formal selection output.

The exact ranking/filtering/selection mechanics remain to be designed.

---

## 6. Diagnostics Module — Working Stage Flow

```text
Authoritative Calculated Outputs
        ↓
Diagnostic Comparison
        ↓
Historical Context
        ↓
Visualization / Reporting
```

This is not necessarily a strict runtime sequence. Historical Context may feed comparisons or visualization directly.

### Historical Context

Historical Context belongs inside Diagnostics for now because its role is explanatory.

```text
Current model output
        +
Historical model history
        ↓
Interpretation
```

Examples:

- how a component has evolved;
- how often a state has occurred;
- how the current rule case compares with earlier periods;
- how core and final stances differed historically after macro constraints.

Historical Context must not become a separately reimplemented stance model.

### Historical Context Preparation

When historical context requires preparation, use the **Historical Context Preparation capability**.

The capability should prepare historical material from authoritative calculations or accepted inputs. If later diagnostics need the same semantics, they should reuse that capability rather than recreate equivalent logic.

---

## 7. Reuse Principle

The central lesson from previous implementation cleanup is not "create a shared module."

It is:

> **If an authoritative capability or derived output with the required semantics already exists, later consumers reuse it rather than implement equivalent logic independently.**

Example:

```text
Historical Context Preparation exists
        ↓
new diagnostic needs the same historical context
        ↓
reuse existing capability
```

Not:

```text
new diagnostic
        ↓
implement almost-identical historical preparation
        ↓
two competing implementations
```

The same rule applies to:

- Feature Calculation;
- Component Calculation;
- State Classification;
- State Stabilization;
- Rule Mapping mechanics;
- Historical Context Preparation;
- other capabilities once equivalent reuse is demonstrated.

---

## 8. Architecture Overview

```text
BONDVIEW
│
├── Stance Calculation Module
│
│      Raw Observations
│             ↓
│      Feature Calculation
│             ↓
│          Features
│             ↓
│      Component Calculation
│             ↓
│      Component Values
│             ↓
│      State Classification
│             ↓
│      Component States
│             ↓
│      Rule-Case Construction
│             ↓
│        Rule Mapping
│             ↓
│
│      ┌─────────────────────────────┐
│      │ Stance                      │
│      │ Type: Duration/Curve/Credit │
│      │                             │
│      │ Core Stance                 │
│      │      ↓                      │
│      │ Macro Constraint            │
│      │      ↓                      │
│      │ Final Stance                │
│      └─────────────────────────────┘
│
│      Duration + Curve + Credit
│             ↓
│      Bond-Exposure Stance Set
│
├── ETF Selection Module
│
│      Bond-Exposure Stance Set
│              +
│          ETF Universe
│              ↓
│      Candidate Preparation
│              ↓
│      Exposure Fit Evaluation
│              ↓
│      Instrument Evaluation
│              ↓
│           Selection
│
└── Diagnostics Module
       │
       Authoritative Calculated Outputs
              ↓
       Diagnostic Comparison
              ↓
       Historical Context
              ↓
       Visualization / Reporting
```

---

## 9. Open Architectural Questions

These are intentionally not fixed by this working document:

- exact Python package/file boundaries;
- whether every semantic stage has a distinct implementation object;
- exact output/result object structures;
- whether some capabilities need extraction into reusable helpers immediately or only after a second real consumer appears;
- final ETF-selection scoring/ranking/filtering mechanics;
- exact Diagnostics public API;
- exact handling of calculation traces and explanatory metadata.
