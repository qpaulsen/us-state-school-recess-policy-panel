"""Write state_school_year_panel.csv: one row per jurisdiction, school year and topic with the strongest
K-12 instrument in force (0 none, 1 recommendation, 2 mandate, 3 mandate coded outdoor_if_feasible).
Derivation as in figures/panel.py (time_dose and structural_recess rows; Pre-K rows excluded;
left-censored rows in force from 2000-2001; rows without a usable start date omitted).
Usage: python make_state_year_panel.py state_school_policy_panel_v1.0.xlsx out.csv
"""
import sys, csv, json, subprocess, os, openpyxl
here = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
subprocess.run([sys.executable, os.path.join(here, 'figures', 'make_rows_json.py'), os.path.abspath(src)], check=True, cwd=os.path.join(here, 'figures'))
subprocess.run([sys.executable, 'panel.py'], check=True, cwd=os.path.join(here, 'figures'), stdout=subprocess.DEVNULL)
P = json.load(open(os.path.join(here, 'figures', 'panel.json')))
wb = openpyxl.load_workbook(src, read_only=True, data_only=True); ws = wb['Panel']
rows = list(ws.iter_rows(values_only=True)); H = [h for h in rows[0] if h]; ci = {h: i for i, h in enumerate(H)}
fips = {r[ci['state']]: r[ci['state_fips']] for r in rows[1:] if r[0]}
LAB = {0: 'none', 1: 'recommendation', 2: 'mandate', 3: 'mandate_outdoor_if_feasible'}
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['jurisdiction_name', 'state_fips', 'school_year', 'topic', 'status_code', 'status'])
    for s in P['states']:
        for i, y in enumerate(P['years']):
            for t in ('recess', 'daily_PA_minutes'):
                v = P['res'][t][s][i]; w.writerow([s, fips[s], f'{y}-{y+1}', t, v, LAB[v]])
print('wrote', out)
