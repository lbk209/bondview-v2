# Bondview Exposure Evaluation Design

## Document Purpose

This document defines the lower-level economic design of **Exposure Evaluation** in Bondview and records the accepted design conclusions for its Constituent Evaluations and their combination.

It sits below `bondview_system_architecture.md`.

The system architecture remains authoritative for:

- system structure;
- ownership;
- dependency direction;
- processing flow;
- Result Boundaries.

This document is authoritative for the accepted lower-level economic design of Exposure Evaluation once individual Constituent designs have been reviewed and validated.

The document is intentionally **result-oriented**.

Detailed exploratory work, Codex prompts, intermediate diagnostics, and temporary review procedures should remain in separate working or validation documents. This document should retain only:

- the accepted economic question for each Constituent;
- the Components and ETF Exposure Profile characteristics used;
- the accepted Core and Macro logic;
- the Result semantics;
- key accepted mappings or parameters;
- concise validation conclusions;
- remaining limitations;
- integrated Exposure Evaluation behavior and validation.

---

# 1. Exposure Evaluation Scope

Exposure Evaluation determines whether an ETF's bond Exposure Profile is economically appropriate under current bond-market and macroeconomic conditions.

Architecturally:

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
```

The current Constituent Evaluations are:

```text
Duration Evaluation
Curve Evaluation
Credit Evaluation
Rates Valuation Evaluation
```

Each Constituent Evaluation answers one distinguishable economic question about the ETF Exposure Profile.

Bondview deliberately uses several interpretable Constituent Evaluations rather than one monolithic bond-price or expected-return forecasting model.

The objective is economically interpretable, traceable, and reviewable decision support.

This decomposition does **not** assume that Constituents are statistically orthogonal or economically independent.

Overlapping inputs and mechanisms are acceptable where different Constituents answer different economic questions.

Materially duplicative effects should be avoided in both Constituent design and Evaluation Combination.

---

# 2. Common Constituent Design Principles

## 2.1 Exposure-specific Core Evaluation

A Constituent Evaluation normally follows:

```text
Components for Core Evaluation
        ↓
[Core Evaluation] <──────── ETF Exposure Profile
        ↓
Core Evaluation Result
        ↓
[Macro Adjustment, where applicable]
        ↓
Constituent Evaluation Result
```

The Core Evaluation Result is already exposure-specific.

Bondview should not create an ETF-independent market-derived exposure preference as an authoritative intermediate result and only afterward compare ETFs against it.

## 2.2 Macro Adjustment

Where Macro Adjustment is used, it modifies the already exposure-specific Core Evaluation Result.

Macro Adjustment must not recreate a second market model that independently re-evaluates the same exposure from scratch.

Its purpose is to modify, constrain, or qualify the Core result using macroeconomic Components whose economic role is not already fully represented by the Core logic.

## 2.3 Result semantics

Constituent Evaluation Results do not need to share identical scales or internal mechanics.

Where an ordinal scale is used, its numbers represent ordered semantic categories rather than cardinal economic magnitude.

## 2.4 Traceability

Each Constituent Evaluation Result should preserve enough lineage to identify:

```text
relevant Components
ETF Exposure Profile characteristics
Core Rule Case or equivalent mapping
Macro action, where applicable
final Constituent Evaluation Result
```

---

# 3. Duration Evaluation

## 3.1 Economic Question

Duration Evaluation asks:

> How favorable or unfavorable are current Duration-relevant rates conditions for this ETF's interest-rate sensitivity?

It evaluates the ETF's sensitivity to changes in the relevant Treasury rate segment. It does **not** independently evaluate overall ETF attractiveness, rates compensation / carry, curve shape, credit, positioning, implementation quality, or risk-adjusted expected return. These distinctions belong to other evaluation responsibilities. A favorable Core Duration score does not itself imply that higher duration has superior risk-adjusted attractiveness.

## 3.2 Exposure Representation

The accepted Core fixture uses these economic centers:

| Duration Exposure | Representative Treasury tenor |
|---|---|
| Short | 6M |
| Intermediate | 10Y |
| Long | 30Y |

The tenor is selected by the economic center of the Duration Exposure. Each exposure uses the Trend and Recent Move States of its **own** representative Treasury tenor. An ETF Exposure Profile participates directly in its Core Evaluation; the system must not first construct an ETF-independent preferred-duration score.

The exposure taxonomy may be expanded if the ETF universe later requires additional economically distinct clusters. This does not change the accepted fixture without an explicit design revision.

## 3.3 Core Components and Accepted State Definitions

Duration Core uses:

```text
Yield Trend State
× Recent Yield Move State
× Duration Exposure
→ Core Duration Evaluation Result
```

**Yield Trend** describes the broader or established rates direction. **Recent Yield Move** describes the shorter-horizon move that confirms, pauses, or challenges that direction; it is not a forecast of a future Trend State.

### Accepted Trend definition

Let `M5(t)` denote the mean of the last five accepted valid yield observations ending at observation `t`, expressed in **basis points** (multiply source yields in percent by 100), with the same source, historical availability, and structural-segment conventions as the frozen Task-1 fixture.

```text
Trend Value (bp) = M5(t) - M5(t-126)
```

The trend uses an approximately six-month overlapping endpoint change. The common directional entry threshold is `±25 bp` for each representative tenor. The following **Hybrid-P3/H5** State Classification is accepted:

- **Stable → Rising:** Trend Value `> +25 bp` on three consecutive valid observations.
- **Stable → Falling:** Trend Value `< -25 bp` on three consecutive valid observations.
- **Rising → Stable:** Trend Value `<= +20 bp` (5 bp hysteresis exit).
- **Falling → Stable:** Trend Value `>= -20 bp` (5 bp hysteresis exit).
- **Pending entry:** A Stable observation or a candidate in the opposite direction resets the pending count as appropriate. Until confirmation, remain Stable.
- **Direct opposite crossing:** If an established Rising State sees Trend `< -25 bp`, or Falling sees Trend `> +25 bp`, exit to Stable on that observation. Count it as observation one of the three needed to confirm the opposite State; do **not** switch directly to the opposite directional State. No special direct-reversal bypass is accepted.
- **Initialization and gaps:** Match the historical fixture's convention: initialize the first valid State of an accepted structural segment using its plain ±25 bp classification, and reset the State and pending counter at structural segment boundaries. Invalid observations do not count toward confirmation. This initialization convention should be explicit in the implementation and diagnostics.

The persistence check applies to *directional entry from Stable*, not to exits from an established Rising/Falling State. Hysteresis applies to *exit from an established direction*, not to entry. This asymmetry deliberately rejects unconfirmed directional crossings while allowing an established condition to survive small threshold retreats.

For numerical consistency, retain the source fixture's unit conventions: the formulas above express yield changes in basis points, irrespective of how source yields are stored.

### Accepted Recent Move definition

```text
Recent Move Value (bp) = M5(t) - M5(t-21)

Falling: value < -10 bp
Stable: -10 bp <= value <= +10 bp
Rising: value > +10 bp
```

Recent Move keeps the existing plain classification; Hybrid-P3/H5 is a **Trend-only** stabilization rule.

## 3.4 Core Result Semantics

The accepted seven-level Core result scale is **ordinal**:

```text
+3 strongly favorable
+2 favorable
+1 mildly favorable
 0 neutral
-1 mildly unfavorable
-2 unfavorable
-3 strongly unfavorable
```

These codes specify economically interpretable order, **not cardinal differences, expected price returns, or risk-adjusted attractiveness**. The greater potential result magnitude for Long versus Short Duration reflects how consequential a given yield-direction environment is for the exposure, not a guarantee that more duration is preferable after carry, compensation, risk, and other Constituents are considered.

## 3.5 Accepted Core Rule Mapping

The accepted table resolves the previously ambiguous Task-1 cells using **weak Trend-first priority**, while retaining the existing single-valued cells and the earlier Task-1 provisional selections. Weak priority permits tied ordinal scores; it is not an obligation to distinguish all nine Rule Cases or expand the seven-level scale.

| Trend | Recent Move | Short | Intermediate | Long |
|---|---|---:|---:|---:|
| Falling | Falling | +1 | +2 | +3 |
| Falling | Stable | +1 | +1 | +2 |
| Falling | Rising | +1 | +1 | +1 |
| Stable | Falling | +1 | +1 | +1 |
| Stable | Stable | 0 | 0 | 0 |
| Stable | Rising | -1 | -1 | -1 |
| Rising | Falling | -1 | -1 | -1 |
| Rising | Stable | -1 | -1 | -2 |
| Rising | Rising | -1 | -2 | -3 |

For comparable exposure-local interpretations, the favorable-score ordering is non-increasing as the case moves from `Falling × Falling` toward `Rising × Rising` in the table. In particular:

```text
Falling × Rising >= Stable × Falling
Stable × Rising >= Rising × Falling
```

Both equalities are acceptable, and both occur in the selected mapping. Under a falling-yield condition, `Long >= Intermediate >= Short`; under a rising-yield condition, `Short >= Intermediate >= Long`. These comparisons refer to *scores for the same rule case*, not to a claim that different Treasury tenors share the same State on any historical date.

The Trend State determines primary directional context. Recent Move affects the strength and interpretation of the resulting Core evaluation without routinely overturning that context. Longer Duration Exposure allows stronger favorable and unfavorable **categories** under aligned directional conditions; scores must not be treated as proportional to modified duration or expected price movement.

## 3.6 Macro Adjustment

Duration Macro Adjustment follows an already exposure-specific Core Result and may use relevant macroeconomic Components such as Inflation Trend and Policy Direction. It must not independently rebuild a second rates-direction model or double-count mechanisms already expressed by Core.

### Accepted Duration Macro mapping

```text
TBD — separate Macro Adjustment design / acceptance stage
```

Acceptance of the Core design does **not** constitute acceptance of the Macro Adjustment or the final Duration Evaluation Result.

## 3.7 Core Decision and Validation Summary

**Decision (2026-10-10):** The six-month overlapping Trend, common ±25 bp directional threshold, Hybrid-P3/H5 Trend stabilization, existing Recent Move definition, and complete seven-level, exposure-specific, weak Trend-first Core Rule Table are **accepted for Duration Core**. This decision supersedes the earlier validation plan's provisional preference for pure 5 bp hysteresis. Detailed exploratory comparisons remain in separate review and validation artifacts.

**Completed narrow consistency checks:** The nine-case table is total and respects the tested ordinal/tenor constraints; eight targeted hybrid transition sequences passed; all 38,330 historically classified observations were replayed across four valid data segments without violating the accepted transition invariants; the frozen source's reference dates precede each `as_of` and the recorded feature arithmetic agrees with its source fields. These are **mechanical and internal-consistency** checks, not evidence of superior predictive returns or proof of economic correctness.

**Explicit remaining work:** Specify and accept Duration Macro Adjustment, then diagnose the complete Duration Constituent while retaining Core, Macro action, and final Result side by side. Do not reopen this Core decision solely to improve back-fitted historical outcomes; require a concrete economic, data-integrity, or architecture-level contradiction.

---

# 4. Curve Evaluation

## 4.1 Economic Question

Curve Evaluation asks:

> Is the ETF's maturity / curve exposure appropriate under current term-structure conditions?

Curve Evaluation focuses on relative term-structure configuration and maturity-location effects.

It may consume some of the same Treasury observations or Components used by Duration Evaluation, but it should answer a different economic question.

## 4.2 Core Components

```text
TBD
```

## 4.3 ETF Exposure Profile Characteristics

```text
TBD
```

## 4.4 Core Logic

```text
TBD
```

## 4.5 Macro Adjustment

```text
TBD, if applicable
```

## 4.6 Result Semantics

```text
TBD
```

## 4.7 Validation Summary

```text
TBD
```

---

# 5. Credit Evaluation

## 5.1 Economic Question

Credit Evaluation asks:

> Is the ETF's credit-risk exposure appropriate under current credit conditions?

## 5.2 Core Components

```text
TBD
```

## 5.3 ETF Exposure Profile Characteristics

```text
TBD
```

## 5.4 Core Logic

```text
TBD
```

## 5.5 Macro Adjustment

```text
TBD, if applicable
```

## 5.6 Result Semantics

```text
TBD
```

## 5.7 Validation Summary

```text
TBD
```

---

# 6. Rates Valuation Evaluation

## 6.1 Economic Question

Rates Valuation Evaluation asks:

> Is the compensation for accepting the ETF's rates exposure sufficiently attractive?

This Constituent is conceptually distinct from Duration Evaluation.

Duration evaluates how favorable current rate-direction conditions are for the ETF's rate sensitivity.

Rates Valuation evaluates whether the yield / carry or other relevant compensation is attractive enough for accepting that exposure.

## 6.2 Core Components and ETF-level Inputs

Potential inputs may include:

```text
ETF Yield / Carry measure
relevant Treasury yield level
term compensation or other justified valuation measures
```

Exact accepted inputs:

```text
TBD
```

## 6.3 ETF Exposure Profile Characteristics

```text
TBD
```

## 6.4 Core Logic

```text
TBD
```

## 6.5 Macro Adjustment

```text
TBD, if applicable
```

## 6.6 Result Semantics

```text
TBD
```

## 6.7 Validation Summary

```text
TBD
```

---

# 7. Evaluation Combination

Evaluation Combination combines the completed Constituent Evaluation Results into the overall Exposure Evaluation Result.

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

## 7.1 Design Questions

The final combination design should explicitly define:

- whether Constituent results are combined through weighting, rules, constraints, conditional logic, or another mechanism;
- whether Constituent result scales require normalization or semantic translation;
- whether any Constituent acts as a constraint rather than an additive contribution;
- how material overlap between Constituents is prevented from becoming double counting;
- how the final Exposure Evaluation Result preserves traceability to its Constituent results.

## 7.2 Double-counting Review

Overlap in Raw Observations or Components is not automatically a problem.

The relevant question is whether two Constituents materially count the same economic mechanism twice in the final Exposure Evaluation Result.

Evaluation Combination should therefore preserve enough information to identify:

```text
independent contribution
shared mechanism
constraint effect
possible duplication
```

where relevant.

## 7.3 Accepted Combination Logic

```text
TBD after individual Constituent designs are accepted
```

---

# 8. Integrated Exposure Evaluation Validation

Integrated validation begins only after the individual Constituent designs are sufficiently stable.

Its purpose is not to re-run each Constituent's internal validation.

Instead, it tests whether the full Exposure Evaluation:

- preserves the distinct economic meaning of each Constituent;
- combines conflicting Constituent results coherently;
- avoids material double counting;
- remains interpretable in historically unusual environments;
- produces a traceable Exposure Evaluation Result.

Historical and contemporaneous cases should be selected because they stress interactions among Constituents rather than merely reproduce single-Constituent test cases.

---

# 9. Planned Integrated Stress and Boundary Cases

## 9.1 2026 High Long-End Yield Regime

The 2026 period in which the U.S. 10-year Treasury yield remained above approximately 5% should be retained as a planned **integrated Exposure Evaluation stress / boundary case**.

Its importance is not that it necessarily represents an unusual Duration Trend / Recent Move Rule Case.

Its importance is that several economic dimensions may point in different directions at the same time.

Conceptually:

```text
historically high absolute long-end yield
        ↓
potentially attractive Rates Valuation

rate Trend / Recent Move
        ↓
Duration assessment may differ

curve configuration
        ↓
Curve assessment may differ

macro / credit conditions
        ↓
other Constituent effects

        ↓
Evaluation Combination
        ↓
Exposure Evaluation Result
```

The integrated diagnostic should eventually test:

1. Does **Rates Valuation**, rather than Duration, capture the attractiveness of unusually high absolute yields?

2. Does Duration continue to respond primarily to rate direction and exposure sensitivity rather than becoming implicitly favorable merely because yields are high?

3. Can favorable valuation and unfavorable Duration coexist without Evaluation Combination flattening their distinct meanings?

4. Does Curve Evaluation add an economically distinct term-structure interpretation rather than duplicating Duration?

5. If macroeconomic or credit conditions differ from earlier high-yield episodes, does the system preserve that distinction rather than treating all high-yield environments as equivalent?

6. Does the final Exposure Evaluation Result remain interpretable when the real economy or risk assets respond differently from superficially similar historical yield regimes?

7. Does the episode reveal material double counting among Duration, Rates Valuation, Curve, Credit, or Macro Adjustment?

8. Can the final result be traced clearly back to the individual Constituent judgments?

This case should be treated primarily as a **coherence, interaction, and boundary test**.

Subsequent equity-market, macroeconomic, or ETF performance should not automatically be treated as the target label that defines whether the Exposure Evaluation Result was correct.

## 9.2 Additional integrated cases

Future integrated cases may include:

```text
TBD
```

Possible categories:

- aggressive tightening / inflation shock;
- rapid easing / recession-risk transition;
- abrupt risk-off Treasury rally;
- extreme curve inversion;
- rapid curve steepening;
- credit-stress regime;
- mixed environment with favorable rates valuation but unfavorable duration;
- mixed environment with supportive duration but poor credit conditions.

Only cases that materially test cross-Constituent interaction should be retained here.

---

# 10. Integrated Validation Record

For each accepted integrated validation case, record only:

```text
case / period
why the case matters
Constituent Evaluation Results
important interactions or conflicts
Evaluation Combination behavior
Exposure Evaluation Result
diagnostic conclusion
remaining limitation, if any
```

Avoid turning this document into a chronological research log.

Detailed calculations and plots may remain in separate diagnostic artifacts.

---

# 11. Open Issues and Future Extensions

Only unresolved model questions that may materially affect Exposure Evaluation should be listed here.

Current placeholders:

```text
Duration Macro Adjustment and completed Duration Evaluation validation
Curve Evaluation design
Credit Evaluation design
Rates Valuation Evaluation design
Evaluation Combination logic
integrated historical case set
```

Implementation todos, temporary coding issues, and exploratory ideas should remain outside this document.

---

# 12. Document Maintenance Principle

This document should evolve from:

```text
partially specified Constituent sections
+
planned validation cases
```

toward:

```text
accepted Constituent designs
+
accepted Evaluation Combination logic
+
compact integrated validation record
```

As each Constituent review is completed:

1. record the accepted result here;
2. remove temporary alternatives that were rejected;
3. retain only short validation conclusions;
4. keep detailed experimental procedure in its separate validation document;
5. update integrated validation only when the full Exposure Evaluation design is sufficiently stable.

This keeps `bondview_exposure_evaluation_design.md` as the durable lower-level economic design record rather than a working notebook.
