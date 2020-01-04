
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.psql_user}:{config.psql_pw}@localhost/league'
db = SQLAlchemy(app)

from . import views

app.secret_key = os.urandom(16)


FB_ID = config.FB_ID
FB_SECRET = config.FB_SECRET

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
