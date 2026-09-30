# Bondview Duration Design Validation — Codex Work Plan

## 1. Purpose

This document defines a temporary Codex work plan for validating the current Bondview **Duration Evaluation** design and resolving the remaining lower-level Duration decisions.

This is:

- **not** a system-architecture review;
- **not** a replacement for `bondview_system_architecture.md` or `bondview_vocabulary.md`;
- **not** a production implementation contract;
- **not** a request for Codex to invent a new Duration model.

The authoritative architecture and vocabulary are already established.

The purpose of this work is to:

1. validate the current Duration design against historical rate environments;
2. establish a simple but economically defensible Duration Exposure taxonomy from the actual ETF universe;
3. assign a representative Treasury tenor to each exposure from the economic center of that exposure;
4. validate whether the chosen Trend and Recent Move calculations actually express their intended Component semantics;
5. treat **Trend-horizon robustness** as a major review item;
6. review unresolved mixed Trend / Recent Move Rule Cases;
7. validate the ordinal Core Duration mapping across materially different Duration Exposures;
8. test Macro Adjustment as a modifier of the already exposure-specific Core result;
9. identify contradictions or unresolved economic choices that still require human review.

Historical data are diagnostic evidence, not optimization targets.

---

# 2. Reference Basis

Use the `update_duration` branch of:

```text
lbk209/bondview-v2
```

as the repository basis.

Authoritative references:

- `docs/bondview_system_architecture.md`
- `docs/bondview_vocabulary.md`

The previous:

```text
docs/bondview_duration_core_macro_codex_review_plan_draft.md
```

is superseded by this plan.

Older Duration notebooks, previous Codex outputs, and retired review documents may be inspected only where they contain useful calculations, historical examples, or diagnostics that remain compatible with the current design.

Do not preserve old model logic merely because code or output already exists.

In particular, do not reintroduce:

- ETF-independent Duration preference as an authoritative intermediate result;
- distance-to-preferred-duration scoring;
- cardinal interpretation of `-3 ... +3`;
- Macro Adjustment applied to an ETF-independent directional score before exposure;
- Stance terminology as part of the current Duration Evaluation path;
- a universal 10Y rates input merely because it was used by an earlier prototype;
- a fixed four-bucket Duration taxonomy merely because it appeared in earlier review work.

---

# 3. Fixed Architectural Premises

Codex should treat the following as fixed unless a direct contradiction with the authoritative architecture is found.

## 3.1 Exposure enters Core Evaluation

Duration follows:

```text
Duration-relevant Components
+
ETF Duration Exposure
        ↓
Core Duration Evaluation
        ↓
Core Duration Evaluation Result
```

The Core result is already exposure-specific.

Do not calculate a complete ETF-independent Duration judgment and attach ETF exposure afterward.

## 3.2 Macro Adjustment follows Core Evaluation

The authoritative order is:

```text
Core Duration Evaluation Result
+
relevant Macroeconomic Components
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

Do not apply Macro Adjustment to a separate market-level Duration preference and then reapply exposure.

## 3.3 Constituent Evaluations are distinguishable, not orthogonal

Duration, Curve, Credit, and Rates Valuation answer distinguishable economic questions, but they do not need:

- disjoint Components;
- disjoint source observations;
- statistically orthogonal factors;
- completely non-overlapping mechanisms.

Overlapping inputs are acceptable where the evaluations answer different economic questions.

Materially duplicative economic effects should be avoided, especially when Constituent Evaluation Results are later combined.

This work must not impose artificial Duration / Curve separation merely to obtain orthogonality.

## 3.4 Core score is ordinal

Use the compact ordered scale:

```text
+3  strongly favorable
+2  favorable
+1  mildly favorable
 0  neutral
-1  mildly unfavorable
-2  unfavorable
-3  strongly unfavorable
```

The numbers are **ordinal category codes**, not cardinal economic quantities.

Therefore:

```text
+2 > +1
```

is meaningful, while:

```text
+2 = twice as favorable as +1
```

is not.

Do not infer utility ratios, equal spacing, or arithmetic economic magnitude from the codes.

---

# 4. Current Duration Economic Interpretation

Core Duration Evaluation asks:

> **How favorable or unfavorable are the current Duration-relevant rates conditions for this ETF's interest-rate sensitivity?**

The result is specific to the Duration constituent.

It is not:

- an overall ETF recommendation;
- a comparison against cash;
- a forecast of future Treasury yields;
- a relative rank only among Duration Exposure categories.

## 4.1 Trend and Recent Move roles

The intended roles are:

```text
Yield Trend
→ broader / established rates condition

Recent Yield Move
→ shorter-horizon behavior that confirms, pauses,
   or challenges that broader condition
```

`Recent Yield Move` is not intended to predict a future Trend State.

For example:

```text
Trend = Rising
Recent Move = Falling
```

means:

> the established rising-yield condition is currently being challenged by observed shorter-horizon behavior.

It does not mean:

> Bondview predicts that the broader Trend will become Falling.

If the counter-move persists, the Trend State may later change when the Trend calculation itself changes.

## 4.2 Design order

The economic roles above come first.

The correct design sequence is:

```text
economic role
        ↓
required time distinction
        ↓
horizon / calculation
        ↓
State Classification
```

not:

```text
choose convenient horizons
        ↓
infer Component meaning afterward
```

Codex should therefore validate whether candidate calculations express the intended Component semantics rather than search for horizons that maximize forecast performance.

---

# 5. Duration Exposure Taxonomy

The exposure taxonomy should be derived from the **actual ETF universe and the economic center of each ETF's designed exposure**, not from a pre-imposed requirement to have a particular number of buckets.

## 5.1 Initial working taxonomy

Start with:

```text
Short
Intermediate
Long
```

This is the preferred initial resolution because it is simple and corresponds naturally to common Treasury ETF exposure families.

Do not create a separate `Very Long` category unless the ETF universe shows that a material group of products has an economically distinct Duration Exposure that cannot be represented adequately by `Long`.

Likewise, do not assume that `Short` must remain one bucket if the actual universe contains multiple large, economically distinct short-end clusters that matter to Duration Evaluation.

## 5.2 Universe-driven assignment rule

For every ETF in the intended universe, inspect at least:

```text
declared benchmark / reference exposure
maturity segment
effective duration, if available
other duration-relevant benchmark characteristics
```

Assign the ETF to the existing exposure category whose economic meaning best matches the ETF's exposure center.

The intended process is:

```text
ETF universe
        ↓
benchmark / exposure characteristics
        ↓
economic center of each ETF exposure
        ↓
assign to existing Duration Exposure category
        ↓
check whether any material cluster is poorly represented
        ↓
expand exposure taxonomy only if justified
```

Therefore:

> **The taxonomy may expand when the ETF universe contains a sufficiently numerous or economically material exposure cluster that the existing categories cannot represent cleanly.**

Expansion should be justified by decision relevance, not by the mere existence of a product with a slightly different stated maturity.

## 5.3 Do not force one-to-one bucket / tenor correspondence

The number of exposure categories and the number of representative Treasury tenors do not have to be identical.

An exposure category exists because Bondview needs to distinguish that economic exposure.

A representative tenor exists because Bondview needs a market-rate condition that reasonably represents the economic center of that exposure.

Do not invent an extra Treasury tenor merely to match the number of buckets.

---

# 6. Representative Treasury Tenor

The design principle is:

> **The representative tenor should follow the economic center of the Duration Exposure.**

The representative tenor is not chosen because it is prominent in financial news and is not optimized by forward ETF return.

## 6.1 Initial working assignments

Use the ETF-universe review to establish the exact assignments.

A reasonable starting structure is:

```text
Short
→ short-end Treasury tenor appropriate to the actual Short exposure cluster

Intermediate
→ approximately 10Y Treasury

Long
→ approximately 30Y Treasury
```

For `Short`, do not assume 2Y automatically.

Examples:

```text
0–1Y exposure
→ 1Y is a more natural initial representative tenor than 2Y

1–3Y exposure
→ 2Y is a natural representative tenor
```

If the actual Short universe includes both and Bondview needs to distinguish them economically, consider expanding the Short taxonomy rather than forcing one tenor to represent materially different exposures.

If the difference is not material to Bondview decisions, retain one Short category and choose the tenor that best represents the dominant / intended exposure center.

## 6.2 What Codex should validate

Codex should not decide representative tenor by return optimization.

It should:

1. inventory the intended ETF universe;
2. show benchmark / maturity / duration characteristics;
3. assign ETFs to the current exposure taxonomy;
4. document the economic center of each resulting cluster;
5. check that the proposed representative tenor is consistent with that center;
6. flag any ETF or cluster that is poorly represented;
7. recommend taxonomy expansion only when the mismatch is economically material.

The main question is:

> Does the representative tenor plausibly represent the rate segment that drives the intended Duration Exposure category?

---

# 7. Signal Horizon Starting Point

Bondview is intended to ignore day-to-day noise and focus on medium-horizon bond-market changes.

The practical use assumption is that an ETF position is normally held for at least roughly one month.

That holding-period assumption does **not** mechanically determine the Component horizon, but it provides useful scale.

Use the following starting point:

```text
Recent Yield Move
→ approximately 1 month

Yield Trend
→ approximately 3 months
```

Treat:

```text
Trend ≈ 6 months
```

as an important robustness alternative.

Do not begin from an annual Trend unless the 3–6 month definitions prove unable to represent the intended broader market condition.

The reason is model role, not a claim that institutional bond investors operate only on these horizons.

---

# 8. Trend-Horizon Robustness — Major Validation Task

**Trend-horizon robustness is a first-class review item.**

The goal is not to find the horizon with the best subsequent return.

The goal is to determine whether the economic meaning of `Yield Trend` is robust to reasonable horizon variation.

At minimum compare:

```text
Trend ≈ 3 months
vs.
Trend ≈ 6 months
```

while holding the Recent Move definition approximately fixed around one month.

## 8.1 Semantic robustness questions

For each representative tenor, ask:

1. Do 3m and 6m Trend usually describe the same broad rates regime?
2. When they differ, are the disagreements economically understandable?
3. Does 3m become too responsive and start duplicating Recent Move?
4. Does 6m become too stale for Bondview's intended medium-horizon decisions?
5. Does either horizon produce excessive state-flipping?
6. Are important historical regimes classified implausibly under either horizon?
7. Does the interpretation of mixed Rule Cases materially depend on Trend horizon?

## 8.2 Required robustness diagnostics

For both Trend horizons, report:

- State frequency;
- average and median State persistence;
- transition frequency;
- percentage agreement between 3m and 6m Trend States;
- disagreement-window frequency and duration;
- historical examples of meaningful disagreement;
- interaction with the 1m Recent Move State;
- number of Core Duration results that change because of the Trend-horizon choice.

The review should conclude whether:

```text
3m Trend is preferable
6m Trend is preferable
or
both are semantically acceptable but one is chosen for simplicity / responsiveness
```

The conclusion must be based on Component meaning and historical plausibility, not forecast fit.

---

# 9. Recent Move Validation

Recent Move should be materially shorter-horizon than Trend and responsive enough to:

```text
confirm
pause
challenge
```

the established Trend.

The initial working horizon is approximately one month.

Report:

- State frequencies;
- average persistence;
- agreement rate with Trend;
- disagreement rate with Trend;
- duration of disagreement windows;
- representative `Falling × Rising` windows;
- representative `Rising × Falling` windows.

## 9.1 Disagreement-window diagnostics

Use historical windows where Trend and Recent Move disagree to verify role separation.

For each window, display:

```text
date
yield level
Trend Value
Trend State
Recent Move Value
Recent Move State
```

The purpose is **not** to test whether Recent Move predicts a future Trend reversal.

The purpose is to test whether:

```text
Trend
→ remains the slower / broader condition

Recent Move
→ can meaningfully disagree with Trend over shorter periods
```

Both outcomes are valid after a disagreement window:

```text
counter-move disappears
→ Trend remains intact
```

or:

```text
counter-move persists
→ Trend eventually changes through its own calculation
```

No forecast success criterion is implied.

---

# 10. Core Duration Rule Representation

With the initial three exposure categories, the abstract Rule Case space is:

```text
Trend State
×
Recent Move State
×
Duration Exposure
→ Core Duration Evaluation Result
```

where:

```text
Trend State       ∈ {Falling, Stable, Rising}
Recent Move State ∈ {Falling, Stable, Rising}
Duration Exposure ∈ {Short, Intermediate, Long}
```

This gives a conceptual `9 × 3` representation.

Important:

> The exposure columns do not imply that all three exposure categories use the same Treasury Rule Case on a historical date.

Each exposure uses the States of its own representative tenor.

---

# 11. Starting Core Mapping for Review

Use the following as the current **starting ordinal mapping**, not as a formula-derived truth.

| Trend | Recent Move | Short | Intermediate | Long | Status |
|---|---|---:|---:|---:|---|
| Falling | Falling | +1 | +2 | +3 | sign/order strong; exact spacing reviewable |
| Falling | Stable | +1 | +1 | +2 | sign/order strong; exact spacing reviewable |
| Falling | Rising | 0 / +1 | +1 | +1 / +2 | unresolved mixed case |
| Stable | Falling | 0 / +1 | +1 | +1 / +2 | unresolved mixed case |
| Stable | Stable | 0 | 0 | 0 | neutral baseline |
| Stable | Rising | 0 / -1 | -1 | -1 / -2 | unresolved mixed case |
| Rising | Falling | 0 / -1 | -1 | -1 / -2 | unresolved mixed case |
| Rising | Stable | -1 | -1 | -2 | sign/order strong; exact spacing reviewable |
| Rising | Rising | -1 | -2 | -3 | sign/order strong; exact spacing reviewable |

Do not replace the ranges with invented values.

Codex should help determine whether ambiguous cells can be narrowed using:

- the established Trend / Recent Move roles;
- exposure sensitivity;
- historical disagreement-window behavior;
- row and column consistency;
- comparison across materially different rate regimes.

Human review remains required for economic mappings that are not justified by the fixed principles or clear evidence.

---

# 12. Core Mapping Constraints Already Established

The following should be treated as design constraints rather than rediscovered through optimization.

## 12.1 Confirmation / challenge ordering

For a fixed positive-duration exposure:

```text
Falling × Falling
>
Falling × Stable
>
Falling × Rising
```

where `>` means more favorable for that exposure.

Likewise:

```text
Rising × Falling
>
Rising × Stable
>
Rising × Rising
```

## 12.2 Exposure sensitivity

For otherwise comparable relevant-tenor conditions:

```text
falling-yield conditions
→ greater Duration Exposure should normally receive a larger favorable effect

rising-yield conditions
→ greater Duration Exposure should normally receive a larger unfavorable effect
```

A Short exposure may therefore be least unfavorable in a strongly rising-rate environment without becoming positively attractive.

## 12.3 Neutral condition

The starting interpretation of:

```text
Stable × Stable
```

is:

```text
0 for all Duration Exposures
```

because the Duration constituent has no directional rates reason to favor or penalize positive-duration exposure under this Rule Case.

Do not reintroduce a hidden "middle duration is best" assumption.

## 12.4 Mixed cases are not automatically equivalent

Do not assume:

```text
Falling × Rising
=
Stable × Falling
```

or:

```text
Stable × Rising
=
Rising × Falling
```

merely because an older rule table compressed each pair to the same directional score.

Their economic meanings differ.

A coarse ordinal scale may still classify some exposure-specific outcomes identically.

Codex should distinguish:

```text
underlying economic ordering
```

from:

```text
final ordinal category
```

---

# 13. Historical Validation Design

Historical work should combine:

1. **regime snapshots**;
2. **Trend / Recent-Move disagreement windows**;
3. **full-sample diagnostics**.

No historical case is a training label.

## 13.1 Regime snapshots

Select a compact set of materially different U.S. Treasury environments, including examples of:

- sustained falling-yield conditions;
- sustained rising-yield conditions;
- abrupt risk-off / easing shock;
- inflation / tightening transition;
- restrictive high-yield environment;
- easing or normalization transition.

Use exact `as_of` dates only after inspecting the underlying rate paths so the dates actually represent the intended environments.

For each selected `as_of`, report by exposure:

```text
exposure_class
representative_tenor
yield_level
trend_horizon
trend_value
trend_state
recent_move_horizon
recent_move_value
recent_move_state
core_duration_result
```

If Macro Adjustment is included in that run, also report:

```text
inflation_state
policy_state
macro_rule_case
macro_action
duration_evaluation_result
```

## 13.2 Cross-sectional comparison

At the same `as_of`, compare:

```text
Short
Intermediate
Long
```

using each exposure's own representative-tenor States.

Ask:

- Are differences economically interpretable?
- Does any exposure receive a sign obviously inconsistent with its relevant rate segment?
- Does the exposure taxonomy appear too coarse for the ETF universe?
- Does the representative-tenor assignment produce obvious mismatches?

## 13.3 Longitudinal comparison

For each exposure separately, compare results across materially different historical environments.

Ask:

- Does the same exposure move sensibly from favorable to unfavorable conditions?
- Are transitions excessively noisy?
- Do Trend and Recent Move play their intended roles?
- Do mixed Rule Cases behave plausibly?
- Are conclusions stable enough across 3m vs 6m Trend to support one default?

---

# 14. Mixed-Case Investigation

The highest-priority unresolved Core cases are:

```text
Falling × Rising
Stable  × Falling

Stable  × Rising
Rising  × Falling
```

For each representative tenor, identify multiple historical examples of each mixed Rule Case where available.

For each example, display:

```text
preceding states
current Rule Case
yield path around the window
3m Trend State
6m Trend State
Recent Move State
```

The purpose is not to ask:

> Which Rule Case predicted the best future return?

The purpose is to ask:

> Does the proposed ordinal interpretation fit what the Components mean at that time, and is that interpretation robust to a reasonable Trend-horizon choice?

Codex should summarize whether the evidence supports:

- the same ordinal category for paired mixed cases;
- a systematic ordering between them;
- exposure-dependent differences in classification;
- continued ambiguity requiring human judgment.

---

# 15. Macro Adjustment Validation

Macro Adjustment operates on the already exposure-specific Core Duration Evaluation Result.

The input form is:

```text
Core Duration Evaluation Result
+
Inflation Trend
+
Policy Direction
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

## 15.1 Existing macro rules are candidate fixtures only

If an older Inflation Trend × Policy Direction table is available, Codex may reproduce it as a **candidate fixture**.

Do not assume old cap rules remain valid under the current exposure-specific Core semantics.

Reuse them only where their economic intent still makes sense.

## 15.2 Ordinal action semantics

The `-3 ... +3` scale is ordinal, but ordered caps remain meaningful.

Examples:

```text
cap positive at +2
cap positive at +1
cap negative at -1
cap negative at -2
pass-through
```

A cap uses only ordering.

For example:

```text
Core = +3
cap positive at +1
Final = +1
```

means that the macro condition prevents the Duration result from remaining above the `+1` category.

It does **not** imply that two equal cardinal units were subtracted.

Avoid operations that assume metric spacing, such as:

```text
multiply score by 0.5
subtract 1.5
average ordinal scores arithmetically without justification
```

If a `weaken one category` action is used, define it explicitly as an ordered category transition rather than as an economic cardinal subtraction.

## 15.3 Macro diagnostics

For each candidate Macro Adjustment mapping, report:

- frequency of each action;
- Core-to-final transition counts;
- cases where Macro changes sign;
- cases where Macro compresses strong Core results;
- cases where different exposures converge to the same final result;
- historical examples of each non-pass-through action;
- potential overlap with the realized rate signal already captured in Core.

Macro rules should not be optimized for historical ETF returns.

---

# 16. Macro Double-Counting Review

The main risk is not repeated use of the same variable name.

The risk is counting substantially the same economic mechanism twice.

Example:

```text
Policy tightening
        ↓
Treasury yields rise
        ↓
Core Duration becomes unfavorable
```

followed by:

```text
Policy tightening
        ↓
Macro Adjustment imposes another strong penalty
```

may partly double-count policy transmission.

This does not imply that Policy Direction or Inflation Trend must be removed.

Realized Treasury yields also reflect:

- inflation expectations;
- term premium;
- Treasury supply;
- growth expectations;
- risk demand;
- other market forces.

Codex should identify candidate Macro cases where the adjustment appears:

```text
clearly incremental
possibly overlapping
apparently duplicative
```

but should not redesign the macro model automatically.

---

# 17. Duration / Curve Boundary Check

This work should confirm only one limited issue:

> Using exposure-relevant Treasury tenors inside Duration Evaluation does not by itself make Curve Evaluation redundant.

Duration asks:

> **How favorable are the relevant rates conditions for this ETF's interest-rate sensitivity?**

Curve separately evaluates the ETF's maturity / curve exposure under relative term-structure conditions.

Codex should not design Curve Evaluation in this work.

Only flag a concern if the proposed Duration logic clearly begins to encode an explicitly relative curve judgment rather than exposure-specific rate sensitivity.

---

# 18. Full-Sample Diagnostics

At minimum produce:

## 18.1 Universe / exposure diagnostics

- ETF universe inventory;
- benchmark / reference exposure;
- effective duration where available;
- assigned Duration Exposure category;
- representative tenor;
- ETFs that fit poorly into the current taxonomy;
- candidate additional exposure cluster, if any.

## 18.2 Component diagnostics

By representative tenor and Trend horizon:

- Trend State distribution;
- Recent Move State distribution;
- full 3 × 3 Rule Case frequency table;
- State persistence;
- Rule Case persistence;
- Trend / Recent Move disagreement frequency;
- 3m / 6m Trend State agreement rate.

## 18.3 Core-result diagnostics

By exposure:

- Core score distribution;
- transition matrix;
- average persistence;
- frequency of each mixed Rule Case;
- frequency of neutral;
- frequency of extreme `±3`;
- cross-exposure divergence at the same `as_of`;
- sensitivity of Core results to 3m vs 6m Trend.

## 18.4 Mapping diagnostics

Report:

- monotonicity violations relative to established constraints;
- cells that remain unresolved;
- historical examples that challenge the starting mapping;
- cells where different economic situations collapse into one ordinal category;
- cases where the same ordinal score remains defensible despite different underlying economic ordering.

## 18.5 Macro diagnostics

When Macro Adjustment is enabled:

- Core vs final distribution;
- action frequency;
- compression frequency;
- sign-change frequency;
- potential double-counting examples.

These diagnostics are review aids, not objectives to optimize.

---

# 19. Explicit Non-Goals

Codex must not:

- redesign the Bondview system architecture;
- treat retired Stance structures as authoritative;
- optimize exposure buckets by forward ETF returns;
- optimize representative tenors by forward ETF returns;
- optimize Trend / Recent Move horizons by predictive performance;
- fit the Core rule table to historical winners;
- infer cardinal utility from ordinal scores;
- reintroduce the old distance-to-preferred-duration formula;
- reintroduce an ETF-independent Duration preference as the authoritative Core result;
- apply Macro Adjustment before ETF exposure enters Core Evaluation;
- force Duration and Curve to use disjoint inputs;
- design Curve Evaluation as part of this task;
- treat historical snapshots as labels that the model must reproduce;
- preserve `Short / Intermediate / Long` if the actual ETF universe demonstrates a materially important missing exposure cluster;
- expand the exposure taxonomy merely because minor product differences exist.

---

# 20. Codex Work Sequence

Execute in this order.

## Phase A — Inventory the ETF universe

1. Identify the intended Korea-listed U.S. Treasury ETF universe.
2. Record benchmark / reference exposure, maturity segment, and effective duration where available.
3. Assign each ETF to `Short`, `Intermediate`, or `Long`.
4. Flag economically material clusters that do not fit.
5. Recommend taxonomy expansion only if justified by the universe.

## Phase B — Set representative tenors

1. Determine the economic center of each exposure category.
2. Assign the representative Treasury tenor from that center.
3. For Short, distinguish whether the dominant exposure is closer to `0–1Y`, `1–3Y`, or another short-end segment.
4. Make the rationale explicit.
5. Do not optimize against forward returns.

## Phase C — Build tenor-aware Components

1. Calculate Recent Move at approximately 1 month.
2. Calculate Trend at approximately 3 months.
3. Also calculate a 6-month Trend robustness alternative.
4. Produce Component diagnostics.
5. Identify Trend / Recent-Move disagreement windows.

## Phase D — Trend-horizon robustness review

1. Compare 3m vs 6m Trend across each representative tenor.
2. Quantify State agreement and persistence.
3. Examine historically important disagreement windows.
4. Compare resulting Core Duration classifications.
5. Recommend a default Trend horizon based on semantic robustness, responsiveness, and interpretability.

## Phase E — Evaluate the starting `9 × 3` Core mapping

1. Apply the starting ordinal table.
2. Produce row / column consistency checks.
3. Inspect the four mixed Rule Cases in detail.
4. Leave unresolved cells explicitly unresolved where evidence is insufficient.

## Phase F — Historical regime review

1. Select representative historical regimes from actual data.
2. Produce cross-sectional exposure tables.
3. Produce longitudinal exposure tables.
4. Produce disagreement-window tables / plots.
5. Include 3m vs 6m Trend comparison where it materially affects interpretation.

## Phase G — Macro Adjustment review

1. Reproduce any reusable old macro mapping only as a candidate fixture.
2. Translate candidate actions into current ordinal Core semantics.
3. Apply Macro directly to the exposure-specific Core result.
4. Produce Core-to-final diagnostics.
5. Flag possible double counting.

## Phase H — Findings

For every reviewed question, classify the result as:

```text
Confirmed
Refine
Unresolved
Rejected
```

with a short economic explanation and supporting diagnostic evidence.

Do not convert an unresolved economic choice into implementation merely for completeness.

---

# 21. Required Deliverables

At minimum:

```text
1. duration_validation_summary.md
2. duration_etf_exposure_inventory.csv
3. duration_exposure_tenor_mapping.csv
4. duration_trend_horizon_robustness.csv
5. duration_component_diagnostics.csv
6. duration_core_rulecase_review.csv
7. duration_historical_regime_review.csv
8. duration_disagreement_window_review.csv
9. duration_macro_review.csv
```

Plots may be generated where useful, especially for:

- 3m vs 6m Trend comparisons;
- Trend / Recent Move disagreement windows;
- historical regime comparisons.

The summary should contain:

## A. Confirmed findings

Only conclusions supported by the fixed design plus the diagnostics.

## B. Recommended refinements

Changes economically justified by the review.

## C. Unresolved decisions

Questions still requiring human judgment.

## D. Rejected prior assumptions

Old logic found incompatible with the current design.

## E. Suggested model-contract updates

Only after validation findings are complete, identify which stable conclusions should move into a dedicated Duration design / model contract.

Codex should not update the authoritative architecture or vocabulary unless explicitly instructed separately.

---

# 22. Questions This Work Must Answer

The review should end with direct answers to these questions:

1. Does the initial `Short / Intermediate / Long` taxonomy adequately represent the intended ETF universe?
2. Does the ETF universe contain a materially distinct exposure cluster that justifies expanding that taxonomy?
3. What representative Treasury tenor best matches the economic center of each exposure category?
4. For Short exposure, is the universe economically centered closer to `0–1Y`, `1–3Y`, or another short-end segment?
5. Does approximately 1 month work as a meaningful Recent Move horizon?
6. Does approximately 3 months or 6 months better express the intended broader Yield Trend?
7. Are the semantics of Yield Trend robust to the 3m / 6m horizon choice?
8. Does Recent Move behave as a contemporaneous confirmation / challenge signal rather than an implicit reversal forecast?
9. Are the strong directional Core cases economically coherent across Short, Intermediate, and Long?
10. How should the four mixed Rule Cases be ordered and classified on the ordinal scale?
11. Is `Stable × Stable → 0` for all Duration Exposures consistent with the intended Duration meaning?
12. Can Macro Adjustment be expressed cleanly as an ordered-category modification of the exposure-specific Core result?
13. Which Macro cases appear incremental versus potentially duplicative of realized rate conditions?
14. Which current Duration choices are sufficiently validated to move into a stable lower-level model contract?
15. Which choices should remain explicitly unresolved?

---

# 23. Current Working Starting Point

The current working model to validate is:

```text
ETF universe
        ↓
benchmark / duration characteristics
        ↓
Duration Exposure taxonomy
        ↓
Short / Intermediate / Long
        ↓
representative Treasury tenor from exposure economic center

representative-tenor Yield Trend
+
representative-tenor Recent Yield Move
+
Duration Exposure
        ↓
Core Duration Evaluation
        ↓
ordinal Core Duration Evaluation Result

Core Duration Evaluation Result
+
Inflation Trend
+
Policy Direction
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

The initial signal timing is:

```text
Recent Move ≈ 1 month

Trend ≈ 3 months
with 6 months as a major semantic-robustness comparison
```

The main unresolved lower-level areas are:

```text
ETF-universe-based exposure taxonomy
representative tenor by exposure
default Trend horizon: approximately 3m vs 6m
mixed Rule Case scores
exact Macro Adjustment mapping
```

The work should validate these directly without reopening system architecture that is already settled.
