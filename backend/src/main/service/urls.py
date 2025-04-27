from flask import Blueprint
from flask import request, jsonify

from service.controllers import (
    list_all_controller,
    create_user_controller,
    create_booking_controller,
    create_flight_controller,
    search_flights_controller,
    get_user_profile_controller,
    get_booking_history_controller,
    get_airline_dashboard_controller,
    update_user_profile_controller,
    modify_booking_controller,
    update_crew_assignment_controller,
    cancel_booking_controller,
    delete_user_account_controller,
    get_crew_assignment_controller,
    login_controller,
    get_user_id_from_token,
    set_token_user_id,
    fetch_airlines,
    get_crews,
    add_crew_controller,
    update_crew_controller,
    fetch_flights_controller,
    fetch_roles_controller,
    fetch_users_controller,
    update_user_controller
)
from service.middleware import role_required

urls_bp = Blueprint("urls", __name__)  # Create a Blueprint


# List all entities
@urls_bp.route("/api/<name>", methods=['GET'])
def list_entities(name):
    return list_all_controller(name)

@urls_bp.route("/login", methods=['POST'])
def login():
    return login_controller()

# User endpoints
@urls_bp.route("/createuser", methods=['POST', 'OPTIONS'])
def create_user():
    print("Create User")
    if request.method == 'OPTIONS':
        print("What's Options precious?")
        return jsonify({"message": "CORS preflight successful"}), 200
    return create_user_controller()

@urls_bp.route("/users/<int:user_id>/delete", methods=['DELETE'])
def delete_user(user_id):
    return delete_user_account_controller(user_id)

@urls_bp.route("/users", methods=['GET', 'PUT'])
def user_operations():
    print(request.headers)
    token = request.headers.get('Authorization').split(' ')[1]
    if request.method == 'GET':
        return get_user_profile_controller(token)
    elif request.method == 'PUT':
        print(request.get_json())
        return update_user_profile_controller(token)
    return None


@urls_bp.route("/fetchusers", methods=['GET'])
def get_users():
    return fetch_users_controller()

@urls_bp.route('/update-user/<int:user_id>', methods=['PUT'])
def updateUser(user_id):
    return update_user_controller(user_id)
    
@urls_bp.route("/token", methods=['GET'])
def getUserIdFromToken():
    token = request.headers.get('Authorization').split(' ')[1]
    return get_user_id_from_token(token)

@urls_bp.route("/gettoken/<int:user_id>", methods=['GET'])
def getToken(user_id):
    return set_token_user_id(user_id)

# Booking endpoints
@urls_bp.route("/createbooking", methods=['POST'])
def create_booking():
    return create_booking_controller()

@urls_bp.route("/bookings/<int:booking_id>", methods=['PUT', 'DELETE'])
def booking_operations(booking_id):
    if request.method == 'PUT':
        return modify_booking_controller(booking_id)
    elif request.method == 'DELETE':
        return cancel_booking_controller(booking_id)
    return None


@urls_bp.route("/users/bookings", methods=['GET'])
def user_bookings():
    token = request.headers.get('Authorization').split(' ')[1]
    return get_booking_history_controller(token)

# Flight endpoints
@urls_bp.route("/createflights", methods=['POST'])
def create_flight():
    return create_flight_controller()

@urls_bp.route("/flights/search", methods=['GET'])
def search_flights():
    return search_flights_controller()

@urls_bp.route("/flights/<int:flight_id>/crew", methods=['GET'])
def get_crew_by_flight(flight_id):
    return get_crew_assignment_controller(flight_id)

@urls_bp.route("/flights/<int:flight_id>/crew", methods=['PUT'])
def update_crew_by_flight(flight_id):
    return update_crew_assignment_controller(flight_id)

# Airline endpoints
@urls_bp.route("/airlines/<int:airline_id>", methods=['GET'])
def airline_dashboard(airline_id):
    return get_airline_dashboard_controller(airline_id)

@urls_bp.route("/airlines", methods=['GET'])
def get_airlines():
    return fetch_airlines()

@urls_bp.route("/flights_by_airlines/<airline_id>")
def fetch_flights_by_airline_id(airline_id):
    return fetch_airlines(airline_id)

@urls_bp.route("/getCrew", methods=['GET'])
def getCrew():
    return get_crews()

@urls_bp.route("/addCrew", methods=['POST'])
def addCrew():
    return add_crew_controller()

@urls_bp.route('/update-crew/<int:crew_id>', methods=['PUT'])
def updateCrew(crew_id):
    return update_crew_controller(crew_id)

@urls_bp.route("/flights", methods=['GET'])
def fetch_flights():
    return fetch_flights_controller()

@urls_bp.route("/roles", methods=['GET'])
def fetch_roles():
    return fetch_roles_controller()

# Admin routes
@urls_bp.route("/admin/users", methods=['GET'])
@role_required(['admin'])
def admin_get_users():
    return get_all_users_controller()

@urls_bp.route("/admin/users/<int:user_id>/role", methods=['PUT'])
@role_required(['admin'])
def admin_update_user_role(user_id):
    return update_user_role_controller(user_id)

@urls_bp.route("/admin/users/<int:user_id>", methods=['GET'])
@role_required(['admin'])
def admin_get_user_data(user_id):
    return get_user_data_for_admin_controller(user_id)

# Crew routes (accessible by crew and admin)
@urls_bp.route("/crew/flights", methods=['POST'])
@role_required(['crew', 'admin'])
def crew_add_flight():
    return create_flight_controller()

@urls_bp.route("/crew/flights/<int:flight_id>", methods=['PUT'])
@role_required(['crew', 'admin'])
def crew_update_flight(flight_id):
    # You'll need to implement this controller function
    return update_flight_controller(flight_id)

@urls_bp.route("/crew/assignments", methods=['GET'])
@role_required(['crew', 'admin'])
def crew_get_assignments():
    # Get all crew assignments for the crew member
    token = request.headers.get('Authorization').split(' ')[1]
    user_id = get_user_id_from_token(token)['user_id']
    return get_crew_assignments_controller(user_id)