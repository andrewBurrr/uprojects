import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";

const Dashboard = () => {
    // const [data, setData] = useState({});
    // const { getData } = useApi();
    //
    // useEffect(() => {
    //     const response = getData("/projects/1");
    //     setData(response.data);
    // },[]);
    return (
        <h1>Hello from dashboard</h1>
    );
}

export { Dashboard };