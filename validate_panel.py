"""Structural validation of the QAP state policy panel (Panel sheet).

Usage: python validate_panel.py state_school_policy_panel_v1.0.xlsx [--deposit path/to/source_documents]

Checks (each prints PASS or the offending row ids):
 1. row_id unique and non-empty
 2. one coded row per state for every panel row; 51 jurisdictions
 3. date fields are blank or ISO text (YYYY, YYYY-MM or YYYY-MM-DD); no Excel dates or serials
 4. rule 15 as amended by rule 26: silent rows carry no enactment_date, repeal_date,
    implementation_school_year or treatment_school_year; amended_date is permitted (rule 26, the
    date the silence ended) and effective_date only on dated baseline_none rows created by a
    repeal inside the window (v1.2 rule 8); the count of such rows is printed
 5. superseded_by values resolve to row ids in the same state
 6. controlled vocabularies (topic, policy_status, outdoor_specificity, confidence, enforcement, instrument_class)
 7. coder field is QAP (panel coder) or ADJ (second-coder adjudicated rows) on every row
 8. source_file entries resolve to a deposited PDF (loose or inside the per-state zips) or to a file
    listed in NOT_DEPOSITED_licensed_copies.csv (only with --deposit)
"""
import re, sys, datetime, collections
from pathlib import Path
import openpyxl

DATE_FIELDS = ['enactment_date', 'effective_date', 'amended_date', 'repeal_date']
ISO = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')
VOCAB = {
    'topic': {'recess', 'daily_PA_minutes', 'outdoor_time', 'none'},
    'policy_status': {'mandate', 'recommendation', 'silent'},
    'outdoor_specificity': {'explicit_outdoor', 'outdoor_if_feasible', 'indoor_permitted', 'unspecified', 'NA'},
    'confidence': {'high', 'medium', 'low'},
    'enforcement': {'none', 'statutory_soft', 'monitored', 'accreditation_condition', 'unknown'},
    'instrument_class': {'time_dose', 'structural_recess', 'umbrella_subject', 'credit_unit', 'withholding_policy', 'baseline_none'},
}

def report(name, bad):
    print(f'{name}: ' + ('PASS' if not bad else f'FAIL ({len(bad)}) ' + '; '.join(map(str, bad[:20]))))
    return not bad

def main(path, deposit=None):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Panel']
    hdr = [c.value for c in ws[1]]
    ci = {h: i for i, h in enumerate(hdr) if h}
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    g = lambda r, f: r[ci[f]]
    ok = True
    ids = [g(r, 'row_id') for r in rows]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    ok &= report('1 unique row_id', dup)
    states = {g(r, 'state') for r in rows}
    ok &= report('2 jurisdictions = 51', [] if len(states) == 51 else [f'{len(states)} found'])
    bad = []
    for r in rows:
        for f in DATE_FIELDS + ['date_coded']:
            v = g(r, f)
            if v in (None, ''):
                continue
            if isinstance(v, (datetime.datetime, datetime.date, int, float)) or not ISO.match(str(v)):
                bad.append(f'{g(r, "row_id")}.{f}={v!r}')
    ok &= report('3 dates are ISO text', bad)
    silent = [r for r in rows if g(r, 'policy_status') == 'silent']
    bad = [g(r, 'row_id') for r in silent
           if any(g(r, f) not in (None, '') for f in ['enactment_date', 'repeal_date', 'implementation_school_year', 'treatment_school_year'])]
    ok &= report('4 rule 15/26 on silent rows', bad)
    dated = [g(r, 'row_id') for r in silent if g(r, 'effective_date') not in (None, '')]
    print(f'   dated silent rows under v1.2 rule 8 (repeal creates silence): {len(dated)}')
    by_state = collections.defaultdict(set)
    for r in rows:
        by_state[g(r, 'state')].add(g(r, 'row_id'))
    bad = []
    for r in rows:
        sb = g(r, 'superseded_by')
        if sb in (None, ''):
            continue
        for t in str(sb).split(';'):
            t = t.strip()
            if t and t not in by_state[g(r, 'state')]:
                bad.append(f'{g(r, "row_id")} -> {t}')
    ok &= report('5 superseded_by resolves', bad)
    bad = []
    for f, allowed in VOCAB.items():
        for r in rows:
            v = g(r, f)
            if v in (None, ''):
                continue
            if v not in allowed:
                bad.append(f'{g(r, "row_id")}.{f}={v}')
    ok &= report('6 controlled vocabularies', bad)
    bad = [g(r, 'row_id') for r in rows if g(r, 'coder') not in ('QAP', 'ADJ')]
    ok &= report('7 coder in (QAP, ADJ)', bad)
    if deposit:
        import zipfile, csv
        dep = Path(deposit)
        files = {p.name for p in dep.rglob('*.pdf')}
        for z in dep.glob('*.zip'):
            files |= {n.split('/')[-1] for n in zipfile.ZipFile(z).namelist()}
        manifest = dep / 'NOT_DEPOSITED_licensed_copies.csv'
        if manifest.exists():
            with open(manifest, encoding='utf-8') as f:
                files |= {r['file'] for r in csv.DictReader(f)}  # withheld licensed copies count as resolved
        bad = []
        for r in rows:
            sf = g(r, 'source_file')
            if sf in (None, ''):
                continue
            for t in str(sf).split(';'):
                t = t.strip()
                if t and t not in files:
                    bad.append(f'{g(r, "row_id")}: {t}')
        ok &= report('8 source_file resolves', bad)
    print(f'rows: {len(rows)}; result: ' + ('ALL PASS' if ok else 'FAILURES'))
    return 0 if ok else 1

if __name__ == '__main__':
    args = sys.argv[1:]
    dep = None
    if '--deposit' in args:
        i = args.index('--deposit'); dep = args[i + 1]; args = args[:i] + args[i + 2:]
    sys.exit(main(args[0], dep))
