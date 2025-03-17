from flask import request, jsonify, make_response, request, current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from main.__init__ import db
import jwt
from sqlalchemy.exc import SQLAlchemyError
from main.dao.models import Airline, Flight, Crew, CrewRole, FlightCrewAssignment, Booking, BookingDetail, Passenger, Payment, User

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
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Both email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': "User doesn't exist"}), 401
    if user and (check_password_hash(user.password, data['password']) or data['password'] == user.password):
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.now() + timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({'message': 'Login successful', 'token': token, 'first_name': user.first_name}), 200
    else:
        return jsonify({'message': 'Invalid password'}), 401
    
def get_user_id_from_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {'user_id': decoded['user_id']}
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    
def set_token_user_id(user_id):
    token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.now() + timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
    return {"token": token}
    

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
    print(data)
    if not all(key in data for key in ['token', 'flight_id', 'booking_date', 'num_passengers', 'total_cost']):
        return jsonify({'message': 'Missing required fields'}), 400

    if not db.session.get(Flight, data['flight_id']):
        return jsonify({'message': 'Invalid flight'}), 400
    
    user_id = get_user_id_from_token(data['token'])['user_id']
    booking = Booking(user_id=user_id)
    db.session.add(booking)
    db.session.flush()  # Get the generated booking_id

    latest_booking_detail = BookingDetail.query.order_by(BookingDetail.booking_details_id.desc()).first().to_dict()['booking_details_id']
    booking_detail = BookingDetail(
        booking_details_id=latest_booking_detail+1,
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
    if not db.session.get(Airline, data['airline_id']):
        return jsonify({'message': 'Invalid airline'}), 400

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


def update_crew_controller(crew_id):
    data = request.get_json()
    
    # Find the crew member by ID
    crew = Crew.query.get(crew_id)
    if not crew:
        return make_response(jsonify({"message": "Crew member not found"}), 404)
    
    # Update the crew member's details
    try:
        crew.first_name = data.get('first_name', crew.first_name)
        crew.last_name = data.get('last_name', crew.last_name)
        
        # Optionally, update other fields if needed
        # crew.flight_id = data.get('flight_id', crew.flight_id)
        # crew.role_id = data.get('role_id', crew.role_id)

        db.session.commit()
        return jsonify(crew.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Database error", "error": str(e)}), 500)


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


def get_user_profile_controller(token):
    user_id = get_user_id_from_token(token)['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user.to_dict())


def get_booking_history_controller(token):
    # Fetch all bookings for the user
    user_id = get_user_id_from_token(token)['user_id']
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
            "booking_id": detail.booking_id,
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
    
    print(response)

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
def update_user_profile_controller(token):
    data = request.get_json()
    user_id = get_user_id_from_token(token)['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    print(data)

    if 'first_name' in data: user.first_name = data['first_name']
    if 'last_name' in data: user.last_name = data['last_name']
    if 'email' in data: user.email = data['email']
    if 'phone' in data: user.phone = data['phone']
    if 'address' in data: user.address = data['address']
    if 'current' in data:
        print(data['current'])
        password = data['current']
        if check_password_hash(user.password) == password:
            user.password = generate_password_hash(data['new'])
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


# def update_flight_schedule_controller(flight_id):
#     data = request.get_json()
#     flight = Flight.query.get(flight_id)
#     if not flight:
#         return jsonify({'message': 'Flight not found'}), 404
#
#     if 'departure_airport' in data: flight.departure_airport = data['departure_airport']
#     if 'arrival_airport' in data: flight.arrival_airport = data['arrival_airport']
#     if 'departure_time' in data: flight.departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M')
#     if 'arrival_time' in data: flight.arrival_time = datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M')
#
#     db.session.commit()
#     return jsonify(flight.to_dict())


# Delete
def update_crew_assignment_controller(flight_id):
    data = request.get_json()
    flight_crew_assignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()
    for assignment in flight_crew_assignments:
        db.session.delete(assignment)
    if not db.session.get(Crew, data['crew_id']):
        return jsonify({'message': 'Invalid crew'})
    if not db.session.get(CrewRole, data['role_id']):
        return jsonify({'message': 'Invalid role'})

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
    booking_detail = BookingDetail.query.filter_by(booking_id=booking_id).all()
    booking = Booking.query.get(booking_id)
    if not (booking_detail or booking):
        return jsonify({'message': 'Booking not found'}), 404
    for detail in booking_detail:
        db.session.delete(detail)

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking canceled successfully', 'success':True})


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

def fetch_airlines(airline_id=None):
    if not airline_id:
        airlines = Airline.query.all()
        response = [{"id": airline.airline_id, "name": airline.airline_name} for airline in airlines]
    
        return response
    else:
        flights = Flight.query.filter_by(airline_id=airline_id).all()
        if not flights:
            return jsonify({'message':'No Flight found for this airline'}), 401
        response = [{
            "id": flight.flight_id, 
            "flight_number": flight.flight_number,
            "departure_airport": flight.departure_airport,
            "arrival_airport": flight.arrival_airport,
            "price_per_seat": flight.price_per_seat
            } for flight in flights]
        return response
    
def get_crews():
    # Join the Crew, FlightCrewAssignment, Flight, and CrewRole tables to gather all related information
    crew_assignments = db.session.query(
        Crew.crew_id,
        Crew.first_name,
        Crew.last_name,
        Flight.flight_number,
        Flight.departure_airport,
        Flight.arrival_airport,
        CrewRole.role_name
    ).join(FlightCrewAssignment, Crew.crew_id == FlightCrewAssignment.crew_id
    ).join(Flight, Flight.flight_id == FlightCrewAssignment.flight_id
    ).join(CrewRole, CrewRole.role_id == FlightCrewAssignment.role_id
    ).all()

    # Construct the response
    response = [{
        "id": assignment.crew_id,
        "name": f"{assignment.first_name} {assignment.last_name}",
        "flight_number": assignment.flight_number,
        "departure_airport": assignment.departure_airport,
        "arrival_airport": assignment.arrival_airport,
        "role": assignment.role_name
    } for assignment in crew_assignments]

    return response

def add_crew_controller():
    data = request.get_json()
    if not all(key in data for key in ['first_name', 'last_name', 'flight_id', 'role_id']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Start a transaction
    try:
        last_crew = Crew.query.order_by(Crew.crew_id.desc()).first().to_dict()['crew_id']
        # Create a new crew member
        new_crew = Crew(
            crew_id=last_crew+1,
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        db.session.add(new_crew)
        db.session.flush()

        # Create a flight crew assignment
        new_assignment = FlightCrewAssignment(
            flight_id=data['flight_id'],
            crew_id=new_crew.crew_id,
            role_id=data['role_id']
        )
        db.session.add(new_assignment)
        
        # Commit the transaction
        db.session.commit()
        return jsonify({
            'crew_id': new_crew.crew_id,
            'first_name': new_crew.first_name,
            'last_name': new_crew.last_name,
            'flight_id': new_assignment.flight_id,
            'role_id': new_assignment.role_id
        }), 201
    except Exception as e:
        db.session.rollback()  # Rollback the transaction on error
        return jsonify({'message': str(e)}), 500
    
def fetch_flights_controller():
    flights = Flight.query.all()
    response = [flight.to_dict() for flight in flights]
    return response

def fetch_roles_controller():
    roles = CrewRole.query.all()
    response = [role.to_dict() for role in roles]
    print(response)
    return response