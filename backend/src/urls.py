from flask import request

from src.app import app
from src.controllers import (
    list_all_controller,
    create_user_controller,
    create_booking_controller,
    create_flight_controller,
    create_crew_controller,
    search_flights_controller,
    get_user_profile_controller,
    get_booking_history_controller,
    get_airline_dashboard_controller,
    update_user_profile_controller,
    modify_booking_controller,
    update_flight_schedule_controller,
    update_crew_assignment_controller,
    cancel_booking_controller,
    delete_user_account_controller,
    remove_outdated_data_controller,
    get_crew_assignment_controller,
    login_controller,
    get_user_id_from_token,
    set_token_user_id,
    fetch_airlines,
    get_crews,
    add_crew_controller,
    update_crew_controller,
    fetch_flights_controller,
    fetch_roles_controller
)

# List all entities
@app.route("/api/<name>", methods=['GET'])
def list_entities(name):
    return list_all_controller(name)

@app.route("/login", methods=['POST'])
def login():
    return login_controller()

# User endpoints
@app.route("/createuser", methods=['POST'])
def create_user():
    return create_user_controller()

@app.route("/users", methods=['GET', 'PUT'])
def user_operations():
    print(request.headers)
    token = request.headers.get('Authorization').split(' ')[1]
    if request.method == 'GET':
        return get_user_profile_controller(token)
    elif request.method == 'PUT':
        print(request.get_json())
        return update_user_profile_controller(token)
    
@app.route("/token", methods=['GET'])
def getUserIdFromToken():
    token = request.headers.get('Authorization').split(' ')[1]
    return get_user_id_from_token(token)

@app.route("/gettoken/<int:user_id>", methods=['GET'])
def getToken(user_id):
    return set_token_user_id(user_id)

# Booking endpoints
@app.route("/createbooking", methods=['POST'])
def create_booking():
    return create_booking_controller()

@app.route("/bookings/<int:booking_id>", methods=['PUT', 'DELETE'])
def booking_operations(booking_id):
    if request.method == 'PUT':
        return modify_booking_controller(booking_id)
    elif request.method == 'DELETE':
        return cancel_booking_controller(booking_id)

@app.route("/users/bookings", methods=['GET'])
def user_bookings():
    token = request.headers.get('Authorization').split(' ')[1]
    return get_booking_history_controller(token)

# Flight endpoints
@app.route("/createflights", methods=['POST'])
def create_flight():
    return create_flight_controller()

@app.route("/flights/search", methods=['GET'])
def search_flights():
    return search_flights_controller()

@app.route("/flights/<int:flight_id>", methods=['PUT'])
def update_flight(flight_id):fetch_roles_controller
@app.route("/addcrew", methods=['POST'])
def create_crew():
    return create_crew_controller()

@app.route("/flights/<int:flight_id>/crew", methods=['GET'])
def get_crew(flight_id):
    return get_crew_assignment_controller(flight_id)

@app.route("/flights/<int:flight_id>/crew", methods=['PUT'])
def update_crew(flight_id):
    return update_crew_assignment_controller(flight_id)

# Airline endpoints
@app.route("/airlines/<int:airline_id>", methods=['GET'])
def airline_dashboard(airline_id):
    return get_airline_dashboard_controller(airline_id)

# Administrative deletion of outdated data
@app.route("/admin/cleanup", methods=['DELETE'])
def admin_cleanup():fetch_roles_controller
@app.route("/users/<int:user_id>/delete", methods=['DELETE'])
def delete_user(user_id):
    return delete_user_account_controller(user_id)

@app.route("/airlines", methods=['GET'])
def get_airlines():
    return fetch_airlines()

@app.route("/flights_by_airlines/<airline_id>")
def fetch_flights_by_airline_id(airline_id):
    return fetch_airlines(airline_id)
# Generic error for unsupported methods at any endpoint

@app.route("/getCrew", methods=['GET'])
def getCrew():
    return get_crews()

@app.route("/addCrew", methods=['POST'])
def addCrew():
    return add_crew_controller()

@app.route('/update-crew/<int:crew_id>', methods=['PUT'])
def updateCrew(crew_id):
    return update_crew_controller(crew_id)

@app.route("/flights", methods=['GET'])
def fetch_flights():
    return fetch_flights_controller()

@app.route("/roles", methods=['GET'])
def fetch_roles():
    return fetch_roles_controller()

@app.errorhandler(405)
def method_not_allowed(e):
    return "Method is Not Allowed", 405

