# Bondview — Module and Configuration Working Notes

This document records evolving ideas that are not yet mature enough to belong in the system architecture or a dedicated module-design document. New ideas may be added during future design discussions. When an area becomes sufficiently stable, it should be considered for extraction into its own authoritative design document.

## 1. Model Configuration

The exact Configuration Schema is not yet defined.

Current design direction is that Model Configuration should describe model semantics without forcing every semantic layer to use different implementation mechanics.

For stance-related calculation, the current conceptual requirement is:

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

Current working ideas include:

- lookback horizons belong primarily to Features rather than to Components or Stance Rule Mapping;
- one Component may depend on multiple Features with different horizons;
- State Classification may be threshold-based or rule-based over multiple lower-level model-ready inputs;
- Stance Rule Mapping and Constraint Rule Mapping remain semantically distinct from State Classification even if they reuse equivalent discrete-state mapping mechanics;
- temporal persistence, stabilization, or hysteresis should be represented separately from Feature lookback horizons;
- Model Configuration should preserve semantic roles even when implementation capabilities are reused;
- exact YAML structure, schema shape, fallback representation, and result-contract integration remain open.

As other modules become more concrete, Model Configuration may need to describe their module-specific inputs or parameters as well. This should be added only when those responsibilities have sufficiently stable semantics.

## 2. Duration Stance Implementation Working Notes

This section records implementation-oriented Duration discussions that are not yet authoritative model design.

The canonical seven-level Duration stance scale and the complete 3 × 3 Stance Rule Table defined in `bondview_stance_design_draft.md` are treated as fixed inputs to this work. The purpose here is to determine how the two Duration Market Components can be calculated from market data without reopening those economic-model decisions.

Once the Feature transformation is sufficiently confirmed, the corresponding Duration sections of `bondview_stance_design_draft.md` should be updated and this working material can be reduced or removed.

### Current Raw Observation direction

The current working choice for the Duration market branch is:

- FRED `DGS10` — 10-Year Treasury Constant Maturity Rate.

Both Duration Market Components are expected to be derived from the same long-end yield Raw Observation:

```text
DGS10
  ├──→ Long-End Yield Trend
  └──→ Recent Long-End Yield Move
```

The distinction between the two Components is therefore expected to come from Feature transformation and horizon rather than from separate Raw Observations.

### Current transformation direction

The current preferred baseline is a moving-average-difference construction.

The general working form uses up to four horizons:

```text
Recent Feature
= MA(R_fast) - MA(R_slow)

Trend Feature
= MA(T_fast) - MA(T_slow)
```

with the intended ordering:

```text
R_fast < R_slow ≤ T_fast < T_slow
```

This formulation allows the Recent and Trend Features to use separate fast/slow comparisons while still permitting a shared intermediate horizon.

When:

```text
R_slow = T_fast
```

the general formulation reduces to the previously discussed three-MA structure:

```text
Recent = MA(short)  - MA(medium)
Trend  = MA(medium) - MA(long)
```

When:

```text
R_slow < T_fast
```

all four horizons may be distinct:

```text
Recent = MA(short)      - MA(recent-reference)
Trend  = MA(trend-fast) - MA(long)
```

The shared-middle case should therefore be treated as one candidate configuration within the general horizon specification rather than as a separate model architecture.

The exact moving-average definition is not yet fixed. In particular, whether the authoritative calculation should use a simple moving average or another deliberately chosen averaging convention remains open.

### Why moving averages are the current baseline

The initial endpoint-change formulation was:

```text
Trend(t)  = yield(t) - yield(t - h_trend)
Recent(t) = yield(t) - yield(t - h_recent)
```

This is simple and directly expresses two horizons, but it depends on particular endpoint observations. If the resulting states are unstable, it may be difficult to distinguish a poor horizon choice from endpoint sensitivity or from a later need for stabilization logic.

Using moving averages removes much of the single-observation endpoint-sensitivity issue before horizon comparison begins. This should make later diagnosis cleaner:

```text
Raw DGS10 observations
        ↓
MA-based Features
        ↓
State Classification
        ↓
Core Stance behavior
        ↓
remaining instability, if any
        ↓
possible stabilization / hysteresis
```

Endpoint change is therefore no longer an active candidate for the authoritative transformation. It may remain useful as a simple diagnostic benchmark.

Other transformations previously discussed remain fallback candidates rather than part of the initial comparison:

- regression slope;
- split-window mean difference.

They should be brought back into active comparison only if the MA-based construction reveals a substantive transformation-level problem that cannot reasonably be addressed through horizon or threshold selection.

### State Classification and normalization

Each Feature will eventually be classified independently into:

```text
falling
stable
rising
```

before entering the existing 3 × 3 Stance Rule Table.

Conceptually:

```text
Trend Feature
        ↓
falling / stable / rising
        │
        ├──────────────┐
        │              │
Recent Feature         │
        ↓              │
falling / stable / rising
        │              │
        └──────┬───────┘
               ↓
       3 × 3 Stance Rule Table
               ↓
           Core Stance
```

Because the Stance Rule Table consumes discrete Component States rather than directly combining raw Feature magnitudes, cross-Feature normalization is not currently required.

Normalization may be reconsidered later if fixed thresholds prove unsuitable across materially different yield-volatility regimes, but it should not be introduced before evidence shows that it is needed.

The exact `falling / stable / rising` thresholds remain unresolved. A provisional symmetric stable band may be used for initial horizon comparison, but threshold refinement should remain separate from horizon selection as far as practical.

### Initial historical comparison strategy

The first validation pass should use a deliberately minimal Core Duration pipeline:

```text
DGS10
  ↓
candidate MA Features
  ↓
provisional State Classification
  ↓
Long-End Yield Trend State
        ×
Recent Long-End Yield Move State
  ↓
existing 3 × 3 Stance Rule Table
  ↓
Core Stance
```

The initial comparison should exclude:

- Macro Constraint calculation;
- Constraint Application;
- hysteresis;
- state-transition confirmation;
- stance-level stabilization;
- ETF Selection.

The purpose is first to determine whether the underlying Feature and horizon structure produces economically sensible Core Stance behavior. Hysteresis and similar mechanisms should be treated as later corrective mechanisms for residual transition instability, not as a way to rescue a poorly behaving basic Feature specification.

Candidate horizon sets should be compared using more than transition count alone. Useful diagnostics include:

- Component-State occupancy and persistence;
- occupancy of the nine Stance Rule Cases;
- frequency and persistence of Core Stance transitions;
- frequency of counter-trend Rule Cases;
- whether counter-trend cases correspond to plausible historical transition periods;
- dependence between Trend and Recent Feature values;
- robustness to modest changes in nearby horizons;
- whether the resulting investment timescale is sufficiently active for the intended use without becoming dominated by short-lived noise.

A rough opportunity-frequency requirement, such as capturing meaningful changes at least on the order of once per year, may be useful as a sanity constraint. It should not by itself be the optimization target.

### Historical validation vs Historical Context

Historical model calibration and validation should not overload the canonical term **Historical Context**.

Under the current vocabulary, Historical Context is a Diagnostics concept built from authoritative calculated model outputs after the model behavior is defined.

For Duration Feature development, historical yield episodes or a curated set of rate-market events may still be useful as qualitative reference points during validation. Such event references should be treated as validation material rather than as canonical Historical Context or as a hidden input to the model.

Full-history statistics should remain important so that horizon selection is not tuned only to a small set of famous events.

### Current open decisions

The main unresolved Duration market-branch questions are:

- exact moving-average convention;
- candidate values for `R_fast`, `R_slow`, `T_fast`, and `T_slow`;
- whether the best horizon configuration uses `R_slow = T_fast` or distinct intermediate horizons;
- provisional and final thresholds for `falling / stable / rising`;
- whether reasonable nearby horizon choices produce broadly similar behavior;
- whether any volatility-aware normalization is eventually justified;
- whether residual instability remains after MA aggregation and therefore justifies hysteresis or other stabilization;
- whether regression slope or split-window mean difference needs to be reconsidered after the MA-based baseline is evaluated.

## 3. Positioning Context Module

### Purpose and architectural gap

Positioning Context is intended to cover market-wide or exposure-level conditions that are not adequately represented by either authoritative stance calculation or individual ETF evaluation.

```text
Stance Calculation
→ What bond exposure is economically favored?

Positioning Context
→ Is the favored exposure unusually crowded, extended, or otherwise difficult to express cleanly?

ETF Selection
→ Which specific ETF implements that exposure appropriately?
```

The motivation is that a valid stance can coexist with an unfavorable implementation backdrop.

For example, a strongly positive Duration stance may still coexist with unusually bullish positioning, extreme sentiment, or crowded long-duration exposure. Such information does not necessarily invalidate the economic Duration stance. At the same time, it is not an intrinsic characteristic of one ETF and therefore does not naturally belong inside ETF-specific Instrument Evaluation.

Positioning Context therefore appears to have an intermediate role between stance interpretation and ETF selection.

### Boundary with other modules

Current working boundaries are:

- it should not recreate Stance Calculation;
- it should not directly rewrite Core Stance or Final Stance;
- it should represent exposure-level or market-wide implementation context rather than individual ETF characteristics;
- ETF Selection may consume the result as additional context when deciding how readily an otherwise valid stance should be implemented;
- the exact downstream effect is not yet defined.

The module may ultimately prove less useful if reliable positioning data cannot be obtained. The architectural need can still be recorded even if automated implementation is deferred or omitted.

### Possible information domains

Potential information domains include, without yet making any of them authoritative:

- positioning;
- sentiment;
- crowding;
- unusually extended exposure;
- other market-wide indicators that describe how heavily a favored exposure may already be expressed.

No specific observations, data vendors, indicators, transformations, or score construction have been selected.

### Possible production paths

The production logic is intentionally unresolved.

Possible implementation paths may include:

```text
data-derived calculation ───────────┐
                                    ├─→ Positioning Context Module
explicitly supplied assessment ─────┤
                                    │
other justified method ─────────────┘
                                              ↓
                           common Positioning Context output boundary
```

An explicitly supplied user or trusted-expert assessment is one possible path rather than a bypass of the module.

For example, if a user has a trusted bond specialist whose positioning view is considered useful, that assessment might eventually be represented directly in whatever canonical Positioning Context representation is adopted. This does not imply that the canonical representation must be a numeric score.

The key interface idea is that different valid production paths should expose semantically equivalent results through the same Positioning Context output boundary. The choice of path should not require downstream modules to use a different interface.

The production path may still be retained as diagnostic or audit metadata if useful, but this is separate from the semantic result consumed downstream.

### Unresolved output design

The output representation is intentionally open. Possibilities might include:

- a score;
- a discrete state or label;
- multiple dimensions rather than one scalar;
- confidence or applicability metadata;
- another representation justified by later design work.

None of these is currently selected.

Absence of usable Positioning Context information should not automatically be interpreted as a neutral positioning signal. The eventual design should distinguish lack of information from whatever representation is chosen for genuinely neutral conditions.

### Open design questions

Important unresolved questions include:

- whether Positioning Context should be one-dimensional or multi-dimensional;
- which observations, if any, can be obtained reliably enough for automated calculation;
- whether sentiment and positioning belong in one result or separate dimensions;
- whether expert/user assessments should coexist with calculated results or simply provide an alternative production path;
- whether Positioning Context affects only final selection, implementation strength/timing, or another downstream decision;
- what output semantics are stable enough to define a Result Contract;
- whether the practical benefit is large enough to justify implementation complexity.

## 4. ETF Selection Module

The current canonical flow remains:

```text
ETF Universe
        +
Bond-Exposure Stance Set
        ↓
[Exposure Fit Evaluation]
        ↓
[Instrument Evaluation]
        ↓
[ETF Selection]
```

Current architecture distinguishes two questions:

```text
What bond exposure is favored?
→ stance calculation

Which ETF expresses that exposure appropriately
and is attractive enough relative to alternatives?
→ ETF selection
```

Current candidate Instrument Evaluation considerations include:

- yield or carry;
- duration or maturity exposure;
- price behavior;
- fees and liquidity;
- tracking or index characteristics;
- currency or hedging exposure where relevant;
- the applicable low-risk or risk-free alternative where required.

Positioning Context introduces an additional possible input to the ETF-selection responsibility, but its exact placement is unresolved.

Possible future designs include consuming Positioning Context:

- after Exposure Fit has identified ETFs that correctly express the stance;
- alongside Instrument Evaluation as broader exposure-level context;
- near the final selection/implementation decision.

Whichever placement is chosen, Positioning Context should not be disguised as an ETF-specific characteristic if the information is actually market-wide or exposure-level.

Likewise, ETF Selection should consume authoritative stance outputs rather than independently recreating Duration, Curve, or Credit logic.

Further ETF-selection design—including exact scoring, filtering, ranking, treatment of alternatives, and how Positioning Context affects final implementation—remains open and should be moved to a dedicated ETF-selection document when sufficiently mature.
