import React, { ChangeEvent, FormEvent, useState } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import { TabPanel } from "./TabPanel";
import {
    Container,
    Tabs,
    Tab,
    TextField,
    Grid,
    Paper,
    Link as MuiLink,
    Typography,
    Chip,
    Box,
    Button, InputAdornment, IconButton, useMediaQuery, useTheme
} from "@mui/material";
import { Link } from "react-router-dom";
import { useApi } from "../../contexts/ApiContext";

interface Tag {
    tag: string;
}

interface Project {
    id: string;
    name: string;
    visibility: string;
    description: string;
    owner_id: string;
    tags: Tag[];
}

interface Team {
    owner_id: string;
    team_name: string;
    tags: Tag[];
}

interface Event {
    event_id: string;
    organization: string;
    event_type: string;
    start_date: string;
    end_date: string;
    name: string;
    tags: Tag[];
}

interface User {
    id: string;
    profile_image: string; // Assuming the image path is stored as a string
    about: string;
    email: string;
    first_name: string;
    last_name: string;
    start_date: string; // Assuming the date is stored as a string
    owner_id: string;
    tags: Tag[];
}

interface Org {
    org_id: string;
    logo: string;
    name: string;
    description: string;
    user_owner: string;
    owner_id: string;
    tags: Tag[];
}

function a11yProps(index: number) {
    return {
        id: `vertical-tab-${index}`,
        'aria-controls': `vertical-tabpanel-${index}`,
    };
}

const Search = () => {
    const { api } = useApi();
    const theme = useTheme();
    const [value, setValue] = React.useState(0);
    const [searchQuery, setSearchQuery] = useState('');
    const [tag, setTag] = useState('');
    const [tags, setTags] = useState<string[]>([]);
    const [projects, setProjects] = useState<Project[]>();
    const [teams, setTeams] = useState<Team[]>();
    const [events, setEvents] = useState<Event[]>();
    const [users, setUsers] = useState<User[]>();
    const [orgs, setOrgs] = useState<Org[]>();

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    const handleSearchChange = (event: ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
    }

    const handleTagInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setTag(event.target.value);
    };

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (tag.trim() !== '') {
            setTags((prevTags) => [...prevTags, tag]);
            setTag('');
        }
    };

    const handleRemoveTag = (removedTag: string) => {
        setTags((prevTags) => prevTags.filter((tag) => tag !== removedTag));
    }

    const handleSearchSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Query: ", searchQuery);
        try {
            const proj_res = await api.getData<Project[]>('/search-projects/', {
                query: searchQuery,
                tags: tags.join(','),
            });
            setProjects(proj_res);
            const team_res = await api.getData<Team[]>('/search-teams/', {
                query: searchQuery,
                tags: tags.join(','),
            });
            setTeams(team_res);
            const event_res = await api.getData<Event[]>('/search-events/', {
                query: searchQuery,
                tags: tags.join(','),
            });
            setEvents(event_res);
            const user_res = await api.getData<User[]>('/search-users/', {
                query: searchQuery,
                tags: tags.join(','),
            });
            setUsers(user_res);
            const org_res = await api.getData<Org[]>('/search-orgs/', {
                query: searchQuery,
                tags: tags.join(','),
            });
            setOrgs(org_res);
            console.log("Projects: ", proj_res);
            console.log("Teams: ", team_res);
            console.log("Events: ", event_res);
            console.log("Users: ", user_res);
            console.log("Orgs: ", org_res);

        } catch (error) {
            // Handle error, e.g., show an error message to the user
            console.error('Error fetching search results:', error);
        }
    };

    return (
        <Container>
            <Grid container spacing={3}>

                <Grid item xs={12}>
                    <form onSubmit={handleSearchSubmit}>
                        <Box display="flex" alignItems="baseline" justifyContent="flex-start" paddingTop={3}>
                            <TextField
                                variant="outlined"
                                fullWidth
                                value={searchQuery}
                                onChange={handleSearchChange}
                                placeholder="Search"
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton type="submit" component={Button}>
                                                <SearchIcon />
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                }}
                            />
                        </Box>
                    </form>
                </Grid>

                {/* Tag Input */}
                <Grid item xs={12}>
                    <form onSubmit={handleSubmit}>
                        <Box display="flex" alignItems="baseline" justifyContent="flex-start">
                            <TextField
                                variant="outlined"
                                fullWidth
                                value={tag}
                                onChange={handleTagInputChange}
                                placeholder="Enter tag"
                                sx={{ height: '100%' }}
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <Button type="submit" variant="contained" color="primary">
                                                Add Tag
                                            </Button>
                                        </InputAdornment>
                                    ),
                                }}
                            />
                        </Box>
                    </form>
                    {/* Display selected tags as chips */}
                    {tags.map((tag) => (
                        <Chip key={tag} label={tag} sx={{ margin: '4px' }} onDelete={() => handleRemoveTag(tag)} />
                    ))}
                </Grid>

                <Grid item xs={12} lg={3}>
                    <Tabs
                        orientation={useMediaQuery(theme.breakpoints.up('md')) ? 'vertical' : 'horizontal'}
                        variant="scrollable"
                        value={value}
                        onChange={handleChange}
                        aria-label="Vertical tabs example"
                        sx={{ borderRight: 1, borderColor: 'divider' }}
                    >
                        <Tab label="Projects" {...a11yProps(0)} />
                        <Tab label="Teams" {...a11yProps(1)} />
                        <Tab label="Events" {...a11yProps(2)} />
                        <Tab label="Users" {...a11yProps(3)} />
                        <Tab label="Organizations" {...a11yProps(4)} />
                    </Tabs>
                </Grid>


                <Grid item xs={12} lg={9}>
                    {/* Replace with your custom grid component for search results */}
                    <div>
                        {/* <h2>Search Results</h2> */}
                        {/* Projects */}
                        <TabPanel value={value} index={0}>
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
                                                                <Chip key={tag.tag}  label={tag.tag} size="small" sx={{ margin: 0.5 }} />
                                                            ))}
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                                <Grid item>
                                                    <Chip label={project.visibility} />
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </TabPanel>
                        {/* Teams */}
                        <TabPanel value={value} index={1}>
                            <Grid container spacing={3} direction='column'>
                                {teams?.map((team) => (
                                    <Grid item>
                                        <Paper elevation={1} sx={{ p: 2 }}>
                                            <Grid container direction='row' spacing={2} justifyContent='space-between'>
                                                <Grid item>
                                                    <Grid container direction='column' spacing={1}>
                                                        <Grid item>
                                                            <MuiLink variant='h5' component={Link} to='/' underline='none' color='secondary' fontWeight='500'>
                                                                {team.team_name}
                                                            </MuiLink>
                                                        </Grid>
                                                        <Grid item>
                                                            {team.tags.map((tag) => (
                                                                <Chip key={tag.tag} label={tag.tag} size="small" sx={{ margin: 0.5 }} />
                                                            ))}
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </TabPanel>
                        {/* Events */}
                        <TabPanel value={value} index={2}>
                            <Grid container spacing={3} direction='column'>
                                {events?.map((event) => (
                                    <Grid item>
                                        <Paper elevation={1} sx={{ p: 2 }}>
                                            <Grid container direction='row' spacing={2} justifyContent='space-between'>
                                                <Grid item>
                                                    <Grid container direction='column' spacing={1}>
                                                        <Grid item>
                                                            <MuiLink variant='h5' component={Link} to='/' underline='none' color='secondary' fontWeight='500'>
                                                                {event.name}
                                                            </MuiLink>
                                                        </Grid>
                                                        <Grid item>
                                                            {event.tags.map((tag) => (
                                                                <Chip key={tag.tag} label={tag.tag} size="small" sx={{ margin: 0.5 }} />
                                                            ))}
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </TabPanel>
                        {/* Users */}
                        <TabPanel value={value} index={3}>
                            <Grid container spacing={3} direction='column'>
                                {users?.map((user) => (
                                    <Grid item>
                                        <Paper elevation={1} sx={{ p: 2 }}>
                                            <Grid container direction='row' spacing={2} justifyContent='space-between'>
                                                <Grid item>
                                                    <Grid container direction='column' spacing={1}>
                                                        <Grid item>
                                                            <MuiLink variant='h5' component={Link} to='/' underline='none' color='secondary' fontWeight='500'>
                                                                {user.first_name} {user.last_name}
                                                            </MuiLink>
                                                        
                                                        </Grid>
                                                        <Grid item>
                                                            {user.tags.map((tag) => (
                                                                <Chip key={tag.tag} label={tag.tag} size="small" sx={{ margin: 0.5 }} />
                                                            ))}
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </TabPanel>
                        {/* Organizations */}
                        <TabPanel value={value} index={4}>
                            <Grid container spacing={3} direction='column'>
                                {orgs?.map((org) => (
                                    <Grid item>
                                        <Paper elevation={1} sx={{ p: 2 }}>
                                            <Grid container direction='row' spacing={2} justifyContent='space-between'>
                                                <Grid item>
                                                    <Grid container direction='column' spacing={1}>
                                                        <Grid item>
                                                            <MuiLink variant='h5' component={Link} to='/' underline='none' color='secondary' fontWeight='500'>
                                                                {org.name}
                                                            </MuiLink>
                                                            <Typography variant='subtitle2'>
                                                                {org.description}
                                                            </Typography>
                                                        </Grid>
                                                        <Grid item>
                                                            {org.tags.map((tag) => (
                                                                <Chip key={tag.tag} label={tag.tag} size="small" sx={{ margin: 0.5 }} />
                                                            ))}
                                                        </Grid>
                                                    </Grid>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </TabPanel>
                    </div>
                </Grid>
            </Grid>
        </Container>
    );
}

export { Search };