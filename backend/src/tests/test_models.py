# import pytest
# from datetime import datetime
# from main.dao.models import (
#     User, Airline, Flight, Crew, CrewRole, 
#     Booking, BookingDetail, Passenger, Payment
# )


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
