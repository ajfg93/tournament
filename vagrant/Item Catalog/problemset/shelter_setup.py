import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'

	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	address = Column(String, nullable = False)
	city = Column(String, nullable = False)
	state = Column(String, nullable = False)
	zipCode = Column(Integer, nullable = True)
	website = Column(String, nullable = True)
	
class Puppy(Base):
	__tablename__ = 'puppy'

	id = Column(Integer, primary_key = True)
	date_of_birth = Column(Date, nullable = False)
	gender = Column(Enum("F","M"), nullable = False)
	weight = Column(Integer, nullable =False)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))

	shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)