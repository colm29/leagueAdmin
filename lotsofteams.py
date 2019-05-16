from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Division, Base, Team

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


# teams for Premier League North
division1 = Division(name="Premier League North", rank = 1)

session.add(division1)
session.commit()

team1 = Team(name="Celtic Park FC", nickname="The Hoops",
                     membership=200.00, email = 'colm29@gmail.com', division=division1)

session.add(team1)
session.commit()


team1 = Team(name="Trinity Donaghmede", nickname="The Layabouts",
                     membership=110, email = 'trindon@anymail.com', division=division1)

session.add(team1)
session.commit()

team1 = Team(name="Swords Celtic 35s", nickname="The Mad Dogs",
                     membership=210.00, email = 'colm29@gmail.com', division=division1)

session.add(team1)
session.commit()



print "added teams!"
