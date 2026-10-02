"""Focused Stage 1 contracts; synthetic fixtures are never historical results."""
from copy import deepcopy
from itertools import product
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
import yaml

from duration_model import load_config, calculate_features, calculate_components, calculate_view


class DurationStage1Tests(unittest.TestCase):
    def setUp(self):
        self.config = load_config()
        self.as_of = '2024-09-30'
        self.raw = {}
        for alias, spec in self.config['series'].items():
            frequency = {'business_daily': 'B', 'daily': 'D', 'monthly': 'MS'}[spec['frequency']]
            index = pd.date_range('2017-01-01', self.as_of, freq=frequency)
            values = 100 * 1.002 ** np.arange(len(index)) if alias == 'inflation' else np.arange(len(index)) * 0.01
            self.raw[alias] = pd.Series(values, index=index)
            self.raw[alias].attrs['vintage_date'] = self.as_of

    def test_formulas_and_lineage(self):
        features = calculate_features(self.raw, self.config, self.as_of)
        components = calculate_components(features, self.config)
        self.assertAlmostEqual(components.loc['Long-End Yield Trend', 'value'], 63)
        self.assertAlmostEqual(components.loc['Recent Long-End Yield Move', 'value'], 21)
        self.assertAlmostEqual(components.loc['Policy Direction', 'value'], 90)
        self.assertAlmostEqual(components.loc['Inflation Trend', 'value'], 0)
        inflation = features.loc['inflation_trend_endpoints']
        self.assertAlmostEqual(inflation['current'], (1.002 ** 12 - 1) * 100)
        self.assertEqual(inflation['base_end'], pd.Timestamp('2024-06-01'))
        self.assertEqual(inflation['base_denominator_end'], pd.Timestamp('2023-06-01'))
        self.assertEqual(calculate_view(components, self.config)['view'], 'duration_headwind')

    def test_future_observations_excluded_and_inputs_unchanged(self):
        baseline = calculate_features(self.raw, self.config, self.as_of)
        for series in self.raw.values():
            series.loc[pd.Timestamp('2025-01-01')] = 999999
        originals = {name: series.copy(deep=True) for name, series in self.raw.items()}
        with_future = calculate_features(self.raw, self.config, self.as_of)
        pd.testing.assert_frame_equal(baseline, with_future)
        for name, series in self.raw.items():
            pd.testing.assert_series_equal(series, originals[name])
        self.raw['inflation'].attrs['vintage_date'] = '2025-01-01'
        with self.assertRaisesRegex(ValueError, 'vintage'):
            calculate_features(self.raw, self.config, self.as_of)

    def test_missing_stale_short_and_nonfinite_data_rejected(self):
        for kind in ('missing_month', 'stale', 'short', 'nonfinite'):
            with self.subTest(kind=kind):
                raw = deepcopy(self.raw)
                if kind == 'missing_month':
                    raw['inflation'] = raw['inflation'].drop(pd.Timestamp('2024-04-01'))
                elif kind == 'stale':
                    raw['long_yield'] = raw['long_yield'].loc[:'2024-08-01']
                elif kind == 'short':
                    raw['long_yield'] = raw['long_yield'].iloc[-10:]
                else:
                    raw['long_yield'].iloc[-1] = np.inf
                with self.assertRaises(ValueError):
                    calculate_features(raw, self.config, self.as_of)

    def test_inclusive_component_thresholds(self):
        features = calculate_features(self.raw, self.config, self.as_of)
        for value, expected in [(-0.26, 'falling'), (-0.25, 'stable'), (0.25, 'stable'), (0.26, 'rising')]:
            features.loc['yield_trend_endpoints', ['base', 'current']] = [0, value]
            actual = calculate_components(features, self.config)
            self.assertEqual(actual.loc['Long-End Yield Trend', 'state'], expected)

    def test_all_81_rule_cases_and_view_thresholds(self):
        components = calculate_components(calculate_features(self.raw, self.config, self.as_of), self.config)
        for states in product(*[spec['states'] for spec in self.config['components'].values()]):
            components['state'] = states
            result = calculate_view(components, self.config)
            votes = [self.config['view']['contributions'][name][state]
                     for name, state in zip(components.index, states)]
            expected = 'duration_supportive' if sum(votes) >= 2 else 'duration_headwind' if sum(votes) <= -2 else 'mixed'
            self.assertEqual(result['view'], expected)
            self.assertEqual(list(result['rule_case']), list(components.index))
        components.loc['Policy Direction', 'as_of'] = pd.Timestamp('2020-01-01')
        with self.assertRaisesRegex(ValueError, 'one as_of'):
            calculate_view(components, self.config)

    def test_invalid_config_rejected(self):
        for kind in ('horizon', 'mapping', 'reference', 'threshold', 'year'):
            config = deepcopy(self.config)
            if kind == 'horizon':
                config['features']['yield_trend_endpoints']['lag'] = 0
            elif kind == 'mapping':
                del config['view']['contributions']['Policy Direction']['easing']
            elif kind == 'reference':
                config['components']['Policy Direction']['feature'] = 'missing'
            elif kind == 'threshold':
                config['components']['Policy Direction']['threshold'] = float('nan')
            else:
                config['features']['inflation_trend_endpoints']['year_periods'] = 6
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'invalid.yaml'
                path.write_text(yaml.safe_dump(config, sort_keys=False))
                with self.assertRaises(ValueError):
                    load_config(path)


if __name__ == '__main__':
    unittest.main()
