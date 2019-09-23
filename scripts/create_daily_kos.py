import os, os.path
import pandas as pd
from models import State, District, CountyFragment, DistrictType
from config import DATA_DIR

SS_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-senate-districts/')
SH_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-house-districts/')
SS_KEYS = ("County", "SD #", "SD Pop.\nin County", "% of County\nin SD")
SH_KEYS = ("County.2", "HD #", "HD Pop.\nin County", "% of County\nin HD")


def create_states(session):
    """Yields states"""
    states_created = 0
    for filename in os.listdir(SS_FOLDER):
        state_abbr = os.path.splitext(filename)[0]
        session.add(State(abbr=state_abbr))
        states_created += 1
        print("States created: %d" % states_created, end="\r")

    print()
    session.commit()

def _clean_distrit_num(district_num):
    if type(district_num) == float:
        return int(district_num)

    if type(district_num) == str:
        chars = [i for i in district_num if i.isdigit()]
        if len(chars) > 0:
            return int(''.join(chars))

    return district_num

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
            district_num = _clean_distrit_num(row.get(district_num_key))
            county_fullname = row.get(county_name_key)
            county_population = row.get(county_pop_key)
            county_percent_of_whole = row.get(percent_key)

            if type(district_num) != int or not county_fullname:
                continue

            district = session.query(District).filter_by(state=state_abbr, district_number=district_num).first()
            district_shortcode = District.to_shortcode(state_abbr, district_type, district_num)
            if not district:
                district = District(shortcode=district_shortcode,
                                    state=state_abbr,
                                    district_type=district_type,
                                    district_number=district_num)
                districts_created += 1
                print("%s Districts created: %d Counties created: %d" % (district_type.value, districts_created, counties_created), end="\r")
                session.add(district)

            county_shortcode = CountyFragment.to_shortcode(state_abbr,
                                                           county_fullname)
            cf = CountyFragment(shortcode=county_shortcode,
                                district_shortcode=district_shortcode,
                                fullname=county_fullname,
                                population=county_population,
                                percent_of_whole=county_percent_of_whole)
            counties_created += 1
            print("%s Districts created: %d Counties created: %d" % (district_type.value, districts_created, counties_created), end="\r")
            session.add(cf)

    print()
    session.commit()

def create_daily_kos(session):
    create_states(session)
    create_counties_and_districts(session, SS_FOLDER, SS_KEYS, DistrictType.STATE_SENATE)
    create_counties_and_districts(session, SH_FOLDER, SH_KEYS, DistrictType.STATE_HOUSE)

