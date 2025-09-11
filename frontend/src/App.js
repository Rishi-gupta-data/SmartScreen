import React, { useState } from 'react';
import {
    ThemeProvider,
    CssBaseline,
    Container,
    AppBar,
    Toolbar,
    Typography,
    Box,
} from '@mui/material';
import theme from './theme';
import HomePage from './components/HomePage';
import IndividualAnalysis from './components/IndividualAnalysis';
import BulkAnalysis from './components/BulkAnalysis';
import ResumeAnalysis from './components/ResumeAnalysis';

function App() {
    const [mode, setMode] = useState(null);
    const [analysis, setAnalysis] = useState(null);

    const renderContent = () => {
        if (analysis) {
            return <ResumeAnalysis analysis={analysis} onBack={() => setAnalysis(null)} />;
        }

        switch (mode) {
            case 'individual':
                return <IndividualAnalysis onBack={() => setMode(null)} setAnalysis={setAnalysis} />;
            case 'recruiter':
                return <BulkAnalysis onBack={() => setMode(null)} />;
            default:
                return <HomePage onModeSelect={setMode} />;
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="static" sx={{ backgroundColor: '#1a237e' }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        SmartScreen ATS
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Box sx={{ mt: 4 }}>
                    {renderContent()}
                </Box>
            </Container>
        </ThemeProvider>
    );
}

export default App;
