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
    LinearProgress,
    Chip,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Divider,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
} from '@mui/material';
import { matchAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import ErrorIcon from '@mui/icons-material/Error';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import CodeIcon from '@mui/icons-material/Code';
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';

const Match = () => {
    const navigate = useNavigate();
    const [resumeText, setResumeText] = useState('');
    const [jdText, setJdText] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);

    const handleMatch = async () => {
        if (!resumeText.trim() || !jdText.trim()) {
            setError('Please enter both resume and job description');
            return;
        }

        try {
            setLoading(true);
            setError('');
            const data = await matchAPI.match(resumeText, jdText);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to match resume to job');
        } finally {
            setLoading(false);
        }
    };

    const getMatchColor = (score) => {
        if (score >= 75) return '#4caf50'; // green
        if (score >= 50) return '#ff9800'; // orange
        return '#f44336'; // red
    };

    const getMatchRecommendation = (recommendation) => {
        const recommendations = {
            'Excellent Match': { icon: CheckCircleIcon, color: '#4caf50' },
            'Good Match': { icon: CheckCircleIcon, color: '#8bc34a' },
            'Moderate Match': { icon: WarningIcon, color: '#ff9800' },
            'Poor Match': { icon: ErrorIcon, color: '#f44336' },
        };
        return recommendations[recommendation] || recommendations['Moderate Match'];
    };

    const handleReset = () => {
        setResumeText('');
        setJdText('');
        setResult(null);
        setError('');
    };

    if (result) {
        const RecIcon = getMatchRecommendation(result.overall_recommendation || result.recommendation).icon;
        const recColor = getMatchRecommendation(result.overall_recommendation || result.recommendation).color;

        return (
            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => setResult(null)}
                    sx={{ mb: 2 }}
                >
                    Back
                </Button>

                <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
                    🎯 Match Analysis Results
                </Typography>

                <Grid container spacing={3}>
                    {/* Overall Match Score Card */}
                    <Grid item xs={12}>
                        <Card sx={{ bgcolor: '#f5f5f5', boxShadow: 3 }}>
                            <CardContent>
                                <Box display="flex" alignItems="center" justifyContent="space-between">
                                    <Box>
                                        <Typography variant="body2" color="textSecondary" sx={{ fontWeight: 600 }}>
                                            Overall Match Score
                                        </Typography>
                                        <Typography variant="h2" sx={{ fontWeight: 'bold', color: getMatchColor(result.match_score) }}>
                                            {Math.round(result.match_score)}%
                                        </Typography>
                                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                                            {result.recommendation_detail || 'Match analysis complete'}
                                        </Typography>
                                    </Box>
                                    <Box textAlign="center">
                                        <RecIcon sx={{ fontSize: 64, color: recColor, mb: 1 }} />
                                        <Chip
                                            label={result.overall_recommendation || result.recommendation}
                                            sx={{
                                                bgcolor: recColor,
                                                color: 'white',
                                                fontWeight: 'bold',
                                                fontSize: '0.95rem',
                                                py: 2.5,
                                                px: 1,
                                            }}
                                        />
                                    </Box>
                                </Box>
                                <LinearProgress
                                    variant="determinate"
                                    value={result.match_score}
                                    sx={{
                                        mt: 2,
                                        height: 12,
                                        borderRadius: 5,
                                        backgroundColor: '#e0e0e0',
                                        '& .MuiLinearProgress-bar': {
                                            backgroundColor: getMatchColor(result.match_score),
                                        },
                                    }}
                                />
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Score Breakdown - Expandable Section */}
                    <Grid item xs={12}>
                        <Accordion defaultExpanded>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                                    <Typography variant="h6" sx={{ fontWeight: 'bold', mr: 2 }}>
                                        📊 Score Breakdown
                                    </Typography>
                                </Box>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Grid container spacing={2}>
                                    {/* Skill Score */}
                                    <Grid item xs={12} md={4}>
                                        <Card sx={{ height: '100%' }}>
                                            <CardContent>
                                                <Box display="flex" alignItems="center" mb={1.5}>
                                                    <CodeIcon sx={{ mr: 1, color: '#2196f3' }} />
                                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                        Skills Match
                                                    </Typography>
                                                </Box>
                                                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#2196f3', mb: 1 }}>
                                                    {Math.round(result.breakdown?.skill_score || 0)}%
                                                </Typography>
                                                <LinearProgress
                                                    variant="determinate"
                                                    value={result.breakdown?.skill_score || 0}
                                                    sx={{
                                                        height: 8,
                                                        borderRadius: 5,
                                                        backgroundColor: '#e3f2fd',
                                                        '& .MuiLinearProgress-bar': {
                                                            backgroundColor: '#2196f3',
                                                        },
                                                    }}
                                                />
                                                {result.breakdown?.skill_score_detail && (
                                                    <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                                                        {result.breakdown.skill_score_detail}
                                                    </Typography>
                                                )}
                                            </CardContent>
                                        </Card>
                                    </Grid>

                                    {/* Experience Score */}
                                    <Grid item xs={12} md={4}>
                                        <Card sx={{ height: '100%' }}>
                                            <CardContent>
                                                <Box display="flex" alignItems="center" mb={1.5}>
                                                    <WorkIcon sx={{ mr: 1, color: '#ff9800' }} />
                                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                        Experience Match
                                                    </Typography>
                                                </Box>
                                                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#ff9800', mb: 1 }}>
                                                    {Math.round(result.breakdown?.experience_score || 0)}%
                                                </Typography>
                                                <LinearProgress
                                                    variant="determinate"
                                                    value={result.breakdown?.experience_score || 0}
                                                    sx={{
                                                        height: 8,
                                                        borderRadius: 5,
                                                        backgroundColor: '#fff3e0',
                                                        '& .MuiLinearProgress-bar': {
                                                            backgroundColor: '#ff9800',
                                                        },
                                                    }}
                                                />
                                                {result.breakdown?.experience_score_detail && (
                                                    <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                                                        {result.breakdown.experience_score_detail}
                                                    </Typography>
                                                )}
                                            </CardContent>
                                        </Card>
                                    </Grid>

                                    {/* Education Score */}
                                    <Grid item xs={12} md={4}>
                                        <Card sx={{ height: '100%' }}>
                                            <CardContent>
                                                <Box display="flex" alignItems="center" mb={1.5}>
                                                    <SchoolIcon sx={{ mr: 1, color: '#4caf50' }} />
                                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                        Education Match
                                                    </Typography>
                                                </Box>
                                                <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#4caf50', mb: 1 }}>
                                                    {Math.round(result.breakdown?.education_score || 0)}%
                                                </Typography>
                                                <LinearProgress
                                                    variant="determinate"
                                                    value={result.breakdown?.education_score || 0}
                                                    sx={{
                                                        height: 8,
                                                        borderRadius: 5,
                                                        backgroundColor: '#f1f8e9',
                                                        '& .MuiLinearProgress-bar': {
                                                            backgroundColor: '#4caf50',
                                                        },
                                                    }}
                                                />
                                                {result.breakdown?.education_score_detail && (
                                                    <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                                                        {result.breakdown.education_score_detail}
                                                    </Typography>
                                                )}
                                            </CardContent>
                                        </Card>
                                    </Grid>
                                </Grid>
                            </AccordionDetails>
                        </Accordion>
                    </Grid>

                    {/* Skill Match Details */}
                    {result.skill_match && Object.keys(result.skill_match).length > 0 && (
                        <Grid item xs={12}>
                            <Accordion>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                        🛠️ Skill Analysis
                                    </Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Box sx={{ width: '100%' }}>
                                        {/* Matched Skills */}
                                        {result.skill_match.matched && result.skill_match.matched.length > 0 && (
                                            <Box sx={{ mb: 3 }}>
                                                <Box display="flex" alignItems="center" mb={1.5}>
                                                    <CheckIcon sx={{ color: '#4caf50', mr: 1, fontWeight: 'bold' }} />
                                                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: '#4caf50' }}>
                                                        Matched Skills ({result.skill_match.matched.length})
                                                    </Typography>
                                                </Box>
                                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                                    {result.skill_match.matched.map((skill, idx) => (
                                                        <Chip
                                                            key={idx}
                                                            label={skill}
                                                            color="success"
                                                            icon={<CheckIcon />}
                                                            variant="outlined"
                                                        />
                                                    ))}
                                                </Box>
                                            </Box>
                                        )}

                                        {/* Missing Skills */}
                                        {result.skill_match.missing && result.skill_match.missing.length > 0 && (
                                            <Box>
                                                <Box display="flex" alignItems="center" mb={1.5}>
                                                    <CloseIcon sx={{ color: '#f44336', mr: 1 }} />
                                                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: '#f44336' }}>
                                                        Missing Skills ({result.skill_match.missing.length})
                                                    </Typography>
                                                </Box>
                                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                                    {result.skill_match.missing.map((skill, idx) => (
                                                        <Chip
                                                            key={idx}
                                                            label={skill}
                                                            color="error"
                                                            icon={<CloseIcon />}
                                                            variant="outlined"
                                                        />
                                                    ))}
                                                </Box>
                                            </Box>
                                        )}
                                    </Box>
                                </AccordionDetails>
                            </Accordion>
                        </Grid>
                    )}

                    {/* Experience Analysis */}
                    {result.experience_match && (
                        <Grid item xs={12}>
                            <Accordion>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                        💼 Experience Analysis
                                    </Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Grid container spacing={2} sx={{ width: '100%' }}>
                                        <Grid item xs={12} sm={6}>
                                            <Card>
                                                <CardContent>
                                                    <Typography color="textSecondary" gutterBottom>
                                                        Required Experience
                                                    </Typography>
                                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                        {result.experience_match.required || 'Not specified'}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                        <Grid item xs={12} sm={6}>
                                            <Card>
                                                <CardContent>
                                                    <Typography color="textSecondary" gutterBottom>
                                                        Your Experience
                                                    </Typography>
                                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                        {result.experience_match.candidate || 'Not available'}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    </Grid>
                                </AccordionDetails>
                            </Accordion>
                        </Grid>
                    )}

                    {/* Education Analysis */}
                    {result.education_match && (
                        <Grid item xs={12}>
                            <Accordion>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                        🎓 Education Analysis
                                    </Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Grid container spacing={2} sx={{ width: '100%' }}>
                                        <Grid item xs={12} sm={6}>
                                            <Card>
                                                <CardContent>
                                                    <Typography color="textSecondary" gutterBottom>
                                                        Required Education
                                                    </Typography>
                                                    <Typography variant="body2">
                                                        {result.education_match.required || 'Not specified'}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                        <Grid item xs={12} sm={6}>
                                            <Card>
                                                <CardContent>
                                                    <Typography color="textSecondary" gutterBottom>
                                                        Your Education
                                                    </Typography>
                                                    <Typography variant="body2">
                                                        {result.education_match.candidate || 'Not available'}
                                                    </Typography>
                                                </CardContent>
                                            </Card>
                                        </Grid>
                                    </Grid>
                                </AccordionDetails>
                            </Accordion>
                        </Grid>
                    )}

                    {/* Improvement Tips */}
                    {result.improvement_tips && result.improvement_tips.length > 0 && (
                        <Grid item xs={12}>
                            <Card sx={{ bgcolor: '#fff8e1', border: '2px solid #ffc107' }}>
                                <CardContent>
                                    <Box display="flex" alignItems="center" mb={2}>
                                        <TipsAndUpdatesIcon sx={{ color: '#ffc107', mr: 1, fontSize: 28 }} />
                                        <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#f57f17' }}>
                                            💡 Improvement Tips ({result.improvement_tips.length})
                                        </Typography>
                                    </Box>
                                    <List>
                                        {result.improvement_tips.map((tip, idx) => (
                                            <ListItem key={idx}>
                                                <ListItemIcon>
                                                    <CheckCircleIcon sx={{ color: '#ffc107' }} />
                                                </ListItemIcon>
                                                <ListItemText
                                                    primary={tip}
                                                    primaryTypographyProps={{
                                                        variant: 'body2',
                                                        color: 'textPrimary',
                                                    }}
                                                />
                                            </ListItem>
                                        ))}
                                    </List>
                                </CardContent>
                            </Card>
                        </Grid>
                    )}

                    {/* Credits Used */}
                    <Grid item xs={12}>
                        <Card sx={{ bgcolor: '#e8f5e9' }}>
                            <CardContent>
                                <Box display="flex" justifyContent="space-between" alignItems="center">
                                    <Box>
                                        <Typography variant="body2" color="textSecondary" sx={{ fontWeight: 600 }}>
                                            Credits Used
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#4caf50' }}>
                                            {result.credits_deducted} credits
                                        </Typography>
                                    </Box>
                                    <Button
                                        variant="contained"
                                        color="primary"
                                        onClick={() => {
                                            setResult(null);
                                            handleReset();
                                        }}
                                    >
                                        Run Another Comparison
                                    </Button>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            </Container>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/dashboard')}
                sx={{ mb: 2 }}
            >
                Back to Dashboard
            </Button>

            <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
                Resume to Job Matcher
            </Typography>

            <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
                Compare a resume with a job description to get a match score and skill gap analysis.
            </Typography>

            <Grid container spacing={3}>
                {error && (
                    <Grid item xs={12}>
                        <Alert severity="error">{error}</Alert>
                    </Grid>
                )}

                {/* Resume Section */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                                Resume
                            </Typography>
                            <TextField
                                fullWidth
                                label="Resume Content"
                                multiline
                                rows={10}
                                value={resumeText}
                                onChange={(e) => setResumeText(e.target.value)}
                                placeholder="Paste resume text here..."
                                disabled={loading}
                                variant="outlined"
                            />
                        </CardContent>
                    </Card>
                </Grid>

                {/* Job Description Section */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                                Job Description
                            </Typography>
                            <TextField
                                fullWidth
                                label="Job Description Content"
                                multiline
                                rows={10}
                                value={jdText}
                                onChange={(e) => setJdText(e.target.value)}
                                placeholder="Paste job description text here..."
                                disabled={loading}
                                variant="outlined"
                            />
                        </CardContent>
                    </Card>
                </Grid>

                {/* Buttons */}
                <Grid item xs={12}>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button
                            variant="contained"
                            color="primary"
                            size="large"
                            onClick={handleMatch}
                            disabled={loading || !resumeText.trim() || !jdText.trim()}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Compare Now'}
                        </Button>

                        <Button
                            variant="outlined"
                            onClick={handleReset}
                            disabled={loading}
                        >
                            Clear All
                        </Button>
                    </Box>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Match;
