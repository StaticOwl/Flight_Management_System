import pytest
from models import User
import os
from dotenv import load_dotenv

from __init__ import create_app

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    load_dotenv()
    os.environ['CONFIG_TYPE'] = 'testing'
    flask_app = create_app(os.getenv("CONFIG_TYPE"))

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def new_user():

    user = User(
        first_name='Charles',
        last_name='Babbage',
        email='AnalyticalEngineer@hotmail.com',
        password='FlaskIsAwesome',
        phone='867-5309',
        address='123 Main St.'
    )
    return user