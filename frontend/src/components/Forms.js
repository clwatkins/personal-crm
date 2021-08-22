import { postEvent, postNote } from "../Api";

import { Button, TextField } from "@material-ui/core";
import CreatableSelect from "react-select/creatable";
import { useState } from "react";

import { PersonSelect } from "./PersonSelect";


const NoteForm = (props) => {
  const [textValue, setTextValue] = useState("");

  const handleFormSubmit = async (e) => {
    postNote(
      props.personId,
      textValue
    );

    setTextValue("");
  };

  return (
    <div>
      <br />
      <TextField
        error={props.personId < 0}
        id="outlined-basic"
        label={'What have you learned?'}
        helperText={(props.personId < 0) ? 'Select a person first' : null }
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
    postEvent(
      eventType,
      selectedPeopleValues.map(({ value }) => value).join(),
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
          isMulti={true}
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
  return BasePersonCommentForm("Who did you meet?", "Where did you meet them?", "add");
};

const PlanForm = () => {
  return BasePersonCommentForm(
    "Who are you planning to meet?",
    "What are you going to do?",
    "plan"
  );
};

const SeeForm = () => {
  return BasePersonCommentForm("Who are you seeing?", "What are you doing?", "see");
};

export { AddForm, PlanForm, SeeForm, NoteForm };
