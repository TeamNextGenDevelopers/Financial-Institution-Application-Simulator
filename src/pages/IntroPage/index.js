import * as React from 'react';
import {Link, useLocation, useNavigate} from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import HeaderB from '../../components/header';

import axios from 'axios';





let theme = createTheme({
    
  });
  theme = createTheme(theme, {
    palette: {
      roktoLaal: theme.palette.augmentColor({
        color: {
          main: '#e30909',
        },
        name: 'roktoLaal',
      }),
    },
  });

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <a color="inherit" href="#">
        T Bank Inc.
      </a>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}



function IntroductionPage() {
  const location = useLocation();
  const accountCreated = location.state?.accountCreated || false;
  const navigate = useNavigate();
  

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email');
    const password = data.get('password');

    axios.post('http://localhost:5000/login', { email, password })
      .then(response => {
        console.log(response.data);
        navigate('/dashboard');
      })
      .catch(error => {
        console.error('There was an error!', error);
        // Handle error (e.g., show an error message)
      });
  };
  

  return (
    <ThemeProvider theme={theme}>
      
      <HeaderB />
      <Grid container component="main" sx={{ height: '100vh' }}>
        <CssBaseline />
        <Grid
          item
          xs={false}
          sm={4}
          md={7}
          sx={{
            backgroundImage: 'url(images/background.jpg)',
            backgroundRepeat: 'no-repeat',
            backgroundColor: (t) =>
              t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <Box
            sx={{
              my: 8,
              mx: 4,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 4, bgcolor: 'red' }}>
              <LockOutlinedIcon />
            </Avatar>
            {accountCreated && <p>Account created!</p>}
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            
            <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
              />
              
              <Button
                type="submit"
                color="roktoLaal"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Grid container>
                <Grid item>
                  <Link to='/Signup'>Don't have an account? Signup</Link>
                
                </Grid>
              </Grid>
              <Copyright sx={{ mt: 5 }} />
            </Box>
          </Box>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}


export default IntroductionPage