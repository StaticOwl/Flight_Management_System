# List all entities

def test_list_entities_success(test_client):
    response = test_client.get('/api/User')
    assert response.status_code == 200


# Login Tests
def test_login_success(test_client, db_session):
    """
    GIVEN a flask application configured for testing
    WHEN the "login" endpoint is issued a POST request with a valid UN and PW
    THEN validate the selected user is logged in
    """
    response = test_client.post('/login',
                                json={'email': 'john.doe@email.com',
                                      'password': 'password123'},
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_login_nonexistant_user_failure(test_client):
    """
    GIVEN a flask application configured for testing
    WHEN the "login" endpoint is issued a POST request with a non-existing UN and PW
    THEN validate the error message "User doesn't exist" is returned
    """

    response = test_client.post('/login',
                                json={'email': 'john.doe@gmail.com',
                                      'password': 'password12365'},
                                follow_redirects=True)
    
    assert response.status_code == 401
    assert b"User doesn't exist" in response.data


def test_login_bad_password_failure(test_client):
    """
    GIVEN a flask application configured for testing
    WHEN the "login" endpoint is issued a POST request with a non-existing UN and PW
    THEN validate the error message "User doesn't exist" is returned
    """

    response = test_client.post('/login',
                                json={'email': 'john.doe@email.com',
                                      'password': 'password12365'},
                                follow_redirects=True)

    assert response.status_code == 401
    assert b"Invalid password" in response.data

def test_login_missing_field_failure(test_client):
    """
    GIVEN a flask application configured for testing
    WHEN the "login" endpoint is issued a POST request with a missing field
    THEN validate the error message "Both email and password are required" is returned
    """

    response = test_client.post('/login',
                                json={'email': 'john.doe@gmail.com'},
                                follow_redirects=True)
    
    assert response.status_code == 400
    assert b"Both email and password are required" in response.data



