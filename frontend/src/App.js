import React from "react";
import store from './store';
import { Provider, useSelector } from 'react-redux';
import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";

import { CssBaseline } from "@mui/material";

import AppBar from "./components/AppBar";
import Login from "./components/Login";
import Analytics from "./components/Analytics";
import Home from "./components/Home";
import People from "./components/People";

function PrivateRoute({ children, ...rest }) {
  const isLoggedIn = useSelector(state => state.auth.isLoggedIn);
  
  return (
    <Route
      {...rest}
      render={({ location }) =>
        isLoggedIn ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: location }
            }}
          />
        )
      }
    />
  );
}

const App = () => {
  return (
    <Provider store={store}>
      <Router>
        <CssBaseline />
        <AppBar />
        <main>
          <Switch>
            <Route exact path="/login">
              <Login />
            </Route>
            <PrivateRoute exact path="/analytics">
              <Analytics />
            </PrivateRoute>
            <PrivateRoute exact path="/people">
              <People />
            </PrivateRoute>
            <PrivateRoute exact path="/">
              <Home />
            </PrivateRoute>
          </Switch>
        </main>
      </Router>
    </Provider>
  );
};

export default App;
