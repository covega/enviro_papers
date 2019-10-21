#!/usr/bin/env python
# coding: utf-8

import os, os.path
import requests
import pandas as pd
import asyncio
from aiohttp import ClientSession

STATES_URL = 'https://api.kevalaanalytics.com/geography/states/'
REGIONS_URL = 'http://assessor.keva.la/cleanenergyprogress/geographies?state=%s&type=%s'
HTML_URL = 'http://assessor.keva.la/cleanenergyprogress/analytics?area_type=%s&area_id=%s'
OUTPUT_CSV = os.path.join(os.getcwd(), 'data/raw/jobs/jobs_metadata.csv')

REGION_TYPES = [
    ('county', 'counties'),
    ('sldu', 'legislativedistrictsupper'),
    ('sldl', 'legislativedistrictslower'),
    ('cd', 'congressionaldistricts')]

async def fetch_region_list(url, session, region_type, state_abbr):
    async with session.get(url) as response:
        resp = await response.json()
        print("Got list [%s, %s]" % (region_type, state_abbr))
        return (resp, region_type, state_abbr)

async def process_states(states_and_geoids):
    fetch_tasks = []
    scrape_tasks = []
    df = pd.DataFrame(columns=['state_abbr', 'region_type', 'geoid', 'name', 'html_url'])

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for state_abbr, state_geoid in states_and_geoids:
            df = df.append({
                'state_abbr': state_abbr,
                'region_type': 'state',
                'geoid': state_geoid,
                'name': None,
                'html_url': HTML_URL % ('state', state_geoid),
            }, ignore_index=True)

            for (region_type_singular, region_type_plural) in REGION_TYPES:
                url = REGIONS_URL % (state_geoid, region_type_plural)
                task = asyncio.ensure_future(
                    fetch_region_list(url, session, region_type_singular, state_abbr))
                fetch_tasks.append(task)

        responses = await asyncio.gather(*fetch_tasks)

        for response_json, region_type, state_abbr in responses:
            for idx, region in enumerate(response_json['features']):
                if state_abbr in ('DC', 'NE') and region_type == 'sldl':
                    continue # DC and NE both doesn't have a state house
                props = region['properties']
                df = df.append({
                    'state_abbr': state_abbr,
                    'region_type': region_type,
                    'geoid': props.get('geoid'),
                    'name': props.get('name'),
                    'html_url': HTML_URL % (region_type, props.get('geoid')),
                }, ignore_index=True)
                print("Appended %d regions" % (idx + 1), end='\r')

        return df

def download_jobs_metadata():
    states_json = requests.get(STATES_URL).json()
    states_and_geoids = [(s['usps'], s['geoid']) for s in states_json]

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(process_states(states_and_geoids))
    df = loop.run_until_complete(future)

    df.to_csv(OUTPUT_CSV)


if __name__ == '__main__':
    download_jobs_metadata()
