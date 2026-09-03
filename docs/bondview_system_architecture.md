# Bondview-v2 System Architecture

## Document Purpose

This document defines the system-level architecture of `bondview-v2`.

The project’s ultimate purpose is to support bond-ETF selection and review. The system separates four different kinds of information before the final ETF decision:

- preferred bond-exposure structure;
- broader macroeconomic context;
- FX and currency-hedging information where applicable;
- ETF- and index-specific information.

This document is authoritative for relationships among major system responsibilities. It does not define the internal calculation contracts of `market_stance` or the detailed model definition of `macro_context`.

## Related Documents

```text
bondview_system_architecture.md
│
├── market_stance_architecture_contract.md
├── market_stance_skeleton_implementation_strategy.md
├── market_stance_capability_contracts.md
└── macro_context_contract.md
```

Future ETF-selection documentation may be added when that module is designed.

# 1. System Goal

The final problem is not simply:

> What is the bond-market stance?

It is:

> Which available bond ETF is appropriate under the current bond-market structure, macroeconomic environment, currency conditions, and instrument characteristics?

The conceptual flow is:

```text
bond-market observations
        ↓
market_stance
        ↓
MarketStanceResult ───────────────┐
                                  │
macroeconomic observations        │
        ↓                         │
macro_context                     │
        ↓                         │
MacroContextResult ───────────────┼──→ ETF selection / review
                                  │
FX information ───────────────────┤
                                  │
ETF / index information ──────────┘
```

`market_stance` and `macro_context` are sibling analytical inputs. Neither is the final ETF decision.

# 2. Major Responsibilities

## 2.1 `market_stance`

`market_stance` evaluates the preferred structure of bond exposure.

Its initial stance outputs are:

- Duration;
- Curve;
- Credit.

These outputs answer questions such as:

- whether shorter or longer duration is preferable;
- which maturity or curve positioning is preferable;
- how much or what quality of credit exposure is preferable.

They do not by themselves mean that bonds are absolutely attractive relative to unrelated asset classes.

## 2.2 `macro_context`

`macro_context` describes broader macroeconomic conditions relevant to interpreting the attractiveness of bond exposure.

Initial dimensions may include:

- growth;
- inflation;
- monetary policy;
- real-rate conditions.

It should not duplicate Duration, Curve, or Credit.

It may expose separate scores or states and is not required to collapse all dimensions into one universal macro score.

## 2.3 FX Information

FX is distinct from Duration, Curve, and Credit.

For a KRW-based investor holding a Korea-listed ETF whose underlying assets are foreign-currency bonds, realized return may depend on:

- underlying currency;
- exchange-rate behavior;
- hedged or unhedged structure;
- hedge ratio;
- hedge cost or carry where relevant.

FX belongs at the downstream decision boundary unless later complexity justifies a separate `fx_context`.

A separate FX module should not be created merely for symmetry.

## 2.4 ETF and Index Information

ETF selection may require information not owned by either analytical context module, including:

- underlying index;
- effective duration;
- maturity distribution;
- credit quality;
- currency exposure;
- hedging policy;
- fees;
- tracking characteristics;
- liquidity;
- market price behavior;
- premium or discount behavior;
- distribution characteristics;
- other instrument-specific constraints.

The detailed ETF-selection model is outside the current contract.

# 3. Relative Exposure Versus Broader Attractiveness

The main semantic separation is:

```text
market_stance
    → what type of bond exposure is preferable?

macro_context
    → what broader macro environment are we in?

ETF selection
    → given both, which instrument should be selected or avoided?
```

For example:

```text
MarketStanceResult
    Duration: prefer longer
    Curve: prefer intermediate sector
    Credit: prefer higher quality

MacroContextResult
    Growth: weakening
    Inflation: easing
    Policy: easing
    Real rate: restrictive but falling
```

The downstream module can interpret the combination without forcing the same macro information into every stance.

This keeps two questions separate:

1. relative structure within bond exposure;
2. broader attractiveness of taking that exposure.

# 4. Data and Source Architecture

## 4.1 Source Acquisition Versus Pure Calculation

External acquisition and pure calculation are separate responsibilities.

```text
FRED / exchange / vendor / local file
        ↓
source adapter
        ↓
input assembly
        ↓
accepted in-memory snapshot
        ↓
analytical execution
```

FRED download logic may exist in the repository and may even live in a package associated with an analytical module if that organization is useful.

The architectural requirement is narrower:

> Once an accepted runtime input has been supplied, the pure calculation path must not require network access, credentials, environment-variable lookup, source-specific clients, or file acquisition.

The source adapter and execution engine may therefore belong to the same broader module while remaining separate responsibilities.

## 4.2 Shared Raw Observations

The same raw observation may be used by more than one analytical module.

For example, a policy-rate series may be used:

- by `market_stance` to construct a bond-market relationship such as a yield-policy spread;
- by `macro_context` to describe policy conditions.

This is permitted because raw observations are not exclusively owned by one derived meaning.

What is prohibited is duplicated ownership of the same derived concept.

If `macro_context` owns an authoritative policy-restrictiveness state, `market_stance` should not independently calculate an equivalent policy-restrictiveness state under another name.

## 4.3 Scenario Coherence

Outputs combined for one ETF decision should represent a coherent scenario.

The system should preserve, where relevant:

- observation dates;
- revision vintages;
- alignment choices;
- market or country identity;
- investor currency;
- model or configuration version.

# 5. Shared Calculation Mechanics

## 5.1 Avoid Both Premature Generalization and Duplication

The system should avoid both:

```text
premature shared framework        duplicated implementations
            ✗                             ✗
```

The preferred rule is:

> Extract on actual second use.

A calculation may initially live with the module that first genuinely needs it.

If a second sibling module later needs semantically identical behavior, the implementation should be extracted to a neutral owner rather than copied.

## 5.2 Neutral Ownership

Conceptually:

```text
market_stance ─────┐
                   ↓
          neutral calculation capability
                   ↑
macro_context ─────┘
```

The neutral owner may initially be one small module rather than a large shared package.

The architecture does not require a hierarchy such as:

```text
shared/
    scoring/
    normalization/
    classification/
    stabilization/
```

unless actual complexity later justifies it.

## 5.3 No Permanent Sibling-to-Sibling Utility Dependency

`macro_context` should not permanently depend on methods semantically owned by a `MarketStanceCalculator`, and `market_stance` should not depend on a `MacroContextCalculator` merely to reuse generic mathematics.

If a method is genuinely generic enough for both sibling modules, that is evidence that its proper owner is neutral.

## 5.4 Extraction Criteria

Extraction is justified when:

- a second module actually needs the behavior;
- the behavior is semantically equivalent, not merely numerically similar;
- the input/output contract can be shared without domain leakage;
- reuse avoids duplicate authoritative logic;
- extraction does not create more complexity than it removes.

# 6. Market, Investor Currency, and FX

Market identity and investor currency must be considered together when applying `market_stance`, `macro_context`, and ETF-specific information.

The analytical results must describe the market underlying the ETF, while FX becomes relevant when the underlying currency differs from the investor's base currency.

Conceptually:

```text
market-specific MarketStanceResult ─┐
                                    │
market-specific MacroContextResult ─┼──→ ETF selection / review
                                    │
FX information, if applicable ──────┤
                                    │
ETF / index information ────────────┘
```

## 6.1 Market Identity

`MarketStanceResult` and `MacroContextResult` MUST preserve enough metadata to identify the market or country context they describe.

For example:

- a U.S.-bond ETF should generally use a U.S. bond-market stance;
- the associated macro context should generally describe the U.S. macroeconomic environment;
- a Korean domestic-bond ETF should generally use Korean bond-market and Korean macroeconomic context.

Downstream logic MUST NOT accidentally combine outputs from incompatible markets.

A cross-market combination MAY be supported when deliberately defined, but it must not occur implicitly.

## 6.2 Investor Currency and FX Applicability

FX is relevant when the currency exposure of the underlying investment differs from the investor's base currency.

For a KRW-based investor, relevant FX information for a foreign-bond ETF MAY include:

- underlying currency;
- KRW exchange-rate behavior;
- currency-hedged or unhedged structure;
- hedge ratio;
- hedge cost or carry where relevant.

For a KRW investor holding ordinary KRW-denominated domestic-bond exposure, foreign-exchange information may be not applicable.

FX applicability is therefore conditional on the relationship among:

- underlying bond market;
- underlying currency exposure;
- investor base currency;
- ETF hedging structure.

## 6.3 Korea-Listed U.S. Bond ETFs

For a KRW investor evaluating a Korea-listed ETF that holds or tracks U.S. bonds, the downstream decision may combine:

- a U.S.-bond `MarketStanceResult`;
- a U.S.-relevant `MacroContextResult`;
- USD/KRW and currency-hedging information;
- ETF- and index-specific information.

The fact that the ETF is listed in Korea does not change the market identity of the underlying bond exposure.

The ETF-selection layer owns the interpretation of how the underlying U.S. bond exposure, macro context, currency exposure, and ETF structure interact.

## 6.4 Korea-Listed Korean Bond ETFs

The same overall architecture can be used for Korea-listed Korean-bond ETFs.

The downstream decision may combine:

- a Korean-bond `MarketStanceResult`;
- a Korean `MacroContextResult`;
- ETF- and index-specific information.

For a KRW investor holding KRW-denominated domestic-bond exposure, ordinary foreign-exchange exposure is normally not applicable.

The structural difference from the U.S.-bond case is therefore small. The main changes are the market-specific analytical inputs and the conditional presence or absence of FX information.

## 6.5 Why FX Is Not a Bond Stance

Duration, Curve, and Credit describe dimensions of the underlying bond exposure.

FX describes how foreign-currency exposure is translated into the investor's base-currency return.

```text
Duration / Curve / Credit
    → underlying bond-exposure structure

FX
    → investor-currency translation and hedge exposure
```

FX therefore SHOULD NOT become a fourth peer stance merely because it affects the final ETF decision.

A separate `fx_context` module also SHOULD NOT be introduced merely for symmetry with `macro_context`.

If FX analysis later develops substantial independent calculation logic, a separate result boundary MAY be considered at that time.

# 7. Result Boundaries

## 7.1 Market Stance Result

The completed market-stance result is authoritative for its declared bond-exposure outputs.

It is not the sole downstream information source.

## 7.2 Macro Context Result

The completed macro-context result is authoritative for its declared macro outputs.

It does not overwrite or reinterpret Duration, Curve, or Credit.

## 7.3 ETF Decision

The ETF-selection responsibility owns the combination of:

- market stance;
- macro context;
- FX information where applicable;
- ETF and index information;
- later approved instrument-level signals.

Upstream modules should not know which particular ETF will eventually be selected.

# 8. Architectural Review Triggers

System-level architectural review is appropriate when a change:

- moves a major decision responsibility between modules;
- makes one sibling module unexpectedly depend on another sibling's domain result;
- changes a public result boundary;
- introduces a new major context such as an independent FX model;
- creates a second authoritative producer for the same derived concept;
- introduces a large shared framework without demonstrated second use;
- requires ETF-selection logic to reach into upstream internal implementation details.

# 9. Summary

```text
market_stance ─────────→ MarketStanceResult ───┐
                                               │
macro_context ─────────→ MacroContextResult ───┼──→ ETF selection / review
                                               │
FX information ────────────────────────────────┤
                                               │
ETF / index information ───────────────────────┘
```

`market_stance` defines preferred bond-exposure structure. `macro_context` describes the broader macro environment. FX represents investor-currency exposure where relevant. ETF-specific information describes the investable instrument. The downstream ETF-selection responsibility combines these distinct inputs.
