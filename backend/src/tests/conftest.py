import pytest
import sys
import os

import sqlalchemy

# Ensure `main/` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main/")))

from main import create_app, db
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

@pytest.fixture(scope='session')
def test_app():
    """Create and configure a new Flask test app instance."""
    app = create_app("testing")

    from main.service.urls import urls_bp
    app.register_blueprint(urls_bp)
    
    with app.app_context():
        db.create_all()

    yield app
    with app.app_context():
        db.session.remove() 
        db.drop_all()
        db.engine.dispose()

@pytest.fixture(scope='session')
def test_client(test_app):
    """Return a test client for making API requests."""
    return test_app.test_client()

@pytest.fixture(scope="session")
def db_session(test_app):
    """Provides a test database session, rolling back after each test."""
    with test_app.app_context():
        session = db.session
        with open("main/resources/DDL.sql", "r") as file:
            q = file.read()
            for statement in q.split(";"):
                s = statement.strip()
                if s:
                    s2 = sqlalchemy.text(s)
                    session.execute(s2)
        yield session
        session.rollback()
        session.close()

@pytest.fixture(scope='session')
def new_user(db_session):
    """Create a new user for testing."""
    from main.dao.models import User
    user = User(
        first_name='John',
        last_name='Doe',
        email='john.doe2@email.com',
        password='password123',
        phone='867-5309',
        address='123 Main St.'
    )
    
    db_session.add(user)
    db_session.commit()

    print(f"New User Created: {user.user_id}, {user.email}")
    return user
