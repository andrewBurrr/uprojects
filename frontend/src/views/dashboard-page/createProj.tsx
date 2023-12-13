import React, { useState } from 'react';
import { Button, Typography, Container, TextField, Radio, RadioGroup, FormControlLabel } from '@mui/material';

interface Project {
  name: string;
  description: string;
  visibility: 'public' | 'private';
}

interface ProjectFormProps {
  onSubmit: (project: Project) => void;
  onClose: () => void; // Callback for closing the form
}

const CreateProj: React.FC<ProjectFormProps> = ({ onSubmit, onClose }) => {
  const [project, setProject] = useState<Project>({ name: '', description: '', visibility: 'public' });

  const handleInputChange = (key: keyof Project) => (event: React.ChangeEvent<HTMLInputElement>) => {
    setProject({ ...project, [key]: event.target.value });
  };

  const handleVisibilityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setProject({ ...project, visibility: event.target.value as 'public' | 'private' });
  };

  const handleSubmit = () => {
    onSubmit(project);
  };

  const handleClose = () => {
    onClose();
  };

  return (
    <Container>
      <Typography variant="h1" align="center" gutterBottom>
        Create a Project
      </Typography>
      <form>
        <TextField
          label="Project Name"
          fullWidth
          margin="normal"
          value={project.name}
          onChange={handleInputChange('name')}
        />
        <TextField
          label="Project Description"
          fullWidth
          multiline
          rows={4}
          margin="normal"
          value={project.description}
          onChange={handleInputChange('description')}
        />
        <RadioGroup
          aria-label="Visibility"
          name="visibility"
          value={project.visibility}
          onChange={handleVisibilityChange}
        >
          <FormControlLabel value="public" control={<Radio />} label="Public" />
          <FormControlLabel value="private" control={<Radio />} label="Private" />
        </RadioGroup>
        <div>
          <Button variant="contained" color="primary" onClick={handleSubmit}>
            Create Project
          </Button>
          <Button variant="outlined" color="secondary" onClick={handleClose} style={{ marginLeft: '10px' }}>
            Close
          </Button>
        </div>
      </form>
    </Container>
  );
};

export {CreateProj};
