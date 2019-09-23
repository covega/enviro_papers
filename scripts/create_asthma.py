import os, os.path
import pandas as pd
from models import CountyAsthmaCounts, CountyFragment
from main import DATA_DIR

COUNTY_ASTHMA_INFO = [
    ("VA", os.path.join(DATA_DIR, 'Asthma_Data_ALA_6.26.2019.csv'))
]

def read_asthma_data(session, state_abbr, csv_path):
    asthma_created = 0
    county_asthma_info = pd.read_csv(csv_path, encoding="ISO-8859-1")

    for _, row in county_asthma_info.iterrows():
        raw_fullname = row['County']

        if raw_fullname == "TOTAL":
            continue # skip last row

        county_shortcode = CountyFragment.to_shortcode(state_abbr, raw_fullname)
        num_children = int(row['Pediatric Asthma'].replace(',', ''))
        num_adults = int(row['Adult Asthma'].replace(',', ''))
        cp = CountyAsthmaCounts(county_shortcode=county_shortcode,
                                num_children=num_children,
                                num_adults=num_adults)
        session.add(cp)
        asthma_created += 1
        print("Asthma records created: %d" % asthma_created, end="\r")

    print()
    session.commit()

def create_asthma(session):
    for state_abbr, csv_path in COUNTY_ASTHMA_INFO:
        read_asthma_data(session, state_abbr, csv_path)
