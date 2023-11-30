import { Team } from "views/about-page/Team";
import {Typography} from "@mui/material";
import React from "react";

const About = () => {
    return (
    <div>
        <Typography color="inherit" align="center" variant="h2">
            Meet The Team
        </Typography>
        <hr/>
        <Team/>
        <Typography color="inherit" align="center" variant="h2" style={{ marginTop: 20 }}>
            Why We Do What We Do
        </Typography>
        <hr/>
        <Typography color="inherit" variant="h6" p={4}>
            {
                'At UPROJECTS, we seek to empower students on their journey to becoming proficient software engineers.'
            }
            {
                ' We are dedicated to providing an innovative project management and version control tool tailored specifically for educational environments.'
            }
            {
                ' By fostering collaboration, enhancing learning experiences, and demystifying the complexities of software engineering tools, we strive to be the catalyst that propels students into the world of successful, impactful software development.'
            }
            <br/><br/>
            {
                ' Through the use of standardized software development practices we aim to revolutionize the educational landscape by equipping students with the tools and knowledge essential for modern workflows.'
            }
            {
                ' We aspire to create a dynamic platform where students can seamlessly explore, collaborate, and iterate on software projects.'
            }
            {
                ' By instilling a passion for efficient project management and version control, we envision a future where every student emerges from their educational journey well-prepared and confident in navigating the dynamic world of software development.'
            }
            {
                ' Together, we\'re building a foundation for the next generation of innovators and problem solvers.'
            }
        </Typography>

    </div>
    );
}

export { About };