import { Link } from "react-router-dom";
function About(){
    return (
    <div>
    <h1>This is the about page</h1>
    <Link to="/">Home</Link> 
    <br></br>
    <Link to="/register">Register</Link>
    </div>
    );
}

export default About;