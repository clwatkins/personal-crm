import { getPersonDetails, updatePersonDetails, createEvent, createNote } from "../Api";

import { Button, Box, TextField } from "@mui/material";
import CreatableSelect from "react-select/creatable";
import React, { useState, useEffect } from "react";

import { PersonSelect } from "./PersonSelect";

const PersonDetailsForm = (props) => {
  const [detailsProps, setDetailsProps] = useState({ name: '', first_met_comment: '' });

  useEffect(() => {
    const getPersonDetailsFromApi = async (personId) => {
      const details = await getPersonDetails(personId);
      setDetailsProps(details);
    };

    if (props.personId > 0) {
      getPersonDetailsFromApi(props.personId);
    }
  }, [props]);

  const handleFormSubmit = async (e) => {
    updatePersonDetails(props.personId, detailsProps);
  };

  return (
    <div>
      <Box
        component="form"
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          variant="standard"
          margin="normal"
          label={"Their name"}
          value={detailsProps.name}
          onChange={(e) => setDetailsProps({ ...detailsProps, name: e.target.value })}
        />
        <TextField
          variant="standard"
          margin="normal"
          label={"How you first met them"}
          value={detailsProps.first_met_comment}
          onChange={(e) => setDetailsProps({ ...detailsProps, first_met_comment: e.target.value })}
        />
        </Box>
        <br />
        <Button variant="contained" color="primary" onClick={handleFormSubmit}>
          Update me!
        </Button>
    </div >
  );
};

const NoteForm = (props) => {
  const [textValue, setTextValue] = useState("");

  const handleFormSubmit = async (e) => {
    createNote(props.personId, textValue);

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

const BasePersonCommentForm = (personPrompt, commentPrompt, eventType) => {
  const [selectedPeopleValues, setSelectedPeopleValues] = useState([]);
  const [textValue, setTextValue] = useState("");

  const handleFormSubmit = async (e) => {
    var mappedPeopleValues;

    if (eventType === 'add') {
      mappedPeopleValues = selectedPeopleValues.map(({ label }) => label);
    }
    else {
      mappedPeopleValues = selectedPeopleValues.map(({ value }) => value);
    }

    createEvent(
      eventType,
      mappedPeopleValues,
      textValue
    );

    setSelectedPeopleValues([]);
    setTextValue("");
  };

  const handleSelectChange = (selectedOption) => {
    setSelectedPeopleValues(selectedOption);
  };

  return (
    <div>
      <br />
      <TextField
        id="outlined-basic"
        label={commentPrompt}
        size="small"
        variant="outlined"
        fullWidth={true}
        onChange={(e) => setTextValue(e.target.value)}
        value={textValue}
      />
      <br />
      <br />
      {eventType === "add" ? (
        <CreatableSelect
          isMulti
          placeholder={personPrompt}
          onChange={handleSelectChange}
        />
      ) : (
        <PersonSelect
          isMulti
          placerholder={personPrompt}
          selectedValues={selectedPeopleValues}
          setSelectedValues={setSelectedPeopleValues}
        />
      )}
      <br />
      <Button variant="contained" color="primary" onClick={handleFormSubmit}>
        Submit
      </Button>
    </div>
  );
};

const AddForm = () => {
  return BasePersonCommentForm(
    "Who did you meet?",
    "Where did you meet them?",
    "add"
  );
};

const PlanForm = () => {
  return BasePersonCommentForm(
    "Who are you planning to meet?",
    "What are you going to do?",
    "plan"
  );
};

const SeeForm = () => {
  return BasePersonCommentForm(
    "Who are you seeing?",
    "What are you doing?",
    "see"
  );
};

export { AddForm, PlanForm, SeeForm, NoteForm, PersonDetailsForm };
