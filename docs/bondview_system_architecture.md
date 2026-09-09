# Bondview System Architecture

## Document Purpose

This document defines the system-level architecture of Bondview: its major responsibilities, their relationships and boundaries, and the system-wide principles that should guide future implementation.

Detailed model rules—including stance-specific scoring and schema and configuration definitions—belong in their respective module or architecture contracts.

---

## 1. System Overview

Bondview derives bond-exposure stances from bond-market and macro conditions, then evaluates how those resulting views map to investable ETFs.

```text
bond-market conditions              macro conditions
          └──────────────┬──────────────┘
                         ↓
              Bond-Exposure Stance Set
             (Duration / Curve / Credit)
                         ↓
                   ETF selection
```

---

## 2. System Responsibilities

### 2.1 Stance Calculation

Bondview produces separate analytical stances for Duration, Curve, and Credit.

Each stance owns the components, classifications, rule structure, constraint logic, and calculation behavior needed to answer its own economic question.

The common conceptual structure separates market-derived stance logic from stance-specific macro-constraint logic:

```text
Stance Components
        ↓
Stance Rule Case
        ↓
Core Stance

Macro Components
        ↓
Macro Rule Case
        ↓
Constraint Action

Core Stance + Constraint Action
        ↓
Final Stance
```

#### Rule mapping

Rule mapping converts economically meaningful combinations of component states into model results.

On the stance path, Stance Rule Cases map to a Core Stance.

```text
credit spreads wide + spreads tightening
→ positive core Credit stance
```

On the macro path, Macro Rule Cases map to a stance-specific Constraint Action.

Stance and macro components remain separate rule inputs rather than being combined into one rule case by default.

Additional information should not automatically become another rule-case dimension merely because it is available.

This principle helps keep rule structures interpretable and limits unnecessary Cartesian expansion.

#### Macro constraints

Macro constraints are applied when macroeconomic conditions materially affect how strongly a Core Stance should be expressed.

A macro rule determines the applicable Constraint Action, while constraint application determines how that action affects the Core Stance.

Constraint Actions may:

- leave the Core Stance unchanged;
- strengthen or weaken it;
- cap its magnitude;
- restrict a particular direction;
- reject an exposure only when a genuinely hard condition is justified.

```text
growth weakening + unemployment rising
→ weaken/cap positive core Credit stance
```

Macro constraints are stance-specific. Duration, Curve, and Credit may therefore consume different Macro Components and apply different constraint logic.

Macro inputs should be introduced only where their relevance to the affected stance can be economically justified.

Reusable constraint mechanics may be used across stances, while the macro conditions and economic rules applied by each stance remain stance-specific.

#### Bond-Exposure Stance Set

The final Duration, Curve, and Credit outputs together form the Bond-Exposure Stance Set used by ETF selection.

The stance set represents the system's analytical view of bond-exposure structure after relevant macro constraints have been applied.

It is not itself an ETF recommendation.

The stance set preserves Duration, Curve, and Credit as separate outputs rather than collapsing them into a single aggregate score.

### 2.2 ETF Selection

ETF selection evaluates ETFs in the eligible ETF Universe according to how well they express the Bond-Exposure Stance Set and whether their instrument-level characteristics justify selection.

It may consider representative instrument and market characteristics such as:

* yield or carry;
* duration or maturity exposure;
* price behavior;
* fees and liquidity;
* tracking or index characteristics;
* currency or hedging exposure where relevant;
* the applicable low-risk or risk-free alternative when the decision requires that comparison.

ETF selection consumes the final stance outputs rather than recreating Duration, Curve, or Credit logic independently for each ETF.

The final decision therefore distinguishes between:

```text
What bond exposure is favored?
        ↓
stance calculation

Which ETF expresses that exposure appropriately
and is attractive enough relative to alternatives?
        ↓
ETF selection
```

---

## 3. Architecture Principles

### 3.1 Data and Observation Boundaries

#### Accepted Runtime Inputs

Data acquisition and source-specific retrieval should remain outside analytical execution once runtime inputs have been accepted.

Raw observations, prepared data, derived features, components, stances, and downstream evaluation inputs should remain distinguishable.

#### Raw Observation Reuse

The same raw observation may legitimately contribute to more than one analytical responsibility.

Raw-data reuse does not imply shared derived meaning.

Each derived concept should have one authoritative owner. If multiple responsibilities require the same derived concept with the same semantics, it should be calculated once and reused rather than independently redefined.

#### Market Identity

Analytical outputs are market-specific.

The relevant market is determined by the underlying exposure, not merely by the ETF's listing venue. For example, a Korea-listed ETF holding U.S. Treasuries still requires U.S. rates and Treasury-market context for its bond stance interpretation.

Investor-currency and hedging considerations belong in ETF selection where they affect the investor’s realized exposure, rather than in the bond-exposure stance calculation.

### 3.2 Reusable Calculation Mechanics and Reuse

#### Reusable Mechanics

Reusable calculation mechanics should remain neutral with respect to any one stance.

Examples include:

* normalization and smoothing;
* state or bucket classification;
* stabilization and hysteresis;
* rule-case construction and score lookup;
* score clipping;
* generic constraint application.

Model-specific configuration determines which mechanics each stance uses and how they are combined. Reusable mechanics should not encode Duration-, Curve-, Credit-, or macro-specific economic meaning.

#### Extract on Actual Second Use

Behavior should be extracted for reuse when a second real consumer requires semantically equivalent behavior.

This improves efficiency and maintainability by preventing duplicated calculation logic without creating speculative reusable frameworks.

Extraction is appropriate when:

* the second use is real;
* the behavior is semantically equivalent;
* a neutral input/output contract can be defined without domain-specific leakage.

### 3.3 Dependency Direction

Duration, Curve, and Credit should not depend on each other's domain logic merely to reuse calculation mechanics. Reusable behavior should be owned by a neutral capability when extraction is justified.

ETF selection consumes the final stance outputs; stance calculations do not depend on ETF-selection logic.

Macro constraints belong to the stance they affect. Component preparation and generic calculation mechanics may reuse neutral capabilities where semantics are equivalent, while macro interpretation and constraint rules remain stance-specific.

### 3.4 Result Boundaries

Formal stance outputs should preserve the Core Stance, the Final Stance, and enough metadata—including the applied Constraint Action where relevant—to explain material differences between them.

The exact field structure belongs in the stance/result contract rather than this system-level document.

---

## 4. Architecture Review Triggers

The system architecture should be reviewed when a proposed change would:

* move economic ownership of a derived concept from one responsibility to another;
* introduce a new major analytical responsibility;
* make one stance depend on another stance's domain logic;
* duplicate an authoritative derived concept in multiple places;
* materially change the public result boundary consumed by downstream responsibilities;
* combine stance and macro conditions into one Rule Case, or otherwise blur the separation between Core Stance derivation and Macro Constraint logic;
* introduce reusable infrastructure broader than the demonstrated reuse requirement;
* move ETF-selection logic into stance calculation or stance logic into ETF selection.

Model-specific rule changes may be significant even when the implementation change is technically small.
