import React, {ReactNode} from 'react';
import { Header } from 'components/Header';
import { Footer } from 'components/Footer';
import { theme } from 'styles/AppTheme';
import { CssBaseline, ThemeProvider } from "@mui/material";
import Box from "@mui/material/Box";

interface LayoutProps {
    children: ReactNode;
}
const AppLayout: React.FC<LayoutProps> = ({ children }) => {

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                minHeight: '100vh'
            }}
        >
            <CssBaseline/>
            <ThemeProvider theme={theme}>
                <Header/>
                { children }
                <Footer />
            </ThemeProvider>

        </Box>
    );
}

export { AppLayout };

