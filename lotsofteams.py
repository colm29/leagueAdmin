from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Division, Base, Team, User

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
division1 = Comp(name="Premier Division North", rank = 1)

session.add(division1)
session.commit()

division2 = Comp(name="Division 1 North", rank = 2)

session.add(division1)
session.commit()

division3 = Comp(name="Division 2 North", rank = 3)

session.add(division1)
session.commit()

division4 = Comp(name="Division 3 North", rank = 4)

session.add(division1)
session.commit()

home1 = Home(name = 'Beaumont Convent', address = 'Dublin 9')
session.add(home1)
home2 = Home(name = 'Fr. Collins Park', address = 'Donaghmede')
session.add(home2)
home3 = Home(name = 'Athletic Park', address = 'Swords')
session.add(home3)
session.commit()


team1 = Team(name="Celtic Park FC", email = 'colm29@gmail.com', home_id = home1, comp_id = division3, user = user1)

session.add(team1)
session.commit()


team1 = Team(name="Trinity Donaghmede B", email = 'trindon@anymail.com', home = home2, division=division3, user = user2)

session.add(team1)
session.commit()

team1 = Team(name="Swords Celtic 35s", nickname="The Mad Dogs",
                     membership=210.00, email = 'sc@swordsvillage.ie', division=division3, user = user2, home = '', description = 'Playing in green and black vertical stripes, this North county Dublin team\'s form is as predictable as the March weather, veering from the sublime to the ridiculous from minute one to ninety.')

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

team1 = Team(name="Trinity Donaghmede", nickname="The Layabouts",
                     membership=110, email = 'trindon@anymail.com', division=division1, user = user2, home = 'Fr. Collins Park, Donaghmede', description = 'Originally founded by escaped convicts in 1964,  many of the current crop of players are direct descendents from its founding fathers, and have the disciplinary records to prove it.  Play in black and red vertical stripes.  The A team are the better version of the B team who play in the Second Division.')

session.add(team1)
session.commit()

team1 = Team(name="Peamount 35s", nickname="The Worldies",
                     membership=175, email = 'pmount@gmail.com', division=division1, user = user3, home = 'Vegetable Patch Park, Cherrywood', description = 'This club was made famous by Stephanie Roche, who scored a goal that came second in the FIFA goal of the year contest.  Its over 35 team don\'t score as great a goal as that in general, but are a competitive outfit, normally finishing in the upper echelons of the Premier Division.')

session.add(team1)
session.commit()

team1 = Team(name="Real Transylvania", nickname="The Vampires",
                     membership=250, email = 'bram@gmail.com', division=division1, user = user4, home = 'The Cave, Ballyfermot', description = 'The vampires play an exciting brand of football, with the emphasis on attack, which is good as their defence has an average age of 50.')

session.add(team1)
session.commit()

team1 = Team(name="Cherry Orchard FC", nickname="The Cherries",
                     membership=290, email = 'cofc@gmail.com', division=division1, user = user1, home = 'Cherry Orchard Park, Dublin 10', description = 'This established club hail from West Dublin and have had many successes over the years.  Currently Premier Division North Champions.')

session.add(team1)
session.commit()

team1 = Team(name="Portmarnock AFC", nickname="The Beachcombers",
                     membership=205, email = 'pafc@hotmail.com', division=division1, user = user4, home = 'Westside Park, Portmarnock', description = 'A team that yo-yo up and down between the Premier division and Division 1 like the waves of the nearby beach.')

session.add(team1)
session.commit()

team1 = Team(name="St Anthonys Kilcoole", nickname="The Saints",
                     membership=235, email = 'saints@eircom.net', division=division1, user = user1, home = 'Kilcoole Park', description = 'West county Dublin team St Anthonys have recently benefitted from an influx of people moving to the area as a cheaper alternative to Dublin city.  The team has benefitted and in 2018 got promoted from Division 1 North.')

session.add(team1)
session.commit()

team1 = Team(name="Bluebell United", nickname="The Bells",
                     membership=168, email = 'bbutd@eircom.net', division=division1, user = user2, home = 'Blackhorse Park', description = 'A traditional footballing powerhouse, the Bells have recently not been performing as well as in previous years due to lack of investment.')

session.add(team1)
session.commit()

team1 = Team(name="Patrician Celtic", nickname="The Celts",
                     membership=195, email = 'pcelt@mailhub.net', division=division2, user = user4, home = 'Patrician Road, Kilbarrack', description = 'Another Northside seaside club, Patrician Celtic have been the top scorers in DIvision 1 North for the last three seasons.  However their defence has more holes than a wedge of swiss cheese so the chances of promotion are slim.')

session.add(team1)
session.commit()


team1 = Team(name="Griffith Rovers", nickname="The Warriors",
                     membership=100, email = 'griffith@gmail.com', division=division2, user = user1, home = 'Johnstown Road, Finglas', description = 'The self proclaimed warriors are labelled by many as the dirtiest team in the league.  The statistics bear this out as they racked up 50 yellow cards and 4 reds in 2018.')

session.add(team1)
session.commit()

team1 = Team(name="Greenfield Park FC", nickname="The Green Machine",
                     membership=249, email = 'greenmachine@hotmail.com', division=division2, user = user3, home = 'Stella Maris Astro Pitch, Dublin 3', description = 'Greenfield normally play with a 4-4-2 formation.  A national lottery payment to the club in 2017 paid for a new clubhouse and kit.  The previous kit had been worn for twenty years straight so it was much needed.')

session.add(team1)
session.commit()

team1 = Team(name="Balbriggan FC", nickname="The Blues",
                     membership=110, email = 'balbriggan@gmail.com', division=division2, user = user3, home = 'Pear Tree Park', description = 'Balbriggan is a one club town so competition for places is high.  A quality team who are going places, were the words of a recent opposion manager after being beaten 5-0.')

session.add(team1)
session.commit()

team1 = Team(name="Broombridge FC", nickname="The Train Robbers",
                     membership=145, email = 'broombridge@hotmail.com', division=division2, user = user1, home = 'Navan Road, Dublin 7', description = 'Broombridge hail from the neighbourhood of Cabra in north Dublin city.  The play in black and white vertical stripes.')

session.add(team1)
session.commit()

team1 = Team(name="Glebe North", nickname="The Canaries",
                     membership=180, email = 'canaries@gmail.com', division=division2, user = user1, home = 'Glebe North Regional Park', description = 'Plying their trade in a green and yellow kit, the canaries certainly don\'t play an exciting brand of football.  Exponents of the hoofball brand of football, their game is about strength and not the finer parts of the game.  Utilizing a 6ft 7inch centre forward, it has worked, despite the criticisms.')

session.add(team1)
session.commit()

team1 = Team(name="Marino Athletic", nickname="The Dockers",
                     membership=220, email = 'mafc@amailserver.com', division=division3, user = user2, home = 'St Annes Park, Raheny', description = 'Marino concentrate the core of their skilled players in central positions so can be difficult to play on their day.  However some teams have gotten good results against them by utilising the space on the wings.  Playing in dark blue, they are a solid Division 2 outfit and will be hoping to be in the promotion places this year.')

session.add(team1)
session.commit()


team1 = Team(name="Elm Mount FC 35s", nickname="The Elmers",
                     membership=240, email = 'mafc@amailserver.com', division=division3, user = user2, home = 'AUL Sports Complex', description = 'A team from the Beaumont / Artane suburb in Dublin city, Elm Mounts biggest claim to fame is having senior Dublin county GAA goalkeeper Stephen Cluxton playing as one of their defenders.')

session.add(team1)
session.commit()


team1 = Team(name="Mountview CFC", nickname="The Magpies",
                     membership=200, email = 'mvcfc@gmail.com', division=division3, user = user2, home = 'Clongriffin Park, Dublin 13', description = 'Mountview CFC were founded and first managed by the late Jim Jeffers in 2001.  Jim is still managing them, and is still late turning up to most of the games, leaving captain Billy Murphy to do most of the pre game team talks.')

session.add(team1)
session.commit()

team1 = Team(name="Hartstown / Huntstown", nickname="Double H",
                     membership=190, email = 'hh@anemailserver.ie', division=division3, user = user2, home = 'Hartstown Park, Blanchardstown', description = 'This club are the result of a merger between two clubs in the Blanchardstown area.  Some say it was for financial reasons, others say pooled resources would make a better fist of chasing glory.')

session.add(team1)
session.commit()

team1 = Team(name="Ashbourne United", nickname="The Meathmen",
                     membership=150, email = 'ashbfch@eircom.net', division=division3, user = user1, home = 'Archerstown Road, Ashbourne', description = 'This is the only club from county Meath in the AFL over 35s league, and they are proud of their role as outsiders, upsetting the Dublin teams who come to Archerstown Park.  Unfortunately, in recent years, most of the visiting teams have left Archerstown Park happy and with all three points in the bag.')

session.add(team1)
session.commit()

team1 = Team(name="Skerries Town", nickname="The Millers",
                     membership=100, email = 'millersh@aflserver.net', division=division4, user = user3, home = 'Park Lane, Skerries', description = 'Hailing from the pleasant coatal town of Skerries, this is a decent team, playing their games at Park Lane under the shadow of a large historic windmill.  Visiting teams complain in the summer months that the surface of the pitch is harder than concrete.  Their groundsman refused to comment.')

session.add(team1)
session.commit()

team1 = Team(name="Stoneybatter Athletic", nickname="The Lawyers",
                     membership=200, email = 'stoneybafc@aflserver.net', division=division4, user = user1, home = 'Law Society of Ireland, Dublin 7', description = 'This team rent the playing facilities from the Law Society of Ireland, and most visting teams like playing in these picuresque surroundings.  Finished 3rd in 2018 which was their best finish ever.')

session.add(team1)
session.commit()

team1 = Team(name="Vianney Boys FC", nickname="The Foxes",
                     membership=180, email = 'stoneybafc@aflserver.net', division=division4, user = user1, home = 'Kilmore Drive, Dublin 5', description = 'Vianney Boys FC was founded by John Vianney in 1971 in the coolock suburb of North Dublin.  Opposition teams have recently complained about the team living up to its nickname by fouling oppsition players behind the referees back.  Not true said Vianney coach Mick O\' Sullivan when local press questioned him.')

session.add(team1)
session.commit()

team1 = Team(name="Rivervalley Rangers", nickname="Rangers",
                     membership=210, email = 'rvrfc@gmail.com', division=division4, user = user1, home = 'Ridgewood Park, Swords', description = 'Rivervalley Rangers FC is a north county Dublin soccer football club based in Swords. The football club was formed in 1981. Starting out with one senior team and one schoolboys team Rivervalley Rangers grew rapidly, particularly the schoolboys section. Currently the club boasts 19 teams.')

session.add(team1)
session.commit()


team1 = Team(name="Malahide United", nickname="The Fishermen",
                     membership=270, email = 'malahideutdfc@gmail.com', division=division4, user = user1, home = 'Gannon Park, Coast Road', description = 'Malahide United FC is North County Dublin soccer football club. The club was formed in 1944 and after a brief lapse it was re-formed in 1971. Malahide United is one of Ireland\'s largest clubs.')

session.add(team1)
session.commit()




print "added teams!"
