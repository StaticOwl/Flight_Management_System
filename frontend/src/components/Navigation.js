// In Navigation.js
import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ApiService from '../api/ApiService';
import '../App.css';

const Navigation = ({ isLoggedIn }) => {
  const Navigate = useNavigate();
  const [userId, setUserId] = useState(0);
  const [userRole, setUserRole] = useState('');

  const handleLogout = (event) => {
    event.preventDefault(); 
    localStorage.removeItem('token'); 
    localStorage.removeItem('role'); // Clear role on logout
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
          setUserRole(localStorage.getItem('role') || 'customer'); // Get the user's role
        } catch (error) {
          console.error('Error fetching user ID:', error);
        }
      };

      fetchUserId();
    }
  }, [isLoggedIn]);


  return (
    <nav className='navbar'>
      <ul className='nav-links'>
        {isLoggedIn && (
          <>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/users">{localStorage.getItem('user')}'s DashBoard</Link></li>

            {/* Links for all users */}
            <li><Link to="/flights">View Flights</Link></li>

            {/* Links for crew and admin only */}
            {(userRole === 'crew' || userRole === 'admin') && (
              <>
                <li><Link to="/crews">Manage Crews</Link></li>
                <li><Link to="/manage-flights">Manage Flights</Link></li>
              </>
            )}

            {/* Links for admin only */}
            {userRole === 'admin' && (
              <li><Link to="/admin">Admin Panel</Link></li>
            )}

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