import {Avatar, Box, Card, CardContent, Grid, styled, Typography} from "@mui/material";

import { Contact } from "views/about-page/Contact";
// @ts-ignore
import Andrew from "../../assets/andrew.jpg";

const ContactGridItem = styled(Grid) `
  padding: ${props => props.theme.spacing(2)};
`

interface TeamMember {
    avatar: string;
    name: string;
    major: string;
    institution: string;
    skills?: string[];
    github: string;
    email: string;
}

const team: TeamMember[] = [
    {
        avatar: Andrew,
        name: "Andrew Burton",
        major: "Computer Science",
        institution: "University of Calgary",
        skills: ["TypeScript", "Python", "Django", "React", "Docker", "Git"],
        github: "https://github.com/andrewBurrr",
        email: "andrew.burton@ucalgary.ca",
    },
    {
        avatar: Andrew,
        name: "Camden Warburton",
        major: "Computer Science",
        institution: "University of Calgary",
        github: "https://github.com/camy-code",
        email: "camden.warburton@ucalgary.ca",
    },
    {
        avatar: Andrew,
        name: "David Zevin",
        major: "Computer Science",
        institution: "University of Calgary",
        github: "https://github.com/Zevind25",
        email: "david.zevin@ucalgary.ca"
    },
    {
        avatar: Andrew,
        name: "Kyle West",
        major: "Computer Science",
        institution: "University of Calgary",
        github: "https://github.com/Croco-Kyle",
        email: "kyle.west1@ucalgary.ca"
    }
]
const Team = () => {
    return (
        <Grid container>
            {team.map((contact) => (
                <ContactGridItem item xs={12} md={6} lg={3}>
                    <Contact contact={contact}/>
                </ContactGridItem>
            ))}
        </Grid>
    );
}

export { Team };