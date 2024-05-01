import React from 'react'

function Home() {
    const user = localStorage.getItem('user');
    return (
      <div>
          <h1>Hello {user}</h1>
          <h2>Welcome to the Flights App</h2>
      </div>
    )
}

export default Home
