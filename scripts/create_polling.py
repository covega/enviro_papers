import os, os.path
import pandas as pd
from models import CountyPoll, CountyFragment
from config import DATA_DIR

COUNTY_POLLING_INFO = [
    ("VA", os.path.join(DATA_DIR, "Yale_Polling.csv"))
]

def read_polling_data(session, state_abbr, csv_path):
    polls_created = 0
    county_polling_info = pd.read_csv(csv_path, encoding="ISO-8859-1")

    for _, row in county_polling_info.iterrows():
        raw_fullname = row['GeoName']
        county_shortcode = CountyFragment.to_shortcode(state_abbr, raw_fullname)
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
        print("Polls created: %d" % polls_created, end="\r")

    print()
    session.commit()

def create_polling(session):
    for state_abbr, csv_path in COUNTY_POLLING_INFO:
        read_polling_data(session, state_abbr, csv_path)