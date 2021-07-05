import { postEvent, getPeople } from "../Api";

import { Button, TextField } from "@material-ui/core";
import Select from "react-select";
import CreatableSelect from "react-select/creatable";
import { useState, useEffect } from "react";

const BaseForm = (personPrompt, commentPrompt, eventType) => {
  const [selectValues, setSelectValues] = useState([]);
  const [textValue, setTextValue] = useState("");
  const [peopleList, setPeopleList] = useState([]);

  useEffect(() => {
    const getPeopleFromApi = async () => {
      const peopleResponse = await getPeople(-1);

      setPeopleList(
        peopleResponse.map((person) => ({
          value: person.id,
          label: person.name,
        }))
      );
    };
    getPeopleFromApi();
  }, []);

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
        <Select
          isMulti
          cacheOptions
          options={peopleList}
          value={selectValues}
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
