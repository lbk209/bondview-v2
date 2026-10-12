"""Focused synthetic contract tests. Live FRED execution is recorded separately."""

import copy
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from duration_config import load_config, validate_config
from duration_components import calculate_components, classify_plain, classify_trend
from duration_core import evaluate_core
from duration_results import load_results, save_results
from duration_plot import DurationControls, common_available_range, create_chart
from fred_data import acquire_fred, parse_fred_csv, prepare_observations


def synthetic_results(config=None):
    config = load_config() if config is None else config
    dates = pd.bdate_range("1990-01-01", periods=180)
    frames = []
    for series in ("DGS6MO", "DGS10", "DGS30"):
        raw = pd.DataFrame({"date": dates, "raw_yield_pct": 4 + np.arange(len(dates)) * .01})
        frames.append(prepare_observations(raw, series))
    components = calculate_components(pd.concat(frames, ignore_index=True), config["trend"], config["recent_move"])
    return evaluate_core(components, config["exposures"], config["rules"])


class ComponentsTest(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.parameters = self.config["trend"]

    def classify(self, values, **changes):
        return classify_trend(pd.Series(values, dtype=float), {**self.parameters, **changes}).tolist()

    def test_plain_strict_thresholds(self):
        self.assertEqual(classify_plain(pd.Series([-25.01, -25, 0, 25, 25.01]), 25).tolist(),
                         ["Falling", "Stable", "Stable", "Stable", "Rising"])
        self.assertEqual(classify_plain(pd.Series([-10.01, -10, 10, 10.01]), 10).tolist(),
                         ["Falling", "Stable", "Stable", "Rising"])

    def test_initialization_and_persistence_both_directions(self):
        self.assertEqual(self.classify([30, 20, 26, 26, 26]),
                         ["Rising", "Stable", "Stable", "Stable", "Rising"])
        self.assertEqual(self.classify([-30, -20, -26, -26, -26]),
                         ["Falling", "Stable", "Stable", "Stable", "Falling"])
        self.assertEqual(self.classify([0, 25, 26, 26, 26]),
                         ["Stable", "Stable", "Stable", "Stable", "Rising"])

    def test_pending_neutral_reset_and_opposing_replacement(self):
        self.assertEqual(self.classify([0, 30, 30, 25, 30, -30, -30, -30]),
                         ["Stable"] * 7 + ["Falling"])

    def test_hysteresis_boundary_inequalities(self):
        self.assertEqual(self.classify([30, 25, 20.001, 20]),
                         ["Rising", "Rising", "Rising", "Stable"])
        self.assertEqual(self.classify([-30, -25, -20.001, -20]),
                         ["Falling", "Falling", "Falling", "Stable"])

    def test_direct_reversal_priority_and_reversed_state_exit(self):
        self.assertEqual(self.classify([30, -30, -20, 30, 30, 30]),
                         ["Rising", "Falling", "Stable", "Stable", "Stable", "Rising"])
        self.assertEqual(self.classify([-30, 30, -30, 30]),
                         ["Falling", "Rising", "Falling", "Rising"])

    def test_full_threshold_reversal_is_strict(self):
        self.assertEqual(self.classify([30, -25, -26, -26, -26]),
                         ["Rising", "Stable", "Stable", "Stable", "Falling"])
        self.assertEqual(self.classify([-30, 25, 26, 26, 26]),
                         ["Falling", "Stable", "Stable", "Stable", "Rising"])

    def test_reversal_after_exit_requires_persistence(self):
        self.assertEqual(self.classify([30, 18, -100, -100, -100]),
                         ["Rising", "Stable", "Stable", "Stable", "Falling"])

    def test_reversal_can_be_disabled(self):
        self.assertEqual(self.classify([30, -30, -30, -30, -30], direct_reversal=False),
                         ["Rising", "Stable", "Stable", "Stable", "Falling"])

    def test_invalid_observation_does_not_confirm_or_reset(self):
        states = self.classify([np.nan, 0, 30, np.nan, 30, 30])
        self.assertTrue(pd.isna(states[0]))
        self.assertTrue(pd.isna(states[3]))
        self.assertEqual([states[i] for i in (1, 2, 4, 5)], ["Stable", "Stable", "Stable", "Rising"])

    def test_plain_disabled(self):
        self.assertEqual(self.classify([0, 30, 24, -30], stabilization_enabled=False),
                         ["Stable", "Rising", "Stable", "Falling"])

    def test_stabilization_switch_preserves_component_values(self):
        baseline = synthetic_results(self.config)
        experimental = copy.deepcopy(self.config)
        experimental["trend"]["stabilization_enabled"] = False
        plain = synthetic_results(experimental)
        columns = ["smoothed_yield_bp", "trend_value_bp", "recent_move_value_bp", "recent_move_state"]
        assert_frame_equal(baseline[columns], plain[columns], check_exact=True)
        expected = classify_plain(plain["trend_value_bp"], 25)
        self.assertEqual(plain["trend_state"].fillna("missing").tolist(), expected.fillna("missing").tolist())

    def test_default_formulas_valid_observation_offsets(self):
        dates = pd.bdate_range("1990-01-01", periods=170)
        yields = np.arange(170, dtype=float) / 100
        yields[10] = np.nan
        obs = prepare_observations(pd.DataFrame({"date": dates, "raw_yield_pct": yields}), "DGS10")
        result = calculate_components(obs, self.parameters, self.config["recent_move"])
        valid = result.loc[result["availability"].eq("accepted")].reset_index(drop=True)
        self.assertTrue(valid.loc[:129, "trend_value_bp"].isna().all())
        self.assertAlmostEqual(valid.loc[130, "smoothed_yield_bp"], 129)
        self.assertAlmostEqual(valid.loc[130, "trend_reference_bp"], 2)
        self.assertEqual(valid.loc[130, "trend_value_bp"], 127)
        self.assertEqual(valid.loc[130, "recent_move_value_bp"], 21)
        self.assertEqual(valid.loc[130, "trend_reference_date"], valid.loc[4, "date"])
        self.assertTrue(result.loc[10, ["smoothed_yield_bp", "trend_state", "recent_move_state"]].isna().all())

    def test_configured_lookbacks_and_shared_smoothing(self):
        config = copy.deepcopy(self.config)
        config["trend"].update(lookback_observations=2, smoothing_observations=2)
        config["recent_move"]["lookback_observations"] = 1
        raw = pd.DataFrame({"date": pd.bdate_range("2000-01-01", periods=5),
                            "raw_yield_pct": [1, 2, 3, 4, 5]})
        result = calculate_components(prepare_observations(raw, "DGS10"), config["trend"], config["recent_move"])
        self.assertEqual(result.loc[3, "trend_value_bp"], 200)
        self.assertEqual(result.loc[3, "recent_move_value_bp"], 100)

    def test_binary_threshold_dust_is_removed(self):
        config = copy.deepcopy(self.config)
        config["trend"].update(lookback_observations=1, smoothing_observations=1)
        config["recent_move"]["lookback_observations"] = 1
        raw = pd.DataFrame({"date": pd.bdate_range("2000-01-01", periods=3),
                            "raw_yield_pct": [4.03, 4.28, 4.38]})
        result = calculate_components(prepare_observations(raw, "DGS10"), config["trend"], config["recent_move"])
        self.assertEqual(result.loc[1, "trend_value_bp"], 25)
        self.assertEqual(result.loc[1, "trend_state"], "Stable")
        self.assertEqual(result.loc[2, "recent_move_value_bp"], 10)
        self.assertEqual(result.loc[2, "recent_move_state"], "Stable")

    def test_structural_reset_warmup_and_plain_reinitialization(self):
        dates = list(pd.bdate_range(end="2002-02-15", periods=140))
        dates += [pd.Timestamp("2003-01-01")]
        dates += list(pd.bdate_range(start="2006-02-09", periods=140))
        raw = pd.DataFrame({"date": dates, "raw_yield_pct": np.r_[4 + np.arange(140) * .01,
                            99, 5 - np.arange(140) * .01]})
        obs = prepare_observations(raw, "DGS30")
        result = calculate_components(obs, self.parameters, self.config["recent_move"])
        self.assertTrue(result.loc[140:270, "trend_state"].isna().all())
        self.assertEqual(result.loc[139, "trend_state"], "Rising")
        self.assertEqual(result.loc[271, "trend_state"], "Falling")
        self.assertEqual(result.loc[141, "observation_index"], 0)
        self.assertEqual(result.loc[271, "trend_reference_date"], result.loc[145, "date"])
        # A pending count from the old segment cannot affect the new one.
        first = self.classify([0, 30, 30])
        second = self.classify([0, 30, 30, 30])
        self.assertEqual(first[-1], "Stable")
        self.assertEqual(second, ["Stable", "Stable", "Stable", "Rising"])


class AcquisitionTest(unittest.TestCase):
    def response(self, request, timeout):
        series = request.full_url.split("id=")[1].split("&")[0]
        import io
        return io.BytesIO(f"observation_date,{series}\n2000-01-03,4.01\n2000-01-04,.\n2000-01-05,4.02\n".encode())

    def test_fresh_cache_reuse_forced_refresh_and_provenance(self):
        with tempfile.TemporaryDirectory() as folder, patch("fred_data.urlopen", side_effect=self.response) as download:
            fresh, provenance = acquire_fred(folder)
            self.assertEqual(download.call_count, 3)
            cached, saved_provenance = acquire_fred(folder)
            self.assertEqual(download.call_count, 3)
            assert_frame_equal(fresh, cached)
            self.assertEqual(provenance, saved_provenance)
            self.assertEqual(set(provenance["series"]), {"DGS6MO", "DGS10", "DGS30"})
            self.assertEqual(provenance["series"]["DGS10"]["units"], "percent")
            acquire_fred(folder, refresh=True)
            self.assertEqual(download.call_count, 6)

    def test_invalid_cache_redownloads(self):
        with tempfile.TemporaryDirectory() as folder, patch("fred_data.urlopen", side_effect=self.response) as download:
            acquire_fred(folder)
            (Path(folder) / "DGS10.csv").write_text("broken")
            with self.assertWarns(UserWarning):
                acquire_fred(folder)
            self.assertEqual(download.call_count, 4)

    def test_failure_without_cache_and_explicit_failed_refresh(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch("fred_data.urlopen", side_effect=OSError("offline")):
                with self.assertRaisesRegex(RuntimeError, "DGS6MO"):
                    acquire_fred(folder)
            with patch("fred_data.urlopen", side_effect=self.response):
                before, _ = acquire_fred(folder)
            with patch("fred_data.urlopen", side_effect=OSError("offline")):
                with self.assertRaises(RuntimeError):
                    acquire_fred(folder, refresh=True)
                cached, _ = acquire_fred(folder)
                assert_frame_equal(before, cached)

    def test_source_gap_endpoints_excluded_even_with_numbers(self):
        raw = pd.DataFrame({"date": pd.to_datetime(["2002-02-15", "2002-02-18", "2006-02-08", "2006-02-09"]),
                            "raw_yield_pct": [4, 99, 99, 5]})
        accepted = prepare_observations(raw, "DGS30")
        self.assertEqual(accepted["availability"].tolist(),
                         ["accepted", "structural_gap", "structural_gap", "accepted"])
        self.assertTrue(accepted.loc[1:2, "yield_pct"].isna().all())
        self.assertEqual(accepted.loc[3, "observation_index"], 0)
        self.assertEqual(accepted.loc[3, "segment"], 2)
        self.assertEqual(accepted.loc[1, "raw_yield_pct"], 99)

    def test_reject_malformed_extracts(self):
        for payload in (b"date,DGS10\n2000-01-01,4", b"DATE,DGS10\n2000-01-01,nope",
                        b"DATE,DGS10\n2000-01-01,4\n2000-01-01,5", b"DATE,DGS10\n2000-01-01,."):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                parse_fred_csv(payload, "DGS10")


class CoreAndPersistenceTest(unittest.TestCase):
    def test_all_twenty_seven_rules_against_accepted_table(self):
        config = load_config()
        states = ["Falling", "Stable", "Rising"]
        components = pd.DataFrame([
            {"date": pd.Timestamp("2000-01-01") + pd.Timedelta(days=i * 3 + j),
             "series_id": identity["series_id"], "trend_state": a,
             "recent_move_state": b, "availability": "accepted"}
            for identity in config["exposures"].values()
            for i, a in enumerate(states) for j, b in enumerate(states)])
        before = components.copy(deep=True)
        result = evaluate_core(components, config["exposures"], config["rules"])
        expected = [[1, 1, 1, 1, 0, -1, -1, -1, -1],
                    [2, 1, 1, 1, 0, -1, -1, -1, -2],
                    [3, 2, 1, 1, 0, -1, -1, -2, -3]]
        for exposure, scores in zip(config["exposures"], expected):
            self.assertEqual(result.loc[result["duration_exposure"].eq(exposure), "core_score"].tolist(), scores)
        assert_frame_equal(components, before)

    def test_upstream_independent_of_core_mapping_and_exposure_selection(self):
        config = load_config()
        result = synthetic_results(config)
        component_columns = ["date", "series_id", "smoothed_yield_bp", "trend_value_bp", "trend_state",
                             "recent_move_value_bp", "recent_move_state"]
        components = result.drop(columns=["duration_exposure", "representative_tenor",
                                          "rule_case", "core_score", "core_availability"]).copy()
        changed_rules = copy.deepcopy(config["rules"])
        changed_rules["Rising × Rising"]["Long"] = 0
        changed = evaluate_core(components, config["exposures"], changed_rules)
        assert_frame_equal(result[component_columns], changed[component_columns])
        create_chart(changed, "Short")
        create_chart(changed, "Long")
        assert_frame_equal(result[component_columns], changed[component_columns])

    def test_roundtrip_and_snapshot_only_load(self):
        config = load_config()
        result = synthetic_results(config)
        with tempfile.TemporaryDirectory() as folder:
            save_results(result, {"test_source": "synthetic"}, config, folder)
            loaded, meta = load_results(folder, expected_config=config)
            assert_frame_equal(result, loaded, check_dtype=False, check_exact=True)
            self.assertEqual(meta["result_kind"], "Core Duration Evaluation Result")
            self.assertEqual(meta["rows"], len(result))
            changed = copy.deepcopy(config)
            changed["trend"]["lookback_observations"] = 63
            with self.assertRaisesRegex(ValueError, "Configuration mismatch"):
                load_results(folder, expected_config=changed)
            load_results(folder)  # Explicit saved-snapshot inspection remains possible.
            changed = copy.deepcopy(config)
            changed["historical_events"]["GFC"]["start"] = "2008-01-01"
            load_results(folder, expected_config=changed)  # Presentation-only change.

    def test_corruption_rejected(self):
        config = load_config()
        with tempfile.TemporaryDirectory() as folder:
            save_results(synthetic_results(), {}, config, folder)
            path = Path(folder) / "duration_core.csv"
            path.write_text(path.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "checksum"):
                load_results(folder)

    def test_invalid_ordinal_and_incomplete_results_rejected(self):
        config = load_config()
        result = synthetic_results()
        with tempfile.TemporaryDirectory() as folder:
            result.loc[result["core_score"].notna(), "core_score"] = 4
            with self.assertRaisesRegex(ValueError, "ordinal"):
                save_results(result, {}, config, folder)
            with self.assertRaisesRegex(ValueError, "all three"):
                save_results(synthetic_results().query("duration_exposure == 'Short'"), {}, config, folder)

    def test_configuration_validation(self):
        for section, key, value in (("trend", "persistence", 0), ("trend", "direct_reversal", "yes"),
                                    ("trend", "lookback_observations", True),
                                    ("recent_move", "threshold_bp", float("nan"))):
            with self.subTest(key=key):
                config = load_config()
                config[section][key] = value
                with self.assertRaises(ValueError):
                    validate_config(config)
        config = load_config()
        config["rules"].pop("Rising × Rising")
        with self.assertRaises(ValueError):
            validate_config(config)
        config = load_config()
        config["trend"]["hysteresis_bp"] = 25
        with self.assertRaises(ValueError):
            validate_config(config)


class VisualizationTest(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.result = synthetic_results()

    def test_axes_selection_and_saved_hover(self):
        figure = create_chart(self.result, "Long")
        self.assertIn("Long / 30Y", figure.layout.title.text)
        self.assertEqual(figure.layout.yaxis.title.text, "Treasury yield (%)")
        self.assertEqual(tuple(figure.layout.yaxis2.tickvals), tuple(range(-3, 4)))
        self.assertEqual(figure.data[1].line.shape, "hv")
        self.assertFalse(figure.data[1].connectgaps)
        self.assertEqual(figure.layout.hovermode, "x unified")
        row = self.result.loc[self.result["duration_exposure"].eq("Long")].iloc[-1]
        self.assertEqual(figure.data[0].customdata[-1].tolist(),
                         row[["yield_pct", "trend_value_bp", "trend_state", "recent_move_value_bp",
                              "recent_move_state", "rule_case", "core_score"]].tolist())
        self.assertEqual(figure.layout.shapes[0].yref, "y2")

    def test_render_emits_interactive_notebook_mime(self):
        ui = DurationControls(self.result, self.config["historical_events"])
        figure = ui.figure()
        with patch.object(ui, "figure", return_value=figure), patch.object(figure, "show") as show:
            ui.render()
            show.assert_called_once_with(renderer="plotly_mimetype")

    def test_custom_dates_preserved_and_preset_dates_disabled(self):
        ui = DurationControls(self.result, self.config["historical_events"])
        self.assertEqual(ui.exposure.value, "Intermediate")
        self.assertEqual(ui.custom_dates, common_available_range(self.result))
        with patch.object(ui, "render"):
            ui.start.value, ui.end.value = date(1990, 4, 1), date(1990, 6, 1)
            ui.period.value = "GFC"
            self.assertTrue(ui.start.disabled and ui.end.disabled)
            self.assertEqual(ui.start.value, date(2008, 9, 1))
            self.assertEqual(ui.end.value, date(2008, 12, 31))
            ui.period.value = "Custom period"
            self.assertEqual((ui.start.value, ui.end.value), (date(1990, 4, 1), date(1990, 6, 1)))
            self.assertFalse(ui.start.disabled or ui.end.disabled)

    def test_controls_have_no_acquisition_or_calculation(self):
        with patch("fred_data.urlopen", side_effect=AssertionError("network")), \
             patch("duration_components.calculate_components", side_effect=AssertionError("components")), \
             patch("duration_core.evaluate_core", side_effect=AssertionError("mapping")):
            ui = DurationControls(self.result, self.config["historical_events"])
            with patch.object(ui, "render"):
                for exposure in self.config["exposures"]:
                    ui.exposure.value = exposure
                    ui.figure()
                for event in self.config["historical_events"]:
                    ui.period.value = event
                    ui.figure()

    def test_empty_reversed_and_partial_periods(self):
        empty = create_chart(self.result, start="2020-01-01", end="2020-02-01")
        self.assertEqual(len(empty.data[0].x), 0)
        self.assertTrue(empty.layout.annotations)
        reverse = create_chart(self.result, start="2000-01-01", end="1990-01-01")
        self.assertEqual(len(reverse.data[0].x), 0)
        partial = create_chart(self.result, start="1980-01-01", end="1990-07-20")
        self.assertGreater(len(partial.data[0].x), 0)
        self.assertTrue(partial.layout.annotations)

    def test_structural_separator_when_source_omits_gap_rows(self):
        rows = self.result.loc[self.result["duration_exposure"].eq("Long")].tail(2).copy()
        rows["date"] = pd.to_datetime(["2002-02-15", "2006-08-15"])
        rows["segment"] = pd.Series([1, 2], index=rows.index, dtype="Int64")
        figure = create_chart(rows, "Long")
        self.assertEqual(len(figure.data[0].x), 3)
        self.assertTrue(np.isnan(figure.data[0].y[1]))
        self.assertTrue(np.isnan(figure.data[1].y[1]))

    def test_default_intersection_does_not_discard_exposure_history(self):
        rows = self.result.copy()
        short = rows["duration_exposure"].eq("Short")
        rows.loc[short, "date"] += pd.Timedelta(days=7)
        shared_start, shared_end = common_available_range(rows)
        ui = DurationControls(rows, self.config["historical_events"])
        self.assertEqual(ui.custom_dates, (shared_start, shared_end))
        self.assertEqual(len(ui.results), len(rows))
        self.assertGreater(len(create_chart(ui.results, "Short").data[0].x),
                           len(create_chart(ui.results, "Short", shared_start, shared_end).data[0].x))
        unavailable = rows.copy()
        unavailable["core_availability"] = "warmup"
        self.assertEqual(common_available_range(unavailable), (None, None))


if __name__ == "__main__":
    unittest.main()
