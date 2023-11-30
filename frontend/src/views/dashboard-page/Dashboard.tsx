import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import {
    Avatar,
    Button,
    Paper,
    Typography,
    Box,
    Grid,
    Chip, Link as MuiLink
} from "@mui/material";
import {Link, useParams} from "react-router-dom";

interface User {
    id: string;
    profile_image: string; // Assuming the image path is stored as a string
    about: string;
    email: string;
    first_name: string;
    last_name: string;
    start_date: string; // Assuming the date is stored as a string
    is_staff: boolean;
    is_active: boolean;
    owner_id?: string;
    tags?: string[];
}

interface Project {
    id: string;
    name: string;
    visibility: string;
    description: string;
    owner_id: string;
    tags: string[];
}

interface Team {
    owner_id: string;
    team_name: string;
    tags: string[];
}

interface Org {
    org_id: string;
    logo: string;
    name: string;
    description: string;
    user_owner: string;
    owner_id: string;
    tags: string[];
}

const Dashboard = () => { // This is the start of the function
    const { user_id } = useParams<{ user_id: string }>();
    const { api } = useApi();
    const [user, setUser] = useState<User>();
    const [projects, setProjects] = useState<Project[]>();
    const [teams, setTeams] = useState<Team[]>();
    const [orgs, setOrgs] = useState<Org[]>();

    const fetchUser = async () => {
        try {
            // Fetch the user
            const response = await api.getData<User>(`/user/${user_id}`);
            console.log("user:", response);
            setUser(response);
        } catch (error) {
            console.error('Error fetching user data: ', error);
        }
    };

    const fetchUserProjects = async () => {
        try {
            const response = await api.getData<Project[]>(`/user-projects/${user?.owner_id}`);
            console.log("user:", response);
            setProjects(response);
        } catch (error) {
            console.error('Error fetching user projects: ', error);
        }
    }

    const fetchUserTeams = async () => {
        try {
            console.log("user = ", user);
            const response = await api.getData<Team[]>(`/user-teams/${user?.id}`);
            console.log("user:", response);
            setTeams(response);
        } catch (error) {
            console.error('Error fetching user teams: ', error);
        }
    }

    const fetchUserOrgs = async () => {
            try {
                const response = await api.getData<Org[]>(`/user-orgs/${user?.owner_id}`);
                console.log("user:", response);
                setOrgs(response);
            } catch (error) {
                console.error('Error fetching user orgs: ', error);
            }
        }

    useEffect(() => {
        // Fetch the user
        fetchUser();
        // Fetch the users projects
        fetchUserProjects();
        // Fetch the user's teams
        fetchUserTeams();
        // Fetch the user's orgs
        fetchUserOrgs();

    }, []);

    return (
        <Box>
            <Grid container justifyContent='center' display='flex'>
                <Grid item padding={5} paddingBottom={1} flexGrow={{ md: 0, xs: 1}}>
                    <Grid container spacing={2} direction={{ xs: 'row', md: 'column' }}>
                        <Grid item>
                            <Grid container spacing={2} direction={{ md: 'column', xs: 'row' }} alignItems='center' justifyContent='center'>
                                <Grid item>
                                    <Avatar alt={user?.first_name + ' ' + user?.last_name} src={user?.profile_image} sx={{ width: 200, height: 200 }} />
                                </Grid>
                                <Grid item>
                                    <Typography variant="h5">{user?.first_name} {user?.last_name}</Typography>
                                    <Typography variant="subtitle1" color="textSecondary">
                                        Developer
                                    </Typography>
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Typography>
                                Teams
                            </Typography>
                            <hr/>
                            <Grid container spacing={1}>
                                {teams?.map((team) => (
                                    <Grid item>
                                        <Avatar alt={team.team_name} sx={{ bgcolor: '#'+Math.floor(Math.random() * 0xFFFFFF).toString() }} variant="rounded">
                                            {team.team_name.split(' ').map((word) => word[0]).join('')}
                                        </Avatar>
                                    </Grid>
                            ))}
                            </Grid>

                            <Typography>
                                Organizations
                            </Typography>
                            <hr/>
                            <Grid container spacing={1}>
                                {orgs?.map((org) => (
                                    <Grid item>
                                        <Avatar alt={org.name} sx={{ bgcolor: '#'+Math.floor(Math.random() * 0xFFFFFF).toString() }} variant="rounded">
                                            {org.name.split(' ').map((word) => word[0]).join('')}
                                        </Avatar>
                                    </Grid>
                            ))}
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item paddingY={5}>
                    <Typography variant="h5">
                        About
                    </Typography>
                    <Typography variant="body1" paragraph>
                        {user?.about}
                    </Typography>
                    <Grid container spacing={3} direction='column'>
                        {projects?.map((project) => (
                            <Grid item>
                                <Paper elevation={1} sx={{ p: 2 }}>
                                    <Grid container direction='row' spacing={2} justifyContent='space-between'>
                                        <Grid item>
                                            <Grid container direction='column' spacing={1}>
                                                <Grid item>
                                                    <MuiLink variant='h5' component={Link} to='/' underline='none' color='secondary' fontWeight='500'>
                                                        {project.name}
                                                    </MuiLink>
                                                    <Typography variant='subtitle2'>
                                                        {project.description}
                                                    </Typography>
                                                </Grid>
                                                <Grid item>
                                                    {project.tags.map((tag) => (
                                                        <Chip label={tag} size="small" sx={{ margin: 0.5 }}/>
                                                    ))}
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                        <Grid item>
                                            <Chip label={project.visibility}/>
                                        </Grid>
                                    </Grid>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>
            </Grid>
        </Box>
      );
}

export { Dashboard };