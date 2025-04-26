from flask import request, jsonify, make_response, request, current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from main.__init__ import db
import jwt
from sqlalchemy.exc import SQLAlchemyError
from main.dao.models import Airline, Flight, Crew, CrewRole, FlightCrewAssignment, Booking, BookingDetail, Passenger, Payment, User
from main.dao.adapters import (
    # Create
    create_user, create_booking, create_booking_detail, create_flight, create_crew, create_flight_crew_assignment,

    # Get by ID
    get_user_by_id, get_airline_by_id, get_flight_by_id, get_booking_by_id, get_booking_detail_by_id, get_crew_by_id,
    get_flightcrewassignment_by_id, get_payment_by_id,

    # Get by Foreign Key
    get_flights_by_airline_id, get_booking_details_by_booking_id, get_booking_details_by_flight_id, get_bookings_by_user_id,
    get_passengers_by_booking_detail_id, get_payments_by_booking_detail_id, get_flightcrewassignments_by_flight_id,
    get_flightcrewassignments_by_crew_id, get_flightcrewassignments_by_role_id,

    # Update
    update_user, update_crew, update_booking_detail, update_flight, update_payment,

    # Delete
    delete_user_by_id, delete_booking_by_id, delete_booking_detail_by_id, delete_flight_by_id,
    delete_flightcrewassignment_by_id, delete_passenger_by_id, delete_payment_by_id
)
import main.dao.adapters as adapter

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

    all_users = get_user_by_id(db.session, None)
    user = next((u for u in all_users if u.email == data['email']), None)

    if not user:
        return jsonify({'message': "User doesn't exist"}), 401

    if check_password_hash(user.password, data['password']) or data['password'] == user.password:
        token = jwt.encode({
            'user_id': user.user_id,
            'role': user.role,
            'exp': datetime.now() + timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'first_name': user.first_name,
            'role': user.role
        }), 200
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

    if get_user_by_id(db.session, None):
        for user in get_user_by_id(db.session, None):
            if user.email == data['email']:
                return jsonify({'message': 'Email already in use'}), 409

    hashed_password = generate_password_hash(data['password'])
    user = create_user(
        db_session=db.session,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        hashed_password=hashed_password,
        phone=data.get('phone'),
        address=data.get('address'),
        booking_ref=[]
    )
    return jsonify(user.to_dict()), 201



def create_booking_controller():
    data = request.get_json()
    if not all(key in data for key in ['token', 'flight_id', 'booking_date', 'num_passengers', 'total_cost']):
        return jsonify({'message': 'Missing required fields'}), 400

    user_id = get_user_id_from_token(data['token'])['user_id']
    booking = create_booking(
        db_session=db.session,
        user_id=user_id
    )

    latest_id = max([b.booking_details_id for b in get_booking_detail_by_id(db.session, None)])

    booking_detail = create_booking_detail(
        db_session=db.session,
        booking_id=booking.booking_id,
        flight_id=data['flight_id'],
        booking_date=datetime.strptime(data['booking_date'], '%Y-%m-%d').date(),
        num_passengers=data['num_passengers'],
        total_cost=data['total_cost']
    )

    return jsonify(booking_detail.to_dict()), 201


def create_flight_controller():
    data = request.get_json()
    if not all(key in data for key in ['airline_id', 'flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'aircraft_type', 'num_seats']):
        return jsonify({'message': 'Missing required fields'}), 400

    flight = create_flight(
        db_session=db.session,
        airline_id=data['airline_id'],
        flight_number=data['flight_number'],
        departure_airport=data['departure_airport'],
        arrival_airport=data['arrival_airport'],
        departure_time=datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M'),
        arrival_time=datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M'),
        aircraft_type=data['aircraft_type'],
        num_seats=data['num_seats'],
        price_per_seat=data.get('price_per_seat')
    )
    return jsonify(flight.to_dict()), 201


def update_crew_controller(crew_id):
    data = request.get_json()
    crew = get_crew_by_id(db.session, crew_id)
    if not crew:
        return make_response(jsonify({"message": "Crew member not found"}), 404)

    try:
        crew.first_name = data.get('first_name', crew.first_name)
        crew.last_name = data.get('last_name', crew.last_name)
        crew = update_crew(db.session, crew)
        return jsonify(crew.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Database error", "error": str(e)}), 500)

def update_user_controller(user_id):  #pragma: no cover
    data = request.get_json()

    # Find the crew member by ID
    user = db.session.get(User, user_id)
    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    # Update the crew member's details
    try:
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)

        db.session.commit()
        return jsonify(user.to_dict()), 200
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

    user = get_user_by_id(db.session, user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404  #pragma: no cover

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
    airline = get_airline_by_id(db.session, airline_id)

    if airline:
        airline_dict = airline.to_dict()
        airline_dict['flights'] = [f.to_dict() for f in get_flights_by_airline_id(db.session, airline_id)]
        return jsonify(airline_dict)
    else:
        return jsonify({'message': 'Airline not found'}), 404   #pragma: no cover

# Update
def update_user_profile_controller(token):
    data = request.get_json()
    user_id = get_user_id_from_token(token)['user_id']
    user = get_user_by_id(db.session, user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404  #pragma: no cover

    if 'first_name' in data: user.first_name = data['first_name']
    if 'last_name' in data: user.last_name = data['last_name']
    if 'email' in data: user.email = data['email']
    if 'phone' in data: user.phone = data['phone']
    if 'address' in data: user.address = data['address']
    if 'current' in data:
        if check_password_hash(user.password, data['current']):  #pragma: no cover
            user.password = generate_password_hash(data['new'])  #pragma: no cover
    user = update_user(db.session, user)
    return jsonify(user.to_dict())



def modify_booking_controller(booking_id):
    data = request.get_json()
    booking_detail = get_booking_detail_by_id(db.session, booking_id)
    if not booking_detail:
        return jsonify({'message': 'Booking not found'}), 404

    if 'flight_id' in data: booking_detail.flight_id = data['flight_id']
    if 'booking_date' in data: booking_detail.booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    if 'num_passengers' in data: booking_detail.num_passengers = data['num_passengers']
    if 'total_cost' in data: booking_detail.total_cost = data['total_cost']
    booking_detail = update_booking_detail(db.session, booking_detail)
    return jsonify(booking_detail.to_dict())


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
    try:
        delete_booking_by_id(db.session, booking_id, cascade=True)
        return jsonify({'message': 'Booking canceled successfully', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def delete_user_account_controller(user_id):
    try:
        delete_user_by_id(db.session, user_id)
        return jsonify({'message': 'User account deleted successfully'})
    except Exception as e: #pragma: no cover
        return jsonify({'message': str(e)}), 500 #pragma: no cover


def remove_outdated_data_controller():  #pragma: no cover
    current_time = datetime.now()

    outdated_flights = Flight.query.filter(Flight.arrival_time < current_time).all()
    for flight in outdated_flights:
        delete_flight_by_id(db.session, flight.flight_id, cascade=True)

    outdated_assignments = FlightCrewAssignment.query.join(Flight).filter(Flight.arrival_time < current_time).all()
    for assignment in outdated_assignments:
        delete_flightcrewassignment_by_id(db.session, assignment.id)

    return jsonify({'message': 'Outdated operational data removed successfully'})

def get_crew_assignment_controller(flight_id):
    assignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()
    if not assignments:
        return jsonify({'message': 'No crew assignments found'}), 404  #pragma: no cover

    response = []
    for assignment in assignments:
        crew = db.session.get(Crew, assignment.crew_id)
        role = db.session.get(CrewRole, assignment.role_id)
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
        airlines = get_airline_by_id(db.session, None)
        response = [{"id": airline.airline_id, "name": airline.airline_name} for airline in airlines]
        return response
    else:
        flights = get_flights_by_airline_id(db.session, airline_id)
        if not flights:
            return jsonify({'message': 'No Flight found for this airline'}), 401
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
    except Exception as e:  #pragma: no cover
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

def fetch_users_controller():  #pragma: no cover
    users =  adapter.get_user_by_id(db.session)
    response = [user.to_dict() for user in users]
    print(response)
    return response

# Add these functions to your controllers.py file

def get_all_users_controller():  #pragma: no cover
    """
    Admin endpoint to fetch all users
    """
    try:
        # Get all users
        users = User.query.all()
        user_list = []

        for user in users:
            user_dict = user.to_dict()
            # Don't send password hash in response
            if 'password' in user_dict:
                del user_dict['password']
            user_list.append(user_dict)

        return jsonify(user_list)
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {str(e)}'}), 500

def update_user_role_controller(user_id):  #pragma: no cover
    """
    Admin endpoint to update a user's role
    """
    data = request.get_json()

    if not data or 'role' not in data:
        return jsonify({'message': 'Role is required'}), 400

    # Validate the role
    valid_roles = ['customer', 'crew', 'admin']
    if data['role'] not in valid_roles:
        return jsonify({'message': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400

    try:
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Update the role
        user.role = data['role']
        db.session.commit()

        return jsonify({'success': True, 'message': f'User role updated to {data["role"]}'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating user role: {str(e)}'}), 500

# Add a function to get user-specific data for admin views
def get_user_data_for_admin_controller(user_id):  #pragma: no cover
    """
    Admin endpoint to fetch detailed data for a specific user
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Get user bookings
        bookings = Booking.query.filter_by(user_id=user_id).all()
        booking_data = []

        for booking in bookings:
            booking_details = BookingDetail.query.filter_by(booking_id=booking.booking_id).first()
            if booking_details:
                flight = Flight.query.get(booking_details.flight_id)
                airline = Airline.query.get(flight.airline_id) if flight else None

                booking_data.append({
                    'booking_id': booking.booking_id,
                    'booking_date': booking_details.booking_date.isoformat() if booking_details.booking_date else None,
                    'num_passengers': booking_details.num_passengers,
                    'total_cost': str(booking_details.total_cost),
                    'flight_number': flight.flight_number if flight else None,
                    'airline_name': airline.airline_name if airline else None,
                    'departure_airport': flight.departure_airport if flight else None,
                    'arrival_airport': flight.arrival_airport if flight else None
                })

        # Create user data object
        user_data = user.to_dict()
        # Don't send password hash
        if 'password' in user_data:
            del user_data['password']

        user_data['bookings'] = booking_data

        return jsonify(user_data)
    except Exception as e:
        return jsonify({'message': f'Error fetching user data: {str(e)}'}), 500