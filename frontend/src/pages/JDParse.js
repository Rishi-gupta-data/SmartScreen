import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
    TextField,
    Button,
    Typography,
    Card,
    CardContent,
    Alert,
    CircularProgress,
    Grid,
    List,
    ListItem,
    ListItemText,
    Tabs,
    Tab,
} from '@mui/material';
import { jdAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const JDParse = () => {
    const navigate = useNavigate();
    const [tab, setTab] = useState(0); // 0 = text input, 1 = file upload
    const [jdText, setJdText] = useState('');
    const [jdFile, setJdFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    const handleParse = async () => {
        if (tab === 0 && !jdText.trim()) {
            setError('Please enter job description content');
            return;
        }
        
        if (tab === 1 && !jdFile) {
            setError('Please select a job description file');
            return;
        }

        try {
            setLoading(true);
            setError('');
            
            let data;
            if (tab === 0) {
                // Text input
                data = await jdAPI.parse(jdText);
            } else {
                // File upload
                data = await jdAPI.parseFile(jdFile);
            }
            
            setResult(data);
        } catch (err) {
            setError(err.message || 'Failed to parse job description');
        } finally {
            setLoading(false);
        }
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file type
            const validTypes = ['application/pdf', 'application/msword', 
                                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                'text/plain'];
            if (!validTypes.includes(file.type)) {
                setError('Please upload a PDF, DOC, DOCX, or TXT file');
                return;
            }
            setJdFile(file);
            setError('');
        }
    };

    const handleReset = () => {
        setJdText('');
        setJdFile(null);
        setResult(null);
        setError('');
    };

    if (result) {
        return (
            <Container maxWidth="md" sx={{ py: 4 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => setResult(null)}
                    sx={{ mb: 2 }}
                >
                    Back
                </Button>

                <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                    Job Description Analysis Results
                </Typography>

                <Grid container spacing={3}>
                    {/* Job Title & Company */}
                    <Grid item xs={12} md={6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Job Details
                                </Typography>
                                <List dense>
                                    <ListItem>
                                        <ListItemText
                                            primary="Title"
                                            secondary={result.title || 'Not found'}
                                        />
                                    </ListItem>
                                    <ListItem>
                                        <ListItemText
                                            primary="Company"
                                            secondary={result.company || 'Not found'}
                                        />
                                    </ListItem>
                                    <ListItem>
                                        <ListItemText
                                            primary="Salary"
                                            secondary={result.salary || 'Not found'}
                                        />
                                    </ListItem>
                                </List>
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Credits Info */}
                    <Grid item xs={12} md={6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Credits Used
                                </Typography>
                                <Typography variant="h4" color="primary">
                                    {result.credits_used}
                                </Typography>
                                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                                    Remaining: {result.remaining_credits}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Required Skills */}
                    {result.required_skills && result.required_skills.length > 0 && (
                        <Grid item xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        Required Skills
                                    </Typography>
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                        {result.required_skills.map((skill, idx) => (
                                            <Box
                                                key={idx}
                                                sx={{
                                                    bgcolor: '#e3f2fd',
                                                    color: '#1976d2',
                                                    px: 2,
                                                    py: 1,
                                                    borderRadius: 1,
                                                    border: '1px solid #1976d2',
                                                }}
                                            >
                                                {skill}
                                            </Box>
                                        ))}
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    )}

                    {/* Responsibilities */}
                    {result.responsibilities && result.responsibilities.length > 0 && (
                        <Grid item xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        Responsibilities
                                    </Typography>
                                    <List dense>
                                        {result.responsibilities.map((resp, idx) => (
                                            <ListItem key={idx}>
                                                <ListItemText primary={resp} />
                                            </ListItem>
                                        ))}
                                    </List>
                                </CardContent>
                            </Card>
                        </Grid>
                    )}

                    <Grid item xs={12}>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => {
                                setResult(null);
                                handleReset();
                            }}
                        >
                            Parse Another Job Description
                        </Button>
                    </Grid>
                </Grid>
            </Container>
        );
    }

    return (
        <Container maxWidth="md" sx={{ py: 4 }}>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/dashboard')}
                sx={{ mb: 2 }}
            >
                Back to Dashboard
            </Button>

            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
                Job Description Parser
            </Typography>

            <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
                Paste a job description below. Our system will extract key information including
                job title, company, required skills, salary, and responsibilities.
            </Typography>

            <Card>
                <CardContent>
                    {error && (
                        <Alert severity="error" sx={{ mb: 2 }}>
                            {error}
                        </Alert>
                    )}

                    {/* Tab Selection */}
                    <Tabs value={tab} onChange={(e, newValue) => setTab(newValue)} sx={{ mb: 3 }}>
                        <Tab label="📝 Paste Text" />
                        <Tab label="📄 Upload File" />
                    </Tabs>

                    {/* Text Input Tab */}
                    {tab === 0 && (
                        <TextField
                            fullWidth
                            label="Job Description Content"
                            multiline
                            rows={12}
                            value={jdText}
                            onChange={(e) => setJdText(e.target.value)}
                            placeholder="Paste the job description text here..."
                            disabled={loading}
                            variant="outlined"
                        />
                    )}

                    {/* File Upload Tab */}
                    {tab === 1 && (
                        <Box sx={{ 
                            p: 3, 
                            border: '2px dashed #1976d2', 
                            borderRadius: 2, 
                            textAlign: 'center',
                            bgcolor: '#f5f5f5'
                        }}>
                            <CloudUploadIcon sx={{ fontSize: 48, color: '#1976d2', mb: 2 }} />
                            <Typography variant="body1" sx={{ mb: 2 }}>
                                Upload your job description (PDF, DOC, DOCX, or TXT)
                            </Typography>
                            <input
                                type="file"
                                accept=".pdf,.doc,.docx,.txt"
                                onChange={handleFileChange}
                                disabled={loading}
                                style={{ marginTop: 16 }}
                            />
                            {jdFile && (
                                <Typography variant="body2" sx={{ mt: 2, color: 'green' }}>
                                    ✅ Selected: {jdFile.name}
                                </Typography>
                            )}
                        </Box>
                    )}

                    <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                        <Button
                            variant="contained"
                            color="primary"
                            size="large"
                            onClick={handleParse}
                            disabled={loading || (tab === 0 && !jdText.trim()) || (tab === 1 && !jdFile)}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Parse Job Description'}
                        </Button>

                        <Button
                            variant="outlined"
                            onClick={handleReset}
                            disabled={loading}
                        >
                            Clear
                        </Button>
                    </Box>

                    <Typography variant="caption" color="textSecondary" sx={{ mt: 2, display: 'block' }}>
                        💡 Tip: Upload a job description document or paste the text directly.
                    </Typography>
                </CardContent>
            </Card>
        </Container>
    );
};

export default JDParse;
