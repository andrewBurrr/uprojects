import React, { useState, ChangeEvent } from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from "contexts/AuthContext";
import { FormGridContainer } from "components/forms/FormGridContainer";
import { FormGrid } from "components/forms/FormGrid";
import { FormTextField } from "components/forms/FormTextField";
import { FormButton } from "components/forms/FormButton";
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { Avatar, Box, Grid, Link, Paper, Typography } from '@mui/material';


const initForm = {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: ''
}

const Register = () => {
    const { register } = useAuth();
    const navigate = useNavigate();
    const [formData, setFormData] = useState(initForm);
    const [errors, setErrors] = useState(initForm);

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        setErrors({ ...errors, [name]: '' });
    }

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setErrors({
            first_name: formData.first_name !== '' ? '' : 'First name is a required field',
            last_name: formData.last_name !== '' ? '' : 'Last name is a required field',
            email: formData.email !== '' ? '' : 'Email is a required field',
            password: formData.password !== '' ? '' : 'Password is a required field',
            confirm_password: formData.password === formData.confirm_password ? '' : 'Passwords do not match'
        });

        if (Object.values(errors).every((error) => error === '')) {
            try {
                await register(formData.email, formData.first_name, formData.last_name, formData.password);
                navigate("/login");
            } catch (error) {
                console.log("Oh no!");
            }
        }
    };

    return (
        <FormGridContainer container>
            <FormGrid item xs={12} sm={8} md={5} component={Paper} square variant="outlined">
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign up
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 3 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <FormTextField
                                fullWidth
                                id="first_name"
                                label="First Name"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleInputChange}
                                error={Boolean(errors.first_name)}
                                helperText={errors.first_name}
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormTextField
                                fullWidth
                                id="last_name"
                                label="Last Name"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleInputChange}
                                error={Boolean(errors.last_name)}
                                helperText={errors.last_name}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormTextField
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                error={Boolean(errors.email)}
                                helperText={errors.email}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormTextField
                                fullWidth
                                id="password"
                                label="Password"
                                name="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                error={Boolean(errors.password)}
                                helperText={errors.password}
                                type="password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormTextField
                                fullWidth
                                id="confirm_password"
                                label="Confirm Password"
                                name="confirm_password"
                                value={formData.confirm_password}
                                onChange={handleInputChange}
                                error={Boolean(errors.confirm_password)}
                                helperText={errors.confirm_password}
                                type="password"
                            />
                        </Grid>
                    </Grid>
                    <FormButton
                        type="submit"
                        fullWidth
                        variant="contained"
                    >
                        Sign Up
                    </FormButton>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href="#" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </FormGrid>
        </FormGridContainer>
    );
}

export { Register };