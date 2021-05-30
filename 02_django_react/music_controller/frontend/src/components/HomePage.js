import React from 'react'
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <>
      <p>
        This is the homepage
      </p>
      <ul>
        <li><Link to="/join">Link to JOIN page</Link></li>
        <li><Link to="/create">Link to CREATE page</Link></li>
        <li><Link to="/api/create-room">Link to API:create-room</Link></li>
        <li><Link to="/api/rooms">Link to API:rooms</Link></li>
      </ul>
    </>
  )
}

export default HomePage
