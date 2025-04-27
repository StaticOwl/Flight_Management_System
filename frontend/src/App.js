import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import {GlobalProvider} from './context/GlobalState';
import Users from './components/Users';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Navigation from './components/Navigation';
import './App.css';
import Flights from './components/Flights';
import Crews from './components/Crews';
import ManageUsers from "./components/ManageUsers";

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
  }, [isLoggedIn]);  // Still empty because the handler itself handles updates

  return (
    <GlobalProvider>
      <Router>
        <div className="app-container">
          <Navigation isLoggedIn={isLoggedIn}/>
          <div className="content">
            <Routes>
              <Route path="/users" element={isLoggedIn ? <Users /> : <Navigate to="/login" replace />} />
              <Route path="/flights" element={<Flights/>} />
              <Route path="/manage-users" element={isLoggedIn ? <ManageUsers /> : <Navigate to="/login" replace />} />
              <Route path="/login" element={isLoggedIn ? <Navigate to="/" replace /> : <Login />} />
              <Route path="/register" element={isLoggedIn ? <Navigate to="/" replace /> : <Register />} />
              <Route path="/" element={isLoggedIn ? <Home /> : <Navigate to="/login" replace />} />
              <Route path="/crews" element={<Crews/>} />
            </Routes>
          </div>
        </div>
      </Router>
    </GlobalProvider>
  );
}

export default App;
