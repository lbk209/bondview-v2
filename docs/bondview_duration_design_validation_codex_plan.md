# Bondview Duration Design Validation — Codex Work Plan

## 1. Purpose and Authority

This document defines the temporary validation work plan for the current Bondview **Duration Evaluation** design.

Work from the latest `main` state of:

```text
lbk209/bondview-v2
```

For Codex validation work, the authoritative design reference is:

```text
docs/bondview_system_architecture.md
```

If needed, this document may be used as supporting task context.

Do not use other repository documents as design authority unless a later prompt explicitly allows them.

This plan is intentionally narrower than a permanent Duration design contract. It records:

- the fixed starting Duration design used for validation;
- the meaningful conclusions from completed Task 1;
- the remaining Trend-definition question;
- the validation gate that must be passed before Macro Adjustment work begins.

Detailed Codex outputs and exploratory diagnostics remain in separate report artifacts.

The work sequence is now:

```text
Task 1 — Core mapping historical validation
        [COMPLETED]
        ↓
Task 2 — Trend Definition Validation
        [MANDATORY]
        ↓
Human Trend / Core Review Gate
        ↓
Optional narrow State-Classification review
        [only if Task 2 identifies a material need]
        ↓
Task 3 — Macro Adjustment validation
```

Task 2 is now a substantive design-validation gate rather than a secondary parameter check.

---

# 2. Fixed Duration Design Context

The Duration path remains:

```text
Duration-relevant Components
+
ETF Duration Exposure
        ↓
Core Duration Evaluation
        ↓
Core Duration Evaluation Result
        ↓
Macro Adjustment
        ↓
Duration Evaluation Result
```

The Core result is already exposure-specific.

Do not introduce an ETF-independent market-derived preferred Duration as an authoritative intermediate result.

The current synthetic Duration Exposure categories are:

```text
Short
Intermediate
Long
```

with representative Treasury tenors:

```text
Short        → 6M
Intermediate → 10Y
Long         → 30Y
```

The representative tenor follows the economic center of the intended Duration Exposure.

The current Core result scale is ordinal:

```text
+3  strongly favorable
+2  favorable
+1  mildly favorable
 0  neutral
-1  mildly unfavorable
-2  unfavorable
-3  strongly unfavorable
```

The codes express ordering, not cardinal distance.

---

# 3. Trend and Recent Move Economic Roles

The intended economic roles remain fixed at this stage:

```text
Yield Trend
→ broader directional rates condition relevant to the exposure

Recent Yield Move
→ shorter-horizon movement that may confirm, pause,
   or oppose that broader condition
```

Task 1 did **not** establish that Trend is an unnecessary Component.

The current issue is narrower:

> Does the provisional Trend calculation represent the intended broader current directional condition well enough for Duration Evaluation?

The distinction between Trend and Recent Move must be economically useful for the Duration decision, not merely linguistically tidy.

A mixed Rule Case such as:

```text
Trend = Falling
Recent Move = Rising
```

is not inherently problematic.

It may legitimately describe:

```text
broader falling-yield condition
+
shorter-horizon countertrend rise
```

The concern arises when the opposing Recent Move persists long enough that the old Trend may no longer represent the economically relevant broader current condition.

---

# 4. Task-1 Fixture

Task 1 used the following fixed research fixture.

## 4.1 Component calculations

For each representative Treasury tenor:

```text
Recent Move
→ approximately 1M
→ 5-observation endpoint mean
   minus 5-observation reference mean
   centered approximately 21 valid observations earlier

Trend
→ approximately 6M
→ 5-observation endpoint mean
   minus 5-observation reference mean
   centered approximately 126 valid observations earlier
```

State Classification:

```text
Recent Move:
Falling < -10 bp
Stable  = -10 bp to +10 bp
Rising  > +10 bp

Trend:
Falling < -25 bp
Stable  = -25 bp to +25 bp
Rising  > +25 bp
```

Absolute yield level is not a separate Duration Core input.

These definitions were Task-1 fixtures, not final production Component definitions.

## 4.2 Starting Core Rule Mapping

| Trend | Recent Move | Short (6M states) | Intermediate (10Y states) | Long (30Y states) |
|---|---|---:|---:|---:|
| Falling | Falling | +1 | +2 | +3 |
| Falling | Stable | +1 | +1 | +2 |
| Falling | Rising | 0 / +1 | +1 | +1 / +2 |
| Stable | Falling | 0 / +1 | +1 | +1 / +2 |
| Stable | Stable | 0 | 0 | 0 |
| Stable | Rising | 0 / -1 | -1 | -1 / -2 |
| Rising | Falling | 0 / -1 | -1 | -1 / -2 |
| Rising | Stable | -1 | -1 | -2 |
| Rising | Rising | -1 | -2 | -3 |

The underlying economic ordering is intended to be strict:

```text
Falling × Falling
more favorable than
Falling × Stable
more favorable than
Falling × Rising
```

and:

```text
Rising × Falling
more favorable than
Rising × Stable
more favorable than
Rising × Rising
```

However, the mapped ordinal scale is coarse.

Therefore mapped categories may tie and need satisfy only:

```text
Falling × Falling
>= Falling × Stable
>= Falling × Rising

Rising × Falling
>= Rising × Stable
>= Rising × Rising
```

where `>=` means **no less favorable**.

For otherwise comparable exposure-local conditions:

```text
falling yields
→ Long >= Intermediate >= Short

rising yields
→ Short >= Intermediate >= Long
```

Mapped-category ties are allowed.

---

# 5. Task 1 — Completed Result

Task 1 historically validated the starting Core mapping using the fixed fixture above.

The detailed evidence is retained in:

```text
reports/duration_task1_core_validation.md
reports/duration_task1_core_results.csv
```

## 5.1 Main accepted findings

Task 1 supports the following conclusions:

1. The fixed Task-1 calculation and State Classification fixture is mechanically usable for historical review.

2. All nine `Trend × Recent Move` Rule Cases have meaningful historical coverage.

3. No currently settled Core Rule Mapping cell requires change based on Task-1 evidence.

4. Aligned falling-yield and rising-yield cases behave consistently with the intended Duration sign and exposure sensitivity.

5. Exposure-local evaluation is materially important. On the common calculable sample, Short / Intermediate / Long occupied different Rule Cases on a large majority of dates. A single same-date market-wide Duration Rule Case would therefore discard economically meaningful tenor differences.

6. Historical event review did not identify a material persistent contradiction in the settled mapping.

7. Historical occurrence is useful for sign, ordering, transition behavior, and interpretability, but does not uniquely calibrate adjacent ordinal categories such as `+1` versus `+2`.

## 5.2 Task-1 provisional mixed-cell conclusions

Task 1 provisionally recommended:

```text
Short:
Stable × Falling → +1
Stable × Rising  → -1

Long:
Falling × Rising → +1
Rising × Falling → -1
```

Task 1 left unresolved:

```text
Short:
Falling × Rising → 0 / +1
Rising × Falling → -1 / 0

Long:
Stable × Falling → +1 / +2
Stable × Rising  → -2 / -1
```

These are **not yet accepted final mappings**.

All Task-1 mixed-cell conclusions remain provisional until Task 2 determines whether the Trend definition materially changes their interpretation.

## 5.3 Important Task-1 Trend finding

Task 1 found prolonged opposing-direction mixed episodes.

For example, cases of:

```text
Falling Trend × Rising Recent Move
```

or:

```text
Rising Trend × Falling Recent Move
```

can persist for dozens of valid observations, including episodes lasting roughly two to three months.

This is the main reason Task 2 is now mandatory.

The finding does **not** by itself mean:

```text
Trend is invalid
```

or:

```text
mixed Rule Cases are invalid
```

It raises the narrower question:

> Is the provisional 6M Trend too slow for the intended role of a broader **current** directional rates condition, or are the prolonged mixed states economically legitimate conditions that the Rule Case design should preserve?

## 5.4 Secondary Task-1 classification observation

Short Duration showed materially higher Stable occupancy than the longer representative tenors, including long Stable runs in low-rate periods.

This is worth retaining as a later diagnostic concern, but State thresholds must remain fixed during Task 2 so that Trend-definition effects can be isolated.

Do not introduce volatility-adaptive thresholds or change endpoint smoothing during the main Task-2 comparison.

---

# 6. Historical Event Basis

Task 1 used predefined historical windows selected before inspecting Bondview outputs.

They remain useful as reference cases for later validation.

| Event window | Historical environment | Type |
|---|---|---|
| 1981-07 to 1981-10 | Volcker tightening / long-rate peak | Anchor |
| 1987-08 to 1987-10 | Pre-crash rate pressure followed by flight-to-quality rally | Challenge |
| 1994-02 to 1994-11 | Fed tightening / bond-market selloff | Anchor |
| 1998-08 to 1998-10 | Russia / LTCM flight to quality | Anchor |
| 2008-09 to 2008-12 | Global financial crisis / Treasury flight to quality | Anchor |
| 2013-05 to 2013-09 | Taper tantrum | Anchor |
| 2020-02 to 2020-03 | COVID Treasury shock | Challenge |
| 2022-01 to 2022-10 | Inflation / aggressive tightening cycle | Anchor |
| 2023-07 to 2023-10 | Long-end Treasury selloff | Challenge |

Task 2 should not repeat the full Task-1 event review equally across all windows.

It should prioritize episodes that are informative about **Trend responsiveness and mixed-state interpretation**.

Priority cases include:

```text
1980 model-derived prolonged opposing-direction episodes
1987 reversal
2008 GFC transition
2020 COVID transition
2022 midsummer relief
2023 long-end selloff
```

The 1980 episodes are model-derived diagnostics, not ex-ante validation events.

---

# 7. Task 2 — Trend Definition Validation

## 7.1 Primary question

Task 2 asks:

> Which Trend definition best represents the broader directional rates condition relevant to Duration Evaluation while remaining meaningfully distinct from Recent Move?

The immediate issue is whether the current approximately 6M overlapping Trend remains tied to an old directional regime for too long when Recent Move has already been persistently opposite.

Task 2 is therefore not merely a generic robustness exercise.

It validates the **Trend Component definition used by Duration Evaluation**.

## 7.2 Fixed inputs during Task 2

Keep fixed:

```text
Short        → 6M Treasury
Intermediate → 10Y Treasury
Long         → 30Y Treasury

Recent Move horizon
→ approximately 1M

Recent Move State thresholds
→ ±10 bp

Trend State thresholds
→ ±25 bp

5-observation endpoint/reference smoothing

Task-1 Core Rule Mapping and candidate sets
```

Do not change smoothing or State thresholds during the main Trend comparison.

This isolates the effect of Trend horizon and window construction.

## 7.3 Trend variants

Compare:

```text
A. 6M overlapping Trend
   current Task-1 baseline

B. 3M overlapping Trend

C. 6M Trend excluding the latest 1M

D. 3M Trend excluding the latest 1M
```

Conceptually:

```text
overlapping Trend
→ broader direction measured through the current date

excluding-latest-1M Trend
→ broader direction established before the latest Recent Move
```

The non-overlapping variants are secondary semantic candidates, not presumed improvements.

### Priority of comparisons

The primary comparison is:

```text
6M overlapping
vs.
3M overlapping
```

because Task 1 raised a concrete concern that the 6M baseline may be too slow during prolonged reversals.

The non-overlapping variants should answer a separate question:

> Does explicit temporal separation between Trend and Recent Move add economically useful interpretation, or does it mainly make Trend more stale?

Do not prefer a non-overlapping definition merely because its verbal semantics are cleaner.

---

# 8. Task-2 Diagnostics

## 8.1 Full-sample diagnostics

For each representative tenor and each Trend variant, report:

- Trend State frequency;
- mean and median Trend-State persistence;
- transition frequency;
- frequency of each `Trend × Recent Move` Rule Case;
- frequency and duration distribution of the four mixed Rule Cases;
- number and percentage of Core candidate/result changes relative to the Task-1 baseline;
- same-date cross-tenor Rule Case disagreement.

These are diagnostics, not optimization objectives.

## 8.2 Opposing-direction episode diagnostics

Focus specifically on:

```text
Falling × Rising
Rising × Falling
```

For each Trend variant, compare:

- episode count;
- median duration;
- upper-tail duration;
- longest episodes;
- magnitude of Trend and Recent Move during prolonged episodes;
- date at which Trend changes State during important reversals.

The purpose is not to minimize mixed-case frequency.

A mixed state is legitimate if it remains economically interpretable.

The key question is:

> Does a prolonged opposing-direction episode still represent a useful broader-condition / recent-move distinction, or is Trend simply retaining a stale regime?

## 8.3 Responsiveness versus redundancy

Task 2 must explicitly evaluate both failure modes:

```text
Trend too slow
→ old regime persists after the economically relevant broader condition has changed

Trend too fast
→ Trend follows Recent Move so closely that the two Components become largely redundant
```

A shorter Trend is not automatically better.

A lower mixed-case frequency is not automatically better.

## 8.4 Historical transition review

For the priority historical episodes, show the State path under all four variants.

At minimum inspect:

```text
1980 prolonged mixed episodes
1987 reversal
2008 GFC transition
2020 COVID transition
2022 midsummer relief
2023 long-end selloff
```

For each, ask:

1. When does Recent Move first change?
2. When does each Trend variant change?
3. Is the delay economically reasonable?
4. Does the resulting mixed-state period convey useful information?
5. Does a shorter Trend improve interpretation or merely duplicate Recent Move?
6. Does excluding the latest 1M clarify interpretation or simply delay the Trend?

Do not evaluate the variants using subsequent returns.

## 8.5 Task-1 mapping robustness

Re-evaluate the Task-1 provisional mixed-cell recommendations under each Trend variant.

Specifically track:

```text
Short:
Stable × Falling
Stable × Rising
Falling × Rising
Rising × Falling

Long:
Falling × Rising
Rising × Falling
Stable × Falling
Stable × Rising
```

For each provisional recommendation, classify its Task-2 status as:

```text
strengthened
unchanged
weakened
reopened
still unresolved
```

Explain whether any change results from:

```text
better Trend semantics
different Rule Case occupancy
different reversal timing
or
mere mechanical shortening / shifting of the Trend window
```

---

# 9. Required Task-2 Conclusion

Task 2 must recommend one of:

```text
6M overlapping Trend
3M overlapping Trend
6M excluding latest 1M
3M excluding latest 1M
Current Trend calculation requires reconsideration
```

The recommendation should be based on:

```text
economic usefulness for Duration Evaluation
+
responsiveness to genuine regime change
+
distinctness from Recent Move
+
persistence / stability
+
historical transition plausibility
+
robustness of Task-1 Core conclusions
```

not predictive performance.

The Task-2 report must also provide:

```text
Recommended Trend definition

Why the chosen definition best represents the broader
current directional rates condition

Whether prolonged mixed states remain economically legitimate

Task-1 provisional mixed cells:
- confirmed provisionally
- reopened
- unresolved

Any settled Core cells that unexpectedly require reopening

Whether State Classification or endpoint smoothing requires
a separate narrow follow-up review
```

---

# 10. Human Trend / Core Review Gate

After Task 2, stop.

Do not automatically proceed to Macro Adjustment.

Required review output:

```text
Recommended Trend definition
Recommended Recent Move definition [unchanged unless explicitly reviewed later]
Recommended Core Rule Table
Remaining unresolved Core cells
Material historical contradictions
Need for optional State-Classification review: yes / no
```

Human review decides whether to accept or modify these conclusions.

If the accepted Trend definition differs materially from the Task-1 baseline, the final Core table must reflect the Task-2 re-evaluation of mixed cells.

---

# 11. Optional Narrow State-Classification / Smoothing Review

This is **not a mandatory task**.

Run it only if Task 2 shows that remaining concerns are primarily caused by:

```text
Stable-threshold behavior
or
endpoint smoothing / responsiveness
```

Possible questions may include:

```text
fixed bp thresholds
vs.
volatility-adaptive thresholds

Recent Move:
1-day vs 3-day vs 5-day endpoint smoothing

Trend:
whether 5-day endpoint smoothing remains appropriate
```

Do not run this review merely because alternative mechanics are available.

Its purpose is to resolve a specific residual concern identified by Task 2.

If required, complete and review it before Task 3.

---

# 12. Task 3 — Macro Adjustment Validation

Task 3 begins only after the Trend / Core Review Gate is accepted and any required narrow classification review is complete.

Its fixed inputs are the accepted:

```text
representative tenors
Recent Move definition
Trend definition
Core Rule Mapping
```

Macro Adjustment then follows:

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

Task 3 asks:

> Does Macro Adjustment add economically useful information to the accepted exposure-specific Core result without materially duplicating rate information already captured by Core?

Candidate ordinal actions may include:

```text
pass-through
cap positive at +2
cap positive at +1
cap negative at -1
cap negative at -2
```

Do not use transformations that assume cardinal spacing.

Required diagnostics should include:

- frequency of each Macro action;
- Core-to-final transitions;
- sign changes;
- compression of strong Core results;
- historical examples of non-pass-through actions;
- cases where Macro adds distinct information;
- cases where Macro appears substantially overlapping or duplicative.

Task 3 must recommend:

```text
Retain candidate Macro mapping
Retain with specified changes
Simplify Macro mapping
Reject specific duplicative actions
Macro design remains unresolved
```

with concise economic reasoning.

---

# 13. Deliverables

## Completed Task 1

```text
duration_task1_core_validation.md
duration_task1_core_results.csv
```

## Task 2

```text
duration_task2_trend_validation.md
duration_task2_trend_comparison.csv
```

The Markdown report must contain Codex's own economic analysis and recommendation.

Plots should be included only where they materially clarify important disagreement or transition periods.

## Trend / Core Review Gate

```text
duration_core_validation_conclusion.md
```

## Optional classification review

Only if required by the review gate; filenames should reflect the exact narrow question tested.

## Task 3

```text
duration_task3_macro_validation.md
duration_task3_macro_results.csv
```

---

# 14. Explicit Non-Goals

Codex must not:

- redesign Bondview system architecture;
- optimize scores, tenors, horizons, thresholds, or smoothing by forward returns;
- treat historical events as supervised target labels;
- infer cardinal utility from ordinal scores;
- reintroduce preferred-duration / distance scoring;
- introduce an ETF-independent authoritative Duration preference;
- redesign the ETF exposure taxonomy during this validation;
- design Curve Evaluation;
- force Duration and Curve to use disjoint observations;
- alter State thresholds during the main Task-2 Trend comparison;
- alter endpoint smoothing during the main Task-2 Trend comparison;
- automatically proceed to Macro Adjustment before the Trend / Core Review Gate is accepted.

The objective is to establish an interpretable and economically coherent Duration Evaluation design, not to maximize predictive fit.
