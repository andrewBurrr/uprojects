import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Grid, Box, Typography, Button, Avatar, CardActions, CardContent, Card } from '@mui/material';


function tagToString(a:string[]) {
    if (a.length==0) {
        return ""
    } else if (a.length==1) {
        return a[0]
    } else if (a.length==2){
        return `${a[0]}, ${a[1]}`
    } else {
        return `${a[0]}, ${a[1]}, ${a[2]}`
    }
}

function createSIU(title:string,tags:string,start:string,end:string){
    return {title,tags,start,end}
}

function createTeam(name:string,tags:string) {

    return {name,tags};
}

const teamDetails = [
    createTeam("TeamA",tagToString(["Java", "C"])),
    createTeam("TeamB", tagToString(["Pyhton", "perl"])),
    createTeam("TeamC",tagToString(["Java", "C"]))
    
]       // Andrew here are how I display the data LMK if we need to change

const eventDetails = [
    {title:"Cam",
tags:"Cam,isc,ca",
start:"today",
end:"tommorow"},

    createSIU("David event", "Superhandsome,man", "1969","3000" )
    // createEvent()
]

// The following is my card test
const card = (
    <React.Fragment>
      <CardContent>
      <Grid
  container
  direction="row"
  justifyContent="flex-end"
  alignItems="flex-start"
  spacing={1}> 
    <Grid item xs={9} container  direction="column"
  justifyContent="flex-end"
  alignItems="baseline">
    <Grid item > <Typography variant="h6">Title</Typography></Grid>
    <Grid item > <Typography variant="caption">Tags</Typography></Grid>
  </Grid>

  <Grid item xs={3} container  direction="column"
  justifyContent="flex-end"
  alignItems="baseline">
    <Grid item > <Typography>Start</Typography></Grid>
    <Grid item > <Typography>End</Typography></Grid>
  </Grid>

  </Grid>
       
      </CardContent>
   
    </React.Fragment>
  );
// The following is the end of my card test
const OrgPage = () => {
    const testTableEvents = []

    const testTableTeams = []

    // const [data, setData] = useState({});
    // const { getData } = useApi();
    //
    // useEffect(() => {
    //     const response = getData("/projects/1");
    //     setData(response.data);
    // },[]);
    return (
        <>
            <Box>
            <Box>
            <Grid container>
                <Grid item padding={5} paddingBottom={1} >
                    <Avatar alt="User Avatar" src="path/to/avatar.jpg"  sx={{ width: 200, height: 200 }} />
                    <Typography variant="h5">Camy Cam's organization</Typography>
                    <Typography variant="subtitle1" color="textSecondary">
                       Frontend Developer
                    </Typography>
                    <Button variant="outlined" size="medium">
  Teams
</Button>
<br></br>
<Button variant="outlined" size="medium"  >
  Events
</Button>
                </Grid>
                <Grid item paddingTop={1} width={0.5}>
                    <Typography variant="h5">
                        About
                    </Typography>
                    <Typography variant="body1" paragraph>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quis lorem ut libero malesuada feugiat.
                    </Typography>
                    
                    <Grid container >
                        <Grid   width={0.48} marginRight={1} >
                            <Typography variant="h5" >Events</Typography>
                        <Card variant="outlined">{card}</Card>
                        <Card variant="outlined">{card}</Card>
                        {eventDetails.map(   (det) => (
                            <Card>
                                           <React.Fragment>
                                           <CardContent>
                                           <Grid
                                       container
                                       direction="row"
                                       justifyContent="flex-end"
                                       alignItems="flex-start"
                                       spacing={1}> 
                                         <Grid item xs={9} container  direction="column"
                                       justifyContent="flex-end"
                                       alignItems="baseline">
                                         <Grid item > <Typography variant="h6">{det.title}</Typography></Grid>
                                         <Grid item > <Typography variant="caption">{det.tags}</Typography></Grid>
                                       </Grid>
                                     
                                       <Grid item xs={3} container  direction="column"
                                       justifyContent="flex-end"
                                       alignItems="baseline">
                                         <Grid item > <Typography>{det.start}</Typography></Grid>
                                         <Grid item > <Typography>{det.end}</Typography></Grid>
                                       </Grid>
                                     
                                       </Grid>
                                            
                                           </CardContent>
                                        
                                         </React.Fragment>
                                         </Card>

                        )  )}
                           
                        </Grid>
                        <Grid  width={0.48} paddingBottom={1}>
                            <Typography variant="h5" >Teams</Typography>
                        
                           {teamDetails.map((det)=>(
                             <Card variant="outlined" >
                                    <React.Fragment>
                                    <CardContent>
                                    <Grid
                                container
                                direction="row"
                                justifyContent="flex-end"
                                alignItems="flex-start"
                                > 
                                <Grid item xs={9} textAlign={"left"} >
                                <Typography variant="h5">{det.name}</Typography>
                                </Grid>
                              
                                <Grid item xs={3}>
                                  <Typography variant="overline">{det.tags}</Typography>
                                </Grid>
                              
                                </Grid>  
                                    </CardContent>
                                  </React.Fragment>
                                  </Card> ))}
                            {/* {teamDetails.map((det)=>(
                                <div>{det.name} {det.tags}</div>
                            ))} */}
                          
                        </Grid>
                       
                    </Grid>

                </Grid>
            </Grid>
        </Box>
            </Box>
            
        </>
    );
}

export {OrgPage}