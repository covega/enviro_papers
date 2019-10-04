#!/usr/bin/env python
# coding: utf-8

import json
import os, os.path

# Pulled from http://assessor.keva.la/cleanenergyprogress/states?states=
INPUT_FILE = os.path.join(os.getcwd(), 'data/raw/jobs/states.json')

# Without useless mapping data
OUTPUT_FILE = os.path.join(os.getcwd(), 'data/raw/jobs/states-cleaned.json')

HTML_URL = "http://assessor.keva.la/cleanenergyprogress/analytics?area_type=%s&area_id=%s"

def clean_energy_job_states():
    states = []
    with open(INPUT_FILE, 'r') as input_file:
        input_data = json.load(input_file)
        for feature in input_data['features']:
            state_data = feature['properties']
            state_data["html_url"] = HTML_URL % (state_data['geography_type'],
                                                 state_data['geoid'])
            states.append(state_data)


    output_data = {
        "states": states
    }

    with open(OUTPUT_FILE, 'w') as output_file:
        json.dump(output_data, output_file)

if __name__ == "__main__":
    preclean_energy_job_states()
