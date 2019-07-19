#usr/bin/python3
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    email = Column(String(80), nullable = False)
    picture = Column(String(80), nullable = False)

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
    email = Column(String(80))
    home_id = Column(Integer, ForeignKey('home.id'))
    home = relationship(Home)
    division_id = Column(Integer, ForeignKey('division.id'))
    division = relationship(Division)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'home': self.home,
            'description': self.description
        }

class Home(Base):
    __tablename__ = 'home'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    address = Column(String(300))
    lat = Column(Float)
    lon = Column(Float)

class Referee(Base):
    __tablename__ = 'referee'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    phone = Column(String(300))


#########insert at end of file ##########

engine = create_engine('postgresql://colm:colm@localhost/league')

Base.metadata.create_all(engine)
