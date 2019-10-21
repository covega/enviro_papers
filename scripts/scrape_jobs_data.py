#!/usr/bin/env python
# coding: utf-8

import sys
import os, os.path
import requests
import time
import pandas as pd
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

METADATA_CSV = os.path.join(os.getcwd(), 'data/raw/jobs/jobs_metadata.csv')
OUTPUT_CSV = os.path.join(os.getcwd(), 'data/cleaned/jobs/all.csv')

JOB_STAT_KEYS = [
    'countSolarJobs',
    'countWindJobs',
    'countEnergyJobs',
    'totalJobs',
    'percentOfStateJobs',
    'residentialMWhInvested',
    'commercialMWhInvested',
    'utilityMWhInvested',
    'totalMWhInvested',
    'residentialDollarsInvested',
    'commercialDollarsInvested',
    'utilityDollarsInvested',
    'totalDollarsInvested',
    'investmentHomesEquivalent',
    'countResidentialInstallations',
    'countCommercialInstallations',
    'countUtilityInstallations',
    'countTotalInstallations',
    'residentialMWCapacity',
    'commercialMWCapacity',
    'utilityMWCapacity',
    'totalMWCapacity'
]

CSV_KEYS = [
    'stateAbbr',
    'geoType',
    'name',
    'geoid',
    'sourceURL'
]
CSV_KEYS.extend(JOB_STAT_KEYS)

HTML_STRUCTURE = {
    'tables': [
        ['countSolarJobs', 'countWindJobs', 'countEnergyJobs'],
        ['residentialDollarsInvested', 'residentialMWhInvested', 'commercialDollarsInvested', 'commercialMWhInvested', 'utilityDollarsInvested', 'utilityMWhInvested'],
        ['countResidentialInstallations', 'residentialMWCapacity', 'countCommercialInstallations', 'commercialMWCapacity', 'countUtilityInstallations', 'utilityMWCapacity'],
    ],
    'totals': [
        ['totalJobs', 'percentOfStateJobs'],
        ['totalDollarsInvested', 'totalMWhInvested', 'investmentHomesEquivalent'],
        ['countTotalInstallations', 'totalMWCapacity']
    ]
}

REGION_TYPES = [
    ('state', 'State'),
    ('county', 'County'),
    ('sldu', 'State Senate District'),
    ('sldl', 'State House District'),
    ('cd', 'Congressional District')]

def scrape(metadata, attempt=1):
    url = metadata['html_url']
    _idx = metadata['_idx']
    with requests.get(url) as response:
        row = {
            'stateAbbr': metadata['state_abbr'],
            'geoid': metadata['geoid'],
            'geoType': metadata['region_type'],
            'name': metadata['name'],
            'sourceURL': metadata['html_url'],
        }
        unique_key = url.replace('http://assessor.keva.la/cleanenergyprogress', '')

        if attempt > 3:
            print("%d: [%d/3] – %s – FAIL  – %s" % (_idx, attempt, response.status_code, unique_key))
            return None

        if response.status_code >= 400:
            print("%d: [%d/3] – %s – RETRY – %s" % (_idx, attempt, response.status_code, unique_key))
            time.sleep(3)
            return scrape(metadata, attempt + 1)

        html = response.text
        soup = BeautifulSoup(html, 'html5lib')

        row['name'] = soup.find('span', id='geography__name').text.strip()

        outer_divs = soup.find_all('div', class_='analytics_data')

        for keylist, outerdiv in zip(HTML_STRUCTURE['tables'], outer_divs):
            tds = outerdiv.find_all('td', class_='table_data')
            values = [elem.text.strip() for elem in tds[:len(keylist)]]

            for idx, key in enumerate(keylist):
                row[key] = values[idx]

        li_buckets = soup.find_all('li', class_=None)
        if len(li_buckets) != 3:
            print("%d: [%d/3] – %s – PARSE – %s" % (_idx, attempt, response.status_code, unique_key))
            print("li_buckets:", li_buckets)
            print(html)
            raise ValueError

        for keylist, outerli in zip(HTML_STRUCTURE['totals'], li_buckets):
            total_spans = outerli.find_all('span', class_='analytics_total_num')
            totals = [elem.text.strip() for elem in total_spans]
            if metadata['region_type'] == 'state' and keylist[-1] == 'percentOfStateJobs':
                keylist = keylist [:-1]

            if len(totals) == 0:
                for key in keylist:
                    row[key] = 0
            elif len(totals) != len(keylist):
                print("%d: [%d/3] – %s – PARSE – %s" % (_idx, attempt, response.status_code, unique_key))
                print("totals:", totals, keylist)
                print(html)
                raise ValueError
            else:
                for idx, key in enumerate(keylist):
                    row[key] = totals[idx]

        print("%d: [%d/3] – %s – OK    – %s" % (_idx, attempt, response.status_code, unique_key))
        return row

def scrape_jobs_data():
    jobs_data = None
    if os.path.exists(OUTPUT_CSV):
        jobs_data = pd.read_csv(OUTPUT_CSV, encoding='ISO-8859-1')
    else:
        jobs_data = pd.DataFrame(columns=CSV_KEYS)

    jobs_metadata = [x for _, x in pd.read_csv(METADATA_CSV, encoding='ISO-8859-1').iterrows()]
    processed_urls = set(jobs_data['sourceURL'])

    batch = []
    batch_size = 100

    for i, metadata_row in enumerate(jobs_metadata):
        url = jobs_metadata[i]['html_url']

        if url in processed_urls:
            print ("Skipped: %d" % i, end='\r')
            if i != len(jobs_metadata) - 1:
                continue

        if url not in processed_urls:
            metadata_row['_idx'] = i
            batch.append(metadata_row)

        if len(batch) >= batch_size or i == len(jobs_metadata) - 1:
            print("\nStarting Batch")
            results = ThreadPool(20).imap_unordered(scrape, batch)
            for data_row in results:
                jobs_data = jobs_data.append(data_row, ignore_index=True)

            jobs_data.to_csv(OUTPUT_CSV)
            batch = []
            print("Wrote to disk.")

    jobs_data.to_csv(OUTPUT_CSV)

if __name__ == '__main__':
    scrape_jobs_data()
