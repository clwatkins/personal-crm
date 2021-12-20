import React from "react";
import { Container, Grid } from "@mui/material";

import FormController from "../fragments/FormController";
import { PersonsSummaryTable } from "../fragments/Tables";

function Main() {
  return (
    <div>
      <Container>
        <br />
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <FormController />
          </Grid>
          <Grid item xs={12}>
            <PersonsSummaryTable />
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default Main;
