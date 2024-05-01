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

const updateUser = (userId, userData) => {
    return axios.put(`${API_BASE_URL}/users/${userId}`, userData);
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

export default {
    createUser,
    getUser,
    updateUser,
    deleteUser,
    login,
    getUserIDFromToken,
    getUserBookings,
    createBooking,
    deleteBooking,
    getAirlines,
    getFlightsByAirline
};
