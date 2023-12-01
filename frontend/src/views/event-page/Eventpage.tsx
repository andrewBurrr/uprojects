// EventPage.js
import React, { useState } from 'react';
import { Button, TextField, Container, Typography, Grid, Paper, MenuItem } from '@mui/material';

const Eventpage = () => {
  const [tags, setTags] = useState('');
  const [eventType, setEventType] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleFileUpload = (e: { target: { files: any; }; }) => {
    // Handle file upload logic here
    const files = e.target.files;
    console.log(files);
  };

  const handleSubmit = () => {
    // Handle form submission logic here
    console.log('Form submitted!');
  };

  return (
    <Container component="main" maxWidth="md">
      <Paper elevation={3} style={{ padding: 20, marginTop: 20 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Create Event
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Event Tags"
                fullWidth
                value={tags}
                onChange={(e) => setTags(e.target.value)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                select
                label="Event Type"
                fullWidth
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
              >
                <MenuItem value="conference">Conference</MenuItem>
                <MenuItem value="workshop">Workshop</MenuItem>
                <MenuItem value="meetup">Meetup</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Start Date"
                type="datetime-local"
                fullWidth
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="End Date"
                type="datetime-local"
                fullWidth
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <input type="file" onChange={handleFileUpload} multiple />
            </Grid>
          </Grid>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Create Event
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export {Eventpage};
