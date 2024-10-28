import os
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize app
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure app
app.config.from_object("config.Config")

# Initialize extensions
db = SQLAlchemy(app)
Session(app)
migrate = Migrate(app, db)

# Import routes
from app.routes import *

# Import models
from app.models import *