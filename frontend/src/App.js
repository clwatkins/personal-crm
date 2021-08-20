import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import { ThemeProvider } from "@material-ui/styles";
import { createMuiTheme } from "@material-ui/core/styles";
import { blue, indigo } from "@material-ui/core/colors";

import Main from "./components/Main";
import Analytics from "./components/Analytics";

const theme = createMuiTheme({
  palette: {
    secondary: {
      main: blue[900],
    },
    primary: {
      main: indigo[700],
    },
  },
  typography: {
    // Use the system font instead of the default Roboto font.
    fontFamily: ['"Lato"', "sans-serif"].join(","),
  },
});

export default function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/analytics">Analytics</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/analytics">
            <ThemeProvider theme={theme}>
              <Analytics />
            </ThemeProvider>
          </Route>
          <Route path="/">
            <ThemeProvider theme={theme}>
              <Main />
            </ThemeProvider>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}
