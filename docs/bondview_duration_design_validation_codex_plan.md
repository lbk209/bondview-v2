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

1. validate the current Duration design against historical rate environments and transition episodes;
2. test whether exposure-relevant Treasury tenors are a better representation than one universal 10Y input;
3. confirm that the intended `Trend` / `Recent Move` roles are actually produced by the chosen calculations and horizons;
4. review the unresolved mixed Trend / Recent Move Rule Cases;
5. validate the ordinal Core Duration mapping across materially different Duration Exposures;
6. test Macro Adjustment as a modifier of the already exposure-specific Core result;
7. identify contradictions or unresolved economic choices that still require human review.

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

Older Duration notebooks, prior Codex outputs, and retired review documents may be inspected only where they contain useful calculations, historical examples, or diagnostics that remain compatible with the current design.

Do not preserve old model logic merely because code or output already exists.

In particular, do not reintroduce:

- ETF-independent Duration preference as an authoritative intermediate result;
- distance-to-preferred-duration scoring;
- cardinal interpretation of `-3 ... +3`;
- Macro Adjustment applied to an ETF-independent directional score before exposure;
- Stance terminology as part of the current Duration Evaluation path.

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

Do not calculate a complete ETF-independent Duration judgment and attach the ETF exposure afterward.

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

## 3.3 Constituent Evaluations need not be orthogonal

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
- a relative rank only among the four synthetic exposures.

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

The Codex work should therefore test whether candidate horizons successfully implement the intended roles rather than search for horizons that maximize return forecasts.

---

# 5. Duration Exposure Representation

Use four working Duration Exposure categories:

```text
Short
Intermediate
Long
Very Long
```

These are the intended model resolution for the current review.

A real ETF Exposure Profile can later be mapped into one of these categories from benchmark and duration characteristics.

Do not replace this four-category model with a continuous or key-rate-duration representation unless the representative-category approach demonstrably loses economically material information.

A richer key-rate profile is a possible future refinement, not a requirement for this work.

---

# 6. Working Hypothesis: Exposure-Relevant Treasury Conditions

The old prototype effectively used a common 10Y-derived rates condition for all Duration Exposures.

The current working hypothesis is:

> **Duration Evaluation should use a rates condition representative of the exposure being evaluated rather than automatically applying one universal 10Y condition to all exposures.**

Conceptually:

```text
Short          → short-end Treasury condition
Intermediate   → intermediate Treasury condition
Long           → long-end Treasury condition
Very Long      → ultra-long Treasury condition
```

An initial candidate mapping is:

```text
Short          → 2Y
Intermediate   → 10Y
Long           → 20Y
Very Long      → 30Y
```

This exact tenor mapping is not yet fixed.

## 6.1 What Codex should test

Compare at least:

```text
Model A:
all four exposures use the same 10Y Trend / Recent Move States

Model B:
each exposure uses Trend / Recent Move from its representative tenor
```

The comparison is not a return-optimization contest.

Evaluate which representation is more economically coherent with:

```text
the ETF exposure's actual rate sensitivity
+
the intended meaning of Duration Evaluation
```

Required diagnostics include:

- historical cases where 2Y, 10Y, 20Y, and 30Y States materially differ;
- whether Model A suppresses economically meaningful cross-exposure differences;
- whether Model B creates interpretable exposure-specific results;
- whether representative-tenor choices generate obvious inconsistencies with the intended exposure categories.

Codex should report evidence for or against each candidate tenor assignment.

Do not select tenors mechanically by forward-return performance.

---

# 7. Trend / Recent Move Horizon Validation

For each candidate representative tenor, calculate:

```text
Yield Trend
Recent Yield Move
```

using one or more economically plausible candidate horizon pairs.

The goal is to validate role separation.

## 7.1 Trend diagnostics

Trend should behave as a broader / established condition.

Report:

- State frequencies;
- average State persistence;
- median State persistence;
- transition frequency;
- representative historical episodes;
- sensitivity to small changes in the candidate horizon.

## 7.2 Recent Move diagnostics

Recent Move should be responsive enough to confirm, pause, or challenge Trend.

Report:

- State frequencies;
- average persistence;
- agreement rate with Trend;
- disagreement rate with Trend;
- length distribution of disagreement episodes;
- representative `Falling × Rising` episodes;
- representative `Rising × Falling` episodes.

## 7.3 Transition-window diagnostics

For selected counter-trend episodes, display a time window showing:

```text
date
yield level
Trend Value
Trend State
Recent Move Value
Recent Move State
```

The purpose is to inspect sequences such as:

```text
Rising × Rising
→ Rising × Stable
→ Rising × Falling
→ Stable × Falling
→ Falling × Falling
```

where such a sequence actually occurred.

Do not assume that every transition must follow this exact path.

The diagnostic question is:

> Does Recent Move provide useful contemporaneous confirmation or challenge before the slower Trend State changes?

This is not a reversal-prediction test.

---

# 8. Core Duration Rule Representation

The complete abstract Rule Case space is:

```text
Trend State
×
Recent Move State
×
Duration Exposure
→ Core Duration Evaluation Result
```

with:

```text
Trend State       ∈ {Falling, Stable, Rising}
Recent Move State ∈ {Falling, Stable, Rising}
Duration Exposure ∈ {Short, Intermediate, Long, Very Long}
```

This gives a conceptual `9 × 4` representation.

Important:

> The four exposure columns do not imply that all four exposures must share the same actual Treasury Rule Case on a historical date.

Under exposure-relevant tenors:

```text
Short
→ uses Short-relevant tenor States

Intermediate
→ uses Intermediate-relevant tenor States

Long
→ uses Long-relevant tenor States

Very Long
→ uses Very-Long-relevant tenor States
```

At one `as_of`, each exposure may therefore occupy a different Rule Case.

---

# 9. Starting Core Mapping for Review

Use the following only as the current **starting ordinal mapping**, not as a formula-derived truth.

| Trend | Recent Move | Short | Intermediate | Long | Very Long | Status |
|---|---|---:|---:|---:|---:|---|
| Falling | Falling | +1 | +2 | +3 | +3 | sign/order strong; exact spacing reviewable |
| Falling | Stable | +1 | +1 | +2 | +2 | sign/order strong; exact spacing reviewable |
| Falling | Rising | 0 / +1 | +1 | +1 / +2 | +1 / +2 | unresolved mixed case |
| Stable | Falling | 0 / +1 | +1 | +1 | +1 / +2 | unresolved mixed case |
| Stable | Stable | 0 | 0 | 0 | 0 | neutral baseline |
| Stable | Rising | 0 / -1 | -1 | -1 | -1 / -2 | unresolved mixed case |
| Rising | Falling | 0 / -1 | -1 | -1 / -2 | -1 / -2 | unresolved mixed case |
| Rising | Stable | -1 | -1 | -2 | -2 | sign/order strong; exact spacing reviewable |
| Rising | Rising | -1 | -2 | -3 | -3 | sign/order strong; exact spacing reviewable |

Do not replace the ranges with invented values.

Codex should help determine whether the ambiguous cells can be narrowed using:

- the established Trend / Recent Move roles;
- exposure sensitivity;
- historical transition behavior;
- row and column consistency;
- comparison across materially different rate regimes.

Human review remains required for any economic mapping not justified by the fixed principles or clear evidence.

---

# 10. Core Mapping Constraints Already Established

The following should be treated as design constraints rather than rediscovered through optimization.

## 10.1 Confirmation / challenge ordering

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

## 10.2 Exposure sensitivity

For otherwise comparable relevant-tenor conditions:

```text
falling-yield conditions
→ greater Duration Exposure should normally receive a larger favorable effect

rising-yield conditions
→ greater Duration Exposure should normally receive a larger unfavorable effect
```

A Short exposure may therefore be least unfavorable in a strongly rising-rate environment without becoming positively attractive.

## 10.3 Neutral condition

The starting interpretation of:

```text
Stable × Stable
```

is:

```text
0 for all four Duration Exposures
```

because the Duration constituent has no directional rates reason to favor or penalize a positive-duration exposure under this Rule Case.

Do not reintroduce a hidden "middle duration is best" assumption.

## 10.4 Mixed cases are not automatically equivalent

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

Their economic meanings differ:

```text
Falling × Rising
→ established favorable broader condition, recently challenged

Stable × Falling
→ no established directional Trend, favorable recent behavior
```

and symmetrically on the rising side.

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

# 11. Historical Validation Design

Historical work should combine:

1. **regime snapshots**;
2. **transition windows**;
3. **full-sample diagnostics**.

No historical case is a training label.

## 11.1 Regime snapshots

Select a compact set of materially different U.S. Treasury environments, including examples of:

- sustained falling-yield conditions;
- sustained rising-yield conditions;
- abrupt risk-off / easing shock;
- inflation / tightening transition;
- restrictive high-yield environment;
- easing or normalization transition.

Use exact `as_of` dates only after inspecting the underlying rate paths so the dates actually represent the intended economic environments.

For each selected `as_of`, report by exposure:

```text
exposure_class
representative_tenor
yield_level
trend_value
trend_state
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

## 11.2 Cross-sectional comparison

At the same `as_of`, compare:

```text
Short
Intermediate
Long
Very Long
```

using each exposure's own representative-tenor States.

Ask:

- Are differences economically interpretable?
- Does the result reflect actual cross-tenor differences rather than merely duration magnitude?
- Does any exposure receive a sign that is obviously inconsistent with its relevant rate segment?

## 11.3 Longitudinal comparison

For each exposure separately, compare results across materially different historical environments.

Ask:

- Does the same exposure move sensibly from favorable to unfavorable conditions?
- Are transitions excessively noisy?
- Do Trend and Recent Move play their intended roles?
- Do mixed Rule Cases behave plausibly?

---

# 12. Mixed-Case Investigation

The highest-priority unresolved Core cases are:

```text
Falling × Rising
Stable  × Falling

Stable  × Rising
Rising  × Falling
```

For each representative tenor, identify multiple historical episodes of each mixed Rule Case where available.

For each episode, display:

```text
preceding Trend / Recent Move States
current Rule Case
subsequent contemporaneous State evolution
yield path around the episode
```

The purpose is not to ask:

> Which Rule Case predicted the best future return?

The purpose is to ask:

> Does the proposed ordinal interpretation fit what the Components actually mean at that time?

Codex should summarize whether historical episodes support:

- the same ordinal category for the paired mixed cases;
- a systematic ordering between them;
- exposure-dependent differences in classification;
- continued ambiguity that should remain a human model-design decision.

---

# 13. Macro Adjustment Validation

Macro Adjustment operates on the already exposure-specific Core Duration Evaluation Result.

The initial input form is:

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

## 13.1 Existing macro rules are not automatically authoritative

If an older Inflation Trend × Policy Direction table is available, Codex may reproduce it as a **candidate fixture**.

Do not assume that old actions such as:

```text
cap positive at +1
cap positive at +2
cap negative at -1
cap negative at -2
```

retain exactly the same meaning under the current exposure-specific ordinal Core score.

The old rule can be reused only if its economic intent still makes sense after translation to the current Core Result semantics.

## 13.2 Candidate action semantics

Useful candidate action types include:

```text
pass-through
weaken
ordinal cap
```

Any action should operate on the ordinal Core result.

For example:

```text
Core = +3
Macro action = cap at +1
Final = +1
```

means:

> a strongly favorable Core Duration assessment is limited to mildly favorable under the macro condition.

It does not mean that two cardinal units of attractiveness were removed.

## 13.3 Macro diagnostics

For each candidate Macro Adjustment mapping, report:

- frequency of each action;
- Core-to-final transition counts;
- cases where Macro changes sign;
- cases where Macro compresses strong Core results;
- cases where different exposures with different Core results converge to the same final result;
- historical examples of each non-pass-through action;
- potential overlap with the realized rate signal already captured in Core.

Macro rules should not be optimized for historical ETF returns.

---

# 14. Macro Double-Counting Review

The main economic risk is not repeated use of the same variable name.

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

Codex should therefore identify candidate Macro cases where the adjustment appears:

```text
clearly incremental
possibly overlapping
apparently duplicative
```

but should not redesign the macro model automatically.

---

# 15. Duration / Curve Boundary Check

This work should confirm only one limited issue:

> Using exposure-relevant Treasury tenors inside Duration Evaluation does not by itself make Curve Evaluation redundant.

Duration asks:

> **How favorable are the relevant rates conditions for this ETF's interest-rate sensitivity?**

Curve separately evaluates the ETF's maturity / curve exposure under relative term-structure conditions.

Example:

```text
2Y rising
10Y stable
30Y falling
```

may legitimately produce:

```text
Short Duration result      → unfavorable
Intermediate result        → near neutral
Very Long result           → favorable
```

while Curve Evaluation may later interpret the relative cross-tenor configuration itself.

Codex should not attempt to design Curve Evaluation in this work.

Only flag a concern if the proposed Duration logic clearly begins to encode an explicitly relative curve judgment rather than exposure-specific rate sensitivity.

---

# 16. Comparison Against the Old 10Y-Only Model

Because the common-10Y design is the main historical baseline, retain it only as a diagnostic comparator.

For selected historical dates and transition windows, produce side-by-side outputs:

```text
common-10Y model
vs.
exposure-relevant-tenor model
```

Compare:

- number of exposures whose Rule Case differs;
- sign differences in Core result;
- ordinal-category differences;
- cases where the common-10Y model appears economically misleading for Short or Very Long exposure;
- cases where the exposure-relevant model adds complexity without meaningful interpretive benefit.

Do not declare the exposure-relevant model superior merely because it produces more differentiated results.

The comparison should be based on economic relevance to the exposure being evaluated.

---

# 17. Full-Sample Diagnostics

At minimum produce:

## 17.1 Component diagnostics

By representative tenor:

- Trend State distribution;
- Recent Move State distribution;
- full 3 × 3 Rule Case frequency table;
- State persistence;
- Rule Case persistence;
- Trend / Recent Move disagreement frequency.

## 17.2 Core-result diagnostics

By exposure:

- Core score distribution;
- transition matrix;
- average persistence;
- frequency of each mixed Rule Case;
- frequency of neutral;
- frequency of extreme `±3`;
- cross-exposure divergence at the same `as_of`.

## 17.3 Mapping diagnostics

Report:

- monotonicity violations relative to established constraints;
- cells that remain unresolved;
- historical examples that challenge the starting mapping;
- cells where multiple economically different situations collapse into one ordinal category;
- cases where the same ordinal score appears defensible despite different underlying economic ordering.

## 17.4 Macro diagnostics

When Macro Adjustment is enabled:

- Core vs final distribution;
- action frequency;
- compression frequency;
- sign-change frequency;
- potential double-counting examples.

These diagnostics are review aids, not objectives to optimize.

---

# 18. Explicit Non-Goals

Codex must not:

- redesign the Bondview system architecture;
- treat retired Stance structures as authoritative;
- optimize representative tenors by forward ETF returns;
- optimize Trend / Recent Move horizons by predictive performance;
- fit the 9 × 4 Core table to historical winners;
- infer cardinal utility from ordinal scores;
- reintroduce the old distance-to-preferred-duration formula;
- reintroduce an ETF-independent Duration preference as the authoritative Core result;
- apply Macro Adjustment before ETF exposure enters the Core Evaluation;
- force Duration and Curve to use disjoint inputs;
- design Curve Evaluation as part of this task;
- treat historical snapshots as labels that the model must reproduce.

---

# 19. Codex Work Sequence

Execute in this order.

## Phase A — Reproduce current inputs

1. Locate reusable existing code for Treasury yield history, Trend, and Recent Move.
2. Reuse only calculations compatible with the current Component roles.
3. Make all reused assumptions explicit.
4. Do not silently inherit old scoring logic.

## Phase B — Build tenor-aware Components

1. Calculate candidate Trend / Recent Move series for the candidate representative tenors.
2. Produce Component diagnostics.
3. Compare horizon candidates.
4. Identify transition windows.

## Phase C — Compare common-10Y vs exposure-relevant inputs

1. Run both input designs over the same historical sample.
2. Compare resulting Rule Cases by exposure.
3. Surface cases where the choice materially affects interpretation.
4. Do not optimize against subsequent returns.

## Phase D — Evaluate the starting 9 × 4 Core mapping

1. Apply the current starting ordinal table.
2. Produce row / column consistency checks.
3. Inspect the four mixed Rule Cases in detail.
4. Leave unresolved cells explicitly unresolved if evidence is insufficient.

## Phase E — Historical regime review

1. Select representative historical regimes from the actual data.
2. Produce cross-sectional exposure tables.
3. Produce longitudinal exposure tables.
4. Produce transition-window plots / tables for key mixed cases.

## Phase F — Macro Adjustment review

1. Reproduce any reusable old macro mapping only as a candidate fixture.
2. Translate candidate actions into current ordinal Core semantics.
3. Apply Macro directly to the exposure-specific Core result.
4. Produce Core-to-final diagnostics.
5. Flag possible double counting.

## Phase G — Findings

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

# 20. Required Deliverables

Codex should produce review artifacts rather than production architecture.

At minimum:

```text
1. duration_validation_summary.md
2. duration_tenor_comparison.csv
3. duration_component_diagnostics.csv
4. duration_core_rulecase_review.csv
5. duration_historical_regime_review.csv
6. duration_transition_episode_review.csv
7. duration_macro_review.csv
```

Plots may be generated where useful, especially for transition windows.

The summary should contain:

## A. Confirmed findings

Only conclusions supported by the fixed design plus the diagnostics.

## B. Recommended refinements

Changes that are economically justified by the review.

## C. Unresolved decisions

Questions that still require human judgment.

## D. Rejected prior assumptions

Old logic found incompatible with the current design.

## E. Suggested model-contract updates

Only after the validation findings are complete, identify which stable conclusions should be moved into a dedicated Duration design / model contract.

Codex should not update the authoritative architecture or vocabulary unless explicitly instructed separately.

---

# 21. Questions This Work Must Answer

The review should end with direct answers to these questions:

1. Does one universal 10Y Trend / Recent Move pair remain defensible for all four Duration Exposures?
2. If not, what representative tenor is justified for each exposure category?
3. Do the selected Trend and Recent Move horizons actually implement the intended broader-condition vs confirmation/challenge roles?
4. Does Recent Move behave as a contemporaneous modifier rather than an implicit reversal forecast?
5. Are the strong directional Core cases economically coherent across Short, Intermediate, Long, and Very Long?
6. How should the four mixed Rule Cases be ordered and classified on the ordinal scale?
7. Is `Stable × Stable → 0` for all four exposures consistent with the Duration constituent's intended meaning?
8. Does the exposure-relevant-tenor design improve economic coherence without making Curve Evaluation redundant?
9. Can Macro Adjustment be expressed cleanly as an ordinal modification of the exposure-specific Core result?
10. Which Macro cases appear incremental versus potentially duplicative of realized rate conditions?
11. Which current Duration choices are sufficiently validated to move into a stable lower-level model contract?
12. Which choices should remain explicitly unresolved?

---

# 22. Current Working Starting Point

The current working model to test is:

```text
ETF Duration Exposure Profile
        ↓
Short / Intermediate / Long / Very Long

Exposure category
        ↓
representative Treasury tenor

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

The main unresolved lower-level areas are:

```text
representative tenor mapping
Trend horizon
Recent Move horizon
mixed Rule Case scores
exact Macro Adjustment mapping
```

The work should validate these directly without reopening system architecture that is already settled.
