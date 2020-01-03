from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from .db_setup import AppUser, engine


def new_session():
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def is_logged_in():
    if login_session.get('user_id') is None:
        return False
    return True


# user functions
def get_user_id(email):
    try:
        session = new_session()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None
    finally:
        session.close()


def get_user_info(user_id):
    try:
        session = new_session()
        user = session.query(AppUser).filter_by(id=user_id).one()
        if user.picture != login_session['picture']:
            user.picture = login_session['picture']
        elif user.name != login_session['username']:
            user.name = login_session['username']
        session.add(user)
        session.commit()
        return user
    except Exception:
        return None
    finally:
        session.close()


def update_user(user_id):
    try:
        session = new_session()
        user = session.query(AppUser).filter_by(id=user_id).one()
        if user.picture != login_session['picture']:
            user.picture = login_session['picture']
        elif user.name != login_session['username']:
            user.name = login_session['username']
        session.add(user)
        session.commit()
    finally:
        session.close()


def create_user(login_session):
    session = new_session()
    new_user = AppUser(name=login_session['username'], email=login_session
                      ['email'], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(AppUser).filter_by(email=login_session['email']).one()
    return user.id
