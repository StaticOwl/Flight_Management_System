def test_get_airlines_success(test_client):
    """
    GIVEN that airlines exist in the database
    WHEN the "/airlines" endpoint is accessed via GET
    THEN validate that the list of airlines is returned successfully
    """

    response = test_client.get('/airlines')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of airlines



def test_get_airline_dashboard_success(test_client, db_session):
    """
    GIVEN an existing airline in the database
    WHEN the "/airlines/<airline_id>" endpoint is accessed via GET
    THEN validate that the airline details are returned correctly
    """

    response = test_client.get('/airlines/1')  # Assuming airline with ID 1 exists

    assert response.status_code == 200
    assert "airline_name" in response.json  # Should contain airline details