import os, os.path
import pandas as pd
from app.models import State, District, CountyFragment, DistrictType
from app.config import DailyKosDatasets as DK


def create_states(session):
    """Yields states"""
    states_created = 0
    for filename in os.listdir(DK.SS_FOLDER):
        state_abbr = os.path.splitext(filename)[0]
        session.add(State(abbr=state_abbr))
        states_created += 1
        print("State records created: %d" % states_created, end="\r")

    print()
    session.commit()


def create_counties_and_districts(session, folder, keys, district_type):
    """Yields counties and districts"""
    districts_created = 0
    counties_created = 0

    for filename in os.listdir(folder):
        state_abbr = os.path.splitext(filename)[0]
        file_path = os.path.join(folder, filename)
        csv_data = pd.read_csv(file_path, encoding = "ISO-8859-1")

        (county_name_key, district_num_key, county_pop_key, percent_key) = keys

        for _, row in csv_data.iterrows():
            raw_district_num = row.get(district_num_key)

            # Exclude floterial districts in New Hampshire that have no
            # associated geographical area
            # (https://en.wikipedia.org/wiki/Floterial_district)
            if type(raw_district_num) == str and "(F)" in raw_district_num:
                continue

            district_num = District.to_district_num(state_abbr, raw_district_num)
            county_fullname = row.get(county_name_key)
            county_population = row.get(county_pop_key)
            county_percent_of_whole = row.get(percent_key)

            if district_num is None or not county_fullname:
                continue

            district = session.query(District).filter_by(state=state_abbr, district_number=district_num).first()
            district_shortcode = District.to_shortcode(state_abbr, district_type, district_num)
            if not district:
                district = District(shortcode=district_shortcode,
                                    state=state_abbr,
                                    district_type=district_type,
                                    district_number=district_num)
                districts_created += 1
                print("%s District records created: %d County fragment records created: %d" % (district_type.value, districts_created, counties_created), end="\r")
                session.add(district)

            county_shortcode = CountyFragment.to_shortcode(state_abbr,
                                                           county_fullname)
            cf = CountyFragment(shortcode=county_shortcode,
                                district_shortcode=district_shortcode,
                                fullname=county_fullname,
                                population=county_population,
                                percent_of_whole=county_percent_of_whole)
            counties_created += 1
            print("%s District records created: %d County fragment records created: %d" % (district_type.value, districts_created, counties_created), end="\r")
            session.add(cf)

    print()
    session.commit()

def create_daily_kos(session):
    create_states(session)
    create_counties_and_districts(session, DK.SS_FOLDER, DK.SS_KEYS, DistrictType.STATE_SENATE)
    create_counties_and_districts(session, DK.SH_FOLDER, DK.SH_KEYS, DistrictType.STATE_HOUSE)
