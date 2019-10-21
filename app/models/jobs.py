from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String
from app.models import Base


class RegionJobStats(object):
    # Clean Energy Jobs
    count_solar_jobs = Column(Integer)
    count_wind_jobs = Column(Integer)
    count_energy_jobs = Column(Integer)
    total_jobs = Column(Integer)

    percent_of_state_jobs = Column(Float)

    # Clean Energy Investment
    residential_mwh_invested = Column(Float)
    commercial_mwh_invested = Column(Float)
    utility_mwh_invested = Column(Float)
    total_mwh_invested = Column(Float)

    residential_dollars_invested = Column(Float)
    commercial_dollars_invested = Column(Float)
    utility_dollars_invested = Column(Float)
    total_dollars_invested = Column(Float)

    investment_homes_equivalent = Column(Float)

    # Clean Energy Installations
    count_residential_installations = Column(Integer)
    count_commercial_installations = Column(Integer)
    count_utility_installations = Column(Integer)
    total_installations = Column(Integer)

    residential_mw_capacity = Column(Float)
    commercial_mw_capacity = Column(Float)
    utility_mw_capacity = Column(Float)
    total_mw_capacity = Column(Float)


class CountyJobStats(Base, RegionJobStats):
    __tablename__ = 'county_job_stats'
    county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'), primary_key=True)

    def __repr__(self):
        return "<CountyJobStats(county_shortcode='%s')>" % (self.county_shortcode)

class DistrictJobStats(Base, RegionJobStats):
    __tablename__ = 'district_job_stats'
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), primary_key=True)

    def __repr__(self):
        return "<DistrictJobStats(district_shortcode='%s')>" % (self.district_shortcode)

class StateJobStats(Base, RegionJobStats):
    __tablename__ = 'state_job_stats'
    state_abbr = Column(String(50), ForeignKey('state.abbr'), primary_key=True)

    def __repr__(self):
        return "<StateJobStats(state_abbr='%s')>" % (self.state_abbr)
