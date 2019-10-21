import re
import pandas as pd
from app.config import STATES_CSV

class StateAbbrLookup(object):
    def __init__(self):
        self._state_abbr_lookup = {}
        states_data = pd.read_csv(STATES_CSV, encoding="ISO-8859-1")

        for _, row in states_data.iterrows():
            self._state_abbr_lookup[row["State"]] = row["Abbreviation"]

    def get_abbr(self, fullname):
        return self._state_abbr_lookup.get(fullname)

def safe_cast(type, value):
    try:
        return type(value)
    except (ValueError, TypeError):
        return None

def clean_float(s):
    if type(s) == str:
        s = re.sub(r"[^0-9.]*", "", s)

    return float(s)
