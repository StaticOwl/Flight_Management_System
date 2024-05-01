import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GlobalProvider } from './context/GlobalState';
import Users from './components/Users';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Handler to update login state based on local storage
    const updateLoginStatus = () => {
      const token = localStorage.getItem('token');
      setIsLoggedIn(!!token);
      console.log(isLoggedIn); // Will still log the previous state due to closures
    };

    // Listen to a custom event, e.g., 'authChange'
    window.addEventListener('authChange', updateLoginStatus);

    // Initial check on component mount
    updateLoginStatus();

    // Cleanup listener on component unmount
    return () => window.removeEventListener('authChange', updateLoginStatus);
  }, []);  // Still empty because the handler itself handles updates

  return (
    <GlobalProvider>
      <Router>
        <div className="app-container">
          <Navigation isLoggedIn={isLoggedIn}/>
          <div className="content">
            <Routes>
              <Route path="/users" element={isLoggedIn ? <Users /> : <Navigate to="/login" replace />} />
              <Route path="/login" element={isLoggedIn ? <Navigate to="/" replace /> : <Login />} />
              <Route path="/register" element={isLoggedIn ? <Navigate to="/" replace /> : <Register />} />
              <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" replace />} />
            </Routes>
          </div>
        </div>
      </Router>
    </GlobalProvider>
  );
}

export default App;
