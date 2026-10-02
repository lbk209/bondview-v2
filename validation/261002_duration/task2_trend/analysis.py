"""Frozen-snapshot Task-2 research; no production model or network access.

Run from repository root. Outputs comparison.csv and numerical Markdown evidence;
the committed report adds human-reviewable economic judgments to that evidence.
"""
import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import math
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from statistics import mean, median

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / 'task1_core' / 'results.csv'
SHA256 = '3316d1a8adece1e27e529a51531713a4cb173be22039100124853321daa66b18'
spec = importlib.util.spec_from_file_location('task1_fixture', HERE.parent / 'task1_core' / 'analysis.py')
task1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task1)
# Reuse the unchanged Task-1 fixture's classification, mapping, and diagnostics mechanics.
TENORS, STATES, CASES, MIXED = task1.TENORS, task1.STATES, task1.CASES, task1.MIXED
OPPOSING = [CASES[2], CASES[6]]
# Explicit endpoint/reference lags of M5, exactly as specified by Task 2.
VARIANTS = {'A': (0, 126), 'B': (0, 63), 'C': (21, 147), 'D': (21, 84)}
EVENTS = [('1987 reversal', '1987-08-01', '1987-10-31'),
          ('2008 GFC', '2008-09-01', '2008-12-31'),
          ('2020 COVID', '2020-02-01', '2020-03-31'),
          ('2022 relief', '2022-06-01', '2022-08-31'),
          ('2023 long-end selloff', '2023-07-01', '2023-10-31')]
REVERSALS = [('10Y', '1980-07-09', '1980-10-14', 68),
             ('30Y', '1980-07-21', '1980-10-14', 60)]
FIELDS = ['as_of', 'representative_tenor', 'duration_exposure', 'segment',
          'observation_index', 'recent_move_bp', 'recent_move_state']
for variant in VARIANTS:
    FIELDS += [f'{variant}_{field}' for field in ('trend_bp', 'trend_state', 'rule_case', 'core_candidates')]
    if variant != 'A':
        FIELDS += [f'{variant}_case_changed', f'{variant}_core_changed']


def calculate_segment(source, ti):
    """Accepted observations -> M5 features -> variants -> local Core candidates."""
    yields = [Decimal(r['yield_pct']) * 100 for r in source]
    m5 = [None] * len(source)
    result = []
    for t, item in enumerate(source):
        r = {'as_of': item['as_of'], 'representative_tenor': TENORS[ti][1],
             'duration_exposure': TENORS[ti][2], 'segment': int(item['segment']),
             'observation_index': t}
        if t >= 4:
            m5[t] = sum(yields[t-4:t+1]) / 5
        if t >= 25:
            recent = m5[t] - m5[t-21]
            r.update(recent_move_bp=recent, recent_move_state=task1.state(recent, 10))
        for v, (endpoint, reference) in VARIANTS.items():
            if t < reference + 4:
                continue
            trend = m5[t-endpoint] - m5[t-reference]
            state = task1.state(trend, 25)
            case = f"{state} × {r['recent_move_state']}"
            r.update({f'{v}_trend_bp': trend, f'{v}_trend_state': state, f'{v}_rule_case': case,
                      f'{v}_core_candidates': json.dumps(task1.RULES[CASES.index(case)][ti], separators=(',', ':'))})
            if v != 'A' and 'A_rule_case' in r:
                r[f'{v}_case_changed'] = int(case != r['A_rule_case'])
                r[f'{v}_core_changed'] = int(r[f'{v}_core_candidates'] != r['A_core_candidates'])
        result.append(r)
    return result


def load_and_validate(path):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError(f'Task-1 snapshot hash mismatch: {digest}')
    with path.open() as f:
        snapshot = list(csv.DictReader(f))
    all_rows, baseline = [], Counter()
    exclusions = Counter((r['representative_tenor'], r['availability']) for r in snapshot)
    for ti, (series, tenor, exposure) in enumerate(TENORS):
        raw = [r for r in snapshot if r['representative_tenor'] == tenor]
        accepted = [r for r in raw if r['availability'] in ('available', 'insufficient_130_observation_history')]
        assert all(r['series_id'] == series and r['duration_exposure'] == exposure for r in raw)
        assert all(not (series == 'DGS30' and '2002-02-18' <= r['as_of'] < '2006-02-09') for r in accepted)
        assert len({r['as_of'] for r in raw}) == len(raw)
        assert [r['as_of'] for r in raw] == sorted(r['as_of'] for r in raw)
        for seg, group in itertools.groupby(accepted, key=lambda r: r['segment']):
            source = list(group)
            assert [int(r['observation_index']) for r in source] == list(range(len(source)))
            assert all((date.fromisoformat(b['as_of'])-date.fromisoformat(a['as_of'])).days <= 7 for a, b in zip(source, source[1:]))
            computed = calculate_segment(source, ti)
            for original, r in zip(source, computed):
                if original['availability'] == 'available':
                    for field in ('trend_bp', 'trend_state', 'recent_move_bp', 'recent_move_state', 'rule_case', 'core_candidates'):
                        actual = r[field if field.startswith('recent') else f'A_{field}']
                        expected = Decimal(original[field]) if field.endswith('_bp') else original[field]
                        if actual != expected:
                            raise ValueError(f'Baseline mismatch {tenor} {r["as_of"]} {field}: {actual} != {expected}')
                    baseline[tenor] += 1
                else:
                    assert 'A_trend_bp' not in r
            # Independent exact-rational recomputation checks every available variant,
            # including coverage outside the primary common sample.
            for v, (end, ref) in VARIANTS.items():
                for t in range(ref+4, len(source)):
                    ep = sum(Fraction(source[k]['yield_pct']) for k in range(t-end-4, t-end+1)) / 5
                    rp = sum(Fraction(source[k]['yield_pct']) for k in range(t-ref-4, t-ref+1)) / 5
                    assert Fraction(computed[t][f'{v}_trend_bp']) == (ep-rp)*100
            # Truncation at fixed observation indices cannot change earlier results.
            for stop in (152, 300, len(source)//2):
                assert calculate_segment(source[:stop], ti) == computed[:stop]
            all_rows.extend(computed)
    assert sum(baseline.values()) == 38330
    # Exact boundary checks and identities for the shifted comparisons.
    for threshold in (10, 25):
        for value, expected in [(-threshold, 'Stable'), (threshold, 'Stable'),
                                (Decimal(-threshold)-Decimal('.2'), 'Falling'),
                                (Decimal(threshold)+Decimal('.2'), 'Rising')]:
            assert task1.state(value, threshold) == expected
    for (_, _), group in itertools.groupby(all_rows, key=lambda r: (r['representative_tenor'], r['segment'])):
        g = list(group)
        for t, r in enumerate(g):
            if 'C_trend_bp' in r:
                assert r['C_trend_bp'] == g[t-21]['A_trend_bp']
                assert r['C_trend_state'] == g[t-21]['A_trend_state']
            if 'D_trend_bp' in r:
                assert r['D_trend_bp'] == g[t-21]['B_trend_bp']
                assert r['D_trend_state'] == g[t-21]['B_trend_state']
    return snapshot, all_rows, baseline, exclusions


def quantile(values, p):
    return sorted(values)[max(0, math.ceil(p*len(values))-1)] if values else 0


def runs(rows, field):
    # Input retains all eligible dates; never filter to a selected case before grouping.
    return task1.episodes(rows, field)


def compact_path(rows, field):
    return '; '.join(f"{e['start'][5:]} {e['key']}" for e in runs(rows, field)) + f"; end {rows[-1]['as_of'][5:]} {rows[-1][field]}"


def evidence(snapshot, all_rows, common, baseline, exclusions):
    out = []
    add = out.append
    table, pct = task1.table, task1.pct
    add('<!-- coverage -->\n## Coverage and baseline\n')
    add(f'Input SHA-256 verified: `{SHA256}`. Baseline exact matches: {sum(baseline.values())}; all six requested fields match on every Task-1 complete row.\n')
    data = []
    for _, tenor, _ in TENORS:
        rr = [r for r in all_rows if r['representative_tenor'] == tenor]
        cc = [r for r in common if r['representative_tenor'] == tenor]
        for v in VARIANTS:
            vv = [r for r in rr if f'{v}_trend_bp' in r]
            segments = [' – '.join([g[0]['as_of'], g[-1]['as_of']]) for _, group in itertools.groupby(vv, key=lambda r: r['segment']) if (g := list(group))]
            data.append([tenor, v, len(vv), len(rr)-len(vv), '; '.join(segments), len(cc), len(vv)-len(cc)])
    add(table(['Tenor', 'Variant', 'Individual n', 'Warmup exclusions', 'Individual eligible segments', 'Common n', 'Individual outside common'], data))
    add(table(['Tenor', 'Baseline matched', 'Raw missing rows', 'Structural-gap rows', 'Task-1 warmup', 'Task-2 common exclusions from accepted'],
              [[t, baseline[t], exclusions[t, 'no_source_observation'], exclusions[t, 'documented_structural_gap'],
                exclusions[t, 'insufficient_130_observation_history'],
                sum(r['representative_tenor']==t for r in all_rows)-sum(r['representative_tenor']==t for r in common)] for _, t, _ in TENORS]))
    add('<!-- trends -->\n## Common-sample Trend behavior\n')
    overview, perstate, relationship, impact, cross, mixed, longest = [], [], [], [], [], [], []
    for _, tenor, _ in TENORS:
        cc = [r for r in common if r['representative_tenor'] == tenor]
        adjacent = [(a,b) for a,b in zip(cc,cc[1:]) if a['segment']==b['segment']]
        for v in VARIANTS:
            field = f'{v}_trend_state'
            eps = runs(cc, field)
            durations = [e['n'] for e in eps]
            transitions = sum(a[field]!=b[field] for a,b in adjacent)
            # Short A-B-A runs diagnose local reversals, not statistical independence.
            return_runs = sum(a['key']==c['key'] and b['n']<=5 and
                              a['rows'][0]['segment']==c['rows'][0]['segment']
                              for a,b,c in zip(eps,eps[1:],eps[2:]))
            overview.append([tenor,v,len(eps),f'{mean(durations):.2f}',median(durations),quantile(durations,.9),max(durations),pct(transitions,len(adjacent)),return_runs])
            for st in STATES:
                ds = [e['n'] for e in eps if e['key']==st]
                perstate.append([tenor,v,st,pct(sum(r[field]==st for r in cc),len(cc)),len(ds),f'{mean(ds):.2f}',median(ds),quantile(ds,.9),max(ds)])
            counts = Counter(r[f'{v}_rule_case'] for r in cc)
            relationship.append([tenor,v,pct(sum(r[field]==r['recent_move_state'] for r in cc),len(cc)),
                                 pct(sum(counts[c] for c in OPPOSING),len(cc)),pct(sum(counts[c] for c in MIXED),len(cc))])
            impact.append([tenor,v,pct(sum(r[f'{v}_rule_case']!=r['A_rule_case'] for r in cc),len(cc)),
                           pct(sum(r[f'{v}_core_candidates']!=r['A_core_candidates'] for r in cc),len(cc))])
            for case in MIXED:
                ee = [e for e in runs(cc,f'{v}_rule_case') if e['key']==case]
                ds = [e['n'] for e in ee]
                mixed.append([tenor,v,case,len(ee),sum(ds),median(ds),quantile(ds,.75),quantile(ds,.9),max(ds),sum(n>=21 for n in ds),sum(n>=42 for n in ds),sum(n>=63 for n in ds)])
                if case in OPPOSING:
                    e = max(ee,key=lambda e:e['n'])
                    longest.append([tenor,v,case,e['start'],e['end'],e['n'],task1.extent(e['rows'],f'{v}_trend_bp'),task1.extent(e['rows'],'recent_move_bp')])
        # Fixed Recent Move benchmark on the identical common sample.
        eps = runs(cc,'recent_move_state'); ds=[e['n'] for e in eps]
        transitions=sum(a['recent_move_state']!=b['recent_move_state'] for a,b in adjacent)
        overview.append([tenor,'Recent',len(eps),f'{mean(ds):.2f}',median(ds),quantile(ds,.9),max(ds),pct(transitions,len(adjacent)),'—'])
        for case in CASES:
            cross.append([tenor,case]+[pct(sum(r[f'{v}_rule_case']==case for r in cc),len(cc)) for v in VARIANTS])
    add(table(['Tenor','Variant','Episodes','Mean n','Median n','P90 n','Max n','Transitions / eligible pairs','Return runs ≤5'],overview))
    add('<!-- perstate -->\n### State-specific persistence\n')
    add(table(['Tenor','Variant','State','Frequency','Episodes','Mean n','Median n','P90 n','Max n'],perstate))
    add('<!-- relationship -->\n## Relationship with fixed Recent Move\n')
    add(table(['Tenor','Variant','Exact State agreement','Opposing direction','All four mixed cases'],relationship))
    add('<!-- crosstab -->\n### Complete Trend × Recent cross-tab\n')
    add(table(['Tenor','Rule Case','A','B','C','D'],cross))
    add('<!-- impact -->\n## Core and cross-tenor impact\n')
    add(table(['Tenor','Variant','Rule Case changes vs A','Candidate-set changes vs A'],impact))
    dates = defaultdict(dict)
    for r in common:
        dates[r['as_of']][r['representative_tenor']]=r
    shared = {d:rs for d,rs in dates.items() if len(rs)==3}
    add(f"All-tenor common dates: {len(shared)}, outer range {min(shared)} – {max(shared)}; excludes the 30Y gap and all variant warmups.\n")
    add(table(['Variant','One common case','Exactly two cases','Three distinct cases','Any disagreement'],
              [[v]+[pct(sum(len({r[f'{v}_rule_case'] for r in rs.values()})==n for rs in shared.values()),len(shared)) for n in (1,2,3)]+
               [pct(sum(len({r[f'{v}_rule_case'] for r in rs.values()})>1 for rs in shared.values()),len(shared))] for v in VARIANTS]))
    add('<!-- mixed -->\n## Mixed-episode distributions\n')
    add(table(['Tenor','Variant','Case','Episodes','Obs','Median','P75','P90','Max','≥21','≥42','≥63'],mixed))
    add('<!-- longest -->\n### Longest opposing-direction episodes\n')
    add(table(['Tenor','Variant','Case','Start','End','n','Trend bp range','Recent bp range'],longest))
    add('<!-- reversal -->\n## Required 1980 reversal diagnostic\n')
    for tenor,start,end,expected_n in REVERSALS:
        rr = [r for r in common if r['representative_tenor']==tenor and '1980-06-01'<=r['as_of']<='1980-11-30']
        original = [r for r in rr if start<=r['as_of']<=end]
        assert len(original)==expected_n and all(r['A_rule_case']==OPPOSING[0] for r in original)
        add(f'### {tenor}: Task-1 episode {start} – {end}, {expected_n} observations\n')
        add(table(['Series','State path (dates in 1980)'],[['Recent',compact_path(rr,'recent_move_state')]]+
                  [[v,compact_path(rr,f'{v}_trend_state')] for v in VARIANTS]))
        transition_rows=[]
        for v in VARIANTS:
            after=[r for r in rr if r['as_of']>=start]
            left=next((r for r in after if r[f'{v}_trend_state']!='Falling'),None)
            rising=next((r for r in after if r[f'{v}_trend_state']=='Rising'),None)
            transition_rows.append([v,after[0][f'{v}_trend_state'],left['as_of'] if left else 'not in extension',
                                    left[f'{v}_trend_state'] if left else '—',rising['as_of'] if rising else 'not in extension',
                                    task1.extent(original,f'{v}_trend_bp')])
        add(table(['Variant','At episode start','First non-Falling on/after start','Exit State','First Rising on/after start','Trend bp over original episode'],transition_rows))
        add(table(['Variant','Rule Case path, fixed June–November context'],[[v,compact_path(rr,f'{v}_rule_case')] for v in VARIANTS]))
        # Numerical context chosen by original boundaries and first B/A exits, not returns.
        chosen={start,end}
        for v in ('A','B'):
            for st in ('Stable','Rising'):
                first=next((r for r in rr if r['as_of']>=start and r[f'{v}_trend_state']==st),None)
                if first: chosen.add(first['as_of'])
        add(table(['as_of','Recent bp','A bp','B bp','C bp','D bp'],
                  [[r['as_of'],r['recent_move_bp']]+[r[f'{v}_trend_bp'] for v in VARIANTS] for r in rr if r['as_of'] in chosen]))
    add('<!-- events -->\n## Required historical transition windows\n')
    for name,start,end in EVENTS:
        add(f'### {name}: {start} – {end}\n')
        paths, conflicts, endpoints=[] ,[], []
        for _,tenor,_ in TENORS:
            rr=[r for r in common if r['representative_tenor']==tenor and start<=r['as_of']<=end]
            paths.append([tenor,'Recent',compact_path(rr,'recent_move_state')])
            for v in VARIANTS:
                paths.append([tenor,v,compact_path(rr,f'{v}_trend_state')])
                ee=[e for e in runs(rr,f'{v}_rule_case') if e['key'] in OPPOSING]
                conflicts.append([tenor,v,'; '.join(f"{e['start'][5:]}–{e['end'][5:]} {e['key']} ({e['n']})" for e in ee) or 'None'])
            for r in (rr[0],rr[-1]):
                endpoints.append([tenor,r['as_of'],r['recent_move_bp']]+[r[f'{v}_trend_bp'] for v in VARIANTS])
        add(table(['Tenor','Series','State path (first state, then every transition; explicit final state)'],paths))
        add(table(['Tenor','Variant','Opposing intervals (event-clipped; observation counts)'],conflicts))
        add(table(['Tenor','as_of','Recent bp','A bp','B bp','C bp','D bp'],endpoints))
    add('<!-- robustness -->\n## Mixed-cell occupancy and membership\n')
    tracked=[('6M',c) for c in MIXED]+[('30Y',c) for c in MIXED]
    cells=[]
    for tenor,case in tracked:
        rr=[r for r in common if r['representative_tenor']==tenor]
        dates_a={r['as_of'] for r in rr if r['A_rule_case']==case}
        row=[tenor,case]
        for v in VARIANTS:
            selected=[r for r in rr if r[f'{v}_rule_case']==case]
            overlap=sum(r['as_of'] in dates_a for r in selected)
            row.append(f'{len(selected)} ({overlap} also A)')
        cells.append(row)
    add(table(['Tenor','Case','A observations','B observations','C observations','D observations'],cells))
    # Revisit every selected Task-1 mixed episode, not just convenient examples.
    add('<!-- task1episodes -->\n### Task-1 selected mixed episodes under all variants\n')
    selected_rows=[]
    for tenor,case in tracked:
        rr=[r for r in all_rows if r['representative_tenor']==tenor and 'A_rule_case' in r]
        ee=[e for e in runs(rr,'A_rule_case') if e['key']==case]
        ds=[e['n'] for e in ee]
        typical_mag=median(median(abs(r['recent_move_bp']) for r in e['rows']) for e in ee)
        selections=[('longest',max(ee,key=lambda e:e['n'])),
                    ('largest Recent',max(ee,key=lambda e:max(abs(r['recent_move_bp']) for r in e['rows']))),
                    ('typical',min(ee,key=lambda e:(abs(e['n']-median(ds)),abs(median(abs(r['recent_move_bp']) for r in e['rows'])-typical_mag),e['start'])))]
        for role,e in selections:
            selected_rows.append([tenor,case,role,f"{e['start']} – {e['end']} ({e['n']})"]+
                                 ['; '.join(f'{c}: {n}' for c,n in Counter(r[f'{v}_rule_case'] for r in e['rows']).items()) for v in VARIANTS])
    add(table(['Tenor','A case','Selection','Original interval','A cases/counts','B cases/counts','C cases/counts','D cases/counts'],selected_rows))
    add('<!-- boundary -->\n## Short-lived B State returns inside the specified event windows\n')
    returns=[]
    for name,start,end in EVENTS:
        for _,tenor,_ in TENORS:
            rr=[r for r in common if r['representative_tenor']==tenor and start<=r['as_of']<=end]
            ee=runs(rr,'B_trend_state')
            for a,b,c in zip(ee,ee[1:],ee[2:]):
                if a['key']==c['key'] and b['n']<=5:
                    returns.append([name,tenor,b['start'],b['end'],b['n'],
                                    f"{a['key']} → {b['key']} → {c['key']}",
                                    task1.extent(b['rows'],'B_trend_bp'),
                                    task1.extent(b['rows'],'recent_move_bp')])
    add(table(['Event','Tenor','Start','End','n','B State return','B bp range','Recent bp range'],returns))
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=SNAPSHOT)
    parser.add_argument('--output',type=Path,default=HERE/'comparison.csv')
    parser.add_argument('--diagnostics',type=Path,default=Path('/tmp/duration_task2_diagnostics.md'))
    args=parser.parse_args()
    if args.output.resolve()==args.input.resolve() or args.diagnostics.resolve()==args.input.resolve():
        raise ValueError('Output must not overwrite the frozen input')
    snapshot,all_rows,baseline,exclusions=load_and_validate(args.input)
    common=[r for r in all_rows if all(f'{v}_trend_bp' in r for v in VARIANTS)]
    with args.output.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n')
        writer.writeheader(); writer.writerows(common)
    args.diagnostics.write_text(evidence(snapshot,all_rows,common,baseline,exclusions))
    print(json.dumps({'input_sha256':SHA256,'baseline_matches':dict(baseline),
                      'baseline_total':sum(baseline.values()),'common_rows':len(common),
                      'comparison_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'exact_fraction_windows_thresholds_shift_identity_prefix_checks':'passed'},indent=2))


if __name__=='__main__':
    main()
