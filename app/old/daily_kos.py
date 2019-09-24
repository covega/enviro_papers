import os, os.path
import pandas as pd
from config import DATA_DIR
from datasets import DistrictType

SS_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-senate-districts/')
SH_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-house-districts/')
SS_KEYS = ("County", "SD #", "SD Pop.\nin County", "% of County\nin SD")
SH_KEYS = ("County.2", "HD #", "HD Pop.\nin County", "% of County\nin HD")

class CountyInDistrict(object):
    def __init__(self, district, name, population, percent_of_county):
        self.district = district
        self.key = name.lower()
        self.name = name
        self.population = int(population)
        self.percent_of_district = percent_of_county

    def __str__(self):
        return self.name

class District(object):
    def __init__(self, state, district_type, number):
        self.state = state
        self.type = district_type
        self.number = number
        self.counties = []
        self.total_population = 0

    def __str__(self):
        return '%s %s District #%s' % (self.state, self.type, self.number)

    def add_county(self, county):
        self.counties.append(county)
        self.total_population += county.population

class State(object):
    def __init__(self, abbr):
        self.abbr = abbr
        self.state_sentate_districts = {}
        self.state_house_districts = {}

    def __str__(self):
        return self.abbr

    @property
    def districts(self):
        for ssd in self.state_sentate_districts.values():
            yield ssd

        for shd in self.state_house_districts.values():
            yield shd

    def add_district(self, district):
        if district.type == DistrictType.STATE_SENATE:
            self.state_sentate_districts[district.number] = district
        elif district.type == DistrictType.STATE_HOUSE:
            self.state_house_districts[district.number] = district
        else:
            raise Exception("Unknown type")

    def get_district(self, district_type, number):
        if district_type == DistrictType.STATE_SENATE:
            return self.state_sentate_districts.get(number)
        elif district_type == DistrictType.STATE_HOUSE:
            return self.state_house_districts.get(number)
        else:
            raise Exception("Unknown type")

class DailyKos(object):
    def __init__(self):
        self.states = {}
        self._create_states()
        self._read_district_info(SS_FOLDER, SS_KEYS, DistrictType.STATE_SENATE)
        self._read_district_info(SH_FOLDER, SH_KEYS, DistrictType.STATE_HOUSE)

    def join_with_dataset(self, dataset):
        for state_abbr, state_data in dataset:
            print(state_abbr, state_data)
            for district in self.states[state_abbr].districts:
                state_data.add_stats(district)

    def _create_states(self):
        for filename in os.listdir(SS_FOLDER):
            state_abbr = os.path.splitext(filename)[0]
            self.states[state_abbr] = State(state_abbr)

    def _read_district_info(self, folder, keys, district_type):
        for filename in os.listdir(folder):
            state_abbr = os.path.splitext(filename)[0]
            state = self.states[state_abbr]

            file_path = os.path.join(folder, filename)
            csv_data = pd.read_csv(file_path, encoding = "ISO-8859-1")

            (county_name_key, district_num_key, county_pop_key, percent_key) = keys

            for _, row in csv_data.iterrows():
                district_num = row.get(district_num_key)
                county_name = row.get(county_name_key)
                county_pop_in_district = row.get(county_pop_key)
                percent_of_county_in_district = row.get(percent_key)

                if not district_num or not county_name:
                    continue

                district_num = district_num if type(district_num) == str else str(int(district_num))

                district = state.get_district(district_type, district_num)
                if not district:
                    district = District(state, district_type, district_num)
                    state.add_district(district)

                district.add_county(
                    CountyInDistrict(district,
                                     county_name,
                                     county_pop_in_district,
                                     percent_of_county_in_district))
