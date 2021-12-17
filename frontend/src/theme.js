import { createTheme } from '@mui/material/styles';
import { blue, indigo } from "@mui/material/colors";

const appTheme = createTheme({
  palette: {
    secondary: {
      main: blue[900],
    },
    primary: {
      main: indigo[700],
    },
  }
});

export default appTheme;
