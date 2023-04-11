import logging
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from pathlib import Path


load_dotenv()

home = str(Path.home())
current_dir = os.getcwd()


project_dir = os.getenv("PROJECT_DIR")
image_path = os.getenv("IMAGE_PATH")



DB_HOST = '10.1.62.97'
PORT = '1521'
SERVICE_NAME = 'jusCourtspdb.sfjustis.sfgov.org'
DB_USERNAME = 'courtadmin'
DB_PASSWORD = 'courtadmin1234$'


app = Flask(__name__)
app.config["SECRET_KEY"] = "secrets.token_hex()"
# basedir  = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "db.sqlite3"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

try:
    db = SQLAlchemy(app)
    m = Migrate(app, db)
except sqlalchemy.exc.ProgrammingError as e:
    print("error", e)

ma = Marshmallow(app)

# init bcrypt
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from application import routes
from application import customer



