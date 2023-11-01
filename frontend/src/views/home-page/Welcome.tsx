import React from 'react';
import {Box, Button, Container, styled, Typography} from "@mui/material";
// @ts-ignore
import Image from "assets/welcome.png";
import {Link} from "react-router-dom";
import {KeyboardArrowDown} from "@mui/icons-material";

const WelcomeRoot = styled('section') `
  color: ${props => props.theme.palette.common.white};
  position: relative;
  display: flex;
  align-items: center;
  ${props => props.theme.breakpoints.up('sm')} {
    height: 80vh;
  }
`

const Background = styled(Box) `
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-size: cover;
  background-repeat: no-repeat;
  z-index: -2;
`

const Welcome = () => {
    return (
        <WelcomeRoot>
            <Container
                sx={{
                    mt: 3,
                    mb: 14,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                }}
            >
                <img
                    style={{ display: 'none' }}
                    src={Image}
                    alt="increase priority"
                />
                <Typography color="inherit" align="center" variant="h2" style={{ textTransform: 'uppercase' }}>
                    Upgrade your projects
                </Typography>
                <Typography
                    color="inherit"
                    align="center"
                    variant="h5"
                    sx={{ mb: 4, mt: { xs: 4, sm: 10 }}}
                >
                    Increase your development skills by up to 70% with the best community of student developers.
                </Typography>
                <Button
                    color="secondary"
                    variant="contained"
                    size="large"
                    component={Link}
                    to="/register"
                    sx={{ minWidth: 200 }}
                >
                    Register
                </Button>
                <Typography variant="body2" color="inherit" sx={{ mt: 2 }}>
                    Discover your potential
                </Typography>
                <Box
                    sx={{
                        position: 'absolute',
                        left: 0,
                        right: 0,
                        top: 0,
                        bottom: 0,
                        backgroundColor: 'common.black',
                        opacity: 0.5,
                        zIndex: -1,
                    }}
                />
                <Background sx={{ backgroundImage: `url(${Image})`}} />
                {/*<Box*/}
                {/*    component="img"*/}
                {/*    src="/static/themes/onepirate/productHeroArrowDown.png"*/}
                {/*    height="16"*/}
                {/*    width="12"*/}
                {/*    alt="arrow down"*/}
                {/*    sx={{ position: 'absolute', bottom: 32 }}*/}
                {/*/>*/}
                <KeyboardArrowDown sx={{ fontSize: 40, position: 'absolute', bottom: 32 }} />
            </Container>
        </WelcomeRoot>
    );
}

export { Welcome };