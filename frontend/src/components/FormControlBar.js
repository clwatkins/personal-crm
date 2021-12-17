import React from "react";
import { styled } from "@mui/material/styles";

import {ToggleButton, ToggleButtonGroup} from "@mui/material";

const FormControlBarButton = styled(ToggleButton)(() => ({
  "&.Mui-selected": {
    background: "#303f9f",
    color: "white",
  }
}));

const FormControlBar = ({ formBarValue, setFormBarValue }) => {

  const handleChangeFormBarValue = (event, newValue) => {
    setFormBarValue(newValue);
  };

  return (
    <ToggleButtonGroup
      value={formBarValue}
      exclusive
      onChange={handleChangeFormBarValue}
      aria-label="text alignment"
    >
      <FormControlBarButton value="see">
        Seeing
      </FormControlBarButton>
      <FormControlBarButton value="add">
        Adding
      </FormControlBarButton>
      <FormControlBarButton value="plan">
        Planning
      </FormControlBarButton>
    </ToggleButtonGroup>
  );
};

export default FormControlBar;
