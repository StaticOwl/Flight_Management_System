from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv('.env')

from config.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_mode="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app)
    return app