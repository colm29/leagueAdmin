# # -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, flash, request, redirect,  make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import json
import random
import string
import os

from .db_setup import AppUser, engine


def newSession():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


# Function to check if user is logged in
def loggedIn():
    if login_session.get('user_id') is None:
        return False
    return True


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
        user = session.query(AppUser).filter_by(id=user_id).one()
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
    newUser = AppUser(name=login_session['username'], email=login_session
                      ['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(AppUser).filter_by(email=login_session['email']).one()
    return user.id
