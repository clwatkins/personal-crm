import { makeStyles } from "@material-ui/core/styles";

import ToggleButton from "@material-ui/lab/ToggleButton";
import ToggleButtonGroup from "@material-ui/lab/ToggleButtonGroup";

const FormControlBar = ({ formBarValue, setFormBarValue }) => {
  const useStyles = makeStyles({
    buttonColor: {
      "&.Mui-selected": {
        background: "#303f9f",
        color: "white",
      },
    },
  });

  const customColorClass = useStyles();

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
      <ToggleButton value="see" className={customColorClass.buttonColor}>
        Seeing
      </ToggleButton>
      <ToggleButton value="add" className={customColorClass.buttonColor}>
        Adding
      </ToggleButton>
      <ToggleButton value="plan" className={customColorClass.buttonColor}>
        Planning
      </ToggleButton>
    </ToggleButtonGroup>
  );
};

export default FormControlBar;
