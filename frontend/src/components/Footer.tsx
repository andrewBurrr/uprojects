import React from 'react';
import Box from "@mui/material/Box";
import {Container, Typography} from "@mui/material";
import Link from "@mui/material/Link";


function Copyright() {
    return (
        <Typography variant="body2" color="text.secondary">
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
                Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

const Footer: React.FC = () => {
    return (
        <Box
            component="footer"
            sx={{
                py: 3,
                px: 2,
                mt: 'auto',
                backgroundColor: (theme) =>
                    theme.palette.mode === 'light'
                        ? theme.palette.grey[200]
                        : theme.palette.grey[800],
            }}
        >
            <Container maxWidth="sm">
                <Typography variant="body1">
                    My sticky footer can be found here.
                </Typography>
                <Copyright />
            </Container>
        </Box>
    );
}

export { Footer };