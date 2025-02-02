import pytest
import os
from __init__ import create_app


def test_list_user_controller(test_client):
    """
    GIVEN a flask application configured for testing
    WHEN the "/api/<name>" endpoint is issued a GET request
    THEN validate that it lists the dictionary form of <name> table
    """


    # Create a test client using the Flask application configured for testing
    response = test_client.get('/api/User')
    assert response.status_code == 200
    assert b"john.doe@email.com" in response.data
    assert b"John" in response.data
    assert b"Doe" in response.data
    assert b"password123" in response.data
    assert b"user_id: 1" in response.data

def test_login(test_client):
    """
    GIVEN a flask application configured for testing
    WHEN the "login" endpoint is issued a POST request with a valid UN and PW
    THEN validate the selected user is logged in
    """

    response = test_client.post('/login',
                                data={'email': 'john.doe@email.com',
                                      'password': 'password123'},
                                follow_redirects=True)

    assert response.status_code == 200
    assert test_client
    assert b"Login successful" in response.data