import { Team } from "views/about-page/Team";
import {Typography} from "@mui/material";
import React from "react";

const About = () => {
    return (
    <div>
        <Typography color="inherit" align="center" variant="h2">
            Our Team
        </Typography>
        <hr/>
        <Team/>
    </div>
    );
}

export { About };