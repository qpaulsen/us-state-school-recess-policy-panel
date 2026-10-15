# Code for the state school recess, physical activity, and outdoor time policy dataset (v1.0)

Data: https://doi.org/10.5281/zenodo.23383730 (Zenodo, dataset v1.0, CC BY 4.0). Code license: MIT.

Cite as: Paulsen, Q. A. & Ludwig, C. A. State policies on school recess, physical activity, and outdoor time in the United States, 2000-2025. Zenodo https://doi.org/10.5281/zenodo.23383730 (2026).

Python 3.10 or later. Install dependencies with `pip install -r requirements.txt`.
All scripts take the deposit workbook `data/state_school_policy_panel_v1.0.xlsx` as input; none writes to it.

## Validation and exports (run from `code/`)

| Script | Purpose | Command |
|---|---|---|
| `validate_panel.py` | Structural checks on the Panel sheet: unique row ids, 51 jurisdictions, ISO text dates, rule 15/26 on silent rows, superseded_by resolution, controlled vocabularies, coder field, and (with `--deposit`) that every `source_file` entry resolves to a deposited PDF | `python validate_panel.py ../data/state_school_policy_panel_v1.0.xlsx --deposit ../source_documents` |
| `export_tables.py` | Writes the CSV copies of every sheet in `data/` | `python export_tables.py ../data/state_school_policy_panel_v1.0.xlsx ../data` |
| `summary_statistics.py` | Regenerates `data/summary_statistics_v1.0.xlsx` (static counts: univariate tables, cross-tabs, date coverage, rows per jurisdiction, outdoor rows) | `python summary_statistics.py ../data/state_school_policy_panel_v1.0.xlsx ../data/summary_statistics_v1.0.xlsx` |

| `make_state_year_panel.py` | Writes `data/state_school_year_panel.csv`: one row per jurisdiction, school year and topic with the strongest K-12 instrument in force (0 none, 1 recommendation, 2 mandate, 3 mandate coded outdoor_if_feasible), derived as in `figures/panel.py` | `python make_state_year_panel.py ../data/state_school_policy_panel_v1.0.xlsx ../data/state_school_year_panel.csv` |
| `build_source_documents.py` | Builds `source_documents/<State_XX>.zip` from the working deposit folder, skipping the licensed copies listed in `NOT_DEPOSITED_licensed_copies.csv`, `_originals` captures and non-PDF files | `python build_source_documents.py /path/to/final_pdf_deposit ../source_documents` |

| `format_workbooks.py` | Applies the deposit house style (Arial 9 pt, navy header row, frozen header and filters on tabular sheets); run last | `python format_workbooks.py ../data/state_school_policy_panel_v1.0.xlsx ../data/summary_statistics_v1.0.xlsx` |

Expected output of `validate_panel.py` on v1.0: all eight checks PASS, 550 rows, 9 dated silent rows under v1.2 rule 8.

## Reliability (`reliability/`)

`round1/`: calibration round (Alabama, Alaska, Arizona, Arkansas; kappa computed on AK, AZ, AR). `compare_kappa_v2_asrun.py` computes instrument detection (Jaccard), field-level Cohen's kappa and exact agreement between the two independent codings, pairing rows through `pair_map.csv`. Inputs beside the script: `QAP_coder_file_asrun.xlsx` (coder QAP) and `CoderB_CL_four_states.xlsx` (coder CL). `kappa_report_FINAL_2026-07-23.txt` is the output as run. Run with `python compare_kappa_v2_asrun.py` from that folder.

`round2/`: production reliability round (Idaho, Indiana, Iowa, Rhode Island, Tennessee, Virginia). `CoderB_CL_round2_six_states.xlsx` is coder CL's file, `pair_map_round2_sensitivity.csv` the row crosswalk, and `kappa_sensitivity_round2.txt` the comparison output against coder QAP's rows for those states as they stood on 2026-08-26 (the same script and procedure as round 1).

## Figures (`figures/`, run from that folder)

1. `python make_rows_json.py ../../data/state_school_policy_panel_v1.0.xlsx` writes `rows.json`.
2. `python panel.py` derives the state-by-school-year status panel (`panel.json`) from the dated rows: treatment starts at `treatment_school_year`, left-censored rows start before 2000, and an interval ends at the school year of `amended_date` or `repeal_date`. Rows without a usable start date are listed as skipped.
3. `python f1_overview.py ../../data/state_school_policy_panel_v1.0.xlsx`, `python f2_datamodel.py`, `python f3_rollout.py states.geojson`, `python f4_validation.py ../../data/state_school_policy_panel_v1.0.xlsx`, `python s1_grid.py` draw Figures 1 to 4 and Supplementary Figure 1 (PDF, PNG and TIFF via `style.save`). `states.geojson` is the US Census Bureau 1:10m cartographic boundary file in the Albers USA projection (from the us-atlas package, `states-albers-10m.json`, converted with topojson-client).
4. `python tables.py` builds Tables 1 and 2; `python combine.py` assembles the figures, legends (`QAP_figure_legends.txt`) and tables into one PDF for review.
   `python si.py` (run in `figures/` after `s1_grid.py`) builds the Supplementary Information PDF (Figure S1 with its legend).

Figure 4a plots the agreement values reported in the Technical Validation text; 4b and 4c are computed from the AUDIT_CANDIDATES sheet.
