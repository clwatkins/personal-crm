import React, { useState, useEffect } from "react";

import { Button, TextField } from "@mui/material";
import CreatableSelect from "react-select/creatable";
import { getPeople, createEvent } from "../../Api";

const CreatablePersonSelect = (personPrompt, commentPrompt, eventType) => {
  const [selectedPeopleList, setSelectedPeopleList] = useState([]);
  const [peopleList, setPeopleList] = useState([]);
  const [textValue, setTextValue] = useState("");

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
    setSelectedPeopleList(selectedOption);
  };

  const handleFormSubmit = async (e) => {
    var existingPeopleValues = selectedPeopleList.filter(
      (person) => !("__isNew__" in person)
    );
    var newPeopleValues = selectedPeopleList.filter(
      (person) => "__isNew__" in person
    );

    existingPeopleValues = existingPeopleValues.map(({ value }) => value);
    newPeopleValues = newPeopleValues.map(({ label }) => label);

    if (existingPeopleValues.length > 0) {
      createEvent(eventType, existingPeopleValues, textValue);
    }
    if (newPeopleValues.length > 0) {
      createEvent("add", newPeopleValues, textValue);
    }
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
      <CreatableSelect
        isMulti
        placeholder={personPrompt}
        onChange={handleSelectChange}
        options={peopleList}
      />
      <br />
      <Button variant="contained" color="primary" onClick={handleFormSubmit}>
        Submit
      </Button>
    </div>
  );
};

export { CreatablePersonSelect };
