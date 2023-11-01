import React from 'react';
import { Link } from "react-router-dom";
import { GitHub, LinkedIn, Twitter, YouTube } from "@mui/icons-material";
import { authOnlyRoutes, publicRoutes, unauthOnlyRoutes } from "helpers/RouteConfig";
import { useAuth } from "contexts/AuthContext";
import { FooterBox } from "./FooterBox";
import { TitleTypography } from "./TitleTypography";
import { TitleBox } from "./TitleBox";
import { LinkBox } from "./LinkBox";
import { FooterLink } from "./FooterLink";
import { SocialBox } from "./SocialBox";
import { Copyright } from "./Copyright";


const Footer: React.FC = () => {
    const { isAuthenticated } = useAuth();
    const links = [
        ...(isAuthenticated ? authOnlyRoutes : unauthOnlyRoutes),
        ...publicRoutes,
    ];
    const socials = [
        { path: "#", icon: <LinkedIn sx={{ fontSize: 'h2.fontSize' }}/> },
        { path: "#", icon: <GitHub sx={{ fontSize: 'h2.fontSize' }} /> },
        { path: "#", icon: <YouTube sx={{ fontSize: 'h2.fontSize' }} /> },
        { path: "#", icon: <Twitter sx={{ fontSize: 'h2.fontSize' }} /> }
    ];
    return (
        <FooterBox component="footer">
            <TitleBox>
                <TitleTypography variant="h4" align="center">
                    UPROJECTS
                </TitleTypography>
                <TitleTypography variant="h5" align="center">
                    Sophisticated Project Management
                </TitleTypography>
            </TitleBox>
            <LinkBox>
                {links.filter((link) => link.icon).map((link, index) => (
                    <FooterLink
                        key={index}
                        component={Link}
                        to={link.path}
                        underline="none"
                        color='inherit'
                    >
                        {link.title}
                    </FooterLink>
                ))}
            </LinkBox>
            <SocialBox>
                {socials.map((social, index) => (
                    <FooterLink
                        key={index}
                        href={social.path}
                        underline="none"
                        color='inherit'
                    >
                        {social.icon}
                    </FooterLink>
                ))}
            </SocialBox>
            <Copyright />
        </FooterBox>
    );
}

export { Footer };