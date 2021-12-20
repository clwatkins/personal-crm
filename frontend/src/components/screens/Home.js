import React from "react";
import { Container, Grid, Typography } from "@mui/material";

import {
  PersonFormController,
  SummaryTableController,
} from "../fragments/ModalControllers";

function Main() {
  return (
    <div>
      <Container>
        <br />
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <PersonFormController />
          </Grid>
          <Grid item xs={12}>
            <Typography variant="h6">Data summary...</Typography>
            <br />
            <SummaryTableController />
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default Main;
