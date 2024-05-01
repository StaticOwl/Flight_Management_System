import React, { createContext, useReducer } from 'react';

const initialState = {
  users: [],
  bookings: [],
  flights: [],
  crews: []
};

const GlobalContext = createContext(initialState);

const reducer = (state, action) => {
  switch (action.type) {
    case 'ADD_USER':
      return { ...state, users: [...state.users, action.payload] };
    // Define more cases as needed
    default:
      return state;
  }
};

export const GlobalProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const addUser = (user) => {
    dispatch({ type: 'ADD_USER', payload: user });
  };

  return (
    <GlobalContext.Provider value={{ users: state.users, addUser }}>
      {children}
    </GlobalContext.Provider>
  );
};

export { GlobalContext };
