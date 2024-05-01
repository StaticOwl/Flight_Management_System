import React, { createContext, useReducer } from 'react';

const initialState = {
  users: [],
};

const GlobalContext = createContext(initialState);

const reducer = (state, action) => {
  switch (action.type) {
    case 'ADD_USER':
      return { ...state, users: [...state.users, action.payload] };
    case 'UPDATE_USER':
      return {
        ...state,
        users: state.users.map(user => 
          user.id === action.payload.id ? action.payload : user
        )
      };
    case 'DELETE_USER':
      return {
        ...state,
        users: state.users.filter(user => user.id !== action.payload)
      };
    default:
      return state;
  }
};

export const GlobalProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const addUser = (user) => {
    dispatch({ type: 'ADD_USER', payload: user });
  };

  const updateUser = (user) => {
    dispatch({ type: 'UPDATE_USER', payload: user });
  };

  const deleteUser = (userId) => {
    dispatch({ type: 'DELETE_USER', payload: userId });
  };

  return (
    <GlobalContext.Provider value={{
      users: state.users,
      addUser,
      updateUser,
      deleteUser
    }}>
      {children}
    </GlobalContext.Provider>
  );
};

export { GlobalContext };
