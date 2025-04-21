from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import relationship

from main.__init__ import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100000), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    role = db.Column(db.String(20), default='customer')
    booking_ref = relationship('Booking', back_populates='user_ref')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Airline(db.Model):
    __tablename__ = 'airlines'
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    flight_ref = relationship('Flight', back_populates='airline_ref')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

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
    airline_ref = relationship('Airline', back_populates='flight_ref')
    booking_detail_ref = relationship('BookingDetail', back_populates='flight_ref')
    flight_crew_assignment_ref = relationship('FlightCrewAssignment', back_populates='flight_ref')

    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Crew(db.Model):
    __tablename__ = 'crews'
    crew_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignment_ref = relationship('FlightCrewAssignment', back_populates='crew_ref')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class CrewRole(db.Model):
    __tablename__ = 'crewroles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignment_ref = relationship('FlightCrewAssignment', back_populates='crew_role_ref')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_ref = relationship('User', back_populates='booking_ref')
    booking_detail_ref = relationship('BookingDetail', back_populates='booking_ref', uselist=False)
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class BookingDetail(db.Model):
    __tablename__ = 'bookingdetails'
    booking_details_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    num_passengers = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    booking_ref = relationship('Booking', back_populates='booking_detail_ref')
    flight_ref = relationship('Flight', back_populates='booking_detail_ref')
    passenger_ref = relationship('Passenger', back_populates='booking_detail_ref')
    payment_ref = relationship('Payment', back_populates='booking_detail_ref')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Passenger(db.Model):
    __tablename__ = 'passengers'
    passenger_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('bookingdetails.booking_details_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    booking_detail_ref = relationship('BookingDetail', back_populates='passenger_ref')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('bookingdetails.booking_details_id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    booking_detail_ref = relationship('BookingDetail', back_populates='payment_ref')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class FlightCrewAssignment(db.Model):
    __tablename__ = 'flightcrewassignments'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    crew_id = db.Column(db.Integer, db.ForeignKey('crews.crew_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('crewroles.role_id'), nullable=False)
    flight_ref = relationship('Flight', back_populates='flight_crew_assignment_ref')
    crew_ref = relationship('Crew', back_populates='flight_crew_assignment_ref')
    crew_role_ref = relationship('CrewRole', back_populates='flight_crew_assignment_ref')
        
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}