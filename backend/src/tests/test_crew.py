import pytest


def test_get_crew_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/getCrew" endpoint is accessed via GET
    THEN validate that it returns a list of crew members
    """
    response = test_client.get('/getCrew')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of crew members

def test_add_crew_success(test_client, db_session):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/addCrew" endpoint is issued a POST request with valid crew data
    THEN validate the new crew member is created successfully
    """
    crew_data = {
        "first_name": "New",
        "last_name": "Crew",
        "flight_id": 1,
        "role_id": 1
    }

    response = test_client.post('/addCrew', json=crew_data)

    assert response.status_code == 201
    assert b"crew_id" in response.data


def test_add_crew_missing_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/addCrew" endpoint is issued a POST request with missing data
    THEN validate that it returns a 400 error
    """
    incomplete_crew_data = {"first_name": "Alice"}  # Missing last_name & role

    response = test_client.post('/addCrew', json=incomplete_crew_data)

    assert response.status_code == 400
    assert b"Missing required fields" in response.data

def test_update_crew_success(test_client, db_session):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/update-crew/<crew_id>" endpoint is issued a PUT request with valid data
    THEN validate that the crew member is updated successfully
    """
    crew_id = 6
    update_data = {"last_name": "Shaman"}

    response = test_client.put(f'/update-crew/{crew_id}', json=update_data)

    assert response.status_code == 200
    assert b"Shaman" in response.data


def test_update_nonexistent_crew(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/update-crew/<crew_id>" endpoint is issued a PUT request for a non-existent crew
    THEN validate that it returns a 404 error
    """
    invalid_crew_id = 9999  # Non-existent crew ID
    update_data = {"role": "Captain"}

    response = test_client.put(f'/update-crew/{invalid_crew_id}', json=update_data)

    assert response.status_code == 404
    assert b"Crew member not found" in response.data