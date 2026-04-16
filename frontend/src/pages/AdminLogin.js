import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
    Card,
    CardContent,
    TextField,
    Button,
    Typography,
    Alert,
    CircularProgress,
    Paper,
} from '@mui/material';
import { authAPI } from '../services/api';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';

const AdminLogin = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        
        if (!email || !password) {
            setError('Email and password are required');
            return;
        }

        try {
            setLoading(true);
            setError('');
            
            const response = await authAPI.login(email, password);
            
            // Store token
            localStorage.setItem('token', response.access_token);
            localStorage.setItem('userRole', 'admin');
            localStorage.setItem('userEmail', email);
            
            // Verify it's an admin token
            const payload = JSON.parse(atob(response.access_token.split('.')[1]));
            if (payload.role !== 'admin') {
                setError('This account does not have admin privileges');
                localStorage.clear();
                return;
            }
            
            // Navigate to admin dashboard
            navigate('/admin-dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            }}
        >
            <Container maxWidth="sm">
                <Card sx={{ boxShadow: 5 }}>
                    <CardContent sx={{ p: 4 }}>
                        {/* Header */}
                        <Box sx={{ textAlign: 'center', mb: 3 }}>
                            <AdminPanelSettingsIcon
                                sx={{
                                    fontSize: 60,
                                    color: '#667eea',
                                    mb: 2,
                                }}
                            />
                            <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                                Admin Panel
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                                Secure login for administrators
                            </Typography>
                        </Box>

                        {/* Error Alert */}
                        {error && (
                            <Alert severity="error" sx={{ mb: 2 }}>
                                {error}
                            </Alert>
                        )}

                        {/* Login Form */}
                        <Box component="form" onSubmit={handleLogin} sx={{ mt: 3 }}>
                            <TextField
                                fullWidth
                                label="Email Address"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                margin="normal"
                                disabled={loading}
                                required
                            />

                            <TextField
                                fullWidth
                                label="Password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                margin="normal"
                                disabled={loading}
                                required
                            />

                            <Button
                                fullWidth
                                variant="contained"
                                sx={{
                                    mt: 3,
                                    mb: 2,
                                    py: 1.5,
                                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                    fontSize: '1rem',
                                }}
                                onClick={handleLogin}
                                disabled={loading}
                            >
                                {loading ? <CircularProgress size={24} color="inherit" /> : 'Login'}
                            </Button>

                            <Button
                                fullWidth
                                variant="outlined"
                                onClick={() => navigate('/dashboard')}
                                disabled={loading}
                            >
                                Back to User Dashboard
                            </Button>
                        </Box>

                        {/* Info Box */}
                        <Paper sx={{ mt: 3, p: 2, bgcolor: '#f5f5f5' }}>
                            <Typography variant="caption" color="textSecondary" display="block">
                                <strong>ℹ️ First time login?</strong>
                            </Typography>
                            <Typography variant="caption" color="textSecondary" display="block" sx={{ mt: 1 }}>
                                Contact your system administrator for admin credentials or run the admin seed script.
                            </Typography>
                        </Paper>
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
};

export default AdminLogin;
