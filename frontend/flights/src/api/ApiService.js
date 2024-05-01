import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const login = (email, password) => {
    return axios.post(`${API_BASE_URL}/login`, {email, password});
};

const createUser = (userData) => {
    console.log(userData);
    return axios.post(`${API_BASE_URL}/createuser`, userData);
};

const getUser = (userId) => {
    return axios.get(`${API_BASE_URL}/users/${userId}`);
};

const updateUser = (userId, userData) => {
    return axios.put(`${API_BASE_URL}/users/${userId}`, userData);
};

const deleteUser = (userId) => {
    return axios.delete(`${API_BASE_URL}/users/${userId}/delete`);
};

export default {
    createUser,
    getUser,
    updateUser,
    deleteUser,
    login
};
