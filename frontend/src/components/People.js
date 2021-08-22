import {
  Container,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@material-ui/core";

import { useState } from "react";

import { PersonSelect } from "./PersonSelect";

const People = () => {
  const [selectedPeopleValues, setSelectedPeopleValues] = useState([]);

  return (
    <>
      <br />
      <Container>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <Typography variant="h6">Who are you thinking about?</Typography>
            <br />
            <PersonSelect
              isMulti={false}
              placerholder="Name"
              selectedValues={selectedPeopleValues}
              setSelectedValues={setSelectedPeopleValues}
            />
            <br />
          </Grid>

          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6">Make a note...</Typography>
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
    </>
  );
};

export default People;
