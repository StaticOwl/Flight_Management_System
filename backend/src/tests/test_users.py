from datetime import timedelta, datetime

import jwt

from service.controllers import SECRET_KEY
from tests.utils import get_auth_token


def test_create_user_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/createuser" endpoint is issued a POST request with valid user data
    THEN validate that the user is created successfully and a 201 status is returned
    """
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "password": "securepassword",
        "phone": "1234567890",
        "address": "123 Main St"
    }

    response = test_client.post('/createuser', json=user_data)

    assert response.status_code == 201
    assert "email" in response.json
    assert response.json["email"] == user_data["email"]


def test_create_user_missing_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/createuser" endpoint is issued a POST request with missing fields
    THEN validate that it returns a 400 error
    """
    incomplete_user_data = {
        "first_name": "Alice",
        "email": "alice@example.com"
    }

    response = test_client.post('/createuser', json=incomplete_user_data)

    assert response.status_code == 400
    assert b"Missing required fields" in response.data


def test_create_user_duplicate_email(test_client, db_session):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/createuser" endpoint is issued a POST request with an already used email
    THEN validate that it returns a 409 error
    """
    user_data = {
        "first_name": "Alice",
        "last_name": "Smit",
        "email": "duplicate@email.com",
        "password": "securepassword"
    }

    # First user creation (should be successful)
    response1 = test_client.post('/createuser', json=user_data)
    assert response1.status_code == 201  # User created successfully

    # Attempt to create a user with the same email again
    response2 = test_client.post('/createuser', json=user_data)

    assert response2.status_code == 409
    assert b"Email already in use" in response2.data


def test_create_user_cors_options(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/createuser" endpoint is issued an OPTIONS request
    THEN validate that it returns a 200 status for CORS preflight
    """
    response = test_client.options('/createuser')

    assert response.status_code == 200
    assert b"CORS preflight successful" in response.data

# /users
def test_get_user_profile_success(test_client, db_session):
    """
    GIVEN a valid user login
    WHEN the "/users" endpoint is accessed via GET
    THEN validate that the user profile is returned
    """
    token = get_auth_token(test_client, db_session)  # Get token before making request

    response = test_client.get('/users', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "email" in response.json


def test_update_user_profile_success(test_client, db_session):
    """
    GIVEN a valid user login
    WHEN the "/users" endpoint is accessed via PUT
    THEN validate that the user profile is updated successfully
    """
    token = get_auth_token(test_client, db_session)

    update_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "9876543210",
        "address": "New Address 123"
    }

    response = test_client.put('/users', json=update_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json["first_name"] == update_data["first_name"]
    assert response.json["last_name"] == update_data["last_name"]


def test_extract_user_id_from_token(test_client, db_session):
    """
    GIVEN a valid token
    WHEN the "/token" endpoint is accessed via GET with the token in the header
    THEN validate that the correct user ID is returned
    """
    token = get_auth_token(test_client, db_session, user_id=1)  # Generate token for user 1

    response = test_client.get('/token', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json['user_id'] == 1

def test_extract_user_id_from_token_expired(test_client):
    """
    GIVEN an expired token
    WHEN the "/token" endpoint is accessed
    THEN a 401 with 'Token has expired' should be returned
    """
    expired_token = jwt.encode({
        'user_id': 1,
        'exp': datetime.now() - timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    response = test_client.get('/token', headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == 401
    assert 'Token has expired' in response.json['message']

def test_extract_user_id_from_token_invalid_format(test_client):
    """
    GIVEN an improperly formatted token
    WHEN the "/token" endpoint is accessed
    THEN a 401 should be returned for invalid token
    """
    response = test_client.get('/token', headers={"Authorization": "Bearer invalid.token.value"})

    assert response.status_code == 401
    assert 'Invalid token' in response.json['message']

def test_delete_user_success(test_client, db_session):
    """
    GIVEN an existing user created via API and a booking
    WHEN the "/users/<user_id>/delete" endpoint is accessed via DELETE
    THEN validate that the user and their bookings are deleted successfully
    """
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "password": "password123",
        "phone": "1234567890",
        "address": "123 Test Street"
    }
    create_user_response = test_client.post('/createuser', json=user_data)
    assert create_user_response.status_code == 201

    user_id = create_user_response.json["user_id"]

    login_response = test_client.post('/login', json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json["token"]

    booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-03-10",
        "num_passengers": 2,
        "total_cost": 500.00
    }
    create_booking_response = test_client.post('/createbooking', json=booking_data)
    assert create_booking_response.status_code == 201

    booking_id = create_booking_response.json["booking_id"]

    delete_response = test_client.delete(f'/users/{user_id}/delete')

    assert delete_response.status_code == 200
    assert b"User account deleted successfully" in delete_response.data

    # Step 5: Verify user and booking are deleted
    user_check_response = test_client.get(f'/users/{user_id}')
    assert user_check_response.status_code == 404  # User should be deleted

    booking_check_response = test_client.get(f'/bookings/{booking_id}')
    assert booking_check_response.status_code == 405  # Booking should be deleted

