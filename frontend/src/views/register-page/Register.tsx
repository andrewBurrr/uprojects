import { Link } from "react-router-dom";
function Register(){
    return (<>
    <h1>This is the Register page</h1>
    <Link to="/about">About</Link> 
    <br></br>
    <Link to="/">Home</Link>
    </>);
}

export default Register;