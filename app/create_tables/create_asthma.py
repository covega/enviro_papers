import os, os.path
import pandas as pd
from app.models import CountyAsthmaCounts, CountyFragment
from app.config import ASTHMA_DATASETS


def read_asthma_data(session, state_abbr, csv_path):
    asthma_created = 0
    county_asthma_info = pd.read_csv(csv_path, encoding="ISO-8859-1")

    for _, row in county_asthma_info.iterrows():
        raw_fullname = row['County']
        county_shortcode = CountyFragment.to_shortcode(state_abbr, raw_fullname)

        if county_shortcode == "VA-total":
            continue # skip last row

        num_children = int(row['Pediatric Asthma'].replace(',', ''))
        num_adults = int(row['Adult Asthma'].replace(',', ''))
        ac = CountyAsthmaCounts(county_shortcode=county_shortcode,
                                num_children=num_children,
                                num_adults=num_adults)
        session.add(ac)
        asthma_created += 1
        print("Asthma records created: %d" % asthma_created, end="\r")

    print()
    session.commit()

def create_asthma(session):
    for state_abbr, csv_path in ASTHMA_DATASETS:
        read_asthma_data(session, state_abbr, csv_path)
