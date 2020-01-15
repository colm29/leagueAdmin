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
    try:
        user = db.session.query(AppUser).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def get_user_info(user_id):
    try:
        user = db.session.query(AppUser).filter_by(id=user_id).one()
        if user.picture != login_session['picture']:
            user.picture = login_session['picture']
        elif user.name != login_session['AppUsername']:
            user.name = login_session['AppUsername']
        db.session.add(AppUser)
        db.session.commit()
        return AppUser
    except Exception:
        return None
    finally:
        db.session.close()


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
        while len(teams) >= 2:
            team1 = teams.pop(random.choice(teams))
            team2 = teams.pop(random.choice(teams))
            match = Match(fixture_round_id=fixture_round.id, home_team=team1.id, away_team=team2.id,
                          home_id=team1.home_id, created_by=1)
            db.session.add(match)
        db.session.commit()
        return db.session.query(Match).filter_by(fixture_round_id=fixture_round.id).all()

