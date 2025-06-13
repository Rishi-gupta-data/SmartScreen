import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#B17457',
      light: '#D8D2C2',
      dark: '#4A4947',
    },
    secondary: {
      main: '#D8D2C2',
      light: '#FAF7F0',
      dark: '#B17457',
    },
    background: {
      default: '#FAF7F0',
      paper: '#FAF7F0',
    },
    text: {
      primary: '#4A4947',
      secondary: '#B17457',
    },
  },
  typography: {
    h3: {
      fontWeight: 600,
      letterSpacing: '0.02em',
      color: '#4A4947',
      textShadow: '2px 2px 4px rgba(74, 73, 71, 0.1)',
    },
    h4: {
      color: '#B17457',
      fontWeight: 500,
    },
    h6: {
      color: '#4A4947',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#FAF7F0',
          border: '1px solid rgba(177, 116, 87, 0.1)',
          boxShadow: '0 8px 32px rgba(74, 73, 71, 0.08)',
          transition: 'transform 0.2s, box-shadow 0.2s',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 12px 40px rgba(74, 73, 71, 0.12)',
            borderColor: 'rgba(177, 116, 87, 0.2)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          padding: '12px 24px',
          fontWeight: 500,
          letterSpacing: '0.05em',
          transition: 'all 0.3s ease',
          '&.MuiButton-contained': {
            backgroundColor: '#B17457',
            color: '#FAF7F0',
            '&:hover': {
              backgroundColor: '#4A4947',
              transform: 'scale(1.03)',
              boxShadow: '0 6px 20px rgba(74, 73, 71, 0.2)',
            },
          },
        },
      },
    },
  },
});

export default theme;