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

## 2. Positioning Context Module

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

## 3. ETF Selection Module

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
