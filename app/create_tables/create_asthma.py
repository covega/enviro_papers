import os, os.path
import pandas as pd
from app.models import CountyAsthmaCounts, CountyFragment
from app.config import ASTHMA_DATASET


def create_asthma(session):
    county_asthma_info = pd.read_csv(ASTHMA_DATASET, encoding="ISO-8859-1")

    for idx, row in county_asthma_info.iterrows():
        state_abbr = row['State']
        raw_fullname = row['County']
        county_shortcode = CountyFragment.to_shortcode(state_abbr, raw_fullname)

        num_children = int(row['PedAshtma'].replace(',', ''))
        num_adults = int(row['AAshthma'].replace(',', ''))
        ac = CountyAsthmaCounts(county_shortcode=county_shortcode,
                                num_children=num_children,
                                num_adults=num_adults)
        session.add(ac)
        print("Asthma records created: %d" % (idx + 1), end="\r")

    print()
    session.commit()
