#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os, os.path
import pathlib


# Counties ↔ Congressional District correspondences

DATA_ROOT = 'data/daily-kos/'


XLSX_CONGRESSIONAL = "Counties ↔ congressional district correspondences.xlsx"
XLSX_STATE = "Counties ↔ legislative district correspondences.xlsx"

CORRESPONDENCES = [
    # (file, columns, output)
    (XLSX_CONGRESSIONAL, 'A:D', 'counties-to-congressional-districts/%s.csv'),
    (XLSX_CONGRESSIONAL, 'F:I', 'congressional-districts-to-counties/%s.csv'),
    (XLSX_STATE, 'A:D', 'counties-to-state-senate-districts/%s.csv'),
    (XLSX_STATE, 'F:I', 'state-senate-districts-to-counties/%s.csv'),
    (XLSX_STATE, 'K:N', 'counties-to-state-house-districts/%s.csv'),
    (XLSX_STATE, 'P:S', 'state-house-districts-to-counties/%s.csv'),
]

for xlsx_path, xlsx_cols, output_format in CORRESPONDENCES:
    input_path = os.path.join(os.getcwd(), DATA_ROOT, xlsx_path)
    output_path = os.path.join(os.getcwd(), DATA_ROOT, output_format)
    df = pd.read_excel(
        input_path,
        sheet_name=None,
        skiprows=1,
        usecols=xlsx_cols)

    # Setup output directories
    path = pathlib.Path(output_path % "foo")
    path.parent.mkdir(parents=True, exist_ok=True)

    for sheet_name, sheet_content in df.items():
        # drop blank rows
        sheet_content.replace('', float('nan'), inplace=True)
        sheet_content.dropna(how='any', inplace=True)

        # Write
        sheet_content.to_csv(output_path % sheet_name)
