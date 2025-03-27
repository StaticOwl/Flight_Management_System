
-- Users
INSERT INTO users (first_name, last_name, email, password, phone, address) VALUES
('John', 'Doe', 'john.doe@email.com', 'password123', '1234567890', '123 Main St, City, Country'),
('Jane', 'Smith', 'jane.smith@email.com', 'pass456', '9876543210', '456 Oak Ave, Town, Country'),
('Michael', 'Johnson', 'michael.johnson@email.com', 'securepass', '5551234567', '789 Elm Rd, Village, Country'),
('Emily', 'Williams', 'emily.williams@email.com', 'pass123456', '1112223333', '321 Pine St, City, Country'),
('David', 'Brown', 'david.brown@email.com', 'password123!', '4445556666', '654 Maple Ln, Town, Country')
RETURNING user_id;

-- Airlines
INSERT INTO airlines (airline_name, contact_email, contact_phone) VALUES
('AirLine One', 'contact@airlineone.com', '1800123456'),
('SkyJet Airlines', 'info@skyjet.com', '1800987654'),
('FlyHigh Airways', 'support@flyhigh.com', '1800456789'),
('Global Travels', 'enquiry@globaltravels.com', '1800555666'),
('JetStream Airlines', 'customercare@jetstream.com', '1800777888')
RETURNING airline_id;


-- Flights
INSERT INTO flights (
  airline_id,
  flight_number,
  departure_airport,
  arrival_airport,
  departure_time,
  arrival_time,
  aircraft_type,
  num_seats,
  price_per_seat
) VALUES
((SELECT airline_id FROM airlines WHERE airline_name = 'AirLine One'), 'AL101', 'JFK', 'LAX', '2023-06-01 08:00:00', '2023-06-01 11:30:00', 'Boeing 737', 180, 10.21),
((SELECT airline_id FROM airlines WHERE airline_name = 'SkyJet Airlines'), 'SJ202', 'ORD', 'SFO', '2023-06-02 10:15:00', '2023-06-02 12:45:00', 'Airbus A320', 150, 23.23),
((SELECT airline_id FROM airlines WHERE airline_name = 'FlyHigh Airways'), 'FH303', 'LHR', 'DXB', '2023-06-03 14:30:00', '2023-06-03 22:00:00', 'Boeing 777', 300, 37.50),
((SELECT airline_id FROM airlines WHERE airline_name = 'Global Travels'), 'GT404', 'SYD', 'NRT', '2023-06-04 06:00:00', '2023-06-04 12:30:00', 'Airbus A350', 280, 15.75),
((SELECT airline_id FROM airlines WHERE airline_name = 'JetStream Airlines'), 'JS505', 'DEL', 'SIN', '2023-06-05 09:15:00', '2023-06-05 15:45:00', 'Boeing 787', 250, 65.00)
RETURNING flight_id;


-- Crew
INSERT INTO crews (first_name, last_name) VALUES
  ('Alice', 'Taylor'),
  ('Bob', 'Anderson'),
  ('Charlie', 'Wilson'),
  ('David', 'Thompson'),
  ('Eve', 'Martinez')
RETURNING crew_id, first_name, last_name;


-- CrewRoles
INSERT INTO crewroles (role_name) VALUES
  ('Pilot'),
  ('Co-Pilot'),
  ('Flight Attendant'),
  ('Purser')
RETURNING role_id, role_name;

-- Bookings
INSERT INTO bookings (user_id) VALUES
  ((SELECT user_id FROM users WHERE email = 'john.doe@email.com')),
  ((SELECT user_id FROM users WHERE email = 'jane.smith@email.com')),
  ((SELECT user_id FROM users WHERE email = 'michael.johnson@email.com')),
  ((SELECT user_id FROM users WHERE email = 'emily.williams@email.com')),
  ((SELECT user_id FROM users WHERE email = 'david.brown@email.com'))
RETURNING booking_id, user_id;



-- BookingDetails
INSERT INTO bookingdetails (booking_id, flight_id, booking_date, num_passengers, total_cost) VALUES
  (
    (SELECT booking_id FROM bookings ORDER BY booking_id OFFSET 0 LIMIT 1),
    (SELECT flight_id FROM flights WHERE flight_number = 'SJ202'),
    '2023-05-25', 2, 800.00
  ),
  (
    (SELECT booking_id FROM bookings ORDER BY booking_id OFFSET 1 LIMIT 1),
    (SELECT flight_id FROM flights WHERE flight_number = 'FH303'),
    '2023-05-26', 4, 1200.00
  ),
  (
    (SELECT booking_id FROM bookings ORDER BY booking_id OFFSET 2 LIMIT 1),
    (SELECT flight_id FROM flights WHERE flight_number = 'GT404'),
    '2023-05-27', 1, 1000.00
  ),
  (
    (SELECT booking_id FROM bookings ORDER BY booking_id OFFSET 3 LIMIT 1),
    (SELECT flight_id FROM flights WHERE flight_number = 'JS505'),
    '2023-05-28', 3, 1500.00
  ),
  (
    (SELECT booking_id FROM bookings ORDER BY booking_id OFFSET 4 LIMIT 1),
    (SELECT flight_id FROM flights WHERE flight_number = 'AL101'),
    '2023-05-29', 2, 900.00
  )
RETURNING booking_details_id, booking_id, flight_id;


-- Passengers
INSERT INTO passengers (booking_details_id, first_name, last_name, date_of_birth) VALUES
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 0 LIMIT 1),
    'John', 'Doe', '1990-01-01'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 0 LIMIT 1),
    'Jane', 'Doe', '1992-03-15'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 1 LIMIT 1),
    'Michael', 'Johnson', '1985-07-20'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 1 LIMIT 1),
    'Emily', 'Johnson', '1988-11-05'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 1 LIMIT 1),
    'David', 'Johnson', '2015-02-28'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 1 LIMIT 1),
    'Sarah', 'Johnson', '2018-09-12'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 2 LIMIT 1),
    'Robert', 'Williams', '1978-04-30'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 3 LIMIT 1),
    'Jessica', 'Brown', '1995-06-10'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 3 LIMIT 1),
    'Christopher', 'Brown', '1997-12-25'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 3 LIMIT 1),
    'Ashley', 'Brown', '2000-08-18'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 4 LIMIT 1),
    'Matthew', 'Davis', '1982-03-03'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 4 LIMIT 1),
    'Olivia', 'Davis', '1984-09-22'
  )
RETURNING passenger_id, booking_details_id;


-- Payments
INSERT INTO payments (booking_details_id, payment_date, amount, payment_method) VALUES
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 0 LIMIT 1),
    '2023-05-25', 800.00, 'Credit Card'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 1 LIMIT 1),
    '2023-05-26', 1200.00, 'Debit Card'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 2 LIMIT 1),
    '2023-05-27', 1000.00, 'PayPal'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 3 LIMIT 1),
    '2023-05-28', 1500.00, 'Credit Card'
  ),
  (
    (SELECT booking_details_id FROM bookingdetails ORDER BY booking_details_id OFFSET 4 LIMIT 1),
    '2023-05-29', 900.00, 'Bank Transfer'
  )
RETURNING payment_id, booking_details_id;


-- FlightCrewAssignments
INSERT INTO flightcrewassignments (flight_id, crew_id, role_id) VALUES
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 0 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 0 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 0 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 0 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 1 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 1 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 0 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 2 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 0 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 3 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),

  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 1 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 1 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 0 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 1 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 2 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 1 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 1 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 3 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 1 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 4 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),

  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 2 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 2 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 0 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 2 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 3 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 1 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 2 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 0 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 2 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 4 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 3 LIMIT 1)),

  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 3 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 3 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 0 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 3 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 4 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 1 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 3 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 0 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 3 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 1 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),

  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 4 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 4 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 0 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 4 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 0 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 1 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 4 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 1 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1)),
  ((SELECT flight_id FROM flights ORDER BY flight_id OFFSET 4 LIMIT 1), (SELECT crew_id FROM crews ORDER BY crew_id OFFSET 2 LIMIT 1), (SELECT role_id FROM crewroles ORDER BY role_id OFFSET 2 LIMIT 1))
RETURNING id, flight_id, crew_id, role_id;
