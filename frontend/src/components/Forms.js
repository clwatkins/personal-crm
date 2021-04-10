import { postEvent, getPeople } from "../Api";

import { Button, TextField } from "@material-ui/core";
import AsyncSelect from "react-select/async";
import CreatableSelect from "react-select/creatable";
import { useState } from "react";

const promiseOptions = async () => {
  const people = await getPeople(-1);

  const selectOptions = people.map((person) => ({
    value: person.id,
    label: person.name,
  }));
  return selectOptions;
};

const BaseForm = (personPrompt, commentPrompt, eventType) => {
  const [selectValues, setSelectValues] = useState([]);
  const [textValue, setTextValue] = useState("");

  const handleSelectChange = (selectedOption) => {
    setSelectValues(selectedOption);
  };

  const handleFormSubmit = async (e) => {
    postEvent(
      eventType,
      selectValues.map(({ value }) => value).join(),
      textValue
    );

    setSelectValues([]);
    setTextValue("");
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
        <AsyncSelect
          isMulti
          cacheOptions
          defaultOptions
          value={selectValues}
          loadOptions={promiseOptions}
          placeholder={personPrompt}
          onChange={handleSelectChange}
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
