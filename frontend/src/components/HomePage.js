import React from 'react';
import { Grid, Button, Typography, Paper, Box, Container, Link } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import BusinessIcon from '@mui/icons-material/Business';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import EmailIcon from '@mui/icons-material/Email';

const HomePage = ({ onModeSelect }) => {
  return (
    <Container>
      <Box sx={{ textAlign: 'center', mb: 8 }}>
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          gap: 2,
          mb: 3
        }}>
          <Typography 
            variant="h2" 
            component="h1" 
            sx={{
              fontFamily: 'Montserrat, Arial, sans-serif', // Updated font
              fontSize: { xs: '2.5rem', md: '3.5rem' },
              fontWeight: 800,
              background: 'linear-gradient(45deg, #B17457 30%, #4A4947 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '0.03em',
              textShadow: '4px 4px 8px rgba(177, 116, 87, 0.2)',
              position: 'relative',
              padding: '0.5rem 0',
              '&::after': {
                content: '""',
                position: 'absolute',
                bottom: 0,
                left: '50%',
                transform: 'translateX(-50%)',
                width: '80%',
                height: '3px',
                background: 'linear-gradient(90deg, transparent, #B17457, transparent)',
              }
            }}
          >
            Intelligent ATS
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={4} sx={{ mt: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ 
            p: 4, 
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
          }}>
            <PersonIcon sx={{ 
              fontSize: 80, 
              color: '#B17457',
              mb: 3,
              filter: 'drop-shadow(0 4px 12px rgba(177, 116, 87, 0.3))',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'scale(1.1)',
                color: '#4A4947',
              }
            }} />
            <Typography 
              variant="h4" 
              gutterBottom
              sx={{
                fontFamily: 'Montserrat, Arial, sans-serif', // Updated font
                fontWeight: 700,
                color: '#4A4947',
                letterSpacing: '0.02em',
                marginBottom: 2
              }}
            >
              For Individuals
            </Typography>
            <Typography 
              sx={{ 
                mb: 4,
                minHeight: '48px',
                opacity: 0.9,
                color: '#4A4947',
                fontFamily: 'Montserrat, Arial, sans-serif', // Updated font
                fontSize: '1.1rem',
                fontWeight: 500,
                letterSpacing: '0.01em'
              }}
            >
              Analyze your resume against a specific job description
            </Typography>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={() => onModeSelect('individual')}
              sx={{ mt: 'auto' }}
            >
              Start Analysis
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ 
            p: 4, 
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
          }}>
            <BusinessIcon sx={{ 
              fontSize: 80, 
              color: '#B17457',
              mb: 3,
              filter: 'drop-shadow(0 4px 12px rgba(177, 116, 87, 0.3))',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'scale(1.1)',
                color: '#4A4947',
              }
            }} />
            <Typography 
              variant="h4" 
              gutterBottom
              sx={{
                fontFamily: 'Montserrat, Arial, sans-serif', // Updated font
                fontWeight: 700,
                color: '#4A4947',
                letterSpacing: '0.02em',
                marginBottom: 2
              }}
            >
              For Recruiters
            </Typography>
            <Typography 
              sx={{ 
                mb: 4,
                minHeight: '48px',
                opacity: 0.9,
                color: '#4A4947',
                fontFamily: 'Poppins, sans-serif',
                fontSize: '1.1rem',
                fontWeight: 500,
                letterSpacing: '0.01em'
              }}
            >
              Analyze multiple resumes in bulk
            </Typography>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={() => onModeSelect('recruiter')}
              sx={{ mt: 'auto' }}
            >
              Bulk Analysis
            </Button>
          </Paper>
        </Grid>
      </Grid>
      
      <Box 
        sx={{ 
          textAlign: 'center',
          mt: 8,
          pt: 4,
          borderTop: '1px solid rgba(177, 116, 87, 0.2)',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, alignItems: 'center' }}>
          <Link href="mailto:rishigupta_official@hotmail.com" sx={{ color: '#B17457', '&:hover': { color: '#4A4947' } }}>
            <EmailIcon />
          </Link>
          <Link href="https://github.com/Rishi-gupta-data" target="_blank" sx={{ color: '#B17457', '&:hover': { color: '#4A4947' } }}>
            <GitHubIcon />
          </Link>
          <Link href="https://www.linkedin.com/in/rishi-datascience/" target="_blank" sx={{ color: '#B17457', '&:hover': { color: '#4A4947' } }}>
            <LinkedInIcon />
          </Link>
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;