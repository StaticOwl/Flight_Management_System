def test_fetch_roles_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/roles" endpoint is accessed via GET
    THEN validate that it returns a list of roles
    """
    response = test_client.get('/roles')

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expecting a list of roles


def test_fetch_roles_invalid_method(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/roles" endpoint is accessed via POST (which is not allowed)
    THEN validate that it returns a 405 error
    """
    response = test_client.post('/roles')

    assert response.status_code == 405
    # assert b"Method is Not Allowed" in response.data