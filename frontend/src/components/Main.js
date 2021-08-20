import {
  AppBar,
  Container,
  CssBaseline,
  Toolbar,
  Typography,
} from "@material-ui/core";
import withStyles from "@material-ui/styles/withStyles";

import FormController from "./FormController";
import Styles from "../styles";

function Main() {
  return (
    <>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h3">Welcome back...</Typography>
        </Toolbar>
      </AppBar>
      <main>
        <Container>
          <br />
          <br />
          <FormController />
        </Container>
      </main>
    </>
  );
}

export default withStyles(Styles)(Main);
