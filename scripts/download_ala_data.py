#!/usr/bin/env python
# coding: utf-8

import yaml
import os, os.path
import requests
import pandas as pd
from app.util import StateAbbrLookup

ASTHMA_YAML_PATH = os.path.join(os.getcwd(), 'data/raw/asthma.yaml')
ASTHMA_CSV_PATH = os.path.join(os.getcwd(), 'data/cleaned/asthma/all.csv')
lookup = StateAbbrLookup()

def download_ala_data():
    df = None
    with open(ASTHMA_YAML_PATH, 'r') as in_file:
        all_states = yaml.safe_load(in_file)
        for idx, state_info in enumerate(all_states):
            state_abbr = lookup.get_abbr(state_info['state'])
            resp = requests.get(state_info['jsonUrl'])
            print("Reading %s (%d/%d)" % (state_abbr, idx+1, len(all_states)), end='\r')

            if not resp.ok:
                print("Bad resp: ", resp.error)

            asthma_json = resp.json()

            if df is None:
                # First time, initialize with columns
                keys = [pop['name']
                        for pop in asthma_json[0]['FormattedPopulations']]
                columns = ['State', 'County']
                columns.extend(keys)
                df = pd.DataFrame(columns=columns)

            for county in asthma_json:
                row = dict([(pop['name'], pop['val'])
                           for pop in county['FormattedPopulations']])
                row['State'] = state_abbr
                row['County'] = county['properCountyName']
                df = df.append(row, ignore_index=True)

    print()
    print("Downloaded.")
    df.to_csv(ASTHMA_CSV_PATH)


if __name__ == '__main__':
    download_ala_data()
