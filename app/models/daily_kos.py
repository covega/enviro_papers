from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String, Enum
from app.models import Base
import enum
import re


class DistrictType(enum.Enum):
    STATE_SENATE = 'State Senate'
    STATE_HOUSE = 'State House'
    CONGRESSIONAL = 'Congressional'

    @classmethod
    def to_abbr(cls, dt):
        if dt == cls.STATE_SENATE:
            return 'SS'
        if dt == cls.STATE_HOUSE:
            return 'SS'
        if dt == cls.CONGRESSIONAL:
            return 'CON'


class State(Base):
    __tablename__ = 'state'
    abbr = Column(String(2), primary_key=True)
    # fullname = Column(String(50))

    def __repr__(self):
        return "<State(abbr='%s', fullname='%s')>" % (self.abbr, self.fullname)


class District(Base):
    __tablename__ = 'district'
    shortcode = Column(String(50), primary_key=True)
    fullname = Column(String(50))
    state = Column(String(2), ForeignKey('state.abbr'), nullable=False)
    district_type = Column(Enum(DistrictType))
    district_number = Column(Integer)
    # total_population = ???

    @staticmethod
    def to_shortcode(state, dtype, num):
        return "%s-%s-%d" % (state, DistrictType.to_abbr(dtype), num)

    def __repr__(self):
        return "<District(state='%s', district_type='%s', district_number=%d)>" % (
            self.state, self.district_type, self.district_number)


class CountyFragment(Base):
    __tablename__ = 'county_fragment'
    id = Column(Integer, Sequence('county_fragment_seq'), primary_key=True)
    shortcode = Column(String(50))
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), nullable=False)
    fullname = Column(String(50))
    population = Column(Integer)
    percent_of_whole = Column(Float())

    @staticmethod
    def to_shortcode(state_abbr, fullname):
        fullname_cleaned = re.sub(r"[^a-zA-Z]+", "", fullname).lower()
        return "%s-%s" % (state_abbr, fullname_cleaned)

    def __repr__(self):
        return "<CountyFragment(district_id=%d, fullname='%s')>" % (
            self.district_id, self.fullname)
