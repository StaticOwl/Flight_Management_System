import pytest

from main.dao.adapters import delete_user_by_id, delete_airline_by_id, delete_bookingdetail_by_id, delete_booking_by_id, delete_crew_by_id, \
    delete_crewrole_by_id, delete_flightcrewassignment_by_id, delete_flight_by_id, delete_passenger_by_id, delete_paymnet_by_id
from main.dao.models import User, Airline, BookingDetail, Booking, Crew, CrewRole, FlightCrewAssignment, Flight, Passenger, Payment
#Courtesy https://testdriven.io/blog/flask-pytest/
# from datetime import datetime

#CREATE
# def test_user_model(db_session):
#     """Test User model creation and retrieval."""
#     user = User(
#         first_name='John',
#         last_name='Doe',
#         email='john.doe@example.com',
#         password='password123',
#         phone='1234567890',
#         address='123 Main St'
#     )
#     db_session.add(user)
#     db_session.commit()

#     retrieved_user = db_session.query(User).filter_by(email='john.doe@example.com').first()
#     assert retrieved_user is not None
#     assert retrieved_user.first_name == 'John'
#     assert retrieved_user.last_name == 'Doe'


# def test_airline_model(db_session):
#     """Test Airline model creation and retrieval."""
#     airline = Airline(
#         airline_name='Test Airline',
#         contact_email='contact@testairline.com',
#         contact_phone='9876543210'
#     )
#     db_session.add(airline)
#     db_session.commit()
#     retrieved_airline = db_session.query(Airline).filter_by(airline_name='Test Airline').first()
#     assert retrieved_airline is not None
#     assert retrieved_airline.contact_email == 'contact@testairline.com'

# def test_flight_model(db_session):
#     """Test Flight model creation and retrieval."""
#     airline = Airline(
#         airline_name='Test Airline',
#         contact_email='contact@testairline.com',
#         contact_phone='9876543210'
#     )
#     db_session.add(airline)
#     db_session.commit()

#     flight = Flight(
#         airline_id=airline.airline_id,
#         flight_number='TEST123',
#         departure_airport='JFK',
#         arrival_airport='LAX',
#         departure_time=datetime.now(),
#         arrival_time=datetime.now(),
#         aircraft_type='Boeing 747',
#         num_seats=300,
#         price_per_seat=199.99
#     )
#     db_session.add(flight)
#     db_session.commit()

#     retrieved_flight = db_session.query(Flight).filter_by(flight_number='TEST123').first()
#     assert retrieved_flight is not None
#     assert retrieved_flight.aircraft_type == 'Boeing 747'


# def test_crew_model(db_session):
#     """Test Crew model creation and retrieval."""
#     crew = Crew(
#         first_name='Jane',
#         last_name='Doe'
#     )
#     db_session.add(crew)
#     db_session.commit()

#     retrieved_crew = db_session.query(Crew).filter_by(first_name='Jane').first()
#     assert retrieved_crew is not None
#     assert retrieved_crew.last_name == 'Doe'


# def test_crew_role_model(db_session):
#     """Test CrewRole model creation and retrieval."""
#     crew_role = CrewRole(role_name='Pilot')
#     db_session.add(crew_role)
#     db_session.commit()

#     retrieved_crew_role = db_session.query(CrewRole).filter_by(role_name='Pilot').first()
#     assert retrieved_crew_role is not None
#     assert retrieved_crew_role.role_name == 'Pilot'


# def test_booking_model(db_session):
#     """Test Booking model creation and retrieval."""
#     user = User(
#         first_name='John',
#         last_name='Doe',
#         email='john.doe@example.com',
#         password='password123',
#         phone='1234567890',
#         address='123 Main St'
#     )
#     db_session.add(user)
#     db_session.commit()

#     booking = Booking(user_id=user.user_id)
#     db_session.add(booking)
#     db_session.commit()

#     retrieved_booking = db_session.query(Booking).filter_by(user_id=user.user_id).first()
#     assert retrieved_booking is not None
#     assert retrieved_booking.user_id == user.user_id


# def test_booking_detail_model(db_session):
#     """Test BookingDetail model creation and retrieval."""
#     user = User(
#         first_name='John',
#         last_name='Doe',
#         email='john.doe@example.com',
#         password='password123',
#         phone='1234567890',
#         address='123 Main St'
#     )
#     db_session.add(user)
#     db_session.commit()

#     airline = Airline(
#         airline_name='Test Airline',
#         contact_email='contact@testairline.com',
#         contact_phone='9876543210'
#     )
#     db_session.add(airline)
#     db_session.commit()

#     flight = Flight(
#         airline_id=airline.airline_id,
#         flight_number='TEST123',
#         departure_airport='JFK',
#         arrival_airport='LAX',
#         departure_time=datetime.now(),
#         arrival_time=datetime.now(),
#         aircraft_type='Boeing 747',
#         num_seats=300,
#         price_per_seat=199.99
#     )
#     db_session.add(flight)
#     db_session.commit()

#     booking = Booking(user_id=user.user_id)
#     db_session.add(booking)
#     db_session.commit()

#     booking_detail = BookingDetail(
#         booking_id=booking.booking_id,
#         flight_id=flight.flight_id,
#         booking_date=datetime.now(),
#         num_passengers=2,
#         total_cost=399.98
#     )
#     db_session.add(booking_detail)
#     db_session.commit()

#     retrieved_booking_detail = db_session.query(BookingDetail).filter_by(booking_id=booking.booking_id).first()
#     assert retrieved_booking_detail is not None
#     assert retrieved_booking_detail.num_passengers == 2


# def test_passenger_model(db_session):
#     """Test Passenger model creation and retrieval."""
#     passenger = Passenger(
#         first_name='Alice',
#         last_name='Smith',
#         date_of_birth=datetime.now()
#     )
#     db_session.add(passenger)
#     db_session.commit()

#     retrieved_passenger = db_session.query(Passenger).filter_by(first_name='Alice').first()
#     assert retrieved_passenger is not None
#     assert retrieved_passenger.last_name == 'Smith'


# def test_payment_model(db_session):
#     """Test Payment model creation and retrieval."""
#     user = User(
#         first_name='John',
#         last_name='Doe',
#         email='john.doe@example.com',
#         password='password123',
#         phone='1234567890',
#         address='123 Main St'
#     )
#     db_session.add(user)
#     db_session.commit()

#     airline = Airline(
#         airline_name='Test Airline',
#         contact_email='contact@testairline.com',
#         contact_phone='9876543210'
#     )
#     db_session.add(airline)
#     db_session.commit()

#     flight = Flight(
#         airline_id=airline.airline_id,
#         flight_number='TEST123',
#         departure_airport='JFK',
#         arrival_airport='LAX',
#         departure_time=datetime.now(),
#         arrival_time=datetime.now(),
#         aircraft_type='Boeing 747',
#         num_seats=300,
#         price_per_seat=199.99
#     )
#     db_session.add(flight)
#     db_session.commit()

#     booking = Booking(user_id=user.user_id)
#     db_session.add(booking)
#     db_session.commit()

#     booking_detail = BookingDetail(
#         booking_id=booking.booking_id,
#         flight_id=flight.flight_id,
#         booking_date=datetime.now(),
#         num_passengers=2,
#         total_cost=399.98
#     )
#     db_session.add(booking_detail)
#     db_session.commit()

#     payment = Payment(
#         booking_details_id=booking_detail.booking_details_id,
#         payment_date=datetime.now(),
#         amount=399.98,
#         payment_method='Credit Card'
#     )
#     db_session.add(payment)
#     db_session.commit()

#     retrieved_payment = db_session.query(Payment).filter_by(payment_method='Credit Card').first()
#     assert retrieved_payment is not None
#     assert retrieved_payment.amount == 399.98

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
    u = CrewRole.query.get(1)
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

def test_update_airline(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Airline.query.get(1)
    u.airline_name = 'AirLine Two'
    db_session.commit()

    u2 = Airline.query.get(1)
    assert u2.airline_name == 'AirLine Two'

def test_update_bookingdetail(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = BookingDetail.query.get(1)
    u.total_cost = 900.50
    db_session.commit()

    u2 = BookingDetail.query.get(1)
    assert u2.total_cost == 900.50

def test_update_booking(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Booking.query.get(1)
    u.user_id = 2
    db_session.commit()

    u2 = Booking.query.get(1)
    assert u2.user_id == 2

def test_update_crew(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Crew.query.get(1)
    u.first_name = 'Arial'
    db_session.commit()

    u2 = Crew.query.get(1)
    assert u2.first_name == 'Arial'

def test_update_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = CrewRole.query.get(1)
    u.role_name = 'Jim'
    db_session.commit()

    u2 = CrewRole.query.get(1)
    assert u2.role_name == 'Jim'

def test_update_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = FlightCrewAssignment.query.get(1)
    u.flight_id = 5
    db_session.commit()

    u2 = FlightCrewAssignment.query.get(1)
    assert u2.flight_id == 5

def test_update_flight(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Flight.query.get(1)
    u.aircraft_type = 'Boeing 787'
    db_session.commit()

    u2 = Flight.query.get(1)
    assert u2.aircraft_type == 'Boeing 787'

def test_update_passenger(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Passenger.query.get(1)
    u.first_name = 'Jim'
    db_session.commit()

    u2 = Passenger.query.get(1)
    assert u2.first_name == 'Jim'

def test_update_payment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    u = Payment.query.get(1)
    u.amount = 900.50
    db_session.commit()

    u2 = Payment.query.get(1)
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

    u2 = Airline.query.get(1)
    assert not u2

def test_delete_bookingdetail(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_bookingdetail_by_id(db_session, 1, True)

    u2 = BookingDetail.query.get(1)
    assert not u2

def test_delete_booking(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_booking_by_id(db_session, 1, True)

    u2 = Booking.query.get(1)
    assert not u2

def test_delete_crew(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_crew_by_id(db_session, 1, True)

    u2 = Crew.query.get(1)
    assert not u2

def test_delete_crewrole(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_crewrole_by_id(db_session, 1, True)

    u2 = CrewRole.query.get(1)
    assert not u2

def test_delete_flightcrewassignment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_flightcrewassignment_by_id(db_session, 1)

    u2 = FlightCrewAssignment.query.get(1)
    assert not u2

def test_delete_flight(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_flight_by_id(db_session, 1)

    u2 = Flight.query.get(1)
    assert not u2

def test_delete_passenger(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_passenger_by_id(db_session, 1)

    u2 = Passenger.query.get(1)
    assert not u2

def test_delete_payment(db_session):
    """
    GIVEN a DB instance
    WHEN an existing user is written to the DB
    THEN check that the retrieved data matches the intended write

    TESTS SQLAlchemy setup for Update
    """
    delete_paymnet_by_id(db_session, 1)

    u2 = Payment.query.get(1)
    assert not u2