from flask import request, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from . import db
import jwt
from src.models import Airline, Flight, Crew, CrewRole, FlightCrewAssignment, Booking, BookingDetail, Passenger, Payment, User

# ----------------------------------------------- #
# Query Object Methods => https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query
# Session Object Methods => https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session
# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
SECRET_KEY = 'A3498fdssADE'

def list_all_controller(class_name):
    class_name = eval(class_name)
    values = class_name.query.all()
    response = []
    for value in values:
        response.append(value.to_dict())
    return jsonify(response)

def login_controller():
    data = request.get_json()
    print(data)
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Both email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Invalid email'}), 401
    if not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid password'}), 401
    if user and check_password_hash(user.password, data['password']):
        token = token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.now() + timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'message': 'Login successful', 'token': token, 'first_name': user.first_name}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# Create
def create_user_controller():
    data = request.get_json()
    if not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already in use'}), 409

    hashed_password = generate_password_hash(data['password'])
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password,
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

def create_booking_controller():
    data = request.get_json()
    if not all(key in data for key in ['user_id', 'flight_id', 'booking_date', 'num_passengers', 'total_cost']):
        return jsonify({'message': 'Missing required fields'}), 400

    booking = Booking(user_id=data['user_id'])
    db.session.add(booking)
    db.session.flush()  # Get the generated booking_id

    booking_detail = BookingDetail(
        booking_id=booking.booking_id,
        flight_id=data['flight_id'],
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date(),
        num_passengers=data['num_passengers'],
        total_cost=data['total_cost']
    )
    db.session.add(booking_detail)
    db.session.commit()
    return jsonify(booking_detail.to_dict()), 201


def create_flight_controller():
    data = request.get_json()
    if not all(key in data for key in ['airline_id', 'flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_type', 'num_seats']):
        return jsonify({'message': 'Missing required fields'}), 400

    flight = Flight(
        airline_id=data['airline_id'],
        flight_number=data['flight_number'],
        departure_airport=data['departure_airport'],
        arrival_airport=data['arrival_airport'],
        departure_time=datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M'),
        arrival_time=datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M'),
        aircraft_type=data['aircraft_type'],
        num_seats=data['num_seats']
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify(flight.to_dict()), 201


def create_crew_controller():
    data = request.get_json()
    if not all(key in data for key in ['first_name', 'last_name']):
        return jsonify({'message': 'Missing required fields'}), 400

    crew = Crew(
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    db.session.add(crew)
    db.session.commit()
    return jsonify(crew.to_dict()), 201


# Read
def search_flights_controller():
    data = request.args
    filters = {key: data[key] for key in data if key in ['departure_airport', 'arrival_airport', 'departure_date']}

    flights = Flight.query.filter_by(**filters).all()
    if not flights:
        return jsonify({'message': 'No flights found'}), 404

    response = [flight.to_dict() for flight in flights]
    response = sorted(response, key=lambda x: x['departure_time'])
    return jsonify(response)


def get_user_profile_controller(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user.to_dict())


def get_booking_history_controller(user_id):
    # Fetch all bookings for the user
    bookings = Booking.query.filter_by(user_id=user_id).all()
    if not bookings:
        return jsonify({'message': 'No bookings found'}), 404

    # Fetch booking details for those bookings
    booking_details = BookingDetail.query.filter(
        BookingDetail.booking_id.in_([booking.booking_id for booking in bookings])
    ).all()

    # Fetch flight details for those booking details
    flight_details = Flight.query.filter(
        Flight.flight_id.in_([detail.flight_id for detail in booking_details])
    ).all()

    # Fetch airline details for those flights
    airline_details = Airline.query.filter(
        Airline.airline_id.in_([flight.airline_id for flight in flight_details])
    ).all()
    
    user_details = User.query.all()

    # Convert airline details into a dictionary for quick lookup
    airlines_dict = {
        airline.airline_id: {
            "airline_name": airline.airline_name,
            "contact_email": airline.contact_email,
            "contact_phone": airline.contact_phone
        } for airline in airline_details
    }

    # Convert flight details into a dictionary and include airline info
    flights_dict = {
        flight.flight_id: {
            "flight_number": flight.flight_number,
            "departure_airport": flight.departure_airport,
            "arrival_airport": flight.arrival_airport,
            "departure_time": flight.departure_time.isoformat(),
            "arrival_time": flight.arrival_time.isoformat(),
            "aircraft_type": flight.aircraft_type,
            "num_seats": flight.num_seats,
            "airline": airlines_dict.get(flight.airline_id)
        } for flight in flight_details
    }
    user_details_dict = {
        user.user_id: {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        } for user in user_details
    }

    # Organize booking details and include flight info
    booking_details_dict = {
        detail.booking_id: {
            "booking_date": detail.booking_date.isoformat(),
            "num_passengers": detail.num_passengers,
            "total_cost": str(detail.total_cost),
            "flight": flights_dict.get(detail.flight_id),
        } for detail in booking_details
    }


    # Create the final response
    response = [
        {
            "bookings": booking_details_dict.get(booking.booking_id),
            "user": user_details_dict.get(user_id)
        } for booking in bookings
    ]

    return jsonify(response)


def get_airline_dashboard_controller(airline_id):
    airline = Airline.query.get(airline_id)
    if airline:
        airline_dict = airline.to_dict()
        airline_dict['flights'] = [flight.to_dict() for flight in airline.flights]
        return jsonify(airline_dict)
    else:
        return jsonify({'message': 'Airline not found'}), 404

# Update
def update_user_profile_controller(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'first_name' in data: user.first_name = data['first_name']
    if 'last_name' in data: user.last_name = data['last_name']
    if 'email' in data: user.email = data['email']
    if 'phone' in data: user.phone = data['phone']
    if 'address' in data: user.address = data['address']

    db.session.commit()
    return jsonify(user.to_dict())


def modify_booking_controller(booking_id):
    data = request.get_json()
    booking_detail = BookingDetail.query.get(booking_id)
    if not booking_detail:
        return jsonify({'message': 'Booking not found'}), 404

    if 'flight_id' in data: booking_detail.flight_id = data['flight_id']
    if 'booking_date' in data: booking_detail.booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    if 'num_passengers' in data: booking_detail.num_passengers = data['num_passengers']
    if 'total_cost' in data: booking_detail.total_cost = data['total_cost']

    db.session.commit()
    return jsonify(booking_detail.to_dict())


def update_flight_schedule_controller(flight_id):
    data = request.get_json()
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({'message': 'Flight not found'}), 404

    if 'departure_airport' in data: flight.departure_airport = data['departure_airport']
    if 'arrival_airport' in data: flight.arrival_airport = data['arrival_airport']
    if 'departure_time' in data: flight.departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M')
    if 'arrival_time' in data: flight.arrival_time = datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M')

    db.session.commit()
    return jsonify(flight.to_dict())


def update_crew_assignment_controller(flight_id):
    data = request.get_json()
    flight_crew_assignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()
    for assignment in flight_crew_assignments:
        db.session.delete(assignment)
    db.session.commit()

    for crew_assignment in data['crew_assignments']:
        crew_id = crew_assignment['crew_id']
        role_id = crew_assignment['role_id']
        new_assignment = FlightCrewAssignment(flight_id=flight_id, crew_id=crew_id, role_id=role_id)
        db.session.add(new_assignment)
    db.session.commit()
    return jsonify({'message': 'Crew assignments updated successfully'})

# Delete
def update_crew_assignment_controller(flight_id):
    data = request.get_json()
    flight_crew_assignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()
    for assignment in flight_crew_assignments:
        db.session.delete(assignment)

    for crew_assignment in data['crew_assignments']:
        new_assignment = FlightCrewAssignment(
            flight_id=flight_id,
            crew_id=crew_assignment['crew_id'],
            role_id=crew_assignment['role_id']
        )
        db.session.add(new_assignment)

    db.session.commit()
    return jsonify({'message': 'Crew assignments updated successfully'})

def cancel_booking_controller(booking_id):
    booking_detail = BookingDetail.query.get(booking_id)
    if not booking_detail:
        return jsonify({'message': 'Booking not found'}), 404

    db.session.delete(booking_detail)
    db.session.commit()
    return jsonify({'message': 'Booking canceled successfully'})


def delete_user_account_controller(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    bookings = Booking.query.filter_by(user_id=user_id).all()
    for booking in bookings:
        booking_details = BookingDetail.query.filter_by(booking_id=booking.booking_id).all()
        for detail in booking_details:
            db.session.delete(detail)
        db.session.delete(booking)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User account deleted successfully'})


def remove_outdated_data_controller():
    current_time = datetime.now()
    outdated_flights = Flight.query.filter(Flight.arrival_time < current_time).all()
    for flight in outdated_flights:
        db.session.delete(flight)

    outdated_crew_assignments = FlightCrewAssignment.query.join(Flight).filter(Flight.arrival_time < current_time).all()
    for assignment in outdated_crew_assignments:
        db.session.delete(assignment)

    db.session.commit()
    return jsonify({'message': 'Outdated operational data removed successfully'})

def get_crew_assignment_controller(flight_id):
    assignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()
    if not assignments:
        return jsonify({'message': 'No crew assignments found'}), 404

    response = []
    for assignment in assignments:
        crew = Crew.query.get(assignment.crew_id)
        role = CrewRole.query.get(assignment.role_id)
        response.append({
            "crew_id": crew.crew_id,
            "first_name": crew.first_name,
            "last_name": crew.last_name,
            "role_id": role.role_id,
            "role_name": role.role_name
        })
    return jsonify(response)
