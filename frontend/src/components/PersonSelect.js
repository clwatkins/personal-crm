import Select from "react-select";
import React, { useState, useEffect } from "react";

import { getPeople } from "../Api";

const PersonSelect = (props) => {
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
    props.setSelectedValues(selectedOption);
  };

  return (
    <Select
      isMulti={props.isMulti}
      cacheOptions
      options={peopleList}
      value={props.selectedValues}
      placeholder={props.placeholder}
      onChange={handleSelectChange}
    />
  );
};

export { PersonSelect };
