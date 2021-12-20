import React from "react";
import { styled } from "@mui/material/styles";

import { ToggleButton, ToggleButtonGroup } from "@mui/material";

const FormControlBarButton = styled(ToggleButton)(() => ({
  "&.Mui-selected": {
    background: "#303f9f",
    color: "white",
  },
}));

const FormControlBar = ({
  formBarValues,
  selectedFormBarValue,
  setSelectedFormBarValue,
}) => {
  const handleChangeFormBarValue = (event, newValue) => {
    setSelectedFormBarValue(newValue);
  };

  return (
    <ToggleButtonGroup
      value={selectedFormBarValue}
      exclusive
      onChange={handleChangeFormBarValue}
      aria-label="text alignment"
    >
      {formBarValues.map((formBarValue, v) => (
        <FormControlBarButton key={v} value={formBarValue.value}>
          {formBarValue.label}
        </FormControlBarButton>
      ))}
    </ToggleButtonGroup>
  );
};

export default FormControlBar;
