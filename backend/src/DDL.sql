-- CREATE TABLE Users (
--     user_id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     password VARCHAR(100) NOT NULL,
--     phone VARCHAR(20),
--     address VARCHAR(200)
-- );

-- CREATE TABLE Airlines (
--     airline_id SERIAL PRIMARY KEY,
--     airline_name VARCHAR(100) NOT NULL,
--     contact_email VARCHAR(100),
--     contact_phone VARCHAR(20)
-- );

-- CREATE TABLE Flights (
--     flight_id SERIAL PRIMARY KEY,
--     airline_id INTEGER NOT NULL REFERENCES Airlines(airline_id),
--     flight_number VARCHAR(10) NOT NULL,
--     departure_airport VARCHAR(100) NOT NULL,
--     arrival_airport VARCHAR(100) NOT NULL,
--     departure_time TIMESTAMP NOT NULL,
--     arrival_time TIMESTAMP NOT NULL,
--     aircraft_type VARCHAR(50) NOT NULL,
--     num_seats INTEGER NOT NULL
-- );

-- CREATE TABLE Crew (
--     crew_id SERIAL PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL
-- );

-- CREATE TABLE CrewRoles (
--     role_id SERIAL PRIMARY KEY,
--     role_name VARCHAR(50) NOT NULL
-- );

-- CREATE TABLE Bookings (
--     booking_id SERIAL PRIMARY KEY,
--     user_id INTEGER NOT NULL REFERENCES Users(user_id)
-- );

-- CREATE TABLE BookingDetails (
--     booking_details_id SERIAL PRIMARY KEY,
--     booking_id INTEGER NOT NULL REFERENCES Bookings(booking_id),
--     flight_id INTEGER NOT NULL REFERENCES Flights(flight_id),
--     booking_date DATE NOT NULL,
--     num_passengers INTEGER NOT NULL,
--     total_cost DECIMAL(10,2) NOT NULL
-- );

-- CREATE TABLE Passengers (
--     passengpassword
-- CREATE TABLE Payments (
--     payment_id SERIAL PRIMARY KEY,
--     booking_details_id INTEGER NOT NULL REFERENCES BookingDetails(booking_details_id),
--     payment_date DATE NOT NULL,
--     amount DECIMAL(10,2) NOT NULL,
--     payment_method VARCHAR(50) NOT NULL
-- );

-- CREATE TABLE FlightCrewAssignments (
--     id SERIAL PRIMARY KEY,
--     flight_id INTEGER NOT NULL REFERENCES Flights(flight_id),
--     crew_id INTEGER NOT NULL REFERENCES Crew(crew_id),
--     role_id INTEGER NOT NULL REFERENCES CrewRoles(role_id)
-- );

-- DROP TABLE flightcrewassignments;
-- DROP TABLE payments;
-- DROP TABLE passengers;
-- DROP TABLE bookingdetails;
-- DROP TABLE bookings;
-- DROP TABLE crewroles;
-- DROP TABLE crew;
-- DROP TABLE flights;
-- DROP TABLE airlines;
-- DROP TABLE users;

delete from users;
delete from flights;
delete from airlines;
delete from crew;

-- Users
INSERT INTO users (user_id, first_name, last_name, email, password, phone, address) VALUES
(1, 'John', 'Doe', 'john.doe@email.com', 'password123', '1234567890', '123 Main St, City, Country'),
(2, 'Jane', 'Smith', 'jane.smith@email.com', 'pass456', '9876543210', '456 Oak Ave, Town, Country'),
(3, 'Michael', 'Johnson', 'michael.johnson@email.com', 'securepass', '5551234567', '789 Elm Rd, Village, Country'),
(4, 'Emily', 'Williams', 'emily.williams@email.com', 'pass123456', '1112223333', '321 Pine St, City, Country'),
(5, 'David', 'Brown', 'david.brown@email.com', 'password123!', '4445556666', '654 Maple Ln, Town, Country');

-- Airlines
INSERT INTO airlines (airline_id, airline_name, contact_email, contact_phone) VALUES
(1,'AirLine One', 'contact@airlineone.com', '1800123456'),
(2,'SkyJet Airlines', 'info@skyjet.com', '1800987654'),
(3,'FlyHigh Airways', 'support@flyhigh.com', '1800456789'),
(4,'Global Travels', 'enquiry@globaltravels.com', '1800555666'),
(5,'JetStream Airlines', 'customercare@jetstream.com', '1800777888');

-- Flights
INSERT INTO flights (flight_id,airline_id, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, aircraft_type, num_seats) VALUES
(1, 1, 'AL101', 'JFK', 'LAX', '2023-06-01 08:00:00', '2023-06-01 11:30:00', 'Boeing 737', 180),
(2, 2, 'SJ202', 'ORD', 'SFO', '2023-06-02 10:15:00', '2023-06-02 12:45:00', 'Airbus A320', 150),
(3, 3, 'FH303', 'LHR', 'DXB', '2023-06-03 14:30:00', '2023-06-03 22:00:00', 'Boeing 777', 300),
(4, 4, 'GT404', 'SYD', 'NRT', '2023-06-04 06:00:00', '2023-06-04 12:30:00', 'Airbus A350', 280),
(5, 5, 'JS505', 'DEL', 'SIN', '2023-06-05 09:15:00', '2023-06-05 15:45:00', 'Boeing 787', 250);

-- Crew
INSERT INTO crew (crew_id, first_name, last_name) VALUES
(1, 'Alice', 'Taylor'),
(2, 'Bob', 'Anderson'),
(3, 'Charlie', 'Wilson'),
(4, 'David', 'Thompson'),
(5, 'Eve', 'Martinez');

-- CrewRoles
INSERT INTO crew_roles (role_id, role_name) VALUES
(1, 'Pilot'),
(2, 'Co-Pilot'),
(3, 'Flight Attendant'),
(4, 'Purser');

-- Bookings
INSERT INTO bookings (booking_id, user_id) VALUES
(2, 1),
(3, 2),
(4, 3),
(5, 4),
(1, 5);


-- BookingDetails
INSERT INTO booking_details (booking_details_id, booking_id, flight_id, booking_date, num_passengers, total_cost) VALUES
(1, 1, 2, '2023-05-25', 2, 800.00),
(2, 2, 3, '2023-05-26', 4, 1200.00),
(3, 3, 4, '2023-05-27', 1, 1000.00),
(4, 4, 5, '2023-05-28', 3, 1500.00),
(5, 5, 1, '2023-05-29', 2, 900.00);

-- Passengers
INSERT INTO passengers (passenger_id, booking_details_id, first_name, last_name, date_of_birth) VALUES
(1, 1, 'John', 'Doe', '1990-01-01'),
(2, 1, 'Jane', 'Doe', '1992-03-15'),
(3, 2, 'Michael', 'Johnson', '1985-07-20'),
(4, 2, 'Emily', 'Johnson', '1988-11-05'),
(5, 2, 'David', 'Johnson', '2015-02-28'),
(6, 2, 'Sarah', 'Johnson', '2018-09-12'),
(7, 3, 'Robert', 'Williams', '1978-04-30'),
(8, 4, 'Jessica', 'Brown', '1995-06-10'),
(9, 4, 'Christopher', 'Brown', '1997-12-25'),
(10, 4, 'Ashley', 'Brown', '2000-08-18'),
(11, 5, 'Matthew', 'Davis', '1982-03-03'),
(12, 5, 'Olivia', 'Davis', '1984-09-22');

-- Payments
INSERT INTO payments (payment_id, booking_details_id, payment_date, amount, payment_method) VALUES
(3, 1, '2023-05-25', 800.00, 'Credit Card'),
(1, 2, '2023-05-26', 1200.00, 'Debit Card'),
(5, 3, '2023-05-27', 1000.00, 'PayPal'),
(2, 4, '2023-05-28', 1500.00, 'Credit Card'),
(4, 5, '2023-05-29', 900.00, 'Bank Transfer');

-- FlightCrewAssignments
INSERT INTO flight_crew_assignments (flight_id, crew_id, role_id) VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(1, 4, 3),
(2, 2, 1),
(2, 3, 2),
(2, 4, 3),
(2, 5, 3),
(3, 3, 1),
(3, 4, 2),
(3, 1, 3),
(3, 5, 4),
(4, 4, 1),
(4, 5, 2),
(4, 1, 3),
(4, 2, 3),
(5, 5, 1),
(5, 1, 2),
(5, 2, 3),
(5, 3, 3);
select * from payments;