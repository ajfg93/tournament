import sys
from sqlalchemy import Column, Integer, Enum

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer, primary_key = True)
	gender = Column(Enum("M", "F"), nullable = False)


####insert at the end of tile#####

engine = create_engine('sqlite:///test.db')

Base.metadata.create_all(engine)