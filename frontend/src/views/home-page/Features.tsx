import React from 'react';
import {Box, styled, lighten, darken, Container, Typography, Grid, SxProps} from "@mui/material";
// @ts-ignore
import Lines from "assets/curvedlines.png";
import {Theme} from "@mui/material/styles";
import {AccountTree, BugReport, Groups2} from "@mui/icons-material";

const item: SxProps<Theme> = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  px: 5,
};

const FeaturesBox = styled(Box) `
  display: flex;
  overflow: hidden;
  background-color: ${props => lighten(props.theme.palette.primary.light, 0)};
`


const Features = () => {
    return (
        <FeaturesBox>
            <Container sx={{ mt: 15, mb: 30, display: 'flex', position: 'relative' }}>
                <Box
                    component="img"
                    src={Lines}
                    sx={{ pointerEvents: 'none', position: 'absolute', top: -180, filter: "brightness(60%)" }}
                />
                <Grid container spacing={5}>
                    <Grid item xs={12} md={4}>
                        <Box sx={item}>
                            <BugReport/>
                            <Typography variant="h6" sx={{ my: 5 }}>
                                Modern Issue Tracking
                            </Typography>
                            <Typography variant="h5">
                                {
                                    'Unleash efficiency with our cutting-edge issue tracking system.'
                                }
                                {
                                    ' Seamlessly identify, prioritize, and resolve tasks, ensuring your team stays ahead of challenges.'
                                }
                            </Typography>
                        </Box>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Box sx={item}>
                            <AccountTree/>
                            <Typography variant="h6" sx={{ my: 5 }}>
                                Project Management
                            </Typography>
                            <Typography variant="h5">
                                {
                                    'Elevate your project game with our intuitive project management tools.'
                                }
                                {
                                    ' From planning to execution, empower your team to collaborate, meet deadlines, and achieve project milestones effortlessly.'
                                }
                            </Typography>
                        </Box>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Box sx={item}>
                            <Groups2/>
                            <Typography variant="h6" sx={{ my: 5 }}>
                                Team Integration
                            </Typography>
                            <Typography variant="h5">
                                {
                                    'Forge a unified force with our powerful team integration capabilities.'
                                }
                                {
                                    ' Foster collaboration, streamline communication, and watch as your team transforms into a synchronized powerhouse driving success.'
                                }
                            </Typography>
                        </Box>
                    </Grid>
                </Grid>
            </Container>
        </FeaturesBox>
    );
}

export { Features };