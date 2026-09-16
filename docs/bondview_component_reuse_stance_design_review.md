# Bondview Component Reuse and Stance Construction — Design Review

## Document Status

**Status:** Review-stage design note  
**Authority:** Non-authoritative  
**Purpose:** Evaluate a limited refinement to the current Bondview stance architecture before deciding whether authoritative documents should be changed.

This document is intended to supersede `bondview_stance_cross_review_notes.md` as the current review reference for this topic. It does **not** itself change the definitions in:

- `docs/bondview_vocabulary.md`
- `docs/bondview_system_architecture.md`
- `docs/bondview_stance_design_draft.md`

If the proposal in this document is accepted, those authoritative or more specific design documents should be updated directly and this review note can then be retired.

---

## 1. Review Question

The current architecture is organized around:

```text
Market Components
        ↓
Stance Rule Case
        ↓
Core Stance

Macro Components
        ↓
Constraint Rule Case
        ↓
Constraint Action

Core Stance + Constraint Action
        ↓
Final Stance
```

The current system architecture also states that each stance owns the Components and rule structure needed to answer its own economic question.

Recent Duration / Curve discussion exposed a possible limitation in interpreting that ownership too strictly.

Several economically meaningful market concepts may be useful to more than one analytical responsibility. If the same derived concept has the same economic meaning wherever it is used, recalculating or redefining a stance-specific version of that concept creates unnecessary duplication and can produce inconsistent semantics.

The proposed refinement is therefore:

> **A Component is a canonical analytical concept within Bondview and may be consumed by one or more Stances. A Component does not inherently belong to exactly one Stance. Each Stance selects the Component States relevant to its own economic question and interprets them through its own Stance Rule Mapping.**

This proposal changes Component ownership and reuse semantics, but does **not** require a new processing layer between Component and Stance.

---

## 2. What Would Remain Unchanged

The proposal is intentionally narrower than a redesign of the stance architecture.

The following structure would remain:

```text
Raw Observations
        ↓
Features
        ↓
Components
        ↓
Stance-specific Rule Cases
        ↓
Stance-specific Rule Mapping
        ↓
Core Stance
        ↓
stance-specific Macro Constraint
        ↓
Final Stance
```

Duration, Curve, and Credit remain separate Stances.

Each Stance still has:

- its own economic question;
- its own selected Rule Dimensions;
- its own Stance Rule Cases;
- its own Stance Rule Mapping;
- its own Core Stance result;
- its own Macro Constraint logic where justified;
- its own Final Stance result.

The Bond-Exposure Stance Set still preserves Final Duration, Final Curve, and Final Credit separately rather than collapsing them into one aggregate score.

ETF Selection remains downstream and does not recreate stance calculation.

---

## 3. Proposed Component Model

### 3.1 Canonical Component identity

Under the proposal, a Component is defined independently of the Stance that consumes it.

For a shared Component, the following must be canonical within Bondview:

- Component name;
- economic definition;
- Raw Observation / Feature lineage;
- Component Value calculation;
- State Classification;
- Component State labels and their meanings.

For example:

```text
Component:
Long-End Yield Trend

Economic meaning:
broader direction of long-term Treasury yields

States:
falling
stable
rising
```

If Duration and another analytical responsibility both consume `Long-End Yield Trend`, then:

```text
Long-End Yield Trend = rising
```

must mean exactly the same market condition in both places.

A Stance must not create its own alternative meaning of `rising` for the same Component.

### 3.2 Descriptive Components, interpretive Stances

A Component State should normally be descriptive rather than a universal judgment of attractiveness.

For example:

```text
Long-End Yield Trend = rising
```

describes a market state.

It should not automatically mean:

```text
Component score = -1
```

if `-1` is intended to mean "unfavorable."

The economic consequence of the state depends on the Stance that consumes it.

The preferred separation is:

```text
Component State
= what economic state exists?

Stance Rule Mapping
= what does the relevant combination of states imply
  for this exposure dimension?
```

A numeric Component Value may of course remain canonical when it measures the Component itself, for example:

```text
Long-End Yield Trend Value = +18 bp
State = rising
```

The caution applies to a universal **favorability score**, not to descriptive numeric values.

---

## 4. Proposed Stance Definition

The current vocabulary defines a Stance as:

> An analytical view about one dimension of bond exposure.

That definition is directionally correct but leaves room for ambiguity around words such as *favorable* or *attractive*. In particular, it can be unclear whether a Stance means:

1. preferred positioning **within one exposure dimension**, or
2. an absolute judgment that a bond exposure or ETF should be owned.

The proposed review-stage definition is:

> **Stance:** an exposure-oriented analytical result for one bond-exposure dimension, produced by applying stance-specific Rule Mapping to selected canonical Market Component States and, where applicable, stance-specific Macro Constraints. A Stance expresses preferred positioning within its exposure dimension; it is not by itself an absolute investment-attractiveness judgment or an ETF recommendation.

This gives the three Stances different exposure questions without requiring each to be a complete description of the bond market.

Illustratively:

```text
Duration
→ preferred positioning along the duration / rate-sensitivity dimension

Curve
→ preferred positioning along the relative maturity / curve dimension

Credit
→ preferred positioning along the credit-risk dimension
```

The distinction between Core and Final Stance remains:

```text
selected Market Component States
        ↓
Stance Rule Mapping
        ↓
Core Stance
        +
stance-specific Macro Constraint
        ↓
Final Stance
```

### 4.1 Does this resolve the previous ambiguity?

**At the conceptual level, mostly yes.**

The definition deliberately avoids using *favorable* as an undefined synonym for absolute attractiveness. It confines Stance meaning to **relative positioning within one defined exposure dimension**.

The following remains outside Stance:

- whether the overall bond allocation is attractive versus cash or another asset class;
- whether a particular ETF offers sufficient yield/carry;
- ETF fees, liquidity, tracking, hedging, and other instrument characteristics;
- whether Positioning Context makes an otherwise valid exposure difficult to implement.

However, exact output semantics for Curve and Credit still need their stance-specific designs to be completed. The general definition can be settled before every individual label or scale is settled.

---

## 5. Rule Mapping When Components Are Not Stance-Owned

The proposal does **not** create one universal Rule Mapping across all Stances.

Instead:

```text
Canonical Component Catalog
        ↓
each Stance selects relevant Components
        ↓
those selected Component States become
that Stance's Rule Dimensions
        ↓
stance-specific Rule Cases
        ↓
stance-specific Rule Mapping
        ↓
Core Stance
```

Conceptually:

```text
Components
├── Component A
├── Component B
├── Component C
├── Component D
└── Component E

Duration consumes: A, B, C
Curve consumes:    A, D, E
Credit consumes:   C, E
```

`A`, `C`, or `E` do not change meaning when reused.

What changes is the **joint rule case in which they participate** and the **Stance result to which that rule case maps**.

This is the key distinction:

> **Component semantics are canonical; Stance interpretation is contextual.**

---

## 6. Cross-Stance Component Reuse — Concrete Mapping Examples

The mechanics of reuse are clear. The exact economic mappings below are partly illustrative because the Curve model and Duration compensation model are not yet finalized.

These examples therefore show **how** shared Components would work, not necessarily the final Bondview Rule Tables.

### 6.1 Example A — `Curve Configuration` reused by Duration and Curve

Assume the canonical Component:

```text
Component:
Curve Configuration

States:
inverted
roughly flat
positively sloped
```

Its meaning is the same everywhere.

#### Use in Curve

A possible Curve Rule Case could combine:

```text
Curve Configuration
        ×
Curve Movement
```

Illustrative cases:

| Curve Configuration | Curve Movement | Illustrative Curve interpretation |
|---|---|---|
| Inverted | Steepening | normalization / steepening case |
| Inverted | Flattening | deeper-inversion / flattening case |
| Positive | Steepening | further-steepening case |
| Positive | Flattening | flattening case |

The authoritative Curve Stance labels and mapping are **not yet settled**.

#### Use in Duration

The same `Curve Configuration` could also contribute to a future Duration compensation or valuation Rule Case because the attractiveness of long-duration exposure may depend partly on how long yields compare with short rates.

For example, a future Duration structure might be:

```text
Long-End Yield Directional Case
        ×
Duration Compensation State
        ↓
Core Duration Stance
```

and `Duration Compensation State` might itself be classified using inputs including:

```text
long-end nominal yield
real yield or term-premium information
Curve Configuration
```

In this use:

```text
Curve Configuration = inverted
```

does not mean something different.

It is the same canonical market state, but it contributes to a different analytical question: whether current compensation for accepting duration risk is attractive, neutral, or unattractive.

**Important:** whether `Curve Configuration` should actually be an input to Duration Compensation is still unresolved. The example demonstrates the reuse mechanism.

---

### 6.2 Example B — `Long-End Yield Trend` reused in different Stance Rule Cases

Assume:

```text
Long-End Yield Trend
= falling / stable / rising
```

#### Duration mapping

The current Duration draft already uses:

```text
Long-End Yield Trend
        ×
Recent Long-End Yield Move
        ↓
Duration Stance Rule Case
        ↓
Core Duration Stance
```

Illustratively:

```text
Long-End Yield Trend = rising
Recent Long-End Yield Move = rising
→ confirmed yield-rise Duration case
→ shorter-duration preference
```

Here `rising` matters because Duration asks about rate sensitivity.

#### Possible Curve use

A future Curve model may need information about which part of the curve is driving a curve move. If so, it could reuse `Long-End Yield Trend` or a more appropriately horizon-aligned long-end movement Component together with Curve-specific Components.

For example:

```text
Curve Movement = steepening
Long-End Move = rising
        ↓
Curve Rule Case concerned with
long-end-led steepening
```

while:

```text
Curve Movement = steepening
Long-End Move = stable/falling
        ↓
Curve Rule Case concerned with
front-end-led steepening
```

The same long-end state is descriptive in both Duration and Curve.

However, there is a design caution:

> If Curve uses long-end rate direction only to recreate `bull steepener`, `bear steepener`, and similar labels inside the authoritative Curve Stance, Curve may begin to reproduce the outright-rate dimension already expressed through Duration.

Therefore this reuse is **possible but not yet accepted as a final Curve Rule Dimension**.

The unresolved question is not whether the Component can technically be reused. It is whether long-end direction economically belongs in the authoritative Curve Stance or only in cross-stance / diagnostic interpretation.

---

### 6.3 Example C — shared Macro Component with different constraint mappings

Shared Component reuse is easier to illustrate on the Macro side because the same macro condition can legitimately have different implications for different exposures.

Assume the canonical Macro Component:

```text
Policy Direction
= easing / stable / tightening
```

The Component itself remains identical.

#### Duration Constraint Rule Mapping

A Duration constraint case might be:

```text
Inflation Trend = falling
Policy Direction = easing
        ↓
Duration Constraint Rule Mapping
        ↓
cap strongly negative Duration expression
```

The reasoning is that falling inflation plus realized easing may make an extreme shorter-duration stance harder to justify.

#### Credit Constraint Rule Mapping

A Credit constraint case could use the same:

```text
Policy Direction = easing
```

together with a different Macro Component such as Growth:

```text
Growth = weakening
Policy Direction = easing
        ↓
Credit Constraint Rule Mapping
        ↓
Credit-specific Constraint Action
```

The Credit action need not match the Duration action, because easing during weakening growth may have different implications for credit risk than for rate duration.

Thus:

```text
Policy Direction = easing
```

has one canonical meaning, while its **stance-specific effect** is determined by the Rule Case in which it participates.

The exact Credit constraint action is not yet specified here.

---

## 7. Why This Is Different From a Universal Component Score

Suppose:

```text
Long-End Yield Trend = rising
```

A universal score such as:

```text
rising = -1
```

would silently assume that `rising` is unfavorable in every use.

That may be meaningful for Duration but not for Curve.

For Curve, long-end rates rising could participate in:

- steepening;
- flattening;
- a parallel move;
- a long-end-led move;
- a broader rates regime whose curve implication depends on the short end.

Therefore the proposal prefers:

```text
canonical Component State
        +
stance-specific Rule Case
        ↓
stance-specific Stance result
```

rather than:

```text
canonical Component State
        ↓
universal favorability score
        ↓
all Stances
```

This preserves reuse without forcing one Stance's interpretation into the Component itself.

---

## 8. Semantic Depth Reframed

Earlier discussion considered whether Duration, Curve, and Credit should have approximately equal semantic depth.

The shared-Component proposal suggests a better target:

> **The Component set should provide a coherent and sufficiently rich description of the market states Bondview needs. Each Stance should then contain enough information to answer its own exposure question, but the Stances do not need identical descriptive depth or identical internal structures.**

This changes the design emphasis from:

```text
make each Stance equally complete
```

to:

```text
build a coherent canonical Component space
        ↓
project the relevant parts into each Stance
```

This is useful because separating Duration, Curve, and Credit inevitably loses some standalone descriptive completeness.

That loss may be an acceptable cost of decomposition if the separation provides:

- clearer economic ownership;
- easier diagnostics;
- less duplicated calculation;
- direct mapping to distinct exposure dimensions;
- ability to combine Stances downstream without hiding their individual contributions.

The Bond-Exposure Stance Set can then provide the multidimensional downstream result without requiring each individual Stance to be a complete bond-market regime description.

---

## 9. Duration / Curve and Bull-Bear Interpretation

The shared-Component proposal helps clarify the earlier bull / bear problem.

A conventional label such as:

```text
bull steepener
bear steepener
bull flattener
bear flattener
```

combines outright yield direction with curve movement.

Embedding that full interpretation inside Curve can duplicate information associated with Duration.

Trying to reconstruct it only from already-finished Final Duration and Final Curve Stances can also lose information because Final Stances may already incorporate compensation and Macro Constraints.

A shared Component model provides a third option:

```text
canonical short-end movement Component
canonical long-end movement Component
canonical curve-movement Component
        ↓
derived cross-market interpretation
        ↓
bull/bear steepener/flattener label
```

Duration and Curve can consume the same authoritative Components where economically justified, without independently redefining them.

Whether bull/bear labels should be:

- diagnostic metadata;
- a Bond-Exposure Stance Set interpretation;
- or some other downstream descriptive output

remains unresolved.

They should not automatically become another authoritative Stance.

---

## 10. Proposed Design Sequence

If Component reuse is accepted, the modeling sequence should shift from a purely stance-by-stance Component design toward a system-level Component catalog.

A practical sequence is:

```text
1. Define the economic questions of Duration / Curve / Credit
        ↓
2. Identify candidate Components required by those questions
        ↓
3. Consolidate candidates into one canonical Component catalog
        ↓
4. Define each Component's value, states, and semantics once
        ↓
5. Check coverage, overlap, redundancy, and missing market concepts
        ↓
6. Select Rule Dimensions for each Stance
        ↓
7. Define stance-specific Rule Cases and Rule Mapping
        ↓
8. Define stance-specific Macro Constraints
        ↓
9. Validate cross-stance interpretation and downstream contracts
```

This avoids trying to invent a complete market ontology before stance requirements are known, while still preventing stance-specific duplicate Components from becoming the default design.

---

## 11. Candidate Architecture Changes If Accepted

If this review direction is accepted, likely authoritative-document changes are relatively limited.

### `bondview_vocabulary.md`

Potential changes:

- revise `Component` / `Market Component` / `Macro Component` wording so a Component is not implicitly owned by exactly one Stance;
- explicitly state that one Component may be used as a Rule Dimension in multiple stance-specific Rule Cases;
- state that Component State semantics remain canonical across consumers;
- refine the Stance definition to distinguish exposure positioning from absolute investment attractiveness.

### `bondview_system_architecture.md`

Potential changes:

Replace or qualify wording such as:

```text
Each stance owns the components...
```

with a structure closer to:

```text
Each stance owns its economic question, selected Rule Dimensions,
Rule Cases, Rule Mapping, and constraint logic.

Components are authoritative derived concepts and may be reused
across stances when their semantics are identical.
```

The existing rule that identical derived concepts should be calculated once and reused would become a normal architectural principle rather than an exceptional case.

### `bondview_stance_design_draft.md`

Potential changes:

- separate the system-level Component catalog concept from stance-specific selection of Rule Dimensions;
- treat current Duration Components as Components consumed by Duration rather than necessarily owned exclusively by Duration;
- revisit Duration / Curve Component overlap after the Curve design is developed;
- retain stance-specific Rule Mapping.

---

## 12. Unresolved Questions

The following should remain explicitly unresolved until additional design work supports a clear answer.

### 12.1 Which Market Components are genuinely shared?

The reuse mechanism is clear, but the final catalog is not.

In particular, it remains unresolved whether Components such as:

- Long-End Yield Trend;
- Recent Long-End Yield Move;
- Curve Configuration;
- Curve Movement;
- short-end rate direction;
- duration-compensation-related states

should actually be consumed by more than one Core Stance.

A Component should be shared only when the semantic concept is truly identical, not merely because the underlying Raw Observation is reused.

### 12.2 Does Curve need outright-rate direction as a Rule Dimension?

This is unresolved.

Using a canonical long-end or short-end movement Component inside Curve could help distinguish the drivers of steepening / flattening.

But it could also make Curve partly reproduce Duration's outright-rate role.

The Curve design should determine whether such information affects the authoritative Curve Stance or belongs only in diagnostics / cross-stance interpretation.

### 12.3 What is the authoritative Curve economic question and output scale?

The general Stance definition can be clarified now, but the exact Curve result semantics and labels are not yet settled.

Until that is defined, Curve mapping examples remain illustrative.

### 12.4 Does Duration require a Compensation / Valuation Component?

Still unresolved.

The shared-Component model does not itself answer whether Duration should use:

- raw long-end yield level;
- yield relative to short/cash rates;
- real yield;
- term premium;
- Curve Configuration;
- or another measure of compensation for duration risk.

If a Duration Compensation Component is introduced, it should have a clear economic definition independent of the stance result it later influences.

### 12.5 Where should bull / bear interpretations live?

Possible locations remain:

- Diagnostics;
- Bond-Exposure Stance Set interpretation;
- another descriptive downstream output.

The current review only argues that bull / bear should not be forced into a stance merely because the information is available.

### 12.6 How should semantic completeness be tested?

The proposal suggests evaluating coherence and coverage primarily at the Component-set level, but there is not yet a formal test for:

- sufficient market coverage;
- excessive redundancy;
- missing dimensions;
- inappropriate overlap between Stances.

This should remain a review criterion rather than a rigid numerical requirement until the Component catalog is more mature.

### 12.7 Can the revised Stance definition be considered final before Curve and Credit are fully designed?

The proposed definition is conceptually clearer and resolves the main ambiguity between within-dimension positioning and absolute investment attractiveness.

However, it should still be validated against completed Duration, Curve, and Credit designs before being promoted into canonical vocabulary.

---

## 13. Review Conclusion

The proposed refinement is modest but potentially important:

```text
Current emphasis:
stance-owned Components

Proposed emphasis:
canonical Components
        ↓
one or more stance consumers
        ↓
stance-specific Rule Cases and Rule Mapping
```

The main benefits are:

- one authoritative semantic definition for each Component;
- no need for a new intermediate processing layer;
- cleaner reuse of market information across Duration, Curve, and Credit;
- less duplicated or inconsistent derived logic;
- clearer separation between descriptive market states and exposure-oriented Stances;
- a more precise Stance definition;
- a natural place for stance-specific interpretation: the Rule Mapping rather than a universal Component favorability score.

The proposal does **not** settle the actual Curve model, the Duration compensation model, or the exact set of shared Components.

Those remain substantive stance-design questions.

If the Component reuse principle survives review, it can then be used as a reference for targeted revisions to the vocabulary, system architecture, and detailed stance-design documents.
