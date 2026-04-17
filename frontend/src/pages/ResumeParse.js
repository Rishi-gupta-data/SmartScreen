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
import { resumeAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const ResumeParse = () => {
    const navigate = useNavigate();
    const [tab, setTab] = useState(0); // 0 = text input, 1 = file upload
    const [resumeText, setResumeText] = useState('');
    const [resumeFile, setResumeFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    const handleParse = async () => {
        if (tab === 0 && !resumeText.trim()) {
            setError('Please enter resume content');
            return;
        }
        
        if (tab === 1 && !resumeFile) {
            setError('Please select a resume file');
            return;
        }

        try {
            setLoading(true);
            setError('');
            
            let data;
            if (tab === 0) {
                // Text input
                data = await resumeAPI.parse(resumeText);
            } else {
                // File upload
                data = await resumeAPI.parseFile(resumeFile);
            }
            
            setResult(data);
        } catch (err) {
            setError(err.message || 'Failed to parse resume');
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
            setResumeFile(file);
            setError('');
        }
    };

    const handleReset = () => {
        setResumeText('');
        setResumeFile(null);
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
                    Resume Analysis Results
                </Typography>

                <Grid container spacing={3}>
                    {/* Personal Info */}
                    <Grid item xs={12} md={6}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Personal Information
                                </Typography>
                                <List dense>
                                    <ListItem>
                                        <ListItemText
                                            primary="Name"
                                            secondary={result.name || 'Not found'}
                                        />
                                    </ListItem>
                                    <ListItem>
                                        <ListItemText
                                            primary="Email"
                                            secondary={result.email || 'Not found'}
                                        />
                                    </ListItem>
                                    <ListItem>
                                        <ListItemText
                                            primary="Phone"
                                            secondary={result.phone || 'Not found'}
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

                    {/* Skills */}
                    {result.skills && result.skills.length > 0 && (
                        <Grid item xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        Skills Found
                                    </Typography>
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                        {result.skills.map((skill, idx) => (
                                            <Box
                                                key={idx}
                                                sx={{
                                                    bgcolor: 'primary.light',
                                                    color: 'white',
                                                    px: 2,
                                                    py: 1,
                                                    borderRadius: 1,
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

                    {/* Experience */}
                    {result.experience && result.experience.length > 0 && (
                        <Grid item xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        Experience
                                    </Typography>
                                    {result.experience.map((exp, idx) => (
                                        <Box key={idx} sx={{ mb: 2 }}>
                                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                                {exp}
                                            </Typography>
                                        </Box>
                                    ))}
                                </CardContent>
                            </Card>
                        </Grid>
                    )}

                    {/* Education */}
                    {result.education && result.education.length > 0 && (
                        <Grid item xs={12}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        Education
                                    </Typography>
                                    {result.education.map((edu, idx) => (
                                        <Typography key={idx} variant="body2" sx={{ mb: 1 }}>
                                            {edu}
                                        </Typography>
                                    ))}
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
                            Parse Another Resume
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
                Resume Parser
            </Typography>

            <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
                Extract key information from your resume. Choose between text input or file upload.
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
                            label="Resume Content"
                            multiline
                            rows={12}
                            value={resumeText}
                            onChange={(e) => setResumeText(e.target.value)}
                            placeholder="Paste your resume text here..."
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
                                Upload your resume (PDF, DOC, DOCX, or TXT)
                            </Typography>
                            <input
                                type="file"
                                accept=".pdf,.doc,.docx,.txt"
                                onChange={handleFileChange}
                                disabled={loading}
                                style={{ marginTop: 16 }}
                            />
                            {resumeFile && (
                                <Typography variant="body2" sx={{ mt: 2, color: 'green' }}>
                                    ✅ Selected: {resumeFile.name}
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
                            disabled={loading || !resumeText.trim()}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Parse Resume'}
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
                        💡 Tip: Copy and paste the resume text, or use Ctrl+A to select all from a document.
                    </Typography>
                </CardContent>
            </Card>
        </Container>
    );
};

export default ResumeParse;
