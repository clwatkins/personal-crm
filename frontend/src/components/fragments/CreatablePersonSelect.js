import React, { useState, useEffect, useMemo } from "react";
import { useSelector } from "react-redux";
import { Button, TextField } from "@mui/material";
import CreatableSelect from "react-select/creatable";

import { EVENT_TYPES } from "./Forms";
import DataService from "../../services/data";

const CreatablePersonSelect = (personPrompt, commentPrompt, eventType) => {
  const [selectedPeopleList, setSelectedPeopleList] = useState([]);
  const [peopleList, setPeopleList] = useState([]);
  const [textValue, setTextValue] = useState("");
  const authToken = useSelector(state => state.auth.token);

  let dataService = useMemo(() => new DataService(authToken), [authToken]);

  useEffect(() => {
    const getPeopleFromApi = async () => {
      const peopleResponse = await dataService.getPeople(-1);

      if (peopleResponse) {
        setPeopleList(
          peopleResponse.map((person) => ({
            value: person.id,
            label: person.name,
          }))
        );
      }
    };
    getPeopleFromApi();
  }, [dataService]);

  const handleSelectChange = (selectedOption) => {
    setSelectedPeopleList(selectedOption);
  };

  const handleFormSubmit = async (e) => {
    // Extract new vs existing people from selected list
    // Existing people have IDs selected
    var existingSelectedPeopleIds = selectedPeopleList
      .filter((person) => !("__isNew__" in person))
      .map(({ value }) => value);

    // New people names
    var newSelectedPeopleLabels = selectedPeopleList
      .filter((person) => "__isNew__" in person)
      .map(({ label }) => label);

    // If there are new people, add them to the database
    var newPeople = [];
    if (newSelectedPeopleLabels.length > 0) {
      newPeople = await dataService.createPeople(newSelectedPeopleLabels, textValue);
    }

    if (newPeople) {
      console.log(newPeople);

      // This returns the new people objects -- merge their ids to the existing
      // list of selected ids
      var combinedPeopleIds = [
        ...existingSelectedPeopleIds,
        ...newPeople.map(({ id }) => id),
      ];
      console.log(combinedPeopleIds);

      // Submit to create one joint event with all people
      if (eventType === EVENT_TYPES.SEE) {
        dataService.createMeeting(combinedPeopleIds, textValue);
      } else if (eventType === EVENT_TYPES.PLAN) {
        dataService.createPlan(combinedPeopleIds, textValue);
      }

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
