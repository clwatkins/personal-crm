import { postEvent } from "../Api";

import { Button, TextField } from "@material-ui/core";
import CreatableSelect from "react-select/creatable";
import { useState } from "react";

import { PersonSelect } from "./PersonSelect";

const BaseForm = (personPrompt, commentPrompt, eventType) => {
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
  return BaseForm("Who did you meet?", "Where did you meet them?", "add");
};

const PlanForm = () => {
  return BaseForm(
    "Who are you planning to meet?",
    "What are you going to do?",
    "plan"
  );
};

const SeeForm = () => {
  return BaseForm("Who are you seeing?", "What are you doing?", "see");
};

export { AddForm, PlanForm, SeeForm };
