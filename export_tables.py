"""Export the deposit workbook sheets to UTF-8 CSV files.

Usage: python export_tables.py state_school_policy_panel_v1.0.xlsx out_dir
Dates are already stored as YYYY-MM-DD text in the workbook; nothing is reformatted.
"""
import csv, sys, datetime
from pathlib import Path
import openpyxl

SHEETS = {  # sheet name: (csv name, number of columns to keep)
    'Panel': ('panel.csv', None),
    'AUDIT_LOG': ('audit_log.csv', None),
    'AUDIT_CANDIDATES': ('audit_candidates.csv', None),
    'Codebook': ('data_dictionary.csv', 3),
    'Codebook_v1-1_Amendments': ('codebook_rules_v1-1_amendments.csv', 2),
    'Codebook_v1-2_Amendments': ('codebook_rules_v1-2_amendments.csv', 2),
    'Codebook_v1-3_Amendments': ('codebook_rules_v1-3_amendments.csv', 2),
    'Codebook_v1-4_Amendments': ('codebook_rules_v1-4_amendments.csv', 2),
    'ADJUDICATION_NOTES': ('adjudication_notes.csv', 1),
}

def cell(v):
    if v is None:
        return ''
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime('%Y-%m-%d')
    return v

def main(src, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(src, data_only=True)
    for sheet, (name, ncols) in SHEETS.items():
        ws = wb[sheet]
        rows = list(ws.iter_rows(values_only=True))
        n = ncols or (max(i for i, h in enumerate(rows[0]) if h) + 1)
        written = 0
        with open(out / name, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            for r in rows:
                r = list(r[:n])
                if not any(v not in (None, '') for v in r):
                    continue
                w.writerow([cell(v) for v in r]); written += 1
        print(f'{name}: {written} rows')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
