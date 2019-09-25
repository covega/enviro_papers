import os, os.path

DATA_DIR = os.path.join(os.getcwd(), 'data/cleaned/')
SQLITE = 'sqlite:///papers.db' # on-disk
# SQLITE = 'sqlite://' # in-memory

VOTING_DATASETS = [
    (
        "VA",
        os.path.join(DATA_DIR, 'voting/va.csv'),
        os.path.join(DATA_DIR, 'Names_Districts_Counties.csv'),
    ),
]

POLLING_DATASETS = [
    ("VA", os.path.join(DATA_DIR, "polling/va.csv"))
]

ASTHMA_DATASETS = [
    ("VA", os.path.join(DATA_DIR, 'asthma/va.csv'))
]

class DailyKosDatasets(object):
    SS_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-senate-districts/')
    SH_FOLDER = os.path.join(DATA_DIR, 'daily-kos/counties-to-state-house-districts/')
    SS_KEYS = ("County", "SD #", "SD Pop.\nin County", "% of County\nin SD")
    SH_KEYS = ("County.2", "HD #", "HD Pop.\nin County", "% of County\nin HD")
