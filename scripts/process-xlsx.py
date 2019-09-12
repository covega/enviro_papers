#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pathlib


# Counties ↔ Congressional District correspondences

XLSX_SOURCE_PATH = "data/daily-kos/Counties ↔ congressional district correspondences.xlsx"

C_TO_D_PATH = 'data/daily-kos/counties-to-congressional-districts/%s.csv'
C_TO_D_COLS = 'A:D'
D_TO_C_PATH = 'data/daily-kos/congressional-districts-to-counties/%s.csv'
D_TO_C_COLS = 'F:I'

CORRESPONDENCES = [
    (C_TO_D_PATH, C_TO_D_COLS),
    (D_TO_C_PATH, D_TO_C_COLS),
]

for output_path, xlsx_cols in CORRESPONDENCES:
    df = pd.read_excel(
        XLSX_SOURCE_PATH,
        sheet_name=None,
        skiprows=1,
        usecols=xlsx_cols)

    # Setup output directories
    path = pathlib.Path(output_path % "foo")
    path.parent.mkdir(parents=True, exist_ok=True)

    for sheet_name, sheet_content in df.items():
        sheet_content.to_csv(output_path % sheet_name)
