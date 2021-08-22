import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import {
  AppBar,
  Button,
  CssBaseline,
  Toolbar,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import Analytics from "./components/Analytics";
import Main from "./components/Main";
import People from "./components/People";

const App = () => {
  const useStyles = makeStyles({
    root: {
      color: "white",
      padding: "20px",
      fontSize: "16px",
    },
  });
  const style = useStyles();

  return (
    <Router>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Welcome back...</Typography>
          <Link to="/">
            <Button className={style.root}>Home</Button>
          </Link>

          <Link to="/people">
            <Button className={style.root}>People</Button>
          </Link>

          <Link to="/analytics">
            <Button className={style.root}>Analytics</Button>
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
