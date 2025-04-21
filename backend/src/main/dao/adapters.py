from .models import User, Airline, BookingDetail, Booking, Crew, CrewRole, FlightCrewAssignment, Flight, Passenger, Payment

def delete_user_by_id(db_session, user_id):
    try:
        User.query.filter_by(user_id=user_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_airline_by_id(db_session, airline_id, cascade = False):
    #ref'd in Flights
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flights = Flight.query.filter_by(airline_id=airline_id).all()
            # For each flight, delete that flight
            for f in flights:
                delete_flight_by_id(db_session, f.flight_id, cascade)
        Airline.query.filter_by(airline_id=airline_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_booking_detail_by_id(db_session, booking_detail_id, cascade = False):
    #ref'd in Passengers, Payments
    try:
        if cascade:
            print("Cascading")
            # Get all Passengers ref'ing booking detail
            passengers = Passenger.query.filter_by(booking_details_id=booking_detail_id).all()
            # For each flight, delete that flight
            for ps in passengers:
                delete_passenger_by_id(db_session, ps.passenger_id)

            pays = Payment.query.filter_by(booking_details_id=booking_detail_id).all()

            for py in pays:
                delete_paymnet_by_id(db_session, py.payment_id, cascade)
        BookingDetail.query.filter_by(booking_details_id=booking_detail_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_booking_by_id(db_session, booking_id, cascade = False):

    #ref'd in BookingDetails
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            bookingdetails = BookingDetail.query.filter_by(booking_id=booking_id).all()
            # For each flight, delete that flight
            for b in bookingdetails:
                delete_booking_detail_by_id(db_session, b.booking_details_id, cascade)
        Booking.query.filter_by(booking_id=booking_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_crew_by_id(db_session, crew_id, cascade = False):

    #ref'd in FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flightcrewassignments = FlightCrewAssignment.query.filter_by(crew_id=crew_id).all()
            # For each flight, delete that flight
            for f in flightcrewassignments:
                delete_flightcrewassignment_by_id(db_session, f.id)
        Crew.query.filter_by(crew_id=crew_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_crewrole_by_id(db_session, crewrole_id, cascade = False):

    #ref'd in FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flightcrewassignments = FlightCrewAssignment.query.filter_by(role_id=crewrole_id).all()
            # For each flight, delete that flight
            for f in flightcrewassignments:
                delete_flightcrewassignment_by_id(db_session, f.id)
        CrewRole.query.filter_by(role_id=crewrole_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_flightcrewassignment_by_id(db_session, flightcrewassignment_id):
    try:
        FlightCrewAssignment.query.filter_by(id=flightcrewassignment_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_flight_by_id(db_session, flight_id, cascade = False):
    #ref'd in BookingDetails, FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all Passengers ref'ing booking detail
            bookingdetails = BookingDetail.query.filter_by(flight_id=flight_id).all()
            # For each flight, delete that flight
            for b in bookingdetails:
                delete_booking_detail_by_id(db_session, b.booking_details_id, cascade)

            flightcrewassignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()

            for f in flightcrewassignments:
                delete_flightcrewassignment_by_id(db_session, f.id)
        Flight.query.filter_by(flight_id=flight_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_passenger_by_id(db_session, passenger_id):
    try:
        Passenger.query.filter_by(passenger_id=passenger_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_paymnet_by_id(db_session, payment_id, cascade = False):
    try:
        Payment.query.filter_by(payment_id=payment_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def create_user(db_session, first_name, last_name, email, hashed_password, phone, address, booking_ref):
    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone=phone,
            address=address,
            booking_ref=booking_ref
        )
        db_session.add(user)
        db_session.commit()
        return user
    except Exception as e:
        print(e)
        raise

def create_airline(db_session, airline_name, contact_email, contact_phone, flight_ref):
    try:
        airline = Airline(
            airline_name = airline_name,
            contact_email = contact_email,
            contact_phone = contact_phone,
            flight_ref = flight_ref
        )
        db_session.add(airline)
        db_session.commit()
        return airline
    except Exception as e:
        print(e)
        raise

def create_flight(db_session, airline_id, flight_number, departure_airport, arrival_airport,
                  departure_time, arrival_time, aircraft_type, num_seats, price_per_seat):
    try:
        flight = Flight(
            airline_id=airline_id,
            flight_number=flight_number,
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            departure_time=departure_time,
            arrival_time=arrival_time,
            aircraft_type=aircraft_type,
            num_seats=num_seats,
            price_per_seat=price_per_seat
        )
        db_session.add(flight)
        db_session.commit()
        return flight
    except Exception as e:
        print(e)
        raise

def create_crew(db_session, first_name, last_name, flight_crew_assignment_ref):
    try:
        crew = Crew(
            first_name=first_name,
            last_name=last_name,
            flight_crew_assignment_ref=flight_crew_assignment_ref
        )
        db_session.add(crew)
        db_session.commit()
        return crew
    except Exception as e:
        print(e)
        raise

def create_crew_role(db_session, role_name, flight_crew_assignment_ref):
    try:
        crew_role = CrewRole(
            role_name=role_name,
            flight_crew_assignment_ref=flight_crew_assignment_ref
        )
        db_session.add(crew_role)
        db_session.commit()
        return crew_role
    except Exception as e:
        print(e)
        raise

def create_booking(db_session, user_id, booking_date, num_passengers, total_cost):
    try:
        booking = Booking(
            user_id=user_id,
            booking_date=booking_date,
            num_passengers=num_passengers,
            total_cost=total_cost
        )
        db_session.add(booking)
        db_session.commit()
        return booking
    except Exception as e:
        print(e)
        raise

def create_booking_detail(db_session, booking_id, flight_id, booking_date, num_passengers, total_cost):
    try:
        booking_detail = BookingDetail(
            booking_id=booking_id,
            flight_id=flight_id,
            booking_date=booking_date,
            num_passengers=num_passengers,
            total_cost=total_cost
        )
        db_session.add(booking_detail)
        db_session.commit()
        return booking_detail
    except Exception as e:
        print(e)
        raise

def create_passenger(db_session, booking_details_id, first_name, last_name, date_of_birth):
    try:
        passenger = Passenger(
            booking_details_id=booking_details_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )
        db_session.add(passenger)
        db_session.commit()
        return passenger
    except Exception as e:
        print(e)
        raise

def create_payment(db_session, booking_details_id, payment_date, amount, payment_method):
    try:
        payment = Payment(
            booking_details_id=booking_details_id,
            payment_date=payment_date,
            amount=amount,
            payment_method=payment_method
        )
        db_session.add(payment)
        db_session.commit()
        return payment
    except Exception as e:
        print(e)
        raise

def create_flight_crew_assignment(db_session, flight_id, crew_id, role_id):
    try:
        flight_crew_assignment = FlightCrewAssignment(
            flight_id=flight_id,
            crew_id=crew_id,
            role_id=role_id
        )
        db_session.add(flight_crew_assignment)
        db_session.commit()
        return flight_crew_assignment
    except Exception as e:
        print(e)
        raise

def update_user(db_session, user):
    try:
        db_session.merge(user)
        db_session.commit()
        return user
    except Exception as e:
        print(e)
        raise

def update_airline(db_session, airline):
    try:
        db_session.merge(airline)
        db_session.commit()
        return airline
    except Exception as e:
        print(e)
        raise

def update_flight(db_session, flight):
    try:
        db_session.merge(flight)
        db_session.commit()
        return flight
    except Exception as e:
        print(e)
        raise

def update_crew(db_session, crew):
    try:
        db_session.merge(crew)
        db_session.commit()
        return crew
    except Exception as e:
        print(e)
        raise

def update_crewrole(db_session, crewrole):
    try:
        db_session.merge(crewrole)
        db_session.commit()
        return crewrole
    except Exception as e:
        print(e)
        raise

def update_booking(db_session, booking):
    try:
        db_session.merge(booking)
        db_session.commit()
        return booking
    except Exception as e:
        print(e)
        raise

def update_booking_detail(db_session, booking_detail):
    try:
        db_session.merge(booking_detail)
        db_session.commit()
        return booking_detail
    except Exception as e:
        print(e)
        raise

def update_passenger(db_session, passenger):
    try:
        db_session.merge(passenger)
        db_session.commit()
        return passenger
    except Exception as e:
        print(e)
        raise

def update_payment(db_session, payment):
    try:
        db_session.merge(payment)
        db_session.commit()
        return payment
    except Exception as e:
        print(e)
        raise

def update_flightcrewassignment(db_session, flightcrewassignment):
    try:
        db_session.merge(flightcrewassignment)
        db_session.commit()
        return flightcrewassignment
    except Exception as e:
        print(e)
        raise
