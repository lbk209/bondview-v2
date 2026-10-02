# Task 2 — Trend Definition Validation

## 1. Executive conclusion

**Recommend B: 3M overlapping Trend**, retaining `M5(t) − M5(t−63)`, the fixed ±25 bp Trend band, and the unchanged Task-1 Recent Move and smoothing for this comparison. This is a provisional design-validation judgment for human review, not a production change. B better represents the broader **current** directional rates condition in repeated sustained reversals, without becoming nearly interchangeable with Recent Move. A remains informative about a longer historical condition, but that condition can be too old for the intended current Duration assessment.

The central evidence is not simply that B has fewer opposing states. In the required 1980 diagnostic it leaves Falling only after weeks of rising Recent Move, then retains Rising through the fixed review extension; A remains Falling until October. The Task-1 Short 2008 and Long 1984 episodes show the same broader issue in other tenors and directions. Conversely, B's brief 10Y Falling classification in August 2022 is a meaningful cost: A more cleanly preserves the distinction between the broader tightening condition and midsummer relief. B is preferable on balance, not uniformly better in every event.

C and D mostly delay the information available to Duration Evaluation. They are exactly A and B shifted back by 21 valid observations; their lower contemporaneous agreement with Recent Move does not demonstrate a better economic distinction. In 2020 they reintroduce older conditions during the shock, and in 2022 D retains the relief interpretation after the recent rise returns. Their semantics are clear, but their current assessment is less useful.

Task-1 mixed-cell conclusions remain provisional: the two Short recommendations and Long Rising × Falling are unchanged; support for the specific Long Falling × Rising = +1 preference **weakens** because the prominent Task-1 evidence changes case under B. Retain +1 as a cautious provisional preference, not as a calibrated result. The four unresolved cells remain unresolved. No settled Rule Table cell needs reopening on this evidence.

A later **narrow State-Classification review is materially warranted for use of B**, focused on short-lived boundary-adjacent Trend labels and their Core consequences, especially the August 2022 examples below. This is not a reason to choose a different horizon by fiat, rescale the threshold here, or optimize for fewer changes. There is no comparable evidence warranting an endpoint-smoothing review now. Neither follow-up nor Task 3 was performed.

## 2. Method and baseline reproduction

Work starts from latest `main` commit `270ebea`, on 2026-10-02. Design authority: [system architecture](../../../docs/bondview_system_architecture.md). Specific context: [Duration validation plan](../../../docs/bondview_duration_design_validation_codex_plan.md), with the task prompt controlling exact windows, outputs, and constraints. The plan still names old Task-1 report paths; the [relocated Task-1 package](../task1_core/) is the evidence actually used. No design document or Task-1 artifact was modified.

The **sole historical input** is the frozen [Task-1 CSV](../task1_core/results.csv). SHA-256 was verified before any calculation:

`3316d1a8adece1e27e529a51531713a4cb173be22039100124853321daa66b18`

Accepted observations are only rows marked `available` or `insufficient_130_observation_history`. Warmup rows are valid raw observations, even though their Task-1 Core is not yet available. `no_source_observation` and `documented_structural_gap` rows are excluded. In particular, the nonblank quarantined 30Y entries are not accepted. The frozen segment IDs and contiguous valid-observation indices are verified, and no window or episode bridges a segment boundary. Routine missing dates are not filled or interpolated. There is no data download, date refresh, return series, or other historical input.

Short / Intermediate / Long retain DGS6MO / DGS10 / DGS30 and their own exposure-local States. For each accepted segment, `M5(k)` is the mean of yields at `k−4 … k`, converted to basis points. Decimal arithmetic classifies exact boundaries safely.

| Component | Exact calculation | Last reference observation needed | Classification |
| --- | --- | --- | --- |
| Recent Move, fixed | M5(t) − M5(t−21) | t−25 | Falling below −10; Stable [−10,+10]; Rising above +10 bp |
| A: 6M overlapping | M5(t) − M5(t−126) | t−130 | Falling below −25; Stable [−25,+25]; Rising above +25 bp |
| B: 3M overlapping | M5(t) − M5(t−63) | t−67 | Same fixed Trend band |
| C: 6M excluding latest 1M | M5(t−21) − M5(t−147) | t−151 | Same fixed Trend band |
| D: 3M excluding latest 1M | M5(t−21) − M5(t−84) | t−88 | Same fixed Trend band |

“Excluding latest 1M” shifts the **entire comparison**; it does not shorten the reference distance or replace only one endpoint. With fixed thresholds, `C(t)=A(t−21)` and `D(t)=B(t−21)` in both Value and State. These identities were checked numerically, without calculating another variant.

Before numerical comparison, A plus fixed Recent Move reproduced **all 38,330** Task-1 complete observations exactly: 11,140 Short, 16,042 Intermediate, and 11,148 Long. All six requested fields matched: `trend_bp`, `trend_state`, `recent_move_bp`, `recent_move_state`, `rule_case`, and `core_candidates`. Numeric equality is exact Decimal equality to the frozen decimal values; candidate arrays and State/Rule Case strings also match. Any mismatch raises an error before outputs are generated. There were no unexplained disagreements.

The unchanged Task-1 fixture supplies classification and Core mapping, with all ranged cells retained as JSON candidate sets. Neither Task-1 provisional recommendations nor new Task-2 judgments are substituted into those sets. Core codes are ordinal: comparisons use category-set equality and frequency, never category means or cardinal transformations. Calculations remain research fixtures outside authoritative production execution. Features, Component Values/States, local Core candidate results, and downstream diagnostic summaries remain distinguishable.

Input SHA-256 verified: `3316d1a8adece1e27e529a51531713a4cb173be22039100124853321daa66b18`. Baseline exact matches: 38330; all six requested fields match on every Task-1 complete row.

| Tenor | Variant | Individual n | Warmup exclusions | Individual eligible segments | Common n | Individual outside common |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | A | 11140 | 130 | 1982-03-16 – 2026-09-30 | 11119 | 21 |
| 6M | B | 11203 | 67 | 1981-12-11 – 2026-09-30 | 11119 | 84 |
| 6M | C | 11119 | 151 | 1982-04-15 – 2026-09-30 | 11119 | 0 |
| 6M | D | 11182 | 88 | 1982-01-13 – 2026-09-30 | 11119 | 63 |
| 10Y | A | 16042 | 130 | 1962-07-10 – 2026-09-30 | 16021 | 21 |
| 10Y | B | 16105 | 67 | 1962-04-09 – 2026-09-30 | 16021 | 84 |
| 10Y | C | 16021 | 151 | 1962-08-08 – 2026-09-30 | 16021 | 0 |
| 10Y | D | 16084 | 88 | 1962-05-09 – 2026-09-30 | 16021 | 63 |
| 30Y | A | 11148 | 260 | 1977-08-23 – 2002-02-15; 2006-08-16 – 2026-09-30 | 11106 | 42 |
| 30Y | B | 11274 | 134 | 1977-05-23 – 2002-02-15; 2006-05-17 – 2026-09-30 | 11106 | 168 |
| 30Y | C | 11106 | 302 | 1977-09-22 – 2002-02-15; 2006-09-15 – 2026-09-30 | 11106 | 0 |
| 30Y | D | 11232 | 176 | 1977-06-22 – 2002-02-15; 2006-06-16 – 2026-09-30 | 11106 | 126 |

| Tenor | Baseline matched | Raw missing rows | Structural-gap rows | Task-1 warmup | Task-2 common exclusions from accepted |
| --- | --- | --- | --- | --- | --- |
| 6M | 11140 | 5622 | 0 | 130 | 151 |
| 10Y | 16042 | 720 | 0 | 130 | 151 |
| 30Y | 11148 | 4446 | 1038 | 260 | 302 |


Individual availability is reported above, but **every primary A/B/C/D statistic uses the within-tenor common sample**: 11,119 / 16,021 / 11,106 observations for 6M / 10Y / 30Y, totaling 38,246. All four Trends and Recent Move must be available in the same segment; therefore the earliest eligible index is 151. A loses 21 observations per accepted segment relative to the baseline-reproduction sample, or 84 observations in total. The common eligible dates are C's eligible segments in the coverage table. Cross-tenor statistics use the 9,974 dates on which all three tenors meet those conditions. Short is unavailable for the 1980 diagnostic; no substitute series is used.

The source snapshot ends on 2026-09-30. The documented 30Y discontinuation remains excluded, and its common comparison sample resumes on 2006-09-15 after the longest required warmup. Missing-row counts include pre-inception and routine source-calendar missing rows, not just market-day data failures. Individual-variant availability is not conflated with a difference in behavior.

An episode is a maximal consecutive State or Rule Case run within a continuous eligible segment. All-sample boundary runs are censored at the sample boundaries; event paths are explicitly clipped to their windows and are not independent full-sample episodes. P75/P90 use the nearest-rank convention; medians use the ordinary midpoint convention. Transition denominators count adjacent eligible observations within segments. “Return runs ≤5” counts a middle State episode of at most five observations whose preceding and following States are the same; this is a descriptive local reversal diagnostic, not a fitted rejection rule.

The fixed 1980 context is June 1–November 30, encompassing both user-specified original episodes and allowing delayed exits to be observed. Other event windows are exactly those requested. Original Task-1 selected episodes are reconstructed on the full A sample using the original longest/largest-Recent/typical selection method; primary distribution comparisons use the common sample. Model-derived examples are identified as such, not promoted into independent ex-ante evidence.

## 3. Full-sample comparison

| Tenor | Variant | Episodes | Mean n | Median n | P90 n | Max n | Transitions / eligible pairs | Return runs ≤5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6M | A | 183 | 60.76 | 12 | 158 | 1534 | 182 (1.64%) | 54 |
| 6M | B | 243 | 45.76 | 15 | 113 | 1700 | 242 (2.18%) | 55 |
| 6M | C | 183 | 60.76 | 12 | 158 | 1534 | 182 (1.64%) | 54 |
| 6M | D | 242 | 45.95 | 15.0 | 113 | 1700 | 241 (2.17%) | 55 |
| 6M | Recent | 492 | 22.60 | 11.0 | 44 | 1567 | 491 (4.42%) | — |
| 10Y | A | 460 | 34.83 | 15.0 | 90 | 813 | 459 (2.87%) | 98 |
| 10Y | B | 608 | 26.35 | 14.0 | 69 | 827 | 607 (3.79%) | 136 |
| 10Y | C | 460 | 34.83 | 15.0 | 90 | 834 | 459 (2.87%) | 98 |
| 10Y | D | 607 | 26.39 | 14 | 69 | 848 | 606 (3.78%) | 136 |
| 10Y | Recent | 1162 | 13.79 | 8.0 | 31 | 403 | 1161 (7.25%) | — |
| 30Y | A | 331 | 33.55 | 14 | 95 | 346 | 329 (2.96%) | 77 |
| 30Y | B | 436 | 25.47 | 14.0 | 69 | 167 | 434 (3.91%) | 101 |
| 30Y | C | 331 | 33.55 | 14 | 95 | 346 | 329 (2.96%) | 77 |
| 30Y | D | 436 | 25.47 | 14.0 | 69 | 167 | 434 (3.91%) | 102 |
| 30Y | Recent | 864 | 12.85 | 8.0 | 29 | 102 | 862 (7.76%) | — |


**A versus B: more responsive, still broader than Recent Move.** B increases Trend switching from 1.64% to 2.18% for Short, 2.87% to 3.79% for Intermediate, and 2.96% to 3.91% for Long. That is a real stability cost. But the corresponding fixed Recent Move rates remain 4.42%, 7.25%, and 7.76%. B's mean episodes remain 45.76 / 26.35 / 25.47 observations, versus Recent Move's 22.60 / 13.79 / 12.85. Median B durations do not collapse: 15 / 14 / 14, versus A's 12 / 15 / 14 and Recent Move's 11 / 8 / 8. Means are influenced by long calm runs, so both means and medians matter.

The upper tail contracts: B Trend P90 is 113 / 69 / 69 observations versus A's 158 / 90 / 95. This improves responsiveness, but is not a standalone objective. Intermediate's short return runs rise from 98 to 136 and Long's from 77 to 101, so it would be wrong to claim that B preserves A's full stability. The event review checks whether the additional transitions add useful current information or merely oscillate near thresholds.


<details>
<summary>State frequencies and State-specific persistence for every tenor and variant</summary>

| Tenor | Variant | State | Frequency | Episodes | Mean n | Median n | P90 n | Max n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6M | A | Falling | 3508 (31.55%) | 47 | 74.64 | 19 | 246 | 455 |
| 6M | A | Stable | 4329 (38.93%) | 91 | 47.57 | 11 | 86 | 1534 |
| 6M | A | Rising | 3282 (29.52%) | 45 | 72.93 | 15 | 282 | 593 |
| 6M | B | Falling | 2612 (23.49%) | 57 | 45.82 | 23 | 111 | 275 |
| 6M | B | Stable | 5943 (53.45%) | 121 | 49.12 | 14 | 101 | 1700 |
| 6M | B | Rising | 2564 (23.06%) | 65 | 39.45 | 13 | 130 | 288 |
| 6M | C | Falling | 3529 (31.74%) | 47 | 75.09 | 19 | 246 | 455 |
| 6M | C | Stable | 4329 (38.93%) | 91 | 47.57 | 11 | 86 | 1534 |
| 6M | C | Rising | 3261 (29.33%) | 45 | 72.47 | 15 | 282 | 593 |
| 6M | D | Falling | 2612 (23.49%) | 57 | 45.82 | 23 | 111 | 275 |
| 6M | D | Stable | 5935 (53.38%) | 121 | 49.05 | 14 | 101 | 1700 |
| 6M | D | Rising | 2572 (23.13%) | 64 | 40.19 | 13.5 | 130 | 288 |
| 10Y | A | Falling | 5282 (32.97%) | 114 | 46.33 | 19.0 | 144 | 473 |
| 10Y | A | Stable | 4975 (31.05%) | 230 | 21.63 | 12.5 | 43 | 813 |
| 10Y | A | Rising | 5764 (35.98%) | 116 | 49.69 | 22.0 | 140 | 365 |
| 10Y | B | Falling | 4429 (27.64%) | 135 | 32.81 | 16 | 82 | 149 |
| 10Y | B | Stable | 6808 (42.49%) | 304 | 22.39 | 13.0 | 45 | 827 |
| 10Y | B | Rising | 4784 (29.86%) | 169 | 28.31 | 13 | 77 | 148 |
| 10Y | C | Falling | 5282 (32.97%) | 114 | 46.33 | 19.0 | 144 | 473 |
| 10Y | C | Stable | 4996 (31.18%) | 230 | 21.72 | 12.5 | 43 | 834 |
| 10Y | C | Rising | 5743 (35.85%) | 116 | 49.51 | 22.0 | 140 | 365 |
| 10Y | D | Falling | 4429 (27.64%) | 135 | 32.81 | 16 | 82 | 149 |
| 10Y | D | Stable | 6829 (42.63%) | 304 | 22.46 | 13.0 | 45 | 848 |
| 10Y | D | Rising | 4763 (29.73%) | 168 | 28.35 | 13.0 | 77 | 148 |
| 30Y | A | Falling | 4103 (36.94%) | 85 | 48.27 | 15 | 152 | 346 |
| 30Y | A | Stable | 3173 (28.57%) | 166 | 19.11 | 13.5 | 42 | 95 |
| 30Y | A | Rising | 3830 (34.49%) | 80 | 47.88 | 15.5 | 142 | 220 |
| 30Y | B | Falling | 3237 (29.15%) | 108 | 29.97 | 16.0 | 77 | 167 |
| 30Y | B | Stable | 4787 (43.10%) | 218 | 21.96 | 13.0 | 50 | 152 |
| 30Y | B | Rising | 3082 (27.75%) | 110 | 28.02 | 14.0 | 79 | 144 |
| 30Y | C | Falling | 4100 (36.92%) | 85 | 48.24 | 15 | 152 | 346 |
| 30Y | C | Stable | 3184 (28.67%) | 165 | 19.30 | 13 | 42 | 95 |
| 30Y | C | Rising | 3822 (34.41%) | 81 | 47.19 | 14 | 142 | 220 |
| 30Y | D | Falling | 3240 (29.17%) | 109 | 29.72 | 16 | 77 | 167 |
| 30Y | D | Stable | 4813 (43.34%) | 219 | 21.98 | 13 | 50 | 152 |
| 30Y | D | Rising | 3053 (27.49%) | 108 | 28.27 | 14.0 | 80 | 144 |


</details>

| Tenor | Variant | Exact State agreement | Opposing direction | All four mixed cases |
| --- | --- | --- | --- | --- |
| 6M | A | 7002 (62.97%) | 860 (7.73%) | 1740 (15.65%) |
| 6M | B | 7872 (70.80%) | 366 (3.29%) | 1865 (16.77%) |
| 6M | C | 6251 (56.22%) | 1167 (10.50%) | 2269 (20.41%) |
| 6M | D | 6689 (60.16%) | 979 (8.80%) | 2759 (24.81%) |
| 10Y | A | 7963 (49.70%) | 2245 (14.01%) | 4887 (30.50%) |
| 10Y | B | 8954 (55.89%) | 1105 (6.90%) | 4738 (29.57%) |
| 10Y | C | 6220 (38.82%) | 3819 (23.84%) | 6556 (40.92%) |
| 10Y | D | 6415 (40.04%) | 3037 (18.96%) | 6984 (43.59%) |
| 30Y | A | 5297 (47.69%) | 1494 (13.45%) | 3462 (31.17%) |
| 30Y | B | 5873 (52.88%) | 692 (6.23%) | 3580 (32.23%) |
| 30Y | C | 4021 (36.21%) | 2655 (23.91%) | 4686 (42.19%) |
| 30Y | D | 4051 (36.48%) | 2004 (18.04%) | 5160 (46.46%) |


B's exact-State agreement with Recent Move is 70.80% / 55.89% / 52.88%, up from A's 62.97% / 49.70% / 47.69%. This is not near interchangeability for the longer tenors. Short's higher agreement needs a different explanation: B Trend is Stable on 53.45% of dates and Stable × Stable alone occupies 39.97%; common quiet periods contribute much of its agreement. The same ±25 bp band over a shorter horizon produces more Stable classifications (B versus A: 53.45% versus 38.93% for Short, 42.49% versus 31.05% for Intermediate, 43.10% versus 28.57% for Long). These are measured small changes, not evidence of a missing state.

Opposing-direction occupancy falls under B, but **all four mixed cases do not disappear**. They actually rise from 15.65% to 16.77% for Short and from 31.17% to 32.23% for Long, while Intermediate changes from 30.50% to 29.57%. Some formerly conflicting established Trends become Stable while Recent Move remains directional. This redistribution preserves an economically useful distinction between an established direction and a recent move without requiring months of old-regime attribution. All nine cases remain populated.

C/D reduce agreement and increase mixed-case occupancy, but also reproduce older States by construction. They have almost the same marginal Trend persistence as A/B; small differences reflect shifted history entering and leaving the finite common sample, not extra smoothing. Lower agreement alone is not evidence of better information.


<details>
<summary>Complete nine-case cross-tab: counts and percentages on each tenor’s common sample</summary>

| Tenor | Rule Case | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| 6M | Falling × Falling | 1776 (15.97%) | 1706 (15.34%) | 1514 (13.62%) | 1251 (11.25%) |
| 6M | Falling × Stable | 1233 (11.09%) | 669 (6.02%) | 1382 (12.43%) | 849 (7.64%) |
| 6M | Falling × Rising | 499 (4.49%) | 237 (2.13%) | 633 (5.69%) | 512 (4.60%) |
| 6M | Stable × Falling | 486 (4.37%) | 788 (7.09%) | 575 (5.17%) | 905 (8.14%) |
| 6M | Stable × Stable | 3449 (31.02%) | 4444 (39.97%) | 3227 (29.02%) | 4155 (37.37%) |
| 6M | Stable × Rising | 394 (3.54%) | 711 (6.39%) | 527 (4.74%) | 875 (7.87%) |
| 6M | Rising × Falling | 361 (3.25%) | 129 (1.16%) | 534 (4.80%) | 467 (4.20%) |
| 6M | Rising × Stable | 1144 (10.29%) | 713 (6.41%) | 1217 (10.95%) | 822 (7.39%) |
| 6M | Rising × Rising | 1777 (15.98%) | 1722 (15.49%) | 1510 (13.58%) | 1283 (11.54%) |
| 10Y | Falling × Falling | 2623 (16.37%) | 2794 (17.44%) | 1858 (11.60%) | 1695 (10.58%) |
| 10Y | Falling × Stable | 1576 (9.84%) | 1101 (6.87%) | 1606 (10.02%) | 1259 (7.86%) |
| 10Y | Falling × Rising | 1083 (6.76%) | 534 (3.33%) | 1818 (11.35%) | 1475 (9.21%) |
| 10Y | Stable × Falling | 1421 (8.87%) | 1841 (11.49%) | 1347 (8.41%) | 1949 (12.17%) |
| 10Y | Stable × Stable | 2333 (14.56%) | 3175 (19.82%) | 2259 (14.10%) | 2882 (17.99%) |
| 10Y | Stable × Rising | 1221 (7.62%) | 1792 (11.19%) | 1390 (8.68%) | 1998 (12.47%) |
| 10Y | Rising × Falling | 1162 (7.25%) | 571 (3.56%) | 2001 (12.49%) | 1562 (9.75%) |
| 10Y | Rising × Stable | 1595 (9.96%) | 1228 (7.66%) | 1639 (10.23%) | 1363 (8.51%) |
| 10Y | Rising × Rising | 3007 (18.77%) | 2985 (18.63%) | 2103 (13.13%) | 1838 (11.47%) |
| 30Y | Falling × Falling | 2034 (18.31%) | 2009 (18.09%) | 1462 (13.16%) | 1178 (10.61%) |
| 30Y | Falling × Stable | 1264 (11.38%) | 842 (7.58%) | 1282 (11.54%) | 1052 (9.47%) |
| 30Y | Falling × Rising | 805 (7.25%) | 386 (3.48%) | 1356 (12.21%) | 1010 (9.09%) |
| 30Y | Stable × Falling | 1101 (9.91%) | 1509 (13.59%) | 1063 (9.57%) | 1652 (14.87%) |
| 30Y | Stable × Stable | 1205 (10.85%) | 1899 (17.10%) | 1153 (10.38%) | 1657 (14.92%) |
| 30Y | Stable × Rising | 867 (7.81%) | 1379 (12.42%) | 968 (8.72%) | 1504 (13.54%) |
| 30Y | Rising × Falling | 689 (6.20%) | 306 (2.76%) | 1299 (11.70%) | 994 (8.95%) |
| 30Y | Rising × Stable | 1083 (9.75%) | 811 (7.30%) | 1117 (10.06%) | 843 (7.59%) |
| 30Y | Rising × Rising | 2058 (18.53%) | 1965 (17.69%) | 1406 (12.66%) | 1216 (10.95%) |


</details>

| Tenor | Variant | Rule Case changes vs A | Candidate-set changes vs A |
| --- | --- | --- | --- |
| 6M | A | 0 (0.00%) | 0 (0.00%) |
| 6M | B | 2721 (24.47%) | 2721 (24.47%) |
| 6M | C | 1602 (14.41%) | 1602 (14.41%) |
| 6M | D | 2745 (24.69%) | 2745 (24.69%) |
| 10Y | A | 0 (0.00%) | 0 (0.00%) |
| 10Y | B | 6264 (39.10%) | 6264 (39.10%) |
| 10Y | C | 4605 (28.74%) | 4605 (28.74%) |
| 10Y | D | 5851 (36.52%) | 5851 (36.52%) |
| 30Y | A | 0 (0.00%) | 0 (0.00%) |
| 30Y | B | 4495 (40.47%) | 4495 (40.47%) |
| 30Y | C | 3321 (29.90%) | 3321 (29.90%) |
| 30Y | D | 4412 (39.73%) | 4412 (39.73%) |

All-tenor common dates: 9974, outer range 1982-04-15 – 2026-09-30; excludes the 30Y gap and all variant warmups.

| Variant | One common case | Exactly two cases | Three distinct cases | Any disagreement |
| --- | --- | --- | --- | --- |
| A | 2385 (23.91%) | 5925 (59.40%) | 1664 (16.68%) | 7589 (76.09%) |
| B | 2627 (26.34%) | 5986 (60.02%) | 1361 (13.65%) | 7347 (73.66%) |
| C | 2184 (21.90%) | 6158 (61.74%) | 1632 (16.36%) | 7790 (78.10%) |
| D | 2199 (22.05%) | 6360 (63.77%) | 1415 (14.19%) | 7775 (77.95%) |


Changing Trend has material downstream consequences despite leaving the mapping untouched. B changes Core candidate sets on 24.47% / 39.10% / 40.47% of Short / Intermediate / Long observations. These are changes in the research fixture's outputs, not production changes or measured changes in economic utility. Here every changed Rule Case also changes the candidate set because Recent Move is fixed and, conditional on each Recent State, the three Trend States map to distinct sets for each exposure.

Same-date cross-tenor disagreement remains the norm under B (73.66%, versus A's 76.09%). Thus faster Trend does not eliminate curve-segment differences or justify a market-wide Trend. C and D show 78.10% and 77.95% disagreement. The criterion is whether the local differences are interpretable, not whether their frequency is high or low.

## 4. Opposing-direction episode comparison

A's longest Falling × Rising episodes are 56 / 68 / 60 observations for Short / Intermediate / Long. B's maxima are 23 / 26 / 26. For Rising × Falling, A's maxima are 35 / 34 / 35, versus B's 13 / 23 / 20. B does not eliminate genuine opposing intervals: for example, both longer tenors retain prolonged Falling × Rising runs in early 2009, including large recent yield increases. The old broader decline and the current challenge remain separately visible.

Under A, at least one Falling × Rising episode reaches 42 observations in each tenor, and the 10Y example reaches 63. None of B's opposing episodes reaches 42. This is descriptive evidence of less lingering disagreement, **not** the reason to choose B. The meaningful question is whether the earlier exit reflects a sustained change in the current broader condition. Sections 5–6 and the original-episode comparisons below address that question.

C can prolong disagreement, but the longest combined-case run need not shift by exactly 21 observations: Recent Move is still current, so it can interrupt the opposing case while the old Trend persists. The 1980 Long example is particularly instructive: C briefly leaves Falling, re-enters it, and does not become Rising until November. Counting only the first exit or the maximum mixed-run length would obscure this staleness.


<details>
<summary>Complete mixed-episode distributions, including both opposing cases and both Stable-Trend mixed cases</summary>

| Tenor | Variant | Case | Episodes | Obs | Median | P75 | P90 | Max | ≥21 | ≥42 | ≥63 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6M | A | Falling × Rising | 39 | 499 | 8 | 20 | 28 | 56 | 9 | 1 | 0 |
| 6M | A | Stable × Falling | 58 | 486 | 7.0 | 12 | 19 | 32 | 2 | 0 | 0 |
| 6M | A | Stable × Rising | 58 | 394 | 6.0 | 10 | 15 | 24 | 1 | 0 | 0 |
| 6M | A | Rising × Falling | 39 | 361 | 6 | 13 | 20 | 35 | 3 | 0 | 0 |
| 6M | B | Falling × Rising | 29 | 237 | 5 | 15 | 20 | 23 | 1 | 0 | 0 |
| 6M | B | Stable × Falling | 94 | 788 | 7.0 | 13 | 18 | 25 | 3 | 0 | 0 |
| 6M | B | Stable × Rising | 86 | 711 | 6.0 | 12 | 21 | 35 | 9 | 0 | 0 |
| 6M | B | Rising × Falling | 27 | 129 | 3 | 8 | 11 | 13 | 0 | 0 | 0 |
| 6M | C | Falling × Rising | 45 | 633 | 11 | 21 | 28 | 56 | 12 | 2 | 0 |
| 6M | C | Stable × Falling | 62 | 575 | 5.0 | 12 | 21 | 39 | 7 | 0 | 0 |
| 6M | C | Stable × Rising | 52 | 527 | 8.0 | 14 | 22 | 38 | 7 | 0 | 0 |
| 6M | C | Rising × Falling | 43 | 534 | 8 | 18 | 31 | 54 | 8 | 1 | 0 |
| 6M | D | Falling × Rising | 39 | 512 | 9 | 21 | 28 | 41 | 11 | 0 | 0 |
| 6M | D | Stable × Falling | 90 | 905 | 7.0 | 13 | 22 | 36 | 12 | 0 | 0 |
| 6M | D | Stable × Rising | 81 | 875 | 7 | 17 | 27 | 44 | 16 | 1 | 0 |
| 6M | D | Rising × Falling | 42 | 467 | 6.0 | 19 | 23 | 34 | 9 | 0 | 0 |
| 10Y | A | Falling × Rising | 104 | 1083 | 6.0 | 16 | 25 | 68 | 16 | 1 | 1 |
| 10Y | A | Stable × Falling | 160 | 1421 | 5.5 | 12 | 20 | 44 | 16 | 4 | 0 |
| 10Y | A | Stable × Rising | 163 | 1221 | 6 | 11 | 17 | 33 | 9 | 0 | 0 |
| 10Y | A | Rising × Falling | 120 | 1162 | 7.0 | 16 | 21 | 34 | 15 | 0 | 0 |
| 10Y | B | Falling × Rising | 84 | 534 | 4.0 | 8 | 14 | 26 | 3 | 0 | 0 |
| 10Y | B | Stable × Falling | 211 | 1841 | 7 | 13 | 20 | 34 | 21 | 0 | 0 |
| 10Y | B | Stable × Rising | 228 | 1792 | 6.0 | 11 | 17 | 29 | 10 | 0 | 0 |
| 10Y | B | Rising × Falling | 85 | 571 | 5 | 9 | 15 | 23 | 2 | 0 | 0 |
| 10Y | C | Falling × Rising | 142 | 1818 | 9.0 | 19 | 29 | 68 | 28 | 4 | 1 |
| 10Y | C | Stable × Falling | 157 | 1347 | 7 | 12 | 19 | 44 | 14 | 3 | 0 |
| 10Y | C | Stable × Rising | 144 | 1390 | 8.0 | 13 | 21 | 42 | 15 | 1 | 0 |
| 10Y | C | Rising × Falling | 147 | 2001 | 10 | 20 | 27 | 45 | 34 | 3 | 0 |
| 10Y | D | Falling × Rising | 130 | 1475 | 8.0 | 18 | 24 | 41 | 26 | 0 | 0 |
| 10Y | D | Stable × Falling | 207 | 1949 | 7 | 14 | 22 | 34 | 26 | 0 | 0 |
| 10Y | D | Stable × Rising | 209 | 1998 | 7 | 14 | 22 | 46 | 24 | 1 | 0 |
| 10Y | D | Rising × Falling | 146 | 1562 | 8.0 | 14 | 22 | 41 | 20 | 0 | 0 |
| 30Y | A | Falling × Rising | 89 | 805 | 6 | 12 | 20 | 60 | 8 | 1 | 0 |
| 30Y | A | Stable × Falling | 120 | 1101 | 6.0 | 13 | 20 | 36 | 12 | 0 | 0 |
| 30Y | A | Stable × Rising | 101 | 867 | 7 | 12 | 19 | 27 | 7 | 0 | 0 |
| 30Y | A | Rising × Falling | 78 | 689 | 5.5 | 13 | 20 | 35 | 6 | 0 | 0 |
| 30Y | B | Falling × Rising | 58 | 386 | 5.0 | 9 | 15 | 26 | 2 | 0 | 0 |
| 30Y | B | Stable × Falling | 170 | 1509 | 7.0 | 13 | 20 | 32 | 16 | 0 | 0 |
| 30Y | B | Stable × Rising | 172 | 1379 | 6.0 | 11 | 18 | 34 | 11 | 0 | 0 |
| 30Y | B | Rising × Falling | 54 | 306 | 5.0 | 7 | 11 | 20 | 0 | 0 | 0 |
| 30Y | C | Falling × Rising | 112 | 1356 | 9.0 | 18 | 25 | 56 | 21 | 1 | 0 |
| 30Y | C | Stable × Falling | 124 | 1063 | 6.0 | 12 | 18 | 35 | 7 | 0 | 0 |
| 30Y | C | Stable × Rising | 103 | 968 | 7 | 13 | 22 | 41 | 13 | 0 | 0 |
| 30Y | C | Rising × Falling | 103 | 1299 | 9 | 20 | 25 | 56 | 22 | 3 | 0 |
| 30Y | D | Falling × Rising | 98 | 1010 | 7.0 | 16 | 22 | 39 | 13 | 0 | 0 |
| 30Y | D | Stable × Falling | 160 | 1652 | 8.0 | 14 | 25 | 47 | 26 | 1 | 0 |
| 30Y | D | Stable × Rising | 166 | 1504 | 6.0 | 12 | 21 | 41 | 19 | 0 | 0 |
| 30Y | D | Rising × Falling | 95 | 994 | 9 | 17 | 22 | 36 | 11 | 0 | 0 |


</details>


<details>
<summary>Longest episode for each tenor, variant, and opposing case; ties choose earliest start</summary>

| Tenor | Variant | Case | Start | End | n | Trend bp range | Recent bp range |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6M | A | Falling × Rising | 2008-04-18 | 2008-07-08 | 56 | -280.0 to -92.4 | 10.6 to 43.4 |
| 6M | A | Rising × Falling | 1983-09-07 | 1983-10-26 | 35 | 25.8 to 147.6 | -67.8 to -15.6 |
| 6M | B | Falling × Rising | 1985-07-18 | 1985-08-19 | 23 | -104.4 to -28.4 | 16.4 to 52.8 |
| 6M | B | Rising × Falling | 1995-02-02 | 1995-02-21 | 13 | 30.0 to 72.2 | -26.6 to -11.0 |
| 6M | C | Falling × Rising | 2008-04-18 | 2008-07-08 | 56 | -298.0 to -128.6 | 10.6 to 43.4 |
| 6M | C | Rising × Falling | 1989-04-18 | 1989-07-03 | 54 | 30.4 to 186.0 | -69.0 to -14.8 |
| 6M | D | Falling × Rising | 2008-04-18 | 2008-06-16 | 41 | -201.4 to -25.8 | 15.6 to 43.4 |
| 6M | D | Rising × Falling | 1995-02-02 | 1995-03-22 | 34 | 30.0 to 114.6 | -29.4 to -11.0 |
| 10Y | A | Falling × Rising | 1980-07-09 | 1980-10-14 | 68 | -203.8 to -38.2 | 16.6 to 109.6 |
| 10Y | A | Rising × Falling | 2025-02-06 | 2025-03-26 | 34 | 38.4 to 65.0 | -31.4 to -10.4 |
| 10Y | B | Falling × Rising | 2009-01-22 | 2009-02-27 | 26 | -156.6 to -32.2 | 17.2 to 59.8 |
| 10Y | B | Rising × Falling | 1975-05-09 | 1975-06-11 | 23 | 26.4 to 71.6 | -28.6 to -11.0 |
| 10Y | C | Falling × Rising | 1980-07-09 | 1980-10-14 | 68 | -203.8 to -35.0 | 16.6 to 109.6 |
| 10Y | C | Rising × Falling | 1980-03-24 | 1980-05-27 | 45 | 40.0 to 431.0 | -228.6 to -17.6 |
| 10Y | D | Falling × Rising | 1981-12-15 | 1982-02-11 | 41 | -215.6 to -48.2 | 12.6 to 119.2 |
| 10Y | D | Rising × Falling | 1980-03-24 | 1980-05-20 | 41 | 40.4 to 276.0 | -228.6 to -17.6 |
| 30Y | A | Falling × Rising | 1980-07-21 | 1980-10-14 | 60 | -160.2 to -32.0 | 15.2 to 92.4 |
| 30Y | A | Rising × Falling | 1984-07-20 | 1984-09-07 | 35 | 25.2 to 152.2 | -85.4 to -11.0 |
| 30Y | B | Falling × Rising | 2009-01-21 | 2009-02-26 | 26 | -129.6 to -27.8 | 13.2 to 87.2 |
| 30Y | B | Rising × Falling | 1987-06-16 | 1987-07-14 | 20 | 43.0 to 105.4 | -56.4 to -16.8 |
| 30Y | C | Falling × Rising | 1988-03-09 | 1988-05-26 | 56 | -111.8 to -34.2 | 10.4 to 45.4 |
| 30Y | C | Rising × Falling | 1984-07-20 | 1984-10-09 | 56 | 25.2 to 176.0 | -85.4 to -10.8 |
| 30Y | D | Falling × Rising | 1981-12-17 | 1982-02-11 | 39 | -161.8 to -27.6 | 12.2 to 107.2 |
| 30Y | D | Rising × Falling | 1980-04-07 | 1980-05-27 | 36 | 32.2 to 239.2 | -173.2 to -17.6 |


</details>


A single extreme episode is insufficient. In the original Short 2008-04-18–07-08 episode, B retains Falling × Rising for 20 observations, then spends 14 at Stable × Rising and 22 at Rising × Rising; A retains Falling × Rising for all 56. In the original Long 1984-07-20–09-07 declining reversal, B spends six observations at Rising × Falling, five at Stable × Falling, then 24 at Falling × Falling; A retains Rising × Falling throughout the 35 observations. These are model-derived supporting diagnostics in different directions and tenors, not extra independent ex-ante trials. Their within-window progression supports a current-condition interpretation: B acknowledges an initial counter-move, then recognizes a broader change. No later return is used to decide whether the state was “correct.”

## 5. Required 1980 prolonged-reversal diagnostic

**B identifies a meaningful broader change earlier than A.** For 10Y, Recent Move becomes Rising on July 9. B retains Falling initially, passes through Stable on July 31, and becomes Rising on August 5. At that date Recent Move is +56.4 bp and B is +37.8 bp, while A is still −55.0 bp. For 30Y, Recent Move becomes Rising on July 10; B becomes Stable August 1 and Rising August 6, with Recent +62.8 bp and B +34.0 bp. Thus B does not simply switch with the first opposing Recent observation. It waits through weeks of accumulated movement.

A stays Falling through October 14 in both original episodes and becomes Rising only October 20 / 21. By the end of the original episodes B shows +120.2 / +102.2 bp while A remains negative. A's values are arithmetically correct, but the old comparison increasingly describes a previous condition instead of the current broader direction needed by Duration Evaluation. B remains Rising through the fixed November extension while Recent Move temporarily becomes Stable in October. That retained distinction is evidence against pure duplication; it is an observed State path, not a forecast-success label.

**C/D do not improve this interpretation.** C's first 30Y exit on July 31 is not a durable recognition of the reversal: it re-enters Falling on August 19, before finally leaving in November. Its first Rising dates are November 20 / 21. D becomes Rising September 4 / 5, retaining the same B sequence but one Recent horizon later. These shifted definitions can explain what the previous broader condition was, but add unnecessary age for the specified current-condition role.

The exact original episode boundaries and durations are reproduced below. Short has no accepted data in 1980. Dates in paths omit the year only because every row in this section is in 1980; state names remain explicit.

### 10Y: Task-1 episode 1980-07-09 – 1980-10-14, 68 observations

| Series | State path (dates in 1980) |
| --- | --- |
| Recent | 06-02 Falling; 06-06 Stable; 06-09 Falling; 07-07 Stable; 07-09 Rising; 10-15 Stable; 10-22 Rising; end 11-28 Rising |
| A | 06-02 Stable; 06-06 Falling; 10-15 Stable; 10-20 Rising; end 11-28 Rising |
| B | 06-02 Falling; 07-31 Stable; 08-05 Rising; end 11-28 Rising |
| C | 06-02 Stable; 06-03 Falling; 07-01 Stable; 07-08 Falling; 11-17 Stable; 11-20 Rising; end 11-28 Rising |
| D | 06-02 Falling; 08-29 Stable; 09-04 Rising; end 11-28 Rising |

| Variant | At episode start | First non-Falling on/after start | Exit State | First Rising on/after start | Trend bp over original episode |
| --- | --- | --- | --- | --- | --- |
| A | Falling | 1980-10-15 | Stable | 1980-10-20 | -203.8 to -38.2 |
| B | Falling | 1980-07-31 | Stable | 1980-08-05 | -218.4 to 201.8 |
| C | Falling | 1980-11-17 | Stable | 1980-11-20 | -203.8 to -35.0 |
| D | Falling | 1980-08-29 | Stable | 1980-09-04 | -331.2 to 160.2 |

| Variant | Rule Case path, fixed June–November context |
| --- | --- |
| A | 06-02 Stable × Falling; 06-06 Falling × Stable; 06-09 Falling × Falling; 07-07 Falling × Stable; 07-09 Falling × Rising; 10-15 Stable × Stable; 10-20 Rising × Stable; 10-22 Rising × Rising; end 11-28 Rising × Rising |
| B | 06-02 Falling × Falling; 06-06 Falling × Stable; 06-09 Falling × Falling; 07-07 Falling × Stable; 07-09 Falling × Rising; 07-31 Stable × Rising; 08-05 Rising × Rising; 10-15 Rising × Stable; 10-22 Rising × Rising; end 11-28 Rising × Rising |
| C | 06-02 Stable × Falling; 06-03 Falling × Falling; 06-06 Falling × Stable; 06-09 Falling × Falling; 07-01 Stable × Falling; 07-07 Stable × Stable; 07-08 Falling × Stable; 07-09 Falling × Rising; 10-15 Falling × Stable; 10-22 Falling × Rising; 11-17 Stable × Rising; 11-20 Rising × Rising; end 11-28 Rising × Rising |
| D | 06-02 Falling × Falling; 06-06 Falling × Stable; 06-09 Falling × Falling; 07-07 Falling × Stable; 07-09 Falling × Rising; 08-29 Stable × Rising; 09-04 Rising × Rising; 10-15 Rising × Stable; 10-22 Rising × Rising; end 11-28 Rising × Rising |

| as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- |
| 1980-07-09 | 16.80 | -46.60 | -218.40 | -35.00 | -295.40 |
| 1980-07-31 | 52.60 | -61.60 | -20.60 | -44.20 | -282.60 |
| 1980-08-05 | 56.40 | -55.00 | 37.80 | -37.60 | -239.80 |
| 1980-10-14 | 16.60 | -39.20 | 120.20 | -127.40 | 160.20 |
| 1980-10-15 | 7.20 | -18.80 | 118.80 | -119.80 | 172.00 |
| 1980-10-20 | -4.40 | 36.80 | 132.20 | -97.20 | 200.40 |

### 30Y: Task-1 episode 1980-07-21 – 1980-10-14, 60 observations

| Series | State path (dates in 1980) |
| --- | --- |
| Recent | 06-02 Falling; 07-08 Stable; 07-10 Rising; 10-15 Stable; 10-23 Rising; end 11-28 Rising |
| A | 06-02 Stable; 06-03 Rising; 06-04 Stable; 06-12 Falling; 07-01 Stable; 07-21 Falling; 10-15 Stable; 10-21 Rising; end 11-28 Rising |
| B | 06-02 Falling; 08-01 Stable; 08-06 Rising; end 11-28 Rising |
| C | 06-02 Rising; 06-06 Stable; 07-02 Rising; 07-03 Stable; 07-14 Falling; 07-31 Stable; 08-19 Falling; 11-17 Stable; 11-21 Rising; end 11-28 Rising |
| D | 06-02 Stable; 06-03 Falling; 09-02 Stable; 09-05 Rising; end 11-28 Rising |

| Variant | At episode start | First non-Falling on/after start | Exit State | First Rising on/after start | Trend bp over original episode |
| --- | --- | --- | --- | --- | --- |
| A | Falling | 1980-10-15 | Stable | 1980-10-21 | -160.2 to -32.0 |
| B | Falling | 1980-08-01 | Stable | 1980-08-06 | -92.4 to 182.2 |
| C | Falling | 1980-07-31 | Stable | 1980-11-21 | -160.2 to -8.2 |
| D | Falling | 1980-09-02 | Stable | 1980-09-05 | -284.0 to 140.8 |

| Variant | Rule Case path, fixed June–November context |
| --- | --- |
| A | 06-02 Stable × Falling; 06-03 Rising × Falling; 06-04 Stable × Falling; 06-12 Falling × Falling; 07-01 Stable × Falling; 07-08 Stable × Stable; 07-10 Stable × Rising; 07-21 Falling × Rising; 10-15 Stable × Stable; 10-21 Rising × Stable; 10-23 Rising × Rising; end 11-28 Rising × Rising |
| B | 06-02 Falling × Falling; 07-08 Falling × Stable; 07-10 Falling × Rising; 08-01 Stable × Rising; 08-06 Rising × Rising; 10-15 Rising × Stable; 10-23 Rising × Rising; end 11-28 Rising × Rising |
| C | 06-02 Rising × Falling; 06-06 Stable × Falling; 07-02 Rising × Falling; 07-03 Stable × Falling; 07-08 Stable × Stable; 07-10 Stable × Rising; 07-14 Falling × Rising; 07-31 Stable × Rising; 08-19 Falling × Rising; 10-15 Falling × Stable; 10-23 Falling × Rising; 11-17 Stable × Rising; 11-21 Rising × Rising; end 11-28 Rising × Rising |
| D | 06-02 Stable × Falling; 06-03 Falling × Falling; 07-08 Falling × Stable; 07-10 Falling × Rising; 09-02 Stable × Rising; 09-05 Rising × Rising; 10-15 Rising × Stable; 10-23 Rising × Rising; end 11-28 Rising × Rising |

| as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- |
| 1980-07-21 | 60.40 | -32.00 | -92.40 | -65.00 | -258.60 |
| 1980-08-01 | 55.60 | -49.20 | -18.80 | -15.60 | -233.60 |
| 1980-08-06 | 62.80 | -54.60 | 34.00 | -16.40 | -202.00 |
| 1980-10-14 | 15.20 | -34.40 | 102.20 | -112.20 | 140.80 |
| 1980-10-15 | 6.80 | -20.60 | 100.20 | -106.60 | 150.60 |
| 1980-10-21 | 1.40 | 40.20 | 122.20 | -79.00 | 180.80 |


The implied mapping impact is substantive. Within the original 60-observation 30Y interval, B has nine Falling × Rising observations, three Stable × Rising observations, and 48 Rising × Rising observations. The unchanged candidate mapping therefore stops applying positive [1,2] merely because the older six-month comparison is negative. This is evidence for correcting the Component's timing, not for fitting a new Core score to that episode.

## 6. Historical transition review

The following paragraphs answer the six requested questions for every event: A's lag, B's timing, B/Recent redundancy, C/D's usefulness versus age, and cross-tenor interpretation. The expandable tables retain every Trend and Recent State transition, opposing interval, and start/end Value. They contain transition summaries rather than every daily observation; the full daily evidence is in [comparison.csv](comparison.csv).

### 1987 reversal: 1987-08-01 – 1987-10-31

**A's lag is mostly legitimate in this short window; B's advantage is modest.** All longer-tenor Trends begin Rising. Recent Move becomes Falling late in October, but 10Y still has a positive broader change under both A and B at the end (+58.0 and +28.0 bp). It is reasonable to preserve some adverse broader condition after only a few declining Recent observations. B moves Long to Stable on October 28 while A remains Rising; it does not make Long Falling. Short moves to Stable on October 26 under both A and B. These differences reflect the local history, not an error to harmonize.

**B is not synonymous with Recent, but does add noise earlier.** Its Short Trend briefly turns Rising for one observation in August while Recent remains Rising more broadly. The longer tenors' B Trend can become Stable during August even with Rising Recent Move. Those earlier fluctuations are a stability cost; the late-October behavior alone does not prove A is too slow. C/D preserve older Rising conditions through the end, including Short after its large recent decline. D also shows an August Short Falling × Rising interval inherited from older history. Temporal separation is legible but supplies no convincing improvement for the current exposure assessment here.


<details>
<summary>Transition paths, opposing intervals, and endpoint values</summary>


| Tenor | Series | State path (first state, then every transition; explicit final state) |
| --- | --- | --- |
| 6M | Recent | 08-03 Rising; 10-22 Stable; 10-23 Falling; end 10-30 Falling |
| 6M | A | 08-03 Rising; 10-26 Stable; end 10-30 Stable |
| 6M | B | 08-03 Stable; 08-11 Rising; 08-12 Stable; 09-04 Rising; 10-26 Stable; end 10-30 Stable |
| 6M | C | 08-03 Rising; 08-05 Stable; 08-19 Rising; end 10-30 Rising |
| 6M | D | 08-03 Stable; 08-12 Falling; 08-20 Stable; 09-10 Rising; 09-11 Stable; 10-06 Rising; end 10-30 Rising |
| 10Y | Recent | 08-03 Rising; 10-23 Stable; 10-26 Falling; end 10-30 Falling |
| 10Y | A | 08-03 Rising; end 10-30 Rising |
| 10Y | B | 08-03 Rising; 08-10 Stable; 08-28 Rising; end 10-30 Rising |
| 10Y | C | 08-03 Rising; end 10-30 Rising |
| 10Y | D | 08-03 Rising; 08-24 Stable; 08-28 Rising; 09-09 Stable; 09-29 Rising; end 10-30 Rising |
| 30Y | Recent | 08-03 Rising; 10-22 Stable; 10-26 Falling; end 10-30 Falling |
| 30Y | A | 08-03 Rising; end 10-30 Rising |
| 30Y | B | 08-03 Rising; 08-13 Stable; 08-28 Rising; 10-28 Stable; end 10-30 Stable |
| 30Y | C | 08-03 Rising; end 10-30 Rising |
| 30Y | D | 08-03 Rising; 09-14 Stable; 09-29 Rising; end 10-30 Rising |

| Tenor | Variant | Opposing intervals (event-clipped; observation counts) |
| --- | --- | --- |
| 6M | A | 10-23–10-23 Rising × Falling (1) |
| 6M | B | 10-23–10-23 Rising × Falling (1) |
| 6M | C | 10-23–10-30 Rising × Falling (6) |
| 6M | D | 08-12–08-19 Falling × Rising (6); 10-23–10-30 Rising × Falling (6) |
| 10Y | A | 10-26–10-30 Rising × Falling (5) |
| 10Y | B | 10-26–10-30 Rising × Falling (5) |
| 10Y | C | 10-26–10-30 Rising × Falling (5) |
| 10Y | D | 10-26–10-30 Rising × Falling (5) |
| 30Y | A | 10-26–10-30 Rising × Falling (5) |
| 30Y | B | 10-26–10-27 Rising × Falling (2) |
| 30Y | C | 10-26–10-30 Rising × Falling (5) |
| 30Y | D | 10-26–10-30 Rising × Falling (5) |

| Tenor | as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | 1987-08-03 | 23.20 | 70.40 | 10.40 | 33.20 | 20.80 |
| 6M | 1987-10-30 | -102.60 | -13.40 | -20.20 | 127.00 | 95.60 |
| 10Y | 1987-08-03 | 31.20 | 149.60 | 31.20 | 119.40 | 83.80 |
| 10Y | 1987-10-30 | -66.60 | 58.00 | 28.00 | 212.40 | 122.60 |
| 30Y | 1987-08-03 | 40.80 | 141.20 | 32.80 | 107.60 | 66.80 |
| 30Y | 1987-10-30 | -67.60 | 50.80 | 19.00 | 197.40 | 124.40 |


</details>

### 2008 GFC: 2008-09-01 – 2008-12-31

**A is sometimes tied to an older reference condition; B improves Short and Long more than Intermediate.** Short A changes from Stable to Rising in early September and does not reach Falling until October 6; B becomes Falling September 11 and retains it through December. Long B begins Falling and has only a one-observation Stable interruption, whereas A repeatedly moves between Stable and Falling into November. B thus treats the later short-lived Recent rises as counter-moves within a broader decline. This is a useful distinction, not suppression of Recent information.

**Intermediate is a counterweight to an overly simple “B is faster and cleaner” story.** B alternates between Stable and Falling during September/October while A alternates between Stable and Rising. Both finally become Falling on November 20. The fixed windows sample different parts of a volatile path; the evidence does not uniquely label every earlier State as right or wrong. B's multiple near-boundary returns are a cost, and its October Falling × Rising period shows it still adds information beyond Recent. C/D delay the final 10Y Falling recognition to December 22 and introduce old rising conditions during declines. Their historical separation does not clarify the current condition enough to offset that age. Tenor differences remain economically interpretable; there is no imposed common crisis verdict.


<details>
<summary>Transition paths, opposing intervals, and endpoint values</summary>


| Tenor | Series | State path (first state, then every transition; explicit final state) |
| --- | --- | --- |
| 6M | Recent | 09-02 Stable; 09-12 Falling; 10-21 Stable; 10-22 Rising; 10-27 Falling; end 12-31 Falling |
| 6M | A | 09-02 Stable; 09-08 Rising; 09-17 Stable; 10-06 Falling; 10-22 Stable; 10-28 Falling; end 12-31 Falling |
| 6M | B | 09-02 Stable; 09-11 Falling; end 12-31 Falling |
| 6M | C | 09-02 Falling; 09-04 Stable; 10-07 Rising; 10-17 Stable; 11-05 Falling; 11-21 Stable; 11-28 Falling; end 12-31 Falling |
| 6M | D | 09-02 Stable; 10-10 Falling; end 12-31 Falling |
| 10Y | Recent | 09-02 Falling; 09-24 Stable; 10-14 Rising; 10-24 Stable; 10-27 Falling; 10-28 Stable; 10-31 Rising; 11-12 Stable; 11-14 Falling; end 12-31 Falling |
| 10Y | A | 09-02 Stable; 09-24 Rising; 10-02 Stable; 10-14 Rising; 10-21 Stable; 11-20 Falling; end 12-31 Falling |
| 10Y | B | 09-02 Stable; 09-04 Falling; 09-30 Stable; 10-03 Falling; 10-10 Stable; 10-22 Falling; 10-30 Stable; 11-20 Falling; end 12-31 Falling |
| 10Y | C | 09-02 Rising; 09-15 Stable; 10-24 Rising; 11-03 Stable; 11-13 Rising; 11-20 Stable; 12-22 Falling; end 12-31 Falling |
| 10Y | D | 09-02 Stable; 10-03 Falling; 10-30 Stable; 11-04 Falling; 11-12 Stable; 11-21 Falling; 12-02 Stable; 12-22 Falling; end 12-31 Falling |
| 30Y | Recent | 09-02 Falling; 09-24 Stable; 10-01 Falling; 10-15 Stable; 10-20 Rising; 10-21 Stable; 10-23 Falling; 10-31 Stable; 11-04 Rising; 11-13 Stable; 11-20 Falling; end 12-31 Falling |
| 30Y | A | 09-02 Stable; 09-09 Falling; 09-11 Stable; 10-07 Falling; 10-14 Stable; 10-22 Falling; 11-03 Stable; 11-04 Falling; end 12-31 Falling |
| 30Y | B | 09-02 Falling; 09-26 Stable; 09-29 Falling; end 12-31 Falling |
| 30Y | C | 09-02 Rising; 09-03 Stable; 09-05 Rising; 09-08 Stable; 10-08 Falling; 10-10 Stable; 11-06 Falling; 11-13 Stable; 11-21 Falling; 12-04 Stable; 12-05 Falling; end 12-31 Falling |
| 30Y | D | 09-02 Stable; 09-29 Falling; 10-28 Stable; 10-29 Falling; end 12-31 Falling |

| Tenor | Variant | Opposing intervals (event-clipped; observation counts) |
| --- | --- | --- |
| 6M | A | 09-12–09-16 Rising × Falling (3) |
| 6M | B | 10-22–10-24 Falling × Rising (3) |
| 6M | C | 10-07–10-16 Rising × Falling (7) |
| 6M | D | 10-22–10-24 Falling × Rising (3) |
| 10Y | A | None |
| 10Y | B | 10-22–10-23 Falling × Rising (2) |
| 10Y | C | 09-02–09-12 Rising × Falling (9); 10-27–10-27 Rising × Falling (1); 11-14–11-19 Rising × Falling (4) |
| 10Y | D | 10-14–10-23 Falling × Rising (8); 11-04–11-10 Falling × Rising (5) |
| 30Y | A | 11-04–11-12 Falling × Rising (6) |
| 30Y | B | 10-20–10-20 Falling × Rising (1); 11-04–11-12 Falling × Rising (6) |
| 30Y | C | 09-02–09-02 Rising × Falling (1); 09-05–09-05 Rising × Falling (1); 11-06–11-12 Falling × Rising (4) |
| 30Y | D | 10-20–10-20 Falling × Rising (1); 11-04–11-12 Falling × Rising (6) |

| Tenor | as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | 2008-09-02 | 4.20 | 8.00 | -3.40 | -33.60 | 19.60 |
| 6M | 2008-12-31 | -23.80 | -193.60 | -128.80 | -147.80 | -147.20 |
| 10Y | 2008-09-02 | -25.20 | 13.20 | -23.00 | 36.20 | 20.60 |
| 10Y | 2008-12-31 | -85.00 | -188.40 | -162.80 | -97.00 | -78.20 |
| 30Y | 2008-09-02 | -22.40 | -12.00 | -31.00 | 26.60 | 8.00 |
| 30Y | 2008-12-31 | -89.60 | -196.80 | -171.60 | -115.80 | -88.00 |


</details>

### 2020 COVID: 2020-02-01 – 2020-03-31

**A's moving reference creates an awkward mid-February weakening; B offers a more coherent later-February path.** The longer tenors' Recent Move remains Falling throughout the window. A begins Falling, becomes Stable February 7 / 10, and returns to Falling February 28. B reaches Falling in both longer tenors on February 12 and stays there. It does not simply echo every Recent observation: 10Y B starts Stable, and Short B remains Stable until March 2 even though its Recent Move turns Falling February 27. Short A was already Falling because its longer window includes earlier declines. The B result is more current, but its initially Stable Short assessment is a tradeoff, not a universal speed advantage.

**C/D mostly reinsert old comparisons.** C becomes Stable again in March while the longer-tenor Recent Move remains Falling; D briefly produces Rising × Falling in February and does not establish sustained Falling until March 13. These paths are mechanically explainable but less persuasive as a current broader condition during the decline. No smoothing or threshold change is needed to explain why the shifted observations are older. Cross-tenor timing differences are plausible because the shorter end's recent move begins later; the variants are not judged against subsequent Treasury or ETF returns.


<details>
<summary>Transition paths, opposing intervals, and endpoint values</summary>


| Tenor | Series | State path (first state, then every transition; explicit final state) |
| --- | --- | --- |
| 6M | Recent | 02-03 Stable; 02-27 Falling; end 03-31 Falling |
| 6M | A | 02-03 Falling; end 03-31 Falling |
| 6M | B | 02-03 Stable; 03-02 Falling; end 03-31 Falling |
| 6M | C | 02-03 Falling; end 03-31 Falling |
| 6M | D | 02-03 Falling; 02-05 Stable; 03-31 Falling; end 03-31 Falling |
| 10Y | Recent | 02-03 Falling; end 03-31 Falling |
| 10Y | A | 02-03 Falling; 02-07 Stable; 02-28 Falling; end 03-31 Falling |
| 10Y | B | 02-03 Stable; 02-12 Falling; end 03-31 Falling |
| 10Y | C | 02-03 Stable; 02-14 Falling; 03-10 Stable; 03-30 Falling; end 03-31 Falling |
| 10Y | D | 02-03 Stable; 02-10 Rising; 02-14 Stable; 03-13 Falling; end 03-31 Falling |
| 30Y | Recent | 02-03 Falling; end 03-31 Falling |
| 30Y | A | 02-03 Falling; 02-10 Stable; 02-28 Falling; end 03-31 Falling |
| 30Y | B | 02-03 Falling; 02-04 Stable; 02-12 Falling; end 03-31 Falling |
| 30Y | C | 02-03 Stable; 02-13 Falling; 03-11 Stable; 03-30 Falling; end 03-31 Falling |
| 30Y | D | 02-03 Stable; 02-10 Rising; 02-13 Stable; 03-04 Falling; 03-05 Stable; 03-13 Falling; end 03-31 Falling |

| Tenor | Variant | Opposing intervals (event-clipped; observation counts) |
| --- | --- | --- |
| 6M | A | None |
| 6M | B | None |
| 6M | C | None |
| 6M | D | None |
| 10Y | A | None |
| 10Y | B | None |
| 10Y | C | None |
| 10Y | D | 02-10–02-13 Rising × Falling (4) |
| 30Y | A | None |
| 30Y | B | None |
| 30Y | C | None |
| 30Y | D | 02-10–02-12 Rising × Falling (3) |

| Tenor | as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | 2020-02-03 | -3.00 | -52.60 | -8.00 | -51.20 | -28.00 |
| 6M | 2020-03-31 | -117.60 | -182.60 | -152.20 | -64.80 | -35.20 |
| 10Y | 2020-02-03 | -32.20 | -48.60 | -23.40 | -12.20 | 20.80 |
| 10Y | 2020-03-31 | -47.20 | -94.00 | -113.60 | -31.40 | -52.40 |
| 30Y | 2020-02-03 | -30.40 | -54.00 | -25.80 | -19.60 | 20.80 |
| 30Y | 2020-03-31 | -37.80 | -78.60 | -97.00 | -30.00 | -46.60 |


</details>

### 2022 relief: 2022-06-01 – 2022-08-31

**This is the strongest required counterexample to preferring faster Trend unconditionally.** Short stays Rising under Recent Move and every Trend throughout the window. The two longer-tenor Recent Moves turn Falling in mid-July; A and C retain Rising Trend throughout, giving a clean broader-rise / recent-relief distinction. That persistence is economically legitimate here and should not be called failure simply because the opposing interval is long.

**B recognizes flattening but briefly goes further than necessary to convey it.** Intermediate B becomes Stable July 15, one observation after Recent Move turns Falling, and becomes Falling for August 8–10 before returning to Stable August 11. Its Falling values are only −26.2 to −25.6 bp. Long B becomes Stable July 20 and never Falling in this window, but briefly becomes Rising August 26–30 at +25.4 to +26.0 bp. B is therefore not interchangeable with Recent, yet its broad/recent distinction becomes weaker during this relief phase. The 10Y three-observation Falling label maps to Favorable +2 instead of the Mildly Favorable +1 for Stable × Falling or A's Mildly Unfavorable −1 for Rising × Falling. That is a real interpretive cost; no arithmetic score difference is inferred.

**Non-overlap is not a satisfactory fix.** C looks helpful because A remains Rising, but D becomes Stable only in mid-August and ends Stable after Recent has returned to Rising. It delays both recognition and exit rather than resolving the threshold question. The shorter-tenor tightening versus longer-tenor relief remains credible under every variant. This event supports retaining mixed-state meaning and motivates the narrow boundary review in Section 8; it does not erase B's stronger evidence in sustained reversals elsewhere.


<details>
<summary>Transition paths, opposing intervals, and endpoint values</summary>


| Tenor | Series | State path (first state, then every transition; explicit final state) |
| --- | --- | --- |
| 6M | Recent | 06-01 Rising; end 08-31 Rising |
| 6M | A | 06-01 Rising; end 08-31 Rising |
| 6M | B | 06-01 Rising; end 08-31 Rising |
| 6M | C | 06-01 Rising; end 08-31 Rising |
| 6M | D | 06-01 Rising; end 08-31 Rising |
| 10Y | Recent | 06-01 Stable; 06-13 Rising; 07-06 Stable; 07-14 Falling; 08-19 Stable; 08-24 Rising; end 08-31 Rising |
| 10Y | A | 06-01 Rising; end 08-31 Rising |
| 10Y | B | 06-01 Rising; 07-15 Stable; 08-08 Falling; 08-11 Stable; 08-26 Rising; end 08-31 Rising |
| 10Y | C | 06-01 Rising; end 08-31 Rising |
| 10Y | D | 06-01 Rising; 08-15 Stable; end 08-31 Stable |
| 30Y | Recent | 06-01 Stable; 06-13 Rising; 07-06 Stable; 07-15 Falling; 08-12 Stable; 08-23 Rising; end 08-31 Rising |
| 30Y | A | 06-01 Rising; end 08-31 Rising |
| 30Y | B | 06-01 Rising; 07-20 Stable; 08-26 Rising; 08-31 Stable; end 08-31 Stable |
| 30Y | C | 06-01 Rising; end 08-31 Rising |
| 30Y | D | 06-01 Rising; 08-18 Stable; end 08-31 Stable |

| Tenor | Variant | Opposing intervals (event-clipped; observation counts) |
| --- | --- | --- |
| 6M | A | None |
| 6M | B | None |
| 6M | C | None |
| 6M | D | None |
| 10Y | A | 07-14–08-18 Rising × Falling (26) |
| 10Y | B | 07-14–07-14 Rising × Falling (1) |
| 10Y | C | 07-14–08-18 Rising × Falling (26) |
| 10Y | D | 07-14–08-12 Rising × Falling (22) |
| 30Y | A | 07-15–08-11 Rising × Falling (20) |
| 30Y | B | 07-15–07-19 Rising × Falling (3) |
| 30Y | C | 07-15–08-11 Rising × Falling (20) |
| 30Y | D | 07-15–08-11 Rising × Falling (20) |

| Tenor | as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | 2022-06-01 | 15.60 | 147.60 | 90.40 | 135.00 | 98.60 |
| 6M | 2022-08-31 | 35.20 | 262.60 | 172.20 | 251.20 | 152.60 |
| 10Y | 2022-06-01 | -5.80 | 125.80 | 93.80 | 125.60 | 106.20 |
| 10Y | 2022-08-31 | 39.40 | 122.20 | 28.40 | 89.40 | -16.80 |
| 30Y | 2022-06-01 | 7.40 | 112.60 | 80.00 | 91.80 | 83.40 |
| 30Y | 2022-08-31 | 24.80 | 102.40 | 22.40 | 88.40 | 5.00 |


</details>

### 2023 long-end selloff: 2023-07-01 – 2023-10-31

**Both A and B recognize longer-tenor adversity; B improves the contrast with a flattening short end.** Short B becomes Stable August 21 and remains there, ending at +0.4 bp with Recent +2.0 bp. A ends Rising at +50.2 bp because it still spans the earlier short-rate increase. For the intended current broader condition, B's Stable Short is more informative than treating that earlier increase as indefinitely current. At the longer end, A/B both end Rising and preserve the adverse directional interpretation. B's 10Y Trend stays Rising through September while A briefly becomes Stable, but B also has a two-observation Stable interruption in July and Long B pauses in July before retaining Rising from July 28. It is not uniformly more stable or earlier.

**Recent remains distinct.** Repeated longer-tenor Recent pauses occur while B retains Rising, so a sustained broader condition and shorter pauses remain visible. C/D add delayed changes; notably D starts 10Y Falling and has Falling × Rising on July 5–10, reflecting an older comparison instead of the emerging current rise. Their additional mixed cases do not clarify current exposure interpretation. Cross-tenor differentiation is preserved without attributing the selloff to any unsupported causal factor.


<details>
<summary>Transition paths, opposing intervals, and endpoint values</summary>


| Tenor | Series | State path (first state, then every transition; explicit final state) |
| --- | --- | --- |
| 6M | Recent | 07-03 Stable; 07-12 Rising; 07-31 Stable; end 10-31 Stable |
| 6M | A | 07-03 Rising; 09-06 Stable; 09-11 Rising; end 10-31 Rising |
| 6M | B | 07-03 Rising; 08-21 Stable; end 10-31 Stable |
| 6M | C | 07-03 Rising; 10-05 Stable; 10-11 Rising; end 10-31 Rising |
| 6M | D | 07-03 Rising; 07-07 Stable; 07-13 Rising; 09-20 Stable; end 10-31 Stable |
| 10Y | Recent | 07-03 Stable; 07-05 Rising; 07-17 Stable; 07-26 Rising; 08-09 Stable; 08-11 Rising; 09-01 Stable; 09-07 Rising; 09-15 Stable; 09-22 Rising; end 10-31 Rising |
| 10Y | A | 07-03 Stable; 07-10 Rising; 08-30 Stable; 09-07 Rising; end 10-31 Rising |
| 10Y | B | 07-03 Rising; 07-21 Stable; 07-25 Rising; end 10-31 Rising |
| 10Y | C | 07-03 Stable; 07-17 Rising; 07-18 Stable; 07-19 Rising; 07-24 Stable; 08-08 Rising; 09-29 Stable; 10-06 Rising; end 10-31 Rising |
| 10Y | D | 07-03 Falling; 07-11 Stable; 07-19 Rising; 07-31 Stable; 08-02 Rising; 08-21 Stable; 08-23 Rising; end 10-31 Rising |
| 30Y | Recent | 07-03 Stable; 07-11 Rising; 07-14 Stable; 07-27 Rising; 09-05 Stable; 09-08 Rising; 09-14 Stable; 09-25 Rising; end 10-31 Rising |
| 30Y | A | 07-03 Stable; 07-11 Rising; end 10-31 Rising |
| 30Y | B | 07-03 Stable; 07-06 Rising; 07-18 Stable; 07-28 Rising; end 10-31 Rising |
| 30Y | C | 07-03 Stable; 07-10 Rising; 07-25 Stable; 08-09 Rising; end 10-31 Rising |
| 30Y | D | 07-03 Stable; 08-04 Rising; 08-16 Stable; 08-28 Rising; end 10-31 Rising |

| Tenor | Variant | Opposing intervals (event-clipped; observation counts) |
| --- | --- | --- |
| 6M | A | None |
| 6M | B | None |
| 6M | C | None |
| 6M | D | None |
| 10Y | A | None |
| 10Y | B | None |
| 10Y | C | None |
| 10Y | D | 07-05–07-10 Falling × Rising (4) |
| 30Y | A | None |
| 30Y | B | None |
| 30Y | C | None |
| 30Y | D | None |

| Tenor | as_of | Recent bp | A bp | B bp | C bp | D bp |
| --- | --- | --- | --- | --- | --- | --- |
| 6M | 2023-07-03 | 2.20 | 75.20 | 57.40 | 76.80 | 28.20 |
| 6M | 2023-10-31 | 2.00 | 50.20 | 0.40 | 62.00 | 5.80 |
| 10Y | 2023-07-03 | 8.60 | -3.60 | 28.40 | 1.20 | -26.60 |
| 10Y | 2023-10-31 | 30.20 | 140.40 | 91.20 | 104.40 | 80.80 |
| 30Y | 2023-07-03 | -5.40 | -6.60 | 13.80 | 14.60 | -4.00 |
| 30Y | 2023-10-31 | 33.40 | 131.80 | 101.00 | 96.20 | 85.80 |


</details>

## 7. Task-1 mixed-cell robustness

The unchanged candidate mapping was used under **all four variants**. The occupancy table reports each case's common-sample membership and overlap with A; the original-episode table shows how the Task-1 selected episodes move between cases. Changes in membership are reasons to reassess the evidence, not reasons by themselves to choose a different ordinal category.

| Tenor | Case | A observations | B observations | C observations | D observations |
| --- | --- | --- | --- | --- | --- |
| 6M | Falling × Rising | 499 (499 also A) | 237 (199 also A) | 633 (497 also A) | 512 (380 also A) |
| 6M | Stable × Falling | 486 (486 also A) | 788 (347 also A) | 575 (265 also A) | 905 (318 also A) |
| 6M | Stable × Rising | 394 (394 also A) | 711 (297 also A) | 527 (254 also A) | 875 (280 also A) |
| 6M | Rising × Falling | 361 (361 also A) | 129 (77 also A) | 534 (312 also A) | 467 (247 also A) |
| 30Y | Falling × Rising | 805 (805 also A) | 386 (260 also A) | 1356 (759 also A) | 1010 (625 also A) |
| 30Y | Stable × Falling | 1101 (1101 also A) | 1509 (622 also A) | 1063 (503 also A) | 1652 (600 also A) |
| 30Y | Stable × Rising | 867 (867 also A) | 1379 (529 also A) | 968 (329 also A) | 1504 (547 also A) |
| 30Y | Rising × Falling | 689 (689 also A) | 306 (232 also A) | 1299 (668 also A) | 994 (520 also A) |


| Exposure / case | Task-1 conclusion | Task-2 status under recommended B | Economic reasoning, evidence, and effect of C/D |
| --- | --- | --- | --- |
| Short Stable × Falling | Provisional +1 from [0,+1] | **Leaves unchanged**, still provisional | A current three-month Stable condition with a recent decline still justifies mild favorability for small positive duration. The 2003 typical episode remains in this case throughout under B; most of the 1997 longest episode remains here before B establishes Falling. C/D sometimes preserve an older rising or falling Trend, changing timing rather than disproving the directional rationale. More observations in the cell do not validate +1 by themselves. |
| Short Stable × Rising | Provisional −1 from [−1,0] | **Leaves unchanged**, still provisional | Same sign logic with no established opposing broader direction. The 1993 typical episode is unchanged under every variant. B reclassifies later parts of the 1997 longest example as Rising × Rising and the 1983 large-move example entirely as Rising × Rising; the adverse interpretation is preserved. C/D's older negative Trend in 1983 illustrates delayed classification, not evidence that a current rise is favorable. |
| Long Falling × Rising | Provisional +1 from [+1,+2] | **Weakens**; retain +1 only as a cautious provisional preference | The 1980 longest/largest example no longer supplies 60 observations of genuine opposition under B: only nine stay in this cell, and most become Rising × Rising. The typical 2012 example retains only two of six observations. The original category preference partly compensated for A's old-regime persistence; that evidence is less applicable. Nevertheless B's 2009 longest episode still combines a substantial broader decline with a recent increase, so tempering favorability remains economically defensible. C/D restoring older cases does not supply independent support. Evidence does not justify finalizing +1 or replacing it with +2. |
| Long Rising × Falling | Provisional −1 from [−2,−1] | **Leaves unchanged**, still provisional | Genuine recent relief can moderate an adverse broader condition even with B. The typical June 1984 episode remains in this cell under all four variants, and 15 of 22 observations of the large April–May 1980 episode remain here under B. Most of the long July–September 1984 episode becomes Falling × Falling, correctly moving the recognition of a new broader decline into the Component rather than forcing the mapping to do it. C/D retaining the prior rise longer supports caution about their timing, not a more severe category for B. |
| Short Falling × Rising | Unresolved [0,+1] | **Leaves unresolved** | B removes much of the sustained 2008 and 1985 reversals from this cell, and moves the 2002 typical case entirely to Stable × Rising. Residual B episodes still represent a genuine older decline opposed by a recent rise. Neutral versus mild favorability is not uniquely determined by those semantics; C/D make the condition older and cannot calibrate the choice. |
| Short Rising × Falling | Unresolved [−1,0] | **Leaves unresolved** | The 1983 long relief episode transitions into Stable and Falling Trend under B, but the 1988 typical case stays Rising × Falling under every variant. That range of economic conditions still admits a mild adverse or neutral category; shorter occupancy is not grounds to force Neutral. |
| Long Stable × Falling | Unresolved [+1,+2] | **Leaves unresolved** | B reclassifies the largest 1981 example entirely as Falling × Falling and divides the 1990 longest example between Rising, Stable, and Falling Trend. The 1988 typical example stays Stable × Falling under B. Earlier recognition of established declines changes which observations require the mixed cell; it does not determine mild versus favorable intensity within it. C/D's shifted memberships similarly do not calibrate intensity. |
| Long Stable × Rising | Unresolved [−2,−1] | **Leaves unresolved** | The entire 2015 longest example becomes Rising × Rising under B, but the 2001–2002 largest-Recent example remains Stable × Rising, as does the 2001 typical example. Thus not all meaningful rises become established Trend even under B. Both candidate severities remain defensible; C/D frequently retain an older Falling condition, demonstrating window effects rather than economic calibration. |

No cell is finalized or mechanically resolved by frequency. None of the settled cells is reopened: their directional and weak-order interpretation remains coherent. The unusual outputs highlighted in 1980 and 2022 chiefly concern the definition or classification of Trend, not a demonstrated reversal of the economic Rule Mapping.


<details>
<summary>All original Task-1 longest, largest-Recent, and typical mixed episodes, preserved without reselection to favor B</summary>

| Tenor | A case | Selection | Original interval | A cases/counts | B cases/counts | C cases/counts | D cases/counts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6M | Falling × Rising | longest | 2008-04-18 – 2008-07-08 (56) | Falling × Rising: 56 | Falling × Rising: 20; Stable × Rising: 14; Rising × Rising: 22 | Falling × Rising: 56 | Falling × Rising: 41; Stable × Rising: 14; Rising × Rising: 1 |
| 6M | Falling × Rising | largest Recent | 1985-02-06 – 1985-03-29 (36) | Falling × Rising: 36 | Falling × Rising: 13; Stable × Rising: 3; Rising × Rising: 20 | Falling × Rising: 36 | Falling × Rising: 34; Stable × Rising: 2 |
| 6M | Falling × Rising | typical | 2002-02-12 – 2002-02-25 (9) | Falling × Rising: 9 | Stable × Rising: 9 | Falling × Rising: 9 | Falling × Rising: 9 |
| 6M | Stable × Falling | longest | 1997-05-27 – 1997-07-10 (32) | Stable × Falling: 32 | Rising × Falling: 1; Stable × Falling: 23; Falling × Falling: 8 | Rising × Falling: 15; Stable × Falling: 17 | Rising × Falling: 22; Stable × Falling: 10 |
| 6M | Stable × Falling | largest Recent | 1987-11-18 – 1987-11-24 (5) | Stable × Falling: 5 | Rising × Falling: 1; Stable × Falling: 4 | Rising × Falling: 5 | Rising × Falling: 5 |
| 6M | Stable × Falling | typical | 2003-05-19 – 2003-05-28 (7) | Stable × Falling: 7 | Stable × Falling: 7 | Falling × Falling: 7 | Stable × Falling: 7 |
| 6M | Stable × Rising | longest | 1997-03-06 – 1997-04-09 (24) | Stable × Rising: 24 | Stable × Rising: 13; Rising × Rising: 11 | Stable × Rising: 24 | Stable × Rising: 24 |
| 6M | Stable × Rising | largest Recent | 1983-03-31 – 1983-04-08 (6) | Stable × Rising: 6 | Rising × Rising: 6 | Falling × Rising: 6 | Falling × Rising: 5; Stable × Rising: 1 |
| 6M | Stable × Rising | typical | 1993-10-26 – 1993-11-02 (6) | Stable × Rising: 6 | Stable × Rising: 6 | Stable × Rising: 6 | Stable × Rising: 6 |
| 6M | Rising × Falling | longest | 1983-09-07 – 1983-10-26 (35) | Rising × Falling: 35 | Rising × Falling: 10; Stable × Falling: 11; Falling × Falling: 14 | Rising × Falling: 35 | Rising × Falling: 31; Stable × Falling: 4 |
| 6M | Rising × Falling | largest Recent | 1987-11-10 – 1987-11-17 (5) | Rising × Falling: 5 | Stable × Falling: 4; Rising × Falling: 1 | Rising × Falling: 5 | Rising × Falling: 5 |
| 6M | Rising × Falling | typical | 1988-09-16 – 1988-09-23 (6) | Rising × Falling: 6 | Rising × Falling: 6 | Rising × Falling: 6 | Rising × Falling: 6 |
| 30Y | Falling × Rising | longest | 1980-07-21 – 1980-10-14 (60) | Falling × Rising: 60 | Falling × Rising: 9; Stable × Rising: 3; Rising × Rising: 48 | Falling × Rising: 47; Stable × Rising: 13 | Falling × Rising: 30; Stable × Rising: 3; Rising × Rising: 27 |
| 30Y | Falling × Rising | largest Recent | 1980-07-21 – 1980-10-14 (60) | Falling × Rising: 60 | Falling × Rising: 9; Stable × Rising: 3; Rising × Rising: 48 | Falling × Rising: 47; Stable × Rising: 13 | Falling × Rising: 30; Stable × Rising: 3; Rising × Rising: 27 |
| 30Y | Falling × Rising | typical | 2012-08-10 – 2012-08-17 (6) | Falling × Rising: 6 | Falling × Rising: 2; Stable × Rising: 4 | Falling × Rising: 6 | Falling × Rising: 6 |
| 30Y | Stable × Falling | longest | 1990-10-19 – 1990-12-11 (36) | Stable × Falling: 36 | Rising × Falling: 8; Stable × Falling: 11; Falling × Falling: 17 | Rising × Falling: 20; Stable × Falling: 16 | Rising × Falling: 29; Stable × Falling: 7 |
| 30Y | Stable × Falling | largest Recent | 1981-12-02 – 1981-12-09 (6) | Stable × Falling: 6 | Falling × Falling: 6 | Rising × Falling: 5; Stable × Falling: 1 | Rising × Falling: 4; Stable × Falling: 2 |
| 30Y | Stable × Falling | typical | 1988-12-22 – 1988-12-30 (6) | Stable × Falling: 6 | Stable × Falling: 6 | Stable × Falling: 6 | Falling × Falling: 6 |
| 30Y | Stable × Rising | longest | 2015-05-05 – 2015-06-11 (27) | Stable × Rising: 27 | Rising × Rising: 27 | Falling × Rising: 21; Stable × Rising: 6 | Stable × Rising: 16; Rising × Rising: 11 |
| 30Y | Stable × Rising | largest Recent | 2001-12-11 – 2002-01-09 (20) | Stable × Rising: 20 | Stable × Rising: 20 | Falling × Rising: 20 | Falling × Rising: 8; Stable × Rising: 12 |
| 30Y | Stable × Rising | typical | 2001-01-25 – 2001-02-02 (7) | Stable × Rising: 7 | Stable × Rising: 7 | Falling × Rising: 7 | Falling × Rising: 7 |
| 30Y | Rising × Falling | longest | 1984-07-20 – 1984-09-07 (35) | Rising × Falling: 35 | Rising × Falling: 6; Stable × Falling: 5; Falling × Falling: 24 | Rising × Falling: 35 | Rising × Falling: 27; Stable × Falling: 5; Falling × Falling: 3 |
| 30Y | Rising × Falling | largest Recent | 1980-04-07 – 1980-05-06 (22) | Rising × Falling: 22 | Rising × Falling: 15; Stable × Falling: 4; Falling × Falling: 3 | Rising × Falling: 22 | Rising × Falling: 22 |
| 30Y | Rising × Falling | typical | 1984-06-15 – 1984-06-22 (6) | Rising × Falling: 6 | Rising × Falling: 6 | Rising × Falling: 6 | Rising × Falling: 6 |


</details>


For the human review gate, the recommended Core table therefore remains the Task-1 proposal, with the same four provisional category preferences and the same four unresolved cells. Long Falling × Rising has weaker support for its exact category preference. This table is a review recommendation; **comparison.csv still retains all eight original candidate sets**.

| Trend | Recent | Short | Intermediate | Long |
| --- | --- | --- | --- | --- |
| Falling | Falling | +1 | +2 | +3 |
| Falling | Stable | +1 | +1 | +2 |
| Falling | Rising | [0,+1] unresolved | +1 | +1 provisional, weakened |
| Stable | Falling | +1 provisional | +1 | [+1,+2] unresolved |
| Stable | Stable | 0 | 0 | 0 |
| Stable | Rising | −1 provisional | −1 | [−2,−1] unresolved |
| Rising | Falling | [−1,0] unresolved | −1 | −1 provisional |
| Rising | Stable | −1 | −1 | −2 |
| Rising | Rising | −1 | −2 | −3 |

## 8. Threshold and smoothing residual concerns

**Recommend a narrow later State-Classification review, not an automatic retuning.** B's fixed-band results are sufficient to prefer its current-condition semantics, but the short-lived August 2022 classifications affect the strength of the mapped Core interpretation at economically important transitions. Intermediate crosses only slightly below −25 bp for three observations; Long crosses only slightly above +25 bp for three observations. The same style of boundary behavior occurs in other requested windows, as shown below. It matters because a transient State label can convey an established direction more strongly than the underlying Values justify, even though the arithmetic is correct.

The review question is whether these marginal, brief Trend classifications communicate the intended broader condition adequately for a human consumer, or whether a narrowly specified classification treatment is needed. It is **not** to rescale ±25 automatically to suit the shorter horizon or to make historical examples cleaner. B's increased Stable occupancy is largely the mechanical consequence of retaining the band over a shorter interval; it is not sufficient evidence by itself to change the threshold. A larger threshold could also delay legitimate reversals. This task did not test any alternate classification or stabilization rule and cannot select one.

There is **no materially demonstrated need to alter five-observation smoothing now**. Some abrupt transitions are inevitably delayed by the specified endpoints, but the biggest A/C/D delays arise from horizons and shifted windows, and the identified B ambiguity is visible at the fixed State boundary. Inferring an optimal smoothing span from those observations would exceed the evidence and this task.

| Event | Tenor | Start | End | n | B State return | B bp range | Recent bp range |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1987 reversal | 6M | 1987-08-11 | 1987-08-11 | 1 | Stable → Rising → Stable | 26.8 to 26.8 | 58.4 to 58.4 |
| 2008 GFC | 10Y | 2008-09-30 | 2008-10-02 | 3 | Falling → Stable → Falling | -24.6 to -21.8 | -2.0 to 0.8 |
| 2008 GFC | 10Y | 2008-10-03 | 2008-10-09 | 5 | Stable → Falling → Stable | -33.0 to -26.6 | -7.4 to -1.2 |
| 2008 GFC | 30Y | 2008-09-26 | 2008-09-26 | 1 | Falling → Stable → Falling | -23.2 to -23.2 | -2.0 to -2.0 |
| 2022 relief | 10Y | 2022-08-08 | 2022-08-10 | 3 | Stable → Falling → Stable | -26.2 to -25.6 | -22.4 to -19.4 |
| 2022 relief | 30Y | 2022-08-26 | 2022-08-30 | 3 | Stable → Rising → Stable | 25.4 to 26.0 | 23.2 to 25.2 |
| 2023 long-end selloff | 10Y | 2023-07-21 | 2023-07-24 | 2 | Rising → Stable → Rising | 24.2 to 24.2 | 5.4 to 7.0 |

These local returns are adverse evidence against claiming that B is always a smoother or more stable broader-condition measure. They are not subsequent-return labels and do not imply that an alternative threshold would improve future decisions. Human review should address their significance before treating the Trend/Core package as accepted input to Macro Adjustment.

## 9. Final recommendation

**B — adopt 3M overlapping Trend as the provisional definition for human Trend/Core review.** Use `M5(t) − M5(t−63)` with the unchanged Recent Move `M5(t) − M5(t−21)`. The current four definitions are sufficient to recommend a horizon/construction; this evidence does not warrant inventing a fifth Trend model or selecting E.

| Criterion | Judgment supporting B | Cost or qualification retained |
| --- | --- | --- |
| Economic usefulness for Duration Evaluation | Represents current broader yield direction better after accumulated reversals, without moving the exposure assessment upstream or creating a market-wide preferred Duration. | It deliberately gives less weight to an older six-month regime; A can be more useful when relief is temporary, as in 2022. |
| Responsiveness to genuine broader change | 1980 becomes Rising after weeks of Recent increases; Short 2008 and Long 1984 corroborate the issue in other tenors/directions. | These additional long episodes are model-derived; neither their duration reduction nor later market performance is a correctness target. |
| Distinctness from Recent Move | Longer-tenor exact-State agreement remains far from complete; B retains broader States through short Recent pauses and preserves many mixed cases. | Short agreement is higher, partly because both measures often remain Stable. July 2022 gives a concrete case of nearly simultaneous Trend/Recent changes. |
| Persistence / stability | Trend remains substantially more persistent than Recent on common samples. | Switching and short return runs increase; near-threshold interpretation warrants a narrow follow-up. |
| Historical transition plausibility | Avoids much of A's moving-old-reference interpretation in sustained reversals and avoids the extra age in C/D. | No uniform advantage in 1987 or volatile 10Y September/October 2008; 2022 is genuine counterevidence. |
| Cross-tenor interpretation | Preserves different short-end and long-end conditions, including the 2023 contrast. | Same-date disagreement is not a metric to maximize or minimize. |
| Task-1 Core robustness | Settled sign/order structure survives; genuine mixed-state semantics remain useful. | One exact provisional preference has weaker evidence, and four cells remain unresolved. Numerical occupancy cannot supply ordinal calibration. |

A is not rejected as a mathematically valid longer-horizon condition; it is less suitable for the specified broader **current** role. C/D do not earn their additional age through demonstrably better Duration interpretation. Prolonged mixed states can be legitimate, as 2022 shows, but the repeated model-derived reversals demonstrate that not every prolonged A conflict deserves to remain classified as the old broader condition. The recommendation weighs these competing cases without a weighted score or a predictive-return ranking.

**Human review gate:** review B, unchanged Recent Move, the provisional Core table above, the four unresolved cells, and the narrow classification concern. No architecture, authoritative design, Task-1 file, threshold, smoothing setting, production evaluator, or macro rule was changed. Task 3 / Macro Adjustment and the optional classification review were not started.

## Reproduction, checks, and scope record

Created [analysis.py](analysis.py), [comparison.csv](comparison.csv), and this report under `validation/261002_duration/task2_trend/`; the validation README only adds links to the completed package. The script uses the Python standard library and the unchanged Task-1 fixture's definitions. It can be run from repository root:

```bash
python -m py_compile validation/261002_duration/task2_trend/analysis.py
python validation/261002_duration/task2_trend/analysis.py \
  --input validation/261002_duration/task1_core/results.csv \
  --output /tmp/duration_task2_comparison.csv \
  --diagnostics /tmp/duration_task2_diagnostics.md
cmp validation/261002_duration/task2_trend/comparison.csv /tmp/duration_task2_comparison.csv
git diff --check
```

The script emits every numerical diagnostic used in this report: availability, baseline matches, persistence, cross-tabs, change flags, cross-tenor disagreement, all mixed-episode duration statistics, longest episodes, original Task-1 episode membership, fixed 1980 paths/exit dates, the five event transition summaries, and short local State returns. The report's economic judgments are analyst-written. No model is selected by an automated objective. Full original-episode distributions are a documented supplemental exception to common-sample statistics, preserving Task-1 example identities.

`comparison.csv` has one row per tenor × accepted `as_of` on the common sample (38,246 rows). It retains segment/index lineage, fixed Recent Value/State, each variant's Trend Value/State/Rule Case/JSON candidates, and case/candidate-set change flags versus A. No duplicated raw-yield history is necessary; the frozen Task-1 CSV remains the source. Its source hash is verified on every invocation, and the script refuses to overwrite its input.

Comparison CSV SHA-256: `fdbb19bcbd12b8579c08f0d831cb84c70f0df406fec80f97f442ca2220eb0a59`.

Checks passed: required input hash; exact reproduction of all six baseline fields on 38,330 observations; independent Fraction-based window recalculation for every individually available Trend variant; inclusive State boundaries; segment/index and structural-gap exclusions; shifted-variant identities; truncation/no-lookahead checks within every accepted segment; syntax compilation; deterministic offline reproduction; and Git whitespace checks. The required 68/60-observation 1980 A episodes are explicitly asserted. No network data or nonstandard dependency is used. Production tests were not run because production code and outputs are unchanged.

Limitations carried forward: this is the Task-1 current historical vintage, not an as-published vintage backtest; the source/metadata discrepancy inside the quarantined 30Y gap remains unresolved; sample coverage differs by tenor; episodes overlap and are not independent statistical experiments; comparison windows and fixed thresholds compress continuous changes into coarse States; and historical interpretation cannot uniquely calibrate adjacent ordinal categories. Same-state or lower mixed-state frequencies are not performance measures. Recommendations remain subject to human review, and nothing is merged into `main` by this task.
