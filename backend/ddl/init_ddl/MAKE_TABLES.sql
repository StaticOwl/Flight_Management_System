 CREATE TABLE users (
     user_id SERIAL PRIMARY KEY,
     first_name VARCHAR(50) NOT NULL,
     last_name VARCHAR(50) NOT NULL,
     email VARCHAR(100) UNIQUE NOT NULL,
     password VARCHAR(100) NOT NULL,
     phone VARCHAR(20),
     role VARCHAR(20),
     address VARCHAR(200)
 );

 CREATE TABLE airlines (
     airline_id SERIAL PRIMARY KEY,
     airline_name VARCHAR(100) NOT NULL,
     contact_email VARCHAR(100),
     contact_phone VARCHAR(20)
 );

 CREATE TABLE flights (
     flight_id SERIAL PRIMARY KEY,
     airline_id INTEGER NOT NULL REFERENCES airlines(airline_id),
     flight_number VARCHAR(10) NOT NULL,
     departure_airport VARCHAR(100) NOT NULL,
     arrival_airport VARCHAR(100) NOT NULL,
     departure_time TIMESTAMP NOT NULL,
     arrival_time TIMESTAMP NOT NULL,
     aircraft_type VARCHAR(50) NOT NULL,
     num_seats INTEGER NOT NULL,
     price_per_seat DECIMAL(10,2) NULL
 );

 CREATE TABLE crews (
     crew_id SERIAL PRIMARY KEY,
     first_name VARCHAR(50) NOT NULL,
     last_name VARCHAR(50) NOT NULL
 );

 CREATE TABLE crewroles (
     role_id SERIAL PRIMARY KEY,
     role_name VARCHAR(50) NOT NULL
 );

 CREATE TABLE bookings (
     booking_id SERIAL PRIMARY KEY,
     user_id INTEGER NOT NULL REFERENCES users(user_id)
 );

 CREATE TABLE bookingdetails (
     booking_details_id SERIAL PRIMARY KEY,
     booking_id INTEGER NOT NULL REFERENCES bookings(booking_id),
     flight_id INTEGER NOT NULL REFERENCES flights(flight_id),
     booking_date DATE NOT NULL,
     num_passengers INTEGER NOT NULL,
     total_cost DECIMAL(10,2) NOT NULL
 );

 CREATE TABLE passengers (
     passenger_id SERIAL PRIMARY KEY,
     booking_details_id INTEGER NOT NULL REFERENCES bookingdetails(booking_details_id),
     first_name varchar(50) NOT NULL,
     last_name varchar(50) NOT NULL,
     date_of_birth DATE NOT NULL
);
 CREATE TABLE payments (
     payment_id SERIAL PRIMARY KEY,
     booking_details_id INTEGER NOT NULL REFERENCES bookingdetails(booking_details_id),
     payment_date DATE NOT NULL,
     amount DECIMAL(10,2) NOT NULL,
     payment_method VARCHAR(50) NOT NULL
 );

 CREATE TABLE flightcrewassignments (
     id SERIAL PRIMARY KEY,
     flight_id INTEGER NOT NULL REFERENCES flights(flight_id),
     crew_id INTEGER NOT NULL REFERENCES crews(crew_id),
     role_id INTEGER NOT NULL REFERENCES crewroles(role_id)
 );