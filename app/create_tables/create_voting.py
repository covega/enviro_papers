import os, os.path
import re
import pandas as pd
from app.util import safe_cast
from app.models import (VotingRecord, Vote, Bill, District, DistrictType,
                        VotingClassification, Party, VotingAction)
from app.config import (VOTING_DATASETS, VOTING_SENTENCES_DATASETS,
                        VotingKeys as VK)

VOTING_CHAMBERS = [('House', DistrictType.STATE_HOUSE),
                   ('Senate', DistrictType.STATE_SENATE)]

def read_voting_sentences(session, state_abbr, voting_csv_path, names_csv_path):
    county_voting_info = pd.read_csv(voting_csv_path, encoding="ISO-88591")
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


def read_voting_data(session, state_abbr, datasets):
    bills_created = 0
    votes_created = 0

    for xlsx_path in datasets:
        df = pd.read_excel(xlsx_path, sheet_name=None)

        bills_sheet = df["Votes"]
        bills = {}

        for _, row in bills_sheet.iterrows():
            bill_id = row[VK.BILL]
            bill_no = row[VK.BILL_NO]
            bill_title = row[VK.BILL_TITLE]
            bill_pro_env = VotingAction.fuzzy_cast(row[VK.BILL_PRO_ENV])
            bill_details = row[VK.BILL_DETAILS]
            bill_outcome = row.get(VK.BILL_OUTCOME, None)
            b = Bill(state=state_abbr,
                     pro_environment_decision=bill_pro_env,
                     title=bill_title,
                     code=bill_no,
                     description=bill_details,
                     outcome=bill_outcome)

            bills[bill_id] = b # For use in this function only
            session.add(b) # Save to db
            bills_created += 1
            print("Voting records created: %d  Bill records created: %d" % (
                  votes_created, bills_created), end="\r")

        session.commit()

        for sheet_name, district_type in VOTING_CHAMBERS:
            sheet_content = df[sheet_name]
            for _, row in sheet_content.iterrows():
                state = row[VK.STATE]
                year = int(row[VK.YEAR])
                district_number = int(row[VK.DISTRICT])
                legislator_name = row[VK.LEGISLATOR_NAME]
                party = safe_cast(Party, row[VK.PARTY])
                year_score = safe_cast(float, row[VK.YEAR_SCORE % year])
                lifetime_score = safe_cast(float, row.get(VK.LIFETIME_SCORE))
                district_shortcode = District.to_shortcode(state_abbr,
                                                           district_type,
                                                           district_number)
                for key in row.keys():
                    if key and re.match(VK.BILL_ID, str(key)): # This column is a vote
                        raw_classification = row[key]
                        try:
                            c = VotingClassification(raw_classification)
                        except ValueError:
                            # print("Invalid vote classification: '%s'%s" % (
                            #       raw_classification, ' ' * 20))
                            c = VotingClassification.UNKNOWN
                        v = Vote(district_shortcode=district_shortcode,
                                 legislator_name=legislator_name,
                                 classification=c,
                                 party=party,
                                 year=year,
                                 year_score=year_score,
                                 lifetime_score=lifetime_score,
                                 bill_id=bills[key].id)
                        votes_created += 1
                        session.add(v)
                        print("Voting records created: %d  Bill records created: %d" % (
                              votes_created, bills_created), end="\r")
    session.commit()
    print()


def create_voting(session):
    # for state_abbr, voting_csv_path, names_csv_path in VOTING_SENTENCES_DATASETS:
    #     read_voting_sentences(session, state_abbr, voting_csv_path, names_csv_path)

    for state_abbr, _, datasets in VOTING_DATASETS:
        read_voting_data(session, state_abbr, datasets)
