import {
  Button,
  Grid,
  Box,
  TextField,
  Rating,
  Typography,
} from "@mui/material";
import FlagIcon from "@mui/icons-material/Flag";
import FlagOutlinedIcon from "@mui/icons-material/FlagOutlined";
import React, { useState, useEffect, useMemo } from "react";
import { useSelector } from "react-redux";

import { CreatablePersonSelect } from "./CreatablePersonSelect";
import DataService from "../../services/data";

export const EVENT_TYPES = {
  PLAN: "plan",
  SEE: "see"
}

const PersonDetailsForm = (props) => {
  const [detailsProps, setDetailsProps] = useState({
    name: "",
    first_met_comment: "",
    priority: 2,
  });
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPersonDetailsFromApi = async (personId) => {
      const details = await dataService.getPersonDetails(personId).catch(err => { console.log(err) });
      if (details) {
        setDetailsProps(details);
      }
    };

    if (props.personId > 0) {
      getPersonDetailsFromApi(props.personId);
    }
  }, [dataService, props]);

  const handleFormSubmit = async (e) => {
    dataService.updatePersonDetails(props.personId, detailsProps);
  };

  return (
    <div>
      <Grid container spacing={3}>
        <Grid item xs={4}>
          <TextField
            variant="standard"
            margin="normal"
            label={"Their name"}
            fullWidth={true}
            value={detailsProps.name}
            onChange={(e) =>
              setDetailsProps({ ...detailsProps, name: e.target.value })
            }
          />
        </Grid>
        <Grid item xs={4}>
          <TextField
            variant="standard"
            margin="normal"
            label={"How you first met them"}
            fullWidth={true}
            value={detailsProps.first_met_comment}
            onChange={(e) =>
              setDetailsProps({
                ...detailsProps,
                first_met_comment: e.target.value,
              })
            }
          />
        </Grid>
        <Grid item xs={4}>
          <Box
            sx={{
              "& > legend": { mt: 2 },
            }}
          >
            <Typography component="legend">Their priority</Typography>
            <Rating
              value={detailsProps.priority}
              max={3}
              icon={<FlagIcon fontSize="inherit" />}
              emptyIcon={<FlagOutlinedIcon fontSize="inherit" />}
              onChange={(e, newValue) =>
                setDetailsProps({
                  ...detailsProps,
                  priority: newValue,
                })
              }
            />
          </Box>
        </Grid>
      </Grid>
      <br />
      <Button variant="contained" color="primary" onClick={handleFormSubmit}>
        Update me!
      </Button>
    </div>
  );
};

const NoteForm = (props) => {
  const [textValue, setTextValue] = useState("");
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  const handleFormSubmit = async (e) => {
    dataService.createNote(props.personId, textValue);

    setTextValue("");
  };

  return (
    <div>
      <br />
      <TextField
        error={props.personId < 0}
        id="outlined-basic"
        label={"What have you learned?"}
        helperText={props.personId < 0 ? "Select a person first" : null}
        multiline
        rows={2}
        variant="outlined"
        fullWidth={true}
        onChange={(e) => setTextValue(e.target.value)}
        value={textValue}
      />
      <br />
      <br />
      <Button variant="contained" color="primary" onClick={handleFormSubmit}>
        Remember that!
      </Button>
    </div>
  );
};

const PlanForm = () => {
  return CreatablePersonSelect(
    "Who are you planning to meet?",
    "What are you going to do?",
    EVENT_TYPES.PLAN
  );
};

const SeeForm = () => {
  return CreatablePersonSelect(
    "Who are you seeing?",
    "What are you doing?",
    EVENT_TYPES.SEE
  );
};

export { PlanForm, SeeForm, NoteForm, PersonDetailsForm };
