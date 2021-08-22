import { createTheme } from '@material-ui/core/styles';
import { blue, indigo } from "@material-ui/core/colors";

const appTheme = createTheme({
  palette: {
    secondary: {
      main: blue[900],
    },
    primary: {
      main: indigo[700],
    },
  },
  typography: {
    // Use the system font instead of the default Roboto font.
    fontFamily: ['"Lato"', "sans-serif"].join(","),
  },
});

export default appTheme;
