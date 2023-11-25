import { Stack } from "@mui/material";
import { Welcome } from "views/home-page/Welcome";
import { Connect } from "views/home-page/Connect";
import { Features } from "views/home-page/Features";
import { Testimonials } from "views/home-page/Testimonials";

const Home = () => {
    return (
        <>
            <Welcome />
            <Features />
            <Testimonials />
        </>
    );
}

export { Home };