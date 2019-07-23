#usr/bin/python3
import sys
import psycopg2
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,func, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key = True)
    name = Column(String, default = str(func.year()), nullable = False)
    start = Column(DateTime)
    end = Column(DateTime)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    email = Column(String(80), nullable = False)
    picture = Column(String(80))

class Section(Base):
    __tablename__ = 'section'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)

class Comp(Base):
    __tablename__ = 'comp'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    rank = Column(Integer, nullable = False)
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship(Section)
    cup = Column(Boolean, nullable = False)
    day_id = Column(Integer, ForeignKey('day.id'))
    day = relationship(Day)
    
class Home(Base):
    __tablename__ = 'home'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    address = Column(String(300))
    lat = Column(Float)
    lon = Column(Float)

class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80))
    home_id = Column(Integer, ForeignKey('home.id'), nullable = False)
    home = relationship(Home)
    comp_id = Column(Integer, ForeignKey('comp.id'))
    comp = relationship(Comp)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Referee(Base):
    __tablename__ = 'referee'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    phone = Column(String(15), nullable = False)

class NewsItem(Base):
    __tablename__ = 'newsItem'
    id = Column(Integer, primary_key = True)
    message = Column(String(500), nullable = False)
    createdOn = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    createdBy = Column(Integer, ForeignKey('user.id'), nullable = False)
    user1 = relationship(User, foreign_keys='NewsItem.createdBy')
    updatedOn = Column(DateTime)
    updatedBy = Column(Integer, ForeignKey('user.id'))
    user2 = relationship(User,  foreign_keys='NewsItem.updatedBy')

class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key = True)
    comp_id = Column(Integer, ForeignKey('comp.id'), nullable = False)
    comp = relationship(Comp)
    homeTeam = Column(Integer, ForeignKey('team.id'), nullable = False)
    team1 = relationship(Team, foreign_keys='Match.homeTeam')
    awayTeam = Column(Integer, ForeignKey('team.id'), nullable = False)
    team2 = relationship(Team ,foreign_keys='Match.awayTeam')
    homeScore = Column(Integer)
    awayScore = Column(Integer)
    home_id = Column(Integer, ForeignKey('home.id'), nullable = False)
    home = relationship(Home)
    referee_id = Column(Integer, ForeignKey('referee.id'), nullable = False)
    referee = relationship(Referee)
    createdOn = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)
    createdBy = Column(Integer, ForeignKey('user.id'), nullable = False)
    user1 = relationship(User, foreign_keys='Match.createdBy')
    updatedOn = Column(DateTime)
    updatedBy = Column(Integer, ForeignKey('user.id'))
    user2 = relationship(User, foreign_keys='Match.updatedBy')

#########insert at end of file ##########

engine = create_engine('postgresql://colm:colm@localhost/league')

Base.metadata.create_all(engine)
