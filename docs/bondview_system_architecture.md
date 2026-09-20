# Bondview System Architecture

## Document Purpose

This document defines the system-level architecture of **Bondview**: its major responsibilities, authoritative analytical boundaries, dependency direction, result boundaries, and system-wide design principles.

Bondview transforms accepted bond-market and macroeconomic observations into reusable Canonical Components and applies those Components to ETF evaluation, human-facing interpretation, and diagnostics.

Detailed economic rules, Component catalogs, calculation formulas, thresholds, evaluator-specific scoring logic, and concrete configuration schemas belong in more specific design documents and contracts.

---

# 1. System Overview

Bondview is a bond-ETF analytical and decision-support system built around **Canonical Components**.

Canonical Components are the authoritative analytical representation of bond-market and macroeconomic conditions. They are produced by Bond Analysis and consumed directly by ETF Evaluation. Bond Exposure Views and Diagnostics use authoritative outputs for interpretation and validation without becoming part of the authoritative ETF Evaluation path.

The system-level structure is:

```text
Accepted Raw Observations
        ↓
[Bond Analysis]
        ↓
Canonical Components ─────────────> [Bond Exposure View Calculation]
        ↓                                  ↓
[ETF Evaluation]                    Bond Exposure Views
        ↓                                  ↓
ETF Evaluation Results ───────────> [Diagnostics]
                                           ↓
                                    Diagnostic Results
```

The architecture distinguishes four kinds of system output:

- **Canonical Components** as authoritative analytical information;
- **ETF Evaluation Results** as ETF-specific decision-support outputs;
- **Bond Exposure Views** as human-facing interpretations;
- **Diagnostic Results** as non-authoritative validation and explanation outputs.

The authoritative ETF Evaluation path is complete without the explanatory and diagnostic branch; that branch consumes authoritative outputs for interpretation and validation but is not required for ETF Evaluation.

The internal ETF Evaluation path is:

```text
Canonical Components
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

The **Bond Analysis Module** produces Canonical Components from accepted Raw Observations.

Its responsibility includes:

* applying the Resolved Model Specification to accepted Raw Observations;
* Feature Calculation;
* Component Calculation;
* State Classification where a discrete Component State is useful;
* preserving the lineage required by authoritative Component results;
* exposing Canonical Components through its Result Boundary for downstream reuse.

Its authoritative Result Boundary is the set of Canonical Components required by downstream consumers.

Data acquisition and source-specific retrieval are outside Bond Analysis once Raw Observations have been accepted. Bond Analysis also does not perform ETF-specific interpretation or evaluation.

The internal preparation flow and Component result semantics are defined in Section 3.


## 2.2 ETF Evaluation Module

The **ETF Evaluation Module** evaluates ETFs by combining Canonical Components with the economic identity and implementation characteristics of each ETF.

It owns ETF-specific economic assessment, positioning adjustment, and instrument-quality assessment, and exposes ETF Evaluation Results through its Result Boundary.

The ETF Evaluation Module does not redefine upstream Components. When an evaluator needs an analytical concept already represented by a Canonical Component, it consumes that Component rather than independently recreating it.

The internal structure of ETF Evaluation is defined in Section 4.

## 2.3 Diagnostics Module

The **Diagnostics Module** explains, inspects, and validates authoritative model behavior without changing authoritative calculations or decisions.

Diagnostics is lineage-scoped by default: it traces the authoritative analytical lineage needed to explain a Component, Bond Exposure View, or ETF Evaluation Result without introducing unrelated supplemental analytical data. Comparison of an evaluation with an ETF Exposure Profile remains part of ETF Evaluation rather than the primary Diagnostics responsibility.

Diagnostics is downstream of authoritative calculations and must not become an upstream dependency of Bond Analysis or ETF Evaluation. Detailed diagnostic behavior is defined in Section 5.2.

---

# 3. Canonical Component Architecture

Canonical Components are the principal analytical boundary of Bondview.

This section defines the system-level Component invariants that more detailed Component design and implementation must preserve.

The Bond Analysis Module owns the authoritative preparation of Canonical Components. The sections below define the analytical structures, identity rules, lineage requirements, calculation mechanics, and result semantics that govern that responsibility.

## 3.1 Component Model

### 3.1.1 Component Authority and Role

A **Component** is a canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State.

Components carry Bondview's authoritative analytical information about bond-market and macroeconomic conditions.

A Component may be consumed by one or more downstream responsibilities, including ETF Evaluation, Bond Exposure View Calculation, Diagnostics, and future analytical capabilities.

A Component does not need to be consumed by every responsibility.

The meaning of a Component is independent of the consumer that uses it. ETF evaluators, Bond Exposure Views, and Diagnostics may interpret the same Component differently, but they must not redefine its authoritative economic meaning.

Downstream consumers select and interpret the Components relevant to their own responsibilities without redefining the Components themselves.

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

are all Canonical Components from the perspective of system architecture.

The relevance of a Component is determined by the consumer that uses it.

---

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

---

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

- economic meaning;
- calculation;
- relevant horizon;
- classification semantics where State Classification applies.

Shared Raw Observations, shared State labels, or shared downstream consumers do not by themselves imply shared Component identity.

Relevant horizon is part of Component identity when changing the horizon materially changes the economic question being answered. Two calculations based on the same market series may therefore remain separate Components when they represent different time-horizon meanings or different classification semantics.

Component consolidation should occur only when semantic equivalence is established, not merely because data lineage overlaps.

---

## 3.4 Component Definition, Lineage, and Reuse

### 3.4.1 Canonical Definition and Result Contract

Each authoritative Component should have one canonical definition and one authoritative calculation path.

The Component definition captures the Component's economic identity and configured calculation semantics. Its Result Contract defines the authoritative runtime representation exposed to downstream consumers, including the required Value or State representation and sufficient lineage references for traceability.

A compact example of how the system-wide configuration principle applies to one Component is:

```text
Long-End Yield Trend definition
├── economic meaning
├── input references
├── calculation / transform
├── relevant horizon
└── State Classification / semantics
        ↓
[Configuration Validation]
        ↓
Resolved Model Specification
   (component entry)
        ↓
[Component Calculation]
        ↓
Long-End Yield Trend result
├── Value / State as defined
└── lineage references
```

Concrete field names and serialization formats belong in the Component design and Configuration Schema rather than this system architecture.

### 3.4.2 Lineage and Traceability

A Component result should preserve enough lineage or provenance information to identify the upstream inputs that materially contributed to that result.

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

### 3.4.3 Consumer Reuse

If multiple consumers require the same concept with equivalent semantics, the Component should be calculated once and reused.

A downstream consumer may select the Components relevant to its purpose, combine multiple Components, map Component States to a consumer-specific result, and apply consumer-specific information.

A downstream consumer should not independently redefine an existing Component, create a second authoritative calculation of the same concept, or alter the Component's meaning to fit a local decision rule.

---

# 4. ETF Evaluation Architecture

ETF Evaluation applies Canonical Components to ETF-specific exposure and implementation information.

The module separates economic exposure assessment from positioning context and instrument quality.

Detailed ETF traded-price-history analysis is outside the current authoritative ETF Evaluation flow. It may be introduced later only where a defined analytical or diagnostic purpose justifies it.

## 4.1 ETF Exposure Profile

The **ETF Exposure Profile** is the economically relevant identity of an ETF's bond exposure.

It may include properties such as:

- maturity exposure;
- duration;
- credit exposure;
- underlying market;
- portfolio construction;
- currency;
- hedging where relevant.

The ETF Exposure Profile is an input identity, not an evaluation result.

It answers:

> What economic bond exposure does this ETF provide?

ETF Evaluation combines this identity with Canonical Components to determine whether the exposure is appropriate under current conditions.

## 4.2 Exposure Evaluation

**Exposure Evaluation** is the broader economic assessment process that determines whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions.

Its internal hierarchy is:

```text
[Exposure Evaluation]
├── [Constituent Evaluations]
│   ├── [Core Evaluation]
│   └── [Macro Adjustment, where applicable]
└── [Evaluation Combination]
        ↓
Exposure Evaluation Result
```

Macro Adjustment therefore belongs within the applicable constituent evaluation rather than operating as a peer analytical layer.

### 4.2.1 Constituent Evaluations

A constituent evaluation assesses one economically distinct aspect of an ETF's Exposure Profile using the Canonical Components and ETF-specific information relevant to that question.

The current constituent evaluations are:

- **Duration Evaluation** — whether the ETF's interest-rate sensitivity is appropriate under current conditions;
- **Curve Evaluation** — whether the ETF's maturity / curve exposure is appropriate under current term-structure conditions;
- **Credit Evaluation** — whether the ETF's credit-risk exposure is appropriate under current credit conditions;
- **Rates Valuation Evaluation** — whether compensation for accepting the ETF's rates exposure is sufficiently attractive.

These evaluations operate in parallel but do not need to share identical output semantics, scales, weighting, State semantics, or Rule Mapping structures.

The general pattern is:

```text
Relevant Canonical Components
        ↓
[Constituent Evaluation] <──────── Relevant ETF Exposure Profile + Applicable ETF-Level Economic Inputs
        ↓
Core Evaluation Result
```

The specific Component set, economic mapping, and ETF-level inputs belong to the relevant evaluator design rather than this system-level architecture.

### 4.2.2 Macro Adjustment

Macroeconomic conditions are represented upstream as Canonical Components and are used selectively by the constituent evaluation whose economic question they affect.

Macro logic is integrated through evaluator-specific **Macro Adjustment**.

The general pattern is:

```text
Core Evaluation Result
        ↓
[Macro Adjustment] <────────────── Relevant Macro Components
        ↓
Evaluation Result
```

Macro Adjustment may modify how strongly an economically attractive exposure should be expressed when macroeconomic conditions materially affect that evaluator.

The architecture does not prescribe the exact adjustment actions, thresholds, Rule Cases, or Rule Mappings. Those belong in evaluator-specific design.

The architectural constraints are:

- macroeconomic conditions remain Canonical Components;
- the relevant evaluator chooses which macro Components it consumes;
- macro effects are applied within the applicable constituent evaluation;
- macro logic must not redefine upstream Component meaning;
- a macro Component may be used by more than one evaluator when economically justified.

The completed constituent evaluation results are combined into the overall Exposure Evaluation Result:

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

Positioning Inputs are not assumed to be Canonical Components merely because they are used by Bondview.

If a positioning concept later satisfies the Component definition and requires broader reuse, that treatment should be established explicitly rather than inferred from its use in Positioning Overlay.

Positioning Overlay must not redefine the underlying Exposure Evaluation Result. It modifies implementation willingness or intensity around that result.

## 4.4 Instrument Quality

**Instrument Quality** evaluates whether an ETF is a sufficiently good vehicle for an exposure after Exposure Evaluation and Positioning Overlay have been applied.

Potential implementation characteristics may include:

- expense ratio or implementation cost;
- tracking quality;
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

Instrument Quality may support both minimum-quality filtering and relative comparison among otherwise acceptable ETFs.

It must remain separate from economic attractiveness. A high-quality ETF can represent an unattractive exposure, and an attractive exposure can be implemented through a poor-quality ETF.

## 4.5 ETF Evaluation Results and Downstream Choice

**ETF Evaluation Results** are the authoritative downstream results of the ETF Evaluation Module. They preserve the ETF-specific analytical outputs required for comparison across ETFs, including the relevant constituent evaluation results and subsequent evaluation stages.

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

Bond Exposure Views are derived from selected Canonical Components.

```text
Selected Canonical Components
        ↓
[Bond Exposure View Calculation]
        ↓
Bond Exposure View
```

Bond Exposure Views are explanatory interpretations rather than authoritative ETF Evaluation inputs.

They may summarize information differently across Duration, Curve, and Credit. The architecture does not require homogeneous output semantics across the three Views.

Bond Exposure View calculation should preserve enough Component-level traceability to identify the selected Component States or other authoritative Component information that produced a View. This supports historical inspection and expert sanity checking without making the View an authoritative ETF Evaluation input.

## 5.2 Diagnostics

Diagnostics inspects an authoritative result or interpretation together with the actual dependency lineage needed to explain it.

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

Raw Observations, Features, Canonical Components, ETF Evaluation Results, Bond Exposure Views, and Diagnostic Results should remain conceptually distinguishable even when Diagnostics traverses their lineage for explanation.

## 6.2 Market Identity

Analytical context is determined by the underlying bond exposure rather than solely by an ETF's listing venue.

For example, an ETF listed in one country but holding another country's government bonds requires the rates, curve, policy, and macroeconomic context relevant to the underlying bond market.

Currency and hedging characteristics belong to the ETF Exposure Profile when they materially affect realized investor exposure.

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
- ETF Evaluation may consume Canonical Components but must not redefine them.
- Bond Exposure Views must not mediate the authoritative ETF Evaluation path.
- Diagnostics may consume authoritative outputs and their dependency lineage but must not modify them.
- one constituent evaluator should not depend on another evaluator's domain logic merely to reuse generic mechanics;
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
- change the definition or authority of Canonical Components;
- introduce a new major Module or remove an existing one;
- create a new system-level Result Boundary;
- make ETF Evaluation depend on Bond Exposure Views rather than Canonical Components;
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
