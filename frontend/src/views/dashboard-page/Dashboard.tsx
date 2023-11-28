import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import {
    Avatar,
    Button,
    Paper,
    Typography,
    Box,
    Grid,
    Chip, Link as MuiLink, Dialog, DialogTitle, DialogContent, IconButton, FormControlLabel, Checkbox, DialogActions, TextField, Stack
} from "@mui/material";
import {Link} from "react-router-dom";
import SettingsIcon from '@mui/icons-material/Settings';
import CloseIcon from "@mui/icons-material/Close"

// The following creates an array for the project
function createProjInfo(
    title:string,
    description:string,
    tags:string

    ) {
    return {title, description, tags}
}

function tagToString(a:string[]) {
    if (a.length==0) {
        return ""
    } else if (a.length==1) {
        return a[0]
    } else if (a.length==2){
        return `${a[0]},${a[1]}`
    } else {
        return `${a[0]},${a[1]},${a[2]}`
    }
}

const Dashboard = () => { // This is the start of the function
    // here is where we do the report bug stuff
    const [open,openchange]=useState(false);
    const functionopenpopup=()=>{
        openchange(true);
    }
    const closepopup=()=>{
        openchange(false);
    }
    const [value, setValue] = React.useState(""); // we may not need 'React' here
    // This is the end of the report bug stuff


    const testTable = [
        createProjInfo("Minecraft1", "This is my new world", tagToString(["java","Python","C"])),
        createProjInfo("Minecraft1", "This is my new world", "TAG"),
        createProjInfo("Minecraft1", "This is my new world", "")

    ]

    const projects = [
        {
            name: 'my project',
            visibility: 'public',
            description: 'welcome to my new project',
            tags: ['python', 'java'],
        },
        {
            name: 'awesome app',
            visibility: 'private',
            description: 'building an amazing application',
            tags: ['react', 'node.js', 'mongodb'],
        },
        {
            name: 'coding challenge',
            visibility: 'public',
            description: 'solving coding problems and improving skills',
            tags: ['javascript', 'algorithms', 'data structures'],
        },
        {
            name: 'portfolio website',
            visibility: 'private',
            description: 'creating a personal portfolio to showcase projects',
            tags: ['html', 'css', 'react'],
        },
    ];

    const teams = [
        {name: 'Good Team',},
        {name: 'Dynamic Dream',},
    ];

    const orgs = [
        {name: 'University of Calgary',},
        {name: 'Some Guys'},
    ];

    return (
        <Box>
            <Grid container justifyContent='center' display='flex'>
                <Grid item padding={5} paddingBottom={1} flexGrow={{ md: 0, xs: 1}}>
                    <Grid container spacing={2} direction={{ xs: 'row', md: 'column' }}>
                        <Grid item>
                            <Grid container spacing={2} direction={{ md: 'column', xs: 'row' }} alignItems='center' justifyContent='center'>
                                <Grid item>
                                    <Avatar alt="User Avatar" src="path/to/avatar.jpg"  sx={{ width: 200, height: 200 }} />
                                </Grid>
                                <Grid item>
                                    <Typography variant="h5">John Doe</Typography>
                                    <Typography variant="subtitle1" color="textSecondary">
                                       Frontend Developer
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
                                {teams.map((team) => (
                                    <Grid item>
                                        <Avatar alt={team.name} sx={{ bgcolor: '#'+Math.floor(Math.random() * 0xFFFFFF).toString() }} variant="rounded">
                                            {team.name.split(' ').map((word) => word[0]).join('')}
                                        </Avatar>
                                    </Grid>
                            ))}
                            </Grid>

                            <Typography>
                                Organizations
                            </Typography>
                            <hr/>
                            <Grid container spacing={1}>
                                {orgs.map((org) => (
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
                <Grid item paddingY={5} spacing={2}>
                    <Typography variant="h5">
                        About
                    </Typography>
                    <Typography variant="body1" paragraph>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis lorem ut libero malesuada feugiat.
                    </Typography>
                    <Grid container spacing={3} direction='column'>
                        {projects.map((project) => (
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
    {/*                <TableContainer component={Paper}>*/}
    {/*  <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">*/}
    {/*    <TableHead>*/}
    {/*      <TableRow>*/}
    {/*        <TableCell>Title</TableCell>*/}
    {/*        <TableCell align="center">Desc</TableCell>*/}
    {/*        <TableCell align="center">Tag</TableCell>*/}

    {/*      </TableRow>*/}
    {/*    </TableHead>*/}
    {/*    <TableBody>*/}
    {/*      {testTable.map((row) => (*/}
    {/*        <TableRow*/}
    {/*          key={row.title}*/}
    {/*          sx={{ '&:last-child td, &:last-child th': { border: 0 } }}*/}
    {/*        >*/}
    {/*          <TableCell component="th" scope="row">*/}
    {/*            {row.title}*/}
    {/*          </TableCell>*/}
    {/*          <TableCell align="center">{row.description}</TableCell>*/}
    {/*          <TableCell align="center">{row.tags}</TableCell>*/}
    {/*      */}
    {/*        </TableRow>*/}
    {/*      ))}*/}
    {/*    </TableBody>*/}
    {/*  </Table>*/}
    {/*</TableContainer>*/}


                </Grid>
            </Grid>
            <Grid item   container
                direction="row"
                justifyContent="flex-end"
                alignItems="flex-start">
                    
                    <Button variant="outlined" startIcon={<SettingsIcon />} onClick={functionopenpopup} >
  Report Bug
</Button>

<Dialog 
            // fullScreen 
            open={open} onClose={closepopup} fullWidth maxWidth="sm">
                <DialogTitle>Report Bug <IconButton onClick={closepopup} style={{float:'right'}}><CloseIcon color="primary"></CloseIcon></IconButton>  </DialogTitle>
                <DialogContent>
                    {/* <DialogContentText>Do you want remove this user?</DialogContentText> */}
                    <Stack spacing={2} margin={2}>
                      <TextField variant="outlined" label="Description" fullWidth    multiline
          rows={4} onChange={(event) => setValue(event.target.value)} value={value}></TextField>
               
                   
                      <Button color="primary" variant="contained" onClick={(event) => {setValue("");
                   alert('Thank you, your response was recorded'); closepopup() }} value={""}>Submit</Button>
                    </Stack>
                </DialogContent>
                <DialogActions>
                {/* <Button color="success" variant="contained">Yes</Button>
                    <Button onClick={closepopup} color="error" variant="contained">Close</Button> */}
                </DialogActions>
            </Dialog>
</Grid>
        </Box>
      );
}
// This last part is where we are doing the report bug
export { Dashboard };