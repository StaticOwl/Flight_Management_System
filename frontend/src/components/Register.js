import React, {useState} from 'react';
import ApiService from '../api/ApiService';
import {useNavigate} from 'react-router-dom';

const Register = () => {
  const [user, setUser] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    phone: '',
    address: ''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUser(prevState => ({ ...prevState, [name]: value }));
  };

  const validateEmail = (email) => {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return re.test(String(email).toLowerCase());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user.first_name || !user.last_name || !user.email || !user.password || !user.phone) {
      setMessage('Please fill in all required fields.');
      return;
    }
    if (!validateEmail(user.email)) {
      setMessage('Invalid email format.');
      return;
    }
    try {
      await ApiService.createUser(user);
      setMessage('Registration successful');
      setTimeout(() => {
        navigate('/login'); // Navigate after a delay
      }, 2000);
    } catch (error) {
      setMessage('Error registering user: ' + error.message);
    }
  };

  return (
    <div className="register-container">
      <h2>Register User</h2>
      <form onSubmit={handleSubmit} method="POST">
        <input type="text" name="first_name" value={user.first_name} onChange={handleChange} placeholder="First Name" required />
        <input type="text" name="last_name" value={user.last_name} onChange={handleChange} placeholder="Last Name" required />
        <input type="email" name="email" value={user.email} onChange={handleChange} placeholder="Email" required />
        <input type="password" name="password" value={user.password} onChange={handleChange} placeholder="Password" required />
        <input type="text" name="phone" value={user.phone} onChange={handleChange} placeholder="Phone" required/>
        <input type="text" name="address" value={user.address} onChange={handleChange} placeholder="Address" />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Register;
