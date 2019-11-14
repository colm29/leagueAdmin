import requests
import random
import string
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import render_template, url_for, flash, request, redirect,  make_response, session as login_session

from leagueAdmin.db_setup import Base, Comp, Team, Home
from .services import newSession, loggedIn, createUser, updateUser, getUserID
from leagueAdmin import app
from . import config

# Route for initial page - show all categories(Divisions in Football League)
@app.route('/')
@app.route('/comps')
def showDivisions():
    try:
        session = newSession()  # creates a new session
        comps = session.query(Comp).order_by(Comp.rank).all()
        return render_template('comps.html', comps=comps)
    finally:
        session.close()  # closes new session to avoid error about objects
        # created in a thread can only be used in that same thread


# Function to show all teams (items) in a Comp
@app.route('/comp/<path:comp_name>')
@app.route('/comp/<path:comp_name>/teams')
def showTeams(comp_name):
    try:
        session = newSession()
        comp = session.query(Comp).filter_by(name=comp_name).one()
        teams = session.query(Team).filter_by(comp_id=comp.id)
        comps = session.query(Comp).order_by(Comp.rank).all()
        if loggedIn():  # can create a new team if logged in
            return render_template('teams.html', teams=teams,
                                   comp=comp, comps=comps)
        else:
            return render_template('publicTeams.html', teams=teams,
                                   comp=comp, comps=comps)
    finally:
        session.close()


# Function to show selected team details
@app.route('/comp/<path:comp_name>/teams/<path:team_name>/teamDetails')
def showTeamDetails(comp_name, team_name):
    session = newSession()
    team = session.query(Team).filter_by(name=team_name).one()
    home = session.query(Home).filter_by(id=team.home_id).one()
    if login_session.get('user_id') == team.user_id:
        # can edit/delete
        #     else:depending on auth
        return render_template('teamDetails.html',
                               team=team, comp_name=comp_name, home=home)
    return render_template('publicTeamDetails.html',
                           team=team, comp_name=comp_name, home=home)


# Function to add new team - any logged in user can do this
@app.route('/comp/<path:comp_name>/teams/new', methods=['GET', 'POST'])
def newTeam(comp_name):
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
                        comp_id=request.form['comp'],
                        user_id=login_session['user_id'])
            session.add(team)
            session.commit()
            flash('New Team Added!')
            comp = session.query(Comp) \
                .filter_by(id=request.form['comp']).one()
            return redirect(url_for('showTeams', comp_name=comp.name))
        else:
            comps = session.query(Comp).order_by(Comp.rank).all()
            return render_template('newTeam.html',
                                   comp_name=comp_name,
                                   comps=comps)
    finally:
        session.close()


# Function to edit team - only available to user who created team
@app.route('/comp/<path:comp_name>/teams/<path:team_name>/edit',
           methods=['POST', 'GET'])
def editTeam(comp_name, team_name):
    try:
        session = newSession()
        comp = session.query(Comp).filter_by(name=comp_name).one()
        comps = session.query(Comp).order_by(Comp.rank).all()
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
            if request.form['comp']:
                team.comp_id = request.form['comp']
            session.add(team)
            session.commit()
            flash('Team Updated!')
            return redirect(url_for('showTeams', comp_name=comp_name))
        else:
            return render_template('editTeam.html', comp=comp,
                                   comps=comps, team=team)
    finally:
        session.close()


# Function to delete team - only available to user who created team
@app.route('/comp/<path:comp_name>/teams/<path:team_name>/delete',
           methods=['POST', 'GET'])
def deleteTeam(comp_name, team_name):
    try:
        session = newSession()
        comp = session.query(Comp).filter_by(name=comp_name).one()
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
            return redirect(url_for('showTeams', comp_name=comp_name))
        else:
            return render_template('deleteTeam.html',
                                   comp=comp, team=team)
    finally:
        session.close()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, fbclient_id=config.FB_ID)


'''facebook token exchange function - if successful
populates login_session with user details'''


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print("access token received %s ") % access_token

    url = 'https://graph.facebook.com/oauth/access_token'
    params = {'grant_type': 'fb_exchange_token',
              'client_id': config.FB_ID,
              'client_secret': config.FB_SECRET,
              'fb_exchange_token': access_token}
    response = requests.get(url, params=params)
    result = response.json()[1]

    # Use token to get user info from API
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first
        index which gives us the key : value for the server access token
        then we split it on colons to pull out the actual token value and
        replace the remaining quotes with nothing so that it can be used
        directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v3.3/me'
    params = {'access_token': 'token',
              'fields': 'name,id,email'}
    response = requests.get(url, params=params)
    result = response.json()[1]
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
    url = 'https://graph.facebook.com/v3.3/me/picture'
    params = {'access_token': token,
              'redirect': '0',
              'height': '200',
              'width': '200'}
    result = requests.get(url)[1]
    data = result.json()[1]

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
    output += ' " style = "width: 200px; height: 200px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = f'https://graph.facebook.com/{facebook_id}/permissions'
    params = {'access_token': access_token}
    requests.get(url, params=params)[1]
    return "you have been logged out"


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
