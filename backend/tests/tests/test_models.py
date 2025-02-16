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

class TestModels(unittest.TestCase):
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

    def test_user_model(self):
        """Test User model creation and retrieval"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890',
            address='123 Main St'
        )
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.first_name, 'John')
        self.assertEqual(retrieved_user.last_name, 'Doe')

    def test_airline_model(self):
        """Test Airline model creation and retrieval"""
        airline = Airline(
            airline_name='Test Airline',
            contact_email='contact@testairline.com',
            contact_phone='9876543210'
        )
        db.session.add(airline)
        db.session.commit()

        retrieved_airline = Airline.query.filter_by(airline_name='Test Airline').first()
        self.assertIsNotNone(retrieved_airline)
        self.assertEqual(retrieved_airline.contact_email, 'contact@testairline.com')

    def test_flight_model(self):
        """Test Flight model creation and retrieval"""
        airline = Airline(
            airline_name='Test Airline',
            contact_email='contact@testairline.com',
            contact_phone='9876543210'
        )
        db.session.add(airline)
        db.session.commit()

        flight = Flight(
            airline_id=airline.airline_id,
            flight_number='TEST123',
            departure_airport='JFK',
            arrival_airport='LAX',
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
        self.assertEqual(retrieved_flight.aircraft_type, 'Boeing 747')

    def test_crew_model(self):
        """Test Crew model creation and retrieval"""
        crew = Crew(
            first_name='Jane',
            last_name='Doe'
        )
        db.session.add(crew)
        db.session.commit()

        retrieved_crew = Crew.query.filter_by(first_name='Jane').first()
        self.assertIsNotNone(retrieved_crew)
        self.assertEqual(retrieved_crew.last_name, 'Doe')

    def test_crew_role_model(self):
        """Test CrewRole model creation and retrieval"""
        crew_role = CrewRole(
            role_name='Pilot'
        )
        db.session.add(crew_role)
        db.session.commit()

        retrieved_crew_role = CrewRole.query.filter_by(role_name='Pilot').first()
        self.assertIsNotNone(retrieved_crew_role)
        self.assertEqual(retrieved_crew_role.role_name, 'Pilot')

    def test_booking_model(self):
        """Test Booking model creation and retrieval"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890',
            address='123 Main St'
        )
        db.session.add(user)
        db.session.commit()

        booking = Booking(
            user_id=user.user_id
        )
        db.session.add(booking)
        db.session.commit()

        retrieved_booking = Booking.query.filter_by(user_id=user.user_id).first()
        self.assertIsNotNone(retrieved_booking)
        self.assertEqual(retrieved_booking.user_id, user.user_id)

    def test_booking_detail_model(self):
        """Test BookingDetail model creation and retrieval"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890',
            address='123 Main St'
        )
        db.session.add(user)
        db.session.commit()

        airline = Airline(
            airline_name='Test Airline',
            contact_email='contact@testairline.com',
            contact_phone='9876543210'
        )
        db.session.add(airline)
        db.session.commit()

        flight = Flight(
            airline_id=airline.airline_id,
            flight_number='TEST123',
            departure_airport='JFK',
            arrival_airport='LAX',
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
            aircraft_type='Boeing 747',
            num_seats=300,
            price_per_seat=199.99
        )
        db.session.add(flight)
        db.session.commit()

        booking = Booking(
            user_id=user.user_id
        )
        db.session.add(booking)
        db.session.commit()

        booking_detail = BookingDetail(
            booking_id=booking.booking_id,
            flight_id=flight.flight_id,
            booking_date=datetime.now(),
            num_passengers=2,
            total_cost=399.98
        )
        db.session.add(booking_detail)
        db.session.commit()

        retrieved_booking_detail = BookingDetail.query.filter_by(booking_id=booking.booking_id).first()
        self.assertIsNotNone(retrieved_booking_detail)
        self.assertEqual(retrieved_booking_detail.num_passengers, 2)

    def test_passenger_model(self):
        """Test Passenger model creation and retrieval"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890',
            address='123 Main St'
        )
        db.session.add(user)
        db.session.commit()

        airline = Airline(
            airline_name='Test Airline',
            contact_email='contact@testairline.com',
            contact_phone='9876543210'
        )
        db.session.add(airline)
        db.session.commit()

        flight = Flight(
            airline_id=airline.airline_id,
            flight_number='TEST123',
            departure_airport='JFK',
            arrival_airport='LAX',
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
            aircraft_type='Boeing 747',
            num_seats=300,
            price_per_seat=199.99
        )
        db.session.add(flight)
        db.session.commit()

        booking = Booking(
            user_id=user.user_id
        )
        db.session.add(booking)
        db.session.commit()

        booking_detail = BookingDetail(
            booking_id=booking.booking_id,
            flight_id=flight.flight_id,
            booking_date=datetime.now(),
            num_passengers=2,
            total_cost=399.98
        )
        db.session.add(booking_detail)
        db.session.commit()

        passenger = Passenger(
            booking_details_id=booking_detail.booking_details_id,
            first_name='Alice',
            last_name='Smith',
            date_of_birth=datetime.now()
        )
        db.session.add(passenger)
        db.session.commit()

        retrieved_passenger = Passenger.query.filter_by(first_name='Alice').first()
        self.assertIsNotNone(retrieved_passenger)
        self.assertEqual(retrieved_passenger.last_name, 'Smith')

    def test_payment_model(self):
        """Test Payment model creation and retrieval"""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890',
            address='123 Main St'
        )
        db.session.add(user)
        db.session.commit()

        airline = Airline(
            airline_name='Test Airline',
            contact_email='contact@testairline.com',
            contact_phone='9876543210'
        )
        db.session.add(airline)
        db.session.commit()

        flight = Flight(
            airline_id=airline.airline_id,
            flight_number='TEST123',
            departure_airport='JFK',
            arrival_airport='LAX',
            departure_time=datetime.now(),
            arrival_time=datetime.now(),
            aircraft_type='Boeing 747',
            num_seats=300,
            price_per_seat=199.99
        )
        db.session.add(flight)
        db.session.commit()

        booking = Booking(
            user_id=user.user_id
        )
        db.session.add(booking)
        db.session.commit()

        booking_detail = BookingDetail(
            booking_id=booking.booking_id,
            flight_id=flight.flight_id,
            booking_date=datetime.now(),
            num_passengers=2,
            total_cost=399.98
        )
        db.session.add(booking_detail)
        db.session.commit()

        payment = Payment(
            booking_details_id=booking_detail.booking_details_id,
            payment_date=datetime.now(),
            amount=399.98,
            payment_method='Credit Card'
        )
        db.session.add(payment)
        db.session.commit()

        retrieved_payment = Payment.query.filter_by(payment_method='Credit Card').first()
        self.assertIsNotNone(retrieved_payment)
        self.assertEqual(retrieved_payment.amount, 399.98)

    