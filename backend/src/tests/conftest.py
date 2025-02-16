import pytest
import sys
import os

import sqlalchemy

# Ensure `main/` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main/")))

from main.dao.models import User
from main import create_app, db
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

@pytest.fixture(scope='session')
def test_app():
    """Create and configure a new Flask test app instance."""
    app = create_app(db, "testing")
    
    with app.app_context():
        db.create_all()
        with open("../main/resources/DDL.sql") as file:
            q = sqlalchemy.text(file.read())
            db.session.execute(q)

    yield app
    with app.app_context():
        db.session.remove() 
        db.drop_all()
        db.get_engine(app).dispose()

@pytest.fixture(scope='function')
def test_client(test_app):
    """Return a test client for making API requests."""
    return test_app.test_client()

@pytest.fixture(scope="function")
def db_session(test_app):
    """Provides a test database session, rolling back after each test."""
    with test_app.app_context():
        session = db.session
        yield session
        session.rollback()
        session.close()

@pytest.fixture(scope='module')
def new_user():
    """Create a new user for testing."""
    user = User(
        first_name='Charles',
        last_name='Babbage',
        email='AnalyticalEngineer@hotmail.com',
        password='FlaskIsAwesome',
        phone='867-5309',
        address='123 Main St.'
    )
    return user
