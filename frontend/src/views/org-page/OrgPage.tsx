import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Grid } from '@mui/material';

const OrgPage = () => {
    // const [data, setData] = useState({});
    // const { getData } = useApi();
    //
    // useEffect(() => {
    //     const response = getData("/projects/1");
    //     setData(response.data);
    // },[]);
    return (
        <>
            <h1>Hello from org page</h1>
            
        </>
    );
}

export {OrgPage}