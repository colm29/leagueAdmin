import random

import typing

from sqlalchemy import or_

from .models import AppUser, FixtureRound, Comp, Match, Team
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


def calculate_table(teams: [Team], comp_id: int) -> typing.List[typing.Dict[str, typing.Dict[str, int]]]:
    table = []
    for team in teams:
        query = (
            db.session.query(Match)
            .join(FixtureRound)
            .filter(or_(Match.home_team == team.id, Match.away_team == team.id))
            .filter_by(comp_id=comp_id)
            .filter(Match.home_score.isnot(None))
        )

        matches = query.all()
        won = 0
        drawn = 0
        lost = 0
        goals_for = 0
        goals_against = 0

        for match in matches:
            if (match.home_team == team.id and match.home_score > match.away_score or
                    match.away_team == team.id and match.away_score > match.home_score):
                won += 1
            elif match.home_score == match.away_score:
                drawn += 1
            else:
                lost += 1

            goals_for += match.home_score if match.home_team == team.id else match.away_score
            goals_against += match.home_score if match.away_team == team.id else match.away_score

        table.append(
            {
                'team': team.name,
                'P': len(matches),
                'W': won,
                'D': drawn,
                'L': lost,
                'F': goals_for,
                'A': goals_against,
                'Pts': won * 3 + drawn * 1,
            }
        )

    table = sorted(
        table,
        key=lambda x: (
                     x['Pts'],
                     x['F'] - x['A'],
                     x['F']
                 ),
        reverse=True
    )
    for index, team in enumerate(table):
        team['pos'] = index + 1

    return table
