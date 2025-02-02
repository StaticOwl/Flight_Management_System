import pytest
from models import User
#Courtesy https://testdriven.io/blog/flask-pytest/

#CRUD per table

#Create
def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, First name, last name, phone, password, and address are defined correctly

    TESTS SQLAlchemy Setup NOT the underlying DB
    """
    assert new_user.email == 'AnalyticalEngineer@hotmail.com'
    assert new_user.password == 'FlaskIsAwesome'
    assert new_user.first_name == 'Charles'
    assert new_user.last_name == 'Babbage'
    assert new_user.phone == '867-5309'
    assert new_user.address == '123 Main St.'

#Read

#Update

#Delete