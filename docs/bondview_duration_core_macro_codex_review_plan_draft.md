# Bondview Duration Core/Macro Review — Codex Work Plan (Revised Draft)

## 1. Purpose

This document defines a temporary Codex work plan for reviewing the current Duration design.

This is **not an MVP specification**, not a production implementation plan, and not a finalized Duration model contract.

Its purpose is to review how the existing Duration market Components and ETF Duration Exposure should produce an exposure-specific Core Evaluation Result, and how the existing provisional Macro Adjustment should interact with that result.

The review should begin from the complete Core Evaluation representation:

```text
Long-End Yield Trend State
        +
Recent Long-End Yield Move State
        +
Duration Exposure
        ↓
Core Evaluation
        ↓
Core Evaluation Result
```

A simpler one-dimensional duration-preference model may be used to generate provisional baseline values, but it should not replace the complete representation or erase economically relevant differences among the original market Rule Cases.

The work should minimize unnecessary case-by-case design while preserving the full market-state information required by the architecture.

---

## 2. Reference Basis

Use the current `main` branch of `lbk209/bondview-v2` as the reference basis.

Primary references:

- `docs/bondview_system_architecture.md`
- `docs/bondview_vocabulary.md`
- `docs/bondview_stance_design_draft.md`
- `bondview_duration_horizon_rulecase_prototype.ipynb`

`docs/bondview_system_architecture.md` and `docs/bondview_vocabulary.md` are authoritative for architecture and terminology.

`docs/bondview_stance_design_draft.md` may be used only as a source of provisional rule content. Its terminology and older structure are not authoritative.

The current architecture requires Core Evaluation to be exposure-specific:

```text
Components for Core Evaluation
        ↓
[Core Evaluation] <──────────────── ETF Exposure Profile
        ↓
Core Evaluation Result
        ↓
[Macro Adjustment, where applicable] <── Macroeconomic Components
        ↓
Constituent Evaluation Result
```

The architecture does not require an intermediate `market duration preference`. If such an intermediate result is used in this review, it is only a provisional internal calculation device.

---

## 3. Existing Market Rule Cases

The existing Duration prototype uses:

```text
Long-End Yield Trend State
        ×
Recent Long-End Yield Move State
        ↓
9 market Rule Cases
```

with the current provisional mapping:

| Trend \ Recent Move | Falling | Stable | Rising |
|---|---:|---:|---:|
| Falling | +3 | +2 | +1 |
| Stable | +1 | 0 | -1 |
| Rising | -1 | -2 | -3 |

The seven-level result may be interpreted provisionally as an ordered directional duration preference:

```text
+3  strongly favor longer duration
+2  favor longer duration
+1  mildly favor longer duration
 0  neutral / middle duration
-1  mildly favor shorter duration
-2  favor shorter duration
-3  strongly favor shorter duration
```

For this review, the existing Trend / Recent Move calculations and the 3 × 3 Rule Table should remain fixed unless a concrete inconsistency is found.

This seven-level mapping is not itself the final Core Evaluation Result.

---

## 4. Synthetic Duration Exposures

Use four ordered synthetic exposure classes:

```text
Short
Intermediate
Long
Very Long
```

These are analytical fixtures, not real ETF definitions.

For the provisional baseline calculation, represent them as equally spaced positions:

```text
Short          = -1.5
Intermediate   = -0.5
Long           = +0.5
Very Long      = +1.5
```

Map the seven directional preference levels to preferred positions:

```text
-3 → -1.5
-2 → -1.0
-1 → -0.5
 0 →  0.0
+1 → +0.5
+2 → +1.0
+3 → +1.5
```

These positions are only a simple device for generating provisional Core values.

They do not imply that real ETF effective durations are equally spaced.

---

## 5. Provisional Core Evaluation Baseline

The initial Core values should be generated from the distance between:

```text
preferred duration position
        and
synthetic exposure position
```

This produces the following provisional seven-level exposure table:

| Directional Preference | Short | Intermediate | Long | Very Long |
|---:|---:|---:|---:|---:|
| **+3** | -3 | -1 | +1 | **+3** |
| **+2** | -2 | 0 | **+2** | **+2** |
| **+1** | -1 | +1 | **+3** | +1 |
| **0** | 0 | **+2** | **+2** | 0 |
| **-1** | +1 | **+3** | +1 | -1 |
| **-2** | **+2** | **+2** | 0 | -2 |
| **-3** | **+3** | +1 | -1 | -3 |

For this review, the Core score should be interpreted as the **exposure-specific result produced under the current Duration market conditions**.

A provisional descriptive scale is:

```text
+3  strongly favorable for this exposure within Duration Evaluation
+2  favorable
+1  mildly favorable
 0  neutral
-1  mildly unfavorable
-2  unfavorable
-3  strongly unfavorable
```

This is local to the Duration constituent.

For example:

```text
Directional preference = -3
Short exposure → Core result = +3
```

does **not** mean that Short Duration is absolutely preferable to cash, deposits, or other asset classes. It means that Short is strongly favorable within the Duration evaluation under those market conditions.

The eventual ETF-level judgment depends on the other Constituent Evaluation Results and later ETF Evaluation stages.

---

## 6. Complete 9 × 4 Core Representation

The Codex review should work from the complete 9 market Rule Cases × 4 exposure classes.

The simpler directional-preference model should only provide the provisional baseline values.

| Trend | Recent Move | Provisional Directional Preference | Short | Intermediate | Long | Very Long | Review Status |
|---|---|---:|---:|---:|---:|---:|---|
| Falling | Falling | +3 | -3 | -1 | +1 | +3 | Accept baseline ordering |
| Falling | Stable | +2 | -2 | 0 | +2 | +2 | Check tie / intensity |
| Falling | Rising | +1 | -1? | +1? | +3? | +1? | Review |
| Stable | Falling | +1 | -1? | +1? | +3? | +1? | Review |
| Stable | Stable | 0 | 0? | +2? | +2? | 0? | Review neutral meaning |
| Stable | Rising | -1 | +1? | +3? | +1? | -1? | Review |
| Rising | Falling | -1 | +1? | +3? | +1? | -1? | Review |
| Rising | Stable | -2 | +2 | +2 | 0 | -2 | Check tie / intensity |
| Rising | Rising | -3 | +3 | +1 | -1 | -3 | Accept baseline ordering |

`?` means that the provisional one-dimensional mapping supplies a usable starting value, but the complete Rule Case should be reviewed before the value is accepted.

The goal is not to redesign all 36 cells independently.

---

## 7. Core Review Priorities

### 7.1 Strong directional cases: `±3`

These are the clearest cases because Trend and Recent Move point in the same direction.

Expected ordering:

```text
Falling × Falling:
Very Long > Long > Intermediate > Short
```

```text
Rising × Rising:
Short > Intermediate > Long > Very Long
```

The ordering can be accepted provisionally unless a concrete economic objection appears.

The exact score spacing is still provisional.

### 7.2 `±2` cases

Each `±2` preference corresponds to only one original market Rule Case:

```text
Falling × Stable → +2
Rising × Stable  → -2
```

There is therefore no loss of distinction from compressing multiple market Rule Cases into the same preference level.

The main item to review is the provisional tie:

```text
+2 → Long = Very Long
-2 → Short = Intermediate
```

Codex should preserve the tie as the baseline and flag it for review rather than silently resolving it.

### 7.3 `±1` cases — highest priority

These are the main cases where the provisional one-dimensional preference may compress economically different market conditions.

For `+1`:

```text
Falling Trend × Rising Recent Move
Stable Trend  × Falling Recent Move
```

For `-1`:

```text
Stable Trend × Rising Recent Move
Rising Trend × Falling Recent Move
```

The review should ask whether the paired Rule Cases really deserve identical exposure-specific results.

For example:

```text
Falling Trend × Rising Recent Move
```

may represent a favorable underlying trend with an adverse recent reversal, while:

```text
Stable Trend × Falling Recent Move
```

may represent a neutral underlying trend with a favorable recent move.

If that distinction matters economically, the complete 9 × 4 Core representation should preserve it instead of forcing both rows to share the same values.

### 7.4 Neutral case: `0`

Only:

```text
Stable Trend × Stable Recent Move
```

maps to `0`.

There is no information-loss problem here.

The open question is semantic:

> Does neutral mean a middle-duration preference, or does it mean that Duration provides no reason to distinguish among exposures?

The provisional baseline assumes:

```text
Short          0
Intermediate  +2
Long          +2
Very Long      0
```

because `0` is treated as a middle-duration preference.

If neutral instead means "no duration information," a flatter row may be more appropriate.

This should be reviewed explicitly.

---

## 8. Structural Checks

Before historical replay, Codex should verify that the provisional Core matrix satisfies the intended structural properties.

### 8.1 Strong-signal ordering

Confirm that the extreme market Rule Cases rank the exposure spectrum in the expected direction.

### 8.2 Smooth movement

As market conditions move from strongly shorter-duration-favorable to strongly longer-duration-favorable, the preferred exposure should move progressively across:

```text
Short → Intermediate → Long → Very Long
```

unless a specific original Rule Case justifies an exception.

### 8.3 Exposure-column behavior

For a fixed exposure:

- Very Long should generally improve as market conditions move longer-duration-favorable;
- Short should generally improve as conditions move shorter-duration-favorable;
- Intermediate and Long should be strongest around nearby market conditions.

### 8.4 Symmetry

The provisional baseline is symmetric.

Examples:

```text
(Falling × Falling, Very Long)
≈
(Rising × Rising, Short)
```

and:

```text
(Falling × Falling, Short)
≈
(Rising × Rising, Very Long)
```

Symmetry should remain the default unless an economic reason justifies asymmetry.

### 8.5 Information-loss check

For every preference level shared by more than one original Rule Case, inspect whether the original Trend / Recent Move distinction matters for the exposure-specific result.

In the current table, this mainly concerns `±1`.

---

## 9. Macro Adjustment

### 9.1 Existing macro Rule Table

For the initial review, reuse the current provisional Inflation Trend × Policy Direction mapping as a fixed test fixture.

Current actions include:

```text
pass-through
cap positive at +2
cap positive at +1
cap negative at -2
cap negative at -1
```

Codex should not optimize or redesign these actions during the initial run.

### 9.2 Apply caps to directional preference, not directly to Core score

The old caps were defined against a directional Duration scale.

Therefore Macro Adjustment should initially operate on the directional preference:

```text
directional preference
        +
macro Rule Case
        ↓
macro action
        ↓
macro-adjusted directional preference
```

Then the same exposure-specific Core mapping should be applied again:

```text
macro-adjusted directional preference
        +
Duration Exposure
        ↓
Duration Evaluation Result
```

Do not directly apply:

```text
cap positive at +1
```

to an exposure-specific Core score merely because that Core score is positive.

A positive Core result means "favorable for this exposure within Duration Evaluation," not "favor longer duration."

### 9.3 Provisional nature of the macro factorization

The architecture does not require an intermediate directional preference.

This review uses it because it provides a simple way to retain the existing macro-cap semantics.

If the complete 9 × 4 Core review reveals that original Rule Case information must survive beyond the directional preference, Macro Adjustment may need to work from a richer Core Result Contract.

Do not assume that the provisional factorization is final.

---

## 10. Double-Counting Review

The same exposure or related variables appearing in more than one stage is not automatically double counting.

The relevant issue is whether the **same economic mechanism** is counted more than once.

Example:

```text
Tightening policy
        ↓
rising long-end yields
        ↓
Core penalizes long-duration exposure
```

followed by:

```text
Tightening policy
        ↓
Macro adds another strong long-duration constraint
```

may partly represent the same policy-transmission mechanism twice.

This does not prove that Macro Adjustment is invalid. Long-end yields can also reflect inflation expectations, term premium, supply, and other forces.

The review should therefore check whether Macro Adjustment acts mainly as a bounded constraint rather than as a second full directional model that mechanically repeats the rates signal.

---

## 11. Codex Review Sequence

### A. Reproduce the 9 market Rule Cases

Required fields:

```text
trend_state
recent_move_state
market_rule_case
provisional_directional_preference
```

### B. Generate the complete 9 × 4 Core table

Use the provisional preference / exposure-distance rule only to seed baseline values.

Required fields:

```text
trend_state
recent_move_state
market_rule_case
provisional_directional_preference
exposure_class
exposure_position
baseline_core_result
review_status
```

Required outputs:

1. full 36-case table;
2. compact 9 × 4 matrix;
3. list of rows requiring substantive review;
4. structural diagnostics.

### C. Review flagged Core cases

Priority order:

1. two `+1` Rule Cases;
2. two `-1` Rule Cases;
3. neutral `0` Rule Case;
4. `±2` tie / intensity questions.

Codex should not invent revised values.

It should display the baseline values, relevant original Rule Case, and the reason the row is flagged.

Economic revisions should be made only after review.

### D. Apply Macro Adjustment

Using the accepted or still-provisional Core mapping:

1. apply the fixed macro action to the directional preference;
2. obtain the macro-adjusted preference;
3. map the same exposure under that adjusted preference;
4. retain all intermediate values.

Required fields:

```text
trend_state
recent_move_state
market_rule_case
directional_preference
exposure_class
core_evaluation_result
inflation_state
policy_state
macro_rule_case
macro_action
macro_adjusted_directional_preference
duration_evaluation_result
```

The composed cases are implementation and interaction checks.

Do not treat all combinations as independent economic-design decisions.

---

## 12. Summary Diagnostics

### 12.1 Core diagnostics

At minimum report:

- preferred exposure(s) by original market Rule Case;
- rows that exactly preserve the provisional baseline;
- rows flagged for review;
- monotonicity violations;
- symmetry violations;
- ties by Rule Case;
- Core-score distribution by exposure;
- whether the `±1` paired Rule Cases remain identical or are intentionally differentiated;
- whether the neutral row retains a middle-duration interpretation.

### 12.2 Macro diagnostics

At minimum report:

- frequency of each macro action;
- pass-through frequency;
- average and maximum change in directional preference;
- resulting change in Duration Evaluation Result;
- cases where macro adjustment changes the preferred exposure;
- cases where previously distinct exposure results collapse;
- potential excessive compression or amplification;
- possible examples of economic double counting.

These diagnostics are review aids, not optimization targets.

---

## 13. Historical Replay

After the structural Core review and macro application are implemented, replay selected historical dates from prior Duration work.

Candidate dates:

```text
2019-08-30
2020-03-31
2021-12-30
2022-10-31
2023-10-31
2024-09-30
```

For each date:

```text
historical Trend State
+
historical Recent Move State
        ↓
original market Rule Case
        ↓
Core Evaluation across four exposures

historical Inflation State
+
historical Policy Direction
        ↓
macro action
        ↓
Duration Evaluation Result across four exposures
```

Required historical comparison:

| `as_of` | Market Rule Case | Macro Rule Case | Short | Intermediate | Long | Very Long |
|---|---|---|---:|---:|---:|---:|
| 2019-08-30 | | | | | | |
| 2020-03-31 | | | | | | |
| 2021-12-30 | | | | | | |
| 2022-10-31 | | | | | | |
| 2023-10-31 | | | | | | |
| 2024-09-30 | | | | | | |

Each result should remain traceable through:

```text
market Rule Case
→ provisional directional preference
→ exposure-specific Core Evaluation Result
→ macro action
→ macro-adjusted preference
→ Duration Evaluation Result
```

Historical replay is an interpretive check.

Do not optimize the Core mapping or Macro Adjustment to fit these dates.

---

## 14. Questions to Answer from the Review

The initial Codex work should help answer:

### 1. Full Core representation

Can the complete 9 × 4 Core Evaluation be represented coherently without designing 36 independent rules?

### 2. Compression validity

Do the two `+1` Rule Cases and the two `-1` Rule Cases really deserve identical exposure-specific results?

### 3. Neutral meaning

Does `Stable × Stable` imply a middle-duration preference or no duration preference?

### 4. Tie / intensity behavior

Are the provisional `±2` ties economically acceptable?

### 5. Macro semantics

Does applying the existing caps to the directional preference preserve their intended economic meaning?

### 6. Macro strength

Do the caps behave as a bounded modifier, or do they excessively compress or amplify the Core evaluation?

### 7. Double counting

Do synthetic or historical cases reveal obvious duplication between realized rates behavior and macro constraints?

---

## 15. Codex Deliverables

Preferred outputs:

```text
duration_core_macro_review.ipynb
duration_core_cases.csv
duration_macro_cases.csv
duration_historical_replay.csv
duration_core_macro_review_summary.md
```

### Notebook

Should:

- reuse existing market calculations where practical;
- reproduce the 9 original market Rule Cases;
- implement the provisional directional-preference baseline;
- generate the complete 9 × 4 Core representation;
- clearly flag rows requiring review;
- preserve any reviewed overrides separately from baseline values;
- apply the existing macro-cap table to directional preference;
- recompute Duration Evaluation Results;
- generate structural diagnostics;
- replay selected historical dates.

### CSV outputs

Keep Core, Macro, and historical results separate.

Preserve both baseline and reviewed values if any Core rows are later changed.

### Summary Markdown

Should report:

- assumptions used;
- complete 9 × 4 Core matrix;
- rows accepted from the provisional baseline;
- rows requiring review;
- any reviewed overrides and their rationale;
- structural findings;
- macro-cap behavior;
- possible double-counting cases;
- historical observations;
- unresolved design questions.

The summary should describe findings rather than automatically finalize the model.

---

## 16. Constraints on Codex

Codex should not:

- add new Raw Observations;
- add new Treasury maturities;
- redesign Trend or Recent Move Components;
- change the existing 3 × 3 market Rule Table;
- silently replace the complete 9 × 4 representation with the one-dimensional preference model;
- invent revised values for flagged Core rows;
- optimize against historical cases;
- redesign the macro Rule Table during the initial run;
- create generalized evaluator abstractions;
- refactor unrelated project code;
- treat this work as an MVP implementation.

If an inconsistency appears, report it rather than silently modifying the design.

---

## 17. Open Decisions for the Next Review

The revised plan intentionally narrows the unresolved questions to:

1. whether the two `+1` Rule Cases require different exposure-specific Core results;
2. whether the two `-1` Rule Cases require different exposure-specific Core results;
3. whether `Stable × Stable` means middle-duration preference or no duration information;
4. whether the `±2` baseline ties should remain;
5. whether the existing macro caps remain economically plausible after the complete Core representation is used;
6. whether any concrete case shows that the provisional directional-preference factorization loses information required by Macro Adjustment.

These questions should be reviewed before formal Duration design documents are changed.
