import React, {useEffect, useState} from 'react';
import ApiService from '../api/ApiService';
import '../App.css'; // Ensure styles are properly linked

function ManageUsers() {
    const [users, setUsers] = useState([]);
    const [editingIndex, setEditingIndex] = useState(-1);
    const [message, setMessage] = useState('');
    const [refresh, setRefresh] = useState(true);

    useEffect(() => {
        if (refresh) {
            fetchUsers();
            setRefresh(false);
        }
    }, [refresh]);
    

    const fetchUsers = async () => {
        try {
            const response = await ApiService.getUsers();
            console.log(response);
            setUsers(response);
        } catch (error) {
            setMessage('Failed to fetch users');
        }
    };

    const handleUpdateUser = async (index) => {
        const userToUpdate = users[index];
        if (!userToUpdate.first_name || !userToUpdate.last_name || !userToUpdate.email || !userToUpdate.phone || !userToUpdate.address) {
            setMessage('All fields must be filled');
            return;
        }
        console.log('updating user', index, userToUpdate);
        try {
            const response = await ApiService.updateUser2(userToUpdate);
            let updatedUsers = [...users];
            updatedUsers[index] = response;
            setUsers(updatedUsers);
            setEditingIndex(-1);
        } catch (error) {
            setMessage('Failed to update user member', error);
        }
    };

    const renderUserForm = (user, index) => (
        <tr key={index}>
            <td><input value={user.first_name} onChange={e => updateUserField(index, 'first_name', e.target.value)} /></td>
            <td><input value={user.last_name} onChange={e => updateUserField(index, 'last_name', e.target.value)} /></td>
            <td><input value={user.email} onChange={e => updateUserField(index, 'email', e.target.value)} /></td>
            <td><input value={user.phone} onChange={e => updateUserField(index, 'phone', e.target.value)} /></td>
            <td><input value={user.address} onChange={e => updateUserField(index, 'address', e.target.value)} /></td>
            <td><button onClick={() => handleUpdateUser(index)}>Save</button></td>
        </tr>
    );

    const updateUserField = (index, field, value) => {
        let updatedUsers = [...users];
        updatedUsers[index] = {...updatedUsers[index], [field]: value};
        setUsers(updatedUsers);
    };

    return (
        <div className="crew-dashboard">
            <h2>User Management</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user, index) => (
                        editingIndex === index ? renderUserForm(user, index) : (
                            <tr key={index}>
                                <td>{user.first_name} {user.last_name}</td>
                                <td>{user.email}</td>
                                <td>{user.phone}</td>
                                <td>{user.address}</td>
                                <td><button onClick={() => setEditingIndex(index)}>Update</button></td>
                            </tr>
                        )
                    ))}
                </tbody>
            </table>
            {message && <p>{message}</p>}
        </div>
    );
}

export default ManageUsers;
