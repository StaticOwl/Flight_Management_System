from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

from dotenv import load_dotenv
load_dotenv('./resources/.env')

from config.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config[os.getenv("CONFIG_MODE")])

    db.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app)
    return app