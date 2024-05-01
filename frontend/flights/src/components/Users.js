import React, { useState } from 'react';
import ApiService from '../api/ApiService';

function Users() {
    const [user, setUser] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        phone: '',
        address: ''
    });
    const [userId, setUserId] = useState('');
    const [message, setMessage] = useState('');
    const [userDetailsVisible, setUserDetailsVisible] = useState(0);

    const resetData = () => {
        setUser({
            firstName: '',
            lastName: '',
            email: '',
            password: '',
            phone: '',
            address: ''
        });
        setUserId('');
        setMessage('');
        setUserDetailsVisible(0);
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser(prevState => ({ ...prevState, [name]: value }));
    };

    const handleCreateUser = async () => {
        try {
            const response = await ApiService.createUser(user);
            setMessage(`User Created: ${JSON.stringify(response.data)}`);
        } catch (error) {
            setMessage('Error creating user: ' + error.message);
        }
    };

    const callCreateUser = () => {
        setUser({
            first_name: '',
            last_name: '',
            email: '',
            password: '',
            phone: '',
            address: ''
        });
        setUserDetailsVisible(5);
        setMessage('Create a New User');
    };

    const callFetchUser = () => {
        setUserDetailsVisible(2);
        setMessage('Fetching User Data');
    };
    const callUpdateUser = () => {
        setMessage('Update the Data In Place');
        setUserDetailsVisible(4);
    };

    const handleGetUser = async () => {
        try {
            const response = await ApiService.getUser(userId);
            setUser(response.data);
            setMessage('User data fetched successfully');
            setUserDetailsVisible(3); // Set a state variable to indicate that user details should be displayed
        } catch (error) {
            const errorMessage = error.response ? error.response.data.message : error.message;
            setMessage('Error fetching user data: ' + errorMessage);
            console.error('Error:', error); // Log the error details to console
        }
    };
    

    const handleUpdateUser = async () => {
        try {
            await ApiService.updateUser(userId, user);
            setMessage('User updated successfully');
        } catch (error) {
            setMessage('Error updating user: ' + error.message);
        }
    };

    const handleDeleteUser = async () => {
        const confirmed = window.confirm('This can\'t be undone. Are you sure you want to delete this user?');
        if (!confirmed) {
            return;
        }
        try {
            await ApiService.deleteUser(userId);
            setMessage('User deleted successfully');
            setUser({
                first_name: '',
                last_name: '',
                email: '',
                password: '',
                phone: '',
                address: ''
            }); // Clear the form after deletion
        } catch (error) {
            setMessage('Error deleting user: ' + error.message);
        }
    };

    const form = () => {
        return (
            <div>
                <input type="text" name="firstName" value={user.first_name} onChange={handleChange} placeholder="First Name" />
                <input type="text" name="lastName" value={user.last_name} onChange={handleChange} placeholder="Last Name" />
                <input type="email" name="email" value={user.email} onChange={handleChange} placeholder="Email" />
                <input type="password" name="password" value={user.password} onChange={handleChange} placeholder="Password" />
                <input type="text" name="phone" value={user.phone} onChange={handleChange} placeholder="Phone" />
                <input type="text" name="address" value={user.address} onChange={handleChange} placeholder="Address" />
            </div>
        );
    }

    return (
        <div>
            <h2>User Operations</h2>
            {/* <button onClick={history.back()}>Create User</button> */}
            <button onClick={callCreateUser}>Create User</button>
            <button onClick={callFetchUser}>Fetch User Data</button>
            <button onClick={resetData}>Reset</button>
            <p>{message}</p>
            {userDetailsVisible==2 && (
               <div> 
                    <div>
                        <input type="text" value={userId} onChange={e => setUserId(e.target.value)} placeholder="Enter User ID to operate on" />
                        <button onClick={handleGetUser}>Fetch User Data</button>
                    </div>
                </div> 
            )}
            <div>
                {userDetailsVisible==3 && (
                <div>    
                    <div>
                        <h2>User Details</h2>
                        <p>First Name: {user.first_name}</p>
                        <p>Last Name: {user.last_name}</p>
                        <p>Email: {user.email}</p>
                    {/* Add other user details as needed */}
                    </div>
                    <div>
                        <button onClick={callUpdateUser}>Update User Profile</button>
                        <button onClick={handleDeleteUser}>Delete User Account</button>
                    </div>
                </div>
                )}
            </div>
            {(userDetailsVisible === 4 || userDetailsVisible === 5) && (
            <div>
                <div>
                    {form()}
                </div>
                {userDetailsVisible == 4 && (
                    <div>
                        <button onClick={handleUpdateUser}>Submit Changes</button>
                    </div>
                )}
                {userDetailsVisible == 5 && (
                    <div>
                        <button onClick={handleCreateUser}>Create New User</button>
                    </div>
                )}
            </div>)}
        </div>
    );
}

export default Users;
