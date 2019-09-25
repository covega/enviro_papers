from abc import ABC, abstractmethod

class StateLeveLinfo(ABC):
    @abstractmethod
    def add_stats(self, district):
        pass

class DataSet(ABC):
    def __init__(self):
        this.by_state = {}

    def __iter__(self):
        for state_abbr, state_data in self.by_state.items() :
            yield (state_abbr, state_data)

    def __getitem__(self, state_abbr):
        return self.by_state[state_abbr]

class DistrictType(object):
    STATE_SENATE = 'State Senate'
    STATE_HOUSE = 'State House'
    CONGRESSIONAL = 'Congressional'
