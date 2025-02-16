import pytest
from main.dao.models import User, Airline, BookingDetail, Booking, Crew, CrewRole, FlightCrewAssignment, Flight, Passenger, Payment
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
def test_read_user(db_session):
    """
    GIVEN a DB instance
    WHEN a user is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = User.query.filter_by(email='john.doe@email.com').first()
    assert u.first_name == 'John'
    assert u.last_name == 'Doe'
    assert u.address == '123 Main St, City, Country'

def test_read_airline(db_session):
    """
    GIVEN a DB instance
    WHEN an airline is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Airline.query.get(1)
    assert u.airline_name == 'AirLine One'
    assert u.contact_email == 'contact@airlineone.com'

def test_read_bookingdetail(db_session):
    """
    GIVEN a DB instance
    WHEN a booking detail is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = BookingDetail.query.get(1)
    assert u.total_cost == 800.00
    assert u.num_passengers == 2
    assert u.flight_id == 2

def test_read_booking(db_session):
    """
    GIVEN a DB instance
    WHEN a booking is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Booking.query.get(2)
    assert u.user_id == 1

def test_read_crew(db_session):
    """
    GIVEN a DB instance
    WHEN a crew is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Crew.query.get(1)
    assert u.first_name == 'Alice'
    assert u.last_name == 'Taylor'

def test_read_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN a crew role is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = User.query.get(1)
    assert u.role_name == 'Pilot'

def test_read_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN a flight crew assignment is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = FlightCrewAssignment.query.get(1)
    assert u.flight_id == 1
    assert u.crew_id == 1
    assert u.role_id == 1

def test_read_flight(db_session):
    """
    GIVEN a DB instance
    WHEN a flight is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Flight.query.get(1)
    assert u.airline_id == 1
    assert u.flight_number == 'AL101'
    assert u.departure_airport == 'JFK'
    assert u.arrival_airport == 'LAX'
    assert u.aircraft_type == 'Boeing 737'
    assert u.num_seats == 180

def test_read_passenger(db_session):
    """
    GIVEN a DB instance
    WHEN a passenger is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Passenger.query.get(1)
    assert u.first_name == 'John'
    assert u.last_name == 'Doe'
    assert u.booking_details_id == 1

def test_read_payment(db_session):
    """
    GIVEN a DB instance
    WHEN a payment is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = Payment.query.get(3)
    assert u.booking_details_id == 1
    assert u.amount == 800.00
    assert u.payment_method == 'Credit Card'



#Update
def test_user_update(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = User.query.filter_by(email='john.doe@email.com').first()
    u.first_name = 'Jim'
    db_session.commit()

    u2 = User.query.filter_by(email='john.doe@email.com').first()
    assert u2.first_name == 'Jim'

#Delete