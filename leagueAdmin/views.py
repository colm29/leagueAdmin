import requests
import random
import string
import json
from datetime import datetime

from flask import render_template, url_for, flash, request, redirect,  make_response, session as login_session
from sqlalchemy.orm import aliased, joinedload

from leagueAdmin.models import Comp, Team, NewsItem, Match, FixtureRound, Home
from .services import is_logged_in, create_user, update_user, get_user_id, create_fixture_round
from leagueAdmin import app, db
from . import config


@app.route('/')
@app.route('/comps')
def show_divisions_and_news():
    comps = db.session.query(Comp).order_by(Comp.rank).all()
    news = db.session.query(NewsItem).order_by(db.desc(NewsItem.created_on)).limit(10).all()
    return render_template('comps.html', comps=comps, news=news)


@app.route('/comp/<path:comp_name>')
@app.route('/comp/<path:comp_name>/teams')
def show_teams(comp_name):
    comp = db.session.query(Comp).filter_by(name=comp_name).one()
    teams = comp.teams
    comps = db.session.query(Comp).order_by(Comp.rank).all()
    if is_logged_in():  # can create a new team if logged in
        return render_template('teams.html', teams=teams, comp=comp, comps=comps)
    else:
        return render_template('public_teams.html', teams=teams, comp=comp, comps=comps)


@app.route('/comp/<path:comp_name>/teams/<path:team_name>/teamDetails')
def show_team_details(comp_name, team_name):
    team = db.session.query(Team).filter_by(name=team_name).one()
    home = team.home
    if login_session.get('user_id') == team.created_by:
        return render_template('team_details.html', team=team, comp_name=comp_name, home=home)
    return render_template('public_team_details.html', team=team, comp_name=comp_name, home=home)


@app.route('/comp/<path:comp_name>/teams/add_team', methods=['GET', 'POST'])
def add_team(comp_name):
    if not is_logged_in():
        return ('<script>function myFunction() {alert("You are not authorised to create a new team.  '
                'Please log in to create a new team.";}</script><body onload="myFunction()">')
    if request.method == 'POST':
        team = Team(name=request.form['name'],
                    email=request.form['email'],
                    home=request.form['home'],
                    created_by=login_session['user_id'])
        db.session.add(team)
        db.session.commit()
        flash('New Team Added!')
        comp = db.session.query(Comp).filter_by(id=request.form['comp']).one()
        return redirect(url_for('showTeams', comp_name=comp.name))
    else:
        comps = db.session.query(Comp).order_by(Comp.rank).all()
        return render_template('add_team.html',
                               comp_name=comp_name,
                               comps=comps)


@app.route('/comp/<path:comp_name>/teams/<path:team_name>/edit', methods=['POST', 'GET'])
def edit_team(comp_name, team_name):
    comps = db.session.query(Comp).order_by(Comp.rank).all()
    comp = comps.filter(name=comp_name)
    team = db.session.query(Team).filter_by(name=team_name).one()
    if team.created_by != login_session['user_id']:
        # in case of access by URL
        return ('<script>function myFunction() {alert("ou are not authorised to edit this team.  Please create your own'
                ' team in order to edit.");}</script><body onload="myFunction()">')
    if request.method == 'POST':
        if request.form['name']:
            team.name = request.form['name']
        if request.form['email']:
            team.email = request.form['email']
        if request.form['home']:
            team.home = request.form['home']
        if request.form['comp']:
            team.comp = request.form['comp']
        db.session.add(team)
        db.session.commit()
        flash('Team Updated!')
        return redirect(url_for('showTeams', comp_name=comp_name))
    else:
        return render_template('edit_team.html', comp=comp,
                               comps=comps, team=team)


@app.route('/comp/<path:comp_name>/teams/<path:team_name>/delete', methods=['DELETE', 'GET'])
def delete_team(comp_name, team_name):
    comp = db.session.query(Comp).filter_by(name=comp_name).one()
    team = db.session.query(Team).filter_by(name=team_name).one()
    if team.created_by != login_session['user_id']:
        # in case of access by URL
        return ('<script>function myFunction() {alert("You are not authorised to delete this team.  Please create your '
                'own team in order to delete.");}</script><body onload="myFunction()">')
    if request.method == 'DELETE':
        db.session.delete(team)
        db.session.commit()
        flash('Team Deleted!')
        return redirect(url_for('showTeams', comp_name=comp_name))
    else:
        return render_template('delete_team.html',
                               comp=comp, team=team)


@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, fbclient_id=config.FB_ID)


@app.route('/fbconnect', methods=['POST'])
def fb_connect():
    """Facebook token exchange function - if successful populates login_session with user details"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print(f"access token received {access_token} ")

    url = 'https://graph.facebook.com/oauth/access_token'
    params = {'grant_type': 'fb_exchange_token',
              'client_id': config.FB_ID,
              'client_secret': config.FB_SECRET,
              'fb_exchange_token': access_token}
    response = requests.get(url, params=params)
    result = response.json()[1]

    # Use token to get user info from API
    """
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first
        index which gives us the key : value for the server access token
        then we split it on colons to pull out the actual token value and
        replace the remaining quotes with nothing so that it can be used
        directly in the graph api calls
    """
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
    result = requests.get(url, params=params)
    data = result.json()[1]

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user()
    login_session['user_id'] = user_id
    # updates the username and picture for a stored user if they have changed
    update_user(user_id)

    # Output HTML returned
    output = ''
    output += '<h3 class="card-title">Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: 150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;">'
    flash(f"Now logged in as {login_session['username']}")
    return output


@app.route('/fbdisconnect')
def fb_disconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = f'https://graph.facebook.com/{facebook_id}/permissions'
    params = {'access_token': access_token}
    requests.get(url, params=params)
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fb_disconnect()
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


@app.route('/admin', methods=['GET', 'POST'])
def show_admin():
    if request.method == 'POST':
        comp_id = request.form.get('comp_id')
        if comp_id:
            dt = datetime.strptime(request.form['match_date'], '%Y-%m-%d')
            create_fixture_round(dt, comp_id)
            return "Done"
    else:
        return render_template('admin.html')


@app.route('/add_news_item', methods=['GET', 'POST'])
def add_news_item():
    if request.method == 'POST':
        news_item = NewsItem(
            title=request.form['title'],
            message=request.form['message'],
            created_by=3)
        db.session.add(news_item)
        db.session.commit()

    news = db.session.query(NewsItem).all()
    return render_template('add_news_item.html', news=news)


@app.route('/fixtures', methods=['GET', 'POST'])
def create_fixtures():
    comps = db.session.query(Comp).all()
    if request.method == 'POST':
        comp = request.form['comp']
        create_fixture_round(request.form['date'], comp)
        return render_template('fixtures.html', comps=comps)
    return render_template('fixtures.html', comps=comps)


@app.route('/results', methods=['GET', 'POST'])
def create_results():
    home_team_alias = aliased(Team)
    away_team_alias = aliased(Team)
    matches = (db.session.query(Match)
               .join(home_team_alias, Match.home_team == home_team_alias.id)
               .join(away_team_alias, Match.away_team == away_team_alias.id)
               .join(FixtureRound)
               .join(Comp)
               .options(joinedload(Match.team1))
               .options(joinedload(Match.team2))
               .all()
               )
    if request.method == 'POST':
        comp = request.form['comp']
        create_fixture_round(request.form['date'], comp)
        return render_template('results.html', matches=matches)
    return render_template('results.html', matches=matches)


