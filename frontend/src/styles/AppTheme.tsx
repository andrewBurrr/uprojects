import { createTheme } from "@mui/material";

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

const theme = createTheme({
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
    },
    shape: {
        borderRadius: 0,
    },
    typography: {},
});

export { theme };