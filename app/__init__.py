from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.models import * # initialize models
from app.config import SQLITE
from app.models import (Base, DistrictIncumbentVote, DistrictPoll,
                        DistrictAsthmaCounts, VotingClassification)
from app.queries import (create_district_asthma_counts,
                         create_district_incumbent_record,
                         create_district_polls)
from app.create_tables import (create_daily_kos, create_polling, create_asthma,
                               create_voting)

class EnvironmentPapersDatabase:
    db_engine = None

    def __init__(self):
        self.db_engine = create_engine(SQLITE)
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def create_tables(self):
        Base.metadata.drop_all(self.db_engine)
        Base.metadata.create_all(self.db_engine)
        create_daily_kos(self.session)
        create_polling(self.session)
        create_asthma(self.session)
        create_voting(self.session)
        print("Basic tables created")

    def create_district_data(self):
        create_district_asthma_counts(self.session)
        create_district_incumbent_record(self.session)
        create_district_polls(self.session)
        print("District tables created")

    def print_district_completeness(self):
        daily_kos_districts = set(r for (r,) in self.session.query(District.shortcode.distinct()))
        asthma_districts = set(r for (r,) in self.session.query(DistrictAsthmaCounts.district_shortcode.distinct()))
        asthma_missing = daily_kos_districts - asthma_districts
        polling_districts = set(r for (r,) in self.session.query(DistrictPoll.district_shortcode.distinct()))
        polling_missing = daily_kos_districts - polling_districts
        voting_districts = set(r for (r,) in self.session.query(DistrictIncumbentVote.district_shortcode.distinct()))

        print("District coverage:")
        print(" - Daily Kos: %d" % len(daily_kos_districts))
        print(" - ALA Asthma: %d (%d missing)" % (len(asthma_districts), len(asthma_missing)))
        print(" - Polling: %d (%d missing)" % (len(polling_districts), len(polling_missing)))
        print(" - Incumbent Voting: %d" % len(voting_districts))

    def print_example_queries(self):
        vote = self.session.query(DistrictIncumbentVote.legislator_name,
                                  DistrictIncumbentVote.district_shortcode,
                                  func.count('*').label('num_votes')).\
                            filter(DistrictIncumbentVote.district_shortcode=='TX-SS-57',
                                   DistrictIncumbentVote.classification==VotingClassification.ANTI_ENVIRONMENT).\
                            first()

        print ('%s in district %s voted %d times against the environment.' % (
            vote.legislator_name, vote.district_shortcode, vote.num_votes))

        asthma_count = self.session.query(DistrictAsthmaCounts.district_shortcode,
                                          DistrictAsthmaCounts.num_children).\
                                    filter_by(district_shortcode='MA-SS-5').\
                                    first()

        print ('{:,} children in district {} have asthma.'.format(
            asthma_count.num_children, asthma_count.district_shortcode))

        district_poll = self.session.query(DistrictPoll.district_shortcode,
                                           DistrictPoll.avg_percent_worried).\
                                     filter_by(district_shortcode='VA-SS-1').\
                                     first()

        print ('%.2f%% of people in district %s are worried about climate change.' %
            (district_poll.avg_percent_worried, district_poll.district_shortcode))


db = EnvironmentPapersDatabase()
