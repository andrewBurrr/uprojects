import {Avatar, Button, Card, Chip, Grid, Typography} from "@mui/material";
// @ts-ignore
import Andrew from "assets/andrew.jpg";
import {GitHub} from "@mui/icons-material";
import React from "react";

interface TeamMember {
    avatar: string;
    name: string;
    major: string;
    institution: string;
    skills?: string[];
    github: string;
    email: string;
}

interface ContactProps {
    contact: TeamMember;
}

const Contact: React.FC<ContactProps> = ({ contact }) => {

    return (
        <Card>
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
                            <Chip label={skill} size="small"/>
                        ))}
                    </Grid>
                    : null
                }

            </Grid>
            <Button
                fullWidth
                variant="contained"
            >
                Contact
            </Button>
        </Card>
    );
}

export { Contact };