# Bondview v2 — Stance Design Draft: Duration

## Document Purpose

This document is a working model-design draft for Bondview v2 stance calculation.

It begins with stance-general concepts that are intended to be shared by Duration, Credit, and Curve, then defines the current first draft of the **Duration** stance in detail.

The objective is to establish the economic model before finalizing implementation mechanics such as exact transforms, thresholds, smoothing, hysteresis, configuration schema, or code structure.

The current system architecture and vocabulary remain authoritative for system-level responsibilities and terminology. This document focuses on stance-model content.

The intended development path is:

```text
shared stance-design structure
        ↓
Duration
        ↓
Credit
        ↓
Curve
        ↓
cross-stance review
        ↓
common mechanics extraction
        ↓
combined stance-design document
```

Open questions are intentionally collected in a dedicated section. As design decisions are resolved, they should be moved into the relevant substantive sections. The document approaches completion as the open-decision section becomes small or disappears.

---

# Part I. Stance-General Design

## 1. Common Conceptual Flow

Each stance answers one economic question about bond exposure.

The common conceptual structure is:

```text
Market Components
        ↓
Stance Rule Case
        ↓
Stance Rule Mapping
        ↓
Core Stance

Macro Components
        ↓
Constraint Rule Case
        ↓
Constraint Rule Mapping
        ↓
Constraint Action

Core Stance
     +
Constraint Action
        ↓
[Constraint Application]
        ↓
Final Stance
```

The market branch determines the **Core Stance**.

The macro branch does not independently recreate the stance. It determines a **Constraint Action** that may limit or adjust the expression of the Core Stance.

The resulting **Final Stance** becomes one element of the Bond-Exposure Stance Set consumed by ETF Selection.

---

## 2. Stance Design Sequence

The preferred design sequence is economic meaning first, implementation mechanics later:

```text
economic question
        ↓
Market Components and states
        ↓
Stance Rule Cases
        ↓
Stance Rule Mapping
        ↓
canonical Stance scale
        ↓
Macro Components and states
        ↓
Constraint Rule Cases
        ↓
Constraint Actions
        ↓
Constraint Application
        ↓
Final Stance
        ↓
raw observations / features / transforms
        ↓
horizons / thresholds / stabilization
        ↓
Model Configuration and implementation
```

The stance scale should follow the distinctions that are economically justified by the Stance Rule Cases rather than being imposed in advance.

Similarly, Constraint Actions should be derived from the economic meaning of the Constraint Rule Cases rather than from a desire to force a symmetric score system.

---

## 3. General Rule-Mapping Principles

### 3.1 Rule Cases

A Rule Case is a concrete combination of Component States.

A Stance Rule Case combines Market Component States and maps to a Core Stance.

A Constraint Rule Case combines Macro Component States and maps to a Constraint Action.

Each Rule Case should have an economically interpretable meaning.

### 3.2 Core Stance representation

A Stance label and its numeric score are two representations of the same Stance result.

For example:

```text
Core Stance
score = +3
label = strongly favor longer duration
```

The Rule Case itself does not have a separate independent score. It maps to the Core Stance, and the Core Stance carries the canonical score/label representation.

### 3.3 Constraint Application

Constraint Application should normally modify the permitted expression of the Core Stance rather than recreate a second independent stance.

Typical actions may include:

```text
pass-through
weaken
strengthen
magnitude cap
directional restriction
hard rejection
```

As a general stance-design principle:

- the market-derived Core Stance normally determines direction;
- Macro Constraints normally modify strength or permitted expression rather than recreate the stance;
- ordinary Constraint Actions should not reverse stance direction unless a stance-specific economic rule explicitly justifies that behavior;
- hard rejection or sign reversal should therefore be exceptional rather than routine.

The exact action set remains stance-specific. A stance may use only a subset of the available action types, and a stance may have no Macro Constraint at all.


### 3.4 Rule-based State Classification vs Rule Mapping

A Component State may itself require joint interpretation of multiple lower-level model-ready inputs.

When discrete lower-level inputs are combined to derive one Component State, the operation is treated semantically as **rule-based State Classification**.

For example:

```text
broader realized-policy trajectory
        +
recent realized-policy action
        ↓
[rule-based State Classification]
        ↓
Policy Direction
```

Canonical **Rule Case / Rule Mapping** terminology remains reserved for model-level mappings in which Component States produce a Core Stance or Constraint Action:

```text
Market Component States
        ↓
Stance Rule Case
        ↓
Stance Rule Mapping
        ↓
Core Stance

Macro Component States
        ↓
Constraint Rule Case
        ↓
Constraint Rule Mapping
        ↓
Constraint Action
```

The underlying discrete-state mapping mechanics may be reusable across both levels even though the semantic roles remain distinct.

---

# Part II. Duration Stance

## 4. Duration Economic Question

Duration expresses whether longer- or shorter-duration bond exposure is favored by the current rates-market environment, subject to stance-specific macro constraints.

The first-draft structure is:

```text
Long-End Yield Trend
        ×
Recent Long-End Yield Move
        ↓
Stance Rule Case
        ↓
Core Duration Stance

Inflation Trend
        ×
Policy Direction
        ↓
Constraint Rule Case
        ↓
Constraint Action

Core Duration Stance
        +
Constraint Action
        ↓
Final Duration Stance
```

---

## 5. Duration Market Components

### 5.1 Long-End Yield Trend

**Economic meaning**

The broader or medium-horizon direction of long-term Treasury yields.

**States**

```text
falling
stable
rising
```

**Current candidate Raw Observations**

- FRED `DGS10` — 10-Year Treasury Constant Maturity Rate
- FRED `DGS30` — 30-Year Treasury Constant Maturity Rate

The authoritative long-end representation is not yet fixed. It may ultimately use:

- 10Y;
- 30Y;
- or a defined composite of multiple long-end maturities.

### 5.2 Recent Long-End Yield Move

**Economic meaning**

A shorter-horizon movement in long-end Treasury yields that indicates whether the latest market move confirms or challenges the broader Long-End Yield Trend.

**States**

```text
falling
stable
rising
```

**Current candidate Raw Observations**

Initially, the same long-end Treasury-yield observations as Long-End Yield Trend:

- FRED `DGS10`
- FRED `DGS30`

The distinction between the two Components is not necessarily the raw data source. It is primarily the economic horizon and transformation.

Conceptually:

```text
long-end Treasury-yield history
        ├── broader horizon ──→ Long-End Yield Trend
        └── shorter horizon ──→ Recent Long-End Yield Move
```

The Recent Long-End Yield Move is **not** currently defined from short-term Treasury yields.

### 5.3 Why short-end yields are not currently Duration Market Components

Short-end rates remain economically important, but the current design assigns their information elsewhere unless evidence shows that Duration needs an additional independent front-end signal.

Current separation:

```text
long-end yield behavior
→ Duration Market Components

realized Federal Reserve policy
→ Duration Macro Component: Policy Direction

relative front-end vs long-end behavior
→ primarily Curve

cash / short-bond attractiveness
→ ETF Selection / Instrument Evaluation
```

This avoids automatically using similar front-end information multiple times.

Short-end yields remain a future candidate only if historical analysis shows that they add information not already preserved by the current Duration design.

---

## 6. Duration Stance Rule Mapping

### 6.1 Stance Rule Table

The proposed complete 3 × 3 mapping is:

| Long-End Yield Trend ↓ / Recent Long-End Yield Move → | Falling | Stable | Rising |
|---|---:|---:|---:|
| **Falling** | **+3** | **+2** | **+1** |
| **Stable** | **+1** | **0** | **-1** |
| **Rising** | **-1** | **-2** | **-3** |

All nine combinations are considered economically meaningful in the first draft.

The broader trend determines the primary directional context, while the recent move confirms, pauses, or challenges that direction.

A counter-trend recent move does not automatically erase the broader trend.

### 6.2 Canonical Duration Stance Scale and Rule-Case Interpretations

The seven-level Duration scale is derived from the economic distinctions found across the nine Stance Rule Cases.

The score and label represent the same Core Stance result.

| Score | Duration Stance | Stance Rule Case interpretation(s) |
|---:|---|---|
| **+3** | **strongly favor longer duration** | falling trend + recent falling → falling trend continuing / strengthening |
| **+2** | **favor longer duration** | falling trend + recent stable → falling trend intact, recent pause |
| **+1** | **mildly favor longer duration** | falling trend + recent rising → falling trend challenged by a counter-move<br>stable trend + recent falling → emerging downward move |
| **0** | **neutral** | stable trend + recent stable → no clear directional signal |
| **-1** | **mildly favor shorter duration** | stable trend + recent rising → emerging upward move<br>rising trend + recent falling → rising trend challenged by a counter-move |
| **-2** | **favor shorter duration** | rising trend + recent stable → rising trend intact, recent pause |
| **-3** | **strongly favor shorter duration** | rising trend + recent rising → rising trend continuing / strengthening |

This table explains where the seven canonical Stance levels come from.

There are nine Rule Cases but only seven Stance results because two pairs of economically different Rule Cases are judged to justify the same stance strength:

```text
+1:
falling trend challenged by recent rise
stable trend with emerging fall

-1:
stable trend with emerging rise
rising trend challenged by recent fall
```

This is provisional and should be validated before implementation.

---

## 7. Duration Macro Components

### 7.1 Inflation Trend

**Economic meaning**

The direction of inflation pressure relevant to the attractiveness of Duration exposure.

**States**

```text
falling
stable
rising
```

**Current candidate Raw Observations**

Primary candidates from FRED:

- `PCEPI` — Personal Consumption Expenditures Price Index
- `PCEPILFE` — Personal Consumption Expenditures Excluding Food and Energy

The authoritative inflation measure is not yet fixed.

The eventual Component may use:

- headline PCE;
- core PCE;
- or a deliberately defined combination.

The goal is to classify inflation direction, not merely the current inflation level.

### 7.2 Policy Direction

**Economic meaning**

The direction of realized Federal Reserve policy.

**States**

```text
easing
stable
tightening
```

**Current candidate Raw Observations**

Preferred FRED candidates:

- `DFEDTARL` — Federal Funds Target Range, Lower Limit
- `DFEDTARU` — Federal Funds Target Range, Upper Limit

A target-range midpoint may be derived from the two series.

`DFF` — Effective Federal Funds Rate — may be useful as an alternative or diagnostic series but is not currently preferred as the authoritative policy input.

### 7.3 Policy Direction State Classification

The initial Policy Direction design is based on **realized policy history**, not on a forecast of the next FOMC decision.

A single latest policy move should not automatically determine the Component State because the federal-funds target rate changes as a step function rather than as a smooth market series.

For example, one hike after an extended easing cycle should not necessarily be interpreted in the same way as one hike within an established tightening cycle.

Policy Direction therefore remains one Macro Component, but its State Classification may use two lower-level features with separate horizons:

```text
Fed target-rate history
        ↓
broader realized-policy trajectory
        +
recent realized-policy action
        ↓
[rule-based State Classification]
        ↓
Policy Direction
    easing / stable / tightening
```

Conceptually:

- **broader realized-policy trajectory** describes the prevailing policy path over a longer horizon;
- **recent realized-policy action** captures the latest decision or shorter sequence of decisions;
- their joint interpretation determines the Policy Direction State.

The exact classification table is not yet defined.

A possible pattern is:

```text
broader easing + recent easing
→ easing

broader easing + recent hold
→ easing or stable depending on persistence

broader easing + isolated recent hike
→ transitional interpretation, likely stable under the current three-state system

broader tightening + recent tightening
→ tightening

broader tightening + recent hold
→ tightening or stable depending on persistence

broader tightening + isolated recent cut
→ transitional interpretation, likely stable under the current three-state system
```

The purpose is to prevent one isolated move from causing an unjustified regime flip while still allowing a genuine new policy sequence to change the state reasonably quickly.

This is **rule-based State Classification**, not a new Constraint Rule Case and not an additional Macro Component.

Market-implied policy expectations such as Fed-funds futures are not currently authoritative inputs to Policy Direction.

They may remain diagnostic or become a separate future Component only if later evidence justifies that change.

---

## 8. Duration Constraint Rule Mapping

### 8.1 Constraint Rule Space

The initial Macro Components create:

```text
Inflation Trend
    falling
    stable
    rising

×

Policy Direction
    easing
    stable
    tightening

=

9 Constraint Rule Cases
```

All nine combinations are valid economic regimes.

Mixed combinations such as:

```text
inflation falling + policy tightening
inflation rising + policy easing
```

are not errors or missing states. They may represent transition, policy lag, or disagreement between inflation conditions and realized policy direction.

### 8.2 Current Constraint Design Principle

The Duration design follows the general conservative constraint principle defined in Part I.

The first-draft Duration Macro Constraint therefore uses the macro regime primarily to limit excessive expression of an opposing Core Duration Stance:

- strongly supportive macro conditions may limit strongly negative Duration exposure;
- strongly adverse macro conditions may limit strongly positive Duration exposure;
- mixed conditions are generally pass-through;
- the current Duration action set does not reverse stance direction;
- whether supportive macro conditions should ever actively strengthen a same-direction Core Stance remains open.

### 8.3 Provisional Constraint Rule Table

| Inflation Trend ↓ / Policy Direction → | Easing | Stable | Tightening |
|---|---|---|---|
| **Falling** | **cap negative at -1** | **cap negative at -2** | **pass-through** |
| **Stable** | **cap negative at -2** | **pass-through** | **cap positive at +2** |
| **Rising** | **pass-through** | **cap positive at +2** | **cap positive at +1** |

This table is more provisional than the Duration Stance Rule Table.

It should be validated against the full Core-Stance × Constraint-Case outcome matrix before being treated as stable design.

---

## 9. Duration Constraint Actions and Application

The current minimal action set is:

| Constraint Action | Effect |
|---|---|
| **pass-through** | Leave Core Stance unchanged. |
| **cap positive at +2** | Reduce positive values above +2 to +2; leave all other values unchanged. |
| **cap positive at +1** | Reduce positive values above +1 to +1; leave all other values unchanged. |
| **cap negative at -2** | Raise negative values below -2 to -2; leave all other values unchanged. |
| **cap negative at -1** | Raise negative values below -1 to -1; leave all other values unchanged. |

For example:

```text
Core Stance = +3
Constraint Action = cap positive at +1
→ Final Stance = +1

Core Stance = -2
Constraint Action = cap positive at +1
→ Final Stance = -2
```

Constraint Actions are directional caps: they constrain an opposing stance when applicable and otherwise behave as no-ops.

Ordinary Duration constraints do not reverse stance direction.

Constraint Rule Mapping selects the action; Constraint Application applies that action consistently to the supplied Core Stance.

---

## 10. Raw Observation Candidates

The following series are current candidates rather than final data contracts.

| Purpose | Candidate FRED series | Current role |
|---|---|---|
| Long-end Treasury yield | `DGS10` | candidate input for both Duration Market Components |
| Longer-end Treasury yield | `DGS30` | candidate input for both Duration Market Components |
| Headline inflation | `PCEPI` | candidate input for Inflation Trend |
| Core inflation | `PCEPILFE` | candidate or secondary input for Inflation Trend |
| Fed target lower bound | `DFEDTARL` | likely Policy Direction input |
| Fed target upper bound | `DFEDTARU` | likely Policy Direction input |
| Effective Fed funds rate | `DFF` | alternative / diagnostic |

### 10.1 Currently excluded or diagnostic-only candidates

The following may help explain Duration behavior but are not currently Rule Dimensions:

```text
short-end Treasury yields
Fed-funds futures / expected policy path
TIPS real yields
breakeven inflation
term premium
Treasury supply / fiscal measures
yield-move driver decomposition
extraordinary short-lived rate shock
```

These should not become new Components merely because the data is available.

Promotion to a Component should require evidence that the information creates a durable economically meaningful distinction not already represented by the current model.

---

## 11. Duration Model Configuration Requirements

The exact serialization format and Configuration Schema are not yet defined.

The Duration Model Configuration should describe the model at its semantic layers without assuming that every layer uses different implementation mechanics.

The current requirement is:

```text
Raw Observations
        ↓
Feature definitions
    transformation
    horizon / lookback
    smoothing / aggregation where needed
        ↓
Component State Classification
        ↓
Component States
        ↓
Stance / Constraint Rule Mapping
        ↓
Core Stance / Constraint Action
```

Equivalent discrete-state mapping mechanics may be reusable inside both **rule-based State Classification** and **Stance / Constraint Rule Mapping**, while the configuration should preserve their different semantic roles.

### 11.1 Feature definitions and horizons

Lookback horizons belong primarily to **Features**.

A Feature definition may therefore need:

- Raw Observation source(s);
- transformation;
- horizon / lookback;
- aggregation method where multiple observations are used;
- smoothing method, if any;
- source-data frequency and alignment rules;
- missing-data behavior;
- historical `as_of` / release-availability handling where required.

There is no requirement that one Component have only one horizon.

If a Component State is derived from multiple Features, each Feature may use its own horizon.

For example:

```text
Policy Direction

Feature A:
    broader realized-policy trajectory
    horizon: TBD longer horizon

Feature B:
    recent realized-policy action
    horizon: TBD shorter horizon

Feature A input + Feature B input
        ↓
[rule-based State Classification]
        ↓
Policy Direction
```

Likewise:

```text
Long-End Yield Trend Feature
    horizon: TBD broader horizon

Recent Long-End Yield Move Feature
    horizon: TBD shorter horizon
```

even when both consume the same Treasury-yield Raw Observations.

### 11.2 Component State Classification

Component State Classification consumes current model-ready Feature representations and produces a Component State.

The configuration should support at least:

- threshold- or bucket-based classification from one model-ready Feature;
- rule-based State Classification when multiple lower-level discrete inputs jointly determine one Component State;
- state thresholds or boundaries where applicable;
- transition, persistence, or hysteresis rules where justified.

For example, Policy Direction may use:

```text
broader policy-trajectory input
        +
recent policy-action input
        ↓
[rule-based State Classification]
        ↓
easing / stable / tightening
```

This internal mapping remains **State Classification**, not a Stance Rule Case or Constraint Rule Case.

### 11.3 Stance and Constraint Rule Mapping

After Component States are available, Stance and Constraint Rule Mapping consume the current states without introducing another lookback horizon.

Conceptually:

```text
Market Component States
        ↓
Stance Rule Mapping
        ↓
Core Stance

Macro Component States
        ↓
Constraint Rule Mapping
        ↓
Constraint Action
```

The configuration should therefore be able to specify:

- participating Component States;
- Rule Case coverage;
- mapped Core Stance or Constraint Action;
- fallback or interpolation behavior where the stance-specific design permits it.

The underlying mapping capability may reuse generic discrete-state mapping mechanics also used by rule-based State Classification, but the semantic configuration remains distinct.

### 11.4 Feature horizon vs temporal stabilization

A Feature horizon defines the historical lookback used to produce a current model-ready measure.

It is not necessarily a moving-average window. A Feature may later use, for example:

```text
moving-average difference
regression slope
cumulative change
smoothed change
another justified transformation
```

Component or stance-level temporal persistence, if needed, is a separate concept.

For example:

```text
new candidate Policy Direction = tightening

but
previous state = easing
and
only one opposing policy move has occurred

→ transition / persistence logic may prevent an immediate full regime flip
```

Such behavior should be configured as State Classification or stabilization logic rather than as an additional Feature horizon.

Likewise, if a future stance requires confirmation across multiple calculation dates before changing, that should be treated as stance-level stabilization rather than another market-data lookback horizon.

### 11.5 Short-lived events

The model is not intended to capture every sub-week market shock immediately.

The working assumption is:

```text
temporary event
→ reverses quickly
→ broader Features should largely ignore it

persistent event
→ changes market behavior beyond the event window
→ later appears in the relevant Feature and Component State
```

The shorter Recent Long-End Yield Move Feature provides more responsiveness than the broader Long-End Yield Trend Feature without turning Duration into an event-trading model.

---

## 12. Validation Requirements

### 12.1 Stance Rule validation

Confirm that all nine market combinations remain economically meaningful and that the seven canonical stance outcomes provide sufficient resolution.

Questions include:

- Do all nine Rule Cases have a defensible interpretation?
- Are +1 and -1 appropriately shared by two distinct cases each?
- Does a counter-trend recent move reduce but not immediately reverse the broader trend?
- Is the seven-level scale necessary, or would a smaller scale preserve the same useful distinctions?

### 12.2 Constraint Application validation

Generate:

```text
7 Core Stances
×
9 Constraint Rule Cases
=
63 outcomes
```

Review for:

- monotonicity;
- unintended sign reversal;
- inconsistent treatment of adjacent macro regimes;
- constraints that are too weak to matter;
- constraints that are so strong that market-derived Core Stance becomes irrelevant.

### 12.3 Full Duration composition validation

Generate:

```text
9 Stance Rule Cases
×
9 Constraint Rule Cases
=
81 derived Final Stances
```

Review the complete distribution for:

- excessive clustering at one Final Stance;
- unexpected extreme outcomes;
- non-monotonic macro effects;
- discontinuities between similar regimes;
- evidence that two market Rule Cases mapped to the same Core Stance actually require different macro treatment.

If the last issue appears repeatedly, the Core Stance representation may be compressing away information needed by the constraint layer.

The 81 outcomes are validation results, not 81 independently authored economic rules.

---

## 13. Result Traceability for Diagnostics

The exact Result Contract is not yet defined, but Duration results should preserve enough of the **authoritative calculation path** to explain how the Final Stance was produced and to support later Diagnostics and Historical Context without reconstructing that path unnecessarily.

This section concerns preservation of the stance-calculation trace, not the addition of separate diagnostic-only market inputs.

Likely useful information includes:

```text
Market Component Values / States
Stance Rule Case
Core Stance score / label

Macro Component Values / States
Constraint Rule Case
Constraint Action

Final Stance score / label
```

This would allow later diagnostics such as:

- how often the current Stance Rule Case occurred historically;
- when the same Constraint Rule Case occurred;
- when Core and Final Stance differed;
- how subsequent yields or ETF total returns behaved.

Historical outcomes remain explanatory and should not directly modify authoritative stance calculation unless a future architecture decision explicitly changes that principle.

---

## 14. Additional Considerations / Open Decisions

This section should shrink as the Duration design matures.

Resolved items should be moved into the relevant substantive section rather than left here.

### 14.1 Higher priority — economic model

- Confirm the seven-level canonical Duration stance scale.
- Confirm the complete 3 × 3 Stance Rule Table.
- Confirm the complete 3 × 3 Constraint Rule Table.
- Validate the five current directional-cap Constraint Actions.
- Decide whether supportive macro conditions may ever actively `strengthen` a same-direction Core Stance rather than merely limit an opposing stance.
- Decide whether Duration needs any hard-rejection or sign-reversal condition at all.

### 14.2 Required before implementation

- Choose the authoritative long-end yield representation: 10Y, 30Y, or composite.
- Define the Long-End Yield Trend Feature horizon.
- Define the Recent Long-End Yield Move Feature horizon.
- Define each market Feature transformation.
- Define falling / stable / rising classification thresholds.
- Choose headline PCE, core PCE, or another deliberate inflation representation.
- Define the Inflation Trend Feature horizon and transformation.
- Define the broader realized-policy trajectory Feature and its horizon.
- Define the recent realized-policy action Feature and its horizon.
- Define the rule-based State Classification table that maps those lower-level policy inputs to `easing / stable / tightening`.
- Define how isolated opposing policy moves and sequences of policy holds affect transitions among Policy Direction states.
- Define whether smoothing is necessary.
- Define whether additional stabilization / hysteresis is necessary for any Component beyond the explicit Policy Direction transition logic.
- Define source-frequency alignment and missing-data behavior.
- Define historical data-availability semantics to prevent look-ahead.

### 14.3 Explicitly deferred

- Short-end Treasury yields as an additional Duration Market Component.
- Expected Policy Direction from Fed-funds futures.
- Real-yield vs nominal-yield decomposition as a Rule Dimension.
- Breakeven inflation as a Rule Dimension.
- Term premium as a Rule Dimension.
- Treasury supply / fiscal variables as Rule Dimensions.
- A distinct extraordinary short-horizon `rate shock` Component.

These items may remain in Diagnostics unless later evidence demonstrates a stable economic distinction that the current Duration model fails to capture.

---

## 15. Current Draft Summary

The first Duration draft is:

```text
MARKET

Long-End Yield Trend
        ×
Recent Long-End Yield Move
        ↓
9 Stance Rule Cases
        ↓
7-level Core Duration Stance


MACRO

Inflation Trend
        ×
Policy Direction
        ↓
9 Constraint Rule Cases
        ↓
directional magnitude cap / pass-through


INTEGRATION

Core Duration Stance
        +
Constraint Action
        ↓
Final Duration Stance
```

Current maturity assessment:

```text
Market Component structure
→ relatively strong

9-case Stance Rule structure
→ relatively strong, still to validate

7-level canonical Stance scale
→ plausible and currently complete

Macro Component structure
→ strong candidate

Policy Direction internal State Classification
→ conceptually clarified; Feature horizons and classification table still provisional

Constraint Rule Table
→ provisional

Constraint Action mechanics
→ simple and explicit, requires 63/81-case validation

Raw observations / Feature horizons / transforms / thresholds
→ intentionally unresolved

Configuration semantics
→ horizons belong to Features; State Classification and Rule Mapping remain distinct semantic layers that may reuse common discrete-state mapping mechanics
```
