from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from models.daily_kos import State, District, CountyFragment, DistrictType
from models.polling import CountyPoll
from models.asthma import CountyAsthmaCounts
