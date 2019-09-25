import os, os.path
import pandas as pd
from app.models import CountyPoll, CountyFragment
from app.config import POLLING_DATASET, STATES_CSV


def create_polling(session):
    polls_created = 0
    states_data = pd.read_csv(STATES_CSV, encoding="ISO-8859-1")
    state_abbr_lookup = {}

    for _, row in states_data.iterrows():
        state_abbr_lookup[row["State"]] = row["Abbreviation"]

    county_polling_data = pd.read_csv(POLLING_DATASET, encoding="ISO-8859-1")

    for _, row in county_polling_data.iterrows():
        if row['GeoType'] != 'County':
            continue
        (county_fullname, state_fullname) = row['GeoName'].split(', ')
        county_fullname = county_fullname.replace('County', '')
        state_abbr = state_abbr_lookup[state_fullname]
        county_shortcode = CountyFragment.to_shortcode(state_abbr,
                                                       county_fullname)
        percent_happening = row['happening']
        percent_worried = row['worried']
        percent_regulate = row['regulate']
        percent_rebates = row['rebates']
        cp = CountyPoll(county_shortcode=county_shortcode,
                        percent_happening=percent_happening,
                        percent_worried=percent_worried,
                        percent_regulate=percent_regulate,
                        percent_rebates=percent_rebates)
        session.add(cp)
        polls_created += 1
        print("Polling records created: %d" % polls_created, end="\r")

    print()
    session.commit()
