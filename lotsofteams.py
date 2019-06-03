from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Division, Base, Team, User

engine = create_engine('sqlite:///league.db')
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

user1 = User(name = 'Colm Faherty', email = 'colm29@gmail.com', picture = 'colm.png')

session.add(user1)
session.commit()

user2 = User(name = 'Someone Else', email = 'someoneelse@someothermail.com', picture = 'anotherpic.png')

user3 = User(name = 'Seamas Doe', email = 'seamasdoe@smtp.com', picture = 'sheamie.png')

session.add(user3)
session.commit()

user4 = User(name = 'Alex Faherty', email = 'oreolover@address.ie', picture = 'lexxie.jpg')

session.add(user4)
session.commit()


# teams for Premier League North
division1 = Division(name="Premier League North", rank = 1)

session.add(division1)
session.commit()

division2 = Division(name="Division 1 North", rank = 2)

session.add(division1)
session.commit()

division3 = Division(name="Division 2 North", rank = 3)

session.add(division1)
session.commit()

division4 = Division(name="Division 3 North", rank = 4)

session.add(division1)
session.commit()

team1 = Team(name="Celtic Park FC", nickname="The Park",
                     membership=200.00, email = 'colm29@gmail.com', division=division3, user = user1, home = 'Beaumont Convent, Dublin 9', description = 'Founded in 1953, Celtic Park Football club have a rich history in the nothside Dublin suburb of Beaumont.  They also boast the eldest player in the league, Aidan Lynch - still plying his trade at the tender young age of 69 this year.  Most of his appearances these days are off the bench, but he still pops up with an important goal from time to time.')

session.add(team1)
session.commit()


team1 = Team(name="Trinity Donaghmede", nickname="The Layabouts",
                     membership=110, email = 'trindon@anymail.com', division=division3, user = user2, home = 'Fr. Collins Park, Donaghmede', description = 'Originally founded by escaped convicts in 1964,  many of the current crop of players are direct descendents from its founding fathers, and have the disciplinary records to prove it.  Play in black and red vertical stripes.')

session.add(team1)
session.commit()

team1 = Team(name="Swords Celtic 35s", nickname="The Mad Dogs",
                     membership=210.00, email = 'sc@swordsvillage.ie', division=division3, user = user2, home = 'Athletic Park, Swords', description = 'Playing in green and black vertical stripes, this North county Dublin team\'s form is as predictable as the March weather, veering from the sublime to the ridiculous from minute one to ninety.')

session.add(team1)
session.commit()

team1 = Team(name="Sandyhill / Shangan", nickname="The Indecisives",
                     membership=152.00, email = 'sandyhill@ballymunemailservers.ie', division=division1, user = user2, home = 'Belclare Road, Ballymun', description = 'This team is the result of a merger between two strong teams in 2010 who couldn\'t pay the pitch rental bill, and so joined forces.  They couldn\'t decide what to call the new team so left the two previous names as they were.')

session.add(team1)
session.commit()

team1 = Team(name="Raheny United", nickname="United",
                     membership=225.00, email = 'rahenyfc@anemailaddress.ie', division=division2, user = user1, home = 'Raheny Park', description = 'A team that play near the beach but who play with the determination of a team who are certainly not on their holidays.  A new chairman played around with the idea of renaming them \'The Seagulls\' in 2015 but the fanbase revolted and put an end to that idea.  Both fans are often still seen cheering on their team.')

session.add(team1)
session.commit()

team1 = Team(name="Dunshaughlin Youths", nickname="The Royals",
                     membership=195.00, email = 'dunshaughliny@eircom.ie', division=division4, user = user4, home = 'Dunshaughlin Park', description = 'A team founded by youths in the early nineties, most of the founding fathers are now actual fathers in their forties.')

session.add(team1)
session.commit()

team1 = Team(name="Chanel SSC", nickname="The Challengers",
                     membership=170.00, email = 'chanelcoolock@eircom.net', division=division4, user = user4, home = 'St Anne\'sPark', description = 'Consistently the worst team in the league for the last few years, this Coolock outfit are usually there to make up the numbers and sit at the bottom of Division 3 North from week 2 to 20.  They sit near the top of the league in week one as it is ranked alphabetically.')

session.add(team1)
session.commit()




print "added teams!"
