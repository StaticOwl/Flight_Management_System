import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ApiService from '../api/ApiService';
import '../App.css';

const Navigation = ({ isLoggedIn }) => {

  const Navigate = useNavigate();
  const [userId, setUserId] = useState(0);

  const handleLogout = (event) => {
    event.preventDefault(); 
    localStorage.removeItem('token'); 
    window.dispatchEvent(new Event('authChange')); 
    Navigate('/login');
  };

  useEffect(() => {
    if (isLoggedIn) {
      const fetchUserId = async () => {
        try {
          const response = await ApiService.getUserIDFromToken();
          console.log('User ID:', response);
          setUserId(response);
          console.log('User ID Updated:', userId);
        } catch (error) {
          console.error('Error fetching user ID:', error);
        }
      };

      fetchUserId();
    }
  }, [isLoggedIn, userId]);


  return (
    <nav className='navbar'>
      <ul className='nav-links'>
        {isLoggedIn && (
          <>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/users">{localStorage.getItem('user')}'s DashBoard</Link></li>
            <li><Link to="/flights">Flights</Link></li>
            <li><Link to="/crews">Crews</Link></li>
            <li><a href="/logout" onClick={handleLogout}>Logout</a></li>
          </>
        )}
        {!isLoggedIn && (
            <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
            </>
        )}
      </ul>
    </nav>
  );
}

export default Navigation;
