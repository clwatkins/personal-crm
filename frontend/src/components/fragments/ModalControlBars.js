import React from "react";
import { styled } from "@mui/material/styles";

import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import EventIcon from "@mui/icons-material/Event";

import { TABLE_TYPES } from "./ModalControllers";

const ModalControlButtonsButton = styled(ToggleButton)(() => ({
  "&.Mui-selected": {
    background: "#303f9f",
    color: "white",
  },
}));

const ModalControlButtons = ({
  buttonValues,
  selectedValue,
  setSelectedValue,
}) => {
  const handleChange = (event, newValue) => {
    setSelectedValue(newValue);
  };

  return (
    <ToggleButtonGroup value={selectedValue} exclusive onChange={handleChange}>
      {buttonValues.map((value, v) => (
        <ModalControlButtonsButton key={v} value={value.value}>
          {value.label}
        </ModalControlButtonsButton>
      ))}
    </ToggleButtonGroup>
  );
};

const ModalControlButtonIcons = ({ selectedValue, setSelectedValue }) => {
  const handleChange = (event, newValue) => {
    setSelectedValue(newValue);
  };

  return (
    <ToggleButtonGroup
      size="small"
      value={selectedValue}
      exclusive
      onChange={handleChange}
      aria-label="text alignment"
    >
      <ToggleButton value={TABLE_TYPES.EVENTS} aria-label="events">
        <EventIcon />
      </ToggleButton>
      <ToggleButton value={TABLE_TYPES.PEOPLE} aria-label="people">
        <PersonIcon />
      </ToggleButton>
    </ToggleButtonGroup>
  );
};

export { ModalControlButtons, ModalControlButtonIcons };
