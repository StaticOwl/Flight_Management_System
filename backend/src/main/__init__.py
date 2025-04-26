from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Updated import statement
from main.config.config import config

print("Creating App")
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_mode="dev"):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    print(f"Running in {config_mode} mode")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not Set')}")

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    return app