import React, { useEffect, useState } from 'react';
import ApiService from '../api/ApiService';
import { useNavigate } from 'react-router-dom';
import '../App.css';  // Make sure this is correctly linked

function Users() {
    const [user, setUser] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
        password: ''
    });
    const [editingUser, setEditingUser] = useState(false);
    const [showPasswordEdit, setShowPasswordEdit] = useState(false)
    const [passwords, setPasswords] = useState({ current: '', new: '', confirm: '' });
    const [bookings, setBookings] = useState([]);
    const [expanded, setExpanded] = useState(null);
    const [message, setMessage] = useState('');
    const [airlines, setAirlines] = useState([]);
    const [selectedAirline, setSelectedAirline] = useState('');
    const [flights, setFlights] = useState([]);
    const [selectedFlight, setSelectedFlight] = useState('');
    const [newBooking, setNewBooking] = useState({
        booking_date: '',
        num_passengers: 1
    });
    const [totalCost, setTotalCost] = useState(-10.0)
    const [updateData, setUpdateData] = useState(true)
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                await fetchUserDetails();
                await fetchUserBookings();
                await fetchAirlines();
            } catch (error) {
                setMessage('Error fetching data: ' + error.message);
                navigate('/login');
            }
        };

        if (updateData){
            fetchUserData();
            setUpdateData(false);
        }
    }, [updateData, navigate]);

    useEffect(() => {
        if (selectedAirline) {
            fetchFlights(selectedAirline);
        }
        else {
            setFlights([]);
            setSelectedAirline('');
        }
    }, [selectedAirline]);

    useEffect(() => {
        if (selectedFlight && newBooking.num_passengers > 0 && newBooking.booking_date) {
            const flight = flights.find(f => f.flight_number === selectedFlight);
            if (flight && flight.price_per_seat) {
                const dateCostAdjustment = calculateDateCostAdjustment(newBooking.booking_date);
                setTotalCost(flight.price_per_seat * newBooking.num_passengers + dateCostAdjustment);
            }
        }
    }, [selectedFlight, newBooking.num_passengers, newBooking.booking_date, flights]);

    const fetchFlights = async (airlineId) => {
        try {
            const flightsResponse = await ApiService.getFlightsByAirline(airlineId);
            setFlights(flightsResponse);
            setSelectedFlight(flightsResponse[0]?.flight_number);  // Automatically select the first flight
        } catch (error) {
            setMessage('Error fetching flights: ' + error.message);
        }
    };

    const calculateDateCostAdjustment = (date) => {
        if (!date) return 0;
        const digits = date.split('-').join(''); // Remove '-' and concatenate
        const sum = digits.split('').reduce((acc, digit) => acc + parseInt(digit, 10), 0);
        return sum / 1.5;
    };
    

    const fetchAirlines = async () => {
        try {
            const response = await ApiService.getAirlines();
            setAirlines(response);
            setSelectedAirline('');
        } catch (error) {
            setMessage('Error fetching airlines: ' + error.message);
        }
    };

    const fetchUserDetails = async () => {
        try {
            const response = await ApiService.getUser();
            setUser(response);
            setMessage('User data fetched successfully');
        } catch (error) {
            setMessage('Error fetching user data: ' + error.message);
        }
    };

    const fetchUserBookings = async () => {
        try {
            const response = await ApiService.getUserBookings();
            if (response === null){
                setMessage("No Booking Found.")
            }
            else{
                const length = response.length;
                setBookings(response);
                setMessage(`${length} ${length === 1 ? "booking" : "bookings"} fetched successfully`);
            }
        } catch (error) {
            setMessage('Error fetching bookings: ' + error.message);
        }
    };

    const toggleDetails = index => {
        setExpanded(expanded === index ? null : index);
    };

    const handleCreateBooking = async (event) => {
        event.preventDefault();
        try {
            if (!selectedAirline || !selectedFlight || !newBooking.booking_date || newBooking.num_passengers <= 0) {
                setMessage('Please fill in all fields to create a booking.');
                return;
            }

            const selectedFlightId = flights.find(f => f.flight_number === selectedFlight).id;

            console.log(selectedFlightId)
    
            // Prepare the data to send to the backend
            const bookingData = {
                airline_id: selectedAirline,
                flight_id: selectedFlightId,
                booking_date: newBooking.booking_date,
                num_passengers: newBooking.num_passengers,
                total_cost: totalCost,
                token: localStorage.getItem('token') // Use the calculated total cost
            };
    
            // API call to create the booking
            const response = await ApiService.createBooking(bookingData);
            console.log(response)
            if (response && response.booking_id) {  // Assuming your API returns the created booking with an 'id'
                setMessage(`Booking created successfully. Keep the Booking ID ${response.booking_id} for reference.`);
                // Reset the booking form state
                setNewBooking({ booking_date: '', num_passengers: 1 });
                setUpdateData(true)
                setTotalCost(0);
            } else {
                setMessage('Failed to create booking.');
            }
        } catch (error) {
            setMessage(`Error creating booking: ${error.message}`);
        }
    };

    const handleDeleteBooking = async (bookingId) => {
        try {
            console.log(bookingId)
            const response = await ApiService.deleteBooking(bookingId);
            console.log(response)
            console.log(response.success)
            if (response.success) {
                setBookings(bookings.filter(booking => booking.id !== bookingId)); // Remove the booking from the list
                setMessage('Booking deleted successfully');
            } else {
                setMessage('Error deleting booking: ' + response.message);
            }
        } catch (error) {
            setMessage('Error deleting booking: ' + error.message);
        }
    };

    const handleUserEditToggle = () => {
        setEditingUser(!editingUser);
    };

    const callPasswordToggle = () => {
        setShowPasswordEdit(!showPasswordEdit)
        console.log(passwords)
    }

    const handleUserUpdate = async () => {
        if (!editingUser) {
            return;
        }
        try {
            console.log(user)
            const response = await ApiService.updateUser(user);
            setEditingUser(false); // Exit editing mode after update
            if (response.success){
                setMessage('User updated successfully');
            }
        } catch (error) {
            setMessage(`Error updating user: ${error.message}`);
        }
    };

    const handlePasswordUpdate = async () => {
        if (passwords.new !== passwords.confirm) {
            setMessage('Passwords do not match');
            return;
        }
        try {
            const response = await ApiService.updateUser(passwords);
            setPasswords({ current: '', new: '', confirm: '' });
            if (response.success){
                setMessage('Password updated successfully');
            }
        } catch (error) {
            setMessage(`Error updating password: ${error.message}`);
        }
    };

    const renderUserDetails = () => (
        editingUser ? (
            <>
                <input value={user.first_name} onChange={e => setUser({ ...user, first_name: e.target.value })} />
                <input value={user.last_name} onChange={e => setUser({ ...user, last_name: e.target.value })} />
                <input value={user.email} onChange={e => setUser({ ...user, email: e.target.value })} />
                <input value={user.phone} onChange={e => setUser({ ...user, phone: e.target.value })} />
                <input value={user.address} onChange={e => setUser({ ...user, address: e.target.value })} />
                <button className="flight-form-button" onClick={handleUserUpdate}>Save Changes</button>
            </>
        ) : (
            <>
                <p>First Name: {user.first_name}</p>
                <p>Last Name: {user.last_name}</p>
                <p>Email: {user.email}</p>
                <p>Phone: {user.phone}</p>
                <p>Address: {user.address}</p>
                <button className="flight-form-button" onClick={handleUserEditToggle}>Edit</button>
            </>
        )
    );

    const renderPasswordForm = () => (
        showPasswordEdit && 
        <form onSubmit={handlePasswordUpdate}>
            <input type="password" value={passwords.current} onChange={e => setPasswords({ ...passwords, current: e.target.value })} placeholder="Current Password" />
            <input type="password" value={passwords.new} onChange={e => setPasswords({ ...passwords, new: e.target.value })} placeholder="New Password" />
            <input type="password" value={passwords.confirm} onChange={e => setPasswords({ ...passwords, confirm: e.target.value })} placeholder="Confirm New Password" />
            <button className="flight-form-button" type="submit">Set Password</button>
        </form>
    );

    return (
        <div className="user-dashboard">
            <h2>Dashboard</h2>
            <div>{renderUserDetails()}</div>
            {/* <button onClick={callPasswordToggle}>Update Password</button> */}
            {renderPasswordForm()}
            <form onSubmit={handleCreateBooking}>
                <h3>Create New Booking</h3>
                <select value={selectedAirline} onChange={e => setSelectedAirline(e.target.value)} required>
                    <option value="" disabled>Select Airline</option>
                    {airlines.map((airline) => (
                        <option key={airline.id} value={airline.id}>
                            {airline.name}
                        </option>
                    ))}
                </select>
                <select value={selectedFlight} onChange={e => setSelectedFlight(e.target.value)} required disabled={!selectedAirline}>
                    <option value="" disabled>{selectedAirline ? 'Select Flight' : 'Select an Airline first'}</option>
                    {flights.map(flight => (
                        <option key={flight.id} value={flight.flight_number}>
                            {flight.flight_number} - {flight.departure_airport} to {flight.arrival_airport}
                        </option>
                    ))}
                </select>
                <input type="date" value={newBooking.booking_date} onChange={e => setNewBooking({ ...newBooking, booking_date: e.target.value })} placeholder="Booking Date" />
                <input type="number" value={newBooking.num_passengers} onChange={e => setNewBooking({ ...newBooking, num_passengers: e.target.value })} placeholder="Number of Passengers" />
                <p>Total Cost: {totalCost >= 0.0 ? totalCost.toFixed(2): "Not Fixed Yet"}</p>
                <button className="flight-form-button" type="submit">Create Booking</button>
            </form>
            <div>
                <h3>Bookings:</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Flight Number</th>
                            <th>Airline</th>
                            <th>Route</th>
                            <th>Arrival</th>
                            <th>Departure</th>
                            <th>Booking For</th>
                            <th>Total Cost</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bookings.map((booking, index) => (
                            <>
                                <tr key={index} onClick={() => toggleDetails(index)} className="detail-row">
                                    <td>{booking.bookings.booking_date}</td>
                                    <td>{booking.bookings.flight.flight_number}</td>
                                    <td>{booking.bookings.flight.airline.airline_name}</td>
                                    <td>{booking.bookings.flight.departure_airport} to {booking.bookings.flight.arrival_airport}</td>
                                    <td>{booking.bookings.flight.arrival_time}</td>
                                    <td>{booking.bookings.flight.departure_time}</td>
                                    <td>{booking.bookings.num_passengers}</td>
                                    <td>${booking.bookings.total_cost}</td>
                                    <button className="flight-form-button" onClick={() => handleDeleteBooking(booking.bookings.booking_id)}>Delete</button>
                                </tr>
                                {expanded === index && (
                                    <tr>
                                        <td colSpan="8" className="detail-info">
                                            AirCraft_Type : {booking.bookings.flight.aircraft_type}<br/>
                                            Airline's Support : <a href={`mailto:${booking.bookings.flight.airline.contact_email}`}> Mail </a> 
                                            or <a href={`tel:${booking.bookings.flight.airline.contact_phone}`}>Call</a><br/>
                                            AirCraft Type : {booking.bookings.flight.aircraft_type}<br/>
                                            Total Passengers: {booking.bookings.flight.num_seats}<br/>
                                        </td>
                                    </tr>
                                )}
                            </>
                        ))}
                    </tbody>
                </table>
            </div>
            <p>{message}</p>
        </div>
    );
}

export default Users;
