import os, os.path
import re
import pandas as pd
from app.models import VotingRecord, District, DistrictType
from app.config import VOTING_DATASETS


def read_voting_data(session, state_abbr, voting_csv_path, names_csv_path):
    votes_created = 0
    county_voting_info = pd.read_csv(voting_csv_path, encoding="ISO-8859-1")
    names_districts_info = pd.read_csv(names_csv_path, encoding="ISO-8859-1")

    candidate_fullnames = [
        first + " " + last
        for first, last in zip(list(names_districts_info['First Name']),
                               list(names_districts_info['Last Name']))]

    district_nums = [
        int(re.search(r'\d+', raw_district).group())
        for raw_district in names_districts_info['District']]

    district_types = [
        (DistrictType.STATE_SENATE if chamber == "Senate" else
         DistrictType.STATE_HOUSE if chamber == "House" else "??")
        for chamber in names_districts_info['Branch']]

    district_shortcodes = [
        District.to_shortcode(state_abbr, dtype, num)
        for dtype, num in zip(district_types, district_nums)
    ]

    name_district_lookup = dict(zip(candidate_fullnames, district_shortcodes))

    for row in county_voting_info.values:
        legislator_name = row[1] + " " + row[2]
        for i in range(4, len(row)):
            district_shortcode = name_district_lookup[legislator_name]
            sentence = row[i].replace("Candidate", legislator_name)
            if sentence != '-':
                vr = VotingRecord(district_shortcode=district_shortcode,
                                  legislator_name=legislator_name,
                                  vote_fulltext=sentence)
                session.add(vr)
                votes_created += 1
                print("Voting records created: %d" % votes_created, end="\r")

    print()
    session.commit()

def create_voting(session):
    for state_abbr, voting_csv_path, names_csv_path in VOTING_DATASETS:
        read_voting_data(session, state_abbr, voting_csv_path, names_csv_path)












