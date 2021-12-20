import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import { AppBar, Button, CssBaseline, Toolbar } from "@mui/material";
import { styled } from "@mui/material/styles";

import Analytics from "./components/screens/Analytics";
import Home from "./components/screens/Home";
import People from "./components/screens/People";

const HeaderButton = styled(Button)(() => ({
  color: "white",
  fontSize: "1rem",
}));

const App = () => {
  return (
    <Router>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Link to="/">
            <HeaderButton>CW CRM</HeaderButton>
          </Link>

          <Link to="/people">
            <HeaderButton>People</HeaderButton>
          </Link>

          <Link to="/analytics">
            <HeaderButton>Analytics</HeaderButton>
          </Link>
        </Toolbar>
      </AppBar>
      <main>
        <Switch>
          <Route path="/analytics">
            <Analytics />
          </Route>
          <Route path="/people">
            <People />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </main>
    </Router>
  );
};

export default App;
