import React from "react";
import ReactDOM from "react-dom";
import Helmet from "react-helmet"
import { ThemeProvider } from "@mui/material/styles";

import App from "./App";
import appTheme from "./theme";

ReactDOM.render(
  <React.StrictMode>
    <Helmet>
      <title>CW Personal CRM</title>
      <meta name="viewport" content="initial-scale=1, width=device-width" />
    </Helmet>
    <ThemeProvider theme={appTheme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
