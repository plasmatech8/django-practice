import React from "react";
import { BrowserRouter as Router, Link, Redirect, Switch, Route } from 'react-router-dom';

import HomePage from './HomePage'
import JoinRoomPage from './JoinRoomPage'
import CreateRoomPage from './CreateRoomPage'
import NotFoundPage from './NotFoundPage'

function App() {
  return (
    <div>
      <h1>Hello World!</h1>
      <p>Wahoo!!!</p>

      <Router>
        <Link to="/join">Link to JOIN room</Link>

        <Switch>
            <Route exact path='/' component={HomePage} />
            <Route exact path='/join' component={JoinRoomPage} />
            <Route exact path='/create' component={CreateRoomPage} />
            <Route component={NotFoundPage}/>
        </Switch>
      </Router>
    </div>
  )
}

export default App
