# League Admin App
This app was designed for administrators and users of an Amateur football league based in Dublin, Ireland.  There are four ranked divisions and in each division are a selection of teams.  Teams can be added and updated depending on authorisation.  Authentication is provided using facebook login.

## Running the app
1. install vagrant virtual machine and `cd` to the vagrant directory from the command line
2. copy the following files to a new folder called catalog in the vagrant directory:
  * application.py
  * db_setup.py
  * fbclientsecrets.json
  * league.db
3. run `vagrant up` to run the virtual machine
4. run `vagrant ssh`
5. `cd /vagrant/catalog` from the vagrant virtual machine
6. from here `python application.py` to run the program
7. In a browser window, open http://localhost:8000

## Divisions
There are four Divisions in the league ranked from the top in terms of quality of teams:
* Premier Division North
* Division 1 North
* Division 2 North
* Division 3 North

## Teams
Each Division has a number of teams.  These can be seen by clicking on the division on the main screen.  More details about each team can then be viewed by clicking on the team.  To return to the main screen at any time, click on the main title header or on the back/ cancel buttons pertaining to the current screen.

## Authentication
Authentication is provided by facebook.  Click on the login button on the top right of the navigation bar.  Logged in users can create a new team in any division by cicking on the green _Add New Team_ button when viewing Division details.

## Alter / Delete teams
The creator of a team is authorised to edit details of a team or even delete the team from the team details screen.

### The Future?
Referee lists, League tables, Weekly Fixtures, Results.  Watch this space :sunglasses: :soccer:
