import os, os.path
from config import DATA_DIR
import pandas as pd
from datasets import DataSet

COUNTY_ASTHMA_INFO_PATH = os.path.join(DATA_DIR,
                                       'Asthma_Data_ALA_6.26.2019.csv')

class StateAsthmaInfo(object):
    def __init__(self, abbr, children, adults):
        self.abbr = abbr
        self.children = children
        self.adults = adults

    def add_stats(self, district):
        asthma_children = int(sum(
            self.children[county.key] * county.percent_of_district
            for county in district.counties))
        setattr(district, 'asthma_children', asthma_children)

        asthma_adults = int(sum(
            self.adults[county.key] * county.percent_of_district
            for county in district.counties))
        setattr(district, 'asthma_adults', asthma_adults)

class Asthma(DataSet):
    def __init__(self):
        self.by_state = {
            "VA": StateAsthmaInfo("VA", *self._read_va_asthma_data())
        }

    def _read_va_asthma_data(self):
        county_asthma_info = pd.read_csv(COUNTY_ASTHMA_INFO_PATH,
                                         encoding="ISO-8859-1")

        # Drop labels 133 to get rid of "total" column
        asthma_info_county_keys = [name.lower() for name in county_asthma_info['County'].drop(labels=133)]
        asthma_info_children = list(county_asthma_info['Pediatric Asthma'].drop(labels=133))
        asthma_info_adults = list(county_asthma_info['Adult Asthma'].drop(labels=133))

        asthma_info_children = [int(x.replace(',', '')) for x in asthma_info_children]
        asthma_info_adults = [int(x.replace(',', '')) for x in asthma_info_adults]

        county_to_asthma_children = dict(zip(asthma_info_county_keys,
                                             asthma_info_children))
        county_to_asthma_adults = dict(zip(asthma_info_county_keys,
                                           asthma_info_adults))

        return county_to_asthma_children, county_to_asthma_adults

