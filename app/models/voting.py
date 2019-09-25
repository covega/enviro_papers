from sqlalchemy import (Column, Integer, Enum, Float, ForeignKey, Sequence,
                        String, Text)
from app.models import Base
import enum

class VotingClassification(enum.Enum):
    PRO_ENVIRONEMNT = "+" # Vote for the environment
    ANTI_ENVIRONMENT = "-" # Vote against the environment
    EXCUSED = "E" # Excused from Vote
    ABSENT = "A" # Unexcused Absence from Vote
    PRESENT = "P" # Present, Not Voting
    UNKNOWN = "N/A"

class VotingAction(enum.Enum):
    YES = "YES"
    NO = "NO"

    @classmethod
    def fuzzy_cast(cls, s):
        out = None
        try:
            out = cls(s)
        except ValueError:
            if s.startswith(cls.YES.value):
                out = cls.YES
            elif s.startswith(cls.NO.value):
                out = cls.NO
        return out

class Party(enum.Enum):
    DEMOCRAT = "D"
    REPUBLICAN = "R"
    INDEPENDANT = "I"


class VotingRecord(Base):
    __tablename__ = 'voting_record'
    id = Column(Integer, Sequence('voting_record_id_seq'), primary_key=True)
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), nullable=False)
    legislator_name = Column(String(50), nullable=False)
    vote_fulltext = Column(Text, nullable=False)

    def __repr__(self):
        return "<VotingRecord(district_shortcode='%s', legislator_name='%s')>" % (
            self.district_shortcode, self.legislator_name)


class Bill(Base):
    __tablename__ = 'bill'
    id = Column(Integer, Sequence('bill_id_seq'), primary_key=True)
    state = Column(String(2), ForeignKey('state.abbr'), nullable=False)
    pro_environment_decision = Column(Enum(VotingAction))
    title = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    description = Column(Text)
    outcome = Column(String(50))

    def __repr__(self):
        return "<Bill(state='%s', code='%s', title='%s')>" % (
            self.state, self.code, self.title)


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, Sequence('vote_id_seq'), primary_key=True)
    district_shortcode = Column(String(50), ForeignKey('district.shortcode'), nullable=False)
    legislator_name = Column(String(50), nullable=False)
    classification = Column(Enum(VotingClassification), nullable=False)
    bill_id = Column(Integer, ForeignKey('bill.id'), nullable=False)
    year = Column(Integer, nullable=False)
    party = Column(Enum(Party))
    year_score = Column(Float)
    lifetime_score = Column(Float)

    def __repr__(self):
        return "<Vote(district_shortcode='%s', legislator_name='%s')>" % (
            self.district_shortcode, self.legislator_name)
