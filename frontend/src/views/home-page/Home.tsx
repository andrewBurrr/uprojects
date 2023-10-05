import { Link } from "react-router-dom";

function Home(){
    return (<>
    <h1>This is the Home page</h1>
    <Link to="about">About</Link>
    <br></br>
    <Link to="register">Register</Link>
    </>);
}

export default Home;