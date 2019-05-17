#!/usr/bin/env python2
from flask import Flask, render_template, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Division, Team

app = Flask(__name__)

engine = create_engine('sqlite:///league.db')
Base.metadata.bind = engine

def newSession():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

#API Endpoints
@app.route('/divisions/JSON')
def divisionsJSON():
    try:
        session = newSession()
        divisions = session.query(Division).all()
        return jsonify(Divisions = [d.serialize for d in divisions])
    except:
        pass
    finally:
        session.close()

@app.route('/divisions/<int:division_id>/teams/JSON')
def teamsJSON(division_id):
    division = session.query(Division).filter_by(id = division_id).one()
    teams = session.query(Team).filter_by(division_id = division)
    return jsonify(Teams = [t.serialize for t in teams])

@app.route('/divisions/<int:division_id>/teams/<int:team_id>/JSON')
def teamJSON(division_id, team_id):
    division = session.query(Division).filter_by(id =  	    division_id).one()
    team = session.query(Team).filter_by(team_id).one()
    return jsonify(Teams = [team.serialize])

@app.route('/')
@app.route('/divisions')
def showDivisions():
    try:
        session = newSession()
        divisions = session.query(Division).all()
        return render_template('divisions.html', divisions = divisions)
    except:
        pass
    finally:
        session.close()

@app.route('/division/new')
def newDivision():
    return render_template('newDivision.html')

@app.route('/division/<int:division_id>/edit')
def editDivision(division_id):
    return render_template('editDivision.html', division_id = division_id)

@app.route('/division/<int:division_id>/delete')
def deleteDivision(division_id):
    return render_template('deleteDivision.html', division_id = division_id)

@app.route('/division/<int:division_id>')
@app.route('/division/<int:division_id>/teams')
def showTeams(division_id):
    try:
        session = newSession()
        division = session.query(Division).filter_by(id = division_id).one()
        teams = session.query(Team).all()
        return render_template('teams.html', division = division, teams = teams)
    except:
        pass
    finally:
        session.close()

@app.route('/division/<int:division_id>/teams/new')
def newTeam(division_id):
    return render_template('newTeam.html', division_id = division_id)

@app.route('/division/<int:division_id>/teams/<int:team_id>/edit')
def editTeam(division_id,team_id):
    return render_template('editTeam.html', team_id = team_id)

@app.route('/division/<int:division_id>/teams/<int:team_id>/delete')
def deleteTeam(division_id,team_id):
    return render_template('deleteTeam.html', team_id = team_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)