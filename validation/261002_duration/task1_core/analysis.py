"""Standalone Task-1 research fixture; never imported by production Bondview.

Use --input for the FRED CSV or --replay for the committed observation CSV.
Only the Python standard library is required. Numerical diagnostics are emitted
separately from the analyst-written report; no recommendations are automated.
"""
import argparse
import csv
import hashlib
import itertools
import math
import json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path
from statistics import mean, median

TENORS = [('DGS6MO', '6M', 'Short'), ('DGS10', '10Y', 'Intermediate'),
          ('DGS30', '30Y', 'Long')]
STATES = ['Falling', 'Stable', 'Rising']
CASES = [f'{a} × {b}' for a in STATES for b in STATES]
MIXED = [CASES[i] for i in (2, 3, 5, 6)]
# Fixed user-supplied research configuration, not production model configuration.
RULES = [((1,), (2,), (3,)), ((1,), (1,), (2,)),
         ((0, 1), (1,), (1, 2)), ((0, 1), (1,), (1, 2)),
         ((0,), (0,), (0,)), ((-1, 0), (-1,), (-2, -1)),
         ((-1, 0), (-1,), (-2, -1)), ((-1,), (-1,), (-2,)),
         ((-1,), (-2,), (-3,))]
EVENTS = [
    ('1981-07-01', '1981-10-31', 'Volcker', 'Anchor'),
    ('1994-02-01', '1994-11-30', '1994 tightening', 'Anchor'),
    ('1998-08-01', '1998-10-31', 'Russia LTCM', 'Anchor'),
    ('2008-09-01', '2008-12-31', 'GFC', 'Anchor'),
    ('2013-05-01', '2013-09-30', 'Taper tantrum', 'Anchor'),
    ('2022-01-01', '2022-10-31', '2022 tightening', 'Anchor'),
    ('1987-08-01', '1987-10-31', '1987 crash', 'Challenge'),
    ('2020-02-01', '2020-03-31', 'COVID', 'Challenge'),
    ('2023-07-01', '2023-10-31', '2023 long-end selloff', 'Challenge'),
]
FIELDS = ['as_of', 'series_id', 'representative_tenor', 'duration_exposure',
          'yield_pct', 'availability', 'segment', 'observation_index',
          'endpoint_pct', 'recent_reference_pct', 'trend_reference_pct',
          'recent_reference_start', 'recent_reference_end',
          'trend_reference_start', 'trend_reference_end',
          'trend_bp', 'trend_state', 'recent_move_bp', 'recent_move_state',
          'rule_case', 'core_candidates', 'rule_episode_id', 'historical_event']


def state(value, threshold):
    return 'Falling' if value < -threshold else 'Rising' if value > threshold else 'Stable'


def calculate(raw):
    """Explicit raw -> smoothed features -> Components -> exposure-local fixture."""
    rows = []
    for ti, (series, tenor, exposure) in enumerate(TENORS):
        history, segment, episode, previous_case = [], 0, 0, None
        last_date = None
        for item in raw:
            ds = item['observation_date']
            r = dict.fromkeys(FIELDS, '')
            r.update(as_of=ds, series_id=series, representative_tenor=tenor,
                     duration_exposure=exposure, yield_pct=item.get(series, ''),
                     historical_event=';'.join(e[2] for e in EVENTS if e[0] <= ds <= e[1]))
            if series == 'DGS30' and '2002-02-18' <= ds < '2006-02-09':
                r['availability'] = 'documented_structural_gap'
                rows.append(r)
                continue
            if item.get(series, '') in ('', '.'):
                r['availability'] = 'no_source_observation'
                rows.append(r)
                continue
            current_date = date.fromisoformat(ds)
            # Conservative structural-break safeguard. Never compress the 30Y
            # 2002-2006 discontinuation into an apparent 126-observation horizon.
            if last_date is None or (current_date - last_date).days > 7:
                history, previous_case = [], None
                segment += 1
            last_date = current_date
            history.append((ds, Decimal(item[series]) * 100))
            t = len(history) - 1
            r.update(segment=segment, observation_index=t,
                     availability='insufficient_130_observation_history')
            if t >= 4:
                endpoint = sum(v for _, v in history[t-4:t+1]) / 5
                r['endpoint_pct'] = float(endpoint / 100)
            if t >= 25:
                reference = sum(v for _, v in history[t-25:t-20]) / 5
                recent = endpoint - reference
                r.update(recent_reference_pct=float(reference / 100),
                         recent_reference_start=history[t-25][0],
                         recent_reference_end=history[t-21][0],
                         recent_move_bp=float(recent), recent_move_state=state(recent, 10))
            if t >= 130:
                reference = sum(v for _, v in history[t-130:t-125]) / 5
                trend = endpoint - reference
                ts, rs = state(trend, 25), r['recent_move_state']
                case = f'{ts} × {rs}'
                if case != previous_case:
                    episode += 1
                previous_case = case
                r.update(availability='available', trend_reference_pct=float(reference / 100),
                         trend_reference_start=history[t-130][0],
                         trend_reference_end=history[t-126][0], trend_bp=float(trend),
                         trend_state=ts, rule_case=case,
                         core_candidates=json.dumps(RULES[CASES.index(case)][ti], separators=(',', ':')),
                         rule_episode_id=f'{tenor}-{episode:05d}')
            rows.append(r)
    return rows


def episodes(rows, field):
    groups = []
    for (_, key), group in itertools.groupby(rows, lambda r: (r['segment'], r[field])):
        g = list(group)
        groups.append(dict(key=key, start=g[0]['as_of'], end=g[-1]['as_of'], n=len(g), rows=g))
    return groups


def table(headers, data):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in data]) + '\n'


def pct(n, total):
    return f'{n} ({100*n/total:.2f}%)' if total else '0 (n/a)'


def extent(rows, field):
    values = [r[field] for r in rows]
    return f'{min(values):.1f} to {max(values):.1f}'


def diagnose(rows):
    out = []
    add = out.append
    valid = {tenor: [r for r in rows if r['representative_tenor'] == tenor and
                     r['availability'] == 'available'] for _, tenor, _ in TENORS}
    add('## Data coverage\n')
    coverage = []
    for series, tenor, exposure in TENORS:
        rr = [r for r in rows if r['representative_tenor'] == tenor and r['yield_pct'] not in ('', '.')]
        vv = valid[tenor]
        coverage.append([series, f"{rr[0]['as_of']} – {rr[-1]['as_of']}", len(rr),
                         f"{vv[0]['as_of']} – {vv[-1]['as_of']}", len(vv), sum(r['availability'] == 'insufficient_130_observation_history' for r in rr)])
    add(table(['Series', 'Downloaded nonmissing range', 'Downloaded nonmissing n', 'Calculable outer range', 'Valid n', 'Lookback exclusions'], coverage))
    for _, tenor, _ in TENORS:
        rr = [r for r in rows if r['representative_tenor'] == tenor and r['yield_pct'] not in ('', '.') and r['availability'] != 'documented_structural_gap']
        for seg, group in itertools.groupby(rr, lambda r: r['segment']):
            gg = list(group)
            excluded = [r for r in gg if r['availability'] != 'available']
            add(f"- {tenor} segment {seg}: raw {gg[0]['as_of']} through {gg[-1]['as_of']}; "
                f"lookback exclusions {excluded[0]['as_of']} through {excluded[-1]['as_of']} ({len(excluded)} observations); "
                f"first calculable {gg[130]['as_of']}.\n")
        gaps = [(a['as_of'], b['as_of'], (date.fromisoformat(b['as_of'])-date.fromisoformat(a['as_of'])).days)
                for a, b in zip(rr, rr[1:]) if (date.fromisoformat(b['as_of'])-date.fromisoformat(a['as_of'])).days > 4]
        add(f"\n{tenor}: gaps longer than four calendar days between observations: {gaps}.\n")
    add('## Analysis A — numerical diagnostics\n')
    for _, tenor, exposure in TENORS:
        vv = valid[tenor]
        add(f'### {exposure} / {tenor}\n')
        for field in ('trend_state', 'recent_move_state'):
            eps = episodes(vv, field)
            counts = Counter(r[field] for r in vv)
            data = []
            for st in STATES:
                durations = [e['n'] for e in eps if e['key'] == st]
                data.append([st, pct(counts[st], len(vv)), len(durations), f'{mean(durations):.2f}',
                             median(durations), max(durations), sum(n == 1 for n in durations)])
            add(f'**{field}**\n')
            add(table(['State', 'Observations', 'Episodes', 'Mean duration', 'Median', 'Max', 'One-observation episodes'], data))
            trans = Counter((a[field], b[field]) for a, b in zip(vv, vv[1:]) if a['segment'] == b['segment'])
            add(table(['From / to'] + STATES, [[s] + [trans[s, t] for t in STATES] for s in STATES]))
            denominator = sum(trans.values())
            switches = sum(n for (a, b), n in trans.items() if a != b)
            add(f'Switching: {pct(switches, denominator)} of adjacent valid within-segment pairs. Diagonal counts are persistence.\n')
        counts = Counter(r['rule_case'] for r in vv)
        add(table(['Rule Case', 'Observations'], [[c, pct(counts[c], len(vv))] for c in CASES]))
        add(f"Four mixed cases combined: {pct(sum(counts[c] for c in MIXED), len(vv))}.\n")
        candidates = Counter(r['core_candidates'] for r in vv)
        add(table(['Core candidate set (singletons settled)', 'Observations'], [[c, pct(n, len(vv))] for c, n in sorted(candidates.items())]))
        lo = Counter(min(json.loads(r['core_candidates'])) for r in vv)
        hi = Counter(max(json.loads(r['core_candidates'])) for r in vv)
        add(table(['Ordinal category', 'All lower candidates', 'All higher candidates'],
                  [[n, pct(lo[n], len(vv)), pct(hi[n], len(vv))] for n in range(-3, 4)]))
    bydate = defaultdict(dict)
    for tenor, vv in valid.items():
        for r in vv:
            bydate[r['as_of']][tenor] = r
    common = {d: r for d, r in bydate.items() if len(r) == 3}
    counts = Counter(len({r['rule_case'] for r in rr.values()}) for rr in common.values())
    add('### Cross-exposure common-date comparison\n')
    add(table(['Distinct cases across three tenors', 'Dates'], [[n, pct(counts[n], len(common))] for n in (1, 2, 3)]))
    add('Representative disagreements: first common date with three distinct cases in each predefined event (deterministic; no return filter).\n')
    examples = []
    for start, end, name, _ in EVENTS:
        dates = [d for d, rr in common.items() if start <= d <= end and len({r['rule_case'] for r in rr.values()}) == 3]
        if dates:
            d = min(dates)
            examples.append([name, d] + [f"{common[d][t]['rule_case']} ({common[d][t]['trend_bp']:.1f}, {common[d][t]['recent_move_bp']:.1f} bp)" for _, t, _ in TENORS])
    add(table(['Event', 'Date', '6M', '10Y', '30Y'], examples))
    add('## Analysis B — predefined event evidence\n')
    add('All valid daily observations are in the CSV. Tables below select the first and last valid date of every calendar month, before looking at states. Transition lists additionally include every Rule Case episode within each event; durations count observations. No calendar dates are filled.\n')
    for start, end, name, kind in EVENTS:
        add(f'### {name} ({kind}), {start} through {end}\n')
        for _, tenor, exposure in TENORS:
            vv = [r for r in valid[tenor] if start <= r['as_of'] <= end]
            add(f'**{exposure} / {tenor}**\n')
            if not vv:
                add('Unavailable: no calculable observations in this window.\n')
                continue
            counts = Counter(r['core_candidates'] for r in vv)
            add(f"All {len(vv)} observations: " + '; '.join(f'{k}: {pct(v, len(vv))}' for k, v in sorted(counts.items())) + '.\n')
            selected = []
            for month, group in itertools.groupby(vv, lambda r: r['as_of'][:7]):
                g = list(group)
                selected.extend([g[0], g[-1]] if len(g) > 1 else g)
            add(table(['as_of', 'Yield %', 'Trend bp', 'Trend', 'Recent bp', 'Recent', 'Rule Case', 'Core set'],
                      [[r['as_of'], r['yield_pct'], f"{r['trend_bp']:.1f}", r['trend_state'],
                        f"{r['recent_move_bp']:.1f}", r['recent_move_state'], r['rule_case'], r['core_candidates']] for r in selected]))
            add('Rule Case path (event-clipped episodes): ' + '; '.join(f"{e['start']}–{e['end']} {e['key']} ({e['n']})" for e in episodes(vv, 'rule_case')) + '.\n')
    add('## Analysis C — complete mixed-episode evidence\n')
    add('An episode is a maximal same-case run of available observations within one continuous data segment. Missing routine source days do not create artificial episodes. Full-sample endpoints are censored; event-clipped runs above are not used as independent episodes here. Selection: longest duration; largest absolute Recent Move anywhere in episode; typical episode minimizing duration distance from the episode median, then distance of episode median absolute Recent Move from the median across episodes. Ties use earliest start. Selected roles may coincide; they are not extra independent examples.\n')
    for _, tenor, exposure in TENORS:
        eps = episodes(valid[tenor], 'rule_case')
        add(f'### {exposure} / {tenor}\n')
        summary, chosen = [], []
        for case in MIXED:
            ee = [e for e in eps if e['key'] == case]
            durations = sorted(e['n'] for e in ee)
            rr = [r for e in ee for r in e['rows']]
            # Nearest-rank quartiles, explicit to avoid library-specific interpolation.
            q = lambda p: durations[max(0, math.ceil(p*len(durations))-1)]
            summary.append([case, len(ee), len(rr), f'{mean(durations):.2f}',
                            f'{min(durations)} / {q(.25)} / {median(durations)} / {q(.75)} / {max(durations)}',
                            extent(rr, 'trend_bp'), extent(rr, 'recent_move_bp')])
            longest = max(ee, key=lambda e: e['n'])
            largest = max(ee, key=lambda e: max(abs(r['recent_move_bp']) for r in e['rows']))
            typical_magnitude = median(median(abs(r['recent_move_bp']) for r in e['rows']) for e in ee)
            typical = min(ee, key=lambda e: (abs(e['n']-median(durations)),
                          abs(median(abs(r['recent_move_bp']) for r in e['rows'])-typical_magnitude), e['start']))
            for role, e in [('longest', longest), ('largest Recent Move', largest), ('typical', typical)]:
                chosen.append([case, role, f"{e['start']} – {e['end']}", e['n'],
                               extent(e['rows'], 'trend_bp'), extent(e['rows'], 'recent_move_bp'),
                               e['rows'][0]['rule_episode_id']])
        add(table(['Case', 'Episodes', 'Observations', 'Mean duration', 'Min / Q1 / median / Q3 / max', 'Trend range bp', 'Recent range bp'], summary))
        add(table(['Case', 'Selection', 'Episode', 'n', 'Trend range bp', 'Recent range bp', 'CSV episode ID'], chosen))
    return '\n'.join(out)


def checks(raw, rows):
    assert len({r['observation_date'] for r in raw}) == len(raw)
    assert [r['observation_date'] for r in raw] == sorted(r['observation_date'] for r in raw)
    assert len(rows) == len(raw) * 3
    for threshold in (10, 25):
        assert [state(Decimal(v), threshold) for v in (-threshold-.2, -threshold, threshold, threshold+.2)] == ['Falling', 'Stable', 'Stable', 'Rising']
    # Known linear path: 1 bp per valid observation yields exactly 21 and 126 bp.
    from datetime import timedelta
    fixture = []
    day = date(2000, 1, 3)
    while len(fixture) < 140:
        if day.weekday() < 5:
            fixture.append({'observation_date': day.isoformat(),
                            **{series: str(Decimal(100 + len(fixture)) / 100)
                               for series, _, _ in TENORS}})
        day += timedelta(days=1)
    synthetic = calculate(fixture)
    for r in synthetic:
        if r['availability'] == 'available':
            assert r['trend_bp'] == 126 and r['recent_move_bp'] == 21
            assert r['rule_case'] == 'Rising × Rising'
    assert sum(r['availability'] == 'available' for r in synthetic) == 30
    for r in rows:
        if r['availability'] == 'available':
            assert r['observation_index'] >= 130
            assert r['trend_reference_end'] < r['recent_reference_end'] < r['as_of']
            assert abs((r['endpoint_pct'] - r['trend_reference_pct'])*100-r['trend_bp']) < 1e-8
            assert abs((r['endpoint_pct'] - r['recent_reference_pct'])*100-r['recent_move_bp']) < 1e-8
            assert r['rule_case'] == f"{r['trend_state']} × {r['recent_move_state']}"
    # All candidate combinations obey the requested weak ordinal orders.
    for ti in range(3):
        for ff, fs, fr in itertools.product(RULES[0][ti], RULES[1][ti], RULES[2][ti]):
            assert ff >= fs >= fr
        for rf, rs, rr in itertools.product(RULES[6][ti], RULES[7][ti], RULES[8][ti]):
            assert rf >= rs >= rr
    for i in (0, 1, 2, 3):
        for short, intermediate, long in itertools.product(*RULES[i]):
            assert long >= intermediate >= short
    for i in (5, 6, 7, 8):
        for short, intermediate, long in itertools.product(*RULES[i]):
            assert short >= intermediate >= long


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--input', type=Path)
    inputs.add_argument('--replay', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--diagnostics', type=Path, required=True)
    args = parser.parse_args()
    if args.input:
        with args.input.open() as f:
            raw = list(csv.DictReader(f))
    else:
        bydate = {}
        with args.replay.open() as f:
            for r in csv.DictReader(f):
                bydate.setdefault(r['as_of'], {'observation_date': r['as_of']})[r['series_id']] = r['yield_pct']
        raw = list(bydate.values())
    assert raw and set(raw[0]) == {'observation_date', 'DGS6MO', 'DGS10', 'DGS30'}
    rows = calculate(raw)
    checks(raw, rows)
    with args.output.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    args.diagnostics.write_text(diagnose(rows))
    print(json.dumps({'rows': len(rows), 'calculable': sum(r['availability'] == 'available' for r in rows),
                      'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'checks': 'passed'}, indent=2))


if __name__ == '__main__':
    main()
