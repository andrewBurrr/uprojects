import 'styled-components';
import { Theme } from '@mui/material/styles';
import { AppTheme } from "styles/AppTheme";

declare module '@mui/material/styles' {
    interface Theme extends AppTheme {}

    interface ThemeOptions extends AppTheme {}
}

declare module 'styled-components' {
    export interface DefaultTheme extends Theme {}
}