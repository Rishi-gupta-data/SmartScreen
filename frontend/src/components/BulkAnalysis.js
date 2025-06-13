import React, { useState } from 'react';
import { Box, Button, Typography, TextField, Container, CircularProgress } from '@mui/material'; // <-- Add CircularProgress
import HomeIcon from '@mui/icons-material/Home';
import { analyzeBulkResumes } from '../services/api';

const BulkAnalysis = ({ onBack }) => {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    // MOCK: Simulate backend response for frontend testing
    setTimeout(() => {
      setResults([
        {
          name: "Resume1.pdf",
          "Match Percentage": "80%",
          "Suitability": "Suitable", // Added
          "Found Keywords": ["Python", "SQL", "Power BI"],
          "Missing Keywords": ["R", "TensorFlow"],
          "Key Strengths": ["Strong Python and SQL skills."],
          "Areas for Improvement": ["Add experience with cloud platforms."],
          "Resume Formatting & Optimization Tips": ["Use a consistent font."]
        },
        {
          name: "Resume2.pdf",
          "Match Percentage": "60%",
          "Suitability": "Not Suitable", // Added
          "Found Keywords": ["Java", "Excel"],
          "Missing Keywords": ["Python", "Power BI"],
          "Key Strengths": ["Good Java skills."],
          "Areas for Improvement": ["Add data analytics experience."],
          "Resume Formatting & Optimization Tips": ["Improve section headings."]
        }
      ]);
      setLoading(false);
    }, 1500);

    // --- Comment out the real backend call below while testing frontend ---
    // try {
    //   const formData = new FormData();
    //   formData.append('resumes', file);
    //   formData.append('job_description', jobDescription);

    //   const data = await analyzeBulkResumes(formData);
    //   setResults(data);
    // } catch (err) {
    //   setError(err.message);
    // } finally {
    //   setLoading(false);
    // }
  };

  return (
    <Container maxWidth="xl" sx={{ minHeight: '100vh', py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Button 
          startIcon={<HomeIcon />} 
          onClick={onBack}
          sx={{ 
            color: '#B17457', 
            '&:hover': { color: '#4A4947' },
            fontSize: '1.3rem',         // Increased font size
            px: 5,                      // Increased horizontal padding
            py: 2,                      // Increased vertical padding
            borderRadius: 3,            // More rounded corners
            minHeight: '56px',          // Ensures button is tall
            minWidth: '180px',          // Ensures button is wide
            fontWeight: 700,
          }}
          size="large"                  // Explicitly set size
        >
          Back
        </Button>
      </Box>

      <Typography 
        variant="h3" 
        sx={{
          fontFamily: 'Montserrat, Arial, sans-serif', // Updated font
          color: '#B17457',
          fontWeight: 700,
          textAlign: 'center',
          mb: 2
        }}
      >
        Resume Analysis
      </Typography>

      <Box sx={{ 
        maxWidth: '800px', 
        mx: 'auto',
        p: 4,
        backgroundColor: '#FAF7F0',
        borderRadius: '12px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        fontFamily: 'Montserrat, Arial, sans-serif'
      }}>
        <input
          accept=".zip"
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ 
            marginBottom: '20px',
            width: '100%',
            fontFamily: 'Open Sans, sans-serif'
          }}
        />
        
        <TextField
          fullWidth
          multiline
          rows={6}
          label="Job Description"
          variant="outlined"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          sx={{
            mb: 3,
            fontFamily: 'Montserrat, Arial, sans-serif',
            '& .MuiInputLabel-root': {
              fontFamily: 'Montserrat, Arial, sans-serif',
              color: '#B17457'
            },
            '& .MuiOutlinedInput-root': {
              fontFamily: 'Montserrat, Arial, sans-serif',
              '& fieldset': {
                borderColor: '#B17457'
              },
              '&:hover fieldset': {
                borderColor: '#4A4947'
              }
            }
          }}
        />

        <Button
          variant="contained"
          fullWidth
          onClick={handleSubmit}
          sx={{
            backgroundColor: '#B17457',
            color: '#FAF7F0',
            fontFamily: 'Raleway, sans-serif',
            fontWeight: 700,
            py: 2.2,
            px: 5,
            fontSize: '1.3rem',
            borderRadius: 3,
            mt: 1,
            mb: 2,
            minHeight: '56px',
            minWidth: '180px',
            '&:hover': {
              backgroundColor: '#4A4947'
            }
          }}
          size="large"
          disabled={loading}
        >
          ANALYZE RESUMES
        </Button>

        {loading && (
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              mt: 3,
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
              Analyzing all resumes, please wait...
            </Typography>
          </Box>
        )}
      </Box>
      {/* Table is now outside the card */}
      {results && (
        <Box sx={{ mt: 6, overflowX: 'auto', maxWidth: '1000px', mx: 'auto' }}>
          <Typography variant="h6" sx={{ mb: 2, fontFamily: 'Montserrat, Arial, sans-serif', fontWeight: 700 }}>
            Bulk Analysis Results
          </Typography>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'Montserrat, Arial, sans-serif' }}>
            <thead>
              <tr style={{ background: '#f0e6dd' }}>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>File Name</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Match %</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Suitability</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Found Keywords</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Missing Keywords</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Key Strengths</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Areas for Improvement</th>
                <th style={{ border: '1px solid #bdbdbd', padding: '8px', fontWeight: 700 }}>Formatting & Tips</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx} style={{ background: idx % 2 === 0 ? '#fff' : '#f9f6f2' }}>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{row.name}</td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{row["Match Percentage"]}</td>
                  <td style={{
                    border: '1px solid #bdbdbd',
                    padding: '8px',
                    fontWeight: 700,
                    color: row["Suitability"] === "Suitable" ? "#2e7d32" : "#c62828" // Green for Suitable, Red for Not Suitable
                  }}>
                    {row["Suitability"]}
                  </td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{(row["Found Keywords"] || []).join(', ')}</td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{(row["Missing Keywords"] || []).join(', ')}</td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{(row["Key Strengths"] || []).join(', ')}</td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{(row["Areas for Improvement"] || []).join(', ')}</td>
                  <td style={{ border: '1px solid #bdbdbd', padding: '8px' }}>{(row["Resume Formatting & Optimization Tips"] || []).join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
      )}
    </Container>
  );
};

export default BulkAnalysis;