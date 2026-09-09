# Bondview v2 — Stance Rule Mapping and Macro Constraint Design

## Document Purpose

This document records the current design direction for calculating the Bondview v2 Duration, Curve, and Credit stances.

The system-level architecture is defined by:

- `docs/bondview_system_architecture.md` in `bondview-v2`
- https://github.com/lbk209/bondview-v2/blob/main/docs/bondview_system_architecture.md

That document is the current source of truth for v2 architecture.

The previous `bondview` repository may be consulted for earlier calculation logic, terminology, and implementation experience, but it is reference material rather than a v2 design contract.

This document focuses on the next design step: defining, for each stance,

1. the market-derived states that participate in rule mapping;
2. the economically meaningful rule mapping that produces the core stance;
3. the stance-specific macro conditions that may constrain that core stance.

The purpose is to establish the economic model before fixing numeric scores, thresholds, smoothing, stabilization, raw input series, or other calculation mechanics.

---

## 1. Overall Stance Calculation Flow

The system architecture defines the conceptual stance flow as:

```text
stance components
      ↓
rule mapping
      ↓
core stance
      ↓
stance-specific macro constraint
      ↓
final stance
```

For implementation design, the full calculation path will eventually include preparation and mechanical processing around that conceptual core.

A likely runtime structure is:

```text
accepted raw observations
        ↓
derived features / prepared inputs
        ↓
normalization or smoothing where justified
        ↓
state / bucket classification
        ↓
state stabilization where justified
        ↓
rule-case construction
        ↓
rule mapping
        ↓
core stance score / core stance
        ↓
stance-specific macro constraint
        ↓
constrained stance
        ↓
final mechanical processing where required
        ↓
final stance score / label / result metadata
```

The exact placement and necessity of normalization, smoothing, hysteresis, persistence, clipping, and similar mechanics are **not yet fixed**.

The important design order is:

```text
economic meaning first
→ rule mapping
→ macro constraint semantics
→ scoring representation
→ calculation mechanics
→ raw/derived input implementation
```

This prevents technical mechanics from determining the economic model.

---

## 2. Core Design Principles

### 2.1 Macro is excluded from core rule mapping

For v2, macro conditions do not participate as dimensions of the core stance rule table.

Instead:

```text
market-derived rule case
→ core stance
→ macro constraint
→ final stance
```

This is an intentional difference from the previous Bondview Duration design, where inflation and policy conditions were included directly in the rule-case Cartesian product.

Macro conditions may leave a stance unchanged, weaken or strengthen it, cap its magnitude, restrict a direction, or reject an exposure when a genuinely hard condition is justified.

They should not be introduced merely because macro data is available.

### 2.2 Rule cases should have joint economic meaning

A rule case should represent a combination whose joint state has an interpretable bond-market meaning.

For example:

```text
credit spreads wide + spreads tightening
→ positive core Credit stance
```

The goal is not to maximize the number of dimensions or cases.

A smaller rule structure is preferable when it retains the economically meaningful distinctions needed by the stance.

### 2.3 Labels should be natural and composable

State labels should be understandable in ordinary economic and bond-market discussion and should combine naturally when written as a rule case.

Good examples include:

```text
wide + tightening
inverted + bull steepening
```

Working labels such as `yield trend`, `recent yield move`, and their state names should therefore be treated as provisional until the rule design is reviewed for terminology.

The label review should favor:

- terms commonly understood in bond-market or economic discussion;
- combinations that read naturally without requiring implementation knowledge;
- directional meaning that is immediately clear;
- consistent vocabulary across documentation, configuration, and result metadata;
- economic labels rather than generic implementation labels such as `positive` or `negative` when a more meaningful term exists.

The purpose is not terminology for its own sake. Clear labels make the rule combinations themselves explainable.

---

## 3. Duration

### 3.1 Core economic question

Duration should express whether longer-duration bond exposure is favored by the current rates-market environment.

The core rule mapping should use rates-market information only.

Inflation and monetary policy should be handled afterward as macro constraints rather than as rule-case dimensions.

### 3.2 Proposed core rule dimensions

A useful starting structure is:

```text
long-end yield trend
    falling
    stable
    rising

recent long-end yield move
    falling
    stable
    rising
```

These names are working labels and should be reviewed for domain-natural terminology and readability in combinations.

The resulting maximum rule space is:

```text
3 × 3 = 9 cases
```

Representative interpretations:

```text
trend falling + recent move falling
→ strongly positive core Duration

trend falling + recent move rising
→ positive but weakening

trend stable + recent move stable
→ neutral

trend rising + recent move falling
→ negative but improving

trend rising + recent move rising
→ strongly negative core Duration
```

The exact stance strengths and numeric scores are not yet defined.

The important current judgment is that the medium-horizon direction and the more recent move provide two distinct pieces of market information:

- the broader direction of long yields;
- whether the latest move confirms or challenges that direction.

This creates a compact rule table in which the combinations are easier to interpret than a rule table that also includes macro conditions.

### 3.3 Proposed macro constraint

The initial macro dimensions are:

```text
inflation trend
    falling
    stable
    rising

policy direction
    easing
    stable
    tightening
```

Representative interpretation:

```text
inflation falling + policy easing
→ supportive of positive Duration
→ leave unconstrained or strengthen if justified

inflation rising + policy tightening
→ adverse to positive Duration
→ weaken or cap

mixed macro conditions
→ unchanged or mild constraint
```

The exact constraint table is not yet defined.

A key design question is how interventionist the constraint should be. A conservative starting principle is:

- the core market rule determines direction;
- macro usually changes the strength or permitted magnitude;
- direction reversal should require a deliberately defined hard condition rather than arise casually from ordinary macro disagreement.

This preserves the distinction between **market-derived core stance** and **macro constraint**.

### 3.4 Main redesign from the previous Bondview model

The previous Duration design combined four three-state inputs:

```text
duration preference
× duration rate shock
× inflation
× policy
```

This produced 81 possible rule cases.

The v2 direction is instead approximately:

```text
market rule:
long-end yield trend
× recent long-end yield move
→ 9 core cases

then:

inflation
× policy
→ stance-specific macro constraint
```

The reduction is not valuable merely because the number of cases is smaller. It is valuable because the market rule and macro constraint now answer different questions and are separately interpretable.

---

## 4. Credit

### 4.1 Core economic question

Credit should express whether credit exposure is attractive based on current compensation and current spread direction.

The prior Bondview structure is already close to the desired v2 core-rule design because it uses two clearly related credit-market concepts rather than mixing macro conditions directly into the rule mapping.

### 4.2 Proposed core rule dimensions

```text
spread level
    wide
    normal
    tight

spread direction
    tightening
    stable
    widening
```

This produces:

```text
3 × 3 = 9 cases
```

Representative interpretations:

```text
wide + tightening
→ positive core Credit

normal + stable
→ neutral core Credit

tight + widening
→ negative core Credit
```

The economic interpretation is straightforward:

- spread level asks whether current compensation is relatively generous or expensive;
- spread direction asks whether credit conditions are improving or deteriorating.

Their combination is therefore a strong candidate for a complete and compact core rule table.

### 4.3 Proposed macro constraint

The initial macro concepts are:

```text
growth
    strengthening
    stable
    weakening

labor-market condition
    improving
    stable
    deteriorating
```

Representative interpretation:

```text
growth weakening + labor market deteriorating
→ weaken/cap positive core Credit
```

Intuitively:

```text
spreads wide + spreads tightening
→ credit looks attractive from market pricing

but

growth weakening + labor market deteriorating
→ fundamentals argue for caution

therefore

positive core Credit
→ positive but constrained Credit
```

A reasonable initial direction is for Credit macro constraints to be primarily **downside-protective** rather than automatically providing symmetric upside boosts.

This is not yet a fixed rule. It reflects the idea that tightening spreads already contain favorable market information, whereas deteriorating macro fundamentals may provide an important reason not to express that positive signal too aggressively.

Whether supportive macro conditions should actively strengthen Credit, or merely leave the core stance unconstrained, remains to be decided.

---

## 5. Curve

### 5.1 Core economic question

Curve should express preferred positioning along the yield curve based on the current curve shape and the nature of the current curve move.

The previous Bondview model used three dimensions:

```text
curve change
× curve state
× yield-move driver
```

with:

```text
3 × 4 × 5 = 60 cases
```

Unlike the previous Duration structure, those dimensions are all market-derived. Therefore the Curve redesign is not primarily a matter of extracting macro inputs.

The goal is instead to find the smallest representation that preserves economically meaningful curve regimes.

### 5.2 Proposed core rule dimensions

A promising v2 simplification is to combine the previous `curve change` and `yield-move driver` concepts into one economically named move regime.

```text
curve state
    inverted
    flat
    normal
    steep

curve-move regime
    bull steepening
    bear steepening
    bull flattening
    bear flattening
    parallel / unclear
```

This gives a maximum conceptual grid of:

```text
4 × 5 = 20 cases
```

Examples:

```text
inverted + bull steepening

flat + bear steepening

normal + bull flattening

steep + bear flattening
```

These combinations are substantially easier to interpret directly than the previous three-dimensional 60-case Cartesian structure.

The target of 20 cases should **not** be interpreted as a requirement that all 20 combinations must receive unique scores.

It is the maximum state grid implied by the proposed two-dimensional representation.

### 5.3 Rule coverage when not every combination deserves a distinct score

A further Curve review should determine whether:

1. all 20 combinations have sufficiently distinct economic meaning;
2. some combinations are economically equivalent and should share a result;
3. some combinations are valid but weakly informative and should fall back to a neutral/default interpretation;
4. additional curve regimes are genuinely needed, increasing the state space.

The v2 flow must support the result of that review.

Several implementation conventions are possible.

#### Complete explicit table

Use when every valid combination can be economically interpreted.

```text
every state combination
→ explicit rule score
```

This is simple and transparent when the table remains small.

#### Canonical cases plus explicit fallback

Use when only some combinations deserve distinct treatment.

```text
economically meaningful cases
→ explicit mappings

remaining valid cases
→ defined neutral/default/fallback behavior
```

This may be preferable to inventing scores for combinations that do not carry a distinct view.

#### Ordered interpolation

Use only if the rule states form a defensible ordered structure and the missing case can genuinely be inferred from neighboring cases.

```text
defined anchor cases
→ deterministic interpolation
→ uncovered ordered cases
```

Interpolation should not be introduced merely to avoid writing cases.

The economic topology must justify it.

The currently inspected old `bondview` main configuration explicitly enumerates the 60 Curve combinations. No interpolation convention should therefore be assumed as a required inheritance for v2.

The v2 rule contract should explicitly define its coverage behavior rather than relying on an implicit historical convention.

### 5.4 Curve macro constraint

The current design is:

```text
Curve macro constraint
→ none / pass-through
```

This is intentional.

Inflation and policy strongly influence the yield curve, but much of their information may already be expressed through the observed curve state and bull/bear steepening or flattening regime.

Reapplying the same macro information as a Curve constraint could therefore double count information unless a distinct economic reason is demonstrated.

The stance pipeline must support a stance with no macro constraint:

```text
core Curve stance
→ no applicable macro constraint
→ final Curve stance = core Curve stance
```

This should be a normal supported path, not an exceptional workaround.

No dummy macro input or artificial no-op rule should be required merely to satisfy the pipeline.

Result metadata should still make it clear that no macro constraint was applied.

A Curve macro constraint may be introduced later if a macro condition is found that materially changes how a curve regime should be expressed without merely restating the curve information already used in the core rule.

---

## 6. Rule Mapping Coverage as a General v2 Requirement

The Curve discussion exposes a requirement that should apply to all rule-mapped stances.

The rule-mapping mechanism should not assume that every Cartesian combination must have a unique explicit score.

Instead, the stance-specific contract should be able to define an appropriate coverage strategy.

Possible strategies are:

```text
complete explicit mapping

or

explicit meaningful cases + defined fallback

or, where economically justified,

anchor cases + deterministic interpolation
```

The choice belongs to the stance model, not to the generic rule-mapping mechanism.

The generic mechanism should provide the capability without imposing one economic convention on every stance.

For the initial designs:

- Duration is expected to be small enough for a complete 9-case mapping.
- Credit is expected to be small enough for a complete 9-case mapping.
- Curve requires explicit review before deciding whether its maximum 20-case grid should be complete, collapsed, or partially covered.

---

## 7. Macro Constraint Contract Requirements

The three stance designs imply several general requirements for macro constraints.

### 7.1 Constraint is stance-specific

Duration and Credit may consume different macro conditions and use different constraint rules.

Curve may consume none.

The generic constraint capability should therefore not encode one fixed set of macro inputs.

### 7.2 No-op must be first-class behavior

A constraint layer must support:

```text
no relevant macro constraint
→ core stance passes through unchanged
```

This applies both:

- to a stance such as Curve that currently has no macro constraint;
- to individual Duration or Credit cases where current macro conditions do not materially constrain the core stance.

### 7.3 Constraint should normally modify expression, not recreate the stance

The core rule mapping answers the stance's market question.

Macro should normally modify how strongly that result is expressed.

Possible actions include:

```text
unchanged
strengthen
weaken
cap magnitude
restrict direction
hard reject
```

Direction reversal should require a deliberately justified condition.

Otherwise the macro layer risks becoming a second stance calculator rather than a constraint.

### 7.4 Constraint mechanics should be separate from economic rules

Generic mechanics may eventually support operations such as:

```text
score adjustment
magnitude cap
directional cap
pass-through
hard rejection
```

But which action applies under which macro state belongs to the individual stance definition.

---

## 8. Raw Input Requirements

Raw inputs do **not** need to be finalized before the mapping and macro-constraint design.

In fact, the preferred direction is to determine them backward from the economic model.

The design sequence should be:

```text
stance question
→ rule dimensions
→ state meanings
→ rule cases
→ macro constraint concepts
→ required observable concepts
→ candidate raw data series
→ derived features
→ horizons / transformations
→ normalization / smoothing
→ thresholds and stabilization
```

For example, once Duration is fixed conceptually as:

```text
long-end yield trend
× recent long-end yield move
```

the implementation design can then ask:

- which Treasury maturities best represent the long end;
- whether one yield, multiple yields, or a composite should be used;
- what horizons represent `trend` and `recent`;
- whether changes should be raw, percentage, z-scored, or otherwise transformed;
- what smoothing is required before state classification.

Likewise, once Credit macro constraints are fixed around growth and labor-market deterioration, the input design can determine which observations best represent those concepts.

This is preferable to inheriting raw inputs merely because the previous repository already used them.

However, input feasibility should be checked once the economic concepts are sufficiently stable. If a desired state cannot be represented reliably with available data, the model definition may need to be revised.

Therefore:

```text
do not design from legacy raw inputs first

but

do validate data feasibility before numeric implementation is frozen
```

---

## 9. Processing Mechanics to Design After Mapping and Constraints

After the semantic model is sufficiently stable, each stance can define the calculation mechanics needed to make the model operational.

These include:

### Input preparation

- derived feature calculation;
- horizon selection;
- smoothing;
- normalization;
- sign handling;
- fixed-anchor or relative transformations where appropriate.

### State classification

- state/bucket thresholds;
- boundary behavior;
- treatment of missing or ambiguous observations.

### State stabilization

- hysteresis;
- minimum persistence;
- other anti-churn mechanics.

These should be used only where economically or operationally justified rather than automatically applied to every state.

### Rule score representation

The rule mapping first needs an ordinal economic interpretation.

For example:

```text
strong negative
negative
weak negative
neutral
weak positive
positive
strong positive
```

A numeric scale can then be assigned to those meanings.

The score scale should represent the rule semantics rather than define them.

### Constraint mechanics

The macro constraint must specify whether it operates through:

- score addition/subtraction;
- multiplicative attenuation;
- magnitude caps;
- ordinal stance limits;
- directional restrictions;
- another explicitly defined operation.

The economic constraint table should be settled before choosing the most convenient arithmetic.

### Final processing

Possible final mechanics include:

- clipping;
- final stance classification;
- final stabilization if justified;
- strength labeling;
- metadata describing the difference between core and constrained stance.

The system result should preserve enough information to explain:

```text
core stance
→ macro action
→ final stance
```

---

## 10. Current Decisions

The following directions are currently accepted for v2.

### Architecture

- `bondview-v2` is the active project.
- `docs/bondview_system_architecture.md` is the current confirmed v2 architecture document.
- The old `bondview` repository is reference material only.
- Duration, Curve, and Credit remain separate stance outputs.
- Macro is excluded from core rule mapping.
- Macro is applied afterward as a stance-specific constraint.
- A stance may legitimately have no macro constraint.

### Design order

- Define economic rule mapping before numeric scoring mechanics.
- Define macro constraint semantics before constraint arithmetic.
- Determine raw input requirements backward from the accepted economic concepts.
- Add smoothing, normalization, hysteresis, clipping, and related mechanics only after the states and rule meanings are understood.

### Duration

- Candidate core structure: long-end yield trend × recent long-end yield move.
- Candidate maximum grid: 9 cases.
- Inflation and policy move out of the core rule table and into the macro constraint.

### Credit

- Candidate core structure: spread level × spread direction.
- Candidate maximum grid: 9 cases.
- Growth and labor-market conditions are candidate macro constraint dimensions.
- The initial macro-constraint philosophy is likely to be primarily downside-protective, subject to further review.

### Curve

- Candidate core structure: curve state × curve-move regime.
- The previous 60-case structure can potentially be reduced to a maximum 20-case conceptual grid.
- `curve change` and `yield-move driver` are conceptually combined into named bull/bear steepening/flattening regimes.
- No Curve macro constraint is currently required.
- The pipeline must support pass-through when no macro constraint applies.
- The 20-case grid is not a requirement for 20 unique explicit scores.

---

## 11. Open Design Questions

The next design work should resolve the following.

### Terminology

- Are the Duration labels such as `long-end yield trend` and `recent long-end yield move` the most natural bond-market terminology?
- Do all state combinations read naturally and communicate their economic meaning?
- Are label names consistent enough to serve in documentation, configuration, and result metadata?

### Duration mapping

- What should the complete 9-case ordinal mapping be?
- How much should a recent move override or merely temper the broader trend?
- Which inflation × policy combinations should leave, weaken, strengthen, or cap the core stance?
- Should supportive macro conditions actively strengthen Duration or merely avoid constraining it?

### Credit mapping

- What should the complete 9-case ordinal mapping be?
- Should spread level and direction have symmetric importance?
- Which growth × labor combinations should constrain positive Credit?
- Should supportive macro conditions strengthen Credit, or should Credit macro constraints initially be downside-only?

### Curve mapping

- Do all proposed 20 combinations deserve an explicit interpretation?
- Which combinations can share one canonical result?
- Are any regimes missing from the five proposed curve-move labels?
- Should weakly informative combinations map to a defined neutral/default result?
- Is interpolation economically defensible anywhere, or should the model use only explicit cases and fallback behavior?
- What should happen if the final review increases rather than decreases the number of meaningful curve regimes?

### Rule-mapping mechanism

- Must each stance provide a complete table?
- Should the shared mechanism support explicit fallback?
- Should interpolation be a generic optional capability, enabled only by stance-specific configuration?
- How should missing valid cases be distinguished from configuration errors?

### Macro constraints

- What is the canonical representation of `no constraint`?
- Should constraints operate on numeric scores, ordinal stance strength, or both?
- Which actions are generic capabilities and which belong entirely in stance-specific rules?
- Under what conditions, if any, may macro reverse a core stance direction?

### Inputs and mechanics

- Which raw observations best represent each accepted rule and macro concept?
- Which horizons distinguish broad trend from recent movement?
- Which concepts require normalization or fixed anchors?
- Where is smoothing actually needed?
- Which states require hysteresis or persistence?
- At what layer should clipping occur?

---

## 12. Recommended Next Sequence

The next work should remain model-first rather than implementation-first.

Recommended order:

```text
1. finalize Duration rule labels and 9-case mapping
2. finalize Duration macro-constraint states and actions

3. finalize Credit 9-case mapping
4. finalize Credit macro-constraint states and actions

5. finalize Curve state and curve-move-regime vocabulary
6. review the maximum 20-case Curve grid
7. choose complete / collapsed / fallback coverage strategy
8. confirm Curve pass-through macro behavior

9. derive required input concepts for all three stances
10. audit candidate raw data and feature feasibility

11. define numeric score scales
12. define classification thresholds
13. define smoothing / normalization / stabilization
14. define generic rule-mapping and constraint mechanics
15. define result fields preserving core and final stance
```

This sequence should make it possible to judge the required score mechanics from the economic model rather than modifying the economic model to fit pre-existing calculation code.
