#!/usr/bin/env python2
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/divisions')
def showDivisions():
    return 'This page will list all divisions in the league.'

@app.route('/division/new')
def newDivision():
    return 'This page will add a new division to the league'

@app.route('/division/<int:division_id/edit')
def editDivision(division_id):
    return 'This page will edit division %s' %division_id

@app.route('/division/<int:division_id>/delete')
def deleteDivision(division_id):
    return 'This page will delete division %s from the league' %division_id

@app.route('/division/<int:division_id>')
@app.route('division/<int:division_id/teams')
def showTeams(division_id):
    return 'This page will show all teams for division %s' %division_id

@app.route('/division/<int:division_id>/teams/new')
def newTeam(division_id):
    return 'This page will add a new team to division %s' %division_id

@app.route('/division/<int:division_id>/teams/<int:team_id>/edit')
def editTeam(team_id):
    return 'This page will allow the user to edit team %s' %team_id

@app.route('/division/<int:division_id>/teams/<int:team_id>/delete')
def deleteTeam(team_id):
    return 'This page will allow the user to delete team %s' %team_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)