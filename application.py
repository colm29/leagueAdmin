#!/usr/bin/env python2
import pdb
from flask import Flask, render_template, url_for, flash, jsonify, request, redirect,  make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Division, Team, User
import httplib2
import requests
import json
import random
import string

app = Flask(__name__)

FBCLIENT_ID = json.loads(
    open('fbclientsecrets.json', 'r').read())['web']['app_id']

engine = create_engine('sqlite:///leagueAdmin.db')
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

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html')

@app.route('/fbconnect', methods =['POST'])
def fbconnect():
    """ if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response """
    
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fbclientsecrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fbclientsecrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.3/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v3.3/me?access_token=%s&fields=name,id,email' % token
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
    url = 'https://graph.facebook.com/v3.3/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session) 
    login_session['user_id'] = user_id 

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/division/<int:division_id>')
@app.route('/division/<int:division_id>/teams')
def showTeams(division_id):
    try:
        session = newSession()
        teams = session.query(Team).filter_by(division_id = division_id)
        if loggedIn():
            return render_template('teams.html', teams = teams, division_id = division_id)
        else:
            return render_template('publicTeams.html', teams = teams, division_id = division_id)
    except Exception as e:
        return e.__doc__
    finally:
        session.close()

""" @app.route('/division/<int:division_id>')
@app.route('/division/<int:division_id>/teams')
def showTeams(division_id):
    session = newSession()
    teams = session.query(Team).filter_by(division_id = division_id)
    return render_template('teams.html', teams = teams, division_id = division_id)
    session.close() """

def loggedIn():
    if login_session.get('user_id') is None:
        return False
    else:
        return True

@app.route('/division/<int:division_id>/teams/<int:team_id>/teamDetails')
def showTeamDetails(division_id, team_id):
    session = newSession()
    team = session.query(Team).filter_by(id = team_id).one()
    if loggedIn():
        if login_session['user_id'] == team.user_id:
            return render_template('teamDetails.html', team = team)
        else:
            return render_template('publicTeamDetails.html', team = team)
    else:
        return render_template('publicTeamDetails.html', team = team)


@app.route('/division/<int:division_id>/teams/new', methods = ['GET', 'POST'])
def newTeam(division_id):
    try:
        session = newSession()
        if request.method == 'POST':
            team = Team(name = request.form['name'], nickname = request.form['nickname'], membership = request.form['membership'], email = request.form['email'], division_id = division_id, user_id = login_session['user_id'])
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
        if team.user_id != login_session['user_id']:
            return "<script>function myFunction() {alert('You are not authorised to edit this team.  Please create your own team in order to edit.');}</script><body onload='myFunction()''>"
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
        if team.user_id != login_session['user_id']:
            return "<script>function myFunction() {alert('You are not authorised to delete this team.  Please create your own team in order to delete.');}</script><body onload='myFunction()''>"
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

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        """ if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token'] """
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['""" user_id """']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showDivisions'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showDivisions'))


#user functions
def getUserID(email):
    try:
        session = newSession()
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None
    finally:
        session.close()

def getUserInfo(user_id):
    try:
        session = newSession()
        user = session.query(User).filter_by(id = user_id).one()
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


def createUser(login_session):
    session = newSession()
    newUser = User(name = login_session['username'], email = 
        login_session['email'], picture = login_session
            ['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session
        ['email']).one()
    return user.id



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
