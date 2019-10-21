#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String, Enum
from app.models import Base
import enum
import re
import unidecode


class DistrictType(enum.Enum):
    STATE_SENATE = 'State Senate'
    STATE_HOUSE = 'State House'
    CONGRESSIONAL = 'Congressional'

    @classmethod
    def to_abbr(cls, dt):
        if dt == cls.STATE_SENATE:
            return 'SS'
        if dt == cls.STATE_HOUSE:
            return 'SH'
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
    state = Column(String(2), ForeignKey('state.abbr'), nullable=False)
    district_type = Column(Enum(DistrictType))
    district_number = Column(String(50)) # Because VT...
    # total_population = ???

    @staticmethod
    def to_shortcode(state, dtype, num):
        return "%s-%s-%s" % (state, DistrictType.to_abbr(dtype), num)

    @staticmethod
    def to_district_num(state_abbr, raw_num):
        if type(raw_num) in (float, int):
            return str(int(raw_num))

        if type(raw_num) == str:
            try:
                return str(int(raw_num))
            except Exception:
                # Only numbers, letters, space, perioid, and dash.
                num_normalized = re.sub(r"[^\w\-\. 0-9]+", "", raw_num).lower().strip()
                # Remove number suffixes like 1st -> 1.
                num_cleaned = re.sub(r"((?:[0-9]+)(th )|(?:[0-9]+)(st )|(?:[0-9]+)(nd ))", r'\1', num_normalized)
                # Remove the word " No. "
                num_cleaned = re.sub(r"(\.[^0-9]|no. )", ' ', num_normalized)
                # Remove leading zeros anywhere
                num_cleaned = re.sub(r"(^0+)", "", num_cleaned)
                num_cleaned = re.sub(r"([\s]+[0]+)", " ", num_cleaned)
                # Remove "County"
                num_cleaned = re.sub(r"(county)", "", num_cleaned)
                # Turn whitespace to dashes
                num_cleaned = re.sub(r"[\s]+", '-', num_cleaned.strip())

                if num_cleaned == 'al':
                    num_cleaned = 'at-large'

                valid_ak = state_abbr == 'AK' and District._is_valid_ak_district(num_cleaned)
                valid_vt = state_abbr in ('VT', 'MA', 'NH') # No district numbers...
                valid_split = District._is_valid_split_district(num_cleaned)
                valid_at_large = District._is_valid_at_large(num_cleaned)

                if valid_ak or valid_vt or valid_split or valid_at_large:
                    # Format like chittenden-6-2, 24b, or a24
                    return num_cleaned

                digits = [i for i in num_cleaned if i.isdigit() or i == '.']

                if len(digits) == 0:
                    raise ValueError(raw_num, num_cleaned, state_abbr)

                # Format like "18"
                return str(int(float(''.join(digits))))

    @staticmethod
    def _is_valid_ak_district(d_num):
        return (type(d_num) == str
                and len(d_num) == 1
                and d_num.isalpha())

    @staticmethod
    def _is_valid_split_district(d_num):
        return type(d_num) == str and re.match(r"^[0-9]+[ab]+", d_num)

    @staticmethod
    def _is_valid_at_large(d_num):
        return d_num == 'at-large'

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
        # You better believe that ñ caused problems for a bit
        fullname_unaccented = unidecode.unidecode(fullname)

        # Normalize
        fullname_normalized = re.sub(r"[^\w]+", "", fullname_unaccented).lower()

        if fullname_normalized in ('baltimorecity', # 'baltimorecounty',
                                   'richmondcity', # 'richmondcounty',
                                   'franklincity', # 'franklincounty',
                                   'fairfaxcity', # 'fairfaxcounty',
                                   'roanokecity', # 'roanokecounty',
                                   'stlouiscity'): # 'stlouiscounty'):
            # Balitmore, Richmond, etc have two associated counties that
            # differ in name only by the presence of one of the below words...
            # Strip the county because that's what Daily Kos does.
            fullname_cleaned = fullname_normalized
        else:
            # Remove descriptor words that are not applied the same by all datasets
            fullname_cleaned = re.sub(r"(county|city|and|borough|municipality|censusarea)", "", fullname_normalized)

        return "%s-%s" % (state_abbr, fullname_cleaned)

    def __repr__(self):
        return "<CountyFragment(district_id=%d, fullname='%s')>" % (
            self.district_id, self.fullname)
