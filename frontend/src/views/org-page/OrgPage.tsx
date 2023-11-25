import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Grid, Box, Typography, Button, Avatar } from '@mui/material';

const OrgPage = () => {
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
                    <Avatar alt="User Avatar" src="path/to/avatar.jpg"  sx={{ width: 120, height: 120 }} />
                    <Typography variant="h5">Camy Cam's organization</Typography>
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
                    


                </Grid>
            </Grid>
        </Box>
            </Box>
            
        </>
    );
}

export {OrgPage}