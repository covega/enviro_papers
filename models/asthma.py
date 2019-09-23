from sqlalchemy import Column, Integer, ForeignKey, Sequence, String
from models import Base

class CountyAsthmaCounts(Base):
    __tablename__ = 'county_asthma_rate'
    id = Column(Integer, Sequence('county_asthma_rate_seq'), primary_key=True)
    county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'), nullable=False)
    num_children = Column(Integer)
    num_adults = Column(Integer)

    def __repr__(self):
        return "<CountyAsthmaRate(county_shortcode='%s')>" % (self.county_shortcode)
