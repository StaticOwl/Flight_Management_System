import unittest
import sys
import os
from datetime import datetime
from pathlib import Path

# Get the absolute path to the src directory
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

from flask import current_app
from src.__init__ import create_app, db
from src.models import (
    User, Airline, Flight, Crew, CrewRole, 
    Booking, BookingDetail, Passenger, Payment, 
    FlightCrewAssignment
)

class TestDatabaseCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test application"""
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Clean up test application context"""
        cls.app_context.pop()

    def setUp(self):
        """Set up test database"""
        db.create_all()

    def tearDown(self):
        """Clean up test database"""
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        """Test if Flask application exists"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Test if Flask application is in testing configuration"""
        self.assertTrue(current_app.config['TESTING'])

    def test_database_tables_exist(self):
        """Test if all database tables were created"""
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = {
            'users',
            'airlines',
            'flights',
            'crew',
            'crew_roles',
            'bookings',
            'booking_details',
            'passengers',
            'payments',
            'flight_crew_assignments'
        }
        
        for table in expected_tables:
            self.assertIn(table, tables, f"Table {table} was not created")

    def test_table_columns(self):
        """Test if tables have the correct columns"""
        inspector = db.inspect(db.engine)
        
        # Test User table columns
        columns = {col['name'] for col in inspector.get_columns('users')}
        expected_columns = {'user_id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address'}
        self.assertEqual(columns, expected_columns)
        
        # Test Flight table columns
        columns = {col['name'] for col in inspector.get_columns('flights')}
        expected_columns = {'flight_id', 'airline_id', 'flight_number', 'departure_airport', 
                          'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_type', 
                          'num_seats', 'price_per_seat'}
        self.assertEqual(columns, expected_columns)
        
        # Test BookingDetail table columns
        columns = {col['name'] for col in inspector.get_columns('booking_details')}
        expected_columns = {'booking_details_id', 'booking_id', 'flight_id', 'booking_date', 
                          'num_passengers', 'total_cost'}
        self.assertEqual(columns, expected_columns)

    def test_create_user(self):
        """Test if we can create a user"""
        user = User(
            first_name='Test',
            last_name='User',
            email='test@test.com',
            password='password123',
            phone='1234567890',
            address='123 Test St'
        )
        db.session.add(user)
        db.session.commit()
        
        retrieved_user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, 'Test')

    def test_create_airline_and_flight(self):
        """Test if we can create an airline and associated flight"""
        airline = Airline(
            airline_name='Test Airline',
            contact_email='airline@test.com',
            contact_phone='1234567890'
        )
        db.session.add(airline)
        db.session.commit()

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
        db.session.add(flight)
        db.session.commit()

        retrieved_flight = Flight.query.filter_by(flight_number='TEST123').first()
        self.assertIsNotNone(retrieved_flight)
        self.assertEqual(retrieved_flight.airline.airline_name, 'Test Airline')

if __name__ == '__main__':
    unittest.main()