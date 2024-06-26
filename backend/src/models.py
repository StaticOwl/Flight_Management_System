from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import relationship

from . import db # from __init__.py

# ----------------------------------------------- #

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100000), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    bookings = relationship('Booking', back_populates='user')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<User {self.email}>"

class Airline(db.Model):
    __tablename__ = 'airlines'
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    flights = relationship('Flight', back_populates='airline')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Airline {self.airline_name}>"

class Flight(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.airline_id'), nullable=False)
    flight_number = db.Column(db.String(10), nullable=False)
    departure_airport = db.Column(db.String(100), nullable=False)
    arrival_airport = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    aircraft_type = db.Column(db.String(50), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    price_per_seat = db.Column(db.Float, nullable=True)
    airline = relationship('Airline', back_populates='flights')
    booking_details = relationship('BookingDetail', back_populates='flight')
    flight_crew_assignments = relationship('FlightCrewAssignment', back_populates='flight')

    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Flight {self.flight_number} from {self.departure_airport} to {self.arrival_airport}>"


class Crew(db.Model):
    __tablename__ = 'crew'
    crew_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignments = relationship('FlightCrewAssignment', back_populates='crew')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Crew {self.first_name} {self.last_name}>"

class CrewRole(db.Model):
    __tablename__ = 'crew_roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignments = relationship('FlightCrewAssignment', back_populates='crew_role')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<CrewRole {self.role_name}>"

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = relationship('User', back_populates='bookings')
    booking_details = relationship('BookingDetail', back_populates='booking', uselist=False)
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Booking {self.booking_id} by User {self.user_id}>"

class BookingDetail(db.Model):
    __tablename__ = 'booking_details'
    booking_details_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    num_passengers = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    booking = relationship('Booking', back_populates='booking_details')
    flight = relationship('Flight', back_populates='booking_details')
    passengers = relationship('Passenger', back_populates='booking_detail')
    payments = relationship('Payment', back_populates='booking_detail')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<BookingDetail {self.booking_details_id} for Flight {self.flight_id}>"


class Passenger(db.Model):
    __tablename__ = 'passengers'
    passenger_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('booking_details.booking_details_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    booking_detail = relationship('BookingDetail', back_populates='passengers')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Passenger {self.first_name} {self.last_name} ID {self.passenger_id}>"


class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('booking_details.booking_details_id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    booking_detail = relationship('BookingDetail', back_populates='payments')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<Payment {self.payment_id} for BookingDetail {self.booking_details_id}>"


class FlightCrewAssignment(db.Model):
    __tablename__ = 'flight_crew_assignments'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    crew_id = db.Column(db.Integer, db.ForeignKey('crew.crew_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('crew_roles.role_id'), nullable=False)
    flight = relationship('Flight', back_populates='flight_crew_assignments')
    crew = relationship('Crew', back_populates='flight_crew_assignments')
    crew_role = relationship('CrewRole', back_populates='flight_crew_assignments')
        
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"<FlightCrewAssignment for Flight {self.flight_id} Crew {self.crew_id} Role {self.role_id}>"