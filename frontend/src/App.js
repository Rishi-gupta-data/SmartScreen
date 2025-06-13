import React, { useState } from 'react';
import { ThemeProvider, CssBaseline, Container } from '@mui/material';
import theme from './theme';
import HomePage from './components/HomePage';
import IndividualAnalysis from './components/IndividualAnalysis';
import BulkAnalysis from './components/BulkAnalysis';
import ResumeAnalysis from './components/ResumeAnalysis'; // <-- Add this line

function App() {
  const [mode, setMode] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  const renderContent = () => {
    if (analysis) {
      // Show analysis results if available
      return <ResumeAnalysis analysis={analysis} onBack={() => setAnalysis(null)} />;
    }
    switch (mode) {
      case 'individual':
        // Pass setAnalysis to IndividualAnalysis so it can update analysis state
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
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {renderContent()}
      </Container>
    </ThemeProvider>
  );
}

export default App;
