import os, os.path
from config import DATA_DIR
import pandas as pd
from datasets import DataSet

COUNTY_POLLING_INFO_PATH = os.path.join(DATA_DIR, 'Yale_Polling.csv')

class PollingResult(object):
    def __init__(self, avg, min_county, min_result, max_county, max_result):
        self.avg = avg
        self.min_county = min_county
        self.min_result = min_result
        self.max_county = max_county
        self.max_result = max_result


class StatePollingInfo(object):
    def __init__(self, abbr, happening, worried, regulate, rebates):
        self.abbr = abbr
        self.happening = happening
        self.worried = worried
        self.regulate = regulate
        self.rebates = rebates

    def add_stats(self, district):
        max_pop_county = max(district.counties, key=lambda c:c.population)
        min_pop_county = min(district.counties, key=lambda c:c.population) # by population

        avg_polling_happening = sum(
            self.happening[county.key] * county.population
            for county in district.counties) / district.total_population
        polling_happening = PollingResult(avg_polling_happening,
                                          min_pop_county,
                                          self.happening[min_pop_county.key],
                                          max_pop_county,
                                          self.happening[max_pop_county.key])
        setattr(district, 'polling_happening', polling_happening)

        avg_polling_worried = sum(
            self.worried[county.key] * county.population
            for county in district.counties) / district.total_population
        polling_worried = PollingResult(avg_polling_worried,
                                        min_pop_county,
                                        self.worried[min_pop_county.key],
                                        max_pop_county,
                                        self.worried[max_pop_county.key])
        setattr(district, 'polling_worried', polling_worried)

        avg_polling_regulate = sum(
            self.regulate[county.key] * county.population
            for county in district.counties) / district.total_population
        polling_regulate = PollingResult(avg_polling_regulate,
                                         min_pop_county,
                                         self.regulate[min_pop_county.key],
                                         max_pop_county,
                                         self.regulate[max_pop_county.key])
        setattr(district, 'polling_regulate', polling_regulate)

        avg_polling_rebates = sum(
            self.rebates[county.key] * county.population
            for county in district.counties) / district.total_population
        polling_rebates = PollingResult(avg_polling_rebates,
                                        min_pop_county,
                                        self.rebates[min_pop_county.key],
                                        max_pop_county,
                                        self.rebates[max_pop_county.key])
        setattr(district, 'polling_rebates', polling_rebates)

class Polling(DataSet):
    def __init__(self):
        self.by_state = {
            "VA": StatePollingInfo("VA", *self._read_va_polling_data())
        }

    def _read_va_polling_data(self):
        county_polling_info = pd.read_csv(COUNTY_POLLING_INFO_PATH,
                                          encoding="ISO-8859-1")

        county_polling_info_counties = [name.lower() for name in county_polling_info['GeoName']]
        county_polling_info_happening = dict(zip(county_polling_info_counties,list(county_polling_info['happening'])))
        county_polling_info_worried = dict(zip(county_polling_info_counties,list(county_polling_info['worried'])))
        county_polling_info_regulate = dict(zip(county_polling_info_counties,list(county_polling_info['regulate'])))
        county_polling_info_rebates = dict(zip(county_polling_info_counties,list(county_polling_info['rebates'])))

        return (county_polling_info_happening,
                county_polling_info_worried,
                county_polling_info_regulate,
                county_polling_info_rebates)













