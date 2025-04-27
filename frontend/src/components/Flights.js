import React, {useEffect, useState} from 'react';
import ApiService from '../api/ApiService';
import '../App.css'; // Ensure this is the path to your CSS

function Flights() {
    const [flights, setFlights] = useState([]);
    const [airlines, setAirlines] = useState([]);
    const [selectedAirline, setSelectedAirline] = useState('');
    const [showAddFlight, setShowAddFlight] = useState(false);
    const [newFlight, setNewFlight] = useState({
        airline_id: '',  // ADD
        flight_number: '',
        departure_airport: '',
        arrival_airport: '',
        departure_time: '',
        arrival_time: '',
        aircraft_type: '',
        num_seats: '',
        price_per_seat: ''
    });

    const [editingIndex, setEditingIndex] = useState(-1);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchAirlines = async () => {
            try {
                const response = await ApiService.getAirlines();
                setAirlines(response);
            } catch (error) {
                setMessage('Failed to fetch airlines');
            }
        };
        fetchAirlines();
    }, []);

    useEffect(() => {
        if (selectedAirline) {
            const fetchFlights = async () => {
                try {
                    const response = await ApiService.getFlightsByAirline(selectedAirline);
                    setFlights(response);
                } catch (error) {
                    setMessage('Failed to fetch flights');
                }
            };
            fetchFlights();
        } else {
            setFlights([]);
        }
    }, [selectedAirline]);

    const handleAddFlight = async () => {
        try {
            const flightData = {...newFlight, airline_id: selectedAirline};
            const response = await ApiService.addFlight(flightData);
            setFlights([...flights, response]);
            setShowAddFlight(false);
            setNewFlight({
                flight_number: '',
                departure_airport: '',
                arrival_airport: '',
                departure_time: '',
                arrival_time: '',
                aircraft_type: '',
                num_seats: '',
                price_per_seat: ''
            });
        } catch (error) {
            setMessage('Failed to add flight');
        }
    };


    const renderFlightForm = () => (
        <div className="flight-modal-overlay">
            <div className="flight-modal">
                <h3>Add New Flight</h3>
                <input
                    placeholder="Flight Number"
                    value={newFlight.flight_number}
                    onChange={e => setNewFlight({...newFlight, flight_number: e.target.value})}
                />
                <input
                    placeholder="Departure Airport"
                    value={newFlight.departure_airport}
                    onChange={e => setNewFlight({...newFlight, departure_airport: e.target.value})}
                />
                <input
                    placeholder="Arrival Airport"
                    value={newFlight.arrival_airport}
                    onChange={e => setNewFlight({...newFlight, arrival_airport: e.target.value})}
                />
                <input
                    type="datetime-local"
                    placeholder="Departure Time"
                    value={newFlight.departure_time}
                    onChange={e => setNewFlight({...newFlight, departure_time: e.target.value})}
                />
                <input
                    type="datetime-local"
                    placeholder="Arrival Time"
                    value={newFlight.arrival_time}
                    onChange={e => setNewFlight({...newFlight, arrival_time: e.target.value})}
                />
                <input
                    placeholder="Aircraft Type"
                    value={newFlight.aircraft_type}
                    onChange={e => setNewFlight({...newFlight, aircraft_type: e.target.value})}
                />
                <input
                    type="number"
                    placeholder="Number of Seats"
                    value={newFlight.num_seats}
                    onChange={e => setNewFlight({...newFlight, num_seats: e.target.value})}
                />
                <input
                    type="number"
                    step="0.01"
                    placeholder="Price Per Seat"
                    value={newFlight.price_per_seat}
                    onChange={e => setNewFlight({...newFlight, price_per_seat: e.target.value})}
                />

                <div className="flight-modal-actions">
                    <button onClick={() => setShowAddFlight(false)}>Cancel</button>
                    <button onClick={handleAddFlight}>Save Flight</button>
                </div>
            </div>
        </div>
    );


    const renderFlights = () => flights.map((flight, index) => (
        <tr key={index}>
            <td>{flight.flight_number}</td>
            <td>{flight.departure_airport}</td>
            <td>{flight.arrival_airport}</td>
            <td>
                <button className="flight-form-button" onClick={() => setEditingIndex(index)}>Update</button>
            </td>
        </tr>
    ));

    return (
        <div className="flight-management-container">
            <div className="flight-management-header">
                <h2>Flight Management</h2>
                <div className="flight-management-actions">
                    <select value={selectedAirline} onChange={e => setSelectedAirline(e.target.value)}>
                        <option value="">Select Airline</option>
                        {airlines.map(airline => (
                            <option key={airline.id} value={airline.id}>{airline.name}</option>
                        ))}
                    </select>
                    <button className="flight-form-button" onClick={() => setShowAddFlight(!showAddFlight)}>Add Flight
                    </button>
                </div>
            </div>
            {showAddFlight && renderFlightForm()}
            <table className="flight-table">
                <thead>
                <tr>
                    <th>Flight Number</th>
                    <th>Departure Airport</th>
                    <th>Arrival Airport</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {editingIndex === -1 ? renderFlights() : renderFlightForm(editingIndex)}
                </tbody>
            </table>
            {message && <p className="error-message">{message}</p>}
        </div>
    );
}

export default Flights;
