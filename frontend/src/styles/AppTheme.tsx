import {createTheme, responsiveFontSizes} from "@mui/material";

export interface AppTheme {
    bg: {
        main: string,
        light: string,
    },
    text: {
        main: string,
        light: string,
    }
}

let theme = createTheme({
    bg: {
        main: '#fff',
        light: '#F4F5F7',
    },
    text: {
        main: '#172B4D',
        light: '#262930',
    },
    palette: {
        mode: "light",
        primary: {
            main: '#000000',
        },
        secondary: {
            main: '#f50057',
        }
    },
    shape: {
        borderRadius: 0,
    },
    typography: {},
});

theme = responsiveFontSizes(theme);

export { theme };