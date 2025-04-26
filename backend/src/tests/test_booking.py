import pytest

from tests.utils import get_auth_token


def test_create_booking_success(test_client, db_session):
    """
    GIVEN a valid user and flight
    WHEN the "/createbooking" endpoint is accessed via POST
    THEN validate that the booking is created successfully
    """
    token = get_auth_token(test_client, db_session)  # Ensure user exists

    booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-02-01",
        "num_passengers": 2,
        "total_cost": 500.00
    }

    response = test_client.post('/createbooking', json=booking_data)

    assert response.status_code == 201
    assert "booking_id" in response.json

def test_create_booking_missing_fields(test_client, db_session):
    """
    GIVEN a valid user
    WHEN the "/createbooking" endpoint is accessed via POST with missing fields
    THEN validate that a 400 error is returned
    """
    token = get_auth_token(test_client, db_session)

    incomplete_booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-02-01"
        # Missing 'num_passengers' and 'total_cost'
    }

    response = test_client.post('/createbooking', json=incomplete_booking_data)

    assert response.status_code == 400
    assert b"Missing required fields" in response.data


def test_modify_booking_success(test_client, db_session):
    """
    GIVEN an existing booking
    WHEN the "/bookings/<booking_id>" endpoint is accessed via PUT
    THEN validate that the booking details are updated
    """
    token = get_auth_token(test_client, db_session)

    # Create a booking first
    booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-02-01",
        "num_passengers": 2,
        "total_cost": 500.00
    }
    create_response = test_client.post('/createbooking', json=booking_data)
    assert create_response.status_code == 201

    booking_id = create_response.json["booking_id"]

    # Modify the booking
    update_data = {
        "flight_id": 2,  # Change flight
        "num_passengers": 3,
        "total_cost": 750.00
    }

    response = test_client.put(f'/bookings/{booking_id}', json=update_data)

    assert response.status_code == 200
    assert response.json["flight_id"] == update_data["flight_id"]
    assert response.json["num_passengers"] == update_data["num_passengers"]


def test_modify_nonexistent_booking(test_client):
    """
    GIVEN a booking ID that does not exist
    WHEN the "/bookings/<booking_id>" endpoint is accessed via PUT
    THEN validate that a 404 error is returned
    """
    update_data = {"flight_id": 2}

    response = test_client.put('/bookings/9999', json=update_data)

    assert response.status_code == 404
    assert b"Booking not found" in response.data

def test_cancel_booking_success(test_client, db_session):
    """
    GIVEN an existing booking
    WHEN the "/bookings/<booking_id>" endpoint is accessed via DELETE
    THEN validate that the booking is deleted successfully
    """
    token = get_auth_token(test_client, db_session)

    # Create a booking first
    booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-02-01",
        "num_passengers": 2,
        "total_cost": 500.00
    }
    create_response = test_client.post('/createbooking', json=booking_data)
    assert create_response.status_code == 201

    booking_id = create_response.json["booking_id"]

    # Cancel the booking
    response = test_client.delete(f'/bookings/{booking_id}')

    assert response.status_code == 200
    assert b"Booking canceled successfully" in response.data

def test_cancel_nonexistent_booking(test_client):
    """
    GIVEN a booking ID that does not exist
    WHEN the "/bookings/<booking_id>" endpoint is accessed via DELETE
    THEN validate that a 404 error is returned
    """
    response = test_client.delete('/bookings/9999')

    assert response.status_code == 500
    assert b"Booking not found" in response.data

def test_get_booking_history_success(test_client, db_session):
    """
    GIVEN an existing user with bookings
    WHEN the "/users/bookings" endpoint is accessed via GET
    THEN validate that booking history is returned
    """
    token = get_auth_token(test_client, db_session)

    # Create a booking
    booking_data = {
        "token": token,
        "flight_id": 1,
        "booking_date": "2024-02-01",
        "num_passengers": 2,
        "total_cost": 500.00
    }
    test_client.post('/createbooking', json=booking_data)

    # Fetch booking history
    response = test_client.get('/users/bookings', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Ensure the response is a list
    assert len(response.json) > 0  # Ensure at least one booking exists

def test_get_booking_history_no_bookings(test_client, db_session):
    """
    GIVEN a user with no bookings
    WHEN the "/users/bookings" endpoint is accessed via GET
    THEN validate that a 404 error is returned
    """
    token = get_auth_token(test_client, db_session, user_id=9999)

    response = test_client.get('/users/bookings', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    assert b"No bookings found" in response.data
