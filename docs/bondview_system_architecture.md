# Bondview System Architecture

## Document Purpose

This document defines the system-level architecture of **Bondview**: its major responsibilities, authoritative analytical boundaries, dependency direction, result boundaries, and system-wide design principles.

Bondview transforms accepted bond-market and macroeconomic observations into reusable Canonical Components and applies those Components to ETF evaluation, human-readable interpretation, and diagnostics.

Detailed economic rules, Component catalogs, calculation formulas, thresholds, evaluator-specific scoring logic, and configuration schemas belong in more specific design documents and contracts.

---

# 1. System Overview

Bondview is a bond-ETF analytical and decision-support system built around **Canonical Components**.

Canonical Components are the authoritative analytical representation of bond-market and macroeconomic conditions. They are produced by Bond Analysis and consumed directly by ETF Evaluation. Bond Exposure Views and Diagnostics use the same authoritative information for interpretation and validation without becoming part of the authoritative ETF Evaluation path.

The system-level structure is:

```text
Accepted Raw Observations
        ↓
[Bond Analysis]
        ↓
Canonical Components ─────────────> [Bond Exposure View Calculation]
        +                                 ↓
ETF Exposure Profile                Bond Exposure Views
        ↓                                      
[ETF Evaluation]                          ↓
        ↓                                      
ETF Evaluation Results ───────────> [Diagnostics]
        ↓                                 ↓
Evaluated Candidate Set             Diagnostic Results
```

The authoritative ETF Evaluation path is complete without the explanatory and diagnostic branch; that branch consumes authoritative outputs for interpretation and validation but is not required for ETF Evaluation.

The internal ETF Evaluation path is:

```text
Canonical Components
        ↓
[Dimension Evaluations] <────────── ETF Exposure Profile
        ↓
Dimension Evaluation Results
        ↓
[Exposure Evaluation]
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
Evaluated Candidate Set
```

The architecture distinguishes four kinds of system output:

- Canonical Components as authoritative analytical information;
- ETF Evaluation Results as ETF-specific decision-support outputs;
- Bond Exposure Views as human-readable interpretations;
- Diagnostic Results as non-authoritative validation and explanation outputs.

---

# 2. System Responsibilities

Bondview is organized around three major Modules.

## 2.1 Bond Analysis Module

The **Bond Analysis Module** produces Canonical Components from accepted Raw Observations.

Its responsibility includes:

- Feature Calculation;
- Component Calculation;
- State Classification where a discrete Component State is useful;
- authoritative reuse of Components across downstream consumers.

Its authoritative result boundary is the set of Canonical Components required by downstream consumers.

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
Component Values
        ↓
[State Classification]
        ↓
Component States
        ↓
Canonical Components
```

A Component may expose a Value, a State, or both, depending on its contract.

The Bond Analysis Module does not make ETF-specific decisions.

## 2.2 ETF Evaluation Module

The **ETF Evaluation Module** evaluates ETFs by combining Canonical Components with the economic identity and implementation characteristics of each ETF.

Its core responsibility is:

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

The ETF Evaluation Module owns ETF-specific economic assessment and implementation assessment.

It does not redefine upstream Components. When an evaluator needs an analytical concept already represented by a Canonical Component, it consumes that Component rather than independently recreating it.

## 2.3 Diagnostics Module

The **Diagnostics Module** explains, inspects, and validates authoritative model behavior without changing authoritative calculations or decisions.

Diagnostics may consume:

- Raw Observations;
- Features;
- Canonical Components;
- Component States;
- Bond Exposure Views;
- ETF Evaluation Results;
- supporting metadata and historical outputs.

Diagnostics may produce:

- Historical Context;
- Diagnostic Comparisons;
- persistence and transition analysis;
- traceability views;
- sensitivity analysis;
- visualizations;
- expert sanity-check outputs.

Diagnostics is downstream of authoritative calculations and must not become an upstream dependency of Bond Analysis or ETF Evaluation.

---

# 3. Canonical Component Architecture

Canonical Components are the principal analytical boundary of Bondview.

This section defines the system-level Component invariants that all more detailed Component design and implementation must preserve.

## 3.1 Component Model

### 3.1.1 Component Authority and Role

A **Component** is a canonical, economically meaningful analytical concept represented by a Component Value and, where useful, a discrete Component State.

Components carry Bondview's authoritative analytical information about bond-market and macroeconomic conditions.

A Component may be consumed by one or more downstream responsibilities, including:

- ETF Evaluation;
- Bond Exposure View Calculation;
- Diagnostics;
- future analytical capabilities.

A Component does not need to be consumed by every responsibility.

The meaning of a Component is independent of the consumer that uses it. ETF evaluators, Bond Exposure Views, and Diagnostics may interpret the same Component differently, but they must not redefine its authoritative economic meaning.

### 3.1.2 Component Value and State

A **Component Value** is the calculated quantitative or structured representation of a Component before discrete classification.

A **Component State** is a discrete economic condition assigned to a Component when discrete classification is useful.

A Component may expose:

- only a Value;
- only a State when the Value is not part of the public result contract;
- both Value and State.

The exact representation belongs to the Component contract.

### 3.1.3 Component Preparation Flow

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
[State Classification]
        ↓
Component State
```

A **Raw Observation** is an accepted source observation used by Bondview.

A **Feature** is a quantitative measure derived from Raw Observations for model use.

Features are generally closer to calculation mechanics, while Components represent economically meaningful analytical concepts intended for authoritative reuse.

---

## 3.2 Calculation Mechanics

Calculation Mechanics are reusable conceptual and implementation structures used to transform values and states without owning domain-specific economic meaning.

They may be used in Component calculation, ETF Evaluation, Bond Exposure View calculation, and Diagnostics where the same processing semantics genuinely apply.

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

### 3.2.2 Rule Mapping

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

Rule Mapping is reusable as a calculation structure, but the economic meaning of the mapping remains owned by the Component, evaluator, or interpretation that uses it.

### 3.2.3 Coverage Strategy

A **Coverage Strategy** defines how the valid Rule Case space is handled.

Possible strategies may include:

- explicit mapping;
- fallback;
- justified interpolation;
- other model-specific handling of uncovered valid cases.

Coverage Strategy is part of the model definition that uses the Rule Table. It is not a separate analytical responsibility.

### 3.2.4 Calculation Mechanics as Capabilities

Calculation Mechanics should be implemented as reusable **Capabilities** when semantically equivalent behavior is required by multiple consumers.

They must remain neutral with respect to Duration, Curve, Credit, macroeconomic conditions, or any one evaluator.

Reusable mechanics should not become hidden owners of economic meaning.

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

Shared Raw Observations do not by themselves imply shared Component identity.

Shared State labels do not by themselves imply shared Component identity.

Shared downstream consumers do not by themselves imply shared Component identity.

### 3.3.3 Horizon and Semantic Equivalence

Relevant horizon is part of Component identity when changing the horizon materially changes the economic question being answered.

Two calculations based on the same market series may therefore remain separate Components when they represent different time-horizon meanings or different classification semantics.

Component consolidation should occur only when semantic equivalence is established, not merely because data lineage overlaps.

---

## 3.4 Component Reuse and Boundaries

### 3.4.1 Canonical Ownership

Each authoritative Component should have one canonical definition and one authoritative calculation path.

The Component contract should determine:

- economic meaning;
- accepted inputs;
- calculation semantics;
- horizon;
- Value representation;
- State Classification where applicable;
- State semantics;
- authoritative result representation.

Detailed field structure belongs in the Component design and Result Contract.

### 3.4.2 Consumer Reuse

If multiple consumers require the same concept with equivalent semantics, the Component should be calculated once and reused.

A downstream consumer may:

- select the Components relevant to its own purpose;
- combine multiple Components;
- map Component States to a consumer-specific result;
- apply ETF-specific information;
- use reusable Calculation Mechanics.

A downstream consumer should not:

- independently redefine an existing Component;
- create a second authoritative calculation of the same concept;
- alter the Component's meaning to fit a local decision rule.

### 3.4.3 Component Domains

Components may describe different economic domains, including:

- rates;
- curve;
- credit;
- inflation;
- monetary policy;
- growth;
- other macroeconomic conditions.

These domain labels are descriptive.

They do not create separate architectural Component types, separate upstream Modules, or separate Component interfaces.

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

## 3.5 Component Consumers

Canonical Components may feed several downstream responsibilities:

```text
Canonical Components
        ├──────────────→ [ETF Evaluation]
        │
        ├──────────────→ [Bond Exposure View Calculation]
        │
        └──────────────→ [Diagnostics]
```

### 3.5.1 ETF Evaluation

ETF Evaluation consumes Components for ETF-specific economic decisions.

It may combine Component information with the ETF Exposure Profile and ETF-level economic or implementation inputs.

ETF Evaluation must not redefine the Components it consumes.

### 3.5.2 Bond Exposure Views

Bond Exposure View Calculation consumes selected Components to produce human-readable interpretations of Duration, Curve, and Credit.

Views may compress or summarize Component information for interpretation, but they do not replace the underlying Components as authoritative ETF Evaluation inputs.

### 3.5.3 Diagnostics

Diagnostics consumes Components and downstream results to inspect historical behavior, traceability, plausibility, and parameter sensitivity.

Diagnostics may refer back to supporting Features and Raw Observations but does not alter Component authority or calculation.

---

# 4. ETF Evaluation Architecture

ETF Evaluation applies Canonical Components to ETF-specific exposure and implementation information.

The module separates economic exposure assessment from positioning context and instrument quality.

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

**Exposure Evaluation** is the combined economic assessment of whether an ETF's Exposure Profile is appropriate under current bond-market and macroeconomic conditions.

The current architecture includes four peer Evaluations:

- Duration Evaluation;
- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation Evaluation.

These Evaluations operate in parallel but do not need to share identical output semantics or weighting.

### 4.2.1 Dimension Evaluations

Each Evaluation consumes:

- the relevant Canonical Components;
- the relevant part of the ETF Exposure Profile;
- any ETF-level economic inputs justified by that evaluator.

The general pattern is:

```text
Relevant Canonical Components
        +
Relevant ETF Exposure Profile
        +
Applicable ETF-Level Economic Inputs
        ↓
[Dimension Evaluation]
        ↓
Core Evaluation Result
```

The specific Component set and economic mapping belong to the relevant evaluator design rather than this system-level architecture.

The four completed Evaluation results are combined into Exposure Evaluation:

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

The architecture requires the four Evaluations to remain distinguishable until aggregation. It does not require them to use identical scales, weights, State semantics, or Rule Mapping structures.

### 4.2.2 Macro Adjustment

Macroeconomic conditions are represented upstream as Canonical Components and are used selectively by the Evaluation whose economic question they affect.

Macro logic is integrated through evaluator-specific **Macro Adjustment**.

The general pattern is:

```text
Core Evaluation Result
        +
Relevant Macro Components
        ↓
[Macro Adjustment]
        ↓
Evaluation Result
```

For example:

```text
Core Duration Evaluation Result
        +
Relevant Macro Components
        ↓
[Duration Macro Adjustment]
        ↓
Duration Evaluation Result
```

Macro Adjustment may modify how strongly an economically attractive exposure should be expressed when macroeconomic conditions materially affect that evaluator.

The architecture does not prescribe the exact adjustment actions, thresholds, Rule Cases, or Rule Mappings. Those belong in evaluator-specific design.

The architectural constraints are:

- macroeconomic conditions remain Canonical Components;
- the relevant evaluator chooses which macro Components it consumes;
- macro effects are applied within the applicable Evaluation;
- macro logic must not redefine upstream Component meaning;
- a macro Component may be used by more than one evaluator when economically justified.

## 4.3 Positioning Overlay

**Positioning Overlay** modifies implementation willingness after Exposure Evaluation without redefining the underlying economic assessment.

It answers:

> Should implementation intensity be restrained or modified despite the economic attractiveness of the exposure?

Typical positioning information may include crowding, sentiment, speculative positioning, unusual directional consensus, or exposure-level extension after a large market move.

Architecturally:

```text
Exposure Evaluation Result
        +
Positioning Inputs
        ↓
[Positioning Overlay]
        ↓
Positioning-Adjusted Exposure Evaluation
```

Positioning Inputs are not assumed to be Canonical Components merely because they are used by Bondview.

If a positioning concept later satisfies the Component contract and requires broader reuse, it may be promoted through explicit design.

Positioning Overlay must not redefine the underlying Exposure Evaluation Result. It modifies implementation willingness or intensity around that result.

## 4.4 Instrument Quality

**Instrument Quality** evaluates whether an ETF is a sufficiently good vehicle for an exposure after Exposure Evaluation and Positioning Overlay have been applied.

Typical implementation characteristics may include:

- expense ratio or implementation cost;
- liquidity;
- bid-ask spread;
- tracking quality;
- other instrument-specific implementation friction.

Architecturally:

```text
Positioning-Adjusted Exposure Evaluation
        +
Instrument Quality Inputs
        ↓
[Instrument Quality]
        ↓
Evaluated Candidate Set
```

Instrument Quality may support both minimum-quality filtering and relative comparison among otherwise acceptable ETFs.

It must remain separate from economic attractiveness. A high-quality ETF can represent an unattractive exposure, and an attractive exposure can be implemented through a poor-quality ETF.

## 4.5 Evaluated Candidate Set

The **Evaluated Candidate Set** is the ETF set remaining after economic evaluation, positioning adjustment, and instrument-quality assessment.

It is the authoritative downstream result of the ETF Evaluation Module.

Final ETF choice may use ranking, weighting, thresholds, portfolio rules, or other decision logic appropriate to the consuming workflow.

Such final choice logic does not need to become a separate Module unless it develops a stable and materially distinct system responsibility with its own meaningful Result Boundary.

## 4.6 ETF Price-History Scope

Detailed ETF traded-price-history analysis is outside the authoritative initial ETF Evaluation flow.

Price-based diagnostics may be added later as optional downstream Capabilities when they answer a concrete diagnostic or decision question and have a clearly defined relationship to underlying bond exposure, benchmark behavior, liquidity, or valuation.

Adding such a Capability should not change the authority of Canonical Components or the ETF Evaluation dependency direction.

---

# 5. Bond Exposure Views and Diagnostics

## 5.1 Bond Exposure Views

A **Bond Exposure View** is a high-level human-readable interpretation of one Bond Exposure Dimension.

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

Their primary roles are:

- human interpretation;
- historical inspection;
- expert sanity checking;
- parameter validation;
- diagnostic comparison.

## 5.2 Diagnostics

Diagnostics may inspect:

- Component Values and States;
- Bond Exposure Views;
- ETF Evaluation Results;
- historical frequency and persistence;
- State transitions;
- historical episodes;
- Component-to-View traceability;
- Component-to-Evaluation traceability;
- sensitivity to model parameters and horizons;
- supporting Features and Raw Observations.

For a selected date or period, Diagnostics should expose enough upstream information for an expert to determine whether the resulting interpretation or evaluation is economically plausible.

Historical Context is diagnostic. It does not create a second authoritative decision model.

Diagnostic Results may include explanatory, comparative, historical, sensitivity, traceability, or sanity-check outputs.

---

# 6. System-Wide Architecture Principles

## 6.1 Data and Observation Boundaries

Data acquisition and source-specific retrieval should remain outside authoritative analytical execution once Raw Observations have been accepted.

Bondview should preserve the conceptual distinction among:

```text
Raw Observations
        ↓
Features
        ↓
Canonical Components
        ↓
ETF Evaluation Results
```

A later analytical layer may refer back to earlier data for explanation or diagnostics, but this does not change the authority of the normal calculation path.

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
- generic result aggregation where semantics are equivalent.

Model-specific economic meaning belongs in the Component, View, or Evaluation that uses the mechanic.

Equivalent mechanics may be reused without collapsing different analytical concepts into one architectural concept.

## 6.4 Extract on Actual Second Use

Reusable implementation behavior should be extracted when a second real consumer requires semantically equivalent behavior.

Extraction is appropriate when:

- the second use is concrete;
- the behavior is semantically equivalent;
- a neutral input/output contract can be defined;
- extraction does not leak domain-specific assumptions into shared infrastructure.

This principle avoids duplicated logic without creating speculative framework layers.

## 6.5 Dependency Direction

The authoritative dependency direction is:

```text
[Bond Analysis]
        ↓
Canonical Components
        ↓
[ETF Evaluation]
        ↓
ETF Evaluation Results
        ↓
Evaluated Candidate Set
```

Additional consumers branch from authoritative outputs:

```text
Canonical Components
        ├──────────────→ [Bond Exposure View Calculation]
        │
        └──────────────→ [Diagnostics]

ETF Evaluation Results
        └──────────────→ [Diagnostics]
```

The following dependency constraints apply:

- Bond Analysis must not depend on ETF Evaluation logic.
- ETF Evaluation may consume Canonical Components but must not redefine them.
- Bond Exposure Views must not mediate the authoritative ETF Evaluation path.
- Diagnostics may consume authoritative outputs but must not modify them.
- one evaluator should not depend on another evaluator's domain logic merely to reuse generic mechanics;
- generic mechanics should be extracted into neutral Capabilities when actual reuse justifies it.

## 6.6 Result Boundaries

Major responsibilities should expose explicit authoritative results.

At system level:

- Bond Analysis exposes Canonical Components;
- ETF Evaluation exposes ETF Evaluation Results and the Evaluated Candidate Set;
- Diagnostics exposes non-authoritative Diagnostic Results.

Concrete result objects should be defined individually through Result Contracts.

The architecture does not require all Modules or Capabilities to share one generic result class.

Result metadata should be sufficient to support material traceability across authoritative boundaries without forcing diagnostic behavior into authoritative calculation.

## 6.7 Model Definition and Configuration

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

Detailed Configuration Schemas belong in more specific model or module contracts.

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
- move Positioning Overlay or Instrument Quality outside ETF Evaluation responsibility;
- introduce cross-evaluator dependencies that bypass neutral reusable Capabilities;
- create a separate macro-processing architecture rather than consuming macroeconomic Components through evaluator-specific logic;
- make Diagnostics part of authoritative decision calculation;
- introduce reusable infrastructure broader than demonstrated reuse requirements;
- materially change the meaning of ETF Evaluation Results or the Evaluated Candidate Set;
- introduce a new downstream responsibility whose scope is stable and distinct enough to require its own Module or Result Boundary.

Changes to individual Component formulas, evaluator rules, thresholds, mappings, score semantics, or configuration values may be significant model changes without necessarily requiring a system-architecture revision, provided they preserve the boundaries defined here.
