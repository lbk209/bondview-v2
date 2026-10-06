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
- the initial Task-2 Trend comparison and the later review that superseded its 3M preference;
- the completed 6M / 9M / 12M Trend-horizon review;
- the completed threshold review and the current common ±25 bp working threshold;
- the corrected 6M State-stabilization review;
- the human review gate required before Macro Adjustment validation begins.

Detailed scripts, observation-level outputs, notebooks, and exploratory diagnostics remain validation artifacts and do not become design authority merely because they are committed or generated.

The current work sequence is:

```text
Task 1 — Core mapping historical validation
        [COMPLETED]
        ↓
Task 2 — Initial Trend Definition Validation
        [COMPLETED; 3M PREFERENCE SUPERSEDED]
        ↓
Trend Horizon Re-review — 6M / 9M / 12M
        [COMPLETED; 6M PROVISIONALLY PREFERRED]
        ↓
Trend Threshold Review
        [COMPLETED; COMMON ±25 BP RETAINED]
        ↓
Task 2B — Trend State-Classification / Stabilization Review
        [COMPLETED; 5 BP HYSTERESIS PROVISIONALLY PREFERRED]
        ↓
Human Trend / Core Review Gate
        ↓
Task 3 — Macro Adjustment validation
```

The current unresolved question is no longer which Trend horizon to test next. The active human-review question is whether the provisionally preferred package:

```text
6M endpoint-change Trend
+
common ±25 bp directional entry threshold
+
5 bp hysteresis band
```

should be accepted as the Trend State definition used by Duration Core Evaluation.

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

The later horizon review reinforced this point. In particular, the 2022 midsummer relief period showed that a 6M Trend could remain broadly `Rising` while Recent Move became `Falling`, cleanly representing:

```text
broader tightening / rising-yield condition
+
shorter-horizon relief
```

The goal is therefore **not** to minimize mixed-state frequency or opposing-state duration.

The current design question is whether the broader Trend can retain this economic role while avoiding short boundary-driven State excursions that are too weak to deserve a full `Rising` or `Falling` interpretation.

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

These definitions began as research fixtures. Later review has provisionally retained the 6M Trend Value and common ±25 bp entry threshold, while adding a stabilization question around the threshold boundary.

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

> Was the approximately 6M Trend too slow for the intended role of a broader current directional rates condition?

That question triggered the initial Task 2 comparison and, later, the dedicated 6M / 9M / 12M horizon re-review.

## 5.4 Secondary Task-1 classification observation

Short Duration showed materially higher Stable occupancy than the longer representative tenors, including long Stable runs in low-rate periods.

This observation motivated threshold review, but downstream ETF exposure behavior must not determine an upstream Component threshold. Threshold and stabilization choices must be justified as better representations of the Yield Trend Component itself.

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

Later Trend reviews additionally emphasized transition cases informative about horizon inertia and State-boundary behavior:

```text
1980 model-derived reversal episodes
1987 reversal
2008 GFC transition
2020 COVID transition
2022 midsummer relief
2023 long-end selloff
```

The 1980 episodes are model-derived diagnostics, not ex-ante validation events.

Historical windows are challenge and interpretation cases. They are not supervised target labels.

---

# 7. Task 2 — Initial Trend Definition Validation

Task 2 compared four Trend constructions while keeping Recent Move, thresholds, smoothing, representative tenors, and the Task-1 Core mapping fixed.

The completed evidence is retained in:

```text
validation/261002_duration/task2_trend/analysis.py
validation/261002_duration/task2_trend/comparison.csv
validation/261002_duration/task2_trend/report.md
```

The result reviewed there was produced on session branch:

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

## 7.2 Mechanical findings retained

The following Task-2 conclusions remain useful:

- the overlapping endpoint-change construction is retained;
- the excluding-latest-1M variants are not preferred;
- non-overlapping variants mainly add an explicit one-month lag rather than a clearly superior economic interpretation;
- five-observation endpoint smoothing did not emerge as the main problem;
- mixed Trend × Recent Move cases remain economically legitimate;
- a shorter Trend can remain statistically distinct from Recent Move, so distinction alone does not choose the preferred horizon.

## 7.3 Initial 3M preference is superseded

Task 2 originally provisionally preferred:

```text
3M overlapping Trend
= M5(t) - M5(t-63)
```

because it responded faster in sustained reversals such as 1980.

That preference is **no longer the current design conclusion**.

Later review clarified that Trend is intended to represent the broader directional condition, while Recent Move already owns the shorter-horizon confirmation / opposition role. The 2022 midsummer relief period also showed that retaining a broader `Rising` Trend while Recent Move turned `Falling` was economically useful rather than a failure to react.

The later 6M / 9M / 12M review therefore reopened the horizon question from the Component's intended economic role rather than from the goal of accelerating reversal recognition.

The 3M result remains useful historical evidence, but it must not be used as the current accepted Trend definition.

## 7.4 Task-2 2022 boundary example is also superseded as the active classification case

The original Task-2 State-classification concern centered on a 3M 10Y Trend that briefly crossed below -25 bp during the 2022 midsummer relief period.

That example remains evidence that a hard threshold can create abrupt categorical changes near a boundary, but it is **not** the active Trend definition anymore.

Under the current 6M Trend, 10Y and 30Y remain strongly `Rising` through that midsummer relief period. The episode now serves primarily as evidence that broad Trend and shorter Recent Move can legitimately disagree.

---

# 8. Completed Trend Horizon Re-review — 6M / 9M / 12M

The later horizon review compared:

```text
6M Trend  = M5(t) - M5(t-126)
9M Trend  = M5(t) - M5(t-189)
12M Trend = M5(t) - M5(t-252)
```

while keeping:

```text
Recent Move = M5(t) - M5(t-21)
Trend threshold = ±25 bp
Recent Move threshold = ±10 bp
5-observation endpoint smoothing
```

fixed as research controls.

The review notebook is:

```text
bondview_duration_trend_horizon_6m_9m_12m_review.ipynb
```

## 8.1 Scale effect

A fixed ±25 bp threshold is not scale-neutral across Trend horizons.

For example, median absolute Trend magnitude for 10Y was approximately:

```text
6M   45.8 bp
9M   55.2 bp
12M  68.0 bp
```

and for the 6M Treasury tenor approximately:

```text
6M   42.2 bp
9M   66.6 bp
12M  83.8 bp
```

Therefore lower Stable occupancy at longer horizons is partly mechanical and must not be treated as evidence that a longer horizon is economically superior.

## 8.2 Transition frequency

All three tested Trend horizons are already materially slower than Recent Move.

For 10Y:

```text
6M Trend   2.88%
9M Trend   2.51%
12M Trend  1.82%
Recent     7.27%
```

For 30Y:

```text
6M Trend   2.99%
9M Trend   2.68%
12M Trend  2.16%
Recent     7.77%
```

A longer horizon is therefore **not needed merely to make Trend distinct from Recent Move**.

## 8.3 Opposing-direction persistence

Longer Trend horizons increase persistence of opposing Trend × Recent Move cases.

This can sometimes be economically useful, but it is also where a stale broad condition can hide. The horizon decision therefore cannot be based on “more persistence” or “more disagreement with Recent” as optimization targets.

## 8.4 Historical challenge interpretation

The main historical conclusion is:

- 6M is already broad enough to remain distinct from Recent Move;
- 9M does not show a sufficiently clear economic improvement over 6M to justify the added inertia;
- 12M becomes materially more inert in important reversals;
- 2022 demonstrates that 6M can preserve a broad rising-yield condition while Recent Move captures a shorter relief move.

## 8.5 Current horizon conclusion

The current provisional Trend horizon is therefore:

```text
6M overlapping endpoint-change Trend
= M5(t) - M5(t-126)
```

This supersedes the earlier Task-2 preference for 3M.

The 6M choice does **not** imply that every long opposing-direction episode is correct. It means that residual instability should first be addressed at State Classification / stabilization rather than by shortening the underlying Trend horizon.

---

# 9. Completed Trend Threshold Review

After the horizon re-review, Trend State thresholds were reviewed separately from the Trend Value definition.

The review considered a small grid of absolute thresholds rather than using downstream Core scores or ETF outcomes as optimization targets.

The important result was:

```text
6M Treasury tenor
→ modest case for ±30 bp

10Y Treasury tenor
→ ±25 bp preferred / adequate

30Y Treasury tenor
→ ±25 bp preferred / adequate
```

For the 6M tenor, ±30 bp reduced short directional episodes relative to ±25 bp, but the improvement was not large enough to justify introducing separate tenor-specific thresholds at this stage.

The working design therefore retains:

```text
Trend directional entry threshold
→ ±25 bp for 6M, 10Y, and 30Y representative tenors
```

This is a deliberate simplification, not a claim that the threshold grid showed identical behavior at all tenors.

## 9.1 Architectural constraint on threshold selection

A threshold may differ by a canonical Component dimension such as representative market tenor if that distinction is justified by the Component's own economic behavior.

However, threshold selection must remain **consumer-independent**.

Do not select or calibrate a Trend threshold because a particular Short, Intermediate, or Long ETF Duration Exposure produces preferred Core scores under that threshold.

Downstream evaluation or Diagnostics may reveal a classification problem and trigger review, but any change must be justified as a better definition of the Yield Trend Component itself.

## 9.2 Current threshold status

The common ±25 bp threshold is now the **working threshold for stabilization review**.

It remains subject to the Human Trend / Core Review Gate together with the selected stabilization rule.

Recent Move remains:

```text
M5(t) - M5(t-21)
threshold = ±10 bp
```

and has not been reopened in the Trend threshold/stabilization work.

---

# 10. Task 2B — Completed 6M Trend State-Classification / Stabilization Review

The State-stabilization review was rerun on the correct Trend definition:

```text
Trend Value
→ M5(t) - M5(t-126)

Trend directional entry threshold
→ ±25 bp for all representative tenors
```

The earlier persistence/hysteresis run performed on the discarded 3M Trend is not valid evidence for the current design.

The corrected review used the full frozen Task-1 6M baseline:

```text
38,330 classified observations
```

and reproduced the committed plain ±25 bp Trend State classification with zero mismatches before applying any stabilization rule.

## 10.1 Tested stabilization mechanics

The corrected review compared:

```text
plain ±25 bp classification

persistence-2
→ candidate State must persist for 2 consecutive valid observations
   before replacing the active State

persistence-3
→ candidate State must persist for 3 consecutive valid observations
   before replacing the active State

5 bp hysteresis
→ directional entry at ±25 bp
→ Rising exits through +20 bp
→ Falling exits through -20 bp

10 bp hysteresis
→ directional entry at ±25 bp
→ Rising exits through +15 bp
→ Falling exits through -15 bp
```

A direct move across the opposite ±25 bp boundary may move directly into the opposite directional State.

Persistence and hysteresis answer different questions:

- persistence requires time confirmation and therefore delays genuine transitions as well as suppressing noise;
- hysteresis retains the directional State until the underlying Trend Value moves sufficiently back inside the original boundary.

## 10.2 Corrected aggregate results

| Tenor | Variant | Short directional episodes ≤5 (%) | Transition (%) | Median directional episode (obs) | Stable (%) | Changed vs plain (%) |
|---|---|---:|---:|---:|---:|---:|
| 6M | Plain | 29.35 | 1.63 | 15.0 | 38.86 | 0.00 |
| 6M | Persistence-2 | 23.53 | 1.50 | 19.0 | 38.86 | 1.57 |
| 6M | Persistence-3 | 17.57 | 1.28 | 29.5 | 38.81 | 2.87 |
| 6M | Hysteresis-5 bp | 10.61 | 1.17 | 37.0 | 36.89 | 1.97 |
| 6M | Hysteresis-10 bp | 8.77 | 1.01 | 44.0 | 34.92 | 3.94 |
| 10Y | Plain | 23.48 | 2.86 | 20.0 | 31.14 | 0.00 |
| 10Y | Persistence-2 | 16.83 | 2.59 | 23.5 | 31.21 | 2.72 |
| 10Y | Persistence-3 | 14.65 | 2.44 | 26.5 | 31.19 | 5.20 |
| 10Y | Hysteresis-5 bp | 11.79 | 2.43 | 29.0 | 28.63 | 2.51 |
| 10Y | Hysteresis-10 bp | 5.39 | 2.08 | 37.0 | 25.51 | 5.64 |
| 30Y | Plain | 24.10 | 2.96 | 15.0 | 28.72 | 0.00 |
| 30Y | Persistence-2 | 19.21 | 2.69 | 19.0 | 28.75 | 2.83 |
| 30Y | Persistence-3 | 11.03 | 2.42 | 32.0 | 28.78 | 5.26 |
| 30Y | Hysteresis-5 bp | 10.85 | 2.30 | 34.0 | 25.72 | 3.01 |
| 30Y | Hysteresis-10 bp | 4.59 | 1.94 | 47.0 | 22.43 | 6.29 |

A **short directional episode** means a `Rising` or `Falling` State episode lasting five valid observations or fewer. It does not mean that the underlying 6M Trend Value has become a short-horizon measure.

## 10.3 Main stabilization finding

Plain ±25 bp classification still produces a material share of short directional episodes even with the correct 6M Trend.

Persistence reduces this instability, but minimum persistence introduces a built-in recognition delay for every confirmed State transition.

The 5 bp hysteresis rule is more targeted:

- directional entry remains at the same ±25 bp boundary;
- clear transitions can therefore be recognized on the same observation as under plain classification;
- a directional State is prevented from disappearing merely because the Trend retreats slightly inside the original boundary;
- it reduces short directional episodes to roughly 11% across all three tenors;
- it changes fewer observations than persistence-3 at each tenor.

The 10 bp hysteresis rule produces the smoothest State path, but it is materially more aggressive, lowers Stable occupancy more substantially, and changes roughly 4–6% of observations. The current evidence does not establish that the added stickiness is economically justified.

## 10.4 Historical challenge findings

The corrected historical review supports the aggregate result.

### 1980 10Y reversal

The 5 bp hysteresis rule leaves the important plain transition dates essentially unchanged, while persistence-3 delays them through its confirmation requirement.

### 2008 GFC

For 10Y, the decisive transition into the broad `Falling` condition begins on the same date under plain classification and 5 bp hysteresis, while persistence confirms it later.

For 30Y, hysteresis suppresses several boundary-driven short episodes before the sustained `Falling` regime.

### 2022 midsummer relief

For both 10Y and 30Y, the correct 6M Trend remains strongly `Rising` through the relief period.

The shorter Recent Move can therefore carry the countertrend information without requiring Trend to flip. Stabilization does not erase the intended broad-vs-recent separation.

### 2023 30Y selloff

The 5 bp hysteresis rule preserves the major directional entries while reducing boundary exits. Persistence-3 shifts the entries later.

## 10.5 Provisional stabilization conclusion

The strongest current candidate is:

```text
Trend Value
→ M5(t) - M5(t-126)

Directional entry
→ Falling < -25 bp
→ Rising  > +25 bp

Hysteresis exit
→ Falling remains active until Trend >= -20 bp
→ Rising remains active until Trend <= +20 bp
```

This is the **provisionally preferred** Trend State Classification / stabilization rule.

It is not yet a final production rule. Human review must explicitly accept or reject it before Macro Adjustment validation begins.

---

# 11. Post-Task-2 Challenger Discussion — Current Minus Trailing Average

An alternative Trend family was considered conceptually:

```text
current smoothed yield - trailing moving average
```

for example:

```text
M5(t) - M60(t)
M5(t) - M120(t)
```

This family is **not currently scheduled as a validation task**.

## 11.1 Decisive semantic difference

The current endpoint-change Trend asks:

> How much have yields changed over the broader horizon?

The current preferred example is:

```text
M5(t) - M5(t-126)
```

The moving-average-reference alternative asks:

> How high or low is the current yield relative to its recent trailing regime?

For example:

```text
M5(t) - M60(t)
```

These are related but not equivalent economic questions.

## 11.2 Duration Constituent ownership concern

Duration Evaluation asks how favorable or unfavorable current **Duration-relevant rates conditions** are for an ETF's interest-rate sensitivity. Within that role, Trend is intended to represent **directional rates conditions**.

A current-minus-trailing-average signal can remain strongly positive after a one-time upward repricing has finished and yields have subsequently stayed flat. In such a case it may continue to look like `Rising` because current yields remain above their trailing average, even though the current directional condition has become flat.

This creates a risk that Duration absorbs information about **relative yield level** rather than direction.

That distinction matters because relative/high yield level can also carry information relevant to **Rates Valuation**. A measure that interprets “yield remains high relative to recent history” as an adverse Duration Trend can therefore blur constituent ownership and create avoidable overlap between Duration and Rates Valuation.

This is a deeper issue than threshold calibration or State stabilization.

## 11.3 Current decision on the challenger

Do not replace the endpoint-change Trend with a current-minus-trailing-average formulation at this stage.

The current evidence supports:

```text
6M endpoint Trend
→ broad enough to remain distinct from Recent Move
→ preferred to 9M / 12M because the longer horizons add inertia
→ retains economically useful broad-vs-recent disagreement

remaining State issue
→ boundary stability
→ addressed more directly by hysteresis than by changing Trend semantics
```

If the Human Trend / Core Review Gate finds a material residual contradiction that hysteresis does not resolve, the Trend measurement itself may be reopened under a separate explicitly scoped task.

Do not launch an MA-reference comparison merely because the formulation is familiar from technical analysis.

---

# 12. Human Trend / Core Review Gate

The next step is human review.

Do not automatically proceed to Macro Adjustment.

The current candidate package for review is:

```text
Representative tenors
Short        → 6M
Intermediate → 10Y
Long         → 30Y

Trend Value
→ M5(t) - M5(t-126)

Trend State Classification
→ common directional entry threshold ±25 bp
→ 5 bp hysteresis band
→ directional exit through ±20 bp

Recent Move
→ M5(t) - M5(t-21)
→ ±10 bp working threshold
→ unchanged in the Trend review

Endpoint smoothing
→ 5 valid observations
→ unchanged

Core Rule Mapping
→ settled cells retained
→ provisional / unresolved mixed cells remain subject to human review
```

Required review output:

```text
Accepted / rejected Trend Value definition
Accepted / rejected common ±25 bp directional entry threshold
Accepted / rejected 5 bp hysteresis stabilization
Recent Move definition status
Recommended Core Rule Table
Remaining provisional / unresolved Core cells
Material historical contradictions
Need to reopen Trend measurement: yes / no
Need to reopen Recent Move or smoothing: yes / no
```

The human review must distinguish:

```text
Component-level adequacy
```

from:

```text
whether a particular downstream ETF exposure receives a preferred Core score
```

Downstream behavior may expose a Component problem, but must not become the calibration target for the Component.

If Trend measurement itself must be reopened, possible challengers may include MA-based constructions, but only under a separate explicitly scoped task.

---

# 13. Task 3 — Macro Adjustment Validation

Task 3 begins only after the Human Trend / Core Review Gate accepts the required Core inputs.

Its fixed inputs are the accepted:

```text
representative tenors
Recent Move definition
Trend Value definition
Trend State Classification / stabilization
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

# 14. Deliverables and Artifact Status

## Completed Task 1

```text
validation/261002_duration/task1_core/analysis.py
validation/261002_duration/task1_core/results.csv
validation/261002_duration/task1_core/report.md
```

## Completed initial Task 2

```text
validation/261002_duration/task2_trend/analysis.py
validation/261002_duration/task2_trend/comparison.csv
validation/261002_duration/task2_trend/report.md
```

These artifacts retain the original 3M-preference analysis for historical traceability. That preference is superseded by the later horizon review.

## Completed horizon re-review

The human-review notebook is:

```text
bondview_duration_trend_horizon_6m_9m_12m_review.ipynb
```

This notebook is the current supporting artifact for the 6M / 9M / 12M horizon decision.

The older:

```text
bondview_duration_2022_10y_trend_visual_check.ipynb
```

is tied to the superseded 3M Trend interpretation and should not be used as current design evidence without that qualification.

## Corrected 6M State-stabilization review

The corrected stabilization review has been completed against the frozen Task-1 6M baseline.

If this review is formalized in the repository, use the existing validation campaign:

```text
validation/261002_duration/
```

with a suitable subdirectory such as:

```text
validation/261002_duration/task2b_trend_state/
```

Expected reproducibility artifacts should include:

```text
analysis.py
comparison.csv
report.md
```

An inspection notebook may also be retained as a human-review companion, but the report should contain the actual economic interpretation and recommendation rather than relying on notebook outputs alone.

Do not treat generated artifacts as design authority until the Human Trend / Core Review Gate accepts the corresponding conclusion.

## Trend / Core Review Gate

After human acceptance, record the accepted conclusion in:

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

# 15. Explicit Non-Goals

Codex must not:

- redesign Bondview system architecture;
- optimize scores, tenors, horizons, thresholds, persistence, hysteresis, or smoothing by forward returns;
- treat historical events as supervised target labels;
- infer cardinal utility from ordinal scores;
- reintroduce preferred-duration / distance scoring;
- introduce an ETF-independent authoritative Duration preference;
- redesign the ETF exposure taxonomy during this validation;
- design Curve Evaluation;
- force Duration and Curve to use disjoint observations;
- treat lower mixed-state frequency as inherently better;
- infer that more or fewer Stable observations are inherently better;
- treat fewer State transitions as inherently better;
- choose a Component threshold or stabilization rule because it improves downstream ETF Core scores;
- automatically replace Trend with a current-minus-moving-average technical indicator;
- blur Direction information with Rates Valuation merely to improve transition behavior;
- alter endpoint smoothing during the current Trend review unless explicitly instructed;
- alter Recent Move during the current Trend review unless explicitly instructed;
- automatically proceed to Macro Adjustment before the Human Trend / Core Review Gate is accepted.

The objective is to establish an interpretable and economically coherent Duration Evaluation design, not to maximize predictive fit or produce the smoothest historical State sequence.
