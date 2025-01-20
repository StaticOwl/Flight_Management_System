import React, { useState, useEffect } from 'react';
import ApiService from '../api/ApiService';
import '../App.css';  // Ensure this is the path to your CSS

function Flights() {
    const [flights, setFlights] = useState([]);
    const [airlines, setAirlines] = useState([]);
    const [selectedAirline, setSelectedAirline] = useState('');
    const [showAddFlight, setShowAddFlight] = useState(false);
    const [newFlight, setNewFlight] = useState({
        flight_number: '',
        departure_airport: '',
        arrival_airport: ''
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
            const response = await ApiService.addFlight(newFlight);
            setFlights([...flights, response]);
            setShowAddFlight(false);
            setNewFlight({ flightNumber: '', departureAirport: '', arrivalAirport: '' });
        } catch (error) {
            setMessage('Failed to add flight');
        }
    };

    // const handleUpdateFlight = async (flight, index) => {
    //     try {
    //         const response = await ApiService.updateFlight(flight);
    //         let updatedFlights = [...flights];
    //         updatedFlights[index] = response;
    //         setFlights(updatedFlights);
    //         setEditingIndex(-1);
    //     } catch (error) {
    //         setMessage('Failed to update flight');
    //     }
    // };

    const renderFlightForm = () => (
        <tr>
            <td><input className="flight-form-input" value={newFlight.flight_number} onChange={e => setNewFlight({ ...newFlight, flight_number: e.target.value })} placeholder="Flight Number" /></td>
            <td><input className="flight-form-input" value={newFlight.departure_airport} onChange={e => setNewFlight({ ...newFlight, departure_airport: e.target.value })} placeholder="Departure Airport" /></td>
            <td><input className="flight-form-input" value={newFlight.arrival_airport} onChange={e => setNewFlight({ ...newFlight, arrival_airport: e.target.value })} placeholder="Arrival Airport" /></td>
            <td><button className="flight-form-button" onClick={handleAddFlight}>Save Flight</button></td>
        </tr>
    );

    const renderFlights = () => flights.map((flight, index) => (
        <tr key={index}>
            <td>{flight.flight_number}</td>
            <td>{flight.departure_airport}</td>
            <td>{flight.arrival_airport}</td>
            <td><button className="flight-form-button" onClick={() => setEditingIndex(index)}>Update</button></td>
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
                    <button className="flight-form-button" onClick={() => setShowAddFlight(!showAddFlight)}>Add Flight</button>
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
