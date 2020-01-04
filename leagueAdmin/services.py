from .models import AppUser
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
