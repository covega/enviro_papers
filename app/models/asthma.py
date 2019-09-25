from sqlalchemy import Column, Integer, ForeignKey, Sequence, String
from app.models import Base

class CountyAsthmaCounts(Base):
    __tablename__ = 'county_asthma_counts'
    id = Column(Integer, Sequence('county_asthma_counts_seq'), primary_key=True)
    county_shortcode = Column(String(50), ForeignKey('county_fragment.shortcode'), nullable=False)
    num_children = Column(Integer)
    num_adults = Column(Integer)

    def __repr__(self):
        return "<CountyAsthmaCounts(county_shortcode='%s')>" % (self.county_shortcode)

class DistrictAsthmaCounts(Base):
    __tablename__ = 'district_asthma_counts'
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), primary_key=True)
    num_children = Column(Integer)
    num_adults = Column(Integer)

    def __repr__(self):
        return "<DistrictAsthmaCounts(district_shortcode='%s')>" % (self.county_shortcode)
