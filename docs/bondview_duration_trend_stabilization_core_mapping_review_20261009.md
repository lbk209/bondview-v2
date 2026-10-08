# Bondview v2 — Duration Trend, State Stabilization, and Core Rule Mapping: Design Review

## Document Status and Purpose

**Status:** Review-stage discussion record; **non-authoritative**  
**Reference branch:** `lbk209/bondview-v2`, `update_duration_plan`, inspected at commit `42c6465018e98eb8a8dc8e7ab1c1c7114d55af67`  
**Discussion cutoff:** 2026-10-09  
**Scope:** Duration **Yield Trend** and **Recent Yield Move** semantics, Trend State Classification and stabilization (including the proposed hybrid), and the **Trend-first** principle for ambiguous Core Rule Mapping cells.  
**Purpose:** Preserve the arguments, objections, empirical observations, counterexamples, and unresolved decisions in a form suitable for repeated private review and later editing. This is **not** a replacement for an accepted Duration design contract, implementation specification, or the original validation artifacts.

**Interpretation rule for future editing:** Preserve the distinction between **(1) repository baseline / completed validation, (2) provisional design preference, (3) exploratory discussion and calculations after that validation, and (4) decisions still requiring human acceptance**. Do not turn a diagnostic observation into proof of economic superiority, and do not turn conversational agreement into an accepted design. Retain meaningful objections and negative results rather than polishing them away.

### Why a separate document?

`docs/bondview_component_reuse_stance_design_review.md` examines canonical Component reuse across analytical responsibilities and the meaning of Stance construction. It also uses earlier *Stance*-centered terminology. The present topic is a narrower Duration-specific design review under the current **Bond Analysis → Components → ETF Evaluation / Duration Constituent Evaluation** architecture. Combining the two would obscure both questions and risk importing superseded vocabulary into a current lower-level design.

The relevant canonical or more-specific documents are:

- [`docs/bondview_system_architecture.md`](https://github.com/lbk209/bondview-v2/blob/update_duration_plan/docs/bondview_system_architecture.md) — foundational architecture and responsibility boundaries.
- [`docs/bondview_vocabulary.md`](https://github.com/lbk209/bondview-v2/blob/update_duration_plan/docs/bondview_vocabulary.md) — canonical term meanings.
- [`docs/bondview_exposure_evaluation_design.md`](https://github.com/lbk209/bondview-v2/blob/update_duration_plan/docs/bondview_exposure_evaluation_design.md) — more-specific Exposure / Duration Evaluation design; the accepted Trend definition and Duration Rule Table still have `TBD` placeholders at this reference commit.
- [`docs/bondview_duration_design_validation_codex_plan.md`](https://github.com/lbk209/bondview-v2/blob/update_duration_plan/docs/bondview_duration_design_validation_codex_plan.md) — supporting validation plan and accepted results *within that validation process*, not an override of the architecture.
- [`bondview_duration_trend_6m_stabilization_review.ipynb`](https://github.com/lbk209/bondview-v2/blob/update_duration_plan/bondview_duration_trend_6m_stabilization_review.ipynb) — corrected 6M plain / persistence / hysteresis calculations and initial interpretation.
- [`validation/261002_duration/task1_core/`](https://github.com/lbk209/bondview-v2/tree/update_duration_plan/validation/261002_duration/task1_core) — frozen historical Task-1 results.

The older `docs/bondview_stance_design_draft.md` and Component-reuse review can inform **historical comparison**, but should not silently replace current v2 architecture or the more-specific Exposure Evaluation design. No `docs/working*` file was used as a design source.

---

## 1. Executive Orientation — What Was Actually Discussed?

There were **three interrelated discussions**, not just a choice between hysteresis and persistence:

1. **What Trend means:** the proper horizon and threshold, its difference from Recent Move, the meaning of opposing directions, and the requirement that a Component's classification not depend on downstream ETF preferences.
2. **When a Trend State deserves to change:** plain thresholds versus confirmation by persistence, hysteresis, and a hybrid applying confirmation to entry and hysteresis to exit; whether lower turnover / fewer short episodes is a legitimate criterion.
3. **How Trend should influence Duration Core Rule Mapping:** whether the broader Trend should take priority when mixed Rule Cases have ambiguous ordinal scores, how that interacts with the seven-level scale and settled cells, and why many historical checks can be *diagnostics* without the power to refute that economic judgment.

These topics are connected but must be resolved at **different architectural boundaries**:

```text
Accepted Treasury Raw Observations
       ↓
Feature / Component Value calculation
       ↓
Yield Trend Component State Classification  ← persistence / hysteresis / hybrid
       +
Recent Yield Move Component State
       ↓
Duration Core Rule Case × ETF Duration Exposure
       ↓
Duration Core Rule Mapping                  ← Trend-first ambiguity principle
       ↓
Core Duration Evaluation Result
       ↓
Macro Adjustment and later ETF-level steps
```

The Trend State Classification is **consumer-independent**; the Core Rule Mapping is **exposure-specific**. Trading turnover is ultimately downstream of both.

**Current status in one sentence:** the 6M overlapping Trend and common ±25 bp directional threshold remain provisional working choices; the branch records 5 bp hysteresis as its provisional stabilization favorite, but subsequent discussions reopened Persistence-3 and introduced the serious hybrid challenger; Trend-first remains a proposed mapping principle rather than an accepted mapping contract.

---

## 2. Baseline, Definitions, and Design Boundaries

### 2.1 The current historical fixture

For each representative Treasury tenor, let `M5(t)` denote the mean of the **five accepted valid yield observations ending at observation t** (not an arbitrary calendar-day window). The current working calculations are:

```text
Yield Trend Value   = M5(t) − M5(t−126)    # approximately 6M
Recent Move Value  = M5(t) − M5(t−21)     # approximately 1M
```

The endpoint smoothing is already contained in `M5`; it is distinct from temporal State stabilization. The two measures overlap by construction, but that does not make their economic roles identical.

Plain classification:

| Component | Falling | Stable | Rising |
|---|---|---|---|
| Yield Trend | `< −25 bp` | `−25 to +25 bp`, inclusive | `> +25 bp` |
| Recent Move | `< −10 bp` | `−10 to +10 bp`, inclusive | `> +10 bp` |

Relevant representative tenors and working Duration Exposure categories:

| Exposure | Treasury tenor supplying its Component States |
|---|---|
| Short | 6M |
| Intermediate | 10Y |
| Long | 30Y |

The **six-month duration of the Trend calculation must not be confused with the 6M Treasury tenor**. Every tenor uses the same approximately six-month Trend lookback, but on its own market yields.

The current Core Result uses ordinal categories from `−3` through `+3`. Their gaps do not claim equal utility or expected-return differences.

### 2.2 What is established versus merely provisional?

- **Completed historical baseline:** Task 1 provides 38,330 classified historical observations across the three tenors, with a separate 30Y structural segment where required. Plain ±25 bp classifications were independently reproduced with zero mismatches in the corrected follow-up diagnostics.
- **Provisional Trend definition:** six-month overlapping endpoint change. This superseded an *earlier* provisional 3M preference after a dedicated 6M / 9M / 12M comparison.
- **Provisional threshold:** common ±25 bp for all representative tenors; a slightly different threshold for the 6M tenor was examined but did not justify increasing model complexity at that time.
- **Existing repository stabilization preference:** 5 bp hysteresis, **not** yet accepted as a production rule. The later discussion changes the candidate shortlist, but not the committed branch's official status.
- **Recent Move:** remains a one-month measure with ±10 bp classification; it was not reopened as part of the Trend stabilization question.
- **Duration Core Rule Table:** contains settled, provisional, and unresolved entries in the validation plan; the authoritative lower-level design still leaves the accepted table `TBD`.

### 2.3 Architectural safeguards

A Trend Component State describes a rates condition; it is not itself an ETF attractiveness score. Selecting a Trend threshold specifically because a given Long- or Short-Duration ETF receives a preferred evaluation would breach this separation. A **market-tenor-specific** threshold may be defensible on market-component grounds, but an **ETF-exposure-derived** threshold is not.

Likewise, stabilizing the Trend State *solely to reduce ETF trading turnover* would confound market description with downstream implementation controls. Stability matters only to the extent that it improves the economic description of an established rates condition. Actual trading restraint can be assessed separately downstream.

---

## 3. Why the Six-Month Trend Survived the Horizon Review

The earlier study considered various 3M / 6M overlapping and non-overlapping constructions. A subsequent dedicated horizon review compared 6M, 9M, and 12M **with the same Recent Move, smoothing, and thresholds**.

The retained economic arguments were:

- Even a 6M Trend is already materially slower than the one-month Recent Move; extending it to 9M or 12M is not required merely to establish a different horizon.
- 9M introduced more inertia without showing a sufficiently clear economic improvement; 12M was notably slower during important reversals.
- Fixed ±25 bp thresholds are **not scale-neutral across horizons**: longer endpoint-change periods tend to produce larger magnitudes, automatically changing Stable occupancy.
- An opposing Rule Case is not evidence of failure by itself. For example, 2022's midsummer relief can sensibly be represented as a broadly **Rising** six-month yield Trend with **Falling** Recent Move.

This does **not** prove that every prolonged countertrend case is correctly interpreted, or that the six-month Trend is immune to staleness. It establishes a reasonable working interpretation: **Trend describes the broader directional rates condition; Recent Move confirms, pauses, or challenges it on a shorter horizon**.

An earlier suggestion to use the internal rising/falling *path* of Trend as another explanatory input becomes less compelling when Recent Move already carries shorter-term path information. A path feature should be added only if it contributes a **different economically meaningful distinction**; adding it merely because Trend can be slow risks duplication.

Historical opposing Trend × Recent Move runs lasted from a few observations to several dozen in the frozen Task-1 data. The existence of both short and sustained opposing cases is expected; their *mere frequency* should not be optimized away by design.

---

## 4. Stabilization: What Is the Problem Being Solved?

The plain classification `Rising if Trend > +25` and `Falling if Trend < −25` can flip in response to small boundary crossings even though the calculated Trend spans roughly six months.

**Crucial distinction:** endpoint smoothing over five observations (`M5`) does not solve path-dependent State-classification churn. A six-month *calculation horizon* does not imply a six-month *minimum State duration*.

Three possible objectives must not be conflated:

1. **Reject an unconfirmed new direction** — do not turn a single threshold crossing into a full established State.
2. **Avoid abandoning a confirmed direction for a small retreat** — make exiting a recognized directional State harder.
3. **Reduce State / Core / ETF turnover** — an output consequence that is not by itself evidence of correct Component semantics.

Persistence primarily addresses (1). Hysteresis primarily addresses (2). The hybrid explicitly combines them. Aggregate smoothness often mixes all three.

### 4.1 Pure persistence

With Persistence-`N`, a candidate new State must appear on `N` consecutive valid observations before replacing the active State. Pending confirmation, the old State remains active. This applies to **all** transitions, including direction → Stable and Stable → direction.

For Persistence-3, a continuously sustained newly classified State is typically recognized two valid observations after plain classification. This delay is **not necessarily material** for a six-month Trend. It is predictable and bounded when the candidate persists.

Strengths: transparent temporal confirmation; rejects one-day excursions; typically limits retention of an old directional State into a sustained plain-Stable run to two observations.

Weaknesses: delays economically genuine entries and exits; repeated short interruptions can prevent confirmation; confirmation count itself is another path dependency.

### 4.2 Pure hysteresis

For 5 bp hysteresis:

```text
Stable → Rising    when Trend > +25 bp
Rising → Stable    when Trend ≤ +20 bp
Stable → Falling   when Trend < −25 bp
Falling → Stable   when Trend ≥ −20 bp
```

The branch's original pure hysteresis allows direct reversal from Rising to Falling if Trend crosses below −25 bp, and vice versa, without first requiring a Stable observation.

Strengths: immediate entry when the threshold is crossed; prevents minor retreats through ±25 bp from terminating an established direction; materially reduces short boundary episodes.

Weaknesses: a single threshold crossing can establish a direction that continues to be reported while plain Trend is Stable. This is intentional **path dependence**, not a computational bug.

For example, the two sequences `26 → 24 → 24 → 19` and `24 → 24 → 24 → 19` can yield different States under hysteresis because the first briefly crossed the entry boundary while the second never did. That discrepancy is semantically defensible only if prior establishment of the direction genuinely matters.

### 4.3 Original corrected full-sample comparison (committed notebook)

A *short directional episode* is a consecutive Rising/Falling State run lasting five valid observations or fewer. The following table reproduces the corrected report in the `update_duration_plan` branch:

| Tenor | Method | Short directional episodes ≤5 (%) | Transition rate (%) | Stable occupancy (%) | Changed from plain (%) |
|---|---|---:|---:|---:|---:|
| 6M | Plain | 29.35 | 1.63 | 38.86 | 0.00 |
| 6M | Persistence-2 | 23.53 | 1.50 | 38.86 | 1.57 |
| 6M | Persistence-3 | 17.57 | 1.28 | 38.81 | 2.87 |
| 6M | Hysteresis-5 bp | 10.61 | 1.17 | 36.89 | 1.97 |
| 10Y | Plain | 23.48 | 2.86 | 31.14 | 0.00 |
| 10Y | Persistence-2 | 16.83 | 2.59 | 31.21 | 2.72 |
| 10Y | Persistence-3 | 14.65 | 2.44 | 31.19 | 5.20 |
| 10Y | Hysteresis-5 bp | 11.79 | 2.43 | 28.63 | 2.51 |
| 30Y | Plain | 24.10 | 2.96 | 28.72 | 0.00 |
| 30Y | Persistence-2 | 19.21 | 2.69 | 28.75 | 2.83 |
| 30Y | Persistence-3 | 11.03 | 2.42 | 28.78 | 5.26 |
| 30Y | Hysteresis-5 bp | 10.85 | 2.30 | 25.72 | 3.01 |

Also tested: Hysteresis-10 bp, which yields still lower short-episode and transition rates but materially greater stickiness and less Stable occupancy; it is not the main finalist.

**Important correction to our earlier interpretation:** 5 bp hysteresis looks better on short-episode frequency, but this metric is partially **endogenous to the stabilization rule**. Persistence can remove a short episode by never admitting it; hysteresis can lengthen an episode beyond five observations by refusing to exit. Neither effect alone establishes better economic classification. Nor is Persistence-3's two-observation entry delay sufficient, by itself, to reject persistence for a six-month Trend.

### 4.4 Additional transition-lag and inherited-State diagnostics (exploratory follow-up)

A follow-up discussion inspected the same frozen historical data using *sustained plain State episodes* (at least 10 or 21 valid observations). The 21-observation benchmark is a retrospective diagnostic, **not a truth label or training target**.

- Persistence-2 typically confirms a sustained change after 1 additional valid observation; Persistence-3 after 2.
- Hysteresis-5 recognizes **new plain directional entry** at once if it was Stable just beforehand. However, sometimes it already holds that directional State through the preceding plain-Stable spell; such cases must not be mislabeled as newly recognized zero-delay entries.
- When **exiting** an established direction, hysteresis delays vary rather than being fixed. For 21-observation sustained plain-Stable exits, mean delays were approximately 2.52 / 1.92 / 1.59 observations for 6M / 10Y / 30Y.
- With 5 bp hysteresis, consecutive stretches of *directional State while plain classification says Stable* had the following duration distributions:

| Tenor | Count of carryover runs | Median valid observations | P90 | Maximum |
|---|---:|---:|---:|---:|
| 6M | 77 | 2 | 6 | 13 |
| 10Y | 190 | 1 | 4 | 11 |
| 30Y | 148 | 1 | 5 | 9 |

In a few historical cases a plain-Stable spell of 10–11 observations was never recognized as Stable by hysteresis. This is a real and informative **path-dependence counterexample** to any claim that hysteresis simply behaves like persistence with faster entries. It is **not** conclusive evidence that hysteresis was economically wrong; that would require an independent criterion for what the established market direction was.

These follow-up figures were exploratory calculations within the discussion, **not accepted results published into the repository's authoritative Duration design**. They should be rerun from a retained notebook or script before promotion into an authoritative document.

---

## 5. Hybrid: Entry Persistence + Exit Hysteresis

### 5.1 Motivation and conceptual defense

The proposed hybrid uses different evidence standards for different transitions:

> **Do not recognize a new direction without repeated confirmation; once it has been confirmed, do not withdraw it merely because Trend retreats slightly back inside the original threshold.**

This is an asymmetric model of an *established directional condition*. It is logically defensible because the evidentiary question at entry differs from the question at exit. It is **not automatically superior**: the hybrid may accumulate both confirmation lag and hysteresis path dependence.

The two principal candidates are:

```text
Hybrid-P2/H5: 2-observation confirmation at entry, 5 bp exit band
Hybrid-P3/H5: 3-observation confirmation at entry, 5 bp exit band
```

For **Hybrid-P3/H5**, the explicit intended rules are:

| Active State | Observation / condition | Result |
|---|---|---|
| Stable | Three consecutive Trend values `> +25` | Enter Rising upon third |
| Stable | Three consecutive Trend values `< −25` | Enter Falling upon third |
| Stable | Candidate fails before confirmation | Stay Stable; reset or redirect candidate counter |
| Rising | Trend `> +20`, without opposite crossing | Remain Rising |
| Rising | Trend `≤ +20` | Exit to Stable immediately |
| Falling | Trend `< −20`, without opposite crossing | Remain Falling |
| Falling | Trend `≥ −20` | Exit to Stable immediately |
| Rising / Falling | Trend already crosses the **opposite** ±25 boundary | Exit old direction; treat that observation as the **first** confirmation candidate for the opposite direction; do not directly leap to opposite direction |

For instance, with initial Stable:

```text
Trend bp:       24   26   24   24   21   19
Plain:           S    R    S    S    S    S
Hysteresis-5:    S    R    R    R    R    S
Hybrid-P3/H5:    S    S    S    S    S    S
```

Here the hybrid prevents a one-observation crossing from creating an inherited Rising State. After **three** confirmed Rising observations, however, the hybrid intentionally applies the same 5 bp exit criterion as hysteresis.

**Implementation nuance:** A direct reversal policy must be specified explicitly. The exploratory hybrid used a *Stable intermediate State with the opposite crossing counted as confirmation observation #1*. This differs from the repository's original pure hysteresis, which allows an immediate direct reversal. The frozen source had **no adjacent plain Rising↔Falling jumps**, so the particular edge case did not alter the reported sample metrics. It still requires dedicated synthetic unit tests.

### 5.2 Exploratory hybrid comparison on the frozen fixture

The following was computed after the committed stabilization review, using the same 38,330 classified observations, provisional six-month Trend, common ±25 bp entry threshold, and five-observation endpoint smoothing. It is **discussion-stage evidence**, not an accepted design update.

| Tenor | Method | Short directional episodes ≤5 (%) | Transition rate (%) | Stable occupancy (%) |
|---|---|---:|---:|---:|
| 6M | Persistence-3 | 17.57 | 1.28 | 38.81 |
| 6M | Hysteresis-5 | 10.61 | 1.17 | 36.89 |
| 6M | **Hybrid-P3/H5** | **11.67** | **1.06** | **38.32** |
| 10Y | Persistence-3 | 14.65 | 2.44 | 31.19 |
| 10Y | Hysteresis-5 | 11.79 | 2.43 | 28.63 |
| 10Y | **Hybrid-P3/H5** | **16.94** | **2.28** | **31.41** |
| 30Y | Persistence-3 | 11.03 | 2.42 | 28.78 |
| 30Y | Hysteresis-5 | 10.85 | 2.30 | 25.72 |
| 30Y | **Hybrid-P3/H5** | **6.61** | **2.15** | **28.34** |

The hybrid consistently reduces transitions relative to these finalists and keeps Stable occupancy closer to Persistence-3 than to pure Hysteresis-5. But its short-episode percentage is **not uniformly better**: it is worse for 10Y than either comparator. Do not describe the hybrid as statistically or economically superior on the strength of this table.

Actual State disagreement proportions:

| Tenor | Hybrid-P3/H5 vs Hysteresis-5 | Hybrid-P3/H5 vs Persistence-3 |
|---|---:|---:|
| 6M | 1.43% | 1.49% |
| 10Y | 2.77% | 1.91% |
| 30Y | 2.62% | 2.20% |

These are non-trivial classification changes, not wholesale redefinitions. Once a direction is established, the hybrid can still retain it through a long plain-Stable stretch: maximum observed hybrid carryover was 11 / 11 / 9 valid observations for the 6M / 10Y / 30Y tenors, respectively. So the hybrid **reduces false entry inheritance; it does not abolish hysteresis exit-side path dependence**.

### 5.3 Feasibility, exact behavior, and cautions

The hybrid requires only a State machine with `active_state`, `pending_direction`, and `pending_count`. It fits naturally into **Component State Classification**, without introducing a new Component or Module or making the result ETF-dependent.

Suggested conceptual state machine:

```text
When active = Stable:
    classify current plain candidate using ±25 bp
    if candidate = Stable:
        clear pending direction and count
    otherwise:
        count consecutive same-direction confirmations
        enter direction when count reaches N

When active = Rising:
    remain Rising until Trend <= +20 bp
    on exit: return to Stable; if Trend < −25 bp,
             initialize Falling confirmation count to 1

When active = Falling:
    remain Falling until Trend >= −20 bp
    on exit: return to Stable; if Trend > +25 bp,
             initialize Rising confirmation count to 1
```

Specify and test at least: exact equality at ±25 / ±20; direction switches during confirmation; repeated oscillation; direct opposite crossing; insufficient sample warm-up; first-State initialization; missing observations; reset across structural segments; reproducibility from the same accepted observation history; and whether counting restarts after interruption. The earlier exploratory code initialized each historical segment using the first plain classification. That pragmatic convention should **not silently become the production initialization contract**.

**Decision status:** Hybrid-P3/H5 should be compared seriously with Persistence-3 and Hysteresis-5. The test supports distinguishable behavior and implementation feasibility, not model acceptance. Hybrid-P2/H5 is also useful for testing sensitivity to confirmation length, but adds no independent economic theory.

---

## 6. Trend-First Priority in Ambiguous Core Rule Mapping

### 6.1 The proposal, and what it does *not* mean

Because Yield Trend denotes the **broader established direction** while Recent Move is a shorter countertrend / confirmation observation, a proposed principle is:

> **When two Core Mapping values are plausible, choose the one that preserves the greater interpretive authority of Trend, subject to exposure-specific economics and existing justified constraints.**

This is a **tie-breaking / ambiguity-resolution preference**, not yet an accepted hard rule. It does **not** mean Recent Move is ignored; nor does it mean that every countertrend move is temporary. Some Recent Move episodes are early information about a genuine reversal.

A stronger version would require strict lexicographic ordering of all nine Rule Cases:

```text
Falling × Falling
 ≥ Falling × Stable
 ≥ Falling × Rising
 > Stable × Falling
 ≥ Stable × Stable
 ≥ Stable × Rising
 > Rising × Falling
 ≥ Rising × Stable
 ≥ Rising × Rising
```

This strong version may conflict with existing settled equal-score cells. **The broad economic premise does not by itself compel strict inequality at every Rule Case boundary.** Ordinal score categories may legitimately tie because the scale is intentionally coarse.

### 6.2 Starting table and exact unresolved choices

The current validation plan's starting Core table, where `0 / +1` means an unresolved choice rather than a numeric range:

| Trend | Recent | Short | Intermediate | Long |
|---|---|---:|---:|---:|
| Falling | Falling | +1 | +2 | +3 |
| Falling | Stable | +1 | +1 | +2 |
| Falling | Rising | 0 / +1 | +1 | +1 / +2 |
| Stable | Falling | 0 / +1 | +1 | +1 / +2 |
| Stable | Stable | 0 | 0 | 0 |
| Stable | Rising | 0 / −1 | −1 | −1 / −2 |
| Rising | Falling | 0 / −1 | −1 | −1 / −2 |
| Rising | Stable | −1 | −1 | −2 |
| Rising | Rising | −1 | −2 | −3 |

Task 1 provisionally preferred **Short Stable×Falling = +1**, **Short Stable×Rising = −1**, **Long Falling×Rising = +1**, and **Long Rising×Falling = −1**. It left the other four mixed cells unresolved (Short Falling×Rising; Short Rising×Falling; Long Stable×Falling; Long Stable×Rising). These Task-1 *preferences* must not be confused with irrevocably settled mapping cells.

The cross-Trend boundaries that matter most are:

```text
Falling × Rising  compared with Stable × Falling
Stable × Rising   compared with Rising × Falling
```

At a coarse seven-category scale, it is possible to impose **non-strict** priority (≥) without changing all settled scores. Imposing **strict** `>` for each boundary would require careful choices within or changes to the currently provisional / unresolved pairs; in Intermediate both adjacent cases currently have the same settled score (`+1/+1`, `−1/−1`), so full strict ordering would reopen settled mapping. **It is not correct to claim full strict Trend-first can be obtained while leaving every previously preferred mapping unchanged.**

One possible Short-side strict arrangement would require choosing `Falling×Rising = +1` while revisiting the provisional `Stable×Falling = +1` to `0`. A Long-side strict arrangement can use `Falling×Rising = +2` and `Stable×Falling = +1`, which revises the Task-1 provisional `Falling×Rising = +1`. Symmetric negative cases face analogous choices. These are **illustrative choices**, not recommended accepted rows.

A nine-level result scale is **not a mechanical consequence** of adopting a Trend-first preference. It becomes a separate question only if we conclude the existing seven ordinal categories fail to express economically necessary distinctions.

### 6.3 Why Trend-first is plausible yet not proven

Two distinct claims must be separated:

1. **Descriptive / architectural claim:** Trend measures a broader rates condition; Recent Move a shorter one.
2. **Evaluation judgment:** When they conflict, that broader condition deserves priority in the exposure-specific Core Result.

Claim 2 does **not logically follow** from Claim 1. A shorter move can contain early or very large economically relevant information even before the six-month Trend adjusts. For example, `Falling Trend = −30 bp` and `Rising Recent Move = +70 bp` would classify as Falling×Rising even though the recent adverse move dominates in magnitude. The three-state mapping deliberately discards that magnitude; the example is a **stress case**, not an empirically demonstrated failure.

The appeal of Trend-first is semantic consistency with an *established broader condition*. Its danger is excessive inertia or discounting a genuine reversal. An absolute assertion that Recent Move “will eventually be reflected in Trend” is only partly mechanistic: the two calculations share observations, but a countertrend move can reverse before a Trend State transition occurs.

### 6.4 What are worthwhile tests—and what can they really establish?

Initially proposed checks included:

1. **Mapping feasibility:** enumerate score constraints and changed provisional/settled cells under weak and strict Trend priority.
2. **Historical path / transition inspection:** inspect Core score paths in 1980, 2008, 2022, 2023 for abrupt changes, stale favorable assessments, or interpretability conflicts.
3. **Countertrend evolution:** classify whether opposing Recent Move episodes revert, become Stable, or precede Trend transitions over later horizons.
4. **Sensitivity to stabilization:** rerun otherwise identical mappings under Persistence-3, Hysteresis-5, and Hybrid-P3/H5.

A subsequent methodological objection materially revised how these tests should be described:

- **Test 1** checks feasibility and internal logical consistency. It cannot refute the economic priority premise.
- **Test 2** is qualitative diagnostics unless we define an *independent* standard for economically correct Core interpretation; otherwise we may simply prefer the path that looks smoother or more intuitive.
- **Test 3** checks a premise about short- and long-horizon movement, but the data are mechanically related and episode outcomes alone do not determine ordinal Core scores. Observing that Recent Move occasionally anticipates Trend does not automatically disprove a broad-condition interpretation.
- **Test 4** checks robustness to upstream classification; it cannot decide whether Trend *deserves* priority.

The key criticism was accepted: **the previous proposal overstated these diagnostics as potential falsification tests.** Without an independently declared criterion, such diagnostics risk confirmation by construction. Forward returns or ETF performance could supply one possible independent criterion, but making those labels the calibration objective would change the current project's validation scope toward predictive optimization.

A more economical route is to treat Trend-first as an **explicit provisional design judgment**, check mapping consistency, and inspect a small set of deliberately difficult cases for **clear conceptual contradictions**. Do not launch a large statistical campaign merely to demonstrate that a Trend-first mapping is more stable; greater stability is expected from the rule itself.

---

## 7. Relationship Between State Stabilization and Core Mapping

These discussions interact, but should not be merged:

| Concern | Architectural location | Question |
|---|---|---|
| Trend lookback, smoothing, ±25 bp | Component Value / State Classification | What broader rates condition is being measured? |
| Persistence / hysteresis / hybrid | Component State Classification | When is a directional condition established or withdrawn? |
| Trend-first ambiguity resolution | Duration Constituent Core Rule Mapping | What is the exposure-specific implication of a mixed Component State pair? |
| Result scale (seven versus nine levels) | Duration Core Result semantics | How many distinguishable ordinal interpretations are justified? |
| ETF turnover | Downstream choice / implementation concerns | How much trading or position adjustment is acceptable? |

It is important **not to use downstream Rule Mapping scores to choose upstream Trend thresholds or State Classification**. If the combination produces incoherent interpretations, diagnose whether the cause is measurement, State Classification, Rule Mapping, or a genuinely missing economic variable—then change the responsible boundary for the right reason.

One practical sequence is to settle the **economic meaning** of an established Trend State before finalizing a stabilization method. At the same time, a Trend-first mapping preference should not be used as a reason to exaggerate Trend State inertia. The meanings of *established direction* and *evaluation priority* are not synonymous.

---

## 8. Current Decision Ledger

| Item | Current position | Status / caution |
|---|---|---|
| Trend Value | `M5(t) − M5(t−126)` | Provisionally preferred; earlier 3M proposal superseded |
| Recent Move Value | `M5(t) − M5(t−21)` | Working definition, not reopened here |
| Trend threshold | Common ±25 bp across 6M / 10Y / 30Y tenors | Working threshold; consumer-independent justification |
| Recent Move threshold | ±10 bp | Existing working threshold |
| Trend stabilization in branch plan | 5 bp hysteresis | **Repository provisional preference only** |
| Stabilization after later discussion | Persistence-3, Hysteresis-5, Hybrid-P3/H5 are finalists; P2/H5 useful sensitivity challenger | No new accepted winner |
| Pure hysteresis early-entry advantage | Immediate threshold recognition | Real, but less decisive given tiny Persistence-3 delay |
| Hysteresis boundary carryover | Intentional and sometimes long | Economic interpretation unresolved |
| Hybrid concept | Confirm entry, resist minor exit pullback | Defensible and feasible; not proven superior |
| Core mapping | Use Trend-first as a *provisional tie-breaking preference* | Not a strict universal ordering or accepted final table |
| Existing seven-level Core scale | Retain initially | No basis yet for automatic expansion to nine levels |
| Large validation campaign for Trend-first | Not recommended absent falsifiable independent criterion | Use narrow consistency and challenge-case diagnostics |
| Macro Adjustment validation | Do not automatically advance | Human Trend / Core Review Gate remains pending |

### Unresolved human decisions

1. What precisely does **established Trend direction** mean operationally: time-confirmed emergence, persistence until materially contradicted, or both? This should govern the stabilizer choice.
2. Is the exit-side path dependency of hysteresis an **essential semantic feature** or an undesirable legacy State effect? How much historical carryover is acceptable, and why?
3. For the hybrid: is Persistence-3 the right entry count; should direct reversals pass through Stable; and what should the initial State and gap-restart policy be?
4. Does Trend-first govern **only ambiguous cells**, or should it become a **hard ordering constraint**? Which provisional Task-1 preferences would that explicitly override?
5. Can the current seven-category ordinal scale express the actual economic distinctions without arbitrary splitting or squeezing?
6. Does a challenging historical example reveal an upstream Trend error, a valid countertrend market condition, a mapping error, or simply information lost when magnitudes are discretized?
7. What evidence or reasoning would be sufficient to **reject** the chosen design? Avoid using indicators guaranteed to reward its own mechanics.

### Recommended next narrow work package

- **Design decision:** write down the intended semantics of entering and exiting an established Trend State; select a stabilization finalist for explicit human acceptance. If further testing is desired, focus narrowly on borderline exits and false-entry inheritance rather than re-optimizing general smoothness.
- **Core mapping decision:** create a constrained side-by-side table of current Task-1 preferences, seven-level **weak Trend-first**, and seven-level **strict Trend-first**. Label every reopened provisional and settled cell; do not silently revise the latter.
- **Challenge diagnostics, not calibration:** inspect a handful of historical transitions where intuition strongly conflicts with the proposed mapped result, and document the nature of the disagreement rather than producing a spurious numerical winner.
- **Authority update only after acceptance:** update the relevant Duration sections and accepted mapping/Component definitions in `docs/bondview_exposure_evaluation_design.md` and other applicable contracts; update the validation plan's review-gate record. Keep this discussion note as historical design reasoning.

---

## 9. Evidence and Reproducibility Notes

**Repository-committed inputs and outputs** at the referenced branch / commit:

```text
validation/261002_duration/task1_core/results.csv
validation/261002_duration/task1_core/analysis.py
validation/261002_duration/task1_core/report.md
bondview_duration_trend_horizon_6m_9m_12m_review.ipynb
bondview_duration_trend_6m_stabilization_review.ipynb
bondview_duration_trend_6m_stabilization_summary.csv
docs/bondview_duration_design_validation_codex_plan.md
```

**Exploratory discussion-stage results:** transition lag and hysteresis carryover; hybrid P2/P3 + H5 comparisons; differences between hybrid and the pure methods; countertrend-episode counts under stabilized classifications. These were derived from the branch's historical fixture during the conversation but **have not thereby become accepted design artifacts**. If cited in a future implementation PR or decision, preserve a reproducible notebook or executable analysis alongside them and explicitly identify the source commit, segment-reset rule, and hybrid direct-reversal convention.

The separate exploratory notebook produced earlier in the conversation was titled `bondview_duration_trend_stabilization_tradeoff_review.ipynb`; it concerns persistence versus hysteresis but **does not itself establish the hybrid comparison** described here. Do not confuse the two. The main data source is the frozen Task-1 CSV; no FRED download or new data acquisition is needed for these replay diagnostics.

All dates and episode durations in the tables above refer to the retained historical observations rather than arbitrary calendar days unless expressly labeled otherwise. No forward-performance claim, optimal trading strategy claim, or probability of success is implied.

---

## 10. Final Synthesis

The conversation moved from an initially attractive **“hysteresis is smoother and faster”** conclusion toward a more careful judgment:

1. **Six-month Yield Trend** is provisionally meaningful as the broader rates condition. Recent Move is a distinct shorter-horizon observation; mixed cases are legitimate, not an instability to eliminate.
2. **Persistence-3** makes entering an established State dependent on repeated evidence, and its ~2-observation lag is not obviously material for a six-month concept.
3. **Hysteresis-5** preserves direction through small retreats but sometimes inherits direction because of a single earlier crossing, for longer than pure persistence would.
4. **Hybrid-P3/H5** expresses a plausible asymmetric epistemology—confirm a new direction; require meaningful retreat to abandon it—and has measurable but non-uniform empirical effects. It is a serious challenger, **not** an accepted winner.
5. **Trend-first** can be a reasonable way to resolve ambiguous Core Mapping choices, but stronger claims of strict order or extra scale levels need independent justification. Historical smoothness and countertrend evolution mostly supply diagnostics; they do not automatically falsify or prove a model-design preference.

The resulting design stance should remain **explicitly provisional** until the Human Trend / Core Review Gate accepts a clear Component State meaning and a complete exposure-specific Core Rule Table.
