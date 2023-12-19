import React, {useEffect, useState} from 'react';
import {Link as RouterLink, useNavigate} from 'react-router-dom';
import { useAuth } from "contexts/AuthContext";
import {
    AppBar, Avatar, Box, Button, Container, Divider, Drawer,
    IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText,
    Menu, MenuItem, styled, Toolbar, Tooltip, Typography,
} from "@mui/material";
import {
    Menu as MenuIcon,
    Settings as SettingsIcon,
    Logout as LogoutIcon
} from '@mui/icons-material';
import {authOnlyRoutes, publicRoutes, unauthOnlyRoutes} from "../../helpers/RouteConfig";


const LogoTypography = styled(Typography) `
  padding: ${props => props.theme.spacing(1)};
  font-family: Garamond, serif;
  color: inherit;
  text-transform: uppercase;
  text-decoration: none;
` as typeof Typography;

const SmallBox = styled (Box) `
  align-items: center;
  justify-content: space-between;
  flex-grow: 1;
  display: flex;
  
  ${props => props.theme.breakpoints.up('md')} {
    display: none;
  }
`

const MediumBox = styled(Box) `
  align-items: center;
  justify-content: space-between;
  flex-grow: 1;
  display: none;
  
  ${props => props.theme.breakpoints.up('md')} {
    display: flex;
  }
`

const LinkContainer = styled('div') `
  display: flex;
  align-items: center;
`

const Header: React.FC = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const [anchorElUser, setAnchorElUser] = useState<null|HTMLElement>(null);
    const [drawerState, setDrawerState] = useState(false);
    const open = Boolean(anchorElUser);

    const links = [
        ...(isAuthenticated ? authOnlyRoutes : unauthOnlyRoutes),
        ...publicRoutes
    ]

    useEffect(() => {
        console.log(links);
    }, [links]);

    const handleUserMenuClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    }

    const handleClose = () => {
        setAnchorElUser(null);
    }

    const handleLogout = async () => {
        await logout();
        navigate("/");
    }

    const handleDrawerToggle = () => {
        setDrawerState(!drawerState);
    };

    return (
        <React.Fragment>
            <AppBar position="static" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                <Container maxWidth={false}>
                    <Toolbar disableGutters>
                        { /* Menu for small displays */ }
                        <SmallBox>
                            <IconButton
                                size="large"
                                aria-label="account of current user"
                                aria-controls="menu-appbar"
                                aria-haspopup="true"
                                onClick={handleDrawerToggle}
                                color="inherit"
                            >
                                <MenuIcon />
                            </IconButton>
                            <LogoTypography
                                variant="h6"
                                noWrap
                                component={RouterLink}
                                to="/"
                            >
                                uprojects
                            </LogoTypography>
                            { /* auth menu */ }
                            { isAuthenticated ?
                            <Box sx={{ flexGrow: 0 }}>
                                <Tooltip title="Open settings">
                                    <IconButton onClick={handleUserMenuClick} sx={{ p: 0 }}>
                                        <Avatar alt={`${user?.first_name} ${user?.last_name}`} src={user?.profile_image} />
                                    </IconButton>
                                </Tooltip>
                                <Menu
                                    anchorEl={anchorElUser}
                                    id="account-menu"
                                    open={open}
                                    onClose={handleClose}
                                    onClick={handleClose}
                                    PaperProps={{
                                        elevation: 0,
                                        sx: {
                                            overflow: 'visible',
                                            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                                            mt: 1.5,
                                            '& .MuiAvatar-root': {
                                                width: 32,
                                                height: 32,
                                                ml: -0.5,
                                                mr: 1,
                                            },
                                            '&:before': {
                                                content: '""',
                                                display: 'block',
                                                position: 'absolute',
                                                top: 0,
                                                right: 14,
                                                width: 10,
                                                height: 10,
                                                bgcolor: 'background.paper',
                                                transform: 'translateY(-50%) rotate(45deg)',
                                                zIndex: 0,
                                            },
                                        },
                                    }}
                                    transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                                    anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                                >
                                    <MenuItem onClick={() => navigate(`/user/${user?.user_id}`)}>
                                        <Avatar /> Profile
                                    </MenuItem>
                                    <Divider />
                                    <MenuItem onClick={handleClose}>
                                        <SettingsIcon fontSize="small"/> Settings
                                    </MenuItem>
                                    <MenuItem onClick={handleLogout}>
                                        <LogoutIcon fontSize="small" /> Logout
                                    </MenuItem>
                                </Menu>
                            </Box>
                            :
                            <Button sx={{ color: "white" }} component={RouterLink} to="/login">Login</Button>
                        }
                        </SmallBox>
                        { /* Menu for medium displays and up */ }
                        <MediumBox>
                            <LinkContainer>
                                <LogoTypography
                                    variant="h6"
                                    noWrap
                                    component={RouterLink}
                                    to="/"
                                >
                                    uprojects
                                </LogoTypography>
                                {links.filter((link) => link.icon).map((link) => (
                                    <Button
                                        key={link.title}
                                        component={RouterLink}
                                        to={link.path}
                                        sx={{ my: 1, color: 'white', display: 'block' }}
                                    >
                                        {link.title}
                                    </Button>
                                ))}
                            </LinkContainer>
                            {isAuthenticated ?
                                <Box sx={{ flexGrow: 0 }}>
                                    <Tooltip title="Open settings">
                                        <IconButton onClick={handleUserMenuClick} sx={{ p: 0 }}>
                                            <Avatar alt={`${user?.first_name} ${user?.last_name}`} src={user?.profile_image} />
                                        </IconButton>
                                    </Tooltip>
                                    <Menu
                                        anchorEl={anchorElUser}
                                        id="account-menu"
                                        open={open}
                                        onClose={handleClose}
                                        onClick={handleClose}
                                        PaperProps={{
                                            elevation: 0,
                                            sx: {
                                                overflow: 'visible',
                                                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                                                mt: 1.5,
                                                '& .MuiAvatar-root': {
                                                    width: 32,
                                                    height: 32,
                                                    ml: -0.5,
                                                    mr: 1,
                                                },
                                                '&:before': {
                                                    content: '""',
                                                    display: 'block',
                                                    position: 'absolute',
                                                    top: 0,
                                                    right: 14,
                                                    width: 10,
                                                    height: 10,
                                                    bgcolor: 'background.paper',
                                                    transform: 'translateY(-50%) rotate(45deg)',
                                                    zIndex: 0,
                                                },
                                            },
                                        }}
                                        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                                        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                                    >
                                        <MenuItem onClick={() => navigate(`/user/${user?.user_id}`)}>
                                            <Avatar /> Profile
                                        </MenuItem>
                                        <Divider />
                                        <MenuItem onClick={handleClose}>
                                            <SettingsIcon fontSize="small"/> Settings
                                        </MenuItem>
                                        <MenuItem onClick={handleLogout}>
                                            <LogoutIcon fontSize="small" /> Logout
                                        </MenuItem>
                                    </Menu>
                                </Box>
                                :
                                <Button sx={{ color: "white" }} component={RouterLink} to="/login">Login</Button>
                            }
                        </MediumBox>
                    </Toolbar>
                </Container>
            </AppBar>
            <Drawer
                variant="temporary"
                anchor="top"
                open={drawerState}
            >
                <Box onClick={handleDrawerToggle}>
                    <Toolbar />
                    <List>
                        { links.filter((link) => link.icon).map((link, index) => (
                            <ListItem disablePadding key={index}>
                                <ListItemButton component={RouterLink} to={link.path}>
                                    <ListItemIcon>
                                        { link.icon }
                                    </ListItemIcon>
                                    <ListItemText primary={link.title} />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Box>
            </Drawer>
        </React.Fragment>
    );
}

export { Header }
