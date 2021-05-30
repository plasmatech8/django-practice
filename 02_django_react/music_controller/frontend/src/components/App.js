import React from "react";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import HomePage from './HomePage'
import JoinRoomPage from './JoinRoomPage'
import CreateRoomPage from './CreateRoomPage'
import NotFoundPage from './NotFoundPage'

function App() {
  return (
    <div>
      <Router>
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
