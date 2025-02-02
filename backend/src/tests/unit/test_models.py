import pytest
from models import User
#Courtesy https://testdriven.io/blog/flask-pytest/

#CRUD per table

#Create
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, First name, last name, phone, password, and address are defined correctly

    TESTS SQLAlchemy Setup NOT the underlying DB
    """
    user = User(
        first_name='Charles',
        last_name='Babbage',
        email='AnalyticalEngineer@hotmail.com',
        password='FlaskIsAwesome',
        phone='867-5309',
        address='123 Main St.'
    )
    assert user.email == 'AnalyticalEngineer@hotmail.com'
    assert user.password == 'FlaskIsAwesome'
    assert user.first_name == 'Charles'
    assert user.last_name == 'Babbage'
    assert user.phone == '867-5309'
    assert user.address == '123 Main St.'

#Read

#Update

#Delete