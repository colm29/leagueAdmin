from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Division, Base, Team, User

engine = create_engine('sqlite:///leagueAdmin.db')
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

session.add(user2)
session.commit()


# teams for Premier League North
division1 = Division(name="Premier League North", rank = 1)

session.add(division1)
session.commit()

team1 = Team(name="Celtic Park FC", nickname="The Hoops",
                     membership=200.00, email = 'colm29@gmail.com', division=division1, user = user1)

session.add(team1)
session.commit()


team1 = Team(name="Trinity Donaghmede", nickname="The Layabouts",
                     membership=110, email = 'trindon@anymail.com', division=division1, user = user2)

session.add(team1)
session.commit()

team1 = Team(name="Swords Celtic 35s", nickname="The Mad Dogs",
                     membership=210.00, email = 'colm29@gmail.com', division=division1, user = user2)

session.add(team1)
session.commit()



print "added teams!"
