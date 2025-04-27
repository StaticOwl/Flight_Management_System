import uuid

def get_auth_token(test_client, db_session, user_id=1):
    """
    Ensures a test user exists and retrieves an authentication token for testing.
    """
    from main.dao.models import User  # Import User model
    from werkzeug.security import generate_password_hash

    # Ensure user exists in the test database
    user = db_session.get(User, user_id)
    if not user:
        user = User(
            user_id=user_id,
            first_name="Test",
            last_name="User",
            email=f"user_{uuid.uuid4().hex[:8]}@email.com",
            password=generate_password_hash("password123"),
            phone="1234567890",
            address="Test Address"
        )
        db_session.add(user)
        db_session.commit()

    # Now, generate a token for the existing user
    response = test_client.get(f'/gettoken/{user_id}')
    assert response.status_code == 200
    return response.json['token']