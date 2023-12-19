import { Welcome } from "views/home-page/Welcome";
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
