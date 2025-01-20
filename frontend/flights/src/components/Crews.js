import React, { useState, useEffect } from 'react';
import ApiService from '../api/ApiService';
import '../App.css';  // Ensure styles are properly linked

function Crews() {
    const [crews, setCrews] = useState([]);
    const [flights, setFlights] = useState([]);
    const [roles, setRoles] = useState([]);
    const [newCrew, setNewCrew] = useState({
        first_name: '',
        last_name: '',
        flight_id: '',
        role_id: ''
    });
    const [editingIndex, setEditingIndex] = useState(-1);
    const [message, setMessage] = useState('');
    const [refresh, setRefresh] = useState(true);

    useEffect(() => {
        if (refresh) {
            fetchCrews();
            fetchFlightsAndRoles();
            setRefresh(false);
        }
    }, [refresh]);
    

    const fetchCrews = async () => {
        try {
            const response = await ApiService.getCrews();
            setCrews(response);
        } catch (error) {
            setMessage('Failed to fetch crews');
        }
    };

    const fetchFlightsAndRoles = async () => {
        try {
            const flightsResponse = await ApiService.getFlights();
            const rolesResponse = await ApiService.getRoles();
            setFlights(flightsResponse);
            setRoles(rolesResponse);
        } catch (error) {
            setMessage('Failed to fetch flights or roles');
        }
    };

    const handleAddCrew = async () => {
        if (!newCrew.first_name || !newCrew.last_name || !newCrew.flight_id || !newCrew.role_id) {
            setMessage('All fields must be filled');
            return;
        }
        try {
            const response = await ApiService.addCrew(newCrew);
            // setCrews([...crews, response]);
            setRefresh(true);
            setNewCrew({ first_name: '', last_name: '', flight_id: '', role_id: '' });
        } catch (error) {
            setMessage('Failed to add crew member'+error);
        }
    };

    const handleUpdateCrew = async (index) => {
        const crewToUpdate = crews[index];
        if (!crewToUpdate.first_name || !crewToUpdate.last_name || !crewToUpdate.flight_id || !crewToUpdate.role_id) {
            setMessage('All fields must be filled');
            return;
        }
        console.log('updating crew', index);
        try {
            const response = await ApiService.updateCrew(crewToUpdate);
            let updatedCrews = [...crews];
            updatedCrews[index] = response;
            setCrews(updatedCrews);
            setEditingIndex(-1);
        } catch (error) {
            setMessage('Failed to update crew member', error);
        }
    };

    const renderCrewForm = (crew, index) => (
        <tr key={index}>
            <td><input value={crew.first_name} onChange={e => updateCrewField(index, 'first_name', e.target.value)} /></td>
            <td><input value={crew.last_name} onChange={e => updateCrewField(index, 'last_name', e.target.value)} /></td>
            <td>
                <select value={crew.flight_id} onChange={e => updateCrewField(index, 'flight_id', e.target.value)}>
                    {flights.map(flight => (
                        <option key={flight.id} value={flight.id}>{flight.flight_number}</option>
                    ))}
                </select>
            </td>
            <td>
                <select value={crew.role_id} onChange={e => updateCrewField(index, 'role_id', e.target.value)}>
                    {roles.map(role => (
                        <option key={role.id} value={role.id}>{role.role_name}</option>
                    ))}
                </select>
            </td>
            <td><button onClick={() => handleUpdateCrew(index)}>Save</button></td>
        </tr>
    );

    const updateCrewField = (index, field, value) => {
        let updatedCrews = [...crews];
        updatedCrews[index] = {...updatedCrews[index], [field]: value};
        setCrews(updatedCrews);
    };

    return (
        <div className="crew-dashboard">
            <h2>Crew Management</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Assigned Flight</th>
                        <th>Role</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {crews.map((crew, index) => (
                        editingIndex === index ? renderCrewForm(crew, index) : (
                            <tr key={index}>
                                <td>{crew.name}</td>
                                <td>Flight {crew.flight_number}</td>
                                <td>{crew.role}</td>
                                <td><button onClick={() => setEditingIndex(index)}>Update</button></td>
                            </tr>
                        )
                    ))}
                    <tr>
                        <td><input value={newCrew.first_name} onChange={e => setNewCrew({ ...newCrew, first_name: e.target.value })} placeholder="First Name" /></td>
                        <td><input value={newCrew.last_name} onChange={e => setNewCrew({ ...newCrew, last_name: e.target.value })} placeholder="Last Name" /></td>
                        <td>
                            <select value={newCrew.flight_id} onChange={e => setNewCrew({ ...newCrew, flight_id: e.target.value })}>
                                <option value="">Select Flight</option>
                                {flights.map(flight => (
                                    <option key={flight.id} value={flight.id}>{flight.flight_number}</option>
                                ))}
                            </select>
                        </td>
                        <td>
                            <select value={newCrew.role_id} onChange={e => setNewCrew({ ...newCrew, role_id: e.target.value })}>
                                <option value="">Select Role</option>
                                {roles.map(role => (
                                    <option key={role.id} value={role.id}>{role.role_name}</option>
                                ))}
                            </select>
                        </td>
                        <td><button onClick={handleAddCrew}>Add Crew</button></td>
                    </tr>
                </tbody>
            </table>
            {message && <p>{message}</p>}
        </div>
    );
}

export default Crews;
