"""Write rows.json (the Panel sheet as header list + row lists) for the figure scripts.
Usage: python make_rows_json.py ../../data/state_school_policy_panel_v1.0.xlsx
"""
import sys, json, datetime, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
ws = wb['Panel']
rows = list(ws.iter_rows(values_only=True))
H = [h for h in rows[0] if h]
n = len(H)
def cell(v):
    if v is None: return None
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime('%Y-%m-%d')
    return v if isinstance(v, (int, float)) else str(v)
data = [[cell(v) for v in r[:n]] for r in rows[1:] if r[0]]
json.dump({'H': H, 'data': data}, open('rows.json', 'w'))
print('rows.json:', len(data), 'rows')
