import pytest
import sys

import os
os.environ['FLASK_ENV'] = 'test'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import sqlalchemy

# Ensure `main/` is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main/")))

from main.__init__ import create_app, db

@pytest.fixture(scope='session')
def test_app():
    """Create and configure a new Flask test app instance."""
    app = create_app()

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
def db_session(test_app, request):
    """Provides a test database session, rolling back after each test."""
    print(db.metadata.tables.keys())
    with test_app.app_context():
        session = db.session
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ddl/init_ddl/DDL.sql")), "r") as file:
            q = file.read()
            for statement in q.split(";"):
                s = statement.strip()
                if s:
                    s2 = sqlalchemy.text(s)
                    session.execute(s2)
        session.commit()

        def teardown():
            with test_app.app_context():
                session.remove()

        request.addfinalizer(teardown)
        yield session