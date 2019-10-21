from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from .daily_kos import *
from .polling import *
from .asthma import *
from .voting import *
from .jobs import *
