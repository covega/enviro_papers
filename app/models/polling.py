from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String
from app.models import Base


class CountyPoll(Base):
    __tablename__ = 'county_poll'
    id = Column(Integer, Sequence('county_poll_id_seq'), primary_key=True)
    county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'), nullable=False)
    percent_happening = Column(Float)
    percent_worried = Column(Float)
    percent_regulate = Column(Float)
    percent_rebates = Column(Float)

    def __repr__(self):
        return "<CountyPoll(county_shortcode='%s')>" % (self.county_shortcode)

class DistrictPoll(Base):
    __tablename__ = 'district_poll'
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), primary_key=True)
    largest_county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'))
    smallest_county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'))

    avg_percent_happening = Column(Float)
    avg_percent_worried = Column(Float)
    avg_percent_regulate = Column(Float)
    avg_percent_rebates = Column(Float)

    largest_county_percent_happening = Column(Float)
    largest_county_percent_worried = Column(Float)
    largest_county_percent_regulate = Column(Float)
    largest_county_percent_rebates = Column(Float)

    smallest_county_percent_worried = Column(Float)
    smallest_county_percent_happening = Column(Float)
    smallest_county_percent_regulate = Column(Float)
    smallest_county_percent_rebates = Column(Float)

    def __repr__(self):
        return "<DistrictPoll(district_shortcode='%s')>" % (self.district_shortcode)

