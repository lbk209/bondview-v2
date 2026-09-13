# Working Architecture Concepts for Bondview v2 — Generalized Rule-Flow Draft

> **Status: Working document.**
>
> This document captures the current architectural direction derived during terminology and stance/macro-constraint design. It is not an authoritative replacement for `docs/bondview_system_architecture.md`. The system architecture remains foundational, and more specific v2 design documents take precedence where applicable.

## 1. Purpose

This document organizes the current working architecture around three concepts:

- **Module** — major system responsibility;
- **Stage** — semantic processing step inside a module;
- **Capability** — implementation behavior that may be reused wherever equivalent semantics are required.

A central working principle is that the analytical flow previously described primarily for stance calculation can be generalized:

> **Stance Components and Macro Components use the same broad preparation and rule-case concepts up to Rule Mapping. They diverge in what their respective rule mappings produce: Stance Rule Mapping produces a Core Stance, while Constraint Rule Mapping produces a Constraint Action.**

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

> Produce Duration, Curve, and Credit stances by interpreting market-derived Stance Components and applying any stance-specific macro constraint derived from Macro Components.

It owns:

- Stance Components;
- Macro Components used by stance-specific constraints;
- Feature and Component preparation required by those concepts;
- Component State classification;
- Rule-Case Construction;
- Stance Rule Mapping;
- Core Stance calculation;
- Constraint Rule Mapping;
- Constraint Application;
- Final Stance outputs;
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

- Features;
- Component Values;
- Component States;
- Stance Rule Cases;
- Macro Rule Cases;
- Core Stances;
- Constraint Actions;
- Final Stances;
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
Rule-Case Construction Stage
Rule Mapping Stage
Constraint Application Stage
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
Rule-Case Construction capability
Rule Mapping capability
Constraint Application capability
Historical Context Preparation capability
```

A capability may be used by several stages or consumers.

```text
State Classification capability
        ├── Stance Component path
        └── Macro Component path
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

## 4. Generalized Component-State Preparation

The same broad preparation vocabulary applies to both Stance Components and Macro Components.

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

The domain identity is carried by the Component:

```text
Component
├── Stance Component
└── Macro Component
```

A Feature may directly represent a Component Value where no distinct Component Calculation operation is needed.

The generalized structure is semantic. It does not require every model path to physically implement every box.

---

## 5. Generalized Rule-Case Structure

Rule-Case Construction is not inherently stance-only. Whenever multiple Component States jointly define an economically meaningful case, those states may form a Rule Case.

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

The model purpose determines the mapped result.

### 5.1 Stance path

Stance Component States form a **Stance Rule Case**.

```text
Stance Component States
        ↓
[Rule-Case Construction]
        ↓
Stance Rule Case
        ↓
[Stance Rule Mapping]
        ↓
Core Stance
```

The Stance Rule Mapping answers the stance's market-derived economic question.

Examples:

```text
Duration:
long-end yield trend
× recent long-end yield move
→ Core Duration Stance

Credit:
spread level
× spread direction
→ Core Credit Stance

Curve:
curve state
× curve-move regime
→ Core Curve Stance
```

### 5.2 Macro-constraint path

Macro Component States may form a **Macro Rule Case**.

```text
Macro Component States
        ↓
[Rule-Case Construction]
        ↓
Macro Rule Case
        ↓
[Constraint Rule Mapping]
        ↓
Constraint Action
```

The Constraint Rule Mapping answers:

> Given these macro conditions, what action should be applied to the Core Stance?

Examples may include:

```text
Duration:
inflation trend
× policy direction
→ Duration Constraint Action

Credit:
growth
× labor-market condition
→ Credit Constraint Action
```

A stance may legitimately have no Macro Constraint. Curve currently follows that path.

---

## 6. Constraint Rule Mapping vs Constraint Application

This distinction is central to the generalized architecture.

### 6.1 Constraint Rule Mapping

**Constraint Rule Mapping** is economic logic.

It maps:

```text
Macro Rule Case
        ↓
Constraint Action
```

Examples:

```text
rising inflation + tightening policy
→ cap positive Duration

weakening growth + deteriorating labor market
→ cap/weaken positive Credit
```

### 6.2 Constraint Application

**Constraint Application** is the mechanic that applies the selected action to a supplied Core Stance.

```text
Constraint Action
        +
Core Stance
        ↓
[Constraint Application]
        ↓
Final Stance
```

The same Constraint Action can therefore produce different results depending on the Core Stance without requiring a separate economic rule for every Core-Stance value.

Example:

```text
Constraint Action:
cap positive stance at +1

Core +3 → Final +1
Core +1 → Final +1
Core  0 → Final  0
Core -2 → Final -2
```

This keeps the economic rule table separate from generic mechanics.

### 6.3 Why this does not require a full market × macro Cartesian table

Suppose Duration has:

```text
9 Stance Rule Cases
9 Macro Rule Cases
```

There are potentially 81 runtime combinations, but the architecture does not require an 81-row economic table.

Instead:

```text
9 Stance Rule Cases
        ↓
Core Stance

9 Macro Rule Cases
        ↓
Constraint Action

Core Stance + Constraint Action
        ↓
[Constraint Application]
        ↓
Final Stance
```

A combined market × macro table becomes necessary only if the appropriate macro treatment depends on information from the specific Stance Rule Case that is not preserved in the Core Stance/result boundary.

That would be a separate architectural decision rather than the default model.

---

## 7. Macro Rule Coverage Is Stance-Specific

The generalized structure does not require identical macro rule coverage across stances.

### Duration

A compact complete macro Rule Table may be appropriate:

```text
inflation trend: falling / stable / rising
×
policy direction: easing / stable / tightening
=
maximum 9 Macro Rule Cases
```

Each case may map to an explicit Constraint Action.

### Credit

A sparse downside-oriented structure may be more appropriate:

```text
economically meaningful adverse cases
        ↓
explicit Constraint Actions

remaining valid cases
        ↓
pass-through fallback
```

This preserves the current idea that Credit macro constraints may be primarily downside-protective.

### Curve

Current design:

```text
no Macro Constraint
→ Core Curve Stance passes through
→ Final Curve Stance
```

No dummy Macro Component, Rule Case, or no-op Rule Table should be required merely to satisfy the generalized structure.

---

## 8. Stance Calculation Module — Working Stage Flow

The full conceptual flow can now be represented as two related branches.

```text
                         Raw Observations
                               ↓
                    [Feature Calculation]
                               ↓
                            Features
                               ↓
                   [Component Calculation]
                               ↓
                        Component Values
                               ↓
                   [State Classification]
                               ↓
                        Component States
                         /                                      /                          Stance Component States    Macro Component States
                    ↓                       ↓
          [Rule-Case Construction] [Rule-Case Construction]
                    ↓                       ↓
             Stance Rule Case          Macro Rule Case
                    ↓                       ↓
          [Stance Rule Mapping]   [Constraint Rule Mapping]
                    ↓                       ↓
               Core Stance           Constraint Action
                         \             /
                          \           /
                           ↓         ↓
                     [Constraint Application]
                              ↓
                         Final Stance
```

The diagram shows semantic symmetry, not mandatory implementation duplication. Equivalent mechanics should use the same authoritative capability where appropriate.

Curve may bypass the macro branch:

```text
Core Curve Stance
        ↓
pass-through
        ↓
Final Curve Stance
```

---

## 9. Stance Structure

For each Stance Type:

```text
┌──────────────────────────────────────────┐
│ Stance                                   │
│                                          │
│ Type: Duration / Curve / Credit          │
│                                          │
│ Stance Components                       │
│      ↓                                   │
│ Stance Component States                 │
│      ↓                                   │
│ Stance Rule Case                        │
│      ↓                                   │
│ Stance Rule Mapping                     │
│      ↓                                   │
│ Core Stance                             │
│                                          │
│ Macro Components, where applicable      │
│      ↓                                   │
│ Macro Component States                  │
│      ↓                                   │
│ Macro Rule Case                         │
│      ↓                                   │
│ Constraint Rule Mapping                 │
│      ↓                                   │
│ Constraint Action                       │
│                                          │
│ Core Stance + Constraint Action         │
│      ↓                                   │
│ Constraint Application                  │
│      ↓                                   │
│ Final Stance                            │
└──────────────────────────────────────────┘
```

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

## 10. ETF Selection Module — Working Stage Flow

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

### 10.1 Candidate Preparation

Purpose:

> Establish which ETFs are eligible and resolve the exposure characteristics required for evaluation.

Likely concepts include ETF Universe, Candidate ETF, Exposure Profile, underlying market identity, maturity/duration exposure, curve segment, credit exposure, and investor-currency or hedging characteristics where relevant.

### 10.2 Exposure Fit Evaluation

Purpose:

> Determine whether an ETF expresses the exposure favored by the Bond-Exposure Stance Set.

Primary output concept: **Stance Fit**.

### 10.3 Instrument Evaluation

Purpose:

> Determine whether the particular ETF is attractive enough after Exposure Fit is established.

Potential evaluation inputs include yield/carry, price behavior, fees, liquidity, tracking/index characteristics, currency/hedging effects, and relevant low-risk or risk-free alternatives.

### 10.4 Selection

Purpose:

> Apply the ETF-selection contract to the evaluated candidates and produce the formal selection output.

The exact ranking/filtering/selection mechanics remain to be designed.

---

## 11. Diagnostics Module — Working Stage Flow

```text
Authoritative Calculated Outputs
        ↓
Diagnostic Comparison
        ↓
Historical Context
        ↓
Visualization / Reporting
```

Historical Context may include Component Values, Component States, Stance Rule Cases, Macro Rule Cases, Core Stances, Constraint Actions, and Final Stances.

Historical Context must not become a separately reimplemented stance or constraint model.

### Historical Context Preparation

When Historical Context requires preparation, use the **Historical Context Preparation capability**.

If later diagnostics need the same semantics, they should reuse that capability rather than recreate equivalent logic.

---

## 12. Reuse Principle

The central lesson from previous implementation cleanup is not "create a shared module."

It is:

> **If an authoritative capability or derived output with the required semantics already exists, later consumers reuse it rather than implement equivalent logic independently.**

The same rule applies to Feature Calculation, Component Calculation, State Classification, State Stabilization, Rule-Case Construction, Rule Mapping mechanics, Constraint Application, Historical Context Preparation, and other capabilities once equivalent reuse is demonstrated.

Generalizing the conceptual flow does not justify separate parallel implementations for stance and macro paths when their mechanics are semantically equivalent.

---

## 13. Architecture Overview

```text
BONDVIEW
│
├── Stance Calculation Module
│
│      Common preparation
│      Raw Observations
│             ↓
│      Feature / Component calculation
│             ↓
│      Component States
│             │
│             ├── Stance Components
│             │       ↓
│             │   Stance Rule Case
│             │       ↓
│             │   Core Stance
│             │
│             └── Macro Components
│                     ↓
│                 Macro Rule Case
│                     ↓
│               Constraint Action
│
│      Core Stance + Constraint Action
│             ↓
│      Constraint Application
│             ↓
│      Final Stance
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

## 14. Relationship to the Stance Mapping / Macro Constraint Design Document

`working_stance_mapping_macro_constraint_design.md` should remain the place for **stance-specific economic design**, including questions such as:

- which Duration Stance Components and states are used;
- the complete Duration Stance Rule Mapping;
- which Duration Macro Components form Macro Rule Cases;
- which Macro Rule Cases map to which Constraint Actions;
- whether Duration uses a complete nine-case macro table;
- whether Credit uses sparse downside-only cases plus pass-through fallback;
- which raw observations best represent growth, labor-market, inflation, and policy Components;
- whether Curve continues to have no Macro Constraint.

This architecture document should instead define the common structure that makes those stance-specific choices possible.

The stance-specific document should eventually align its terminology with this structure, but the generalized architecture should not be duplicated there.

---

## 15. Open Architectural Questions

These remain intentionally unresolved:

- exact Python package/file boundaries;
- exact concrete result structures;
- whether Constraint Action is represented numerically, ordinally, structurally, or through a bounded action specification;
- whether Stance Rule Mapping and Constraint Rule Mapping use exactly the same configured lookup capability or only share lower-level mechanics;
- how much explanatory metadata from Stance Rule Cases and Macro Rule Cases belongs in formal results;
- whether any future stance requires a combined market × macro rule case because Core Stance alone does not preserve enough information;
- final ETF-selection scoring/ranking/filtering mechanics;
- exact Diagnostics public API.
