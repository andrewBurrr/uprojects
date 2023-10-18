import React, { useState } from 'react';
import {Link as RouterLink, useNavigate} from 'react-router-dom';
import { useAuth } from "contexts/AuthContext";
import {
    AppBar, Avatar, Box, Button, Container, Divider, Drawer,
    IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText,
    Menu, MenuItem, Toolbar, Tooltip, Typography,
} from "@mui/material";
import {
    Adb as AdbIcon, Home as HomeIcon, Menu as MenuIcon,
    ImportContacts as AboutIcon, Settings as SettingsIcon,
    Logout as LogoutIcon
} from '@mui/icons-material';


const Header: React.FC = () => {
    const { user, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();
    const [anchorElUser, setAnchorElUser] = useState<null|HTMLElement>(null);
    const [drawerState, setDrawerState] = useState(false);
    const open = Boolean(anchorElUser);

    const pages = [
        { name: "Home", url: "/", icon: <HomeIcon/> },
        { name: "About", url: "/about", icon: <AboutIcon/>},
    ]

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
                <Container maxWidth="xl">
                    <Toolbar disableGutters>
                        <AdbIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
                        <Typography
                            variant="h6"
                            noWrap
                            component={RouterLink}
                            to="/"
                            sx={{
                                mr: 2,
                                display: { xs: 'none', md: 'flex' },
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: 'inherit',
                                textDecoration: 'none',
                            }}
                        >
                            LOGO
                        </Typography>

                        <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
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
                        </Box>
                        <AdbIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
                        <Typography
                            variant="h5"
                            noWrap
                            component={RouterLink}
                            to="/"
                            sx={{
                                mr: 2,
                                display: { xs: 'flex', md: 'none' },
                                flexGrow: 1,
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: 'inherit',
                                textDecoration: 'none',
                            }}
                        >
                            LOGO
                        </Typography>
                        <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                            {pages.map((page) => (
                                <Button
                                    key={page.name}
                                    component={RouterLink}
                                    to={page.url}
                                    sx={{ my: 2, color: 'white', display: 'block' }}
                                >
                                    {page.name}
                                </Button>
                            ))}
                        </Box>

                        { isAuthenticated ?
                            <Box sx={{ flexGrow: 0 }}>
                                <Tooltip title="Open settings">
                                    <IconButton onClick={handleUserMenuClick} sx={{ p: 0 }}>
                                        <Avatar alt={`${user.first_name} ${user.last_name}`} src={user.profile_image} />
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
                                    <MenuItem onClick={handleClose}>
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
                        { pages.map((page, index) => (
                            <ListItem disablePadding key={index}>
                                <ListItemButton component={RouterLink} to={page.url}>
                                    <ListItemIcon>
                                        { page.icon }
                                    </ListItemIcon>
                                    <ListItemText primary={page.name} />
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