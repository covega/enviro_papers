from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from scripts import create_daily_kos, create_polling, create_asthma
import os, os.path

DATA_DIR = os.path.join(os.getcwd(), 'data/')
SQLITE = 'sqlite:///papers.db' # on-disk
# SQLITE = 'sqlite://' # in-memory

class EnvironmentPapersDatabase:
    db_engine = None

    def __init__(self):
        self.db_engine = create_engine(SQLITE)
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def create_tables(self):
        try:
            Base.metadata.drop_all(self.db_engine)
            Base.metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

db = EnvironmentPapersDatabase()

from models import *

if __name__ == '__main__':
    # db.create_tables()
    # create_daily_kos(db.session)
    # create_polling(db.session)
    Base.metadata.create_all(db.db_engine)
    create_asthma(db.session)
