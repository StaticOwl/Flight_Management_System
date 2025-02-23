from models import User, Airline, BookingDetail, Booking, Crew, CrewRole, FlightCrewAssignment, Flight, Passenger, Payment

def delete_user(db_session, user_id):
    try:
        User.query.filter_by(user_id=user_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_airline(db_session, airline_id, cascade = False):
    #ref'd in Flights
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flights = Flight.query.filter_by(airline_id=airline_id).all()
            # For each flight, delete that flight
            for f in flights:
                delete_flight(db_session, f.flight_id, cascade)
        Airline.query.filter_by(airline_id=airline_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_bookingdetail(db_session, bookingdetail_id, cascade = False):
    #ref'd in Passengers, Payments
    try:
        if cascade:
            print("Cascading")
            # Get all Passengers ref'ing booking detail
            passengers = Passenger.query.filter_by(booking_details_id=bookingdetail_id).all()
            # For each flight, delete that flight
            for ps in passengers:
                delete_passenger(db_session, ps.passenger_id)

            pays = Payment.query.filter_by(booking_detail_id=bookingdetail_id).all()

            for py in pays:
                delete_paymnet(db_session, py.payment_id, cascade)
        BookingDetail.query.filter_by(booking_detail_id=bookingdetail_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_booking(db_session, booking_id, cascade = False):

    #ref'd in BookingDetails
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            bookingdetails = BookingDetail.query.filter_by(booking_id=booking_id).all()
            # For each flight, delete that flight
            for b in bookingdetails:
                delete_bookingdetail(db_session, b.booking_detail_id, cascade)
        Booking.query.filter_by(booking_id=booking_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_crew(db_session, crew_id, cascade = False):

    #ref'd in FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flightcrewassignments = FlightCrewAssignment.query.filter_by(crew_id=crew_id).all()
            # For each flight, delete that flight
            for f in flightcrewassignments:
                delete_flightcrewassignment(db_session, f.id)
        Crew.query.filter_by(crew_id=crew_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_crewrole(db_session, crewrole_id, cascade = False):

    #ref'd in FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all flights ref'ing airline
            flightcrewassignments = FlightCrewAssignment.query.filter_by(role_id=crewrole_id).all()
            # For each flight, delete that flight
            for f in flightcrewassignments:
                delete_flightcrewassignment(db_session, f.id)
        CrewRole.query.filter_by(role_id=crewrole_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_flightcrewassignment(db_session, flightcrewassignment_id):
    try:
        FlightCrewAssignment.query.filter_by(id=flightcrewassignment_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_flight(db_session, flight_id, cascade = False):
    #ref'd in BookingDetails, FlightCrewAssignments
    try:
        if cascade:
            print("Cascading")
            # Get all Passengers ref'ing booking detail
            bookingdetails = BookingDetail.query.filter_by(flight_id=flight_id).all()
            # For each flight, delete that flight
            for b in bookingdetails:
                delete_bookingdetail(db_session, b.booking_detail_id, cascade)

            flightcrewassignments = FlightCrewAssignment.query.filter_by(flight_id=flight_id).all()

            for f in flightcrewassignments:
                delete_flightcrewassignment(db_session, f.id)
        Flight.query.filter_by(flight_id=flight_id).delete()
        db_session.commit()
    except Exception as e:
        print(e)
        raise

def delete_passenger(db_session, passenger_id):
    try:
        Passenger.query.filter_by(passenger_id=passenger_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise

def delete_paymnet(db_session, payment_id, cascade = False):
    try:
        Payment.query.filter_by(payment_id=payment_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        raise