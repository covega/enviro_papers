import os, os.path

DATA_DIR = os.path.join(os.getcwd(), 'data/cleaned/')
SQLITE = 'sqlite:///papers.db' # on-disk
# SQLITE = 'sqlite://' # in-memory

VOTING_SENTENCES_DATASETS = [
    (
        "VA",
        os.path.join(DATA_DIR, 'voting/va.csv'),
        os.path.join(DATA_DIR, 'Names_Districts_Counties.csv'),
    )
]

VOTING_DATASETS = [
    ("TX", (os.path.join(DATA_DIR, "voting/TX-scorecard-2013.xlsx"),
            os.path.join(DATA_DIR, "voting/TX-scorecard-2015.xlsx"),
            os.path.join(DATA_DIR, "voting/TX-scorecard-2017.xlsx"),
            os.path.join(DATA_DIR, "voting/TX-scorecard-2019.xlsx")))
]

STATES_CSV = os.path.join(DATA_DIR, "states.csv")

class VotingKeys(object):
    STATE = "State"
    YEAR = "Year"
    CHAMBER = "Chamber"
    LEGISLATOR_NAME = "Representative"
    PARTY = "Party"
    DISTRICT = "District"
    BILL_ID = r"^\d+[HS]?$" # 1, 2, 20, 4H, 9S
    YEAR_SCORE = "%d Score"
    LIFETIME_SCORE = "Lifetime Score"
    BILL = "Vote"
    BILL_NO = "No"
    BILL_TITLE = "Title"
    BILL_PRO_ENV = "Pro-environment vote"
    BILL_DETAILS = "Vote details"
    BILL_OUTCOME = "Outcome"

POLLING_DATASET = os.path.join(DATA_DIR, "polling/yale-all-2019.csv")

ASTHMA_DATASETS = [
    ("VA", os.path.join(DATA_DIR, 'asthma/va.csv'))
]

class DailyKosDatasets(object):
    SS_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-senate-districts/')
    SH_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-house-districts/')
    SS_KEYS = ("County", "SD #", "SD Pop.\nin County", "% of County\nin SD")
    SH_KEYS = ("County.2", "HD #", "HD Pop.\nin County", "% of County\nin HD")
