from datetime import datetime
from main.dao.models import (
    User, Airline, Flight
)
from sqlalchemy import inspect
from datetime import datetime

from sqlalchemy import inspect

from main.dao.models import (
    User, Airline, Flight
)


def test_database_tables_exist(db_session):
    """Test if all database tables were created"""
    inspector = inspect(db_session.get_bind())
    tables = set(inspector.get_table_names())
    
    expected_tables = {
        'users',
        'airlines',
        'flights',
        'crews',
        'crewroles',
        'bookings',
        'bookingdetails',
        'passengers',
        'payments',
        'flightcrewassignments'
    }
    
    assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"

def test_table_columns(db_session):
    """Test if tables have the correct columns."""
    inspector = inspect(db_session.get_bind())
    
    # Test User table columns
    user_columns = {col['name'] for col in inspector.get_columns('Users')}
    assert user_columns == {'user_id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'role'}

    # Test Flight table columns
    flight_columns = {col['name'] for col in inspector.get_columns('Flights')}
    assert flight_columns == {
        'flight_id', 'airline_id', 'flight_number', 'departure_airport',
        'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_type',
        'num_seats', 'price_per_seat'
    }

    # Test BookingDetail table columns
    booking_columns = {col['name'] for col in inspector.get_columns('BookingDetails')}
    assert booking_columns == {'booking_details_id', 'booking_id', 'flight_id', 'booking_date', 'num_passengers', 'total_cost'}


def test_create_user(db_session):
    """Test if we can create a user."""
    user = User(
        first_name='Test',
        last_name='User',
        email='test@test.com',
        password='password123',
        phone='1234567890',
        address='123 Test St'
    )
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(email='test@test.com').first()
    assert retrieved_user is not None
    assert retrieved_user.first_name == 'Test'

def test_create_airline_and_flight(db_session):
    """Test if we can create an airline and associated flight."""
    airline = Airline(
        airline_name='Test Airline',
        contact_email='airline@test.com',
        contact_phone='1234567890'
    )
    db_session.add(airline)
    db_session.commit()

    flight = Flight(
        airline_id=airline.airline_id,
        flight_number='TEST123',
        departure_airport='TEST1',
        arrival_airport='TEST2',
        departure_time=datetime.now(),
        arrival_time=datetime.now(),
        aircraft_type='Boeing 747',
        num_seats=300,
        price_per_seat=199.99
    )
    db_session.add(flight)
    db_session.commit()

    retrieved_flight = db_session.query(Flight).filter_by(flight_number='TEST123').first()
    assert retrieved_flight is not None
    assert retrieved_flight.airline_ref.airline_name == 'Test Airline'