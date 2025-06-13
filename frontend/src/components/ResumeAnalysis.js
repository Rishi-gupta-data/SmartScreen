import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const sectionData = [
  {
    label: '📊 Match Percentage',
    key: ['Match Percentage', 'match_percentage'],
    render: (data) => (
      <Typography>
        <strong>Match Percentage:</strong> {data['Match Percentage'] || data['match_percentage']}
      </Typography>
    ),
  },
  {
    label: '🔑 Found Keywords',
    key: ['Found Keywords', 'found_keywords'],
    render: (data) => (
      <Typography>
        <strong>Found Keywords:</strong> {(data['Found Keywords'] || data['found_keywords'] || []).join(', ')}
      </Typography>
    ),
  },
  {
    label: '❌ Missing Keywords',
    key: ['Missing Keywords', 'missing_keywords'],
    render: (data) => (
      <Typography>
        <strong>Missing Keywords:</strong> {(data['Missing Keywords'] || data['missing_keywords'] || []).join(', ')}
      </Typography>
    ),
  },
  {
    label: '⭐ Key Strengths',
    key: ['Key Strengths', 'key_strengths'],
    render: (data) => (
      <Typography>
        <strong>Key Strengths:</strong> {(data['Key Strengths'] || data['key_strengths'] || []).join(', ')}
      </Typography>
    ),
  },
  {
    label: '🔍 Areas for Improvement',
    key: ['Areas for Improvement', 'areas_for_improvement'],
    render: (data) => (
      <Typography>
        <strong>Areas for Improvement:</strong> {(data['Areas for Improvement'] || data['areas_for_improvement'] || []).join(', ')}
      </Typography>
    ),
  },
  {
    label: '🎨 Resume Formatting & Optimization Tips',
    key: ['Resume Formatting & Optimization Tips', 'resume_formatting_tips'],
    render: (data) => (
      <Typography>
        <strong>Resume Formatting & Optimization Tips:</strong> {(data['Resume Formatting & Optimization Tips'] || data['resume_formatting_tips'] || []).join(', ')}
      </Typography>
    ),
  },
];

const accordionStyle = {
  border: '2px solid #bdbdbd',
  borderRadius: '8px',
  marginBottom: '16px',
  boxShadow: 'none',
  '&:hover': {
    borderColor: '#1976d2',
    backgroundColor: '#f5faff',
  },
};

const summaryStyle = {
  fontWeight: 'bold',
  fontSize: '1.1rem',
};

function ResumeAnalysis({ analysis, onBack }) {
  if (!analysis) {
    return <div style={{ fontFamily: 'Montserrat, Arial, sans-serif' }}>No analysis data available.</div>;
  }

  return (
    <Box sx={{ mt: 2, fontFamily: 'Montserrat, Arial, sans-serif' }}>
      <button onClick={onBack} style={{ marginBottom: 16, fontFamily: 'Montserrat, Arial, sans-serif' }}>Back</button>
      <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', fontFamily: 'Montserrat, Arial, sans-serif' }}>
        Analysis Results:
      </Typography>
      {sectionData.map((section, idx) => {
        // Find the first key that exists in the analysis object
        const key = section.key.find(k => analysis[k]);
        if (!key) return null;
        return (
          <Accordion key={section.label} sx={accordionStyle}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`panel${idx}-content`}
              id={`panel${idx}-header`}
              sx={{ ...summaryStyle, fontFamily: 'Montserrat, Arial, sans-serif' }}
            >
              {section.label}
            </AccordionSummary>
            <AccordionDetails sx={{ fontFamily: 'Montserrat, Arial, sans-serif' }}>
              {section.render(analysis)}
            </AccordionDetails>
          </Accordion>
        );
      })}
    </Box>
  );
}

export default ResumeAnalysis;