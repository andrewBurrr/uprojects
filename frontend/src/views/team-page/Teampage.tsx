import React, { useEffect, useState } from "react";
import { useApi } from "contexts/ApiContext";
import {

  Grid,
  Box,
  Typography,
  Avatar,
  
  CardContent,
  Card,
} from "@mui/material";
import { Margin, RampLeft } from "@mui/icons-material";
import StarIcon from '@mui/icons-material/Star';

const leaderName = "Billy"
const leaderImg= "path/to/avatar.jpg"

function createCard(name:string,path:string) {
    return {name,path}
}

const cardInfo = [
    createCard("Sydney Crosby", "path/to/avatar.jpg"),
    createCard("Hendrix", "path/to/avatar.jpg")
    
]

function makeOwnerCard( name:string,picturePath:string) {
    return (
        <Card  sx={{ minWidth: 275,  width:500 }  }>
          <CardContent >
<Grid container direction="column">
    <Grid item container direction="row"> 
        <Grid item><StarIcon ></StarIcon></Grid>
        <Grid item marginLeft={1} marginBottom={1}> <Typography variant="h6">Owner</Typography></Grid>
    </Grid>
            <Grid container item>
                <Grid item>
                <Avatar alt="User Avatar" src={picturePath}  sx={{ width: 50, height: 50 }} />
                </Grid>
                <Grid item marginLeft={3}>
                    <Typography variant="h5">{name}</Typography>
                </Grid>
    
    
            </Grid>
            </Grid>
          </CardContent>
        </Card>
      );
}

function MakeBasicCard(name:string,picturePath:string) {
  return (
    <Card  sx={{ minWidth: 275,  width:500 }  }>
      <CardContent >
        <Grid container>
            <Grid item>
            <Avatar alt="User Avatar" src={picturePath}  sx={{ width: 50, height: 50 }} />
            </Grid>
            <Grid item marginLeft={3}>
                <Typography variant="h5"> {name}</Typography>
            </Grid>


        </Grid>
      </CardContent>
    </Card>
  );
}

const Teampage = () => {
  return (
    <Box>
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        <Grid item marginTop={3} marginBottom={1}>
          
            <Typography variant="h2">
              Team name
              </Typography>
              
           
        
        </Grid>

        <Grid item>
            {makeOwnerCard(leaderName, leaderImg)}
            {MakeBasicCard("cam", "path/to/avatar.jpg")}
            {cardInfo.map(  (det)=> (

            MakeBasicCard(det.name, det.path)

            ) )}
       
        
        </Grid>
      </Grid>
     <Grid container 
     justifyContent="flex-end"
     alignItems="flex-start">
            <Grid item> Okay so we have item now!</Grid>

     </Grid>
    </Box>
  );
};

export { Teampage };
