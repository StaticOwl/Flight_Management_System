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
    login_controller
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

@app.route("/users/<int:user_id>", methods=['GET', 'PUT'])
def user_operations(user_id):
    if request.method == 'GET':
        return get_user_profile_controller(user_id)
    elif request.method == 'PUT':
        return update_user_profile_controller(user_id)

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

@app.route("/users/<int:user_id>/bookings", methods=['GET'])
def user_bookings(user_id):
    return get_booking_history_controller(user_id)

# Flight endpoints
@app.route("/flights", methods=['POST'])
def create_flight():
    return create_flight_controller()

@app.route("/flights/search", methods=['GET'])
def search_flights():
    return search_flights_controller()

@app.route("/flights/<int:flight_id>", methods=['PUT'])
def update_flight(flight_id):
    return update_flight_schedule_controller(flight_id)

# Crew endpoints
@app.route("/crew", methods=['POST'])
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
def admin_cleanup():
    return remove_outdated_data_controller()

# Account deletion
@app.route("/users/<int:user_id>/delete", methods=['DELETE'])
def delete_user(user_id):
    return delete_user_account_controller(user_id)

# Generic error for unsupported methods at any endpoint
@app.errorhandler(405)
def method_not_allowed(e):
    return "Method is Not Allowed", 405

