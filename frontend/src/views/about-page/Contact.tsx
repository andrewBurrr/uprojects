import {Avatar, Chip, Grid, Typography} from "@mui/material";
import React from "react";

interface TeamMember {
    avatar: string;
    name: string;
    major: string;
    institution: string;
    skills?: string[];
    email: string;
}

interface ContactProps {
    contact: TeamMember;
}

const Contact: React.FC<ContactProps> = ({ contact }) => {

    return (
        <Grid container direction="column" alignItems="center" justifyContent="center" sx={{ flexGrow: 1 }}>
            <Grid item>
                <Grid container alignItems="center" justifyContent="center">
                    <Grid item sx={{p: 3}}>
                        <Avatar alt={contact.name} src={contact.avatar} sx={{width: 100, height: 100}}/>
                    </Grid>
                    <Grid item>
                        <Typography variant="subtitle1" fontWeight="bold" align="center">
                            {contact.name}
                        </Typography>
                        <Typography variant="subtitle2" align="center" color="textSecondary">
                            {contact.major}, {contact.institution}
                        </Typography>
                    </Grid>
                </Grid>
            </Grid>
            { contact.skills ?
                <Grid item sx={{p: 1}}>
                    {contact.skills.map((skill) => (
                        <Chip label={skill} key={skill} size="small" sx={{ margin: 0.5 }}/>
                    ))}
                </Grid>
                : null
            }
        </Grid>
    );
}

export { Contact };
