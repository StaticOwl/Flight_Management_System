import pytest

from main.dao.adapters import delete_user_by_id, delete_airline_by_id, delete_booking_detail_by_id, delete_booking_by_id, delete_crew_by_id, \
    delete_crewrole_by_id, delete_flightcrewassignment_by_id, delete_flight_by_id, delete_passenger_by_id, delete_paymnet_by_id
from main.dao.models import User, Airline, BookingDetail, Booking, Crew, CrewRole, FlightCrewAssignment, Flight, Passenger, Payment

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
    u = db_session.get(Airline, 1)
    assert u.airline_name == 'AirLine One'
    assert u.contact_email == 'contact@airlineone.com'

def test_read_bookingdetail(db_session):
    """
    GIVEN a DB instance
    WHEN a booking detail is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = db_session.get(BookingDetail, 1)
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
    u = db_session.get(Booking, 2)
    assert u.user_id == 2

def test_read_crew(db_session):
    """
    GIVEN a DB instance
    WHEN a crew is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = db_session.get(Crew, 1)
    assert u.first_name == 'Alice'
    assert u.last_name == 'Taylor'

def test_read_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN a crew role is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = db_session.get(CrewRole, 1)
    assert u.role_name == 'Pilot'

def test_read_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN a flight crew assignment is retrieved from the DB
    THEN check that the data matches the seed data

    TESTS SQLAlchemy setup for READ
    """
    u = db_session.get(FlightCrewAssignment, 1)
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
    u = db_session.get(Flight, 1)
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
    u = db_session.get(Passenger, 1)
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
    u = db_session.get(Payment, 3)
    assert u.booking_details_id == 3
    assert u.amount == 1000.00
    assert u.payment_method == 'PayPal'



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

def test_update_airline(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Airline, 1)
    u.airline_name = 'AirLine Two'
    db_session.commit()

    u2 = db_session.get(Airline, 1)
    assert u2.airline_name == 'AirLine Two'

def test_update_bookingdetail(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(BookingDetail, 1)
    u.total_cost = 900.50
    db_session.commit()

    u2 = db_session.get(BookingDetail, 1)
    assert u2.total_cost == 900.50

def test_update_booking(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Booking, 1)
    u.user_id = 2
    db_session.commit()

    u2 = db_session.get(Booking, 1)
    assert u2.user_id == 2

def test_update_crew(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Crew, 1)
    u.first_name = 'Arial'
    db_session.commit()

    u2 = db_session.get(Crew, 1)
    assert u2.first_name == 'Arial'

def test_update_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(CrewRole, 1)
    u.role_name = 'Jim'
    db_session.commit()

    u2 = db_session.get(CrewRole, 1)
    assert u2.role_name == 'Jim'

def test_update_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(FlightCrewAssignment, 1)
    u.flight_id = 5
    db_session.commit()

    u2 = db_session.get(FlightCrewAssignment, 1)
    assert u2.flight_id == 5

def test_update_flight(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Flight, 1)
    u.aircraft_type = 'Boeing 787'
    db_session.commit()

    u2 = db_session.get(Flight, 1)
    assert u2.aircraft_type == 'Boeing 787'

def test_update_passenger(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Passenger, 1)
    u.first_name = 'Jim'
    db_session.commit()

    u2 = db_session.get(Passenger, 1)
    assert u2.first_name == 'Jim'

def test_update_payment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = db_session.get(Payment, 1)
    u.amount = 900.50
    db_session.commit()

    u2 = db_session.get(Payment, 1)
    assert u2.amount == 900.50

#Delete
def test_user_delete(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = User.query.filter_by(email='john.doe@email.com').first()
    delete_user_by_id(db_session, u.user_id)

    u2 = User.query.filter_by(email='john.doe@email.com').first()
    assert not u2

def test_delete_airline(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_airline_by_id(db_session, 1, True)

    u2 = db_session.get(Airline, 1)
    assert not u2

def test_delete_booking_detail(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_booking_detail_by_id(db_session, 1, True)

    u2 = db_session.get(BookingDetail, 1)
    assert not u2

def test_delete_booking(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_booking_by_id(db_session, 1, True)

    u2 = db_session.get(Booking, 1)
    assert not u2

def test_delete_crew(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_crew_by_id(db_session, 1, True)

    u2 = db_session.get(Crew, 1)
    assert not u2

def test_delete_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_crewrole_by_id(db_session, 1, True)

    u2 = db_session.get(CrewRole, 1)
    assert not u2

def test_delete_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_flightcrewassignment_by_id(db_session, 1)

    u2 = db_session.get(FlightCrewAssignment, 1)
    assert not u2

def test_delete_flight(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_flight_by_id(db_session, 1)

    u2 = db_session.get(Flight, 1)
    assert not u2

def test_delete_passenger(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_passenger_by_id(db_session, 1)

    u2 = db_session.get(Passenger, 1)
    assert not u2

def test_delete_payment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_paymnet_by_id(db_session, 1)

    u2 = db_session.get(Payment, 1)
    assert not u2