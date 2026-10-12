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

Each Constituent Evaluation operates within its accepted exposure coverage. ETF Exposure Profile characteristics not adequately covered by the existing design require explicit handling rather than an implicit extension of the evaluation model.

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

## 2.5 Constituent Design Documentation Structure

Each Constituent design should explain its economic question and scope, a concise evaluation overview, relevant Components and ETF-specific inputs, Core Evaluation logic, applicable Macro Adjustment, Result semantics and traceability, and accepted design conclusions and limitations.

This is a **documentation convention**, not a requirement that Constituents use identical Components, calculations, Rule Tables, Macro mechanisms, or Result scales. The headings and internal level of detail may vary; inapplicable material can be omitted or identified as such. Keep exploration, validation workflows, and test logs outside this document unless a finding is necessary to understand an accepted design decision.

---

# 3. Duration Evaluation

## 3.1 Economic Question and Scope

Duration Evaluation asks:

> How favorable or unfavorable are current Duration-relevant rates conditions for this ETF's interest-rate sensitivity?

It evaluates the ETF's sensitivity to changes in the relevant Treasury rate segment. It does **not** independently evaluate overall ETF attractiveness, rates compensation / carry, curve shape, credit, positioning, implementation quality, or risk-adjusted expected return. These distinctions belong to other evaluation responsibilities. A favorable Core Duration score does not itself imply that higher duration has superior risk-adjusted attractiveness.

## 3.2 Evaluation Overview

Duration Core relates market direction at the ETF exposure's representative Treasury tenor to the ETF's Duration Exposure. Macro Adjustment, when designed and accepted, will subsequently qualify that already exposure-specific Core Result.

```text
ETF Duration Exposure → Representative Treasury tenor
                                ↓
                   Tenor-local Yield Trend State
                   + Recent Yield Move State
                                ↓
Duration Exposure ───────→ [Core Rule Mapping]
                                ↓
                     Core Duration Evaluation Result
                                ↓
Macroeconomic Components → [Macro Adjustment — TBD]
                                ↓
                       Duration Evaluation Result
```

Market Component Values and States are defined for the applicable Treasury tenor, independently of the downstream ETF evaluator. The Duration Exposure category selects the applicable exposure-specific Core mapping; it does not redefine or recalibrate those Components. There is no authoritative ETF-independent preferred-duration score between the Components and the Core Result.

The **Core design is accepted**; the Macro Adjustment mapping and the completed Duration Evaluation Result remain to be specified.

## 3.3 Inputs and Exposure Representation

### Duration Exposure and representative Treasury tenor

The accepted exposure categories and their representative Treasury tenors are:

| Duration Exposure | Representative Treasury tenor |
|---|---|
| Short | 6M |
| Intermediate | 10Y |
| Long | 30Y |

Each tenor represents the economic center of its Duration Exposure category; it is **not** an assertion that an ETF's numerical duration equals the tenor's maturity. Each exposure uses the Yield Trend and Recent Yield Move States of its **own** representative Treasury tenor, while its exposure category selects the corresponding Core Rule Mapping column. Consequently, different exposures may occupy different Rule Cases on the same date.

These exposure characteristics come from the ETF Exposure Profile. The taxonomy may be expanded if the ETF universe later requires additional economically distinct Duration clusters, but that would require an explicit revision of the accepted design.

### Yield Trend — broader directional condition

**Yield Trend** describes the broader or established Treasury rates direction. Let `M5(t)` denote the mean of the last five accepted valid yield observations ending at observation `t`, expressed in **basis points**. If source yields are expressed in percent, multiply by 100 to obtain basis points. Lookback offsets refer to accepted observation indices within a continuous structural data segment, not calendar days.

```text
Trend Value (bp) = M5(t) - M5(t-126)
```

This six-month overlapping endpoint-change horizon represents established yield direction while allowing Recent Yield Move to capture shorter-horizon confirmation or opposition. Longer horizons add unnecessary inertia for this purpose. A current-minus-trailing-average measure was not adopted because it may primarily represent yield level relative to recent history rather than ongoing direction, blurring the boundary with Rates Valuation.

The directional entry thresholds are common to all three representative Treasury tenors:

```text
Rising candidate:   Trend Value > +25 bp
Falling candidate:  Trend Value < -25 bp
Otherwise:          no new directional candidate
```

The accepted **Hybrid-P3/H5 State Classification** combines three-observation directional-entry persistence with 5 bp directional-exit hysteresis, with an immediate direct-reversal exception. Evaluate its rules in the following priority order:

1. **Direct directional reversal — highest priority.** If the established State is `Rising` and Trend Value becomes `< -25 bp`, transition directly to `Falling` on that observation. Conversely, established `Falling` transitions directly to `Rising` when Trend Value becomes `> +25 bp`. No Persistence-3 confirmation is required for a direct crossing of both directional thresholds; clear any pending entry count.
2. **Directional exit — hysteresis.** Otherwise, established `Rising` becomes `Stable` when Trend Value is `<= +20 bp`, and established `Falling` becomes `Stable` when Trend Value is `>= -20 bp`. Retain the directional State while its exit condition is not met.
3. **Entry from Stable — persistence.** An already `Stable` State enters `Rising` only after three consecutive valid observations with Trend Value `> +25 bp`, or enters `Falling` only after three consecutive valid observations with Trend Value `< -25 bp`. Before confirmation, remain `Stable`. A neutral or opposing candidate resets or replaces the pending confirmation sequence.
4. **Initialization and structural gaps.** At the first calculable observation in each accepted structural segment, initialize from the plain `±25 bp` classification. Reset both State and pending confirmation count at structural segment boundaries. Invalid observations do not count toward confirmation.

The direct-reversal exception operates **only while the prior directional State is still established**. Once that State has already exited to `Stable`, a new directional entry requires Persistence-3 regardless of Trend magnitude. For example, `Rising (+30) → Falling (-30)` is immediate, while `Rising (+30) → Stable (+18) → Stable (-30)` remains pending until Falling is confirmed. An established Falling State, including one entered through direct reversal, exits to Stable at `-20 bp` or above.

The intent is to suppress ambiguous boundary fluctuations without delaying a direct crossing of the entire opposite directional range. This changes the classification of **Trend**, not the calculation of Trend Value or the classification of Recent Yield Move. The stabilized Trend State need not equal the plain classification of the current Trend Value on every observation.

### Recent Yield Move — shorter-horizon condition

**Recent Yield Move** describes a shorter-horizon yield move that confirms, pauses, or challenges the broader Trend; it is **not** a forecast of a future Trend State.

```text
Recent Move Value (bp) = M5(t) - M5(t-21)

Falling: value < -10 bp
Stable: -10 bp <= value <= +10 bp
Rising: value > +10 bp
```

Recent Yield Move retains plain threshold classification. Hybrid-P3/H5 applies to **Yield Trend only**. Both Component calculations use the same valid-observation, structural-segment, and basis-point conventions described above, irrespective of how source yields are stored.

## 3.4 Core Evaluation

The accepted Core Rule Mapping is:

```text
Yield Trend State
× Recent Yield Move State
× Duration Exposure
→ Core Duration Evaluation Result
```

The Trend State establishes the primary directional context. Recent Move confirms or challenges it and may affect the strength of the Core judgment without routinely overturning its direction. **Weak Trend-first priority** permits tied ordinal outcomes; it does not require different scores for every Rule Case or an expanded score scale.

### Accepted Core Rule Table

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

For comparable exposure-local interpretations, the favorable-score ordering is non-increasing down the table from `Falling × Falling` toward `Rising × Rising`. In particular:

```text
Falling × Rising >= Stable × Falling
Stable × Rising >= Rising × Falling
```

Both equalities are permitted and hold for the accepted mapping. Within a *common Rule Case*, under falling-yield conditions `Long >= Intermediate >= Short`, whereas under rising-yield conditions `Short >= Intermediate >= Long`. This does **not** imply that the three representative Treasury tenors have the same State on any given date.

Longer Duration Exposure can have stronger favorable or unfavorable **categories** when directions align, reflecting the greater consequence of a given yield-direction condition for the exposure. These category differences are not proportional measures of modified duration or forecast price movement.

## 3.5 Macro Adjustment

Duration Macro Adjustment, when defined, will operate on the already exposure-specific Core Duration Evaluation Result. Potentially relevant macroeconomic Components include **Inflation Trend** and **Policy Direction**.

Its role is to modify, constrain, or qualify that Core judgment using economically distinct information. It must not independently reconstruct another rates-direction model or double-count mechanisms already represented by Core.

### Accepted Duration Macro mapping

```text
TBD — separate Macro Adjustment design and acceptance stage
```

Accepting the Core design does **not** constitute acceptance of the Macro Adjustment or final Duration Evaluation Result.

## 3.6 Result Semantics and Traceability

The accepted Core Duration Evaluation Result has a **seven-level ordinal scale**:

```text
+3 strongly favorable
+2 favorable
+1 mildly favorable
 0 neutral
-1 mildly unfavorable
-2 unfavorable
-3 strongly unfavorable
```

These codes denote ordered economic judgments, **not cardinal differences, expected price returns, or risk-adjusted attractiveness**. In particular, stronger Long Duration scores under favorable rate-direction conditions do not guarantee that Long Duration is preferable after yield/carry, compensation, risk, and other Constituents are considered.

To explain a Duration result, preserve the relevant ETF Duration Exposure and representative tenor, the tenor-local Component Values and States, the applicable Core Rule Case and Core Result, any eventual Macro action, and the final Duration Evaluation Result. This lineage must keep Core and Macro judgments distinguishable; the final Result's additional semantics remain subject to Macro Adjustment design.

## 3.7 Accepted Design, Validation, and Limitations

**Accepted Core design (2026-10-10).** The six-month overlapping Yield Trend, common `±25 bp` entry thresholds, Hybrid-P3/H5 with immediate direct opposite-direction crossings, unchanged one-month Recent Yield Move and `±10 bp` thresholds, and the complete exposure-specific seven-level Core Rule Table are the accepted Duration Core contract. Earlier provisional alternatives do not supersede these definitions.

**Validation conclusion.** Historical review found meaningful occurrences of all nine Trend × Recent Move Rule Cases and frequent same-date differences across representative Treasury tenors, supporting exposure-local Core Evaluation. Historical review and consistency checks identified no material contradiction in the accepted Component definitions, ordinary State transitions, Rule Mapping, or intended exposure ordering. The immediate direct-reversal exception did **not** occur in the frozen historical dataset; it is a deliberate boundary convention, not an empirically optimized rule. Historical consistency does not uniquely determine adjacent ordinal categories, establish predictive investment performance, or prove economic optimality.

**Remaining limitations and work.** Duration Macro Adjustment and the full Duration Evaluation Result are not yet accepted. After Macro design is completed, run integrated historical diagnostics that expose the Core Result, Macro action, and final Result separately. Reopen the Core design only if a substantive economic, data-integrity, or architectural contradiction warrants it. Detailed experiments, implementation tasks, and intermediate validation logs remain outside this design document.

---

# 4. Curve Evaluation

**Design status — Provisional (not accepted).** This section records a proposed economic structure for review and MVP investigation. Except for the general scope already stated in the system architecture, its candidate Components, exposure representation, Core interpretation, and Result semantics are **not** accepted Curve contracts. Numerical parameters, Rule Cases, and scores remain open. The accepted Duration Core design in Section 3 must not be inferred to apply to Curve.

## 4.1 Economic Question and Scope

Curve Evaluation asks:

> Is the ETF's structural maturity / curve exposure relatively favorable or unfavorable under current Treasury term-structure conditions?

Its proposed subject is **relative maturity-location and curve-shape effects**, rather than the absolute interest-rate sensitivity of the ETF or the compensation received for accepting that exposure.

- **Duration** interprets yield-direction conditions for the exposure's interest-rate sensitivity, using the relevant tenor-local Components.
- **Curve** interprets relative yield relationships and their changes across maturities for the ETF's maturity exposure.
- **Rates Valuation** evaluates yield / carry and other compensation for accepting rates exposure, including term compensation where economically justified.

These distinctions concern **economic questions**, not mutually exclusive observations. The same Treasury yields or yield-direction Components may legitimately inform multiple Constituents when their interpretation is different. Duplicating essentially the same price effect or carry judgment must nevertheless be avoided in Core design and later Evaluation Combination.

Curve Core is an interpretation of observed current and historical conditions, **not a forecast** of future steepening, flattening, relative returns, or ETF prices. This is the same interpretive standard applied to Duration Core.

## 4.2 Evaluation Overview

The provisional analytical structure is:

```text
Treasury Raw Observations
           ↓
   [Feature Calculation]
           ↓
Curve Configuration + Curve Movement
  (candidate Component Values / States)
           │
           │          ETF Curve Exposure
           │        (structural benchmark /
           │          product characteristics)
           │                   │
           └─────────┬─────────┘
                     ↓
             [Curve Core Evaluation]
                     ↓
          Core Curve Evaluation Result
                     ↓
          [Macro Adjustment — TBD,
             only if justified]
                     ↓
             Curve Evaluation Result
```

Component calculations and classifications belong upstream in Bond Analysis and remain **independent of ETF Exposure Profiles**. The Curve Exposure Profile selects or characterizes the relevant exposure at Core Evaluation; it does not change Component definitions, parameters, Values, or States. The diagram proposes no mandatory Macro Adjustment and does not imply an accepted final Constituent Result.

## 4.3 Inputs and Exposure Representation

### ETF Curve Exposure — structural maturity characteristics

The preferred source is the ETF's **declared product design and reference benchmark**, not a classification estimated from the ETF's traded-price time history. The relevant descriptions may include target maturity bands, benchmark construction, physical-bond versus futures exposure, and, where available, explicit sensitivity measures. Actual-holdings or tracking-quality verification remains outside this Profile responsibility.

A practical **candidate MVP taxonomy** is:

| Curve Exposure | Intended structural meaning | Status |
|---|---|---|
| Short-end | Predominant exposure near the short maturity segment | Proposed |
| Belly | Predominant exposure near intermediate maturities | Proposed |
| Long-end | Predominant exposure near the long maturity segment | Proposed |

A representative maturity location may approximate a concentrated benchmark exposure. It does **not** fully specify sensitivity to non-parallel yield-curve changes. Two instruments with similar total duration or a similar headline maturity can have different distributions of interest-rate sensitivity across tenors. A key-rate duration profile or an appropriately documented maturity-distribution proxy may be needed for barbell, broad-maturity, STRIPS, futures-based, or otherwise atypical exposures. The initial MVP need not require full key-rate duration data for every synthetic exposure.

**Pending design decisions:** the accepted exposure taxonomy and covered ETF universe; the conditions under which representative location is insufficient; acceptable benchmark-based approximations; and treatment of exposure structures that cannot be characterized reliably from product documentation. A fixed structural profile used in historical scenarios must not be described as the ETF's actual historical holdings or sensitivity.

### Curve Configuration — relative yield levels

**Candidate Component concept:** the prevailing relative configuration of Treasury yields across selected maturity segments, such as a positive, approximately flat, or inverted slope.

For an illustrative long–short segment pair:

```text
Slope Value(t) = Yield_long(t) - Yield_short(t)
Candidate States: Positive / Flat / Inverted
```

A term-structure configuration is not a forecast and not automatically a favorable or unfavorable exposure judgment. A positive curve alone, for example, does not establish that Long-end exposure is preferable; any carry or roll-down interpretation must be reconciled with Rates Valuation.

**Pending Component design:** which tenor pairs or multiple segments matter; whether one slope adequately represents belly and long-end exposures; whether a separate curvature concept is needed; exact Value definitions and source observations; classification boundaries and stability mechanics. State labels above are candidates, not accepted classifications.

### Curve Movement — changes in relative yields

**Candidate Component concept:** the direction of change in the *relative* configuration of Treasury yields, not merely the absolute direction of an individual tenor's yield.

For the same illustrative slope:

```text
Curve Movement Value(t) = Slope Value(t) - Slope Value(t-h)
Candidate States: Steepening / Stable / Flattening
```

Configuration describes the **level** of the spread; Movement describes its **change**. A curve may remain inverted while steepening, or remain positive while flattening. These are distinct economic conditions, although they use related source observations.

A flattening event can occur while both yields rise, both fall, or move in opposite directions. Absolute rate direction is separately interpreted in Duration; any Curve classification that explicitly distinguishes bull/bear steepening or flattening must demonstrate why that additional distinction belongs in Curve rather than reproducing Duration.

**Pending Component design and MVP research:** movement horizon, smoothing, thresholds, stabilization, segment-specific movements versus one aggregate measure, and the possible need for curvature-change information. Consistency with any reused canonical tenor-local Yield Trend Component is required; reusing observations does not authorize redefining that Component for Curve.

## 4.4 Core Evaluation

The **candidate**, not accepted, Core structure is:

```text
Curve Configuration State
× Curve Movement State
× ETF Curve Exposure characteristics
→ Core Curve Evaluation Result
```

The provisional purpose of this mapping is to judge the relative suitability of an exposure's maturity location or distribution under the observed configuration and curve-shape movement. It must be **exposure-specific** rather than an ETF-independent preferred-maturity score subsequently adjusted for ETF characteristics.

A useful *candidate analytical reference* is a **parallel yield change**, under which curve shape does not change. Departures from that reference distinguish relative yield movements across maturity segments. When making price-effect comparisons, exposure sensitivities must be appropriately normalized; a given number of basis points does not imply equal returns across exposures with different dollar durations.

For example, if 2Y yields rise by 60 bp while 10Y yields rise by 20 bp, the 10Y–2Y slope falls by 40 bp (flattening). That creates a relative yield-change distinction between the two maturity locations. It does **not** by itself establish the 10Y ETF's total return, an unconditional buy signal, or continuation of the flattening.

The following substantive design questions remain open:

- Does Configuration change the economic interpretation of Movement, and if so through what mechanism other than carry / roll-down already owned by Rates Valuation?
- Should the full Configuration × Movement combination form the Rule Case, or should Configuration initially remain descriptive context? Neither priority nor a Rule Table is accepted.
- How should belly exposures, multiple curve segments, distributed sensitivities, and non-parallel twists be mapped without merely reproducing Duration judgments?
- Is the parallel-shift reference sufficiently well-defined for ordinal relative judgments, and what sensitivity normalization is needed?

**No Curve Rule Table or ordinal score assignment is accepted yet.** The MVP may compare explicit provisional mappings, but its experimental defaults must be labeled as such and must not be elevated into the authoritative design by implementation alone.

## 4.5 Macro Adjustment

```text
TBD — no separate Curve Macro Adjustment has been justified or accepted.
```

Policy expectations, inflation-related information, and term-premium mechanisms may influence the term structure, but their relevance alone does not establish a need for a sequential post-Core correction. If a distinct Curve economic question requires such information, first examine whether it belongs in the appropriate upstream Components and Curve Core. Do not implement a placeholder Macro adjustment merely to complete the diagram.

## 4.6 Result Semantics and Traceability

**Proposed Core meaning:** an exposure-specific, **relative** judgment about the favorability of the ETF's structural maturity exposure under observed term-structure conditions, distinct from absolute yield-direction suitability and rates compensation.

A favorable Curve Core Result would **not** mean that the ETF will rise in price, earn a positive return, outperform all other ETFs, or that yield-curve movements are forecast to persist. It can therefore coexist without contradiction with an unfavorable Duration Core Result for the same ETF.

**Pending decisions:** the precise neutral/reference condition, the amount and type of sensitivity normalization, whether to use an ordinal scale at all, the number and labels of Result categories, and how to distinguish neighboring categories economically. Curve need not copy Duration's seven-level scores or cardinalize their differences.

Traceability should preserve the ETF's documented Curve Exposure representation and its approximation status, the relevant curve segments, the Configuration and Movement Component Values / States, the applicable Core Rule Case or equivalent evaluation basis, and the resulting Core judgment. If a Macro stage is eventually justified, its action and the final Constituent Result must remain separately identifiable.

## 4.7 Provisional Design, Validation Needs, and Limitations

**Provisional design basis:** a structural ETF Curve Exposure defined from product/benchmark information; distinct ETF-independent candidate Components for Curve Configuration and Curve Movement; exposure-specific Core interpretation of relative maturity conditions; and an explicitly nonforecast Result meaning. These are research propositions, **not accepted Curve model parameters or mappings**.

**Design decisions required before a Core contract can be accepted:** the role of Configuration in Core, exposure representation and coverage, economically justified comparison/reference semantics, overlap boundaries with Duration and Rates Valuation, and Core Result categories/mapping.

**MVP-suitable investigations:** candidate Treasury segments and shape measures; lookback horizons, smoothing, thresholds, and stabilization; observation coverage and structural gaps; frequencies and persistence of candidate Component States / Rule Cases; behavior under parallel shifts, twists, inversions and reinversions, and belly-led moves; sensitivity to exposure representation and alternative provisional mappings. Historical analysis may reveal inconsistency or weak interpretation but does not alone validate future relative returns or establish the correct economic mapping.

The Curve MVP is a **research instrument**, not implementation acceptance. Subsequent review should update this section with accepted definitions and concise validation conclusions, while retaining detailed experimental evidence in `validation/`.

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
