from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

from src.main.config.config import config
import src.main.config.defaults as defaults
from src.main.config.config import DevelopmentConfig

print("Creating App")
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    config_mode = os.getenv('FLASK_ENV', defaults.FLASK_ENV)
    print(f"{os.getenv("DATABASE_URL", defaults.DATABASE_URL)}")
    app = Flask(__name__)

    config_obj = config.get(config_mode, DevelopmentConfig())
    if config_obj is not None:
        app.config.from_object(config_obj)

    print(f"Running in {config_mode} mode")
    print(f"Config: {app.config}")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not Set')}")

    db.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app)
    return app