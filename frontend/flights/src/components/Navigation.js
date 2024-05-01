import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../App.css';

const Navigation = ({ isLoggedIn }) => {

  const Navigate = useNavigate();

  const handleLogout = (event) => {
    event.preventDefault();  // Prevent the link from navigating
    localStorage.removeItem('token');  // Remove the token from local storage
    // setIsLoggedIn(false);  // Update the state to false
    window.dispatchEvent(new Event('authChange'));  // Navigate to login page
    Navigate('/login');
  };


  return (
    <nav className='navbar'>
      <ul className='nav-links'>
        {isLoggedIn && (
          <>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/users">Users</Link></li>
            <li><Link to="/bookings">Bookings</Link></li>
            <li><Link to="/flights">Flights</Link></li>
            <li><Link to="/crews">Crews</Link></li>
            <li><Link to="/airports">Airports</Link></li>
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
