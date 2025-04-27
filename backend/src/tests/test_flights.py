def test_create_flight_success(test_client, db_session):
    """
    GIVEN a valid airline and flight details
    WHEN the "/createflights" endpoint is accessed via POST
    THEN validate that the flight is created successfully
    """
    flight_data = {
        "airline_id": 1,
        "flight_number": "FL123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": "2024-03-10T08:00",
        "arrival_time": "2024-03-10T11:30",
        "aircraft_type": "Boeing 737",
        "num_seats": 180
    }

    response = test_client.post('/createflights', json=flight_data)

    assert response.status_code == 201
    assert "flight_id" in response.json
    assert response.json["flight_number"] == flight_data["flight_number"]

def test_create_flight_missing_fields(test_client):
    """
    GIVEN a flight creation request with missing fields
    WHEN the "/createflights" endpoint is accessed via POST
    THEN validate that a 400 error is returned
    """
    incomplete_flight_data = {
        "airline_id": 1,
        "flight_number": "FL123"
        # Missing departure_airport, arrival_airport, etc.
    }

    response = test_client.post('/createflights', json=incomplete_flight_data)

    assert response.status_code == 400
    assert b"Missing required fields" in response.data

def test_search_flights_success(test_client, db_session):
    """
    GIVEN existing flights in the database
    WHEN the "/flights/search" endpoint is accessed via GET with filters
    THEN validate that matching flights are returned
    """
    # Create a flight first
    flight_data = {
        "airline_id": 909,
        "flight_number": "FL123",
        "departure_airport": "DUMMY_DEP",
        "arrival_airport": "DUMMY_ARR",
        "departure_time": "2024-03-10T08:00",
        "arrival_time": "2024-03-10T11:30",
        "aircraft_type": "Boeing 737",
        "num_seats": 180
    }
    test_client.post('/createflights', json=flight_data)

    # Now search for the created flight
    response = test_client.get('/flights/search?departure_airport=DUMMY_DEP&arrival_airport=DUMMY_ARR')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Should return a list of flights
    assert len(response.json) > 0
    assert response.json[0]["flight_number"] == "FL123"

def test_search_flights_no_matches(test_client):
    """
    GIVEN no flights matching the search criteria
    WHEN the "/flights/search" endpoint is accessed via GET
    THEN validate that a 404 error is returned
    """
    response = test_client.get('/flights/search?departure_airport=XYZ&arrival_airport=ABC')

    assert response.status_code == 404
    assert b"No flights found" in response.data



def test_fetch_flights_by_airline_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/flights_by_airlines/<airline_id>" endpoint is accessed via GET
    THEN validate that it returns a list of flights for that airline
    """
    airline_id = 1
    response = test_client.get(f'/flights_by_airlines/{airline_id}')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of flights


def test_fetch_flights_by_invalid_airline(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/flights_by_airlines/<airline_id>" endpoint is accessed for a non-existent airline
    THEN validate that it returns an error
    """
    invalid_airline_id = 420
    response = test_client.get(f'/flights_by_airlines/{invalid_airline_id}')

    assert response.status_code == 401  # Expecting a "Not Found" or "Bad Request" error


def test_get_crew_by_flight_success(test_client, db_session):
    """
    GIVEN an existing flight with crew assignments
    WHEN the "/flights/<flight_id>/crew" endpoint is accessed via GET
    THEN validate that the crew assignments are returned correctly
    """

    flight_data = {
        "airline_id": 1,
        "flight_number": "FL100",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": "2024-03-10T08:00",
        "arrival_time": "2024-03-10T11:30",
        "aircraft_type": "Boeing 737",
        "num_seats": 180
    }
    flight_response = test_client.post('/createflights', json=flight_data)
    assert flight_response.status_code == 201
    flight_id = flight_response.json["flight_id"]

    crew1_data = {"first_name": "John", "last_name": "Doe", "flight_id": flight_id, "role_id": "1"}
    crew2_data = {"first_name": "Alice", "last_name": "Smith", "flight_id": flight_id, "role_id": "2"}

    crew1_response = test_client.post('/addCrew', json=crew1_data)
    crew2_response = test_client.post('/addCrew', json=crew2_data)

    assert crew1_response.status_code == 201
    assert crew2_response.status_code == 201

    crew1_id = crew1_response.json["crew_id"]
    crew2_id = crew2_response.json["crew_id"]

    crew_assignments = {
        "crew_assignments": [
            {"crew_id": crew1_id, "role_id": 1},  # Assuming role_id 1 is Pilot
            {"crew_id": crew2_id, "role_id": 2}  # Assuming role_id 2 is Co-Pilot
        ]
    }

    assign_crew_response = test_client.put(f'/flights/{flight_id}/crew', json=crew_assignments)
    assert assign_crew_response.status_code == 200
    assert b"Crew assignments updated successfully" in assign_crew_response.data

    get_crew_response = test_client.get(f'/flights/{flight_id}/crew')

    assert get_crew_response.status_code == 200
    crew_list = get_crew_response.json
    assert len(crew_list) == 2  # Expecting two crew members
    assert crew_list[0]["first_name"] == "John"
    assert crew_list[1]["first_name"] == "Alice"

def test_update_crew_by_flight_success(test_client, db_session):
    """
    GIVEN an existing flight with assigned crew members
    WHEN the "/flights/<flight_id>/crew" endpoint is accessed via PUT
    THEN validate that the crew assignments are updated correctly
    """

    flight_data = {
        "airline_id": 1,
        "flight_number": "FL101",
        "departure_airport": "LAX",
        "arrival_airport": "ORD",
        "departure_time": "2024-03-15T14:00",
        "arrival_time": "2024-03-15T17:00",
        "aircraft_type": "Airbus A320",
        "num_seats": 200
    }
    flight_response = test_client.post('/createflights', json=flight_data)
    assert flight_response.status_code == 201
    flight_id = flight_response.json["flight_id"]

    crew1_data = {"first_name": "Jake", "last_name": "Brown", "flight_id": flight_id, "role_id": 1}
    crew2_data = {"first_name": "Emily", "last_name": "Clark", "flight_id": flight_id, "role_id": 2}

    crew1_response = test_client.post('/addCrew', json=crew1_data)
    crew2_response = test_client.post('/addCrew', json=crew2_data)

    assert crew1_response.status_code == 201
    assert crew2_response.status_code == 201

    crew1_id = crew1_response.json["crew_id"]
    crew2_id = crew2_response.json["crew_id"]

    crew_assignments = {
        "crew_assignments": [
            {"crew_id": crew1_id, "role_id": 1},  # Pilot
            {"crew_id": crew2_id, "role_id": 3}   # Flight Attendant
        ]
    }
    assign_response = test_client.put(f'/flights/{flight_id}/crew', json=crew_assignments)
    assert assign_response.status_code == 200

    # Step 4: Create new crew members for update
    new_crew1_data = {"first_name": "Mark", "last_name": "Davis", "flight_id": flight_id, "role_id": 1}
    new_crew2_data = {"first_name": "Sophie", "last_name": "Taylor", "flight_id": flight_id, "role_id": 3}

    new_crew1_response = test_client.post('/addCrew', json=new_crew1_data)
    new_crew2_response = test_client.post('/addCrew', json=new_crew2_data)

    assert new_crew1_response.status_code == 201
    assert new_crew2_response.status_code == 201

    new_crew1_id = new_crew1_response.json["crew_id"]
    new_crew2_id = new_crew2_response.json["crew_id"]

    updated_crew_assignments = {
        "crew_assignments": [
            {"crew_id": new_crew1_id, "role_id": 2},  # Co-Pilot
            {"crew_id": new_crew2_id, "role_id": 4}   # Flight Engineer
        ]
    }
    update_response = test_client.put(f'/flights/{flight_id}/crew', json=updated_crew_assignments)

    assert update_response.status_code == 200
    assert b"Crew assignments updated successfully" in update_response.data

    get_updated_crew_response = test_client.get(f'/flights/{flight_id}/crew')
    assert get_updated_crew_response.status_code == 200
    updated_crew_list = get_updated_crew_response.json
    assert len(updated_crew_list) == 2  # Expecting two updated crew members
    assert updated_crew_list[0]["first_name"] == "Mark"
    assert updated_crew_list[1]["first_name"] == "Sophie"

def test_get_flights_success(test_client):
    """
    GIVEN that flights exist in the database
    WHEN the "/flights" endpoint is accessed via GET
    THEN validate that the list of flights is returned successfully
    """

    response = test_client.get('/flights')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of airlines

