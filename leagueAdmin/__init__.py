
from flask import Flask
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from leagueAdmin.db_setup import Base

from . import config

app = Flask(__name__)

from . import views

app.secret_key = os.urandom(16)


FB_ID = config.FB_ID
FB_SECRET = config.FB_SECRET

engine = create_engine(
    f'postgresql://{config.psql_user}:{config.psql_pw}@localhost/league')
Base.metadata.bind = engine

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
