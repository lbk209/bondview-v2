# Bondview Duration Design Validation — Codex Work Plan

## 1. Purpose

This document defines a temporary Codex work plan for validating the current Bondview **Duration Evaluation** design.

It is intentionally narrower than a general Duration design document. The system architecture and vocabulary are already authoritative; this plan exists only to test lower-level Duration choices that benefit from historical calculation and structured diagnostics.

This plan does **not** ask Codex to redesign Bondview or optimize a predictive model.

The work is organized into three tasks:

```text
Task 1
Historical validation of the proposed Core Duration mapping
        ↓
Task 2
Robustness of Trend definition
        ↓
Human review / acceptance
        ↓
Task 3
Macro Adjustment validation
```

The order is deliberate.

The Core mapping is the more important economic question, so it is reviewed first using a simple provisional Trend definition. Trend length and the possible separation of Trend and Recent Move windows are then tested as robustness questions. Macro Adjustment is evaluated only after the Core design has been reviewed.

---

# 2. Reference Basis and Fixed Constraints

Use the `update_duration` branch of:

```text
lbk209/bondview-v2
```

Authoritative references:

- `docs/bondview_system_architecture.md`
- `docs/bondview_vocabulary.md`

Older Duration documents, notebooks, and previous Codex outputs may be reused only when they provide calculations or historical information compatible with the current design.

Do not treat earlier Duration design documents as authoritative.

The following are fixed for this work:

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

The `-3 ... +3` result scale is ordinal:

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

Do not reintroduce:

- an ETF-independent market-derived Duration preference as the authoritative Core result;
- distance-to-preferred-duration scoring;
- cardinal arithmetic on the ordinal scale;
- Macro Adjustment before exposure enters Core Evaluation;
- Stance terminology as part of the current Duration path;
- artificial orthogonality between Duration and Curve.

---

# 3. Fixed Starting Exposure Design

For this validation run, use three synthetic Duration Exposure categories:

```text
Short
Intermediate
Long
```

The initial representative exposures are:

```text
Short
→ economic anchor: U.S. Treasury 0–1Y exposure
→ representative Treasury tenor: approximately 6M

Intermediate
→ economic anchor: approximately 10Y Treasury exposure
→ representative Treasury tenor: 10Y

Long
→ economic anchor: approximately 30Y Treasury exposure
→ representative Treasury tenor: 30Y
```

The Short anchor is intended to represent a Korean-listed U.S. short-Treasury ETF with approximately 0–1Y exposure. Additional short-end categories such as ultra-short or 1–3Y should be considered later only if the intended ETF universe requires a materially distinct Duration Exposure.

The general rule remains:

> The representative tenor should follow the economic center of the Duration Exposure.

The exposure taxonomy may later expand if a materially important ETF cluster cannot be represented cleanly by `Short / Intermediate / Long`. That universe-design question is outside the current Codex run.

---

# 4. Trend and Recent Move Semantics

The intended economic roles are:

```text
Yield Trend
→ broader / established rates condition

Recent Yield Move
→ shorter-horizon behavior that confirms, pauses,
   or challenges that broader condition
```

Recent Move is not a forecast of a future Trend State.

The important design issue is that there are two plausible ways to construct Trend.

## 4.1 Conventional overlapping construction

A conventional trailing Trend includes the latest observations:

```text
6M Trend
→ t-6m → t

Recent Move
→ t-1m → t
```

This is familiar and simple, but the latest month is mechanically embedded inside Trend.

## 4.2 Semantically separated construction

A Bondview-specific alternative is to exclude the latest Recent-Move window from Trend:

```text
6M established Trend
→ t-7m → t-1m

Recent Move
→ t-1m → t
```

This is **not** presented as a universal bond-market convention.

Its purpose is semantic separation:

```text
Trend
→ condition established before the most recent move

Recent Move
→ what happened most recently relative to that condition
```

This may make a Rule Case such as:

```text
Trend = Falling
Recent Move = Rising
```

more interpretable as:

> a previously established falling-yield condition is currently being challenged by the latest month's rise.

However, this construction should not be adopted solely because it is conceptually elegant. It will be tested in **Task 2** together with the Trend-horizon choice.

---

# 5. Provisional Signal Definition for Task 1

Task 1 needs one fixed baseline so that the Core mapping can be reviewed before secondary signal-definition choices are introduced.

Use:

```text
Recent Move
→ latest 1 month

Trend
→ conventional trailing 6 months including the latest month
```

This is a **provisional reference definition**, not the final approved Trend design.

The reason for using it in Task 1 is practical:

- it is conventional and easy to interpret;
- it minimizes new assumptions before the Core mapping is reviewed;
- Task 2 explicitly tests whether a shorter Trend or a non-overlapping construction improves the intended Component semantics.

Any Task-1 conclusion involving the mixed Rule Cases remains provisional until Task 2 confirms that it is robust to the Trend definition.

---

# 6. Core Duration Rule Mapping

The abstract mapping is:

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
Duration Exposure ∈ {Short, Intermediate, Long}
```

## 6.1 Important interpretation of the table

Each row below is a **reusable semantic Rule Case**, not one common Treasury observation applied to every exposure column.

For example:

```text
Falling × Rising / Short
→ uses the 6M Treasury Trend and Recent Move States

Falling × Rising / Intermediate
→ uses the 10Y Treasury Trend and Recent Move States

Falling × Rising / Long
→ uses the 30Y Treasury Trend and Recent Move States
```

At a real `as_of`, the three exposures may therefore occupy different rows.

Example:

```text
same as_of:

6M Treasury
→ Rising × Stable
→ Short uses Rising × Stable row

10Y Treasury
→ Stable × Falling
→ Intermediate uses Stable × Falling row

30Y Treasury
→ Falling × Falling
→ Long uses Falling × Falling row
```

The table defines how each exposure is evaluated **when its own representative tenor is in a given Rule Case**.

> **Trend and Recent Move are exposure-local inputs.** The `Short` column uses States calculated from the 6M Treasury series, `Intermediate` from the 10Y series, and `Long` from the 30Y series. A single `as_of` date may therefore select a different row for each exposure. The rows are reusable semantic mappings, not same-date cross-exposure market states.

## 6.2 Starting mapping

| Trend | Recent Move | Short (6M states) | Intermediate (10Y states) | Long (30Y states) | Status |
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

Do not fill the ranged cells mechanically.

Established constraints are:

```text
Falling × Falling
>
Falling × Stable
>
Falling × Rising
```

and:

```text
Rising × Falling
>
Rising × Stable
>
Rising × Rising
```

for a fixed positive-duration exposure.

For otherwise comparable relevant-tenor conditions:

```text
falling yields
→ greater Duration Exposure should normally receive a stronger favorable effect

rising yields
→ greater Duration Exposure should normally receive a stronger unfavorable effect
```

`Stable × Stable` starts at `0` for all exposures.

Do not reintroduce a hidden assumption that a middle-duration exposure is automatically preferred under neutral rates conditions.

---


# 6A. Ex-Ante Historical Event Set for Task 1

Task 1 should use a small set of **predefined historical event windows** chosen before inspecting Bondview's model outputs.

The purpose is to reduce post-hoc episode selection and to ensure that the Core Duration mapping is tested against economically recognizable Treasury environments.

The event set should contain both:

```text
Anchor events
→ broad Duration interpretation is reasonably clear ex ante

Challenge events
→ economically important transitions where the exact Trend / Recent Move
   configuration is intentionally not predetermined
```

Anchor events test whether the basic sign and exposure-sensitivity logic works.

Challenge events test whether Bondview preserves the distinction between the broader Trend and shorter-horizon Recent Move rather than forcing every important episode into an obvious Rule Case.

The expected behavior below is **qualitative**, not a target score. It should not be used to force a particular `-3 ... +3` category.

| Event window | Historical environment | Type | Ex-ante Duration expectation |
|---|---|---|---|
| 1981-07 to 1981-10 | Volcker tightening / long-rate peak | Anchor | Broadly unfavorable for positive Duration; greater Duration should normally be more penalized under comparable rising-rate conditions. |
| 1987-08 to 1987-10 | Pre-crash rate pressure followed by flight-to-quality rally | Challenge | The sharp recent yield decline should improve the Duration assessment, but the exact broader Trend State is intentionally not predetermined. |
| 1994-02 to 1994-11 | Fed tightening / bond-market selloff | Anchor | Broadly unfavorable, especially for Intermediate and Long exposure. |
| 1998-08 to 1998-10 | Russia / LTCM flight to quality | Anchor | Falling Treasury yields should make Duration favorable; longer exposure should normally benefit more under comparable falling-rate conditions. |
| 2008-09 to 2008-12 | Global financial crisis / Treasury flight to quality | Anchor | Strongly favorable Duration environment, especially for longer exposure. |
| 2013-05 to 2013-09 | Taper tantrum | Anchor | Rising yields should produce unfavorable Duration results, with stronger penalty for greater Duration under comparable conditions. |
| 2020-02 to 2020-03 | COVID Treasury shock | Challenge | Broad yield declines should improve Duration assessment, but the speed and market dislocation make the exact Trend / Recent Move configuration a diagnostic question rather than a predetermined label. |
| 2022-01 to 2022-10 | Inflation / aggressive tightening cycle | Anchor | Clearly unfavorable across positive-duration exposures, with greater Duration normally more penalized. |
| 2023-07 to 2023-10 | Long-end Treasury selloff / term-premium repricing | Challenge | Long exposure should plausibly deteriorate more than Short where long-end conditions weaken materially; cross-tenor divergence is more important than forcing one common market verdict. |

## 6A.1 Use of Event Windows

Codex should evaluate the evolution of States and Core results **within the predefined windows** rather than selecting a single favorable `as_of` after seeing the model output.

The purpose is not to require every day in an event window to match the qualitative expectation.

Instead, the review should ask whether the model's behavior through the window is economically interpretable and whether major transitions are represented coherently.

## 6A.2 Anchor vs Challenge Interpretation

For Anchor events, a material contradiction with the qualitative expectation is evidence that the Core mapping, State Classification, or Component calculation deserves review.

For Challenge events, disagreement is not automatically a failure.

The main questions are:

```text
Does Recent Move respond before the broader Trend where appropriate?

Can different representative tenors occupy different Rule Cases in the same event?

Does the model preserve economically meaningful cross-tenor divergence?

Are transitions interpretable without relying on subsequent returns as target labels?
```

## 6A.3 Supplemental Model-Derived Episodes

In addition to the ex-ante event set, Codex may identify model-derived episodes for diagnostic purposes, especially:

```text
longest Falling × Falling episodes
longest Rising × Rising episodes
mixed Rule Case episodes
long Stable periods
```

These should be labeled as **supplemental diagnostics**, not independent validation cases, because they are selected from the model's own State output.


# 7. Task 1 — Historical Validation of the Core Mapping

## 7.1 Question

> Does the proposed `9 × 3` Core Duration mapping produce economically plausible and internally coherent results when applied to actual historical Treasury conditions?

Task 1 is the primary validation task.

Use the provisional Task-1 signal definition from Section 5:

```text
Recent Move
→ latest 1M

Trend
→ trailing 6M including latest 1M
```

Representative tenors remain:

```text
Short        → 6M
Intermediate → 10Y
Long         → 30Y
```

## 7.2 Analysis A — full-sample structural diagnostics

Over the common historical sample, calculate:

- frequency of each `Trend × Recent Move` Rule Case by representative tenor;
- frequency of each Core score by exposure;
- average and median State persistence;
- Core-result persistence;
- transition counts;
- frequency with which Short / Intermediate / Long receive different Core results at the same `as_of`;
- frequency of the four mixed Rule Cases.

Purpose:

- identify unreachable or extremely rare Rule Cases;
- detect excessive flipping;
- detect pathological concentration in a narrow score range;
- determine whether the mixed cases occur often enough to deserve separate treatment.

These statistics are diagnostics, not optimization targets.

## 7.3 Analysis B — historical-regime review

Use the **ex-ante historical event set in Section 6A** as the primary historical-regime review.

Do not replace those windows with post-hoc periods selected after inspecting Bondview outputs.

For each predefined window, report the State and Core-result evolution for Short, Intermediate, and Long using each exposure's own representative Treasury tenor.

The review should compare actual model behavior with the qualitative ex-ante expectation for Anchor events and should examine transition behavior without forcing a predetermined score for Challenge events.

Supplemental model-derived episodes may be added where useful, but they must be clearly distinguished from the predefined validation set.

Broader stress cases whose significance depends mainly on yield level, valuation, macro response, positioning, or interactions among multiple Constituents should be reserved for later integrated **Exposure Evaluation** diagnostics rather than required here as Duration-specific validation cases.

For every selected `as_of`, show:

```text
Short:
6M yield
Trend Value / State
Recent Move Value / State
Rule Case
Core score

Intermediate:
10Y yield
Trend Value / State
Recent Move Value / State
Rule Case
Core score

Long:
30Y yield
Trend Value / State
Recent Move Value / State
Rule Case
Core score
```

Codex should then evaluate:

1. Does the sign of each result make economic sense?
2. Does exposure sensitivity behave sensibly?
3. Are cross-exposure differences explainable by differences in the corresponding Treasury segments?
4. Are there historical cases that clearly contradict the proposed mapping?

Do not evaluate success by subsequent ETF returns.

## 7.4 Analysis C — mixed Rule Cases

Focus on:

```text
Falling × Rising
Stable  × Falling
Stable  × Rising
Rising  × Falling
```

Use historical **episodes**, rather than treating every consecutive daily observation as an independent example.

For each mixed Rule Case, inspect representative episodes across the 6M, 10Y, and 30Y Treasury series and compare the economically related cases:

```text
Falling × Rising
vs.
Stable × Falling

Stable × Rising
vs.
Rising × Falling
```

The purpose is to determine whether the proposed ordinal interpretation is economically coherent at the time the mixed state occurs, not whether that state predicts the subsequent return.

For each currently ranged cell, Codex should recommend the lower candidate, the higher candidate, or leave the cell unresolved, with a concise economic explanation and representative historical evidence.

Any mixed-case conclusion remains **provisional pending Task 2**, because the frequency and interpretation of mixed states may change under a different Trend definition.

## 7.5 Required Task-1 conclusion

Codex must finish Task 1 with a concise review containing:

```text
Confirmed without change
Recommended Core-mapping changes
Mixed cells that can be provisionally resolved
Still unresolved
Historical cases that contradict the proposed mapping
```

Any resolution of mixed cells is **provisional pending Task 2**.

---

# 8. Task 2 — Trend Definition Robustness

Task 2 begins only after Task 1 has produced a provisional Core mapping.

Its purpose is broader than a simple `6m vs 3m` parameter test.

It tests two separate design dimensions:

```text
A. Trend horizon
   6M vs 3M

B. Window construction
   overlapping vs excluding the latest 1M
```

Recent Move remains fixed at the latest 1 month.

## 8.1 Four Trend variants

Compare:

```text
A. 6M overlapping Trend
   t-6m → t

B. 3M overlapping Trend
   t-3m → t

C. 6M established Trend excluding Recent Move
   t-7m → t-1m

D. 3M established Trend excluding Recent Move
   t-4m → t-1m
```

Use the same State Classification mechanics for all four variants.

Do **not** change thresholds, representative tenors, Recent Move definition, or the provisional Core mapping during this comparison.

The purpose is to isolate the effect of Trend definition.

## 8.2 Why test non-overlapping Trend here

The non-overlapping construction is a deliberate Bondview semantic candidate, not a generic market convention.

It may improve the conceptual relationship:

```text
established Trend
+
latest Recent Move
```

but it may also:

- become too stale;
- create unnecessary discontinuity between the two windows;
- change mixed-case frequency in an undesirable way;
- add complexity without materially improving interpretation.

Therefore it should be judged empirically for **semantic robustness**, not adopted only because it sounds cleaner.

## 8.3 Required diagnostics

For each representative tenor and each of the four Trend variants, report:

- Trend State frequency;
- average and median State persistence;
- transition frequency;
- agreement among the four Trend definitions;
- disagreement-window frequency and duration;
- interaction with Recent Move;
- frequency of each `Trend × Recent Move` Rule Case;
- number and percentage of Core results that differ from the Task-1 baseline;
- historical episodes where the choice materially changes interpretation.

## 8.4 Required analysis

Codex should explicitly answer:

1. Does the 3M Trend become too responsive and begin to duplicate Recent Move?
2. Does the 6M Trend become too stale for Bondview's medium-horizon use?
3. Does excluding the latest 1M materially improve the semantic distinction between Trend and Recent Move?
4. Does the separated construction merely shift or delay Trend without adding interpretive value?
5. Are Task-1 conclusions about strong and mixed Rule Cases robust across reasonable Trend definitions?
6. Which Rule Cases, if any, need to be reopened because their interpretation depends materially on Trend construction?

## 8.5 Required Task-2 conclusion

Codex must recommend one of:

```text
6M overlapping Trend
3M overlapping Trend
6M excluding latest 1M
3M excluding latest 1M
Current Trend concept requires reconsideration
```

The recommendation should be based on:

```text
semantic clarity
+
persistence
+
responsiveness
+
historical plausibility
+
robustness of Task-1 conclusions
```

not predictive performance.

Task 2 should also state:

```text
Task-1 mapping remains robust
```

or identify the exact cells that require another review.

---

# 9. Review Gate

After Tasks 1 and 2, stop and produce a consolidated conclusion.

Do not automatically continue to Macro Adjustment using an unreviewed Codex recommendation.

Required consolidated output:

```text
Recommended representative model definition
Recommended Trend construction / horizon
Recommended completed Core Rule Table
Remaining unresolved Core cells
Material historical contradictions, if any
```

Human review should accept or modify these conclusions before Task 3.

---

# 10. Task 3 — Macro Adjustment Validation

Task 3 is defined now but should be executed only after the Review Gate.

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

Older Inflation × Policy mappings may be reused only as candidate fixtures.

## 10.1 Question

> Does Macro Adjustment add economically useful information to the accepted exposure-specific Core result without materially duplicating rate information already captured by Core?

## 10.2 Ordinal actions

Ordered caps remain permissible:

```text
pass-through
cap positive at +2
cap positive at +1
cap negative at -1
cap negative at -2
```

because they use ordering only.

Do not use operations that assume metric spacing, such as:

```text
score × 0.5
score - 1.5
```

## 10.3 Required diagnostics

Report:

- frequency of each Macro action;
- Core-to-final transition counts;
- sign changes;
- compression of strong Core results;
- historical examples of each non-pass-through action;
- cases where Macro appears clearly incremental;
- cases where Macro appears to overlap substantially with rate information already captured in Core;
- cases that appear materially duplicative.

## 10.4 Required Task-3 conclusion

Codex must recommend:

```text
Retain candidate Macro mapping
Retain with specified changes
Simplify Macro mapping
Reject specific duplicative actions
Macro design remains unresolved
```

with concise economic reasoning.

---

# 11. Required Deliverables

Keep outputs small and review-oriented.

## Task 1

```text
duration_task1_core_validation.md
duration_task1_core_results.csv
```

The Markdown file should contain Codex's analysis and conclusion, not merely raw tables.

## Task 2

```text
duration_task2_trend_robustness.md
duration_task2_trend_comparison.csv
```

Include only plots that materially help compare Trend definitions or important disagreement periods.

## Review Gate

```text
duration_core_validation_conclusion.md
```

This should summarize the recommended model after Tasks 1 and 2.

## Task 3

```text
duration_task3_macro_validation.md
duration_task3_macro_results.csv
```

---

# 12. Explicit Non-Goals

Codex must not:

- redesign Bondview system architecture;
- optimize scores, tenors, or horizons by forward ETF returns;
- fit the Core mapping to historical winners;
- treat historical events as target labels;
- infer cardinal utility from ordinal scores;
- reintroduce the old preferred-duration / distance formula;
- reintroduce an ETF-independent authoritative Duration preference;
- redesign the ETF exposure taxonomy during Tasks 1 or 2;
- design Curve Evaluation;
- force Duration and Curve to use disjoint data;
- automatically proceed to Task 3 before the Task-1 / Task-2 Review Gate is accepted.

---

# 13. Current Working Model

The current provisional model used to begin Task 1 is:

```text
Short
→ 6M Treasury

Intermediate
→ 10Y Treasury

Long
→ 30Y Treasury

Recent Move
→ latest 1M

Trend
→ trailing 6M including latest 1M
   [provisional Task-1 baseline]

representative-tenor Trend
+
representative-tenor Recent Move
+
Duration Exposure
        ↓
Core Duration Evaluation
        ↓
ordinal Core Duration Evaluation Result
```

Task 2 then tests whether Trend should instead be:

```text
3M overlapping
6M excluding latest 1M
3M excluding latest 1M
```

The purpose is to finish the important Core economic design first and then determine whether a different Trend definition materially improves or destabilizes that design.
