# Bondview Bond-Analysis / ETF-Selection Redesign Review

## Document Status

**Status:** Review-stage design document  
**Authority:** Non-authoritative  
**Primary purpose:** Provide a concrete working design sketch for the revised Bondview architecture and implementation direction.  
**Secondary purpose:** Serve as the decision bridge for later revisions to `bondview_system_architecture.md`, `bondview_vocabulary.md`, and the remaining detailed design documents.

This document supersedes `bondview_proposed_design_sequence_steps_1_3_review.md` as the current review reference where the two documents conflict.

The earlier review remains useful as historical reasoning for:

- iterative Component discovery;
- canonical Component identity;
- horizon-sensitive Component separation;
- the provisional rates-side Component catalog;
- coverage / redundancy / missing-information review.

However, the architecture in this document is now primary.

---

# 1. Redesign Summary

The previous architecture treated Duration, Curve, and Credit Stances as the principal outputs of stance calculation and as the main analytical inputs to ETF Selection.

The revised design changes that relationship.

## 1.1 Core change

```text
Previous direction

Raw Observations
        ↓
Features
        ↓
Components
        ↓
Duration / Curve / Credit Stances
        ↓
Bond-Exposure Stance Set
        ↓
ETF Selection
```

The proposed direction is:

```text
Raw Observations
        ↓
Features
        ↓
Canonical Components
        ↓
Authoritative Analysis Result
        ├────────────────────────────→ ETF Selection
        │                               uses Components directly
        │
        └────────────────────────────→ Derived Interpretations
                                        Duration / Curve / Credit Stances
                                        human-facing only
```

The central principle is:

> **Canonical Components carry the authoritative analytical information. Stances are derived human-readable interpretations of those Components along familiar bond-market dimensions. ETF Selection does not depend on Stances as decision inputs.**

This removes Stances as information bottlenecks.

---

# 2. Why the Redesign Is Useful

Several problems in the previous stance-centered structure came from requiring each Stance to carry enough information to support downstream ETF choice.

Examples included:

- whether Duration needed a compensation / valuation Component merely to become sufficiently preference-oriented;
- whether Curve had to express a direct portfolio preference rather than a descriptive curve condition;
- whether Duration, Curve, and Credit needed comparable semantic depth;
- how bull / bear steepener or flattener information could survive Stance compression;
- whether useful Component information was lost once the Bond-Exposure Stance Set was produced;
- whether a shared Component should be duplicated across multiple Stances.

The revised structure resolves much of this pressure by preserving Components as first-class authoritative outputs.

A Stance may summarize selected Components for human interpretation without determining what information ETF Selection is allowed to use.

---

# 3. Module Boundaries

The revised design now points toward three major responsibilities rather than one enlarged ETF Selection module.

```text
Upstream Analysis Module
        ↓
Canonical Components
        ↓
ETF Evaluation Module
        ↓
Implementation-qualified Candidate Set
        ↓
Final ETF Selection
```

Human-facing Stances remain a derived interpretation path from canonical Components and are not authoritative ETF-selection inputs.

## 3.1 Upstream Analysis Module

The upstream analytical responsibility calculates canonical Components from accepted observations.

A final module name is not yet fixed.

Current working candidates include:

- `Bond Analysis Module`
- `Bond Component Analysis Module`
- `Component Analysis Module`

The name should eventually reflect that the module produces bond-relevant analytical Components rather than Stance decisions.

Its core responsibility is:

```text
Raw Observations
        ↓
Features
        ↓
Canonical Components
```

Human-facing Duration / Curve / Credit interpretations may also be produced from the same Components, but they do not define the module's authoritative result boundary.

## 3.2 ETF Evaluation Module

The ETF Evaluation Module consumes:

```text
Canonical Components
+
ETF Exposure Profile
+
ETF-specific economic / implementation properties
```

and performs:

- Duration Evaluation;
- Curve Evaluation;
- Credit Evaluation;
- Rates Valuation / Compensation Evaluation;
- dimension-specific macro effects;
- Exposure / Market aggregation;
- Positioning Overlay;
- Instrument Quality filtering / ranking.

Its output is an:

> **Implementation-qualified Candidate Set**

This module is property- and analytical-state-driven. It does not require detailed ETF price history for its core evaluation logic.

## 3.3 ETF price-history analysis is excluded from the initial version

ETF traded-price history can produce descriptive statistics such as:

- recent return;
- drawdown;
- realized price volatility;
- trend / extension;
- historical percentile.

However, these statistics do not by themselves provide a reliable directional investment rule.

Poor recent ETF performance can mean that the underlying thesis deteriorated, that valuation improved after a price decline, or simply that the ETF behaved normally given its exposure. Price history alone cannot distinguish among those interpretations.

More decision-relevant diagnostics also require additional data:

```text
premium / discount to NAV
→ ETF price + NAV / iNAV history

tracking dislocation
→ ETF returns + benchmark / underlying returns

liquidity breakdown
→ volume + bid / ask + spread data

price move inconsistent with underlying bonds
→ ETF price + underlying bond / index / yield data
```

Therefore the initial Bondview version should **exclude ETF price-history analysis from the authoritative selection flow**.

If later work identifies a concrete, economically justified price-based rule or diagnostic need, ETF Price Diagnostics can be added as an optional downstream capability without changing the Component-authoritative architecture.

## 3.4 No structural Market / Macro split in Component calculation

The previous architecture distinguished:

```text
Market Components
Macro Components
```

because Market Components fed Stance calculation while Macro Components fed Macro Constraints.

That structural distinction is no longer required in the upstream calculation flow.

From the perspective of Component production:

```text
Long-End Yield Trend
Inflation Trend
Policy Direction
Credit Spread Level
Curve Configuration
```

are all canonical Components.

Their economic category may remain useful descriptive metadata, but it does not require:

- different calculation modules;
- different Component interfaces;
- separate upstream processing paths.

The relevant distinction is made by the consumer.

Therefore:

> **Component identity is independent of whether the concept is informally described as market-derived or macro-derived. Consumer logic determines how the Component is interpreted.**

A separate `Macro Analysis Module` is not currently justified.

---

# 4. Canonical Components

## 4.1 Component role

A Component is an authoritative analytical concept that preserves information needed by one or more downstream consumers.

Its identity should eventually define:

- economic meaning;
- Raw Observation / Feature lineage;
- Component Value calculation;
- relevant horizon;
- State Classification where applicable;
- Component State labels and semantics.

A Component may be calculated from Features or, where economically appropriate, from other Components or their Values.

For example:

```text
Short-End Yield Move
+
Long-End Yield Move B
        ↓
Curve Movement
```

`Curve Movement` can still be a Component because `steepening / stable / flattening` is itself an economically meaningful reusable concept.

The design does **not** require a formal `Primitive Component` / `Derived Component` taxonomy. Where useful, an individual Component description may simply state that it is derived from other Components or their Values.

A Component is not defined by the Stance or ETF evaluator that consumes it.

## 4.2 Consolidation rule

The working consolidation rule remains:

> **Same economic meaning + same calculation + same horizon + same State semantics → one canonical Component.**

The following are insufficient by themselves:

```text
same Raw Observation
same state labels
same consumer family
```

## 4.3 Horizon as part of identity

If two consumers require economically different horizons, the corresponding concepts should normally remain separate Components.

For example:

```text
Long-End Yield Move A
Long-End Yield Move B
```

are currently treated as separate candidates because:

```text
A
→ supports broader Duration interpretation
   by confirming / pausing / challenging Long-End Yield Trend

B
→ participates in relative short-end / long-end Curve Movement
```

Even if both eventually use the same Treasury series, they answer different time-horizon questions.

The default working assumption is therefore:

> **A and B remain separate unless later analysis positively demonstrates that horizon, calculation, classification, and semantics can be identical.**

`A / B` are temporary working names. Final canonical names should be semantic once their horizons are defined.

---

# 5. Current Candidate Component Catalog

The catalog is still provisional.

## 5.1 Rates / curve candidates

| Candidate Component | Current economic role | Status |
|---|---|---|
| **Long-End Yield Trend** | Broader direction of long-end Treasury yields | Strong candidate |
| **Long-End Yield Move A** | Duration-relevant recent long-end movement relative to the broader trend | Strong candidate; horizon unresolved |
| **Long-End Yield Move B** | Curve-relevant long-end movement over the Curve Movement horizon | Strong candidate; horizon unresolved |
| **Short-End Yield Move** | Curve-relevant short-end movement aligned with Yield Move B | Strong candidate; horizon unresolved |
| **Curve Movement** | Relative term-structure movement: steepening / stable / flattening | Strong candidate |
| **Curve Configuration** | Current curve shape / slope condition | Strong candidate |
| **Term Premium** | Candidate compensation measure for bearing long-horizon interest-rate risk | Coverage candidate; inclusion unresolved |
| **Real Long-End Yield** | Candidate broader real-income / valuation context | Coverage candidate; inclusion unresolved |
| **Nominal Long-End Yield Level** | Observable starting-yield / income context; may overlap with ETF yield / carry | Coverage candidate; inclusion unresolved |
| **Underlying Rate Volatility** | Volatility of the underlying rates market; candidate risk modifier for duration exposure | Coverage candidate; inclusion unresolved |

A generic `Duration Compensation` Component is no longer preferred.

If compensation is needed, the design should preserve the specific economically meaningful concept that is actually required, such as `Term Premium`, rather than create a vague synthetic symmetry with `Credit Spread Level`.

## 5.2 Credit candidates

| Candidate Component | Current economic role | Status |
|---|---|---|
| **Credit Spread Level** | Compensation for accepting credit risk | Strong candidate |
| **Credit Spread Direction** | Direction of spread change | Strong candidate |

Additional Credit Components should be added only if ETF-selection coverage requires them.

## 5.3 Macro / economic-condition candidates

These are canonical Components like any others; the category is descriptive rather than structural.

| Candidate Component | Current economic role | Status |
|---|---|---|
| **Inflation Trend** | Inflation direction relevant to rates / credit evaluation | Strong existing candidate |
| **Policy Direction** | Realized monetary-policy direction | Strong existing candidate |
| **Growth Condition / Trend** | Economic-growth condition potentially relevant to credit evaluation | Candidate |

The exact catalog is not yet complete.

---

# 6. Stances as Derived Interpretations

## 6.1 Revised role of Stance

A Stance is no longer an authoritative ETF-selection input.

Working definition:

> **Stance:** a human-readable analytical interpretation of selected canonical Components along one specified bond-market dimension.

Examples:

```text
Duration Stance
→ interpretation of the outright-rate / duration dimension

Curve Stance
→ interpretation of the term-structure dimension

Credit Stance
→ interpretation of the credit-risk dimension
```

Stances do not need homogeneous output semantics.

That is acceptable because their job is explanation and diagnostics rather than direct selection.

A Stance can also serve as a **sanity-check projection** of selected Components.

Across the full historical sample, Bondview should be able to inspect:

- frequency of each Stance;
- transition counts;
- average persistence;
- historical episodes;
- Component-to-Stance traceability;
- sensitivity to horizon / threshold choices.

For a selected date or period, the system should expose the Component States and supporting Features / Raw Observations that produced the interpretation so that a bond specialist can quickly assess whether the result is economically plausible.

This makes Stances useful for validating Component logic and parameter choices even though they are not authoritative ETF-selection inputs.

For example:

```text
Duration
→ may naturally look preference-like:
   longer / neutral / shorter duration

Curve
→ may naturally be descriptive:
   inversion normalizing / persistent inversion /
   increasing positive slope / etc.

Credit
→ may combine compensation and direction
   into a credit-risk interpretation
```

The key design test is not whether the three Stances look alike.

It is:

> **Do the authoritative Components preserve enough information for ETF Selection to make the intended decisions?**

## 6.2 Existing stance logic remains useful

Previous Stance rule work is not necessarily discarded.

It can be reused for:

- human-facing interpretation;
- diagnostics;
- explanations of why ETF evaluations behave as they do;
- possibly shared economic mapping capabilities if the same semantics are also required in ETF evaluation.

However:

> **ETF Selection must not consume the Stance result as a substitute for the underlying authoritative Components.**

---

# 7. Curve Interpretation and Bull / Bear Descriptions

The current rates-side structure is provisionally:

```text
Short-End Yield Move
        +
Long-End Yield Move B
        ↓
Curve Movement
```

with:

```text
Curve Configuration
        +
Curve Movement
        ↓
Curve Stance / Curve Interpretation
```

`Curve Movement` should currently be treated as a Component rather than automatically equated with the final Curve interpretation.

It may be described as derived from `Short-End Yield Move` and `Long-End Yield Move B`, but this is descriptive lineage rather than a separate formal Component type.

Examples:

| Curve Configuration | Curve Movement | Human interpretation |
|---|---|---|
| Inverted | Steepening | inversion normalizing |
| Inverted | Stable | persistent inversion |
| Inverted | Flattening | inversion deepening |
| Roughly flat | Steepening | positive slope emerging |
| Roughly flat | Stable | persistent flat curve |
| Roughly flat | Flattening | inversion emerging |
| Positive | Steepening | positive slope increasing |
| Positive | Stable | persistent positive slope |
| Positive | Flattening | positive slope compressing |

Bull / bear steepener / flattener descriptions **cannot be derived from `Curve Movement` alone**.

`Curve Movement = steepening` or `flattening` identifies the relative slope change, but not whether the underlying yield moves were upward or downward.

The bull / bear label can instead be derived from the already proposed:

```text
Short-End Yield Move
+
Long-End Yield Move B
+
Curve Movement
```

No additional raw market series is necessarily required if those two Yield Move Components already exist.

For example:

```text
short end falls more than long end
→ bull steepener

long end rises more than short end
→ bear steepener

long end falls more than short end
→ bull flattener

short end rises more than long end
→ bear flattener
```

The bull / bear label itself is initially best treated as a **derived interpretation**.

If later coverage testing shows that bull vs bear curve drivers change ETF maturity choice beyond what Duration and Curve Evaluations already capture, the underlying Yield Move Components should affect ETF Evaluation directly. The label itself does not need to become an authoritative Component merely for that reason.

---

# 8. ETF Evaluation and Selection Flow

## 8.1 Master hierarchy

The initial design should distinguish **one input identity layer and three decision layers**:

```text
Input:
ETF Exposure Profile
→ What economic exposure does this ETF provide?

Decision Layer 1:
Market-derived ETF Evaluation
→ Is that exposure economically appropriate under the current bond environment?
   Dimension-specific macro effects are applied internally here.

Decision Layer 2:
Positioning Overlay
→ Should implementation intensity be restrained despite economic attractiveness?

Decision Layer 3:
Instrument Quality
→ Is this ETF a sufficiently good vehicle for the intended exposure?

```

This hierarchy is the master reference for Sections 8 and 9.

`ETF Exposure Profile` is an input, not another peer evaluation stage.

Dimension-specific macro effects are internal mechanics of Decision Layer 1.

ETF traded-price history is excluded from the authoritative initial-version selection flow.

## 8.2 ETF Exposure Profile

The ETF Exposure Profile contains properties that define what economic exposure the ETF actually provides.

Typical fields include:

- underlying market;
- maturity segment;
- effective duration;
- credit exposure;
- index / portfolio construction;
- currency exposure;
- hedging structure where applicable.

These are identity properties, not quality scores.

They are required by the market-derived ETF evaluations.

## 8.3 Market-derived ETF evaluations

```text
Canonical Components
        +
ETF Exposure Profile
        ↓
┌───────────────────────────────────────┐
│ Duration Evaluation                   │
│ Curve Evaluation                      │
│ Credit Evaluation                     │
│ Rates Valuation / Compensation Eval.  │
└───────────────────────────────────────┘
        ↓
Exposure / Market Evaluation
```

The first four evaluations determine whether an ETF's economic exposure fits the current bond environment.

Dimension-specific macro effects are applied **inside** the relevant evaluations before aggregation.

### 8.3.1 Duration Evaluation

Possible inputs:

```text
Long-End Yield Trend
Long-End Yield Move A
Underlying Rate Volatility, if retained
+
ETF Duration Profile
```

Question:

> **How appropriate is this ETF's interest-rate sensitivity under the current rates environment?**

Macro-related Components such as:

```text
Inflation Trend
Policy Direction
```

may modify a Core Duration Evaluation:

```text
Duration-related Components
+
ETF Duration Profile
        ↓
Core Duration Evaluation

Inflation Trend
+
Policy Direction
        ↓
Duration Macro Effect
        ↓
Final Duration Evaluation
```

Possible macro-effect semantics include:

```text
pass-through
weaken
cap
restrict aggressive long-duration expression
```

The exact mechanics should be defined only after the evaluation scale is designed.

The same macro condition may affect a very-high-duration ETF more strongly than a moderate-duration ETF.

### 8.3.2 Curve Evaluation

Possible inputs:

```text
Curve Configuration
Curve Movement
Short-End Yield Move
Long-End Yield Move B
+
ETF maturity-segment exposure
```

Question:

> **How appropriate is this ETF's position on the maturity structure under the current curve environment?**

Curve Evaluation may act as a relative-maturity qualifier to Duration Evaluation rather than as an independent directional preference.

Bull / bear steepener / flattener information can be derived from Short-End Yield Move and Long-End Yield Move B if needed. Whether that derived information changes ETF choice remains a coverage question.

### 8.3.3 Credit Evaluation

Possible inputs:

```text
Credit Spread Level
Credit Spread Direction
+
ETF credit exposure
```

Question:

> **How appropriate is this ETF's credit-risk exposure under current credit conditions?**

Macroeconomic Components such as:

```text
Growth Condition
Inflation Trend
Policy Direction
```

may produce a Credit-specific macro effect:

```text
Credit-related Components
+
ETF Credit Profile
        ↓
Core Credit Evaluation

Growth / Inflation / Policy Components
        ↓
Credit Macro Effect
        ↓
Final Credit Evaluation
```

### 8.3.4 Rates Valuation / Compensation Evaluation

This evaluation addresses the market-level problem that was previously considered as `Duration Compensation`.

Possible candidate inputs include:

```text
Term Premium
Real Long-End Yield
Nominal Long-End Yield Level
ETF-level yield / carry where appropriate
+
ETF rate exposure
```

Question:

> **Is the market-level compensation for accepting this ETF's rates exposure sufficiently attractive?**

A generic `Duration Compensation` Component is not required merely for symmetry.

The Component catalog should preserve whichever economically specific concepts materially improve ETF choice.

A useful design test is to project how each candidate would change evaluation across ETFs with different rate exposure:

```text
Short-duration ETF
Intermediate-duration ETF
Long-duration ETF
```

For example:

- **Term Premium** is the cleanest candidate for compensation specifically associated with bearing longer-horizon rate risk. A high positive value should matter more to longer-duration ETFs than to short-duration ETFs.
- **Real Long-End Yield** provides broader real-income / valuation context. It may improve the attractiveness of medium/long government-bond exposure but is not a pure duration-risk-premium measure.
- **Nominal Long-End Yield Level** is directly observable and closely related to starting income, but may overlap materially with ETF yield / carry.

This ETF-by-ETF application test should help decide which candidates deserve canonical Component status.

### 8.3.5 Instrument-level yield / carry

Instrument-level yield / carry should **not** be treated as Instrument Quality.

Higher yield is not evidence that an ETF is a better-constructed instrument.

Yield / carry belongs on the **economic-evaluation side** because it contributes to the expected economics of holding the bond exposure.

The exact placement remains open:

```text
Rates Valuation / Compensation Evaluation
Credit Evaluation
or
a later explicit Carry / Income Evaluation
```

depending on the exposure.

The main design risk is double counting because:

```text
Term Premium
Real Yield
Credit Spread Level
ETF yield / carry
```

can contain overlapping compensation information.

The decision should therefore be based on incremental information value, not on adding every available yield measure.

### 8.3.6 Underlying rate volatility

Generic `rate volatility` should be split into distinct concepts.

```text
Underlying Rate Volatility
→ candidate canonical Component / market-derived evaluation input

Positioning data
→ Positioning Overlay

ETF realized price volatility
→ ETF Price Review
```

Underlying rate volatility may reduce the attractiveness of extreme duration exposure even when the directional Duration Evaluation is favorable.

It should not be classified as Positioning merely because both can restrain implementation.

## 8.4 Exposure / Market Evaluation

The four market-derived evaluations collectively determine whether an ETF is economically appropriate under the current bond environment.

The initial result should be an evaluation vector rather than an assumed weighted sum:

```text
ETF Market Evaluation
├── Final Duration Evaluation
├── Final Curve Evaluation
├── Final Credit Evaluation
└── Rates Valuation / Compensation Evaluation
```

These may later be combined through rule-based logic, eligibility rules, caps, scoring, or a hybrid approach.

The output is the **Exposure / Market Evaluation**.

## 8.5 Positioning Evaluation / Overlay

Positioning is an exposure-level implementation context rather than an intrinsic ETF property.

Possible inputs include:

- crowding;
- sentiment;
- speculative positioning;
- unusual directional consensus;
- exposure-level extension after a large market move;
- other indicators of implementation risk.

Positioning does not redefine the economic merits already represented by the market-derived evaluations.

It asks:

> **Even if the exposure is economically attractive, should implementation intensity be restrained because the exposure is unusually crowded, extended, or difficult to express cleanly?**

```text
Exposure / Market Evaluation
        +
Positioning Evaluation
        ↓
Positioning-adjusted Exposure Evaluation
```

Possible effects may include:

```text
pass-through
weaken implementation preference
cap aggressive expression
prefer a less-extreme maturity / duration implementation
reduce implementation intensity
```

Illustrative application:

```text
20+Y Treasury ETF

Exposure / Market Evaluation
→ strong

Positioning evidence
→ unusually bullish long-duration consensus
→ heavy long-duration crowding
→ large rally already realized

Positioning Overlay
→ preserve the favorable economic view
→ reduce preference for the most aggressive long-duration implementation

Possible result:
20+Y ETF  → downgraded / smaller implementation
7–10Y ETF → remains eligible or preferred
```

This should be interpreted as:

```text
Economic thesis remains valid.
Implementation intensity is restrained.
```

not:

```text
The Duration thesis was invalidated.
```

The output is the **Exposure-qualified Candidate Set**.

## 8.6 Instrument Quality Evaluation

Instrument Quality is:

> **The degree to which an ETF provides its intended Exposure Profile reliably, efficiently, and with acceptable implementation friction.**

Typical inputs include:

- expense ratio / total implementation cost;
- liquidity;
- bid-ask spread;
- tracking quality.

Instrument Quality does **not** determine what bond exposure the current market calls for.

It evaluates whether an ETF is a sufficiently good vehicle for implementing an exposure that has already passed the market and Positioning evaluations.

```text
Exposure-qualified ETF
        ↓
Instrument Quality
        ├─ minimum-quality filter
        └─ relative implementation ranking
```

The output is the **Implementation-qualified Candidate Set**.

## 8.7 Optional future ETF Price Diagnostics

ETF price-history analysis is **not part of the initial authoritative ETF-selection flow**.

Price history alone can support descriptive diagnostics such as recent return, drawdown, realized ETF price volatility, trend / extension, and historical percentile.

These outputs do not inherently imply buy / avoid / reject decisions.

A future optional `ETF Price Diagnostics` capability may be added if Bondview later defines a concrete use case. More decision-relevant diagnostics such as NAV dislocation, abnormal tracking, or liquidity breakdown require additional data beyond ETF price history and therefore should not be implied by a price-only module.


---

# 9. Aggregation and Final Selection

The master flow is:

```text
Canonical Components
+
ETF Exposure Profile
        ↓
Market-derived ETF Evaluations
   └─ dimension-specific macro effects applied internally
        ↓
Exposure / Market Evaluation
        ↓
Positioning Overlay
        ↓
Exposure-qualified Candidate Set
        ↓
Instrument Quality
        ↓
Implementation-qualified Candidate Set
        ↓
Final ETF Selection
```

A simple formula such as:

```text
Duration
+ Curve
+ Credit
+ Rates Valuation
+ Positioning
+ Instrument Quality
```

should not be assumed.

The stages do not play identical roles:

```text
Market-derived evaluations
→ Is this ETF economically appropriate?

Macro effects
→ Modify the economic evaluation inside the relevant dimension.

Positioning Overlay
→ Should implementation intensity be restrained despite economic attractiveness?

Instrument Quality
→ Is this ETF a sufficiently good implementation vehicle?

ETF price-history diagnostics
→ Optional descriptive context only; excluded from the initial authoritative selection flow.
```

Possible later aggregation methods inside Exposure / Market Evaluation include:

- weighted scoring;
- rule-based aggregation;
- eligibility / hard-fit checks followed by scoring;
- hybrid rules with caps or minimum requirements.

Positioning should normally act as a post-evaluation overlay rather than as an equal-weight peer score.

Instrument Quality should normally act as a downstream filter / ranker rather than as an equal-weight peer score.

ETF price-history analysis is excluded from the initial authoritative selection flow. A future optional diagnostics capability can be added if a concrete decision or monitoring use case emerges.

---

# 10. Macro Effects and Positioning in the Revised Structure

## 10.1 Macro effects

The previous architecture used:

```text
Market Components
→ Core Stance

Macro Components
→ Constraint Action

Core Stance + Constraint Action
→ Final Stance
```

That path is no longer authoritative because Stances no longer drive ETF Selection.

In the revised design, macroeconomic Components are consumed directly by the relevant market-derived ETF evaluator.

For example:

```text
Duration-related Components
+
ETF Duration Profile
        ↓
Core Duration Evaluation

Inflation Trend
+
Policy Direction
        ↓
Duration Macro Effect
        ↓
Final Duration Evaluation
```

and similarly:

```text
Credit-related Components
+
ETF Credit Profile
        ↓
Core Credit Evaluation

Growth / Inflation / Policy Components
        ↓
Credit Macro Effect
        ↓
Final Credit Evaluation
```

The economic action may still resemble earlier ideas such as:

```text
pass-through
weaken
cap
directional restriction
```

but old numeric Stance mechanics should not automatically be preserved.

A macro condition may affect ETFs with different exposure intensity differently.

For example, an adverse Duration macro effect may penalize a 20+Y Treasury ETF more strongly than a 7–10Y Treasury ETF.

Therefore:

> **Macro effects modify the economic evaluation inside a specific dimension.**

No separate `Macro Analysis Module` is required.

No upstream structural split between Market and Macro Components is required.

## 10.2 Positioning

Positioning is structurally different from macro effects.

```text
Macro Effect
→ internal modifier of a dimension-specific economic evaluation

Positioning Overlay
→ post-evaluation modifier of implementation willingness / intensity
```

Positioning operates after the market-derived evaluations have been combined into the Exposure / Market Evaluation.

It does not modify the underlying Duration, Curve, Credit, or Rates Valuation interpretation.

It is also distinct from optional ETF price-history diagnostics:

```text
Positioning
→ exposure-level crowding / sentiment / extension

ETF price-history diagnostics
→ descriptive history of the specific traded ETF
```

This distinction should be preserved in later architecture and vocabulary revisions.

---

# 11. Revised Design Sequence

The revised sequence is Component- and decision-driven.

```text
1. Define downstream ETF-selection information requirements
        ↓
2. Identify candidate canonical Components
        ↓
3. Consolidate and delimit the Component catalog
        ↓
4. Define Component semantics and calculations
        ↓
5. Validate Component coverage for ETF-selection decisions
        ↓
6. Define ETF Exposure Profile and market-derived evaluation dimensions
        ↓
7. Define dimension-specific ETF evaluation logic and macro effects
        ↓
8. Define Exposure / Market aggregation and Positioning Overlay
        ↓
9. Define Instrument Quality and the ETF Evaluation Module result boundary
        ↓
10. Define human-facing derived interpretations and diagnostic uses
        ↓
11. Validate diagnostics, explanation, and cross-module contracts
        ↓
12. Revisit optional ETF price-history diagnostics only if a concrete use case emerges
```

Steps 1–3 remain iterative:

```text
Decision requirements
        ↕
Candidate Components
        ↕
Canonical Component catalog
```

A candidate Component may reveal a missing decision requirement.

A downstream decision requirement may reveal that a Component has been omitted, duplicated, or defined at the wrong horizon.

The current high-level module structure is sufficiently stable that detailed choices inside Steps 2–10 are expected mainly to refine calculations and contracts rather than overturn the entire architecture.

---

# 12. Current Progress Against the Revised Sequence

## Step 1 — Define downstream ETF-selection information requirements

**Status: substantially started, not complete.**

Current identified dimensions / requirements include:

- outright rate / duration exposure;
- relative maturity / curve structure;
- credit-risk exposure;
- market-level rates compensation / valuation;
- ETF Exposure Profile requirements;
- instrument-level yield / carry where relevant;
- cash / low-risk alternative;
- positioning / crowding / sentiment effects on implementation intensity;
- implementation quality: fees / liquidity / bid-ask / tracking;
- ETF-specific price-review requirements;
- currency / hedging;
- macroeconomic effects on exposure suitability.

Remaining work:

- test Term Premium, Real Long-End Yield, Nominal Long-End Yield, and related candidates by how much incremental ETF-selection information each adds;
- determine whether bull / bear curve-driver information changes ETF choice beyond the existing Short-End / Long-End Yield Move Components;
- define the minimum ETF Exposure Profile required for evaluation;
- decide the exact economic-evaluation home for ETF-level yield / carry while preventing double counting;
- define Positioning Overlay inputs, semantics, and application rules;
- determine whether Underlying Rate Volatility deserves canonical Component status and how it modifies duration exposure.

## Step 2 — Identify candidate Components

**Status: substantially started.**

The current candidate catalog is listed in Section 5.

Remaining work includes:

- completing Credit-related candidates;
- deciding whether Growth is required;
- determining whether `Term Premium`, `Real Long-End Yield`, and/or `Nominal Long-End Yield Level` provide distinct enough information to retain;
- determining whether `Underlying Rate Volatility` deserves canonical Component status;
- reviewing whether any additional volatility / risk Components are required.

## Step 3 — Consolidate and delimit the Component catalog

**Status: partially started.**

Current important conclusions:

- Component identity is independent of Stance ownership;
- Market vs Macro is not a structural calculation distinction;
- Long-End Yield Move A and B are separate by default;
- Curve Movement is a canonical Component candidate;
- Curve Configuration is a canonical Component candidate;
- vague `Duration Compensation` is not preferred; preserve a specific concept if compensation is required.

Remaining work:

- assign semantic final names to A / B once horizons are understood;
- determine exact role of Term Premium / Real Long-End Yield;
- confirm whether Curve Movement is directly calculated from Yield Moves or requires additional representation;
- complete Credit and economic-condition catalog review;
- check for redundant or missing concepts.

## Step 4 — Define Component semantics and calculations

**Status: not ready for systematic execution.**

The model should not prematurely finalize:

- exact horizons;
- thresholds;
- transforms;
- State Classification;
- smoothing;
- hysteresis;

until the Step-3 catalog is sufficiently stable.

## Steps 5–10

**Status: conceptual discussion only.**

Some useful structure has already emerged for ETF evaluations and Stance interpretations, but detailed design should follow Component stabilization.

---

# 13. Step-5 Coverage Test

The coverage test is now more important than semantic symmetry across Stances.

Core question:

> **Can the canonical Component set distinguish all economically different ETF-selection cases that Bondview is expected to distinguish?**

Examples:

### Duration compensation

Do two environments with identical rate direction but very different term premium / real-yield conditions need different ETF decisions?

If yes, the necessary compensation concept must exist as a canonical Component.

The question is no longer:

```text
Does Duration Stance need compensation?
```

It is:

```text
Does ETF Selection need market-level duration-compensation information?
If yes, which canonical Component preserves it?
```

### Curve driver

Do bull steepener and bear steepener conditions lead to materially different ETF decisions after Duration and Curve Components are already considered?

If yes, the required short-end / long-end move information must remain available.

If no, bull / bear terminology can remain explanatory only.

### Information-loss rule

> **Any information required for authoritative ETF Selection must be preserved in canonical Components or ETF-specific inputs. It must not exist only inside a human-facing Stance interpretation.**

---

# 14. Relationship to Existing Design Work

## 14.1 Work that remains valuable

The redesign preserves much of the prior economic work:

- Component / Value / State concepts;
- canonical Component reuse;
- Duration directional concepts;
- Curve Configuration and Curve Movement analysis;
- Credit Spread Level / Direction;
- Inflation / Policy / Growth concepts;
- economic rule-case reasoning;
- separation of descriptive Component state from consumer-specific interpretation;
- Diagnostics and Historical Context principles;
- ETF instrument characteristics.

## 14.2 Work that changes role

The following concepts may remain useful but no longer occupy the same authoritative position:

- Duration / Curve / Credit Stances;
- Core Stance / Final Stance;
- Macro Constraint;
- Constraint Action;
- Bond-Exposure Stance Set.

They should be reviewed after the new architecture stabilizes.

## 14.3 Work that should not be mechanically preserved

The following assumptions should not be carried forward merely for backward compatibility:

- Stances are the authoritative inputs to ETF Selection;
- every relevant piece of market information must be compressed into a Stance;
- Duration / Curve / Credit require homogeneous output semantics;
- Market Components and Macro Components require separate upstream calculation paths;
- a simple Stance score is necessarily the correct target for macro adjustment.

---

# 15. Implications for Vocabulary and System Architecture

This review is intended to inform later authoritative document revisions, but this document does **not** modify those files.

The high-level structure is now relatively stable:

```text
Upstream Analysis Module
        ↓
Canonical Components
        ↓
ETF Evaluation Module
        ↓
Implementation-qualified Candidate Set
        ↓
Final ETF Selection
```

with human-facing Stances derived from Components rather than consumed by ETF Evaluation.

Most remaining decisions concern detailed Component content, evaluation semantics, aggregation, and thresholds rather than the existence of these major responsibilities.

## 15.1 Likely vocabulary work

Terms requiring review include:

- **Component**
- **Stance**
- **Stance Calculation Module**
- **Market Component**
- **Macro Component**
- **Bond-Exposure Stance Set**
- **Core Stance**
- **Final Stance**
- **Macro Constraint**
- **Constraint Action**
- **ETF Exposure Profile**
- **ETF Evaluation**
- **Exposure / Market Evaluation**
- **Positioning Overlay**
- **Instrument Quality**
- **ETF Price Review**
- **Candidate Set**
- names for the three major modules and their result boundaries.

Because these terms will be used repeatedly in detailed design, stabilizing vocabulary before extensive Step-4+ work should improve consistency and reduce rework.

## 15.2 Architecture readiness

The system architecture document is high-level enough that it does not need to wait for decisions such as:

- exact Term Premium methodology;
- Real Yield vs Nominal Yield thresholds;
- Positioning cap magnitudes;
- Instrument Quality thresholds;
- precise aggregation formulas.

Those belong in lower-level contracts.

Before revising the architecture document, the main architectural items that should be settled are:

1. final names of the major modules;
2. whether the ETF Evaluation / ETF Price Review split is accepted;
3. Result Boundary names;
4. formal status of Stances and retirement / redefinition of `Bond-Exposure Stance Set`.

Once those are settled, the architecture can be revised without waiting for every lower-level open decision.

---

# 16. Recommended Documentation Migration

The preferred documentation sequence is now:

```text
1. Stabilize this redesign review and major module boundaries
        ↓
2. Revise bondview_vocabulary.md
        ↓
3. Revise bondview_system_architecture.md using the stabilized vocabulary
        ↓
4. Continue detailed Component / ETF Evaluation design
        ↓
5. Review remaining detailed design documents
        ↓
6. Revise / split / merge / retire them as appropriate
```

Vocabulary is placed before architecture because the redesigned system introduces several recurring terms whose consistent use should make subsequent architecture and implementation-design work more efficient.

This review remains non-authoritative until those authoritative documents are revised.

---

# 17. Main Open Decisions

The remaining decisions should be separated into **architecture-level** and **lower-level design** items.

## 17.1 Architecture-level decisions

These can still materially affect the authoritative architecture document:

1. **Final name and boundary of the upstream analytical module**
2. **Final name of the ETF Evaluation Module**
3. **Exact Result Boundary of the ETF Evaluation Module**
4. **Role and formal status of Stances, including their diagnostic / sanity-check role**
5. **Whether `Bond-Exposure Stance Set` should remain a vocabulary term at all**
6. **Whether optional ETF Price Diagnostics should exist later as a non-authoritative capability**

The current expectation is that these decisions may adjust names and boundaries but are unlikely to reverse the Component-authoritative design.

## 17.2 Lower-level design decisions

These are important for implementation but are less likely to overturn the high-level structure:

1. **Final canonical Component catalog**
2. **Long-End Yield Move A / B semantic names and horizons**
3. **Whether Term Premium, Real Long-End Yield, and/or Nominal Long-End Yield Level provide distinct enough value**
4. **Whether Underlying Rate Volatility becomes a canonical Component**
5. **Exact Curve Evaluation semantics**
6. **Whether bull / bear curve-driver information changes ETF choice beyond existing Components**
7. **Credit Component completeness**
8. **Exact Rates Valuation / Compensation Evaluation inputs**
9. **Exact placement and semantics of ETF-level yield / carry**
10. **Minimum ETF Exposure Profile required for market-derived evaluations**
11. **Positioning Overlay inputs, semantics, and application mechanics**
12. **Instrument Quality thresholds and ranking semantics**
13. **Whether optional ETF Price Diagnostics are useful enough to add later**
14. **How macroeconomic Components modify ETF-specific evaluations**
15. **Whether a reusable `Constraint Action` abstraction remains useful**
16. **Exposure / Market Evaluation aggregation method**
17. **Final ETF selection / ranking method**

Most of these should refine evaluator behavior rather than change the major module topology.

---

# 18. Current Working Conclusion

The revised direction can be summarized as:

```text
Canonical Components
= authoritative analytical information

ETF Evaluation Module
= authoritative economic / implementation-quality evaluation
  using Components + ETF Exposure Profile

ETF price-history diagnostics
= excluded from the initial authoritative selection flow;
  optional later diagnostic capability only

Stances
= derived human-readable interpretations

Macro effects
= internal modifiers inside relevant market-derived ETF evaluations

Positioning
= post-evaluation overlay on implementation willingness / intensity

Instrument Quality
= downstream quality filter / ranker among economically suitable ETFs

Stances
= human-readable interpretations and historical sanity-check projections
  for validating Component behavior and parameter choices
```

The core selection flow is:

```text
Canonical Components
+
ETF Exposure Profile
        ↓
Market-derived ETF Evaluations
        ↓
Exposure / Market Evaluation
        ↓
Positioning Overlay
        ↓
Instrument Quality
        ↓
Implementation-qualified Candidate Set
        ↓
Final ETF Selection
```

The high-level structure is now expected to be more stable than the lower-level Component and evaluation details.

The immediate analytical work should continue to test the Component catalog and evaluation sufficiency, while the next documentation decision can reasonably focus on stabilizing module names and vocabulary before revising the system architecture.

