import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import { Avatar, Button, Container, Paper, Typography, Box, Grid, TableContainer, Table, TableCell, TableRow, TableBody, TableHead} from "@mui/material";

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
    
    
    const testTable = [
        createProjInfo("Minecraft1", "This is my new world", tagToString(["java","Python","C"])),
        createProjInfo("Minecraft1", "This is my new world", "TAG"),
        createProjInfo("Minecraft1", "This is my new world", "")

    ]

    return (
        <Box>
            <Grid container>
                <Grid item padding={5} paddingBottom={1} >
                    <Avatar alt="User Avatar" src="path/to/avatar.jpg"  sx={{ width: 120, height: 120 }} />
                    <Typography variant="h5">John Doe</Typography>
                    <Typography variant="subtitle1" color="textSecondary">
                       Frontend Developer
                    </Typography>
                    <Button variant="outlined" size="medium">
  Team
</Button>
<br></br>
<Button variant="outlined" size="medium"  >
  Orgs
</Button>
                </Grid>
                <Grid item paddingTop={1}>
                    <Typography variant="h5">
                        About
                    </Typography>
                    <Typography variant="body1" paragraph>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis lorem ut libero malesuada feugiat.
                    </Typography>
                    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell align="center">Desc</TableCell>
            <TableCell align="center">Tag</TableCell>

          </TableRow>
        </TableHead>
        <TableBody>
          {testTable.map((row) => (
            <TableRow
              key={row.title}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.title}
              </TableCell>
              <TableCell align="center">{row.description}</TableCell>
              <TableCell align="center">{row.tags}</TableCell>
          
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>


                </Grid>
            </Grid>
        </Box>
        // <Container component="main"  maxWidth="lg" >
        //   <Paper elevation={3} >
        //     <Avatar alt="User Avatar" src="path/to/avatar.jpg" />
        //     <Typography variant="h5">John Doe</Typography>
        //     <Typography variant="subtitle1" color="textSecondary">
        //       Frontend Developer
        //     </Typography>
        //     <Typography variant="body1" paragraph>
        //       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis lorem ut libero malesuada feugiat.
        //     </Typography>
        //     <Button variant="contained" color="primary">
        //       Edit Profile
        //     </Button>
        //   </Paper>
        // </Container>
      );
}

export { Dashboard };