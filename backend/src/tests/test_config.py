import os
import pytest

def test_config_loading(test_app):
    """Test if the app loads the testing configuration"""
    expected_db_uri = os.getenv('DATABASE_URL')

    assert test_app.config['TESTING'], "TESTING flag is not set"
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == expected_db_uri, "Database URI mismatch"