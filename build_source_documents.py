"""Build source_documents/<State_XX>.zip from the working deposit folder.

Excludes licensed database copies (source_documents/NOT_DEPOSITED_licensed_copies.csv),
the Background/_originals HTML captures, and any non-PDF file.
Usage: python build_source_documents.py /path/to/final_pdf_deposit ../source_documents [State_XX ...]
"""
import sys, csv, zipfile
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
states = sys.argv[3:] or sorted(p.name for p in src.iterdir() if p.is_dir())
with open(out / 'NOT_DEPOSITED_licensed_copies.csv', encoding='utf-8') as f:
    excluded = {r['file'] for r in csv.DictReader(f)}
for st in states:
    files = sorted(p for p in (src / st).rglob('*.pdf') if '_originals' not in p.parts and p.name not in excluded)
    target = out / f'{st}.zip'
    if target.exists():
        print(f'{st}: exists, skipped'); continue
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for p in files:
            z.write(p, p.relative_to(src).as_posix())
    print(f'{st}: {len(files)} files, {target.stat().st_size/1e6:.1f} MB')
