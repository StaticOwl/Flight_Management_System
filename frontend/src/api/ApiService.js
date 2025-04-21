import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const login = (email, password) => {
    return axios.post(`${API_BASE_URL}/login`, {email, password});
};

const createUser = (userData) => {
    console.log(userData);
    return axios.post(`${API_BASE_URL}/createuser`, userData);
};

const getUser = async() => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_BASE_URL}/users`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;  // Assuming the response structure { user_id: "xyz" }
    } catch (error) {
        console.error('Error fetching user ID:', error);
        return null;  // Handle error appropriately
    }
};

const getUsers = async() => {
    const response = await fetch(`${API_BASE_URL}/fetchusers`);
    return await response.json();
}

const updateUser2 = async (user) => {
    try{
        const token = localStorage.getItem('token')
        const response = await axios.put(`${API_BASE_URL}/update-user/${user.user_id}`, user, {
            headers:{
                'Content-Type':'application/json',
                Authorization : `Bearer ${token}`
            }
        });
        return response.success;
    }
    catch(error){
        console.error('Error Updating Data:', error);
        return false;
    }
};

const updateUser = async (user) => {
    try{
        const token = localStorage.getItem('token')
        const response = await axios.put(`${API_BASE_URL}/users`, user, {
            headers:{
                'Content-Type':'application/json',
                Authorization : `Bearer ${token}`
            }
        });
        return response.success;
    }
    catch(error){
        console.error('Error Updating Data:', error);
        return false;
    }
};

const deleteUser = (userId) => {
    return axios.delete(`${API_BASE_URL}/users/${userId}/delete`);
};

const getUserIDFromToken = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_BASE_URL}/token`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data.user_id;  // Assuming the response structure { user_id: "xyz" }
    } catch (error) {
        console.error('Error fetching user ID:', error);
        return null;  // Handle error appropriately
    }
}

const getUserBookings = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_BASE_URL}/users/bookings`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching user bookings:', error);
        return null;  // Handle error appropriately
    }

}

const createBooking = async(bookingData) => {
    const response = await fetch(`${API_BASE_URL}/createbooking`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(bookingData)
    });
    return await response.json();
}

const deleteBooking = async(bookingId) => {
    const response = await fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    });
    return await response.json();
}

const getAirlines = async() => {
    const response = await fetch(`${API_BASE_URL}/airlines`);
    return await response.json();
}

const getFlightsByAirline = async(airlineId) => {
    const response = await fetch(`${API_BASE_URL}/flights_by_airlines/${airlineId}`);
    return await response.json();
}


const getCrews = async() => {
    const response = await fetch(`${API_BASE_URL}/getCrew`);
    return await response.json();
}

const addCrew = async(crewData) => {
    const response = await fetch(`${API_BASE_URL}/addCrew`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(crewData)
    });
    return await response.json();
}

const getFlights = async() => {
    const response = await fetch(`${API_BASE_URL}/flights`);
    return await response.json();
}

const getRoles = async() => {
    const response = await fetch(`${API_BASE_URL}/roles`);
    return await response.json();
}

// -------------------- New Role Management Functions --------------------

/**
 * Get all users (admin only)
 */
const getAllUsers = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${API_BASE_URL}/admin/users`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching all users:', error);
        throw error;
    }
};

/**
 * Update a user's role (admin only)
 */
const updateUserRole = async (userId, role) => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.put(
            `${API_BASE_URL}/admin/users/${userId}/role`, 
            { role },
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error updating user role:', error);
        throw error;
    }
};

/**
 * Get current user's role from localStorage
 */
const getCurrentUserRole = () => {
    return localStorage.getItem('role') || 'customer';
};

/**
 * Check if current user has the specified role
 */
const hasRole = (role) => {
    const currentRole = getCurrentUserRole();
    if (Array.isArray(role)) {
        return role.includes(currentRole);
    }
    return currentRole === role;
};

/**
 * Update a flight (crew or admin only)
 */
const updateFlight = async (flightData) => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.put(
            `${API_BASE_URL}/flights/${flightData.flight_id}`,
            flightData,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error updating flight:', error);
        throw error;
    }
};

/**
 * Add a new flight (crew or admin only)
 */
const addFlight = async (flightData) => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
            `${API_BASE_URL}/createflights`,
            flightData,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error adding flight:', error);
        throw error;
    }
};

/**
 * Update an existing crew member (crew or admin only)
 */
const updateCrew = async (crewData) => {
    try {
        const token = localStorage.getItem('token');
        const response = await axios.put(
            `${API_BASE_URL}/update-crew/${crewData.crew_id}`,
            crewData,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error updating crew member:', error);
        throw error;
    }
};

export default {
    createUser,
    getUser,
    getUsers,
    updateUser,
    deleteUser,
    login,
    getUserIDFromToken,
    getUserBookings,
    createBooking,
    deleteBooking,
    getAirlines,
    getFlightsByAirline,
    getCrews,
    getFlights,
    getRoles,
    addCrew,
    getAllUsers,
    updateUserRole,
    getCurrentUserRole,
    hasRole,
    updateFlight,
    addFlight,
    updateCrew
};