import React, {useEffect, useState} from "react";
import {useApi} from "contexts/ApiContext";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Grid } from '@mui/material';

const projects = [
  {
    name: 'my project',
    visibility: 'public',
    description: 'welcome to my new project',
    tags: ['python', 'java'],
  },
  {
    name: 'awesome app',
    visibility: 'private',
    description: 'building an amazing application',
    tags: ['react', 'node.js', 'mongodb'],
  },
  {
    name: 'coding challenge',
    visibility: 'public',
    description: 'solving coding problems and improving skills',
    tags: ['javascript', 'algorithms', 'data structures'],
  },
  {
    name: 'portfolio website',
    visibility: 'private',
    description: 'creating a personal portfolio to showcase projects',
    tags: ['html', 'css', 'react'],
  },
  // Add more projects as needed
];


const MyTable = () => {
  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Header 1</TableCell>
            <TableCell>Header 2</TableCell>
            <TableCell>Header 3</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>
              <Grid container direction='column'>
                <Grid item xs={6}>
                  <div>Content 1</div>
                </Grid>
                <Grid item xs={6}>
                  <div>Content 2</div>
                </Grid>
              </Grid>
            </TableCell>
            <TableCell>
              <Grid container>
                <Grid item xs={12}>
                  <div>Content 3</div>
                </Grid>
              </Grid>
            </TableCell>
            <TableCell>
              <Grid container>
                <Grid item xs={4}>
                  <div>Content 4</div>
                </Grid>
                <Grid item xs={4}>
                  <div>Content 5</div>
                </Grid>
                <Grid item xs={4}>
                  <div>Content 6</div>
                </Grid>
              </Grid>
            </TableCell>
          </TableRow>
          {/* Add more rows as needed */}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const Projects = () => {

}

const Project = ({ project }) => {
  return (
      <Grid>

      </Grid>
  );
}


const Dashboard = () => {
    // const [data, setData] = useState({});
    // const { getData } = useApi();
    //
    // useEffect(() => {
    //     const response = getData("/projects/1");
    //     setData(response.data);
    // },[]);
    return (
        <>
            <h1>Hello from dashboard</h1>
            <MyTable />
        </>
    );
}

export { Dashboard };