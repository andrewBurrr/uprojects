import React, { useEffect, useState } from "react";
import { useApi } from "contexts/ApiContext";
import {

  Grid,
  Box,
  Typography,
  Avatar,
  
  CardContent,
  Card,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  TextField,
  Checkbox,
  FormControlLabel,
  DialogActions,
  Stack,
} from "@mui/material";
import { Margin, RampLeft } from "@mui/icons-material";
import StarIcon from '@mui/icons-material/Star';
import CloseIcon from "@mui/icons-material/Close"

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

            <Grid item
  container
  direction="row"
  justifyContent="flex-end"
  alignItems="flex-end"
> 
<Grid item> <Button>Remove</Button></Grid>
</Grid>

        </Grid>
      </CardContent>
    </Card>
  );
}

const Teampage = () => {
// This is the start of the callbacks
  const [open,openchange]=useState(false);
  const functionopenpopup=()=>{
      openchange(true);
  }
  const closepopup=()=>{
      openchange(false);
  }
  // This is the end of the callbacks
  
  const [value, setValue] = React.useState(""); // we may not need 'React' here
  // Other callbacks

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
     <Grid   container
  direction="row"
  justifyContent="center"
  alignItems="flex-end">
            <Grid item marginRight={5}> <Typography variant="h4">Add member</Typography></Grid>
            <Grid item> 
              <Button variant="contained" href="#contained-buttons" onClick={functionopenpopup}>
                Add
              </Button>
              <Dialog 
            // fullScreen 
            open={open} onClose={closepopup} fullWidth maxWidth="sm">
                <DialogTitle>Add member  <IconButton onClick={closepopup} style={{float:'right'}}><CloseIcon color="primary"></CloseIcon></IconButton>  </DialogTitle>
                <DialogContent>
                    {/* <DialogContentText>Do you want remove this user?</DialogContentText> */}
                    <Stack spacing={2} margin={2}>
                      <TextField variant="outlined" label="email" onChange={(event) => setValue(event.target.value)} value={value}></TextField>
                    
                      <Button color="primary" variant="contained" onClick={(event) => setValue("")} value={""} >Submit</Button> 
                      {/* We need to add a method here that submits this to the DB, I will need some help with this*/}
                    </Stack>
                </DialogContent>
                <DialogActions>
                {/* <Button color="success" variant="contained">Yes</Button>
                    <Button onClick={closepopup} color="error" variant="contained">Close</Button> */}
                </DialogActions>
            </Dialog>
              </Grid>
     </Grid>
    </Box>
  );
};

export { Teampage };
