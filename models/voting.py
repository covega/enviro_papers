from sqlalchemy import Column, Integer, Float, ForeignKey, Sequence, String, Text
from models import Base


class VotingRecord(Base):
    __tablename__ = 'voting_record'
    id = Column(Integer, Sequence('voting_record_id_seq'), primary_key=True)
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), nullable=False)
    legislator_name = Column(String(50), nullable=False)
    vote_fulltext = Column(Text, nullable=False)

    def __repr__(self):
        return "<VotingRecord(district_shortcode='%s', legislator_name='%s')>" % (
            self.district_shortcode, self.legislator_name)
