from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import *
from app.models import Base
from app.config import SQLITE
from app.asthma import create_district_astham_counts
from app.polling import create_district_polls
from app.create_tables import (create_daily_kos,
                               create_polling,
                               create_asthma,
                               create_voting)

class EnvironmentPapersDatabase:
    db_engine = None

    def __init__(self):
        self.db_engine = create_engine(SQLITE)
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def create_tables(self):
        # Base.metadata.drop_all(self.db_engine)
        Base.metadata.create_all(self.db_engine)
        # create_daily_kos(self.session)
        create_polling(self.session)
        create_asthma(self.session)
        create_voting(self.session)
        print("Basic tables created")

    def create_district_data(self):
        create_district_astham_counts(self.session)
        create_district_polls(self.session)
        print("District tables created")


db = EnvironmentPapersDatabase()
