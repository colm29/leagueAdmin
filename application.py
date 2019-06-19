#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import pdb
from flask import Flask, render_template, url_for, flash, jsonify, \
    request, redirect,  make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Division, Team, User
import httplib2
import requests
import json
import random
import string

app = Flask(__name__)

FB_ID = json.loads(
    open('fbclientsecrets.json', 'r').read())['web']['app_id']

FB_SECRET = json.loads(
        open('fbclientsecrets.json', 'r').read())['web']['app_secret']

engine = create_engine('sqlite:///league.db')
Base.metadata.bind = engine


def newSession():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


# API Endpoints
@app.route('/divisions/JSON')
def divisionsJSON():
    try:
        session = newSession()
        divisions = session.query(Division).order_by(Division.rank).all()
        return jsonify(Divisions=[d.serialize for d in divisions])
    finally:
        session.close()


@app.route('/divisions/<path:division_name>/teams/JSON')
def teamsJSON(division_name):
    try:
        session = newSession()
        division = session.query(Division).filter_by(name=division_name)\
            .one()
        teams = session.query(Team).filter_by(division_id=division.id)
        return jsonify(Teams=[t.serialize for t in teams])
    finally:
        session.close()


@app.route('/divisions/<path:division_name>/teams/<path:team_name>/JSON')
def teamJSON(division_name, team_name):
    try:
        session = newSession()
        division = session.query(Division).filter_by(name=division_name).one()
        team = session.query(Team).filter_by(name=team_name).one()
        return jsonify(Teams=[team.serialize])
    finally:
        session.close()

# End of JSON API Section


# Route for initial page - show all categories(Divisions in Football League)
@app.route('/')
@app.route('/divisions')
def showDivisions():
    try:
        session = newSession()  # creates a new session
        divisions = session.query(Division).order_by(Division.rank).all()
        return render_template('divisions.html', divisions=divisions)
    finally:
        session.close()  # closes new session to avoid error about objects
        # created in a thread can only be used in that same thread


# Function to show all teams (items) in a Division
@app.route('/division/<path:division_name>')
@app.route('/division/<path:division_name>/teams')
def showTeams(division_name):
    try:
        session = newSession()
        division = session.query(Division).filter_by(name=division_name).one()
        teams = session.query(Team).filter_by(division_id=division.id)
        divisions = session.query(Division).order_by(Division.rank).all()
        if loggedIn():  # can create a new team if logged in
            return render_template('teams.html', teams=teams,
                                   division=division, divisions=divisions)
        else:
            return render_template('publicTeams.html', teams=teams,
                                   division=division, divisions=divisions)
    finally:
        session.close()


# Function to show selected team details
@app.route('/division/<path:division_name>/teams/<path:team_name>/teamDetails')
def showTeamDetails(division_name, team_name):
    session = newSession()
    team = session.query(Team).filter_by(name=team_name).one()
    if login_session.get('user_id') == team.user_id:
        # can edit/delete depending on auth
        return render_template('teamDetails.html',
                               team=team, division_name=division_name)
    else:
        return render_template('publicTeamDetails.html',
                               team=team, division_name=division_name)


# Function to add new team - any logged in user can do this
@app.route('/division/<path:division_name>/teams/new', methods=['GET', 'POST'])
def newTeam(division_name):
    try:
        session = newSession()
        if not loggedIn():
            return "<script>function myFunction() {alert('You are not authorised to create a \
                    new team.  Please log in to create a new team.')\
                        ;}</script><body onload='myFunction()''>"
        if request.method == 'POST':
            team = Team(name=request.form['name'],
                        nickname=request.form['nickname'],
                        membership=request.form['membership'],
                        email=request.form['email'],
                        home=request.form['home'],
                        description=request.form['description'],
                        division_id=request.form['division'],
                        user_id=login_session['user_id'])
            session.add(team)
            session.commit()
            flash('New Team Added!')
            division = session.query(Division) \
                .filter_by(id=request.form['division']).one()
            return redirect(url_for('showTeams', division_name=division.name))
        else:
            divisions = session.query(Division).order_by(Division.rank).all()
            return render_template('newTeam.html',
                                   division_name=division_name,
                                   divisions=divisions)
    finally:
        session.close()


# Function to edit team - only available to user who created team
@app.route('/division/<path:division_name>/teams/<path:team_name>/edit',
           methods=['POST', 'GET'])
def editTeam(division_name, team_name):
    try:
        session = newSession()
        division = session.query(Division).filter_by(name=division_name).one()
        divisions = session.query(Division).order_by(Division.rank).all()
        team = session.query(Team).filter_by(name=team_name).one()
        if team.user_id != login_session['user_id']:
            # in case of access by URL
            return "<script>function myFunction() {alert('You are not authorised to edit \
                this team.  Please create your own team in order to edit.');}\
                    </script><body onload='myFunction()''>"
        if request.method == 'POST':
            if request.form['name']:
                team.name = request.form['name']
            if request.form['nickname']:
                team.nickname = request.form['nickname']
            if request.form['membership']:
                team.membership = request.form['membership']
            if request.form['email']:
                team.email = request.form['email']
            if request.form['home']:
                team.home = request.form['home']
            if request.form['description']:
                team.description = request.form['description']
            if request.form['division']:
                team.division_id = request.form['division']
            session.add(team)
            session.commit()
            flash('Team Updated!')
            return redirect(url_for('showTeams', division_name=division_name))
        else:
            return render_template('editTeam.html', division=division,
                                   divisions=divisions, team=team)
    finally:
        session.close()


# Function to delete team - only available to user who created team
@app.route('/division/<path:division_name>/teams/<path:team_name>/delete',
           methods=['POST', 'GET'])
def deleteTeam(division_name, team_name):
    try:
        session = newSession()
        division = session.query(Division).filter_by(name=division_name).one()
        team = session.query(Team).filter_by(name=team_name).one()
        if team.user_id != login_session['user_id']:
            # in case of access by URL
            return "<script>function myFunction() {alert('You are not authorised to delete\
                 this team.  Please create your own team in order to\
                      delete.');}</script><body onload='myFunction()''>"
        if request.method == 'POST':
            session.delete(team)
            session.commit()
            flash('Team Deleted!')
            return redirect(url_for('showTeams', division_name=division_name))
        else:
            return render_template('deleteTeam.html',
                                   division=division, team=team)
    finally:
        session.close()


'''Login Page Function avoids hard coding front end
 with client codes and passes state string'''


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, fbclient_id=FB_ID)


'''facebook token exchange function - if successful
populates login_session with user details'''


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print "access token received %s " % access_token

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=\
        %s&client_secret=%s&fb_exchange_token=%s' % (
        FB_ID, FB_SECRET, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.3/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first
        index which gives us the key : value for the server access token
        then we split it on colons to pull out the actual token value and
        replace the remaining quotes with nothing so that it can be used
        directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v3.3/me?access_token=%s&\
            fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v3.3/me/picture?access_token=%s&redirect=0&height=\
        200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    # updates the username and picture for a stored user if they have changed
    updateUser(user_id)

    # Output HTML returned
    output = ''
    output += '<h3 class="card-title">Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: 150px;-webkit-\
        border-radius: 150px;-moz-border-radius: 150px;">'
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'\
        % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Function to check if user is logged in
def loggedIn():
    if login_session.get('user_id') is None:
        return False
    else:
        return True


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showDivisions'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showDivisions'))


# user functions
def getUserID(email):
    try:
        session = newSession()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
    finally:
        session.close()


def getUserInfo(user_id):
    try:
        session = newSession()
        user = session.query(User).filter_by(id=user_id).one()
        if user.picture != login_session['picture']:
            user.picture = login_session['picture']
        elif user.name != login_session['username']:
            user.name = login_session['username']
        session.add(user)
        session.commit()
        return user
    except:
        return None
    finally:
        session.close()


def updateUser(user_id):
    try:
        session = newSession()
        user = session.query(User).filter_by(id=user_id).one()
        if user.picture != login_session['picture']:
            user.picture = login_session['picture']
        elif user.name != login_session['username']:
            user.name = login_session['username']
        session.add(user)
        session.commit()
    finally:
        session.close()


def createUser(login_session):
    session = newSession()
    newUser = User(name=login_session['username'], email=login_session
                   ['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
