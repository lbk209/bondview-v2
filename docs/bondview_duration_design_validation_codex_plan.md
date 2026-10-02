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

This document is supporting task context. Do not use other repository documents as design authority unless a later prompt explicitly allows them.

This plan is intentionally narrower than a permanent Duration design contract. It records:

- the fixed Duration design context used for validation;
- the accepted conclusions from completed Task 1;
- the accepted conclusions and remaining qualification from completed Task 2;
- the required narrow State-Classification review triggered by Task 2;
- the human review gate required before Macro Adjustment validation begins.

Detailed scripts, observation-level outputs, and exploratory diagnostics remain in `validation/` artifacts and do not become design authority merely because they are committed.

The work sequence is now:

```text
Task 1 — Core mapping historical validation
        [COMPLETED]
        ↓
Task 2 — Trend Definition Validation
        [COMPLETED]
        ↓
Task 2B — Trend State-Classification Validation
        [REQUIRED BY TASK-2 RESULT]
        ↓
Human Trend / Core Review Gate
        ↓
Task 3 — Macro Adjustment validation
```

Task 2 resolved the main **Trend horizon / window-construction** question but exposed a material **State-Classification** question. Therefore the previously optional narrow classification review is now required before the Trend/Core package can be accepted for Macro work.

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

The intended economic roles remain fixed:

```text
Yield Trend
→ broader directional rates condition relevant to the exposure

Recent Yield Move
→ shorter-horizon movement that may confirm, pause,
   or oppose that broader condition
```

The distinction must be economically useful for **Duration Evaluation**, not merely linguistically tidy.

A mixed Rule Case such as:

```text
Trend = Falling
Recent Move = Rising
```

is not inherently problematic. It may legitimately describe:

```text
broader falling-yield condition
+
shorter-horizon countertrend rise
```

Task 1 and Task 2 together support retaining both Components. The remaining question is not whether Trend should exist, but whether the selected Trend Value is classified into `Falling / Stable / Rising` in a sufficiently stable and economically meaningful way.

---

# 4. Task-1 Fixture

Task 1 used the following fixed research fixture.

## 4.1 Component calculations

For each representative Treasury tenor:

```text
Recent Move
→ approximately 1M
→ M5(t) - M5(t-21)

Trend
→ approximately 6M
→ M5(t) - M5(t-126)
```

where `M5(k)` is the mean of the five valid observations ending at `k`.

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

These definitions were research fixtures, not automatically final production definitions.

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

The underlying economic ordering is intended to be strict, but mapped ordinal categories may tie because the scale is coarse.

Mapped constraints therefore remain:

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

---

# 5. Task 1 — Completed Result

Detailed Task-1 evidence is retained in:

```text
validation/261002_duration/task1_core/analysis.py
validation/261002_duration/task1_core/results.csv
validation/261002_duration/task1_core/report.md
```

`results.csv` is both the committed observation-level result and the frozen Task-1 source snapshot used for exact replay.

## 5.1 Main accepted findings

Task 1 supports the following conclusions:

1. The Task-1 calculation and State-Classification fixture is mechanically usable for historical review.
2. All nine `Trend × Recent Move` Rule Cases have meaningful historical coverage.
3. No currently settled Core Rule Mapping cell requires change based on Task-1 evidence.
4. Aligned falling-yield and rising-yield cases behave consistently with the intended Duration sign and exposure sensitivity.
5. Exposure-local evaluation is materially important. Short / Intermediate / Long occupy different Rule Cases on a large majority of common dates; a single market-wide Duration Rule Case would discard meaningful tenor differences.
6. Historical event review did not identify a material persistent contradiction in the settled mapping.
7. Historical occurrence supports sign, ordering, transition behavior, and interpretability, but does not uniquely calibrate adjacent ordinal categories such as `+1` versus `+2`.

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

These were not final mappings.

## 5.3 Important Task-1 Trend finding

Task 1 found prolonged opposing-direction mixed episodes. In particular, `Falling × Rising` or `Rising × Falling` could persist for dozens of valid observations, including roughly two to three months.

This did **not** invalidate mixed Rule Cases or the Trend concept. It raised the narrower question:

> Was the approximately 6M Trend too slow for the intended role of a broader **current** directional rates condition?

That question became Task 2.

## 5.4 Secondary Task-1 classification observation

Short Duration showed materially higher Stable occupancy than the longer representative tenors, including long Stable runs in low-rate periods. This remained a diagnostic concern but thresholds and smoothing were deliberately held fixed during Task 2 so the Trend-horizon question could be isolated.

---

# 6. Historical Event Basis

The following predefined windows remain the general historical reference set:

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

Task 2 additionally emphasized transition cases informative about Trend responsiveness:

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

# 7. Task 2 — Completed Trend Definition Validation

Task 2 compared four Trend constructions while keeping Recent Move, thresholds, smoothing, representative tenors, and the Task-1 Core mapping fixed.

The completed evidence is retained in:

```text
validation/261002_duration/task2_trend/analysis.py
validation/261002_duration/task2_trend/comparison.csv
validation/261002_duration/task2_trend/report.md
```

The result reviewed here was produced on session branch:

```text
codex/session/261002_1713
```

## 7.1 Tested variants

```text
A. 6M overlapping
   M5(t) - M5(t-126)

B. 3M overlapping
   M5(t) - M5(t-63)

C. 6M excluding latest 1M
   M5(t-21) - M5(t-147)

D. 3M excluding latest 1M
   M5(t-21) - M5(t-84)
```

Recent Move remained:

```text
M5(t) - M5(t-21)
```

Task-2 State thresholds remained fixed:

```text
Trend: ±25 bp
Recent Move: ±10 bp
```

## 7.2 Mechanical validation accepted

Task 2 used only the frozen Task-1 source snapshot and verified its SHA-256 before analysis.

The 6M-overlapping baseline reproduced all **38,330** complete Task-1 observations exactly for:

```text
trend_bp
trend_state
recent_move_bp
recent_move_state
rule_case
core_candidates
```

The analysis preserved:

- valid-observation indexing;
- no calendar interpolation;
- the DGS30 structural-gap exclusion;
- segment boundaries;
- exact threshold handling;
- no network refresh or return-series labels.

No material implementation problem was identified in review.

## 7.3 Main accepted Task-2 finding

Task 2 provisionally prefers:

```text
3M overlapping Trend
= M5(t) - M5(t-63)
```

for the intended role:

> broader **current** directional rates condition relevant to Duration Evaluation.

The conclusion is specifically about **Trend horizon and window construction**. It is not yet acceptance of the full Trend definition including the current ±25 bp State Classification.

### Why 3M overlapping is preferred

The 6M baseline can remain tied to an old directional regime for too long during sustained reversals.

The strongest example is the 1980 reversal.

For 10Y:

```text
Recent becomes Rising: 1980-07-09
3M Trend → Stable:     1980-07-31
3M Trend → Rising:     1980-08-05
6M Trend → Stable:     1980-10-15
6M Trend → Rising:     1980-10-20
```

For 30Y:

```text
Recent becomes Rising: 1980-07-10
3M Trend → Stable:     1980-08-01
3M Trend → Rising:     1980-08-06
6M Trend → Stable:     1980-10-15
6M Trend → Rising:     1980-10-21
```

The 3M Trend does not merely copy the first opposing Recent Move. It allows several weeks of counter-movement before recognizing a new broader condition. The 6M Trend, by contrast, can retain the old regime into a point where the historical comparison is no longer a good representation of the broader **current** direction.

Task-1 Short 2008 and Long 1984 reversal episodes provide additional evidence in other tenors and directions.

## 7.4 3M Trend remains distinct from Recent Move

The 3M Trend is more responsive than the 6M baseline but remains materially more persistent than Recent Move.

Transition frequencies on the common sample were approximately:

```text
                6M Trend    3M Trend    Recent Move
Short             1.64%       2.18%       4.42%
Intermediate      2.87%       3.79%       7.25%
Long              2.96%       3.91%       7.76%
```

Thus Task 2 does not support the concern that the 3M Trend simply becomes another copy of the 1M Recent Move.

Mixed Rule Cases also remain materially populated.

## 7.5 Non-overlapping variants not preferred

The non-overlapping variants satisfy:

```text
C(t) = A(t-21)
D(t) = B(t-21)
```

within accepted segments.

For a Component intended to represent the broader **current** directional condition, this explicit one-month shift generally adds age rather than useful interpretation. Historical transitions, including 2020 and 2022, do not show enough compensating benefit.

Therefore the current validation path does not retain C or D as active Trend candidates.

## 7.6 Important counterexample: 2022 midsummer relief

Task 2 also established that prolonged opposing-direction states can be economically legitimate.

During 2022 midsummer relief, the 6M Trend retained a broader Rising condition while 10Y and 30Y Recent Move became Falling. This cleanly represented:

```text
broader tightening / rising-yield condition
+
shorter-horizon relief
```

The 3M Trend responded sooner, which is useful in sustained reversals but also created short boundary-adjacent classifications that were stronger than the underlying continuous Values appeared to justify.

This counterexample is important because Task 2 does **not** support minimizing mixed-state duration as an objective.

## 7.7 Material State-Classification finding

Changing the Trend horizon from 6M to 3M while holding the ±25 bp threshold fixed materially changed Trend State occupancy.

Stable occupancy changed approximately as follows:

```text
                6M Trend    3M Trend
Short             38.93%      53.45%
Intermediate      31.05%      42.49%
Long              28.57%      43.10%
```

These are material changes, not minor differences.

The changed Trend States also changed Core candidate sets on approximately:

```text
Short             24.47%
Intermediate      39.10%
Long              40.47%
```

of common-sample observations.

This does not invalidate the 3M horizon. It means the State boundary is now sufficiently consequential that the full Trend definition cannot be accepted without a narrow classification review.

A central example is 2022 10Y. The 3M Trend briefly crossed below the fixed -25 bp threshold for three observations at approximately -26 bp, changing the Rule Case and mapped Core category sharply despite only a marginal movement around the boundary.

Similar short boundary returns occurred in 1987, 2008, 2022, and 2023.

Task 2 therefore **triggered the previously optional State-Classification review**.

## 7.8 Endpoint smoothing status

Task 2 did not identify a material reason to reopen five-observation endpoint smoothing.

The main unresolved issue is State Classification, not smoothing. Do not vary smoothing in Task 2B unless a later human instruction explicitly expands its scope.

## 7.9 Task-1 mixed-cell status after Task 2

Task 2 leaves the following provisional recommendations unchanged:

```text
Short:
Stable × Falling → +1 provisional
Stable × Rising  → -1 provisional

Long:
Rising × Falling → -1 provisional
```

The Task-1 preference:

```text
Long:
Falling × Rising → +1 provisional
```

is **weakened**. The prominent 1980 evidence that supported restraint within this cell largely changes Rule Case under the 3M Trend. Retain `+1` only as a cautious working candidate, not as independently validated calibration.

The following remain unresolved:

```text
Short:
Falling × Rising → 0 / +1
Rising × Falling → -1 / 0

Long:
Stable × Falling → +1 / +2
Stable × Rising  → -2 / -1
```

No settled Core cell requires reopening based on Task-2 evidence.

## 7.10 Task-2 accepted status

The current design-validation status is:

```text
Trend concept
→ retained

Trend construction
→ overlapping retained
→ excluding-latest-1M not preferred

Trend horizon
→ 3M preferred over 6M

Provisional Trend Value
→ M5(t) - M5(t-63)

Trend State threshold
→ NOT YET ACCEPTED
→ requires Task 2B

Trend smoothing
→ retain 5D for now

Recent Move
→ unchanged for now

Core mapping
→ settled cells retained
→ provisional / unresolved cells remain provisional / unresolved

Macro
→ blocked pending Task 2B and human review gate
```

---

# 8. Post-Task-2 Challenger Discussion — Current Minus Trailing Average

After Task 2, an alternative family was considered conceptually:

```text
current smoothed yield - trailing moving average
```

for example:

```text
M5(t) - M60(t)
M5(t) - M120(t)
```

This family is **not currently scheduled as a validation task**.

## 8.1 Decisive semantic difference

The current endpoint-change Trend asks:

> How much have yields changed over the broader horizon?

For example:

```text
M5(t) - M5(t-63)
```

The moving-average-reference alternative asks:

> How high or low is the current yield relative to its recent trailing regime?

For example:

```text
M5(t) - M60(t)
```

These are related but not equivalent economic questions.

## 8.2 Duration Constituent ownership concern

Duration Evaluation asks how favorable or unfavorable current **Duration-relevant rates conditions** are for an ETF's interest-rate sensitivity. Within that role, Trend is intended to represent **directional rates conditions**.

A current-minus-trailing-average signal can remain strongly positive after a one-time upward repricing has finished and yields have subsequently stayed flat. In such a case it may continue to look like `Rising` because current yields remain above their trailing average, even though the current directional condition has become flat.

This creates a risk that Duration absorbs information about **relative yield level** rather than direction.

That distinction matters because relative/high yield level can also carry information relevant to **Rates Valuation**. A measure that interprets “yield remains high relative to recent history” as an adverse Duration Trend can therefore blur constituent ownership and create avoidable overlap between Duration and Rates Valuation.

This is a deeper issue than threshold calibration.

## 8.3 Current decision on the challenger

Do not replace the endpoint-change Trend with a current-minus-trailing-average formulation at this stage.

Task 2 did not show that the 3M endpoint-change Trend is generally broken. It showed:

```text
6M endpoint Trend
→ too stale in some sustained reversals

3M endpoint Trend
→ materially improves those reversals
→ remains distinct from Recent Move

remaining material issue
→ State Classification around the fixed threshold
```

Therefore the next step is to resolve the demonstrated classification problem rather than change the underlying Trend semantics.

If Task 2B still leaves material economic contradictions after a defensible State Classification is tested, the Trend measurement itself may be reopened. At that point, MA-based challengers may be considered explicitly, with constituent ownership and direction-vs-relative-level semantics evaluated before any empirical parameter search.

Do not launch an MA-reference comparison merely because the formulation is familiar from technical analysis.

---

# 9. Task 2B — Required Trend State-Classification Validation

Task 2B is now mandatory before the Human Trend / Core Review Gate.

## 9.1 Primary question

Task 2B asks:

> Given the provisionally preferred 3M overlapping Trend Value, does the State Classification convert that continuous Value into `Falling / Stable / Rising` in a way that is economically meaningful, sufficiently stable, and appropriate for Duration Core Rule Cases?

The task is about the **classification of the selected Trend Value**, not about selecting another Trend horizon or another Trend semantic concept.

## 9.2 Fixed inputs

Keep fixed unless a later human prompt explicitly changes scope:

```text
Short        → 6M Treasury
Intermediate → 10Y Treasury
Long         → 30Y Treasury

Trend Value
→ M5(t) - M5(t-63)

Recent Move Value
→ M5(t) - M5(t-21)

Recent Move threshold
→ ±10 bp

5-observation endpoint/reference smoothing

Task-1 Core Rule Mapping and candidate sets
```

Do not:

- return to the 6M Trend as a competing candidate;
- reopen overlapping vs non-overlapping construction;
- introduce current-minus-moving-average Trend semantics;
- change Recent Move in the same task;
- change smoothing in the same task;
- use forward returns or ETF returns as labels.

These restrictions isolate State Classification.

## 9.3 Candidate classification mechanics are not yet fixed

The exact alternative classification candidates for Task 2B must be specified by human review before Codex execution.

Codex must not invent threshold values, volatility scaling, hysteresis, persistence filters, or other stabilization rules on its own.

The current baseline is:

```text
Falling < -25 bp
Stable  = [-25 bp, +25 bp]
Rising  > +25 bp
```

The next prompt should identify a small, explicit candidate set designed to test the specific boundary problem found in Task 2.

## 9.4 Required diagnostics once candidates are fixed

At minimum, Task 2B should evaluate:

- State frequency by tenor;
- transition frequency and episode persistence;
- short boundary-return episodes;
- how often small Value changes around a boundary create materially different Core Rule Cases;
- the 2022 10Y and 30Y boundary examples identified by Task 2;
- relevant 1987, 2008, and 2023 boundary-return examples;
- whether genuine reversals such as 1980 remain recognized at economically reasonable times;
- whether mixed Rule Cases remain interpretable;
- whether settled Core cells remain coherent;
- whether Task-1/Task-2 provisional mixed-cell judgments are strengthened, weakened, reopened, or unchanged.

The goal is not to maximize Stable occupancy or minimize switching.

## 9.5 Required conclusion

Task 2B must determine whether:

```text
Current ±25 bp Trend classification can be retained
```

or whether a specifically tested alternative should replace it.

It must also state whether any material residual problem now points to:

```text
Trend Value definition itself
Recent Move definition
endpoint smoothing
Core Rule Mapping
```

rather than State Classification.

If a material residual problem remains outside State Classification, stop and report it. Do not redesign another layer automatically.

---

# 10. Human Trend / Core Review Gate

After Task 2B, stop.

Do not automatically proceed to Macro Adjustment.

Required review output:

```text
Accepted / rejected Trend Value definition
Accepted / rejected Trend State Classification
Recent Move definition status
Recommended Core Rule Table
Remaining provisional / unresolved Core cells
Material historical contradictions
Need to reopen Trend measurement: yes / no
Need to reopen Recent Move or smoothing: yes / no
```

Human review decides whether the Trend / Recent / Core package is sufficiently settled for Macro validation.

If Trend measurement itself must be reopened, possible challengers may include MA-based directional constructions, but only under a separate explicitly scoped task.

---

# 11. Task 3 — Macro Adjustment Validation

Task 3 begins only after the Human Trend / Core Review Gate accepts the required Core inputs.

Its fixed inputs are the accepted:

```text
representative tenors
Recent Move definition
Trend Value definition
Trend State Classification
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

Task 3 must recommend one of:

```text
Retain candidate Macro mapping
Retain with specified changes
Simplify Macro mapping
Reject specific duplicative actions
Macro design remains unresolved
```

with concise economic reasoning.

---

# 12. Deliverables

## Completed Task 1

```text
validation/261002_duration/task1_core/analysis.py
validation/261002_duration/task1_core/results.csv
validation/261002_duration/task1_core/report.md
```

## Completed Task 2

```text
validation/261002_duration/task2_trend/analysis.py
validation/261002_duration/task2_trend/comparison.csv
validation/261002_duration/task2_trend/report.md
```

## Task 2B

Use the existing validation campaign:

```text
validation/261002_duration/
```

Create a task subdirectory only when the exact State-Classification candidate set is fixed. A suitable name is:

```text
validation/261002_duration/task2b_trend_state/
```

Expected artifacts:

```text
analysis.py
comparison.csv
report.md
```

The report must contain Codex's own economic analysis and recommendation, not only numerical diagnostics.

## Trend / Core Review Gate

After Task 2B and human review, record the accepted conclusion in:

```text
validation/261002_duration/core_conclusion/
```

Do not create this directory before a conclusion is actually accepted.

## Task 3

Create only after the Trend / Core Review Gate is accepted:

```text
validation/261002_duration/task3_macro/
```

with filenames reflecting the actual analysis implementation and report.

---

# 13. Explicit Non-Goals

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
- treat lower mixed-state frequency as inherently better;
- infer that more Stable observations are inherently better;
- automatically replace Trend with a current-minus-moving-average technical indicator;
- blur Direction information with Rates Valuation merely to improve transition behavior;
- let Codex invent new classification mechanics not specified by the human-reviewed Task-2B prompt;
- alter endpoint smoothing during Task 2B unless explicitly instructed;
- alter Recent Move during Task 2B unless explicitly instructed;
- automatically proceed to Macro Adjustment before the Human Trend / Core Review Gate is accepted.

The objective is to establish an interpretable and economically coherent Duration Evaluation design, not to maximize predictive fit or produce the smoothest historical State sequence.
