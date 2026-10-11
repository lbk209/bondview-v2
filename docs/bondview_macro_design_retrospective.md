# Bondview-v2 — Macro Design Retrospective

**Purpose:** Preserve and critically revisit the development of Bondview-v2's macro-related design, including abandoned alternatives, unresolved objections, and changes in reasoning. This is **not** a proposal for immediate implementation or a final decision to retain or remove Macro Adjustment.

**Review date:** 2026-10-11  
**Authoritative design baseline for comparison:** [`update_design` branch](https://github.com/lbk209/bondview-v2/tree/update_design), particularly [`bondview_system_architecture.md`](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_system_architecture.md), [`bondview_exposure_evaluation_design.md`](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_exposure_evaluation_design.md), and [`bondview_vocabulary.md`](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_vocabulary.md).  
**Historical scope:** Bondview-v2 design discussions from early September to October 11, 2026. The original `lbk209/bondview` project is reference-only and must not be treated as establishing v2 decisions.

> **How to read this record.** The narrative reconstructs the reasoning process rather than treating the latest view as an inevitable conclusion. A proposition marked *proposed*, *questioned*, or *rejected as a justification* is not an accepted model contract. Earlier terminology—`macro_context`, `market_stance`, `Macro Constraint`, `Final Stance`—is retained where needed to describe historical alternatives. It must not be substituted for the current v2 terminology without an explicit design revision. The exact dates and boundaries between conversational stages are approximate; the linked `update_design` documents, not this retrospective, define the current accepted architecture.

---

## 1. Executive review: the question beneath the design

The central controversy evolved from **“How should macroeconomic information be incorporated?”** to **“What economically distinct question would a separate macro stage answer?”**

Several different propositions were at times treated as though they implied one another:

1. Inflation, monetary policy, growth, and employment conditions matter economically to bonds.
2. These observations differ from Treasury yields, yield curves, and credit spreads as data sources and subject matter.
3. Bondview's market-derived Components cannot preserve every piece of macroeconomic information.
4. Macro information may therefore deserve to modify an already exposure-specific Core result.
5. That modification should be a distinct, predefined architectural stage.

Propositions 1–3 are plausible in varying degrees. **They do not, by themselves, establish propositions 4 or 5.** This missing logical step became the decisive issue.

The present working assessment is that no compelling, economically independent use of the predefined Macro Adjustment stage has yet been established for **Duration, Curve, Credit, or Rates Valuation**. This is a reason to reopen the stage's architectural justification, **not** a settled decision to remove it. A future example could change the assessment.

The review also exposes a process error: the design invested heavily in making Macro Adjustment architecturally coherent—downstream of Core, exposure-specific, nonduplicative, traceable—without first demonstrating that a separate adjustment was economically needed.

---

## 2. Historical evolution of the concept

### 2.1 Early September: independent `macro_context` versus `market_stance`

An early v2 framing distinguished a broader macroeconomic environment from a market-oriented view of Duration, Curve, and Credit. An important motivation was the difference between:

- **Relative or structural bond choice:** Which duration, curve, or credit exposure is suitable within the bond universe?
- **Absolute attractiveness:** Are bonds attractive at all relative to cash or another low-risk alternative?

At one point, `macro_context` was contemplated as a sibling assessment alongside `market_stance`, capable of describing broader economic circumstances or absolute attractiveness. There was also discussion of a macro gate, versus softer penalties or boosts.

**Appeal:** The market's preferred bond structure need not imply an investor should own bonds instead of cash. A broader context might prevent a structurally favorable but economically unattractive choice.

**Objection:** A free-standing macro view risked becoming a second bond-attractiveness model, with overlapping economic inputs and unclear ownership. Cash-relative attractiveness might instead belong in valuation or final-choice logic. Merely naming two outputs differently does not make them economically independent.

**Status:** Historical alternative, not the `update_design` architecture.

### 2.2 September 3–4: peer model versus supporting-context model

Two broad arrangements were debated:

```text
Peer / sibling model:
Market Stance + Macro Context -> broader bond assessment / ETF decision

Supporting-context model:
Shared macro-derived conditions -> selectively inform stance-specific rules
```

The supporting-context idea was attractive because Inflation Trend might matter to Duration differently from Credit, and a single independent macro score could erase those differences. `macro_context` consequently began to look less like an independent major Module and more like reusable macro-derived states or Features consumed selectively by other evaluations.

The user pressed a more fundamental objection at this stage: **Treasury yields and credit spreads already reflect market expectations about inflation, Fed policy, growth, and risk.** Adding separate macro conditions might count the same forces twice. The claim that macro data were *orthogonal* to market data was not defensible merely because the sources differed.

**What changed:** The design moved toward selective integration and away from an ETF-independent peer macro score.

**What remained unanswered:** Why should any macro condition modify a stance, rather than simply help explain it?

### 2.3 Approximately September 8–13: `Core Stance` followed by `Macro Constraint`

A stance-oriented design developed this sequence:

```text
Market-derived Rule Case -> Core Stance
Macro-derived Rule Case -> Constraint Action
Core Stance + Constraint Action -> Final Stance
```

Candidate actions included pass-through, weakening, strengthening, caps, directional restrictions, and exceptional hard rejection. The preference shifted away from a universal binary macro gate toward selective constraints. A complete Cartesian product of all market and macro cases was not required simply to express the model; it could instead be used in diagnostics.

**Appeal:** Core preserved an interpretable market judgment. Macro conditions would limit or qualify its expression without pretending to reconstruct the entire rates, curve, or credit model. Duration, Credit, and Curve could receive different actions from the same upstream macro condition.

**Objection:** A cap or attenuation is still a substantive economic decision. Changing from an additive macro score to a constraint reduces the *form* of duplication but does not demonstrate independent *information value*. An “unchanged” or pass-through action does not cure the weakness of the nontrivial actions.

The question of bonds versus cash continued to complicate this design. A Core Stance could identify a relative exposure preference without establishing absolute attractiveness; however, that gap did not establish that a macro constraint was the proper remedy.

**Status:** Historical v2 design stage; later replaced by exposure-specific Constituent terminology.

### 2.4 Mid-September: the compensation problem surfaced

There was a particularly revealing discussion about yield **level** versus yield **direction**:

- A Duration model based on direction might miss whether the investor is adequately compensated for taking duration risk.
- In Credit, the difference between “spreads wide and tightening” and “spreads tight and tightening” is material; spread direction alone is insufficient.
- A provisional alternative considered a stance-local valuation or compensation adjustment alongside a macro constraint.

**Appeal:** This identified a real economic incompleteness in direction-only analysis.

**Why the allocation was questioned:** Yield level, carry, and compensation are not inherently macroeconomic adjustments. They directly concern the economics of the exposure. The later four-Constituent decomposition assigned this distinct question to **Rates Valuation**. The example is useful because it shows that a substantive missing consideration can be addressed by a **different economic question**, not by forcing it into a macro stage.

This shift does **not** establish that Duration Core is complete; rather, its limited mandate is intentional.

### 2.5 Late September: implementation and redesign clarified the boundary

Earlier validation/implementation discussions tested how Trend, Recent Move, Inflation, and Policy might be combined. One reviewed approach effectively treated the four as peer votes. That was criticized because it flattened the intended distinction between market-based Core and subsequent macro qualification.

This matters for the historical reconstruction: **there was a legitimate architectural concern about conflating two stages, conditional on having chosen those stages in the first place.** Rejecting a flattened implementation was consistent with the *then-current* design, but did not validate the economic necessity of Macro Adjustment itself.

As Bondview-v2 moved away from market-wide “stances” toward evaluating ETF **Exposure Profiles**, the current Constituent structure emerged:

```text
ETF Exposure Profile + relevant Core Components
              -> exposure-specific Core Evaluation Result
              -> Macro Adjustment (where applicable)
              -> Constituent Evaluation Result
```

The current Constituents became **Duration, Curve, Credit, Rates Valuation**. Macro Adjustment remained an optional evaluator-specific step, not an independent peer market assessment. This solved several problems of ordering, exposure specificity, and upstream Component authority, but did not settle its distinct economic purpose.

**Current baseline:** `update_design` system architecture §§4.2.1–4.2.2; exposure evaluation design §§2.1–2.2 and 3.5.

### 2.6 October: accepted Duration Core, followed by the Macro design challenge

Duration Core was accepted independently of Macro Adjustment. It uses exposure-local Treasury tenors (Short/6M, Intermediate/10Y, Long/30Y), six-month Yield Trend and one-month Recent Yield Move, state classification, and an exposure-specific ordinal Rule Table. The seven-level Core categories express an economic judgment about rate-direction conditions for the relevant exposure; they are **not** price forecasts or cardinal expected returns.

This made the next task concrete: specify what Macro Adjustment would add **after** an already exposure-specific Duration Core Result.

An initial candidate used **Inflation Trend** and **Policy Direction**, with a conflict-only rule: when inflation and policy conditions conflicted with a strong Duration Core judgment, attenuate or cap Core rather than produce an independently bullish/bearish macro score.

That candidate was subsequently challenged more seriously than earlier stage-format discussions had been. The decisive question became:

> What economically meaningful property of an ETF's duration exposure can inflation or monetary-policy conditions change that is not already captured by rate-direction Core and does not properly belong to another Constituent?

No sufficiently convincing answer was established. The provisional conflict-only rule was therefore **not accepted**. The discussion then extended the challenge to Curve, Credit, and Rates Valuation, ultimately questioning whether a predefined Macro Adjustment stage is required anywhere.

---

## 3. Inventory of proposed ideas and their disposition

| Proposal or intuition | Original attraction | Why it was challenged | Current assessment |
|---|---|---|---|
| Independent `macro_context` as peer to market stance | Describe broad macro conditions; perhaps absolute bond attractiveness versus cash | Duplicative market judgment, unclear ETF specificity, unclear economic ownership | Not current architecture |
| Universal macro gate | Avoid favorable exposures under adverse macro regimes | Too coarse; macro effects differ across exposures and constituents | Abandoned as a general design |
| Macro penalty/boost | More nuanced than a binary gate | Still needs economic justification for direction and magnitude | No accepted general rule |
| Stance-specific Macro Constraint | Preserve market-based Core while qualifying it selectively | A distinct processing stage is not automatically a distinct economic contribution | Historical design; necessity unresolved |
| Make Trend, Recent Move, Inflation, and Policy four peer votes | Simple implementation | Confuses Core and secondary macro semantics under the then-accepted design; potential double counting | Rejected relative to that stage-based design |
| Inflation Rising + Policy Tightening weakens bullish Duration Core | Seemingly conflicting evidence of inflation pressure | Bond yields anticipate macro developments; policy tightening may *cause* lower future inflation/yields; no derived monotonic rule | Provisional hypothesis not accepted |
| Inflation Falling + Policy Easing weakens bearish Duration Core | Symmetric counter-signal | Same forward-looking-price and policy-response ambiguity | Provisional hypothesis not accepted |
| Macro modifies Core only by capping or attenuation | Avoid independent market forecast and limits double counting | A cap remains an economic claim; reduced computational overlap is not proof of relevance | Mechanically coherent, economically unjustified so far |
| Use yield level or compensation as adjustment to directional stance | Captures dimension missed by direction-only rule | Compensation has distinct responsibility, leading toward Rates Valuation | Better handled through valuation question |
| Retain Macro Adjustment as an optional stage “just in case” | Future extensibility without breaking architecture | A placeholder is not a demonstrated responsibility and may bias future designs to fill it | Under architectural reconsideration |
| Remove predefined Macro stage; let each Constituent consume justified market and macro Components | Align inputs with economic question; avoid artificial data-source boundary | Requires review of terminology, traceability, current docs and possibility of a genuinely sequential qualification | Plausible simplification, **not yet accepted** |

“Rejected” here generally means **rejected as a currently adequate justification**; it is not proof that no evidence could ever support a related rule.

---

## 4. Core conceptual distinctions established or sharpened

### 4.1 Market-derived and macroeconomic Components are *both* ETF-independent upstream

An important late correction concerned the argument that macro data are special because they do not depend on ETF Exposure Profiles.

Under `update_design` system architecture §3.1.1, **all** authoritative Component definitions, Values, States, and parameters must be independent of downstream ETF identities and desired evaluation outcomes. A Treasury 10Y Yield Trend and a core-PCE Inflation Trend are both upstream, ETF-independent Components.

The differences are their economic subject matter and observation sources—not consumer independence. The same macro condition can have different economic consequences for nominal versus inflation-linked bonds or hedged versus unhedged exposures **through the downstream evaluation mapping**.

Thus:

- ETF independence **does not** justify a separate Macro Adjustment stage.
- ETF independence **does not** make a new Constituent impossible.
- New Constituents require new economic **questions**, not merely new data categories.

### 4.2 Macro data contain information not explicitly represented by Core; this is not enough

Core compresses market observations into limited features and discrete States. Inflation and policy observations may supply information not preserved by that compression. But there are at least three possible interpretations:

1. The data explain an already observed Treasury-yield movement.
2. The data identify a separate economic consideration properly assigned to another Constituent.
3. The data identify a *new* consideration that justifies qualifying this Constituent's result.

Only the third would provide a potential justification for Macro Adjustment—and even then, it would not automatically justify a **separate stage** rather than an integrated Core mapping.

There is a further diagnostic trap: an inflation feature may improve a prediction relative to a **three-State** rate signal simply because the rate classification discarded magnitude/path information. Such improvement does not automatically establish independent economic relevance for inflation or macro-stage ownership.

### 4.3 Macro explanation is not necessarily macro *evaluation*

Nominal Treasury yields reflect expectations of short-rate paths and term premiums; those can be shaped by policy, inflation, growth, supply/demand, and risk preferences. A statement like “yields are falling despite sticky inflation” has more than one interpretation: markets may anticipate disinflation or recession, or term premiums may be changing.

Therefore **disagreement between realized macro conditions and observed yields is not intrinsically a contradiction**. A macro description can be valuable as interpretive context without authorizing a score adjustment.

### 4.4 Policy Direction versus Policy Stance

- **Policy Direction:** recent rate increases, decreases, or no change.
- **Policy Stance:** restraint/accommodation relative to inflation and the unobservable neutral rate.

Holding rates unchanged can be restrictive; cutting rates can leave policy restrictive; tightening can remain accommodative. Neither the convenience of observed rate changes nor the label “macro” determines which concept belongs in an ETF evaluation.

An additional issue: expected future Fed policy can affect Treasury yields before any realized policy change, making simple actual-change classifications poor proxies for forward monetary conditions.

### 4.5 Backward-looking Core built from forward-looking prices

Bondview Duration Core computes historical yield changes. **It is not itself a forecast.** But the underlying yields are prices formed partly from investors' forward-looking expectations. Both statements can be true.

This weakens any naive story that newer macro releases necessarily “correct” backward-looking market information. The macro series may be economically informative, stale relative to bond repricing, or both.

### 4.6 Underlying formulas do not naturally imply a post-Core macro correction

For a conventional fixed-rate bond:

\[
P=\sum_t\frac{CF_t}{(1+y)^t},\qquad
D_{mod}=-\frac{1}{P}\frac{\partial P}{\partial y},\qquad
\frac{\Delta P}{P}\approx-D_{mod}\Delta y.
\]

Inflation and Fed policy do not enter these basic nominal fixed-cash-flow equations as separate post-valuation terms; they affect the market's discount rates and expectations. A heuristic term-structure decomposition is:

\[
y_t^{(n)}\approx \operatorname{Average}_k E_t[r_{t+k}] + TP_t^{(n)}.
\]

For TIPS, inflation linkage instead changes contractual real/nominal cash-flow mechanics. For corporate bonds, growth and balance-sheet conditions influence default risk and required compensation. These mechanisms may justify **specific exposures or Constituents**. They do not, by themselves, justify an additional correction *after* their respective Core evaluations.

The lesson is not that a macro-driven mechanism is irrelevant. It is that its **economic location** must be established independently of its data source.

---

## 5. The four Constituents examined on their own terms

### 5.1 Duration

**Question:** How favorable or unfavorable are current rates-direction conditions for the ETF's interest-rate sensitivity?

- Accepted Core already relates yield direction to exposure-specific sensitivity.
- Inflation and current policy action may explain yields but do not imply that favorable rate-direction evidence must be weakened.
- A “macro conflict” might indicate a genuinely fragile trend, or instead a bond market correctly anticipating changes not yet in published data.
- Absolute rates compensation belongs more naturally to Rates Valuation.

**Assessment:** No validated economic role for Duration Macro Adjustment; favor keeping the accepted Core rule unchanged while the architectural question is reviewed.

### 5.2 Curve

**Question:** Is maturity/curve exposure suitable under term-structure conditions?

Policy expectations and term premiums influence the shape of the curve; these can be part of the **substance of Curve Evaluation**. If they materially distinguish curve exposures, the case for treating them as Curve Core inputs appears stronger than the case for an after-Core macro correction.

**Assessment:** No distinct Macro Adjustment responsibility identified.

### 5.3 Credit

**Question:** Is the ETF's credit-risk exposure suitable under current credit conditions?

Corporate leverage, coverage ratios, recession risks, expected losses, and credit-risk premiums can add fundamentally different evidence from raw credit spreads. This is the **strongest candidate for useful non-price information** within an existing Constituent.

But default-risk fundamentals are *central* to credit assessment; they do not obviously belong in a secondary macro stage. Combining spreads and fundamental credit conditions within Credit Core may be economically cleaner.

**Assessment:** The case for extra information is strong; the case for a separate Macro Adjustment stage is still unproven.

### 5.4 Rates Valuation

**Question:** Is compensation for accepting the ETF's rates exposure attractive enough?

Nominal yield, real yield, inflation compensation, term premiums, and carry are directly relevant to valuation. Calling inflation an after-Core macro correction risks treating a fundamental valuation input as secondary.

**Assessment:** Macro-sensitive measures plausibly belong in the Rates Valuation economic model itself. Separate adjustment not established.

**Cross-cutting conclusion:** A relevant macro variable does not establish a new economic question, much less a new processing stage. The four Constituents remain intentionally nonexhaustive individually, but the missing considerations should first be assigned according to their economic ownership.

---

## 6. A reversed search: missing economic questions first, data second

When asked to find *new* Constituents without beginning from familiar macro indicators, the discussion identified these candidate gaps:

| Candidate question | Why it might be distinct | Principal boundary problem | Status |
|---|---|---|---|
| **Currency Exposure:** What FX risk or hedge economics does an ETF create for a specified base-currency investor? | Otherwise similar Treasury ETFs may be hedged versus unhedged | Investor-specific benchmark/portfolio choice; hedging *quality* belongs to Instrument Quality | Strongest apparent gap for KR-listed US-bond ETFs; no model accepted |
| **Inflation Protection:** Does the contractual exposure protect real purchasing power? | Nominal vs inflation-indexed cash flows differ | Attractive *pricing* of inflation protection belongs largely to Rates Valuation; depends on TIPS coverage | Conditional candidate |
| **Convexity / Optionality:** Does nonlinear yield sensitivity or an embedded option materially distinguish ETF exposures? | Duration alone is first-order; MBS/callable instruments may add structural optionality | Could instead expand Duration Evaluation; materiality depends on universe | Conditional candidate |
| **Portfolio Protection:** Does this exposure hedge an investor's other assets or liabilities under stress? | Depends on diversification and portfolio role, not just bond-level evaluation | Probably downstream portfolio/final-choice logic, not intrinsic ETF Exposure Evaluation | Likely out of Constituent scope |

These were **illustrative conceptual candidates**, not accepted additions. The point is methodological: an independent question, distinguishable ETF exposures, and nonredundant ownership must precede observation selection.

A separate *Macro Constituent* was also questioned. An ETF-independent “inflation rising / policy tightening = macro score -2” does not evaluate an ETF Exposure Profile. Yet independence of the upstream inflation Component does **not** prevent exposure-specific effects: a macro condition can have distinct contractual implications for nominal bonds versus TIPS. Such an evaluation would need a specific exposure question, not a generic macro label.

---

## 7. Proposed historical testing: what it can and cannot settle

Early suggestions included testing a candidate Duration macro conflict rule with historical core-PCE inflation and Fed policy rates:

1. **Activation/coverage:** Does the proposed macro condition arise frequently enough to matter? Count economic episodes, not just highly autocorrelated daily rows.
2. **Conditional contrasts:** Within similar Core States and underlying continuous rate Values, do macro conditions discriminate economically meaningful outcomes or risks?
3. **Incremental information:** Is a macro rule different from information already preserved by rate Components, including continuous values lost by State bucketing?
4. **Counterexamples:** Identify episodes where policy and inflation conditions are inconsistent with the proposed directional interpretation; inspect regime timing and alternative economic mechanisms.
5. **Real-time validity:** Use information actually published at the decision date, including release lags and appropriate vintages, rather than ex post revised observations.

The candidate inflation measure was **three-month annualized core PCE acceleration**, constructed from a monthly PCE price index, not a raw FRED three-month annualized observation. Its responsiveness was plausible but its horizon was *not* justified from the intended economic responsibility. Core PCE was selected as a tentative measure of underlying inflation pressure, not because food and energy or headline inflation never matter. Policy Direction (observed Fed target changes) was easier to calculate than Policy Stance but had distinct economic limitations. **Neither Component definition nor the original macro conflict cap was accepted.**

### A crucial objection to “Test B: are conflicting Core signals less reliable?”

Testing next-month or next-quarter Treasury yield changes may be a legitimate **diagnostic consequence** of a specified economic hypothesis, even though Bondview is not a yield-forecasting system. However, selecting macro rules because they improve future rate outcomes would silently turn the design process toward predictive optimization.

More fundamentally, no backtest alone can determine **which economic responsibility owns an effect**. A favorable historical contrast could arise from a genuine new mechanism, market data lost in coarse State classification, overlapping valuation signals, data revisions, or selection bias.

The proposed sequence was therefore criticized as backward:

```text
Weak sequence: choose macro indicators -> propose cap -> search history for benefit

Stronger sequence: define unanswered economic question -> specify mechanism
                  -> derive conditional implication -> test counterexamples
                  -> only then consider accepting a mapping
```

Historical tests remain useful to **refute** a specifically articulated mechanism, assess coverage, and reveal violations. They cannot manufacture its conceptual legitimacy.

---

## 8. What did we actually learn, and what was the design-process failure?

Three explanations for the long evolution were considered:

1. **Genuine conceptual difficulty.** Inflation, Fed policy, rates, term premiums, credit losses, and risk compensation interact, and financial prices already anticipate some of their effects. Decomposing distinct economic assessments without double counting is hard.
2. **Premature attention to architecture.** We repeatedly improved the shape of the macro stage—peer versus supporting, pre-/post-Core, constraints versus scores, traceability—before proving a unique economic responsibility. This was identified as the **largest process mistake**.
3. **Misallocated responsibilities.** Some apparent macro gaps were actually valuation, curve, credit fundamental, currency, or portfolio questions. Relocating them can eliminate the need for a separate stage without denying the importance of macro information.

The persistent user objection—macro drivers are already partly incorporated in market yields and spreads—was acknowledged in early September but was not tested rigorously enough as a **challenge to the existence** of Macro Adjustment. The October reasoning came substantially closer to accepting that objection. The shift was not caused by historical data falsifying a particular accepted Macro rule: **there was no such accepted rule**. It resulted primarily from reassessing the logic of architectural ownership.

A useful retrospective distinction:

- **Architectural consistency:** A post-Core, exposure-specific, traceable Macro Adjustment can be specified without violating Component authority.
- **Economic necessity:** We have not yet found a distinct judgment that *requires* that stage.

The former was achieved; the latter remains unestablished. Neither implies that all macro data are redundant.

---

## 9. Questions deliberately left open

This document does **not** settle the following:

1. **Stage necessity:** Is there a defensible economic mechanism for which a sequential *post-Core* qualification is superior to a single Constituent mapping that consumes all justified inputs?
2. **Scope:** If the answer is no for the four current Constituents, should `Macro Adjustment` be removed from the predefined architecture, retained only as optional terminology, or generalized to a different kind of evaluator-internal rule? What is gained and lost in traceability and contracts?
3. **Constituent boundaries:** How should Curve, Credit, and Rates Valuation each claim economic mechanisms, particularly those involving policy expectations, default fundamentals, and inflation-related compensation?
4. **Universe:** Does the current KR-listed US-bond ETF universe materially require currency, inflation-linked, or optionality evaluation? Should a model that depends on an investor's base currency sit within Exposure Evaluation or downstream choice?
5. **Market information:** How much additional *economic* information can macro releases supply beyond both the discrete Core States and their underlying continuous market Components?
6. **Historical evidence:** What observations would count as genuine counterexamples to a newly proposed mechanism, rather than post-hoc labels or backtested fit?
7. **Terminology and revision discipline:** Which current `update_design` passages assume a distinct Macro result or two-stage Constituent evaluation, and which would need careful coordinated revision **if** removal were accepted? A review must not silently rewrite the accepted Duration Rule Table or upstream Component authority.

### Proposed decision standard for a future review

Before adopting **any** separate Macro Adjustment—or new Constituent—state in writing:

- The exact **economic question** not adequately answered by existing responsibilities.
- The **ETF exposure characteristic** whose treatment differs under that question.
- The **mechanism** relating authoritative inputs to the assessment.
- Why the effect does not belong in an existing Constituent's Core, another Constituent, Positioning Overlay, Instrument Quality, or downstream portfolio choice.
- The consequences and **counterexamples** that would make the proposed interpretation untenable.

For a specifically separate *post-Core* stage, an additional requirement applies: **explain why sequencing is economically meaningful, rather than merely convenient for code organization.**

---

## 10. Provisional review summary — not a decision record

The evidence and reasoning assembled so far support these *provisional* observations:

- Market and macroeconomic observations can be economically different, but **both kinds of Components are upstream and ETF-independent**; this difference does not dictate Core-versus-Macro ownership.
- Inflation, monetary policy, growth, and default fundamentals may matter greatly to bonds while supplying **no independent justification** for a generic macro score or a predefined post-Core adjustment.
- The accepted Duration Core evaluates a narrow rates-direction question; its lack of comprehensive bond attractiveness is intentional. It should not be “completed” by arbitrarily inserting macro information.
- For Curve, Credit, and Rates Valuation, plausible macro-relevant mechanisms generally appear to fit **within the existing economic questions** rather than after their Core results.
- New exposure dimensions may be worth considering, but only after demonstrating an unanswered question and a relevant universe of distinguishable ETF Profiles.
- Removing Macro Adjustment from the *predefined* hierarchy is a coherent candidate architectural revision. **It has not yet been formally accepted**, and no current design document is changed by this retrospective.

**Review prompt:** If we had designed Bondview-v2 from scratch knowing only the four current Constituents and their economic questions, would we independently invent a post-Core `Macro Adjustment` stage? If so, what exact counterexample would force us to do so? If not, what would be lost by allowing each Constituent to consume all economically justified market and macro Components directly?

---

## Reference points within the current v2 design

- [`docs/bondview_system_architecture.md` — §3.1.1 Component authority; §4.2 Constituent/Core/Macro hierarchy; §6.3 reusable mechanics; §6.4 dependency direction](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_system_architecture.md)
- [`docs/bondview_exposure_evaluation_design.md` — §2 common principles; §3 Duration; §§4–6 Curve/Credit/Rates Valuation; §7 Evaluation Combination](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_exposure_evaluation_design.md)
- [`docs/bondview_vocabulary.md` — Component, Constituent, Core Evaluation, Macro Adjustment and Result definitions](https://github.com/lbk209/bondview-v2/blob/update_design/docs/bondview_vocabulary.md)

*Historical discussions are summarized as reasoning and design alternatives, not represented as accepted branch-specific implementation decisions. Any eventual architecture or exposure-evaluation design change requires a separate explicit review.*
