# Duration Task 1 — Core Rule Mapping validation

Prepared 2026-10-02 from `main` commit `70419d2` of `lbk209/bondview-v2`. This report follows the **revised Task-1 request**, including weak ordinal ordering and permitted category ties. The sole repository design authority consulted was [Bondview System Architecture](../../../docs/bondview_system_architecture.md). No other design document, previous model, or return series informed the findings.

The fixed calculations are mechanically usable, and the nine predefined events broadly support the mapping's directional interpretation. They do **not** establish that any ordinal category is uniquely calibrated. Four candidate cells receive provisional recommendations below; four remain unresolved. No settled-cell change is recommended. The principal follow-up concerns are a moving historical reference during reversals, concentration of Short observations in Stable states, and the difference between an economic improvement and a change in a coarse ordinal category.

These are research fixtures for the proposed Core, not a new production evaluation path. The standalone script retains raw observations, endpoint/reference Features, Component Values and States, and exposure-specific Core candidate sets in distinguishable columns. It neither imports nor modifies production Bondview logic. It performs no Macro Adjustment, Curve Evaluation, ETF ranking, return forecasting, or Task 2. Human review is required before any recommendation becomes accepted design.

## Sources, acceptance policy, and reproducibility

All three nominal constant-maturity series come from the Federal Reserve's H.15 family, distributed by FRED: [DGS6MO](https://fred.stlouisfed.org/series/DGS6MO), [DGS10](https://fred.stlouisfed.org/series/DGS10), and [DGS30](https://fred.stlouisfed.org/series/DGS30). Units are percent per annum, daily, not seasonally adjusted. Downloaded on 2026-10-02; requested upper cutoff 2026-10-01; last returned observation 2026-09-30. This is a current historical extract, **not an as-published historical vintage**. Ex-ante refers to the event selection, not to a claim of real-time vintage backtesting.

The [combined FRED download](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS6MO,DGS10,DGS30&cosd=1962-01-01&coed=2026-10-01) was checked against a [single-series DGS30 download](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS30&cosd=1977-01-01&coed=2026-10-01) and the [Federal Reserve H.15 CSV extract](https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&series=bf17364827e38702b42a58cf8eaa3f78&lastobs=&from=&to=&filetype=csv&label=include&layout=seriescolumn). The latter identifies the corresponding daily series as `RIFLGFCM06_N.B`, `RIFLGFCY10_N.B`, and `RIFLGFCY30_N.B`. Across 16,892 source dates per tenor, all numeric values agree; apparent differences are exclusively blank versus `ND` missing-value encodings. This is a same-source-family consistency check, not independent measurement confirmation.

**Material source discrepancy:** the downloaded FRED and H.15 extracts contain 994 numeric 30Y entries inside 2002-02-18 through 2006-02-08, despite [H.15 footnote 9](https://www.federalreserve.gov/releases/h15/) and the DGS30 notes documenting discontinuation and reintroduction on 2006-02-09. For example, the extracts return 5.54% on 2002-02-19 and 4.44% on 2005-07-25. The notes discuss a historical 20Y adjustment factor, but this study cannot establish the provenance of these particular entries. They are **not accepted as valid DGS30 observations**. No adjustment-factor estimate or substitute maturity is used. All 1,038 source-calendar rows in that interval are explicitly marked `documented_structural_gap`; the 994 returned numeric values remain in `yield_pct` solely for audit. They never enter a Feature, State, episode, or diagnostic denominator. This conservative exclusion is a disclosed data limitation, not a claim that the discrepancy has been explained.

After the gap, the first 130 valid 30Y observations rebuild the history. Long is therefore unavailable through 2006-08-15 and resumes on 2006-08-16. The accepted 30Y raw segments are 1977-02-15–2002-02-15 and 2006-02-09–2026-09-30 (11,408 accepted observations). The script also treats any separation greater than seven calendar days between accepted observations as a continuity break; the documented 30Y gap is the only such break in this extract. The small gaps listed below are processed using valid-observation indexing, not filled. No data are interpolated by this study. Treasury's construction of a constant-maturity yield is distinct from filling missing dates here.

**Observation convention.** The analytical sample consists of actual accepted observation dates: `as_of` equals the date indexed by `t`. Thus the latest valid observation on or before each analytical `as_of` is itself. Source-calendar rows without a yield are retained as unavailable raw rows and are not counted again as stale analytical observations. This is not a calendar-day expansion. Weekend or holiday queries are outside the CSV's analytical sampling grid; their latest-observation interpretation would refer back to the preceding accepted observation, without producing another independent observation. No results are carried across the structural discontinuation.

For each continuous tenor segment, the endpoint is the mean of indices `t-4` through `t`. Recent reference uses `t-25` through `t-21`; Trend reference uses `t-130` through `t-126`. A complete Core requires 131 observations including `t`. Values are endpoint minus reference, in basis points; Decimal arithmetic prevents a mathematically exact threshold from moving out of Stable because of binary rounding. Thresholds are inclusive at ±10 bp for Recent Move and ±25 bp for Trend. The Trend includes the latest month. Absolute yield level never enters the Rule Mapping.

Each tenor's Analysis-A and Analysis-C denominator is its complete Task-1 sample with both Components available. Recent Move can be calculated earlier during warmup and is retained in the CSV, but these partial rows do not enter complete-Core diagnostics. Common-date statistics require all three complete results. Episode duration means **number of valid observations**, not calendar days; first/last sample episodes may be censored. Samples differ substantially across tenors, so their full-sample percentages are not controlled comparisons of economic sensitivity.

The scale is ordinal: −3 Strongly Unfavorable; −2 Unfavorable; −1 Mildly Unfavorable; 0 Neutral; +1 Mildly Favorable; +2 Favorable; +3 Strongly Favorable. `core_candidates` contains a JSON array: a singleton is settled and a two-element array preserves the unresolved cell. Arrays use ascending numeric order, so the lower candidate in `[-2,-1]` is −2. No category averages, multiplication, cardinal differences, fitted thresholds, or subsequent-return labels are used. The two aggregate candidate scenarios in Analysis A are distributions, not adopted mappings. All combinations satisfy the requested **weak** within-exposure and comparable-condition cross-exposure ordering; ties are legitimate.

The starting mapping is reproduced here for review; these remain the candidates used in every observation and in Analyses A and B.

| Trend | Recent Move | Short | Intermediate | Long |
| --- | --- | --- | --- | --- |
| Falling | Falling | +1 | +2 | +3 |
| Falling | Stable | +1 | +1 | +2 |
| Falling | Rising | [0,+1] | +1 | [+1,+2] |
| Stable | Falling | [0,+1] | +1 | [+1,+2] |
| Stable | Stable | 0 | 0 | 0 |
| Stable | Rising | [−1,0] | −1 | [−2,−1] |
| Rising | Falling | [−1,0] | −1 | [−2,−1] |
| Rising | Stable | −1 | −1 | −2 |
| Rising | Rising | −1 | −2 | −3 |

The [observation CSV](results.csv) contains 50,676 rows, including 38,330 complete Core observations. Its full raw-date grid preserves every source date and tenor, including pre-inception, routine missing, warmup, and structural-gap rows. `availability` controls eligibility; never infer eligibility merely from a nonblank `yield_pct`. `segment` and `observation_index` document valid-observation indexing; reference start/end dates and smoothed values expose the calculation lineage. `rule_episode_id` identifies maximal full-sample case episodes. Filtering the four mixed cases and grouping this ID reproduces all Analysis-C episodes. `historical_event` applies the nine inclusive user-specified windows, including unavailable rows.

Reproduce numerical results offline with Python 3.12 and the standard library:

```bash
python validation/261002_duration/task1_core/analysis.py \
  --replay validation/261002_duration/task1_core/results.csv \
  --output /tmp/duration_task1_replayed.csv \
  --diagnostics /tmp/duration_task1_diagnostics.md
cmp validation/261002_duration/task1_core/results.csv /tmp/duration_task1_replayed.csv
python -m py_compile validation/261002_duration/task1_core/analysis.py
```

Alternatively pass the combined FRED CSV using `--input` instead of `--replay`. The script regenerates numerical evidence, not this report's economic judgments. Offline replay is preferred for an exact snapshot; live-source revisions can change a new download.

Snapshot SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| Combined FRED source bytes | `ccdbfcc64ec75a756d03012810d119cfe841efee3c1a1c3009326f9b0c7454e3` |
| Single-series DGS30 source bytes | `243a5757448688d1d3ac13d0415e5e287de4bc80806f5a4dc03839f02226ebe1` |
| Federal Reserve extract bytes | `11fcceee63b3827fd4f830f62bcbf456786fae2228ce78cc7080ac3ead3b9b73` |
| Committed results CSV | `3316d1a8adece1e27e529a51531713a4cb173be22039100124853321daa66b18` |

Only the results CSV is committed as the data snapshot; it preserves the downloaded values needed for replay. The auxiliary source downloads were temporary consistency checks. Their URLs, identifiers, encodings, and hashes are recorded above.

## Data coverage

| Series | Downloaded nonmissing range | Downloaded nonmissing n | Calculable outer range | Valid n | Lookback exclusions |
| --- | --- | --- | --- | --- | --- |
| DGS6MO | 1981-09-01 – 2026-09-30 | 11270 | 1982-03-16 – 2026-09-30 | 11140 | 130 |
| DGS10 | 1962-01-02 – 2026-09-30 | 16172 | 1962-07-10 – 2026-09-30 | 16042 | 130 |
| DGS30 | 1977-02-15 – 2026-09-30 | 12402 | 1977-08-23 – 2026-09-30 | 11148 | 260 |

- 6M segment 1: raw 1981-09-01 through 2026-09-30; lookback exclusions 1981-09-01 through 1982-03-15 (130 observations); first calculable 1982-03-16.


6M: gaps longer than four calendar days between observations: [('1982-02-11', '1982-02-16', 5)].

- 10Y segment 1: raw 1962-01-02 through 2026-09-30; lookback exclusions 1962-01-02 through 1962-07-09 (130 observations); first calculable 1962-07-10.


10Y: gaps longer than four calendar days between observations: [('1971-02-11', '1971-02-16', 5), ('1973-12-21', '1973-12-26', 5), ('1978-05-26', '1978-05-31', 5), ('1982-02-11', '1982-02-16', 5)].

- 30Y segment 1: raw 1977-02-15 through 2002-02-15; lookback exclusions 1977-02-15 through 1977-08-22 (130 observations); first calculable 1977-08-23.

- 30Y segment 2: raw 2006-02-09 through 2026-09-30; lookback exclusions 2006-02-09 through 2006-08-15 (130 observations); first calculable 2006-08-16.


30Y: gaps longer than four calendar days between observations: [('1978-05-26', '1978-05-31', 5), ('1982-02-11', '1982-02-16', 5), ('2002-02-15', '2006-02-09', 1455)].

## Analysis A — numerical diagnostics

### Short / 6M

**trend_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 3529 (31.68%) | 47 | 75.09 | 19 | 455 | 5 |
| Stable | 4329 (38.86%) | 91 | 47.57 | 11 | 1534 | 4 |
| Rising | 3282 (29.46%) | 45 | 72.93 | 15 | 593 | 1 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 3482 | 47 | 0 |
| Stable | 46 | 4238 | 45 |
| Rising | 0 | 44 | 3237 |

Switching: 182 (1.63%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

**recent_move_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 2632 (23.63%) | 124 | 21.23 | 16.5 | 119 | 3 |
| Stable | 5827 (52.31%) | 245 | 23.78 | 8 | 1567 | 16 |
| Rising | 2681 (24.07%) | 125 | 21.45 | 14 | 242 | 6 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 2508 | 123 | 1 |
| Stable | 121 | 5582 | 124 |
| Rising | 2 | 122 | 2556 |

Switching: 493 (4.43%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

| Rule Case | Observations |
| --- | --- |
| Falling × Falling | 1785 (16.02%) |
| Falling × Stable | 1234 (11.08%) |
| Falling × Rising | 510 (4.58%) |
| Stable × Falling | 486 (4.36%) |
| Stable × Stable | 3449 (30.96%) |
| Stable × Rising | 394 (3.54%) |
| Rising × Falling | 361 (3.24%) |
| Rising × Stable | 1144 (10.27%) |
| Rising × Rising | 1777 (15.95%) |

Four mixed cases combined: 1751 (15.72%).

| Core candidate set (singletons settled) | Observations |
| --- | --- |
| [-1,0] | 755 (6.78%) |
| [-1] | 2921 (26.22%) |
| [0,1] | 996 (8.94%) |
| [0] | 3449 (30.96%) |
| [1] | 3019 (27.10%) |

| Ordinal category | All lower candidates | All higher candidates |
| --- | --- | --- |
| -3 | 0 (0.00%) | 0 (0.00%) |
| -2 | 0 (0.00%) | 0 (0.00%) |
| -1 | 3676 (33.00%) | 2921 (26.22%) |
| 0 | 4445 (39.90%) | 4204 (37.74%) |
| 1 | 3019 (27.10%) | 4015 (36.04%) |
| 2 | 0 (0.00%) | 0 (0.00%) |
| 3 | 0 (0.00%) | 0 (0.00%) |

### Intermediate / 10Y

**trend_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 5282 (32.93%) | 114 | 46.33 | 19.0 | 473 | 8 |
| Stable | 4996 (31.14%) | 230 | 21.72 | 12.5 | 834 | 8 |
| Rising | 5764 (35.93%) | 116 | 49.69 | 22.0 | 365 | 9 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 5168 | 114 | 0 |
| Stable | 114 | 4766 | 116 |
| Rising | 0 | 115 | 5648 |

Switching: 459 (2.86%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

**recent_move_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 5206 (32.45%) | 291 | 17.89 | 13 | 88 | 17 |
| Stable | 5515 (34.38%) | 581 | 9.49 | 6 | 403 | 39 |
| Rising | 5321 (33.17%) | 291 | 18.29 | 14 | 83 | 17 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 4915 | 291 | 0 |
| Stable | 291 | 4934 | 290 |
| Rising | 0 | 290 | 5030 |

Switching: 1162 (7.24%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

| Rule Case | Observations |
| --- | --- |
| Falling × Falling | 2623 (16.35%) |
| Falling × Stable | 1576 (9.82%) |
| Falling × Rising | 1083 (6.75%) |
| Stable × Falling | 1421 (8.86%) |
| Stable × Stable | 2344 (14.61%) |
| Stable × Rising | 1231 (7.67%) |
| Rising × Falling | 1162 (7.24%) |
| Rising × Stable | 1595 (9.94%) |
| Rising × Rising | 3007 (18.74%) |

Four mixed cases combined: 4897 (30.53%).

| Core candidate set (singletons settled) | Observations |
| --- | --- |
| [-1] | 3988 (24.86%) |
| [-2] | 3007 (18.74%) |
| [0] | 2344 (14.61%) |
| [1] | 4080 (25.43%) |
| [2] | 2623 (16.35%) |

| Ordinal category | All lower candidates | All higher candidates |
| --- | --- | --- |
| -3 | 0 (0.00%) | 0 (0.00%) |
| -2 | 3007 (18.74%) | 3007 (18.74%) |
| -1 | 3988 (24.86%) | 3988 (24.86%) |
| 0 | 2344 (14.61%) | 2344 (14.61%) |
| 1 | 4080 (25.43%) | 4080 (25.43%) |
| 2 | 2623 (16.35%) | 2623 (16.35%) |
| 3 | 0 (0.00%) | 0 (0.00%) |

### Long / 30Y

**trend_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 4103 (36.80%) | 85 | 48.27 | 15 | 346 | 5 |
| Stable | 3202 (28.72%) | 166 | 19.29 | 13.5 | 95 | 7 |
| Rising | 3843 (34.47%) | 81 | 47.44 | 14 | 220 | 5 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 4018 | 85 | 0 |
| Stable | 85 | 3036 | 80 |
| Rising | 0 | 80 | 3762 |

Switching: 330 (2.96%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

**recent_move_state**

| State | Observations | Episodes | Mean duration | Median | Max | One-observation episodes |
| --- | --- | --- | --- | --- | --- | --- |
| Falling | 3848 (34.52%) | 216 | 17.81 | 13.0 | 102 | 7 |
| Stable | 3570 (32.02%) | 435 | 8.21 | 6 | 49 | 24 |
| Rising | 3730 (33.46%) | 218 | 17.11 | 11.0 | 82 | 11 |

| From / to | Falling | Stable | Rising |
| --- | --- | --- | --- |
| Falling | 3632 | 216 | 0 |
| Stable | 216 | 3135 | 218 |
| Rising | 0 | 217 | 3512 |

Switching: 867 (7.78%) of adjacent valid within-segment pairs. Diagonal counts are persistence.

| Rule Case | Observations |
| --- | --- |
| Falling × Falling | 2034 (18.25%) |
| Falling × Stable | 1264 (11.34%) |
| Falling × Rising | 805 (7.22%) |
| Stable × Falling | 1115 (10.00%) |
| Stable × Stable | 1220 (10.94%) |
| Stable × Rising | 867 (7.78%) |
| Rising × Falling | 699 (6.27%) |
| Rising × Stable | 1086 (9.74%) |
| Rising × Rising | 2058 (18.46%) |

Four mixed cases combined: 3486 (31.27%).

| Core candidate set (singletons settled) | Observations |
| --- | --- |
| [-2,-1] | 1566 (14.05%) |
| [-2] | 1086 (9.74%) |
| [-3] | 2058 (18.46%) |
| [0] | 1220 (10.94%) |
| [1,2] | 1920 (17.22%) |
| [2] | 1264 (11.34%) |
| [3] | 2034 (18.25%) |

| Ordinal category | All lower candidates | All higher candidates |
| --- | --- | --- |
| -3 | 2058 (18.46%) | 2058 (18.46%) |
| -2 | 2652 (23.79%) | 1086 (9.74%) |
| -1 | 0 (0.00%) | 1566 (14.05%) |
| 0 | 1220 (10.94%) | 1220 (10.94%) |
| 1 | 1920 (17.22%) | 0 (0.00%) |
| 2 | 1264 (11.34%) | 3184 (28.56%) |
| 3 | 2034 (18.25%) | 2034 (18.25%) |

### Cross-exposure common-date comparison

| Distinct cases across three tenors | Dates |
| --- | --- |
| 1 | 2401 (23.97%) |
| 2 | 5942 (59.33%) |
| 3 | 1673 (16.70%) |

Representative disagreements: first common date with three distinct cases in each predefined event (deterministic; no return filter).

| Event | Date | 6M | 10Y | 30Y |
| --- | --- | --- | --- | --- |
| GFC | 2008-09-09 | Rising × Stable (29.8, -4.6 bp) | Stable × Falling (7.0, -33.0 bp) | Falling × Falling (-27.6, -33.6 bp) |
| Taper tantrum | 2013-05-15 | Stable × Stable (-6.4, -1.0 bp) | Stable × Rising (22.4, 13.0 bp) | Rising × Rising (28.4, 16.8 bp) |
| 2022 tightening | 2022-07-14 | Rising × Rising (257.8, 91.6 bp) | Rising × Falling (123.6, -14.4 bp) | Rising × Stable (105.8, -6.8 bp) |
| COVID | 2020-02-07 | Falling × Stable (-46.0, 1.0 bp) | Stable × Falling (-24.2, -22.8 bp) | Falling × Falling (-30.4, -22.8 bp) |
| 2023 long-end selloff | 2023-07-05 | Rising × Stable (74.4, 2.6 bp) | Stable × Rising (-0.8, 15.0 bp) | Stable × Stable (-5.6, -0.6 bp) |

### Analysis-A interpretation

**Component calculation / State Classification:** there is no full-sample absence of Stable or evidence of pathological daily flipping. Trend Stable accounts for 38.86% / 31.14% / 28.72% of Short / Intermediate / Long observations; Recent Stable accounts for 52.31% / 34.38% / 32.02%. Trend switches on 1.63% / 2.86% / 2.96% of adjacent eligible pairs, versus 4.43% / 7.24% / 7.78% for Recent Move. Median Trend-state episodes range from 11 to 22 observations, while median Recent-state episodes range from 6 to 16.5. The faster Component actually changes faster. One-observation runs occur but are a minority (see counts), not the prevailing regime. Five-day endpoints moderate noise without implying a daily execution signal.

Short's Recent Stable majority and Stable × Stable share of 30.96% deserve attention, but do not make the fixture unusable. Intermediate's largest case is Rising × Rising at 18.74%; Long's is the same case at 18.46%. Across individual cases the minimum shares are 3.24%, 6.75%, and 6.27%, respectively: none is effectively unreachable or merely a handful of observations. Mixed cases occupy 15.72% / 30.53% / 31.27%; resolving their semantics matters especially for the two longer exposures. Unequal frequencies alone are not defects. Fixed absolute change bands naturally classify long stretches with small short-rate changes as Stable; no level-dependent rule is introduced to counteract that.

**Core mapping:** candidate uncertainty affects 1,751 Short observations and 3,486 Long observations, but no Intermediate observations. Core category concentrations partly reflect the intended compression: Short never reaches ±2 or ±3. That is consistent with mild positive-duration exposure, not evidence that Short is strongly attractive when longer exposure is penalized. The unresolved candidates alter how many observations are Neutral versus Mildly directional for Short, and Mildly directional versus directional for Long. Historical frequency cannot identify a uniquely correct category.

**Cross-tenor behavior:** of 10,016 common calculable dates, all three cases agree on 2,401 (23.97%); exactly two cases occur on 5,942 (59.33%); three different cases occur on 1,673 (16.70%). Thus some disagreement occurs on 76.03%. The examples are explainable directly from the tenor-local changes. On 2008-09-09 Short retained a positive six-month change while 30Y had fallen over both horizons. On 2013-05-15 the short tenor barely moved while 30Y rose. On 2022-07-14 the 6M recent increase coexisted with a recent 10Y decline. None requires one common market verdict or a rule-table error. Magnitudes in the table describe yield changes, not cardinal Core differences.

**Usability judgment:** use the fixed baseline for historical review without retuning. There is no serious Rule Case coverage failure or reversal of the weak ordinal orders. Retain three limitations: sample/regime dependence of occupancy; lags and moving reference endpoints during reversals; the documented 30Y data interruption. The longest-run supplemental inspection appears after Analysis C so it is not confused with predefined-event evidence.

## Analysis B — predefined event evidence

All valid daily observations are in the CSV. Tables below select the first and last valid date of every calendar month, before looking at states. Transition lists additionally include every Rule Case episode within each event; durations count observations. No calendar dates are filled.

### Volcker (Anchor), 1981-07-01 through 1981-10-31

**Interpretation.** At the beginning, 10Y and 30Y are Rising × Rising and map to −2 and −3. Those categories occupy 80.00% and 88.24% of the window, respectively. Intermediate first improves out of that case on September 23; Long on October 7. The October paths include both renewed increases and recent declines, ending Rising × Falling with still-positive Trend Values of +124.2 and +136.8 bp. Less unfavorable results late in the window are supported by the observed reversal; they do not invalidate the rising-rate expectation. Short cannot be assessed anywhere in this window: DGS6MO starts September 1 and does not have the required history until March 1982. This is a data limitation, not missing evidence to be supplied by a bill proxy. No material mapping contradiction is found in the available exposures.


**Short / 6M**

Unavailable: no calculable observations in this window.

**Intermediate / 10Y**

All 85 observations: [-1]: 17 (20.00%); [-2]: 68 (80.00%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1981-07-01 | 14.04 | 147.2 | Rising | 23.2 | Rising | Rising × Rising | [-2] |
| 1981-07-31 | 14.67 | 182.2 | Rising | 79.6 | Rising | Rising × Rising | [-2] |
| 1981-08-03 | 14.95 | 195.8 | Rising | 85.0 | Rising | Rising × Rising | [-2] |
| 1981-08-31 | 15.41 | 188.8 | Rising | 74.6 | Rising | Rising × Rising | [-2] |
| 1981-09-01 | 15.41 | 186.8 | Rising | 65.4 | Rising | Rising × Rising | [-2] |
| 1981-09-30 | 15.84 | 241.0 | Rising | 31.2 | Rising | Rising × Rising | [-2] |
| 1981-10-01 | 15.75 | 251.6 | Rising | 38.8 | Rising | Rising × Rising | [-2] |
| 1981-10-30 | 14.63 | 124.2 | Rising | -39.4 | Falling | Rising × Falling | [-1] |

Rule Case path (event-clipped episodes): 1981-07-01–1981-09-22 Rising × Rising (58); 1981-09-23–1981-09-25 Rising × Stable (3); 1981-09-28–1981-10-05 Rising × Rising (6); 1981-10-06–1981-10-06 Rising × Stable (1); 1981-10-07–1981-10-20 Rising × Falling (9); 1981-10-21–1981-10-21 Rising × Stable (1); 1981-10-22–1981-10-27 Rising × Rising (4); 1981-10-28–1981-10-28 Rising × Stable (1); 1981-10-29–1981-10-30 Rising × Falling (2).

**Long / 30Y**

All 85 observations: [-2,-1]: 6 (7.06%); [-2]: 4 (4.71%); [-3]: 75 (88.24%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1981-07-01 | 13.47 | 132.8 | Rising | 10.8 | Rising | Rising × Rising | [-3] |
| 1981-07-31 | 13.96 | 153.0 | Rising | 63.4 | Rising | Rising × Rising | [-3] |
| 1981-08-03 | 14.27 | 166.4 | Rising | 70.6 | Rising | Rising × Rising | [-3] |
| 1981-08-31 | 14.78 | 160.8 | Rising | 74.8 | Rising | Rising × Rising | [-3] |
| 1981-09-01 | 14.70 | 159.8 | Rising | 65.2 | Rising | Rising × Rising | [-3] |
| 1981-09-30 | 15.19 | 224.4 | Rising | 42.0 | Rising | Rising × Rising | [-3] |
| 1981-10-01 | 15.14 | 235.8 | Rising | 49.2 | Rising | Rising × Rising | [-3] |
| 1981-10-30 | 14.36 | 136.8 | Rising | -16.4 | Falling | Rising × Falling | [-2,-1] |

Rule Case path (event-clipped episodes): 1981-07-01–1981-10-06 Rising × Rising (68); 1981-10-07–1981-10-07 Rising × Stable (1); 1981-10-08–1981-10-15 Rising × Falling (5); 1981-10-16–1981-10-19 Rising × Stable (2); 1981-10-20–1981-10-28 Rising × Rising (7); 1981-10-29–1981-10-29 Rising × Stable (1); 1981-10-30–1981-10-30 Rising × Falling (1).

### 1994 tightening (Anchor), 1994-02-01 through 1994-11-30

**Interpretation.** Short and Intermediate begin Neutral. Long begins Favorable for four observations because its own Trend is still Falling, then passes through Stable before becoming unfavorable. This is a short initial transition, not persistent optimism during the selloff. Rising × Rising starts February 14 / 22 / 23 for Short / Intermediate / Long. Their principal unfavorable categories dominate thereafter: Short is settled −1 on 91.83% of observations; Intermediate −2 on 62.98%; Long −3 on 63.46%. June and August recent declines temporarily reduce the penalty without erasing the broader rising condition. At the end, Short is Rising × Rising while both longer tenors are Rising × Stable. Results −1 / −1 / −2 preserve the distinct recent paths. The ex-ante expectation is supported without demanding equal transition dates or forbidding ties.


**Short / 6M**

All 208 observations: [-1,0]: 11 (5.29%); [-1]: 191 (91.83%); [0]: 6 (2.88%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1994-02-01 | 3.29 | -8.2 | Stable | -7.2 | Stable | Stable × Stable | [0] |
| 1994-02-28 | 3.72 | 50.6 | Rising | 47.8 | Rising | Rising × Rising | [-1] |
| 1994-03-01 | 3.82 | 54.4 | Rising | 51.6 | Rising | Rising × Rising | [-1] |
| 1994-03-31 | 3.92 | 81.0 | Rising | 18.8 | Rising | Rising × Rising | [-1] |
| 1994-04-04 | 4.19 | 86.4 | Rising | 22.0 | Rising | Rising × Rising | [-1] |
| 1994-04-29 | 4.45 | 115.6 | Rising | 47.6 | Rising | Rising × Rising | [-1] |
| 1994-05-02 | 4.57 | 118.4 | Rising | 51.2 | Rising | Rising × Rising | [-1] |
| 1994-05-31 | 4.87 | 142.6 | Rising | 38.6 | Rising | Rising × Rising | [-1] |
| 1994-06-01 | 4.83 | 143.6 | Rising | 35.2 | Rising | Rising × Rising | [-1] |
| 1994-06-30 | 4.83 | 146.2 | Rising | -4.2 | Stable | Rising × Stable | [-1] |
| 1994-07-01 | 4.84 | 147.2 | Rising | -3.0 | Stable | Rising × Stable | [-1] |
| 1994-07-29 | 4.87 | 177.8 | Rising | 25.2 | Rising | Rising × Rising | [-1] |
| 1994-08-01 | 4.93 | 176.4 | Rising | 21.8 | Rising | Rising × Rising | [-1] |
| 1994-08-31 | 5.03 | 132.4 | Rising | 11.4 | Rising | Rising × Rising | [-1] |
| 1994-09-01 | 4.99 | 128.2 | Rising | 12.8 | Rising | Rising × Rising | [-1] |
| 1994-09-30 | 5.43 | 147.2 | Rising | 33.6 | Rising | Rising × Rising | [-1] |
| 1994-10-03 | 5.61 | 145.2 | Rising | 39.0 | Rising | Rising × Rising | [-1] |
| 1994-10-31 | 5.72 | 125.4 | Rising | 29.6 | Rising | Rising × Rising | [-1] |
| 1994-11-01 | 5.75 | 121.0 | Rising | 29.4 | Rising | Rising × Rising | [-1] |
| 1994-11-30 | 6.22 | 129.8 | Rising | 38.4 | Rising | Rising × Rising | [-1] |

Rule Case path (event-clipped episodes): 1994-02-01–1994-02-08 Stable × Stable (6); 1994-02-09–1994-02-11 Stable × Rising (3); 1994-02-14–1994-06-06 Rising × Rising (77); 1994-06-07–1994-06-08 Rising × Stable (2); 1994-06-09–1994-06-20 Rising × Falling (8); 1994-06-21–1994-07-06 Rising × Stable (11); 1994-07-07–1994-08-03 Rising × Rising (20); 1994-08-04–1994-08-12 Rising × Stable (7); 1994-08-15–1994-08-25 Rising × Rising (9); 1994-08-26–1994-08-29 Rising × Stable (2); 1994-08-30–1994-09-02 Rising × Rising (4); 1994-09-06–1994-09-20 Rising × Stable (11); 1994-09-21–1994-11-30 Rising × Rising (48).

**Intermediate / 10Y**

All 208 observations: [-1]: 71 (34.13%); [-2]: 131 (62.98%); [0]: 6 (2.88%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1994-02-01 | 5.77 | -14.8 | Stable | -3.6 | Stable | Stable × Stable | [0] |
| 1994-02-28 | 6.15 | 57.2 | Rising | 40.2 | Rising | Rising × Rising | [-2] |
| 1994-03-01 | 6.28 | 66.2 | Rising | 45.8 | Rising | Rising × Rising | [-2] |
| 1994-03-31 | 6.77 | 132.6 | Rising | 46.8 | Rising | Rising × Rising | [-2] |
| 1994-04-04 | 7.16 | 145.6 | Rising | 55.2 | Rising | Rising × Rising | [-2] |
| 1994-04-29 | 7.06 | 156.4 | Rising | 35.6 | Rising | Rising × Rising | [-2] |
| 1994-05-02 | 7.09 | 156.0 | Rising | 32.0 | Rising | Rising × Rising | [-2] |
| 1994-05-31 | 7.17 | 130.4 | Rising | 18.8 | Rising | Rising × Rising | [-2] |
| 1994-06-01 | 7.12 | 131.0 | Rising | 14.6 | Rising | Rising × Rising | [-2] |
| 1994-06-30 | 7.34 | 152.0 | Rising | 12.0 | Rising | Rising × Rising | [-2] |
| 1994-07-01 | 7.34 | 152.8 | Rising | 15.8 | Rising | Rising × Rising | [-2] |
| 1994-07-29 | 7.12 | 151.0 | Rising | 6.0 | Stable | Rising × Stable | [-1] |
| 1994-08-01 | 7.13 | 149.2 | Rising | -1.6 | Stable | Rising × Stable | [-1] |
| 1994-08-31 | 7.19 | 100.0 | Rising | 3.4 | Stable | Rising × Stable | [-1] |
| 1994-09-01 | 7.19 | 95.4 | Rising | 6.4 | Stable | Rising × Stable | [-1] |
| 1994-09-30 | 7.62 | 90.2 | Rising | 37.0 | Rising | Rising × Rising | [-2] |
| 1994-10-03 | 7.66 | 81.0 | Rising | 40.8 | Rising | Rising × Rising | [-2] |
| 1994-10-31 | 7.81 | 87.2 | Rising | 26.2 | Rising | Rising × Rising | [-2] |
| 1994-11-01 | 7.91 | 82.4 | Rising | 25.8 | Rising | Rising × Rising | [-2] |
| 1994-11-30 | 7.91 | 73.2 | Rising | 0.6 | Stable | Rising × Stable | [-1] |

Rule Case path (event-clipped episodes): 1994-02-01–1994-02-08 Stable × Stable (6); 1994-02-09–1994-02-18 Stable × Rising (8); 1994-02-22–1994-05-18 Rising × Rising (60); 1994-05-19–1994-05-24 Rising × Stable (4); 1994-05-25–1994-06-01 Rising × Rising (5); 1994-06-02–1994-06-06 Rising × Stable (3); 1994-06-07–1994-06-17 Rising × Falling (9); 1994-06-20–1994-06-29 Rising × Stable (8); 1994-06-30–1994-07-20 Rising × Rising (14); 1994-07-21–1994-07-25 Rising × Stable (3); 1994-07-26–1994-07-28 Rising × Rising (3); 1994-07-29–1994-08-02 Rising × Stable (3); 1994-08-03–1994-08-10 Rising × Falling (6); 1994-08-11–1994-09-14 Rising × Stable (24); 1994-09-15–1994-11-25 Rising × Rising (49); 1994-11-28–1994-11-30 Rising × Stable (3).

**Long / 30Y**

All 208 observations: [-2,-1]: 23 (11.06%); [-2]: 46 (22.12%); [-3]: 132 (63.46%); [0]: 3 (1.44%); [2]: 4 (1.92%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1994-02-01 | 6.31 | -36.2 | Falling | -1.2 | Stable | Falling × Stable | [2] |
| 1994-02-28 | 6.67 | 47.4 | Rising | 37.4 | Rising | Rising × Rising | [-3] |
| 1994-03-01 | 6.79 | 53.6 | Rising | 42.8 | Rising | Rising × Rising | [-3] |
| 1994-03-31 | 7.11 | 102.2 | Rising | 30.2 | Rising | Rising × Rising | [-3] |
| 1994-04-04 | 7.43 | 113.0 | Rising | 37.2 | Rising | Rising × Rising | [-3] |
| 1994-04-29 | 7.31 | 126.4 | Rising | 24.2 | Rising | Rising × Rising | [-3] |
| 1994-05-02 | 7.33 | 125.4 | Rising | 21.6 | Rising | Rising × Rising | [-3] |
| 1994-05-31 | 7.44 | 108.4 | Rising | 18.4 | Rising | Rising × Rising | [-3] |
| 1994-06-01 | 7.39 | 110.2 | Rising | 15.6 | Rising | Rising × Rising | [-3] |
| 1994-06-30 | 7.63 | 129.8 | Rising | 13.6 | Rising | Rising × Rising | [-3] |
| 1994-07-01 | 7.62 | 129.4 | Rising | 16.0 | Rising | Rising × Rising | [-3] |
| 1994-07-29 | 7.39 | 121.8 | Rising | 4.0 | Stable | Rising × Stable | [-2] |
| 1994-08-01 | 7.41 | 121.0 | Rising | -3.0 | Stable | Rising × Stable | [-2] |
| 1994-08-31 | 7.46 | 74.8 | Rising | 2.4 | Stable | Rising × Stable | [-2] |
| 1994-09-01 | 7.46 | 71.2 | Rising | 5.0 | Stable | Rising × Stable | [-2] |
| 1994-09-30 | 7.82 | 78.0 | Rising | 33.4 | Rising | Rising × Rising | [-3] |
| 1994-10-03 | 7.86 | 70.4 | Rising | 36.4 | Rising | Rising × Rising | [-3] |
| 1994-10-31 | 7.97 | 78.2 | Rising | 19.6 | Rising | Rising × Rising | [-3] |
| 1994-11-01 | 8.06 | 74.0 | Rising | 19.2 | Rising | Rising × Rising | [-3] |
| 1994-11-30 | 7.99 | 58.8 | Rising | -4.8 | Stable | Rising × Stable | [-2] |

Rule Case path (event-clipped episodes): 1994-02-01–1994-02-04 Falling × Stable (4); 1994-02-07–1994-02-09 Stable × Stable (3); 1994-02-10–1994-02-22 Stable × Rising (8); 1994-02-23–1994-05-18 Rising × Rising (59); 1994-05-19–1994-05-25 Rising × Stable (5); 1994-05-26–1994-06-02 Rising × Rising (5); 1994-06-03–1994-06-07 Rising × Stable (3); 1994-06-08–1994-06-16 Rising × Falling (7); 1994-06-17–1994-06-20 Rising × Stable (2); 1994-06-21–1994-06-24 Rising × Rising (4); 1994-06-27–1994-06-29 Rising × Stable (3); 1994-06-30–1994-07-20 Rising × Rising (14); 1994-07-21–1994-08-02 Rising × Stable (9); 1994-08-03–1994-08-12 Rising × Falling (8); 1994-08-15–1994-09-12 Rising × Stable (20); 1994-09-13–1994-11-23 Rising × Rising (50); 1994-11-25–1994-11-30 Rising × Stable (4).

### Russia LTCM (Anchor), 1998-08-01 through 1998-10-31

**Interpretation.** All three begin Stable × Stable; their favorable transitions do not occur simultaneously. Long moves first to Falling × Stable on August 10 and Falling × Falling on August 17, Intermediate to Falling × Falling on August 25, and Short through Stable × Falling on August 28 to Falling × Falling on August 31. The latter case occupies 68.25% / 66.67% / 74.60% of the window, mapping to +1 / +2 / +3 on each tenor's own dates. By the end, Short still has a recent decline, whereas 10Y and 30Y Recent Move has become Stable, reducing their categories to +1 and +2. Those legitimate ties and reductions describe decelerating declines. This event supports favorable duration interpretation and comparative sensitivity, not a forecast of continued yield falls.


**Short / 6M**

All 63 observations: [0,1]: 1 (1.59%); [0]: 19 (30.16%); [1]: 43 (68.25%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1998-08-03 | 5.25 | -5.8 | Stable | -2.2 | Stable | Stable × Stable | [0] |
| 1998-08-31 | 5.03 | -25.2 | Falling | -13.2 | Falling | Falling × Falling | [1] |
| 1998-09-01 | 4.97 | -28.4 | Falling | -17.4 | Falling | Falling × Falling | [1] |
| 1998-09-30 | 4.49 | -68.4 | Falling | -52.0 | Falling | Falling × Falling | [1] |
| 1998-10-01 | 4.36 | -72.6 | Falling | -52.2 | Falling | Falling × Falling | [1] |
| 1998-10-30 | 4.36 | -105.0 | Falling | -30.4 | Falling | Falling × Falling | [1] |

Rule Case path (event-clipped episodes): 1998-08-03–1998-08-27 Stable × Stable (19); 1998-08-28–1998-08-28 Stable × Falling (1); 1998-08-31–1998-10-30 Falling × Falling (43).

**Intermediate / 10Y**

All 63 observations: [0]: 16 (25.40%); [1]: 5 (7.94%); [2]: 42 (66.67%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1998-08-03 | 5.46 | -11.8 | Stable | 5.0 | Stable | Stable × Stable | [0] |
| 1998-08-31 | 5.05 | -52.4 | Falling | -34.4 | Falling | Falling × Falling | [2] |
| 1998-09-01 | 5.05 | -59.0 | Falling | -38.2 | Falling | Falling × Falling | [2] |
| 1998-09-30 | 4.44 | -109.8 | Falling | -57.8 | Falling | Falling × Falling | [2] |
| 1998-10-01 | 4.33 | -113.6 | Falling | -60.0 | Falling | Falling × Falling | [2] |
| 1998-10-30 | 4.64 | -112.4 | Falling | 5.2 | Stable | Falling × Stable | [1] |

Rule Case path (event-clipped episodes): 1998-08-03–1998-08-24 Stable × Stable (16); 1998-08-25–1998-10-23 Falling × Falling (42); 1998-10-26–1998-10-30 Falling × Stable (5).

**Long / 30Y**

All 63 observations: [0]: 5 (7.94%); [2]: 11 (17.46%); [3]: 47 (74.60%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1998-08-03 | 5.67 | -16.0 | Stable | 9.8 | Stable | Stable × Stable | [0] |
| 1998-08-31 | 5.30 | -59.4 | Falling | -34.6 | Falling | Falling × Falling | [3] |
| 1998-09-01 | 5.34 | -63.8 | Falling | -36.0 | Falling | Falling × Falling | [3] |
| 1998-09-30 | 4.98 | -84.6 | Falling | -28.4 | Falling | Falling × Falling | [3] |
| 1998-10-01 | 4.90 | -87.4 | Falling | -31.4 | Falling | Falling × Falling | [3] |
| 1998-10-30 | 5.15 | -90.6 | Falling | 1.4 | Stable | Falling × Stable | [2] |

Rule Case path (event-clipped episodes): 1998-08-03–1998-08-07 Stable × Stable (5); 1998-08-10–1998-08-14 Falling × Stable (5); 1998-08-17–1998-10-22 Falling × Falling (47); 1998-10-23–1998-10-30 Falling × Stable (6).

### GFC (Anchor), 2008-09-01 through 2008-12-31

**Interpretation.** The full window is not a smooth decline. Short begins Neutral; Intermediate and Long begin Stable × Falling. Short briefly turns unfavorable in early September, while the longer tenors have different broader conditions. Intermediate is unfavorable on 21 of 83 observations, with yields rising again around late September/October; its October 14–20 Rising × Rising run is therefore not an unexplained contradiction. Long is settled Neutral on ten observations and has only one negative candidate-set observation. Intermediate and Long both settle into Falling × Falling on November 20 through year end. Short is in that case continuously from October 28. All three end at +1 / +2 / +3, with Trend Values −193.6 / −188.4 / −196.8 bp. The major favorable shift is supported; forcing every September/October observation to agree with the crisis label would conceal economically meaningful transitions. The report leaves every early mixed candidate set intact.


**Short / 6M**

All 83 observations: [-1,0]: 6 (7.23%); [-1]: 4 (4.82%); [0,1]: 14 (16.87%); [0]: 4 (4.82%); [1]: 55 (66.27%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2008-09-02 | 1.93 | 8.0 | Stable | 4.2 | Stable | Stable × Stable | [0] |
| 2008-09-30 | 1.60 | 1.2 | Stable | -42.8 | Falling | Stable × Falling | [0,1] |
| 2008-10-01 | 1.49 | 0.6 | Stable | -41.4 | Falling | Stable × Falling | [0,1] |
| 2008-10-31 | 0.94 | -58.4 | Falling | -40.8 | Falling | Falling × Falling | [1] |
| 2008-11-03 | 1.07 | -64.6 | Falling | -39.4 | Falling | Falling × Falling | [1] |
| 2008-11-28 | 0.44 | -146.4 | Falling | -92.8 | Falling | Falling × Falling | [1] |
| 2008-12-01 | 0.44 | -147.8 | Falling | -84.4 | Falling | Falling × Falling | [1] |
| 2008-12-31 | 0.27 | -193.6 | Falling | -23.8 | Falling | Falling × Falling | [1] |

Rule Case path (event-clipped episodes): 2008-09-02–2008-09-05 Stable × Stable (4); 2008-09-08–2008-09-11 Rising × Stable (4); 2008-09-12–2008-09-16 Rising × Falling (3); 2008-09-17–2008-10-03 Stable × Falling (13); 2008-10-06–2008-10-20 Falling × Falling (10); 2008-10-21–2008-10-21 Falling × Stable (1); 2008-10-22–2008-10-24 Stable × Rising (3); 2008-10-27–2008-10-27 Stable × Falling (1); 2008-10-28–2008-12-31 Falling × Falling (44).

**Intermediate / 10Y**

All 83 observations: [-1]: 16 (19.28%); [-2]: 5 (6.02%); [0]: 13 (15.66%); [1]: 21 (25.30%); [2]: 28 (33.73%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2008-09-02 | 3.74 | 13.2 | Stable | -25.2 | Falling | Stable × Falling | [1] |
| 2008-09-30 | 3.85 | 26.8 | Rising | 0.4 | Stable | Rising × Stable | [-1] |
| 2008-10-01 | 3.77 | 25.2 | Rising | 0.8 | Stable | Rising × Stable | [-1] |
| 2008-10-31 | 4.01 | 9.4 | Stable | 13.2 | Rising | Stable × Rising | [-1] |
| 2008-11-03 | 3.96 | 12.4 | Stable | 21.0 | Rising | Stable × Rising | [-1] |
| 2008-11-28 | 2.93 | -84.6 | Falling | -62.8 | Falling | Falling × Falling | [2] |
| 2008-12-01 | 2.72 | -97.0 | Falling | -78.0 | Falling | Falling × Falling | [2] |
| 2008-12-31 | 2.25 | -188.4 | Falling | -85.0 | Falling | Falling × Falling | [2] |

Rule Case path (event-clipped episodes): 2008-09-02–2008-09-23 Stable × Falling (16); 2008-09-24–2008-10-01 Rising × Stable (6); 2008-10-02–2008-10-10 Stable × Stable (7); 2008-10-14–2008-10-20 Rising × Rising (5); 2008-10-21–2008-10-23 Stable × Rising (3); 2008-10-24–2008-10-24 Stable × Stable (1); 2008-10-27–2008-10-27 Stable × Falling (1); 2008-10-28–2008-10-30 Stable × Stable (3); 2008-10-31–2008-11-10 Stable × Rising (7); 2008-11-12–2008-11-13 Stable × Stable (2); 2008-11-14–2008-11-19 Stable × Falling (4); 2008-11-20–2008-12-31 Falling × Falling (28).

**Long / 30Y**

All 83 observations: [-2,-1]: 1 (1.20%); [0]: 10 (12.05%); [1,2]: 25 (30.12%); [2]: 7 (8.43%); [3]: 40 (48.19%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2008-09-02 | 4.36 | -12.0 | Stable | -22.4 | Falling | Stable × Falling | [1,2] |
| 2008-09-30 | 4.31 | -3.8 | Stable | -7.8 | Stable | Stable × Stable | [0] |
| 2008-10-01 | 4.22 | -7.8 | Stable | -10.6 | Falling | Stable × Falling | [1,2] |
| 2008-10-31 | 4.35 | -29.0 | Falling | -4.0 | Stable | Falling × Stable | [2] |
| 2008-11-03 | 4.33 | -25.0 | Stable | 5.0 | Stable | Stable × Stable | [0] |
| 2008-11-28 | 3.45 | -104.4 | Falling | -47.6 | Falling | Falling × Falling | [3] |
| 2008-12-01 | 3.22 | -115.8 | Falling | -61.0 | Falling | Falling × Falling | [3] |
| 2008-12-31 | 2.69 | -196.8 | Falling | -89.6 | Falling | Falling × Falling | [3] |

Rule Case path (event-clipped episodes): 2008-09-02–2008-09-08 Stable × Falling (5); 2008-09-09–2008-09-10 Falling × Falling (2); 2008-09-11–2008-09-23 Stable × Falling (9); 2008-09-24–2008-09-30 Stable × Stable (5); 2008-10-01–2008-10-06 Stable × Falling (4); 2008-10-07–2008-10-10 Falling × Falling (4); 2008-10-14–2008-10-14 Stable × Falling (1); 2008-10-15–2008-10-17 Stable × Stable (3); 2008-10-20–2008-10-20 Stable × Rising (1); 2008-10-21–2008-10-21 Stable × Stable (1); 2008-10-22–2008-10-22 Falling × Stable (1); 2008-10-23–2008-10-30 Falling × Falling (6); 2008-10-31–2008-10-31 Falling × Stable (1); 2008-11-03–2008-11-03 Stable × Stable (1); 2008-11-04–2008-11-12 Falling × Rising (6); 2008-11-13–2008-11-19 Falling × Stable (5); 2008-11-20–2008-12-31 Falling × Falling (28).

### Taper tantrum (Anchor), 2013-05-01 through 2013-09-30

**Interpretation.** Short remains Neutral for all 106 observations, with very small changes in its own representative series. This is the strongest Anchor example against applying one common case to all exposures. Both longer tenors begin with a recent decline, then move into unfavorable cases in mid-May; Long reaches Rising × Rising on May 15 and Intermediate on May 16. Intermediate spends 69.81% and Long 66.98% of the window at their most unfavorable available categories. September declines improve Intermediate to Rising × Falling; Long briefly does the same before ending Rising × Stable. End results are 0 / −1 / −2. The initial favorable observations and later partial improvements are explained by the actual windows; neither is a sustained contradiction during the main rising-yield phase.


**Short / 6M**

All 106 observations: [0]: 106 (100.00%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2013-05-01 | 0.08 | -6.8 | Stable | -2.8 | Stable | Stable × Stable | [0] |
| 2013-05-31 | 0.07 | -6.8 | Stable | -0.8 | Stable | Stable × Stable | [0] |
| 2013-06-03 | 0.08 | -6.8 | Stable | -0.6 | Stable | Stable × Stable | [0] |
| 2013-06-28 | 0.10 | -0.8 | Stable | 3.0 | Stable | Stable × Stable | [0] |
| 2013-07-01 | 0.09 | -1.2 | Stable | 2.8 | Stable | Stable × Stable | [0] |
| 2013-07-31 | 0.08 | -3.8 | Stable | -3.4 | Stable | Stable × Stable | [0] |
| 2013-08-01 | 0.08 | -3.8 | Stable | -2.4 | Stable | Stable × Stable | [0] |
| 2013-08-30 | 0.05 | -6.4 | Stable | -1.0 | Stable | Stable × Stable | [0] |
| 2013-09-03 | 0.05 | -6.4 | Stable | -1.4 | Stable | Stable × Stable | [0] |
| 2013-09-30 | 0.04 | -7.2 | Stable | -2.6 | Stable | Stable × Stable | [0] |

Rule Case path (event-clipped episodes): 2013-05-01–2013-09-30 Stable × Stable (106).

**Intermediate / 10Y**

All 106 observations: [-1]: 22 (20.75%); [-2]: 74 (69.81%); [0]: 7 (6.60%); [1]: 3 (2.83%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2013-05-01 | 1.66 | -11.4 | Stable | -18.0 | Falling | Stable × Falling | [1] |
| 2013-05-31 | 2.16 | 45.2 | Rising | 41.6 | Rising | Rising × Rising | [-2] |
| 2013-06-03 | 2.13 | 49.0 | Rising | 45.6 | Rising | Rising × Rising | [-2] |
| 2013-06-28 | 2.52 | 77.0 | Rising | 45.8 | Rising | Rising × Rising | [-2] |
| 2013-07-01 | 2.50 | 77.2 | Rising | 41.6 | Rising | Rising × Rising | [-2] |
| 2013-07-31 | 2.60 | 62.2 | Rising | 7.4 | Stable | Rising × Stable | [-1] |
| 2013-08-01 | 2.74 | 62.0 | Rising | 12.4 | Rising | Rising × Rising | [-2] |
| 2013-08-30 | 2.78 | 88.0 | Rising | 13.2 | Rising | Rising × Rising | [-2] |
| 2013-09-03 | 2.86 | 89.0 | Rising | 13.6 | Rising | Rising × Rising | [-2] |
| 2013-09-30 | 2.64 | 76.8 | Rising | -12.4 | Falling | Rising × Falling | [-1] |

Rule Case path (event-clipped episodes): 2013-05-01–2013-05-03 Stable × Falling (3); 2013-05-06–2013-05-14 Stable × Stable (7); 2013-05-15–2013-05-15 Stable × Rising (1); 2013-05-16–2013-07-24 Rising × Rising (48); 2013-07-25–2013-07-31 Rising × Stable (5); 2013-08-01–2013-08-05 Rising × Rising (3); 2013-08-06–2013-08-14 Rising × Stable (7); 2013-08-15–2013-09-17 Rising × Rising (23); 2013-09-18–2013-09-20 Rising × Stable (3); 2013-09-23–2013-09-30 Rising × Falling (6).

**Long / 30Y**

All 106 observations: [-2,-1]: 4 (3.77%); [-2]: 22 (20.75%); [-3]: 71 (66.98%); [0]: 5 (4.72%); [1,2]: 4 (3.77%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2013-05-01 | 2.83 | -6.8 | Stable | -22.6 | Falling | Stable × Falling | [1,2] |
| 2013-05-31 | 3.30 | 46.0 | Rising | 39.4 | Rising | Rising × Rising | [-3] |
| 2013-06-03 | 3.27 | 48.6 | Rising | 43.0 | Rising | Rising × Rising | [-3] |
| 2013-06-28 | 3.52 | 62.4 | Rising | 31.2 | Rising | Rising × Rising | [-3] |
| 2013-07-01 | 3.48 | 62.8 | Rising | 27.6 | Rising | Rising × Rising | [-3] |
| 2013-07-31 | 3.64 | 50.6 | Rising | 10.2 | Rising | Rising × Rising | [-3] |
| 2013-08-01 | 3.77 | 50.4 | Rising | 15.2 | Rising | Rising × Rising | [-3] |
| 2013-08-30 | 3.70 | 63.8 | Rising | 5.4 | Stable | Rising × Stable | [-2] |
| 2013-09-03 | 3.79 | 63.8 | Rising | 4.2 | Stable | Rising × Stable | [-2] |
| 2013-09-30 | 3.69 | 57.6 | Rising | -6.8 | Stable | Rising × Stable | [-2] |

Rule Case path (event-clipped episodes): 2013-05-01–2013-05-06 Stable × Falling (4); 2013-05-07–2013-05-13 Stable × Stable (5); 2013-05-14–2013-05-14 Stable × Rising (1); 2013-05-15–2013-07-24 Rising × Rising (49); 2013-07-25–2013-07-30 Rising × Stable (4); 2013-07-31–2013-08-07 Rising × Rising (6); 2013-08-08–2013-08-14 Rising × Stable (5); 2013-08-15–2013-08-28 Rising × Rising (10); 2013-08-29–2013-09-06 Rising × Stable (6); 2013-09-09–2013-09-16 Rising × Rising (6); 2013-09-17–2013-09-23 Rising × Stable (5); 2013-09-24–2013-09-26 Rising × Falling (3); 2013-09-27–2013-09-30 Rising × Stable (2).

### 2022 tightening (Anchor), 2022-01-01 through 2022-10-31

**Interpretation.** Short and Intermediate begin Neutral while Long already has a Rising Recent Move against a Stable Trend. Short reaches Rising × Rising on January 19 and remains there through October 31 (197 observations). Intermediate reaches that case sooner, January 7, but recent declines produce a July 14–August 18 Rising × Falling episode. Long reaches Rising × Rising on February 4 and has its analogous relief episode July 15–August 11. During that relief Short stays Rising × Rising: the curve does not move as a single case. At the end all three are Rising × Rising, producing −1 / −2 / −3. Long never has a nonnegative candidate in this window. The midsummer improvement retains an unfavorable broader interpretation and does not predict renewed tightening or a future rally. The ex-ante unfavorable assessment is supported.


**Short / 6M**

All 208 observations: [-1,0]: 10 (4.81%); [-1]: 197 (94.71%); [0]: 1 (0.48%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-01-03 | 0.22 | 14.0 | Stable | 10.0 | Stable | Stable × Stable | [0] |
| 2022-01-31 | 0.49 | 37.6 | Rising | 23.4 | Rising | Rising × Rising | [-1] |
| 2022-02-01 | 0.48 | 39.4 | Rising | 25.0 | Rising | Rising × Rising | [-1] |
| 2022-02-28 | 0.69 | 65.0 | Rising | 31.2 | Rising | Rising × Rising | [-1] |
| 2022-03-01 | 0.60 | 62.2 | Rising | 27.0 | Rising | Rising × Rising | [-1] |
| 2022-03-31 | 1.06 | 100.0 | Rising | 38.4 | Rising | Rising × Rising | [-1] |
| 2022-04-01 | 1.09 | 101.6 | Rising | 39.2 | Rising | Rising × Rising | [-1] |
| 2022-04-29 | 1.41 | 133.6 | Rising | 37.0 | Rising | Rising × Rising | [-1] |
| 2022-05-02 | 1.49 | 135.0 | Rising | 36.4 | Rising | Rising × Rising | [-1] |
| 2022-05-31 | 1.64 | 146.2 | Rising | 15.0 | Rising | Rising × Rising | [-1] |
| 2022-06-01 | 1.63 | 147.6 | Rising | 15.6 | Rising | Rising × Rising | [-1] |
| 2022-06-30 | 2.51 | 234.8 | Rising | 98.6 | Rising | Rising × Rising | [-1] |
| 2022-07-01 | 2.52 | 234.4 | Rising | 96.8 | Rising | Rising × Rising | [-1] |
| 2022-07-29 | 2.91 | 257.0 | Rising | 44.0 | Rising | Rising × Rising | [-1] |
| 2022-08-01 | 2.96 | 253.4 | Rising | 40.6 | Rising | Rising × Rising | [-1] |
| 2022-08-31 | 3.32 | 262.6 | Rising | 35.2 | Rising | Rising × Rising | [-1] |
| 2022-09-01 | 3.34 | 263.6 | Rising | 35.6 | Rising | Rising × Rising | [-1] |
| 2022-09-30 | 3.92 | 285.4 | Rising | 61.2 | Rising | Rising × Rising | [-1] |
| 2022-10-03 | 3.97 | 284.2 | Rising | 59.8 | Rising | Rising × Rising | [-1] |
| 2022-10-31 | 4.57 | 309.8 | Rising | 60.8 | Rising | Rising × Rising | [-1] |

Rule Case path (event-clipped episodes): 2022-01-03–2022-01-03 Stable × Stable (1); 2022-01-04–2022-01-18 Stable × Rising (10); 2022-01-19–2022-10-31 Rising × Rising (197).

**Intermediate / 10Y**

All 208 observations: [-1]: 66 (31.73%); [-2]: 141 (67.79%); [0]: 1 (0.48%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-01-03 | 1.63 | 5.2 | Stable | 8.2 | Stable | Stable × Stable | [0] |
| 2022-01-31 | 1.79 | 52.6 | Rising | 29.4 | Rising | Rising × Rising | [-2] |
| 2022-02-01 | 1.81 | 54.4 | Rising | 29.6 | Rising | Rising × Rising | [-2] |
| 2022-02-28 | 1.83 | 66.0 | Rising | 15.0 | Rising | Rising × Rising | [-2] |
| 2022-03-01 | 1.72 | 59.6 | Rising | 10.0 | Stable | Rising × Stable | [-1] |
| 2022-03-31 | 2.32 | 96.0 | Rising | 53.6 | Rising | Rising × Rising | [-2] |
| 2022-04-01 | 2.39 | 89.6 | Rising | 53.8 | Rising | Rising × Rising | [-2] |
| 2022-04-29 | 2.89 | 119.8 | Rising | 42.0 | Rising | Rising × Rising | [-2] |
| 2022-05-02 | 2.99 | 125.6 | Rising | 46.0 | Rising | Rising × Rising | [-2] |
| 2022-05-31 | 2.85 | 118.2 | Rising | -5.8 | Stable | Rising × Stable | [-1] |
| 2022-06-01 | 2.94 | 125.8 | Rising | -5.8 | Stable | Rising × Stable | [-1] |
| 2022-06-30 | 2.98 | 162.6 | Rising | 35.2 | Rising | Rising × Rising | [-2] |
| 2022-07-01 | 2.88 | 156.4 | Rising | 26.6 | Rising | Rising × Rising | [-2] |
| 2022-07-29 | 2.67 | 96.2 | Rising | -39.4 | Falling | Rising × Falling | [-1] |
| 2022-08-01 | 2.60 | 91.4 | Rising | -41.4 | Falling | Rising × Falling | [-1] |
| 2022-08-31 | 3.15 | 122.2 | Rising | 39.4 | Rising | Rising × Rising | [-2] |
| 2022-09-01 | 3.26 | 128.8 | Rising | 45.0 | Rising | Rising × Rising | [-2] |
| 2022-09-30 | 3.83 | 142.8 | Rising | 74.2 | Rising | Rising × Rising | [-2] |
| 2022-10-03 | 3.67 | 140.4 | Rising | 65.4 | Rising | Rising × Rising | [-2] |
| 2022-10-31 | 4.10 | 121.6 | Rising | 24.0 | Rising | Rising × Rising | [-2] |

Rule Case path (event-clipped episodes): 2022-01-03–2022-01-03 Stable × Stable (1); 2022-01-04–2022-01-06 Stable × Rising (3); 2022-01-07–2022-02-28 Rising × Rising (35); 2022-03-01–2022-03-15 Rising × Stable (11); 2022-03-16–2022-05-17 Rising × Rising (44); 2022-05-18–2022-06-10 Rising × Stable (17); 2022-06-13–2022-07-05 Rising × Rising (15); 2022-07-06–2022-07-13 Rising × Stable (6); 2022-07-14–2022-08-18 Rising × Falling (26); 2022-08-19–2022-08-23 Rising × Stable (3); 2022-08-24–2022-10-31 Rising × Rising (47).

**Long / 30Y**

All 208 observations: [-2,-1]: 43 (20.67%); [-2]: 34 (16.35%); [-3]: 131 (62.98%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-01-03 | 2.01 | -15.8 | Stable | 13.8 | Rising | Stable × Rising | [-2,-1] |
| 2022-01-31 | 2.11 | 20.0 | Stable | 19.4 | Rising | Stable × Rising | [-2,-1] |
| 2022-02-01 | 2.12 | 20.6 | Stable | 19.6 | Rising | Stable × Rising | [-2,-1] |
| 2022-02-28 | 2.17 | 35.6 | Rising | 14.6 | Rising | Rising × Rising | [-3] |
| 2022-03-01 | 2.11 | 31.8 | Rising | 12.0 | Rising | Rising × Rising | [-3] |
| 2022-03-31 | 2.44 | 56.2 | Rising | 30.6 | Rising | Rising × Rising | [-3] |
| 2022-04-01 | 2.44 | 48.0 | Rising | 28.2 | Rising | Rising × Rising | [-3] |
| 2022-04-29 | 2.96 | 84.6 | Rising | 36.8 | Rising | Rising × Rising | [-3] |
| 2022-05-02 | 3.07 | 91.8 | Rising | 42.0 | Rising | Rising × Rising | [-3] |
| 2022-05-31 | 3.07 | 106.4 | Rising | 9.0 | Stable | Rising × Stable | [-2] |
| 2022-06-01 | 3.09 | 112.6 | Rising | 7.4 | Stable | Rising × Stable | [-2] |
| 2022-06-30 | 3.14 | 134.4 | Rising | 25.0 | Rising | Rising × Rising | [-3] |
| 2022-07-01 | 3.11 | 130.0 | Rising | 19.8 | Rising | Rising × Rising | [-3] |
| 2022-07-29 | 3.00 | 91.6 | Rising | -23.6 | Falling | Rising × Falling | [-2,-1] |
| 2022-08-01 | 2.92 | 89.2 | Rising | -24.6 | Falling | Rising × Falling | [-2,-1] |
| 2022-08-31 | 3.27 | 102.4 | Rising | 24.8 | Rising | Rising × Rising | [-3] |
| 2022-09-01 | 3.37 | 105.6 | Rising | 28.6 | Rising | Rising × Rising | [-3] |
| 2022-09-30 | 3.79 | 123.4 | Rising | 51.6 | Rising | Rising × Rising | [-3] |
| 2022-10-03 | 3.73 | 126.8 | Rising | 49.4 | Rising | Rising × Rising | [-3] |
| 2022-10-31 | 4.22 | 128.2 | Rising | 46.6 | Rising | Rising × Rising | [-3] |

Rule Case path (event-clipped episodes): 2022-01-03–2022-02-03 Stable × Rising (23); 2022-02-04–2022-03-02 Rising × Rising (18); 2022-03-03–2022-03-14 Rising × Stable (8); 2022-03-15–2022-05-23 Rising × Rising (49); 2022-05-24–2022-05-24 Rising × Stable (1); 2022-05-25–2022-05-25 Rising × Rising (1); 2022-05-26–2022-06-10 Rising × Stable (11); 2022-06-13–2022-07-05 Rising × Rising (15); 2022-07-06–2022-07-14 Rising × Stable (7); 2022-07-15–2022-08-11 Rising × Falling (20); 2022-08-12–2022-08-22 Rising × Stable (7); 2022-08-23–2022-10-31 Rising × Rising (48).

### 1987 crash (Challenge), 1987-08-01 through 1987-10-31

**Interpretation.** All three start Rising × Rising and remain there through most of the window. After the October shock, Long and Short first leave that case on October 22 and Intermediate on October 23. By October 30 Short has Stable Trend and Recent Move −102.6 bp, giving [0,+1]; the longer tenors retain Rising Trend but Recent Moves −66.6 and −67.6 bp, giving −1 and [−2,−1]. Both candidates improve Long relative to its initial −3. The long-tenor Trend need not become Falling to acknowledge the rally. Five-day smoothing and the 21-observation comparison prevent instantaneous response to every daily reversal. This is interpretable Challenge-event lag, not a demand that October 19 itself be assigned a particular category. Short's improvement eventually crosses Neutral even while longer-tenor assessments remain negative; their broader reference comparisons are different.


**Short / 6M**

All 63 observations: [-1,0]: 1 (1.59%); [-1]: 57 (90.48%); [0,1]: 5 (7.94%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1987-08-03 | 6.49 | 70.4 | Rising | 23.2 | Rising | Rising × Rising | [-1] |
| 1987-08-31 | 6.62 | 87.2 | Rising | 15.0 | Rising | Rising × Rising | [-1] |
| 1987-09-01 | 6.61 | 86.8 | Rising | 14.6 | Rising | Rising × Rising | [-1] |
| 1987-09-30 | 7.19 | 127.0 | Rising | 67.4 | Rising | Rising × Rising | [-1] |
| 1987-10-01 | 7.18 | 123.4 | Rising | 64.8 | Rising | Rising × Rising | [-1] |
| 1987-10-30 | 6.27 | -13.4 | Stable | -102.6 | Falling | Stable × Falling | [0,1] |

Rule Case path (event-clipped episodes): 1987-08-03–1987-10-21 Rising × Rising (56); 1987-10-22–1987-10-22 Rising × Stable (1); 1987-10-23–1987-10-23 Rising × Falling (1); 1987-10-26–1987-10-30 Stable × Falling (5).

**Intermediate / 10Y**

All 63 observations: [-1]: 6 (9.52%); [-2]: 57 (90.48%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1987-08-03 | 8.81 | 149.6 | Rising | 31.2 | Rising | Rising × Rising | [-2] |
| 1987-08-31 | 9.00 | 169.4 | Rising | 27.2 | Rising | Rising × Rising | [-2] |
| 1987-09-01 | 9.05 | 177.2 | Rising | 29.4 | Rising | Rising × Rising | [-2] |
| 1987-09-30 | 9.63 | 212.4 | Rising | 67.4 | Rising | Rising × Rising | [-2] |
| 1987-10-01 | 9.66 | 208.4 | Rising | 64.0 | Rising | Rising × Rising | [-2] |
| 1987-10-30 | 8.88 | 58.0 | Rising | -66.6 | Falling | Rising × Falling | [-1] |

Rule Case path (event-clipped episodes): 1987-08-03–1987-10-22 Rising × Rising (57); 1987-10-23–1987-10-23 Rising × Stable (1); 1987-10-26–1987-10-30 Rising × Falling (5).

**Long / 30Y**

All 63 observations: [-2,-1]: 5 (7.94%); [-2]: 2 (3.17%); [-3]: 56 (88.89%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1987-08-03 | 9.02 | 141.2 | Rising | 40.8 | Rising | Rising × Rising | [-3] |
| 1987-08-31 | 9.17 | 159.2 | Rising | 22.2 | Rising | Rising × Rising | [-3] |
| 1987-09-01 | 9.24 | 166.4 | Rising | 24.6 | Rising | Rising × Rising | [-3] |
| 1987-09-30 | 9.79 | 197.4 | Rising | 64.4 | Rising | Rising × Rising | [-3] |
| 1987-10-01 | 9.80 | 193.2 | Rising | 61.0 | Rising | Rising × Rising | [-3] |
| 1987-10-30 | 9.03 | 50.8 | Rising | -67.6 | Falling | Rising × Falling | [-2,-1] |

Rule Case path (event-clipped episodes): 1987-08-03–1987-10-21 Rising × Rising (56); 1987-10-22–1987-10-23 Rising × Stable (2); 1987-10-26–1987-10-30 Rising × Falling (5).

### COVID (Challenge), 2020-02-01 through 2020-03-31

**Interpretation.** Short begins Falling × Stable, whereas both longer tenors begin Falling × Falling. Intermediate switches to Stable × Falling on February 7 and Long on February 10 despite continuing favorable Recent Moves; both return to Falling × Falling on February 28. This apparent weakening reflects the moving six-month reference as well as the endpoint, not a prediction of a yield rebound. Short moves into Falling × Falling on February 27 but stays at +1 because the settled Short categories tie. By March 31 the exposures remain +1 / +2 / +3 with large negative changes. The broad favorable interpretation survives throughout, but it cannot diagnose every March dislocation. A unchanged Core category does not imply unchanged Component Values or economic intensity. This is a Component/reference and ordinal-compression limitation, not a material sign contradiction or a reason to retune Task 1.


**Short / 6M**

All 41 observations: [1]: 41 (100.00%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-02-03 | 1.56 | -52.6 | Falling | -3.0 | Stable | Falling × Stable | [1] |
| 2020-02-28 | 1.11 | -53.0 | Falling | -20.2 | Falling | Falling × Falling | [1] |
| 2020-03-02 | 0.95 | -64.8 | Falling | -31.2 | Falling | Falling × Falling | [1] |
| 2020-03-31 | 0.15 | -182.6 | Falling | -117.6 | Falling | Falling × Falling | [1] |

Rule Case path (event-clipped episodes): 2020-02-03–2020-02-26 Falling × Stable (17); 2020-02-27–2020-03-31 Falling × Falling (24).

**Intermediate / 10Y**

All 41 observations: [1]: 14 (34.15%); [2]: 27 (65.85%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-02-03 | 1.54 | -48.6 | Falling | -32.2 | Falling | Falling × Falling | [2] |
| 2020-02-28 | 1.13 | -27.0 | Falling | -36.6 | Falling | Falling × Falling | [2] |
| 2020-03-02 | 1.10 | -31.4 | Falling | -38.8 | Falling | Falling × Falling | [2] |
| 2020-03-31 | 0.70 | -94.0 | Falling | -47.2 | Falling | Falling × Falling | [2] |

Rule Case path (event-clipped episodes): 2020-02-03–2020-02-06 Falling × Falling (4); 2020-02-07–2020-02-27 Stable × Falling (14); 2020-02-28–2020-03-31 Falling × Falling (23).

**Long / 30Y**

All 41 observations: [1,2]: 13 (31.71%); [3]: 28 (68.29%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-02-03 | 2.01 | -54.0 | Falling | -30.4 | Falling | Falling × Falling | [3] |
| 2020-02-28 | 1.65 | -27.8 | Falling | -32.6 | Falling | Falling × Falling | [3] |
| 2020-03-02 | 1.66 | -30.0 | Falling | -33.4 | Falling | Falling × Falling | [3] |
| 2020-03-31 | 1.35 | -78.6 | Falling | -37.8 | Falling | Falling × Falling | [3] |

Rule Case path (event-clipped episodes): 2020-02-03–2020-02-07 Falling × Falling (5); 2020-02-10–2020-02-27 Stable × Falling (13); 2020-02-28–2020-03-31 Falling × Falling (23).

### 2023 long-end selloff (Challenge), 2023-07-01 through 2023-10-31

**Interpretation.** Short begins and ends −1, mostly Rising × Stable, while both longer exposures begin Neutral and end at −2 / −3. Raw yields move from 5.53% to 5.54% for 6M, 3.86% to 4.88% for 10Y, and 3.87% to 5.04% for 30Y across the window. These are observed within-window changes, not subsequent-return targets. Long is Rising × Rising on 60 of 84 observations, versus 61 for Intermediate; Short has only 13 such observations and its category remains mild. Intermediate temporarily becomes Neutral September 1–6 as its rolling comparisons become small, while Long retains Rising Trend. The marked long-end deterioration relative to the short end is supported without asserting a term-premium or other causal decomposition. Short's persistent negative Trend also shows that this Core describes the two specified horizons, not just change since the event began.


**Short / 6M**

All 84 observations: [-1]: 81 (96.43%); [0]: 3 (3.57%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-03 | 5.53 | 75.2 | Rising | 2.2 | Stable | Rising × Stable | [-1] |
| 2023-07-31 | 5.53 | 74.0 | Rising | 9.2 | Stable | Rising × Stable | [-1] |
| 2023-08-01 | 5.54 | 74.2 | Rising | 7.4 | Stable | Rising × Stable | [-1] |
| 2023-08-31 | 5.48 | 35.4 | Rising | -0.2 | Stable | Rising × Stable | [-1] |
| 2023-09-01 | 5.47 | 31.8 | Rising | -2.2 | Stable | Rising × Stable | [-1] |
| 2023-09-29 | 5.53 | 62.0 | Rising | -3.0 | Stable | Rising × Stable | [-1] |
| 2023-10-02 | 5.58 | 62.8 | Rising | 0.4 | Stable | Rising × Stable | [-1] |
| 2023-10-31 | 5.54 | 50.2 | Rising | 2.0 | Stable | Rising × Stable | [-1] |

Rule Case path (event-clipped episodes): 2023-07-03–2023-07-11 Rising × Stable (6); 2023-07-12–2023-07-28 Rising × Rising (13); 2023-07-31–2023-09-05 Rising × Stable (26); 2023-09-06–2023-09-08 Stable × Stable (3); 2023-09-11–2023-10-31 Rising × Stable (36).

**Intermediate / 10Y**

All 84 observations: [-1]: 19 (22.62%); [-2]: 61 (72.62%); [0]: 4 (4.76%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-03 | 3.86 | -3.6 | Stable | 8.6 | Stable | Stable × Stable | [0] |
| 2023-07-31 | 3.97 | 44.6 | Rising | 18.4 | Rising | Rising × Rising | [-2] |
| 2023-08-01 | 4.05 | 46.2 | Rising | 19.8 | Rising | Rising × Rising | [-2] |
| 2023-08-31 | 4.09 | 17.6 | Stable | 14.2 | Rising | Stable × Rising | [-1] |
| 2023-09-01 | 4.18 | 15.0 | Stable | 9.0 | Stable | Stable × Stable | [0] |
| 2023-09-29 | 4.59 | 104.4 | Rising | 39.6 | Rising | Rising × Rising | [-2] |
| 2023-10-02 | 4.69 | 109.2 | Rising | 45.2 | Rising | Rising × Rising | [-2] |
| 2023-10-31 | 4.88 | 140.4 | Rising | 30.2 | Rising | Rising × Rising | [-2] |

Rule Case path (event-clipped episodes): 2023-07-03–2023-07-03 Stable × Stable (1); 2023-07-05–2023-07-07 Stable × Rising (3); 2023-07-10–2023-07-14 Rising × Rising (5); 2023-07-17–2023-07-25 Rising × Stable (7); 2023-07-26–2023-08-08 Rising × Rising (10); 2023-08-09–2023-08-10 Rising × Stable (2); 2023-08-11–2023-08-29 Rising × Rising (13); 2023-08-30–2023-08-31 Stable × Rising (2); 2023-09-01–2023-09-06 Stable × Stable (3); 2023-09-07–2023-09-14 Rising × Rising (6); 2023-09-15–2023-09-21 Rising × Stable (5); 2023-09-22–2023-10-31 Rising × Rising (27).

**Long / 30Y**

All 84 observations: [-2]: 19 (22.62%); [-3]: 60 (71.43%); [0]: 5 (5.95%).

| as_of | Yield % | Trend bp | Trend | Recent bp | Recent | Rule Case | Core set |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-03 | 3.87 | -6.6 | Stable | -5.4 | Stable | Stable × Stable | [0] |
| 2023-07-31 | 4.02 | 36.8 | Rising | 15.6 | Rising | Rising × Rising | [-3] |
| 2023-08-01 | 4.11 | 39.4 | Rising | 18.2 | Rising | Rising × Rising | [-3] |
| 2023-08-31 | 4.20 | 29.8 | Rising | 17.2 | Rising | Rising × Rising | [-3] |
| 2023-09-01 | 4.29 | 29.8 | Rising | 11.8 | Rising | Rising × Rising | [-3] |
| 2023-09-29 | 4.73 | 96.2 | Rising | 43.8 | Rising | Rising × Rising | [-3] |
| 2023-10-02 | 4.81 | 101.6 | Rising | 48.6 | Rising | Rising × Rising | [-3] |
| 2023-10-31 | 5.04 | 131.8 | Rising | 33.4 | Rising | Rising × Rising | [-3] |

Rule Case path (event-clipped episodes): 2023-07-03–2023-07-10 Stable × Stable (5); 2023-07-11–2023-07-13 Rising × Rising (3); 2023-07-14–2023-07-26 Rising × Stable (9); 2023-07-27–2023-09-01 Rising × Rising (27); 2023-09-05–2023-09-07 Rising × Stable (3); 2023-09-08–2023-09-13 Rising × Rising (4); 2023-09-14–2023-09-22 Rising × Stable (7); 2023-09-25–2023-10-31 Rising × Rising (26).

## Analysis C — complete mixed-episode evidence

An episode is a maximal same-case run of available observations within one continuous data segment. Missing routine source days do not create artificial episodes. Full-sample endpoints are censored; event-clipped runs above are not used as independent episodes here. Selection: longest duration; largest absolute Recent Move anywhere in episode; typical episode minimizing duration distance from the episode median, then distance of episode median absolute Recent Move from the median across episodes. Ties use earliest start. Selected roles may coincide; they are not extra independent examples.

### Short / 6M

| Case | Episodes | Observations | Mean duration | Min / Q1 / median / Q3 / max | Trend range bp | Recent range bp |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | 39 | 510 | 13.08 | 1 / 3 / 9 / 20 / 56 | -446.8 to -25.4 | 10.2 to 95.4 |
| Stable × Falling | 58 | 486 | 8.38 | 1 / 3 / 7.0 / 12 / 32 | -25.0 to 24.6 | -122.6 to -10.2 |
| Stable × Rising | 58 | 394 | 6.79 | 1 / 3 / 6.0 / 10 / 24 | -25.0 to 25.0 | 10.2 to 81.8 |
| Rising × Falling | 39 | 361 | 9.26 | 1 / 3 / 6 / 13 / 35 | 25.4 to 171.6 | -128.8 to -10.2 |

| Case | Selection | Episode | n | Trend range bp | Recent range bp | CSV episode ID |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | longest | 2008-04-18 – 2008-07-08 | 56 | -280.0 to -92.4 | 10.6 to 43.4 | 6M-00522 |
| Falling × Rising | largest Recent Move | 1985-02-06 – 1985-03-29 | 36 | -267.8 to -171.0 | 10.8 to 95.4 | 6M-00068 |
| Falling × Rising | typical | 2002-02-12 – 2002-02-25 | 9 | -162.4 to -149.8 | 10.8 to 21.0 | 6M-00444 |
| Stable × Falling | longest | 1997-05-27 – 1997-07-10 | 32 | -3.2 to 23.0 | -24.6 to -10.4 | 6M-00351 |
| Stable × Falling | largest Recent Move | 1987-11-18 – 1987-11-24 | 5 | 1.2 to 20.8 | -122.6 to -16.0 | 6M-00139 |
| Stable × Falling | typical | 2003-05-19 – 2003-05-28 | 7 | -20.4 to -17.2 | -14.4 to -10.2 | 6M-00472 |
| Stable × Rising | longest | 1997-03-06 – 1997-04-09 | 24 | -16.0 to 24.4 | 11.6 to 34.2 | 6M-00344 |
| Stable × Rising | largest Recent Move | 1983-03-31 – 1983-04-08 | 6 | -19.4 to 17.2 | 41.2 to 81.8 | 6M-00025 |
| Stable × Rising | typical | 1993-10-26 – 1993-11-02 | 6 | 21.2 to 25.0 | 10.8 to 19.6 | 6M-00270 |
| Rising × Falling | longest | 1983-09-07 – 1983-10-26 | 35 | 25.8 to 147.6 | -67.8 to -15.6 | 6M-00040 |
| Rising × Falling | largest Recent Move | 1987-11-10 – 1987-11-17 | 5 | 28.6 to 37.4 | -128.8 to -106.8 | 6M-00138 |
| Rising × Falling | typical | 1988-09-16 – 1988-09-23 | 6 | 152.8 to 171.6 | -18.0 to -11.8 | 6M-00162 |

### Intermediate / 10Y

| Case | Episodes | Observations | Mean duration | Min / Q1 / median / Q3 / max | Trend range bp | Recent range bp |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | 104 | 1083 | 10.41 | 1 / 3 / 6.0 / 16 / 68 | -339.2 to -25.2 | 10.2 to 109.6 |
| Stable × Falling | 160 | 1421 | 8.88 | 1 / 3 / 5.5 / 12 / 44 | -25.0 to 25.0 | -217.8 to -10.2 |
| Stable × Rising | 164 | 1231 | 7.51 | 1 / 3 / 6.0 / 11 / 33 | -25.0 to 25.0 | 10.2 to 83.2 |
| Rising × Falling | 120 | 1162 | 9.68 | 1 / 3 / 7.0 / 16 / 34 | 25.2 to 368.6 | -203.0 to -10.2 |

| Case | Selection | Episode | n | Trend range bp | Recent range bp | CSV episode ID |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | longest | 1980-07-09 – 1980-10-14 | 68 | -203.8 to -38.2 | 16.6 to 109.6 | 10Y-00353 |
| Falling × Rising | largest Recent Move | 1980-07-09 – 1980-10-14 | 68 | -203.8 to -38.2 | 16.6 to 109.6 | 10Y-00353 |
| Falling × Rising | typical | 1993-06-04 – 1993-06-11 | 6 | -86.4 to -74.8 | 11.4 to 18.0 | 10Y-00680 |
| Stable × Falling | longest | 1968-06-18 – 1968-08-19 | 44 | -21.8 to 8.2 | -36.0 to -12.2 | 10Y-00083 |
| Stable × Falling | largest Recent Move | 1980-04-28 – 1980-05-01 | 4 | -17.6 to 19.6 | -217.8 to -209.4 | 10Y-00347 |
| Stable × Falling | typical | 2025-09-09 – 2025-09-15 | 5 | -23.4 to -14.2 | -22.4 to -10.8 | 10Y-01552 |
| Stable × Rising | longest | 2015-05-04 – 2015-06-18 | 33 | -22.6 to 23.0 | 12.0 to 33.2 | 10Y-01268 |
| Stable × Rising | largest Recent Move | 2003-07-18 – 2003-07-28 | 7 | -19.6 to 23.2 | 70.0 to 83.2 | 10Y-00932 |
| Stable × Rising | typical | 2024-01-29 – 2024-02-05 | 6 | -2.8 to 24.2 | 11.0 to 27.2 | 10Y-01492 |
| Rising × Falling | longest | 2025-02-06 – 2025-03-26 | 34 | 38.4 to 65.0 | -31.4 to -10.4 | 10Y-01526 |
| Rising × Falling | largest Recent Move | 1980-03-24 – 1980-04-25 | 24 | 40.0 to 368.6 | -203.0 to -17.6 | 10Y-00346 |
| Rising × Falling | typical | 2003-11-18 – 2003-11-26 | 7 | 74.0 to 82.2 | -22.6 to -11.4 | 10Y-00943 |

### Long / 30Y

| Case | Episodes | Observations | Mean duration | Min / Q1 / median / Q3 / max | Trend range bp | Recent range bp |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | 89 | 805 | 9.04 | 1 / 4 / 6 / 12 / 60 | -362.4 to -25.2 | 10.2 to 92.4 |
| Stable × Falling | 122 | 1115 | 9.14 | 1 / 4 / 6.0 / 13 / 36 | -25.0 to 25.0 | -200.6 to -10.2 |
| Stable × Rising | 101 | 867 | 8.58 | 1 / 4 / 7 / 12 / 27 | -25.0 to 25.0 | 10.2 to 68.2 |
| Rising × Falling | 79 | 699 | 8.85 | 1 / 3 / 6 / 13 / 35 | 25.2 to 338.4 | -168.4 to -10.2 |

| Case | Selection | Episode | n | Trend range bp | Recent range bp | CSV episode ID |
| --- | --- | --- | --- | --- | --- | --- |
| Falling × Rising | longest | 1980-07-21 – 1980-10-14 | 60 | -160.2 to -32.0 | 15.2 to 92.4 | 30Y-00062 |
| Falling × Rising | largest Recent Move | 1980-07-21 – 1980-10-14 | 60 | -160.2 to -32.0 | 15.2 to 92.4 | 30Y-00062 |
| Falling × Rising | typical | 2012-08-10 – 2012-08-17 | 6 | -41.8 to -26.0 | 11.8 to 28.4 | 30Y-00768 |
| Stable × Falling | longest | 1990-10-19 – 1990-12-11 | 36 | -24.4 to 7.2 | -46.2 to -13.2 | 30Y-00290 |
| Stable × Falling | largest Recent Move | 1981-12-02 – 1981-12-09 | 6 | -18.8 to 14.2 | -200.6 to -94.0 | 30Y-00090 |
| Stable × Falling | typical | 1988-12-22 – 1988-12-30 | 6 | -6.4 to 7.2 | -18.0 to -12.6 | 30Y-00248 |
| Stable × Rising | longest | 2015-05-05 – 2015-06-11 | 27 | -23.2 to 23.8 | 17.4 to 47.6 | 30Y-00854 |
| Stable × Rising | largest Recent Move | 2001-12-11 – 2002-01-09 | 20 | -21.0 to -9.8 | 11.6 to 68.2 | 30Y-00577 |
| Stable × Rising | typical | 2001-01-25 – 2001-02-02 | 7 | -21.4 to -15.0 | 12.0 to 23.4 | 30Y-00547 |
| Rising × Falling | longest | 1984-07-20 – 1984-09-07 | 35 | 25.2 to 152.2 | -85.4 to -11.0 | 30Y-00154 |
| Rising × Falling | largest Recent Move | 1980-04-07 – 1980-05-06 | 22 | 33.0 to 298.0 | -168.4 to -17.6 | 30Y-00054 |
| Rising × Falling | typical | 1984-06-15 – 1984-06-22 | 6 | 125.8 to 146.6 | -28.8 to -10.6 | 30Y-00148 |

### Analysis-C economic assessment and candidate decisions

The complete summaries above, rather than daily counts treated as independent experiments, are the evidence base. Short has 39 / 58 / 58 / 39 episodes in Falling × Rising / Stable × Falling / Stable × Rising / Rising × Falling. Intermediate has 104 / 160 / 164 / 120; Long has 89 / 122 / 101 / 79 after structural-gap exclusions. Their median durations are generally 5.5–9 observations, but maxima reach 68 for Intermediate Falling × Rising and 60 for Long. There are enough episodes to establish that these states recur; there is no statistical target here that estimates a unique ordinal category. Confidence below concerns semantic plausibility, not an estimated probability of future success.

**Falling × Rising versus Stable × Falling.** The former retains a broader decline that is currently being challenged. In the latter, a recent decline occurs without an established broader direction. The values show the distinction: Intermediate Falling × Rising reaches Trend −339.2 bp while Recent Move is positive; Stable × Falling restricts Trend to ±25 bp yet includes Recent Move as negative as −217.8 bp. The 1980-07-09–10-14 Intermediate episode and 1980-07-21–10-14 Long episode have sizeable recent increases for many observations while their six-month comparisons remain negative. A higher favorable category in those conflict cases is difficult to defend solely by pointing to the older decline. Conversely, a six-observation near-threshold Long episode in August 2012 is much milder. Stable × Falling also spans moderate persistent declines (Long October–December 1990) and abrupt ones (December 1981). Equal mapped categories can legitimately compress different mechanisms, but the Core lineage must keep them distinguishable. None of these observations establishes what happens next.

**Stable × Rising versus Rising × Falling.** The former has a currently adverse move without an established broader trend; the latter has relief within a still-adverse broader condition. The Long May–June 2015 Stable × Rising episode persists for 27 observations with Recent Move +17.4 to +47.6 bp. Long July–September 1984 Rising × Falling instead combines positive Trend with a sustained recent decline. Its largest-recent-decline example in April–May 1980 is more extreme still. These should not be described interchangeably as generic mixed signals. A mild unfavorable category for the latter recognizes relief without asserting that the earlier rising condition is gone; choosing −2 can understate that relief. Stable × Rising can plausibly justify either −1 or −2 because the task provides no economic calibration separating them.

For the following table, **lower/higher refer to ordinal numeric order**, not absolute severity. The detailed episode selections were mechanical and include large contradictory moves as well as typical cases. The 1980 and other episodes outside the nine event windows are model-derived Analysis-C evidence, not additional ex-ante tests. No candidate decision has been written back to the CSV or to an authoritative Rule Table.

| Exposure | Rule Case | Candidates | Decision | Proposed category | Rationale and supporting episode evidence | Material counterevidence / limitation | Strength |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Short | Falling × Rising | [0,+1] | remain unresolved | — | Older decline can justify mild favorability: typical 2002-02-12–02-25 has Trend −162.4 to −149.8 bp against Recent +10.8 to +21.0. | Longest 2008-04-18–07-08 lasts 56 observations with Recent increases; largest 1985-02-06–03-29 reaches +95.4 bp. Neutral also has a credible economic interpretation. | Insufficient to choose; strong evidence of heterogeneity. |
| Short | Stable × Falling | [0,+1] | recommend higher candidate | +1 Mildly Favorable | A recent decline favors small positive duration with no established opposing broader direction. Longest 1997-05-27–07-10 (32 observations, Recent −24.6 to −10.4) and typical 2003-05-19–05-28 (7 observations, −14.4 to −10.2) support a restrained directional label. | The typical episode is close to the threshold; Neutral is defensible under stronger evidence requirements. The abrupt 1987-11-18–11-24 episode reaches −122.6 but does not justify claiming that +1 is a calibrated magnitude. No material opposing-sign episode within this case. | Moderate semantic support; weak category calibration. |
| Short | Stable × Rising | [−1,0] | recommend lower candidate | −1 Mildly Unfavorable | Symmetric small-duration interpretation of a recent increase without broader directional support. Longest 1997-03-06–04-09 (24 observations, +11.6 to +34.2) and typical 1993-10-26–11-02 (+10.8 to +19.6) support mild adversity. | Some Trend Values are negative inside Stable; early reversal or threshold proximity can justify Neutral. Largest 1983-03-31–04-08 reaches +81.8; one category cannot express that intensity. No material opposing-sign episode within this case. | Moderate semantic support; weak category calibration. |
| Short | Rising × Falling | [−1,0] | remain unresolved | — | Typical 1988-09-16–09-23 retains Trend +152.8 to +171.6 against a small recent decline, supporting −1. | Longest 1983-09-07–10-26 (35 observations, Recent −67.8 to −15.6) and largest 1987-11-10–11-17 (−128.8 to −106.8) support acknowledging relief with Neutral. Neither candidate fits every mechanism uniquely. | Insufficient to choose; strong evidence of heterogeneity. |
| Long | Falling × Rising | [+1,+2] | recommend lower candidate | +1 Mildly Favorable | Preserve the broader favorable condition but reduce conviction when a recent rise challenges it. Longest/largest 1980-07-21–10-14 lasts 60 observations with Recent +15.2 to +92.4; the typical 2012-08-10–08-17 episode has +11.8 to +28.4. These favor restraint relative to +2 Falling × Stable. | A very deep broader decline with a modest recent increase can justify +2; the full Trend range reaches −362.4. The prolonged 1980 reversal also challenges retaining any positive label if the consumer reads it as a current rally call. +1 reduces but does not resolve that interpretive risk. | Low-to-moderate; provisional semantic preference, not unique validation. |
| Long | Stable × Falling | [+1,+2] | remain unresolved | — | Long sensitivity and longest 1990-10-19–12-11 (36 observations, Recent −46.2 to −13.2) support +2. Largest 1981-12-02–12-09 reaches −200.6. | Typical 1988-12-22–12-30 (6 observations, −18.0 to −12.6) supports +1 when no broader decline is established. The evidence does not calibrate Mildly Favorable versus Favorable. | Direction well supported; category unresolved. |
| Long | Stable × Rising | [−2,−1] | remain unresolved | — | Long sensitivity and longest 2015-05-05–06-11 (+17.4 to +47.6) support −2; largest 2001-12-11–2002-01-09 reaches +68.2. | Typical 2001-01-25–02-02 (+12.0 to +23.4, with negative but Stable Trend) supports −1 absent an established rising Trend. No unique ordinal calibration follows from event occupancy. | Direction well supported; category unresolved. |
| Long | Rising × Falling | [−2,−1] | recommend higher candidate | −1 Mildly Unfavorable | A recent decline provides actual relief but does not erase the broader rise. Longest 1984-07-20–09-07 (35 observations, Recent −85.4 to −11.0) and largest 1980-04-07–05-06 (22 observations, down to −168.4) favor a milder category than −2 Rising × Stable. The 1987 Challenge improvement is consistent with this treatment. | Typical 1984-06-15–06-22 retains Trend +125.8 to +146.6 with Recent only −28.8 to −10.6; −2 remains economically credible there. Some persistent declines may challenge any negative label if mistaken for a contemporaneous price-direction claim. | Low-to-moderate; provisional semantic preference, not unique validation. |

These four recommendations preserve all required weak orders, including comparisons with the settled Intermediate cells. Long and Intermediate can tie at +1 or −1 in the two opposing-direction cases. That is allowable ordinal compression, not a claim that the economic sensitivity is identical. All eight decisions are provisional pending Task 2; unresolved cells retain both candidates.

## Supplemental diagnostics — model-derived, not ex-ante evidence

Selecting the longest State runs explains the occupancy concentrations seen in Analysis A. Short Trend Stable persists from 2009-10-08 through 2015-11-24 for 1,534 observations; its longest Recent Stable run spans 2009-05-06 through 2015-08-06 for 1,567 observations. These are long periods of small measured changes. They explain why means greatly exceed medians and why Short's full-sample distribution is concentrated; they are not missing-state bugs. Intermediate's longest Trend Stable run is 1962-07-10–1965-11-12 (834 observations, left-censored by the lookback), reflecting the different era in its longer sample. Long's longest Falling Trend run is 1985-05-03–1986-09-19 (346 observations). These selections come from model output and do not add independent evidence to the Anchor results.

The prolonged 1980 opposing-direction mixed episodes are a more consequential stress case than isolated one-day State flips. A six-month endpoint comparison is not a statement that the entire intervening path is monotonic. A recent rising phase can coexist for months with a negative Trend comparison, and vice versa. A consumer interpreting the resulting positive or negative category as the direction of today's price movement would receive misleading guidance. This is principally a **Component calculation / interpretation concern**, with a downstream category-semantics question. It is not resolved by choosing the better-looking historical candidate, and it does not establish a settled-cell sign error. Recheck these exact episode identities under Task 2 without using future returns to decide correctness.

## Validation and limitations

Validation passed: syntax compilation of the sole new Python file; all candidate-combination weak-order checks; exact threshold boundary classification; a synthetic linear-yield fixture yielding exactly 21 bp Recent and 126 bp Trend; independent Fraction-based recalculation of all 38,330 complete observations directly from indexed raw windows; explicit 6M Volcker unavailability and 30Y post-gap warmup checks; and prefix/no-lookahead checks at 1981-10-30, 2006-08-16, 2008-12-31, 2020-03-31, and 2023-10-31. Full offline replay produced byte-identical results CSV and numerical diagnostic tables. An initial Git whitespace check flagged the CSV writer's CRLF line endings; the writer now emits LF, and the staged whitespace check passes. This changed serialization only, not observations or calculations. The script's built-in checks run on every ordinary invocation; the additional Fraction and prefix checks were run as separate temporary validation commands.

Production tests were not run because no production code, dependencies, interfaces, or configuration changed. Production model outputs are unchanged. The research results are new outputs; provisional recommended categories have not replaced their candidate sets. No missing credentials or dependencies prevented this analysis. The base Python environment lacked pandas, so this study uses the standard library and does not install dependencies. The execution sandbox could not start (`mountinfo path is not absolute`); repository and analysis commands were run through approved escalation.

Limits: current historical vintage rather than real-time vintages; the unresolved source/metadata discrepancy inside the excluded 30Y interval; no Short Core during the 1981 Anchor; no 30Y Core during its discontinuation or rebuilt lookback; unequal historical samples; correlated episodes and overlapping Components; and an inherently judgmental boundary between adjacent ordinal categories. No return-based validation or out-of-sample predictive claim is made. Cross-tenor ordering is meaningful only under comparable local conditions, not as a mandatory same-date ranking across different cases. No hypothesis of a particular selloff cause is tested.

## Confirmed without change

The 6M / 10Y / 30Y exposure-local representation, fixed five-observation endpoints, 21/126-observation lags, inclusive State bands, nine-case coverage, and ordinal candidate preservation are usable for Task-1 review. The predefined episodes support favorable treatment of aligned declines and unfavorable treatment of aligned rises, with stronger or equal ordinal treatment for greater Duration under comparable conditions. Weak ordering and category ties behave as intended. This is support for interpretability, not proof of predictive efficacy or unique category calibration.

## Recommended Core-mapping changes

**None to settled cells.** The predefined events do not supply an economically meaningful contradiction sufficient to change them. Keep the proposed settled mapping for human review. Do not alter thresholds to obtain cleaner event narratives.

## Mixed cells provisionally resolved

Every previously ranged cell is accounted for below; a dash is an explicit unresolved decision, not an omitted recommendation. Detailed episode evidence and counterevidence are in Analysis C.

| Exposure | Rule Case | Candidates | Recommended category | Economic reason | Strength |
| --- | --- | --- | --- | --- | --- |
| Short | Falling × Rising | [0,+1] | —; remain unresolved | Established decline and current reversal support competing neutral/mild interpretations. | Insufficient |
| Short | Stable × Falling | [0,+1] | +1; higher candidate | Recent decline favors small positive duration without an opposing broader direction. | Moderate semantics; weak calibration |
| Short | Stable × Rising | [−1,0] | −1; lower candidate | Symmetric mild penalty for a recent rise without broader support. | Moderate semantics; weak calibration |
| Short | Rising × Falling | [−1,0] | —; remain unresolved | Relief and retained broader adversity cannot uniquely select Neutral or Mildly Unfavorable. | Insufficient |
| Long | Falling × Rising | [+1,+2] | +1; lower candidate | Temper the broader favorable interpretation when recent yields rise. | Low-to-moderate |
| Long | Stable × Falling | [+1,+2] | —; remain unresolved | Favorable direction is clear, but mild versus favorable intensity is uncalibrated. | Insufficient for category |
| Long | Stable × Rising | [−2,−1] | —; remain unresolved | Unfavorable direction is clear, but mild versus unfavorable intensity is uncalibrated. | Insufficient for category |
| Long | Rising × Falling | [−2,−1] | −1; higher candidate | Acknowledge recent relief while retaining broader adverse direction. | Low-to-moderate |

## Still unresolved

The four dash-marked cells remain candidate sets. More generally, historical yields alone do not identify a unique semantic boundary between Mildly Favorable and Favorable, or between Mildly Unfavorable and Unfavorable. The persistence of conflicting-horizon episodes, sample dependence of Stable occupancy, and appropriate consumer interpretation of those episodes require review. The 30Y download/metadata inconsistency is contained by exclusion, but its source provenance remains unexplained.

## Historical contradictions

No material, persistent contradiction of the settled mapping is identified in the nine predefined windows. This does not mean every date matches the broad event label. The material concerns are classified explicitly:

| Evidence | Primary classification | Assessment |
| --- | --- | --- |
| Long/Intermediate 1980 long mixed reversal episodes (model-derived Analysis C) | Component calculation concern; downstream Core-semantic concern | Sustained recent reversal coexists with opposite broader comparison. Positive/negative labels can mislead if read as contemporaneous direction. A serious interpretation stress case, not proof of a settled-cell error or an independent ex-ante test. |
| February 2020 longer-tenor Trend temporarily becomes Stable while Recent remains Falling | Component calculation concern / expected Challenge-event ambiguity | Moving reference changes the broader comparison. Favorability weakens but never becomes unfavorable; no material sign contradiction. |
| October 1987 recent declines improve the Core while long-tenor Trend remains Rising | Expected Challenge-event ambiguity | The prescribed horizons respond at different speeds; improvement is supported without requiring an immediate favorable sign. |
| Short's long Stable runs and occasional threshold crossings | State Classification concern for follow-up | Fixed bands compress long calm periods and boundary moves; no pathological full-sample switching or missing States. |
| Short unavailable in 1981; 30Y documented discontinuation and warmup | Data limitation | Explicitly excluded; no substitute series or inferred Core result. The contradictory downloaded 30Y entries are quarantined. |
| GFC September/October adverse Intermediate intervals; early 1994 Long favorability; early 2013 longer-tenor favorability | No material Core mapping contradiction | Actual local changes and within-window transitions explain these observations; full event labels should not overwrite them. |

## Task-2 implications

Recheck **6M versus 3M Trend** and **overlapping Trend versus Trend excluding the latest 1M**, with the same lineage and candidate-preservation discipline. Prioritize: the 1980 prolonged opposing-direction episodes; the February 2020 moving-reference transitions; October 1987 response speed; GFC cross-tenor and within-window divergence; 2022 midsummer relief; and 2023 long-end versus short-end behavior. Compare complete-episode frequencies and durations, Stable occupancy, and whether the four provisional recommendations retain their economic rationale. Distinguish reference/horizon effects from mapping effects and carry all data exclusions forward. Task 2 was **not performed**.
