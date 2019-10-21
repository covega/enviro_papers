import os, os.path
import pandas as pd
from app.models import (CountyFragment, District, DistrictType, CountyJobStats,
                        DistrictJobStats, StateJobStats)
from app.config import JOBS_DATASET, JOBS_STATS
from app.util import clean_float

def _clean_region_name(name):
    if pd.isna(name):
        return name

    return (name.replace('State House District', '')
                .replace('State Senate District', '')
                .replace('Congressional District', '')
                .replace('State Legislative District', '')
                .replace('State Legislative Subdistrict', '')
                .replace('Delegate District', '')
                .replace('Assembly District', '')
                .replace('District', '')
                .replace('State House', '')
                .replace('Ward ', '')
                .replace('First', '1st')
                .replace('Second', '2nd')
                .replace('Third', '3rd')
                .replace('Fourth', '4th')
                .replace('Fifth', '5th'))

def create_jobs(session):
    js_created = 0
    county_polling_data = pd.read_csv(JOBS_DATASET, encoding="ISO-8859-1")

    session.query(CountyJobStats).delete()
    session.query(DistrictJobStats).delete()
    session.query(StateJobStats).delete()

    for _, row in county_polling_data.iterrows():
        # stateAbbr,geoType,name,geoid,sourceURL

        js = None
        state_abbr = row['stateAbbr']
        geo_type = row['geoType']
        region_name = _clean_region_name(row['name'])

        if geo_type == 'county':
            county_shortcode = CountyFragment.to_shortcode(state_abbr,
                                                           region_name)
            js = CountyJobStats(county_shortcode=county_shortcode)
        elif geo_type == 'sldl':
            district_num = District.to_district_num(state_abbr, region_name)
            district_shortcode = District.to_shortcode(state_abbr,
                                                       DistrictType.STATE_HOUSE,
                                                       district_num)
            js = DistrictJobStats(district_shortcode=district_shortcode)
        elif geo_type == 'sldu':
            district_num = District.to_district_num(state_abbr, region_name)
            district_shortcode = District.to_shortcode(state_abbr,
                                                       DistrictType.STATE_SENATE,
                                                       district_num)
            js = DistrictJobStats(district_shortcode=district_shortcode)
        elif geo_type == 'cd':
            district_num = District.to_district_num(state_abbr, region_name)
            district_shortcode = District.to_shortcode(state_abbr,
                                                       DistrictType.CONGRESSIONAL,
                                                       district_num)
            js = DistrictJobStats(district_shortcode=district_shortcode)
        elif geo_type == 'state':
            js = StateJobStats(state_abbr=row['stateAbbr'])

        for csv_key, sql_fieldname in JOBS_STATS.items():
            setattr(js, sql_fieldname, clean_float(row[csv_key]))

        session.add(js)
        try:
            session.commit()
        except Exception as e:
                print("OOPS: ", state_abbr, district_num, region_name)
        js_created += 1
        print("Job stats records created: %d" % js_created, end="\r")

    print()
