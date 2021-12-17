import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import {
  AppBar,
  Button,
  CssBaseline,
  Toolbar,
  Typography,
} from "@mui/material";
import { styled } from "@mui/material/styles";

import Analytics from "./components/Analytics";
import Main from "./components/Main";
import People from "./components/People";

const HeaderButton = styled(Button)(() => ({
  color: "white",
  padding: "20px",
  fontSize: "16px",
}));

const App = () => {
  return (
    <Router>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Welcome back...</Typography>
          <Link to="/">
            <HeaderButton>Home</HeaderButton>
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
            <Main />
          </Route>
        </Switch>
      </main>
    </Router>
  );
};

export default App;
