import pandas as pd
import os, os.path
import re
from collections import defaultdict
from config import DATA_DIR
from datasets import DataSet, DistrictType


COUNTY_VOTING_INFO_PATH = os.path.join(DATA_DIR, 'vote_history.csv')
NAMES_DISTRICTS_INFO_PATH = os.path.join(DATA_DIR, 'Names_Districts_Counties.csv')

class StateVotingInfo(object):
    def __init__(self, abbr, names, votes):
        self.abbr = abbr
        self.names = names
        self.votes = votes

    def add_stats(self, district):
        lookup_key = (int(district.number), district.type)
        setattr(district, 'legislator', self.names[lookup_key])
        setattr(district, 'votes', self.votes[lookup_key])

class Voting(DataSet):
    def __init__(self):
        self.by_state = {
            "VA": StateVotingInfo("VA", *self._read_va_voting_data())
        }

    def _read_va_voting_data(self):
        names_districts_info = pd.read_csv(NAMES_DISTRICTS_INFO_PATH, encoding="ISO-8859-1")
        county_voting_info = pd.read_csv(COUNTY_VOTING_INFO_PATH,
                                          encoding="ISO-8859-1")

        candidate_fullnames = [
            first + " " + last
            for first, last in zip(list(names_districts_info['First Name']),
                                   list(names_districts_info['Last Name']))]

        district_nums = [
            int(re.search(r'\d+', raw_district).group())
            for raw_district in names_districts_info['District']]

        chambers = [
            (DistrictType.STATE_SENATE if chamber == "Senate" else
             DistrictType.STATE_HOUSE if chamber == "House" else "??")
            for chamber in names_districts_info['Branch']]

        name_district_lookup = dict(zip(candidate_fullnames, zip(district_nums, chambers)))
        district_name_lookup = dict(zip(zip(district_nums, chambers), candidate_fullnames))
        district_votes_lookup = defaultdict(list)

        for row in county_voting_info.values:
            candidate_name = row[1] + " " + row[2]
            for i in range(4, len(row)):
                district = name_district_lookup[candidate_name]
                sentence = row[i].replace("Candidate", candidate_name)
                if sentence != '-':
                    district_votes_lookup[district].append(sentence)

        return (district_name_lookup,
                district_votes_lookup)













