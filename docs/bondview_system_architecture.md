# Bondview System Architecture

## Document Purpose

This document defines the system-level architecture of **Bondview**: its major responsibilities, authoritative analytical boundaries, dependency direction, result boundaries, and system-wide design principles.

Bondview transforms accepted bond-market and macroeconomic observations into reusable Components and applies those Components to ETF evaluation, human-facing interpretation, and diagnostics.

`bondview_vocabulary.md` is the source of truth for canonical term meaning and naming. This document is the source of truth for system structure, ownership, dependency direction, processing flow, and Result Boundaries.

Detailed economic rules, Component catalogs, calculation formulas, thresholds, evaluator-specific scoring logic, and concrete configuration schemas belong in more specific design documents and contracts.

---

# 1. System Overview

Bondview is a bond-ETF analytical and decision-support system built around **Components**.

Components are the authoritative analytical representation of bond-market and macroeconomic conditions. They are produced by Bond Analysis and consumed directly by ETF Evaluation. Bond Exposure Views and Diagnostics use authoritative outputs for interpretation and validation without becoming part of the authoritative ETF Evaluation path.

The system-level structure is:

```text
Accepted Raw Observations
        ↓
[Bond Analysis]
        ↓
Components ───────────────────────> [Bond Exposure View Calculation]
        ↓                                  ↓
[ETF Evaluation]                    Bond Exposure Views
        ↓                                  ↓
ETF Evaluation Results ───────────> [Diagnostics]
                                           ↓
                                    Diagnostic Results
```

The architecture distinguishes four kinds of system output:

- **Components** as authoritative analytical information;
- **ETF Evaluation Results** as ETF-specific decision-support outputs;
- **Bond Exposure Views** as human-facing interpretations;
- **Diagnostic Results** as non-authoritative validation and explanation outputs.

The authoritative ETF Evaluation path is complete without the explanatory and diagnostic branch; that branch consumes authoritative outputs for interpretation and validation but is not required for ETF Evaluation.

The internal ETF Evaluation path is:

```text
Components
        ↓
[Constituent Evaluations] <──────── ETF Exposure Profile
        ↓
Constituent Evaluation Results
        ↓
[Evaluation Combination]
        ↓
Exposure Evaluation Result
        ↓
[Positioning Overlay] <──────────── Positioning Inputs
        ↓
Positioning-Adjusted
Exposure Evaluation
        ↓
[Instrument Quality] <───────────── Instrument Quality Inputs
        ↓
ETF Evaluation Results
```

---

# 2. System Responsibilities

Bondview is organized around three major Modules.

## 2.1 Bond Analysis Module

The **Bond Analysis Module** produces Components from accepted Raw Observations.

Its responsibility includes:

* applying the Resolved Model Specification to accepted Raw Observations;
* Feature Calculation;
* Component Calculation;
* State Classification where a discrete Component State is useful;
* preserving the lineage required by authoritative Component results;
* exposing Components through its Result Boundary for downstream reuse.

Its authoritative Result Boundary is the set of Components required by downstream consumers.

Data acquisition and source-specific retrieval are outside Bond Analysis once Raw Observations have been accepted. Bond Analysis also does not perform ETF-specific interpretation or evaluation.

The internal preparation flow and Component result semantics are defined in Section 3.

## 2.2 ETF Evaluation Module

The **ETF Evaluation Module** evaluates ETFs by combining Components with the economic identity and implementation characteristics of each ETF.

It owns ETF-specific economic assessment, positioning adjustment, and instrument-quality assessment, and exposes ETF Evaluation Results through its Result Boundary.

The ETF Evaluation Module does not redefine upstream Components. When an evaluator needs an analytical concept already represented by a Component, it consumes that Component rather than independently recreating it.

The internal structure of ETF Evaluation is defined in Section 4.

## 2.3 Diagnostics Module

The **Diagnostics Module** explains, inspects, and validates authoritative model behavior without changing authoritative calculations or decisions.

Diagnostics is lineage-scoped by default: it traces the authoritative analytical lineage needed to explain a Component, Bond Exposure View, or ETF Evaluation Result without introducing unrelated supplemental analytical data. Comparison of an evaluation with an ETF Exposure Profile remains part of ETF Evaluation rather than the primary Diagnostics responsibility.

Diagnostics is downstream of authoritative calculations and must not become an upstream dependency of Bond Analysis or ETF Evaluation. Detailed diagnostic behavior is defined in Section 5.2.

---

# 3. Component Architecture

Components are the principal analytical boundary of Bondview.

This section defines the system-level Component invariants that more detailed Component design and implementation must preserve.

The Bond Analysis Module owns the authoritative preparation of Components. The sections below define the analytical structures, identity rules, lineage requirements, calculation mechanics, and result semantics that govern that responsibility.

## 3.1 Component Model

### 3.1.1 Component Authority and Role

A **Component** is a canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State.

Components carry Bondview's authoritative analytical information about bond-market and macroeconomic conditions.

A Component may be consumed by one or more downstream responsibilities, including ETF Evaluation, Bond Exposure View Calculation, Diagnostics, and future analytical capabilities.

A Component does not need to be consumed by every responsibility.

The meaning of a Component is independent of the consumer that uses it. ETF evaluators, Bond Exposure Views, and Diagnostics may interpret the same Component differently, but they must not redefine its authoritative economic meaning.

If multiple consumers require the same Component with equivalent semantics, they should reuse the same authoritative Component rather than create consumer-specific versions or alternative authoritative calculations. Downstream consumers may select, combine, and interpret the Components relevant to their own responsibilities without altering the Components themselves.

### 3.1.2 Component Value, State, and Preparation Flow

A **Component Value** is the calculated quantitative or structured representation of a Component before discrete classification.

A **Component State** is a discrete economic condition assigned to a Component when discrete classification is useful.

The normal analytical preparation path is:

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

A Component may expose only a Value, only a State as its public result representation, or both. The required representation is part of the Component definition and Result Contract.

A **Raw Observation** is an accepted source observation used by Bondview. A **Feature** is a quantitative measure derived from Raw Observations for model use. Features are generally closer to calculation mechanics, while Components represent economically meaningful analytical concepts intended for authoritative reuse.

### 3.1.3 Component Domains

Components may describe different economic domains, including rates, curve, credit, inflation, monetary policy, growth, or other macroeconomic conditions.

These domain labels are descriptive. They do not create separate architectural Component types, separate upstream Modules, or separate Component interfaces.

For example:

```text
Long-End Yield Trend
Inflation Trend
Policy Direction
Credit Spread Level
Curve Configuration
```

are all Components from the perspective of system architecture.

The relevance of a Component is determined by the consumer that uses it.

## 3.2 Calculation Mechanics

Calculation Mechanics are reusable conceptual structures used to transform values and states without owning domain-specific economic meaning.

### 3.2.1 State Classification

**State Classification** converts a Component Value into a Component State.

```text
Component Value
        ↓
[State Classification]
        ↓
Component State
```

The classification method may use thresholds, buckets, smoothing, hysteresis, historical percentiles, or other justified mechanics.

The exact method belongs to the relevant Component design.

### 3.2.2 Rule Mapping and Coverage

**Rule Mapping** converts a combination of Component States into a model-specific result.

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

A **Rule Dimension** is a Component whose State participates in a particular Rule Case.

A **Rule Case** is one concrete combination of Rule Dimension States.

A **Rule Mapping** defines the relationship between a Rule Case and the model result produced from that case.

A **Rule Table** is the configured set of Rule Mappings for one defined model purpose.

A **Coverage Strategy** defines how the valid Rule Case space is handled, such as explicit mapping, fallback, justified interpolation, or other model-specific handling of valid uncovered cases.

Rule Mapping is reusable as a calculation structure, but the economic meaning of a mapping remains owned by the Component, View, or Evaluation that uses it.

System-wide principles for reusable mechanics are defined in Section 6.3.

## 3.3 Component Construction and Identity

### 3.3.1 Component Derivation

A Component may be calculated directly from Features or, where economically meaningful, from other Components or Component Values.

For example:

```text
Short-End Yield Move
        +
Long-End Yield Move
        ↓
[Curve Movement Calculation]
        ↓
Curve Movement
```

The resulting `Curve Movement` remains a Component when it represents an economically meaningful reusable concept.

The architecture does not require separate structural Component types based on whether a Component is calculated directly from Features or from other Components.

### 3.3.2 Component Identity

Two analytical concepts should normally be treated as the same Component only when the following are equivalent:

* economic meaning;
* calculation;
* relevant horizon;
* classification semantics where State Classification applies.

Shared Raw Observations, shared State labels, or shared downstream consumers do not by themselves imply shared Component identity.

Relevant horizon is part of Component identity when changing the horizon materially changes the economic question being answered. Two calculations based on the same market series may therefore remain separate Components when they represent different time-horizon meanings or different classification semantics.

Component consolidation should occur only when semantic equivalence is established, not merely because data lineage overlaps.

## 3.4 Component Definition and Lineage

### 3.4.1 Canonical Definition and Result Contract

Each authoritative Component should have one canonical definition and one authoritative calculation path.

The Component definition captures the Component's economic identity and configured calculation semantics. Its Result Contract defines the authoritative runtime representation exposed to downstream consumers, including the required Value or State representation and sufficient lineage references for traceability.

A compact example of how the system-wide configuration principle applies to one Component is:

```text
Long-End Yield Trend definition
├── economic meaning
├── input references
├── calculation / transform specification
├── relevant horizon
└── State Classification specification / semantics
        ↓
[Configuration Validation]
        ↓
Resolved Model Specification
        ↓
[Component Calculation] <──────── Input Features
        ↓
Long-End Yield Trend result
├── Value / State as defined
└── lineage references
```

Concrete field names and serialization formats belong in the Component design and Configuration Schema rather than this system architecture.

### 3.4.2 Lineage and Traceability

A Component result should preserve enough lineage or provenance information to identify the upstream inputs that materially contributed to that result.

The arrows below represent **backward traceability from the Component result to its upstream analytical dependencies**, rather than the forward calculation direction used in most other diagrams.

The intended traceability direction is:

```text
Component Result
        ↑
Supporting Components / Features
        ↑
Supporting Raw Observations
```

When one Component is derived from other Components, the lineage should preserve that dependency rather than flattening it into unrelated source data.

Lineage exists to support explanation, reproducibility, and lineage-scoped Diagnostics. It does not require every result object to duplicate all upstream data values; stable references or other explicit provenance may satisfy the Result Contract when they allow the authoritative calculation path to be reconstructed or inspected.

---

# 4. ETF Evaluation Architecture

ETF Evaluation applies Components to ETF-specific exposure and implementation information.

The module separates economic exposure assessment from positioning context and instrument quality.

Detailed ETF traded-price-history analysis is outside the current authoritative ETF Evaluation flow. It may be introduced later only where a defined analytical or diagnostic purpose justifies it.

## 4.1 ETF Exposure Profile

The **ETF Exposure Profile** is the economic identity of the bond exposure that an ETF is designed to provide.

Bondview consumes the ETF Exposure Profile as an input and does not prescribe a single method for constructing it. In practice, the ETF's declared benchmark or other reference exposure may provide a convenient basis for the profile, supplemented where necessary by material exposure characteristics such as currency hedging, leverage, or explicit duration, maturity, or credit characteristics.

These examples are illustrative rather than a required construction schema. A concrete Profile schema should be defined only when implementation requirements justify one.

The ETF Exposure Profile answers:

> What bond exposure is this ETF designed to provide?

Determining whether the ETF's actual holdings, tracking behavior, or realized performance faithfully deliver that exposure is outside the current ETF Exposure Profile responsibility. Such characteristics may instead be assessed under Instrument Quality where supported by defined data and rules.

ETF Evaluation combines the ETF Exposure Profile with Components to determine how appropriate that exposure is under current conditions.

## 4.2 Exposure Evaluation

**Exposure Evaluation** is the broader economic assessment process that determines whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions.

Its internal hierarchy is:

```text
[Exposure Evaluation]
     ├── [Constituent Evaluations]
     │        ├── [Core Evaluation]
     │        └── [Macro Adjustment, where applicable]
     └── [Evaluation Combination]
```

Macro Adjustment therefore belongs within the applicable Constituent Evaluation rather than operating as a peer analytical layer.

### 4.2.1 Constituent Evaluations

A **Constituent Evaluation** assesses one economically distinct aspect of an ETF's Exposure Profile using the Components relevant to that question.

The current Constituent Evaluations are:

* **Duration Evaluation** — whether the ETF's interest-rate sensitivity is appropriate under current conditions;
* **Curve Evaluation** — whether the ETF's maturity / curve exposure is appropriate under current term-structure conditions;
* **Credit Evaluation** — whether the ETF's credit-risk exposure is appropriate under current credit conditions;
* **Rates Valuation Evaluation** — whether compensation for accepting the ETF's rates exposure is sufficiently attractive.

These evaluations operate in parallel but do not need to share identical output semantics, scales, weighting, State semantics, or Rule Mapping structures.

The general pattern is:

```text
Relevant Components
        ↓
[Constituent Evaluation] <──────── Relevant ETF Exposure Profile
        ↓
Core Evaluation Result
```

A Constituent Evaluation may additionally consume ETF-level economic inputs when its economic question specifically requires them. In the current design, the clearest example is a defined ETF Yield / Carry measure used by Rates Valuation Evaluation.

The specific Component set, economic mapping, Profile information, and any additional ETF-level economic inputs belong to the relevant evaluator design rather than this system-level architecture.

### 4.2.2 Macro Adjustment

Macroeconomic conditions are represented upstream as Components and are used selectively by the Constituent Evaluation whose economic question they affect.

Macro logic is integrated through evaluator-specific **Macro Adjustment**.

The general pattern is:

```text
Core Evaluation Result
        ↓
[Macro Adjustment] <────────────── Relevant macroeconomic Components
        ↓
Evaluation Result
```

Macro Adjustment may modify the economic assessment represented by the Core Evaluation Result when macroeconomic conditions materially affect that evaluator.

Possible behavior may include pass-through, weakening, magnitude caps, or other evaluator-specific modifications. These are illustrative possibilities rather than a system-wide required action set.

The architecture does not prescribe the exact adjustment actions, thresholds, Rule Cases, or Rule Mappings. Those belong in evaluator-specific design.

Macro Adjustment may consume any macroeconomic Components relevant to the evaluator, and the same Component may be used by more than one evaluator where justified. Such use must not redefine the meaning of the upstream Components.

The completed Constituent Evaluation results are combined into the overall Exposure Evaluation Result:

```text
Duration Evaluation Result
        +
Curve Evaluation Result
        +
Credit Evaluation Result
        +
Rates Valuation Evaluation Result
        ↓
[Evaluation Combination]
        ↓
Exposure Evaluation Result
```

The exact combination logic may use weighting, rules, conditional mappings, or other justified mechanics. It belongs in ETF Evaluation design rather than this system-level architecture.

## 4.3 Positioning Overlay

**Positioning Overlay** modifies implementation willingness after Exposure Evaluation without redefining the underlying economic assessment.

It answers:

> Should implementation intensity be restrained or modified despite the economic attractiveness of the exposure?

Typical positioning information may include crowding, sentiment, speculative positioning, unusual directional consensus, or exposure-level extension after a large market move.

Architecturally:

```text
Exposure Evaluation Result
        ↓
[Positioning Overlay] <──────────── Positioning Inputs
        ↓
Positioning-Adjusted Exposure Evaluation
```

Positioning Inputs are not assumed to be Components merely because they are used by Bondview.

If a positioning concept later satisfies the Component definition and requires broader reuse, that treatment should be established explicitly rather than inferred from its use in Positioning Overlay.

Positioning Overlay does not imply that the underlying economic thesis is incorrect; for example, heavy crowding may justify weaker implementation even when Exposure Evaluation remains strongly positive.

Positioning Overlay must not redefine the underlying Exposure Evaluation Result. It modifies implementation willingness or intensity around that result.

## 4.4 Instrument Quality

**Instrument Quality** evaluates whether an ETF is a sufficiently good vehicle for an exposure after Exposure Evaluation and Positioning Overlay have been applied.

Potential implementation characteristics may include:

- expense ratio or implementation cost;
- tracking quality, where tracking is an intended objective;
- active-management effectiveness, where applicable and supported by defined data and rules;
- other instrument-specific implementation characteristics supported by defined data and rules.

Execution-specific conditions that Bondview does not currently model, such as live liquidity, bid-ask spread, order size, or market conditions at the time of trading, remain outside the current authoritative ETF Evaluation logic and are considered by the user or consuming workflow at execution time.

Architecturally:

```text
Positioning-Adjusted Exposure Evaluation
        ↓
[Instrument Quality] <───────────── Instrument Quality Inputs
        ↓
ETF Evaluation Results
```

Instrument Quality may identify failure of an explicit minimum-quality requirement and support relative comparison among ETFs while preserving the ETF Evaluation Result.

It must remain separate from economic attractiveness. A high-quality ETF can represent an unattractive exposure, and an attractive exposure can be implemented through a poor-quality ETF.

## 4.5 ETF Evaluation Results and Downstream Choice

**ETF Evaluation Results** are the authoritative downstream results of the ETF Evaluation Module. They preserve the ETF-specific analytical outputs required for comparison across ETFs, including the relevant Constituent Evaluation results and subsequent evaluation stages.

ETF ranking and final-choice logic are downstream from ETF Evaluation Results:

```text
ETF Evaluation Results
        ↓
[Ranking / Final Decision Logic]
        ↓
Final ETF Choice
```

Final ETF choice may use ranking, weighting, thresholds, portfolio rules, or other decision logic appropriate to the consuming workflow. Such final-choice logic does not need to become a separate Module unless it develops a stable and materially distinct system responsibility with its own meaningful Result Boundary.

---

# 5. Bond Exposure Views and Diagnostics

## 5.1 Bond Exposure Views

A **Bond Exposure View** is a high-level human-facing interpretation of one Bond Exposure Dimension.

The current Bond Exposure Dimensions are:

- Duration;
- Curve;
- Credit.

Bond Exposure Views are derived from selected Components.

```text
Selected Components
        ↓
[Bond Exposure View Calculation]
        ↓
Bond Exposure View
```

Bond Exposure Views are explanatory interpretations rather than authoritative ETF Evaluation inputs.

They may summarize information differently across Duration, Curve, and Credit. The architecture does not require homogeneous output semantics across the three Views.

Bond Exposure View calculation should preserve enough Component-level traceability to identify the selected Component States or other authoritative Component information that produced a View. This supports historical inspection and expert sanity checking without making the View an authoritative ETF Evaluation input.

## 5.2 Diagnostics

Diagnostics inspects an authoritative result or a Bond Exposure View together with the actual dependency lineage needed to explain it.

For a diagnostic target, Diagnostics may inspect:

- the target result or Bond Exposure View;
- intermediate evaluation results in its calculation path;
- relevant Component Values and States;
- supporting Features and Raw Observations;
- historical frequency and persistence;
- State transitions;
- historical episodes;
- Component-to-View or Component-to-Evaluation traceability;
- sensitivity to model parameters and horizons.

The default diagnostic boundary is the target's dependency lineage. This limits which analytical variables and dependencies Diagnostics may introduce; it does not limit Diagnostics to the target date. Historical realizations of those same lineage entities may be inspected for context and sanity checking. Diagnostics should not introduce unrelated supplemental market or macro data merely because those data are available.

For a selected date or period, Diagnostics should expose enough lineage and supporting information for an expert to determine whether the resulting interpretation or evaluation is economically plausible.

Historical Context is diagnostic. It does not create a second authoritative decision model.

Diagnostic Results may include explanatory, comparative, historical, sensitivity, traceability, visualization, or sanity-check outputs.

---

# 6. System-Wide Architecture Principles

## 6.1 Data and Observation Boundaries

Data acquisition and source-specific retrieval should remain outside authoritative analytical execution once Raw Observations have been accepted.

Raw Observations, Features, Components, ETF Evaluation Results, Bond Exposure Views, and Diagnostic Results should remain conceptually distinguishable even when Diagnostics traverses their lineage for explanation.

## 6.2 Market Identity

Analytical context is determined by the underlying bond exposure rather than solely by an ETF's listing venue.

For example, an ETF listed in one country but holding another country's government bonds requires the rates, curve, policy, and macroeconomic context relevant to the underlying bond market.

Currency and hedging characteristics belong to the ETF Exposure Profile when they materially affect investor economic exposure.

## 6.3 Reusable Calculation Mechanics

Reusable calculation behavior should remain neutral with respect to a particular economic domain when the behavior is genuinely shared.

Potential reusable mechanics include:

- normalization;
- smoothing;
- State Classification;
- stabilization or hysteresis;
- Rule Case Construction;
- Rule Mapping;
- clipping or bounded transformation;
- generic result combination where semantics are equivalent.

Model-specific economic meaning belongs in the Component, View, or Evaluation that uses the mechanic.

Equivalent mechanics may be reused without collapsing different analytical concepts into one architectural concept.

Well-established, domain-neutral behavior may be implemented as a shared Capability from the outset when semantic equivalence and a neutral input/output contract are clear.

For novel or domain-specific behavior whose reuse semantics are uncertain, prefer local implementation until concrete reuse demonstrates that extraction is justified.

This principle aims to avoid both duplicated mechanics and speculative framework layers.

## 6.4 Dependency Direction

The following dependency constraints apply:

- Bond Analysis must not depend on ETF Evaluation logic.
- ETF Evaluation may consume Components but must not redefine them.
- Bond Exposure Views must not mediate the authoritative ETF Evaluation path.
- Diagnostics may consume authoritative outputs and their dependency lineage but must not modify them.
- one Constituent Evaluation should not depend on another evaluator's domain logic merely to reuse generic mechanics;
- generic mechanics should be implemented through neutral Capabilities when their shared semantics are sufficiently established.

## 6.5 Result Boundaries

Major responsibilities should expose explicit Result Boundaries with documented Result Contracts.

A Result Contract should define the authoritative contents and semantics of its result and preserve enough metadata or references to support material traceability across boundaries.

Concrete result objects should be defined individually. The architecture does not require all Modules or Capabilities to share one generic result class.

Diagnostic traceability requirements should not force every result to duplicate all upstream data values; explicit lineage references may satisfy the boundary when they reliably identify the authoritative upstream calculation path.

## 6.6 Model Definition and Configuration

Model-specific structure and parameters should be declared through explicit Model Configuration and resolved through validation before calculation.

Conceptually:

```text
Model Configuration
        ↓
[Configuration Validation]
        ↓
Resolved Model Specification
```

Configuration defines model behavior but does not change the architectural ownership of Components, Evaluations, or Result Boundaries.

Concrete Configuration Schemas and serialization formats belong in more specific model, Component, or module contracts.

---

# 7. Architecture Review Triggers

The system architecture should be reviewed when a proposed change would:

- change which responsibility owns an authoritative analytical concept;
- change the definition or authority of Components;
- introduce a new major Module or remove an existing one;
- create a new system-level Result Boundary;
- make ETF Evaluation depend on Bond Exposure Views rather than Components;
- make Bond Analysis depend on ETF-specific evaluation logic;
- introduce a structural Component subtype that changes upstream processing or interfaces;
- materially change the Component lineage or traceability contract;
- move Positioning Overlay or Instrument Quality outside ETF Evaluation responsibility;
- introduce cross-evaluator dependencies that bypass neutral reusable Capabilities;
- create a separate macro-processing architecture rather than consuming macroeconomic Components through evaluator-specific logic;
- make Diagnostics part of authoritative decision calculation or allow unrelated supplemental data to become an implicit diagnostic decision path;
- introduce reusable infrastructure broader than justified by established semantics or demonstrated reuse requirements;
- materially change the meaning or Result Boundary of ETF Evaluation Results;
- introduce a new downstream responsibility whose scope is stable and distinct enough to require its own Module or Result Boundary.

Changes to individual Component formulas, evaluator rules, thresholds, mappings, score semantics, or configuration values may be significant model changes without necessarily requiring a system-architecture revision, provided they preserve the boundaries defined here.
