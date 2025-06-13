import React, { useState } from 'react';
import axios from 'axios';
import ResumeAnalysis from './ResumeAnalysis';
import { Button, TextField, Box, Typography, CircularProgress } from '@mui/material';

function IndividualAnalysis({ onBack }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');
    setAnalysis(null);

    // MOCK: Simulate backend response
    setTimeout(() => {
      setAnalysis({
        "Match Percentage": "65%",
        "Found Keywords": ["Python", "SQL", "Power BI"],
        "Missing Keywords": ["R", "TensorFlow"],
        "Key Strengths": ["Strong Python and SQL skills."],
        "Areas for Improvement": ["Add experience with cloud platforms."],
        "Resume Formatting & Optimization Tips": ["Use a consistent font."]
      });
      setLoading(false);
    }, 1500);

    // --- Comment out the real backend call below while testing frontend ---
    // const formData = new FormData();
    // formData.append('resume', resumeFile);
    // formData.append('job_description', jobDescription);

    // try {
    //   const response = await axios.post('http://localhost:5000/api/analyze', formData, {
    //     headers: { 'Content-Type': 'multipart/form-data' },
    //   });
    //   setAnalysis(response.data);
    // } catch (err) {
    //   setError(err.response?.data?.error || 'Error analyzing resume');
    // } finally {
    //   setLoading(false);
    // }
  };

  return (
    <Box sx={{ fontFamily: 'Montserrat, Arial, sans-serif' }}>
      <Button
        onClick={onBack}
        variant="outlined"
        size="large"
        sx={{
          mb: 2,
          fontFamily: 'Montserrat, Arial, sans-serif',
          fontWeight: 600,
          fontSize: '1.1rem',
          px: 4,
          py: 1.5,
          borderRadius: 2,
        }}
      >
        Back
      </Button>
      <Typography variant="h5" gutterBottom sx={{ fontFamily: 'Montserrat, Arial, sans-serif' }}>
        Individual Resume Analysis
      </Typography>
      <label htmlFor="resume-upload">
        <input
          id="resume-upload"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <Button
          component="span"
          variant="contained"
          color="secondary"
          size="large"
          sx={{
            mb: 2,
            fontFamily: 'Montserrat, Arial, sans-serif',
            fontWeight: 600,
            fontSize: '1.1rem',
            px: 4,
            py: 1.5,
            borderRadius: 2,
          }}
        >
          Choose File
        </Button>
        {resumeFile && (
          <Typography variant="body2" sx={{ ml: 2, display: 'inline', fontFamily: 'Montserrat, Arial, sans-serif' }}>
            {resumeFile.name}
          </Typography>
        )}
      </label>
      <TextField
        label="Job Description"
        multiline
        rows={4}
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        fullWidth
        margin="normal"
        sx={{ fontFamily: 'Montserrat, Arial, sans-serif' }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleAnalyze}
        disabled={!resumeFile || !jobDescription || loading}
        size="large"
        sx={{
          fontFamily: 'Montserrat, Arial, sans-serif',
          fontWeight: 600,
          fontSize: '1.1rem',
          px: 4,
          py: 1.5,
          borderRadius: 2,
          mt: 2,
        }}
      >
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </Button>
      {loading && (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            mt: 4,
            mb: 2,
          }}
        >
          <CircularProgress size={48} thickness={5} sx={{ color: '#B17457', mb: 2 }} />
          <Typography
            sx={{
              fontFamily: 'Montserrat, Arial, sans-serif',
              fontWeight: 700,
              fontSize: '1.2rem',
              color: '#B17457',
              letterSpacing: '0.05em',
            }}
          >
            Analyzing your resume, please wait...
          </Typography>
        </Box>
      )}
      {error && <Typography color="error" sx={{ fontFamily: 'Montserrat, Arial, sans-serif' }}>{error}</Typography>}
      {analysis && <ResumeAnalysis analysis={analysis} />}
    </Box>
  );
}

export default IndividualAnalysis;