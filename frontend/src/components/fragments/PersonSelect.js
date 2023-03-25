import Select from "react-select";
import { useSelector } from "react-redux";
import React, { useState, useEffect, useMemo } from "react";

import DataService from "../../services/data";

const PersonSelect = (props) => {
  const [peopleList, setPeopleList] = useState([]);
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
