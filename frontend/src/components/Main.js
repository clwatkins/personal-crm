import {
  AppBar,
  Container,
  Card,
  CardContent,
  CssBaseline,
  Grid,
  Toolbar,
  Typography
} from "@material-ui/core";
import withStyles from "@material-ui/styles/withStyles";

import FormController from "./FormController";
import { EventsTable, PlansTable } from "./Tables";

const styles = (theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.grey["100"],
    overflow: "hidden",
    backgroundSize: "cover",
    backgroundPosition: "0 400px",
    paddingBottom: 200,
  },
  grid: {
    marginTop: 40,
    [theme.breakpoints.down("sm")]: {
      width: "calc(100% - 20px)",
    },
  },
  paper: {
    padding: theme.spacing(3),
    textAlign: "left",
    color: theme.palette.text.secondary,
  },
  rangeLabel: {
    display: "flex",
    justifyContent: "space-between",
    paddingTop: theme.spacing(2),
  },
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 32,
  },
  outlinedButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1),
  },
  actionButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1),
    width: 152,
  },
  blockCenter: {
    padding: theme.spacing(2),
    textAlign: "center",
  },
  block: {
    padding: theme.spacing(2),
  },
  box: {
    marginBottom: 40,
    height: 65,
  },
  inlining: {
    display: "inline-block",
    marginRight: 10,
  },
  buttonBar: {
    display: "flex",
  },
  alignRight: {
    display: "flex",
    justifyContent: "flex-end",
  },
  noBorder: {
    borderBottomStyle: "hidden",
  },
  loadingState: {
    opacity: 0.05,
  },
  loadingMessage: {
    position: "absolute",
    top: "40%",
    left: "40%",
  },
});

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
          <br />
          <Grid container spacing={3}>
            <Grid item xs={6}>
              <Card variant="outlined">
                <CardContent>
                  {" "}
                  <Typography variant="h6">
                    Who have you seen lately?
                  </Typography>
                  <EventsTable />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6}>
              <Card variant="outlined">
                <CardContent>
                  {" "}
                  <Typography variant="h6">
                    Who do you want to see more of?
                  </Typography>
                  <PlansTable />
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </main>
    </>
  );
}

export default withStyles(styles)(Main);
