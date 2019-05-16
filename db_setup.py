import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Division(Base):
    __tablename__ = 'division'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    rank = Column(Integer, nullable = False)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return{
            'id': self.id,
            'name': self.name,
            'rank': self.rank
        }
    

class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    nickname = Column(String(80), nullable = True)
    membership = Column(Integer, nullable = False)
    email = Column(String(80), nullable = True)
    division_id = Column(Integer, ForeignKey('division.id'), nullable = False)
    division = relationship(Division)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return{
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname,
            'membership': self.membership,
            'email': self.email
        }


#########insert at end of file ##########

engine = create_engine('sqlite:///league.db')

Base.metadata.create_all(engine)


