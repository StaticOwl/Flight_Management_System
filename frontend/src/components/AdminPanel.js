import React, { useState, useEffect } from 'react';
import ApiService from '../api/ApiService';
import '../App.css';

function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await ApiService.getAllUsers();
      setUsers(response);
      setLoading(false);
    } catch (error) {
      setMessage('Failed to fetch users: ' + (error.response?.data?.message || error.message));
      setLoading(false);
    }
  };

  const handleSelectUser = (user) => {
    setSelectedUser(user);
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      const response = await ApiService.updateUserRole(userId, newRole);
      if (response.success) {
        setMessage(`Role updated successfully for user #${userId}`);
        // Update the user in the list
        setUsers(users.map(user => 
          user.user_id === userId ? { ...user, role: newRole } : user
        ));
        // Update the selected user if it's the one being modified
        if (selectedUser && selectedUser.user_id === userId) {
          setSelectedUser({ ...selectedUser, role: newRole });
        }
      } else {
        setMessage('Failed to update role: ' + response.message);
      }
    } catch (error) {
      setMessage(`Error updating role: ${error.response?.data?.message || error.message}`);
    }
  };

  return (
    <div className="admin-panel">
      <h2>Admin Panel</h2>
      <p>Welcome to the admin management dashboard. Here you can manage users and their roles.</p>
      
      {loading ? (
        <p>Loading users...</p>
      ) : (
        <div className="admin-content">
          <div className="user-list">
            <h3>Users</h3>
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.user_id}>
                    <td>{user.user_id}</td>
                    <td>{user.first_name} {user.last_name}</td>
                    <td>{user.email}</td>
                    <td>{user.role || 'customer'}</td>
                    <td>
                      <button className="view-btn" onClick={() => handleSelectUser(user)}>View</button>
                      <select 
                        value={user.role || 'customer'} 
                        onChange={(e) => handleRoleChange(user.user_id, e.target.value)}
                        className="role-select"
                      >
                        <option value="customer">Customer</option>
                        <option value="crew">Crew</option>
                        <option value="admin">Admin</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {selectedUser && (
            <div className="user-details">
              <h3>User Details</h3>
              <p><strong>ID:</strong> {selectedUser.user_id}</p>
              <p><strong>Name:</strong> {selectedUser.first_name} {selectedUser.last_name}</p>
              <p><strong>Email:</strong> {selectedUser.email}</p>
              <p><strong>Phone:</strong> {selectedUser.phone || 'Not provided'}</p>
              <p><strong>Address:</strong> {selectedUser.address || 'Not provided'}</p>
              <p><strong>Role:</strong> {selectedUser.role || 'customer'}</p>
              
              <div className="user-stats">
                <h4>User Statistics</h4>
                <button className="btn" onClick={() => fetchUserBookings(selectedUser.user_id)}>
                  View Bookings
                </button>
              </div>
            </div>
          )}
        </div>
      )}
      
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default AdminPanel;