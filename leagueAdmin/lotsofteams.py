from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from leagueAdmin.models import Comp, Base, Team, AppUser, Day, Section, Season, Referee, Home, Surface

engine = create_engine('postgresql://colm:colm@localhost/league')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

season1 = Season(name='2020', start = '2020-04-01', end = '2020-11-30')
session.add(season1)
session.commit()

sec1 = Section(name='North')
session.add(sec1)
session.commit()

ref1 = Referee(name='John Murphy', phone='087 1111111')
session.add(ref1)
ref2 = Referee(name='Eddie Murphy', phone='087 2222222')
session.add(ref2)
ref3= Referee(name='Tommy Murphy', phone='087 3333333')
session.add(ref3)
session.commit()

user1 = AppUser(name='Colm Faherty', email='colm29@gmail.com', picture='colm.png')
session.add(user1)
session.commit()

user2 = AppUser(name='Someone Else', email='someoneelse@someothermail.com', picture='anotherpic.png')
session.add(user2)
session.commit()

user3 = AppUser(name='Seamas Doe', email='seamasdoe@smtp.com', picture='sheamie.png')
session.add(user3)
session.commit()

user4 = AppUser(name='Alex Faherty', email='oreolover@address.ie', picture='lexxie.jpg')

session.add(user4)
session.commit()

sec1 = Section(name='North')
session.add(sec1)
session.commit()

day1 = Day(name='Monday')
session.add(day1)
day2 = Day(name='Tuesday')
session.add(day2)
day3 = Day(name='Wednesday')
session.add(day3)
day4 = Day(name='Thursday')
session.add(day4)
day5 = Day(name='Friday')
session.add(day5)
day6 = Day(name='Saturday')
session.add(day6)
day7 = Day(name='Sunday')
session.add(day7)
session.commit()

# teams for Premier League North
division1 = Comp(name="Premier Division North", rank=1, day=day6, section=sec1)

session.add(division1)
session.commit()

division2 = Comp(name="Division 1 North", rank=2, day=day6, section=sec1)

session.add(division2)
session.commit()

division3 = Comp(name="Division 2 North", rank=3, day=day6, section=sec1)

session.add(division1)
session.commit()

division4 = Comp(name="Division 3 North", rank=4, day=day6, section=sec1)

session.add(division1)
session.commit()

surf1 = Surface(name='Grass')
surf2 = Surface(name='Astro Turf')
session.add(surf1)
session.add(surf2)
session.commit()

home1 = Home(name='Beaumont Convent', address='Dublin 9', surface=surf1)
session.add(home1)
home2 = Home(name='Fr. Collins Park', address='Donaghmede', surface=surf1)
session.add(home2)
home3 = Home(name='Athletic Park', address='Swords', surface=surf1)
session.add(home3)
home4 = Home(name='St Annes Park', address='Raheny', surface=surf1)
session.add(home4)
session.commit()


team1 = Team(name="Celtic Park FC", email='colm29@gmail.com', home=home1, comp=division3, appuser=user1)

session.add(team1)
session.commit()


team1 = Team(name="Trinity Donaghmede B", email='trindon@anymail.com', home=home2, comp=division3, appuser=user2)

session.add(team1)
session.commit()

team1 = Team(name="Swords Celtic 35s", email='sc@swordsvillage.ie', home=home3, comp=division3, appuser=user2)

session.add(team1)
session.commit()

team1 = Team(name="Marino Athletic",  email='mafc@amailserver.com', home=home4, comp=division3, appuser=user2)

session.add(team1)
session.commit()

print("added teams!")
