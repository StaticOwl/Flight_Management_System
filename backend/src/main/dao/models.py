from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import relationship

from main.__init__ import db

class User(db.Model):
    __tablename__ = 'Users'
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

class Airline(db.Model):
    __tablename__ = 'Airlines'
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    flights = relationship('Flight', back_populates='airline')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Flight(db.Model):
    __tablename__ = 'Flights'
    flight_id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey('Airlines.airline_id'), nullable=False)
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

class Crew(db.Model):
    __tablename__ = 'Crew'
    crew_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignments = relationship('FlightCrewAssignment', back_populates='crew')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class CrewRole(db.Model):
    __tablename__ = 'CrewRoles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    flight_crew_assignments = relationship('FlightCrewAssignment', back_populates='crew_role')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Booking(db.Model):
    __tablename__ = 'Bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    user = relationship('User', back_populates='bookings')
    booking_details = relationship('BookingDetail', back_populates='booking', uselist=False)
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class BookingDetail(db.Model):
    __tablename__ = 'BookingDetails'
    booking_details_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.booking_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('Flights.flight_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    num_passengers = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    booking = relationship('Booking', back_populates='booking_details')
    flight = relationship('Flight', back_populates='booking_details')
    passengers = relationship('Passenger', back_populates='booking_detail')
    payments = relationship('Payment', back_populates='booking_detail')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Passenger(db.Model):
    __tablename__ = 'Passengers'
    passenger_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('BookingDetails.booking_details_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    booking_detail = relationship('BookingDetail', back_populates='passengers')
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Payment(db.Model):
    __tablename__ = 'Payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_details_id = db.Column(db.Integer, db.ForeignKey('BookingDetails.booking_details_id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    booking_detail = relationship('BookingDetail', back_populates='payments')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class FlightCrewAssignment(db.Model):
    __tablename__ = 'FlightCrewAssignments'
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('Flights.flight_id'), nullable=False)
    crew_id = db.Column(db.Integer, db.ForeignKey('Crew.crew_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('CrewRoles.role_id'), nullable=False)
    flight = relationship('Flight', back_populates='flight_crew_assignments')
    crew = relationship('Crew', back_populates='flight_crew_assignments')
    crew_role = relationship('CrewRole', back_populates='flight_crew_assignments')
        
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}