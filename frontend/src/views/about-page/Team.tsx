import {Avatar, Box, Button, Card, CardContent, Grid, styled, Typography} from "@mui/material";

import { Contact } from "views/about-page/Contact";
// @ts-ignore
import Andrew from "../../assets/andrew.jpg";
import React from "react";

const ContactGridItem = styled(Grid) `
  padding: ${props => props.theme.spacing(2)};
`

interface TeamMember {
    avatar: string;
    name: string;
    major: string;
    institution: string;
    skills?: string[];
    email: string;
}

const team: TeamMember[] = [
    {
        avatar: Andrew,
        name: "Andrew Burton",
        major: "Computer Science",
        institution: "University of Calgary",
        skills: ["TypeScript", "Python", "Django", "React", "Docker", "Git"],
        email: "andrew.burton@ucalgary.ca",
    },
    {
        avatar: Andrew,
        name: "Camden Warburton",
        major: "Computer Science",
        institution: "University of Calgary",
        email: "camden.warburton@ucalgary.ca",
    },
    {
        avatar: Andrew,
        name: "David Zevin",
        major: "Computer Science",
        institution: "University of Calgary",
        email: "david.zevin@ucalgary.ca"
    },
    {
        avatar: Andrew,
        name: "Kyle West",
        major: "Computer Science",
        institution: "University of Calgary",
        email: "kyle.west1@ucalgary.ca"
    }
]
const Team = () => {
    return (
        <Grid container>
            {team.map((contact) => (
                <ContactGridItem key={contact.name} item xs={12} md={6} lg={3}>
                    <Card style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                        <Contact contact={contact}/>
                        <Button
                            fullWidth
                            variant="contained"
                        >
                            Contact
                        </Button>
                    </Card>
                </ContactGridItem>
            ))}
        </Grid>
    );
}

export { Team };