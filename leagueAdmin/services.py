import random

from .models import AppUser, FixtureRound, Comp, Match
from .views import login_session
from . import db


def is_logged_in():
    if login_session.get('user_id') is None:
        return False
    return True


# AppUser functions
def get_user_id(email):
    user = db.session.query(AppUser).filter_by(email=email).one()
    return user.id


def get_user_info(user_id):
    user = db.session.query(AppUser).filter_by(id=user_id).one()
    if user.picture != login_session['picture']:
        user.picture = login_session['picture']
    elif user.name != login_session['AppUsername']:
        user.name = login_session['AppUsername']
    db.session.add(AppUser)
    db.session.commit()
    return AppUser


def update_user(user_id):
    user = db.session.query(AppUser).filter_by(id=user_id).one()
    if user.picture != login_session['picture']:
        user.picture = login_session['picture']
    elif user.name != login_session['AppUsername']:
        user.name = login_session['AppUsername']
    db.session.add(user)
    db.session.commit()


def create_user():
    new_user = AppUser(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    db.session.add(new_user)
    db.session.commit()
    user = db.session.query(AppUser).filter_by(email=login_session['email']).one()
    return user.id


def create_fixture_round(date, comp_id):
    # need to dynamically add season and user below
    fixture_round = FixtureRound(date=date, season_id=1, comp_id=comp_id, created_by=1)
    db.session.add(fixture_round)
    db.session.flush()
    comp = db.session.query(Comp).filter_by(id=comp_id).one()
    teams = comp.teams

    if len(teams) > 2:
        random.shuffle(teams)
        while len(teams) >= 2:
            team1 = teams.pop()
            team2 = teams.pop()
            match = Match(fixture_round_id=fixture_round.id, home_team=team1.id, away_team=team2.id,
                          home_id=team1.home_id, referee_id=1, created_by=1)
            db.session.add(match)
        db.session.commit()
        return db.session.query(Match).filter_by(fixture_round_id=fixture_round.id).all()


def save_results(results):
    for result in results:
        if result[:1] == 'h':
            match_id = result[1:]
            home_score = results[result]
            away_score = results['a'+match_id]
            match = db.session.query(Match).filter_by(id=int(match_id)).one()
            match.home_score = home_score
            match.away_score = away_score
            db.session.commit()
