import {
  Container,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import React, { useState } from "react";

import { PersonSelect } from "./PersonSelect";
import { NotesTable } from "./Tables";
import { NoteForm } from "./Forms";

const People = () => {
  const [selectedPersonValue, setSelectedPersonValue] = useState({ value: -1 });

  return (
    <div>
      <br />
      <Container>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Typography variant="h6">Who are you thinking about?</Typography>
            <br />
            <PersonSelect
              isMulti={false}
              placerholder="Contact name"
              selectedValues={selectedPersonValue}
              setSelectedValues={setSelectedPersonValue}
            />
            <br />
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Make a note...</Typography>
                <NoteForm personId={selectedPersonValue.value} />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">See notes...</Typography>
                <NotesTable personId={selectedPersonValue.value} />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Change some details...</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};

export default People;
