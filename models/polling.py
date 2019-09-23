from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String
from models import Base


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
