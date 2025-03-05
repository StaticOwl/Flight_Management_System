 CREATE TABLE Users (
     user_id SERIAL PRIMARY KEY,
     first_name VARCHAR(50) NOT NULL,
     last_name VARCHAR(50) NOT NULL,
     email VARCHAR(100) UNIQUE NOT NULL,
     password VARCHAR(100) NOT NULL,
     phone VARCHAR(20),
     address VARCHAR(200)
 );

 CREATE TABLE Airlines (
     airline_id SERIAL PRIMARY KEY,
     airline_name VARCHAR(100) NOT NULL,
     contact_email VARCHAR(100),
     contact_phone VARCHAR(20)
 );

 CREATE TABLE Flights (
     flight_id SERIAL PRIMARY KEY,
     airline_id INTEGER NOT NULL REFERENCES Airlines(airline_id),
     flight_number VARCHAR(10) NOT NULL,
     departure_airport VARCHAR(100) NOT NULL,
     arrival_airport VARCHAR(100) NOT NULL,
     departure_time TIMESTAMP NOT NULL,
     arrival_time TIMESTAMP NOT NULL,
     aircraft_type VARCHAR(50) NOT NULL,
     num_seats INTEGER NOT NULL
 );

 CREATE TABLE Crew (
     crew_id SERIAL PRIMARY KEY,
     first_name VARCHAR(50) NOT NULL,
     last_name VARCHAR(50) NOT NULL
 );

 CREATE TABLE CrewRoles (
     role_id SERIAL PRIMARY KEY,
     role_name VARCHAR(50) NOT NULL
 );

 CREATE TABLE Bookings (
     booking_id SERIAL PRIMARY KEY,
     user_id INTEGER NOT NULL REFERENCES Users(user_id)
 );

 CREATE TABLE BookingDetails (
     booking_details_id SERIAL PRIMARY KEY,
     booking_id INTEGER NOT NULL REFERENCES Bookings(booking_id),
     flight_id INTEGER NOT NULL REFERENCES Flights(flight_id),
     booking_date DATE NOT NULL,
     num_passengers INTEGER NOT NULL,
     total_cost DECIMAL(10,2) NOT NULL
 );

 CREATE TABLE Passengers (
     passenger_id SERIAL PRIMARY KEY,
     booking_details_id INTEGER NOT NULL REFERENCES BookingDetails(booking_details_id),
     first_name varchar(50) NOT NULL,
     last_name varchar(50) NOT NULL,
     date_of_birth DATE NOT NULL
);
 CREATE TABLE Payments (
     payment_id SERIAL PRIMARY KEY,
     booking_details_id INTEGER NOT NULL REFERENCES BookingDetails(booking_details_id),
     payment_date DATE NOT NULL,
     amount DECIMAL(10,2) NOT NULL,
     payment_method VARCHAR(50) NOT NULL
 );

 CREATE TABLE FlightCrewAssignments (
     id SERIAL PRIMARY KEY,
     flight_id INTEGER NOT NULL REFERENCES Flights(flight_id),
     crew_id INTEGER NOT NULL REFERENCES Crew(crew_id),
     role_id INTEGER NOT NULL REFERENCES CrewRoles(role_id)
 );


delete from users;
delete from flights;
delete from airlines;
delete from crew;
