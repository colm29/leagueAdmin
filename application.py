#!/usr/bin/env python2
import pdb
from flask import Flask, render_template, url_for, flash, jsonify, request, redirect
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
    try:
        session = newSession()
        division = session.query(Division).filter_by(id = division_id).one()
        teams = session.query(Team).filter_by(division_id = division)
        return jsonify(Teams = [t.serialize for t in teams])
    except:
        pass
    finally:
        session.close()

@app.route('/divisions/<int:division_id>/teams/<int:team_id>/JSON')
def teamJSON(division_id, team_id):
    try:
        session = newSession()
        division = session.query(Division).filter_by(id = division_id).one()
        team = session.query(Team).filter_by(team_id).one()
        return jsonify(Teams = [team.serialize])
    except:
        pass
    finally:
        session.close()


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



@app.route('/division/<int:division_id>')
@app.route('/division/<int:division_id>/teams')
def showTeams(division_id):
    try:
        session = newSession()
        teams = session.query(Team).filter_by(division_id = division_id)
        return render_template('teams.html', teams = teams, division_id = division_id)
    except:
        return 'There\'s been an error.. it seems.'
    finally:
        session.close()


@app.route('/division/<int:division_id>/teams/new', methods = ['GET', 'POST'])
def newTeam(division_id):
    try:
        session = newSession()
        if request.method == 'POST':
            team = Team(name = request.form['name'], nickname = request.form['nickname'], membership = request.form['membership'], email = request.form['email'], division_id = division_id)
            session.add(team)
            session.commit()
            flash('New Team Added!')
            return redirect(url_for('showTeams', division_id = division_id))
        else:
            return render_template('newTeam.html', division_id = division_id)
    except:
        return 'There has been an error...I think.'
    finally:
        session.close()

@app.route('/division/<int:division_id>/teams/<int:team_id>/edit', methods = ['POST','GET'])
def editTeam(division_id,team_id):
    try:
        session = newSession()
        division = session.query(Division).filter_by(id = division_id).one()
        team = session.query(Team).filter_by(id = team_id).one()
        if request.method == 'POST':
            if request.form['name']:
                team.name = request.form['name']
            if request.form['nickname']:
                team.nickname = request.form['nickname']
            if request.form['membership']:
                team.membership = request.form['membership']
            if request.form['email']:
                team.email = request.form['email']
            session.add(team)
            session.commit()
            flash('Team Updated!')
            return redirect(url_for('showTeams', division_id = division_id))
        else:
            return render_template('editTeam.html', division = division, team = team)
    except:
        pass
    finally:
        session.close()

@app.route('/division/<int:division_id>/teams/<int:team_id>/delete', methods = ['POST','GET'])
def deleteTeam(division_id,team_id):
    try:
        session = newSession()
        division = session.query(Division).filter_by(id = division_id).one()
        team = session.query(Team).filter_by(id = team_id).one()
        if request.method == 'POST':
            session.delete(team)
            session.commit
            flash('Team Deleted!')
        else:
            return render_template('deleteTeam.html', division = division, team = team)
    except:
        pass
    finally:
        session.close()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)