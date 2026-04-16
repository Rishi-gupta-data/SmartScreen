import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
    Grid,
    Card,
    CardContent,
    Typography,
    Button,
    CircularProgress,
    Alert,
    Avatar,
    Paper,
} from '@mui/material';
import { authAPI } from '../services/api';
import axios from 'axios';
import LogoutIcon from '@mui/icons-material/Logout';
import PeopleIcon from '@mui/icons-material/People';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import HistoryIcon from '@mui/icons-material/History';
import SettingsIcon from '@mui/icons-material/Settings';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [userEmail, setUserEmail] = useState('');

    useEffect(() => {
        fetchAdminStats();
        setUserEmail(localStorage.getItem('userEmail') || 'Admin');
    }, []);

    const fetchAdminStats = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:8000/api/v1/admin/stats', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setStats(response.data);
            setError('');
        } catch (err) {
            setError('Failed to load admin stats');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/admin-login');
    };

    const StatCard = ({ title, value, icon: Icon, color, action }) => (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                        <Typography color="textSecondary" gutterBottom sx={{ fontSize: '0.875rem' }}>
                            {title}
                        </Typography>
                        <Typography variant="h4" sx={{ fontWeight: 'bold', color }}>
                            {value || 0}
                        </Typography>
                    </Box>
                    <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
                        <Icon />
                    </Avatar>
                </Box>
                {action && (
                    <Button
                        size="small"
                        onClick={action}
                        sx={{ mt: 2, textTransform: 'none' }}
                    >
                        View Details →
                    </Button>
                )}
            </CardContent>
        </Card>
    );

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            {/* Header */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        Admin Dashboard
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        Welcome back, {userEmail}
                    </Typography>
                </Box>
                <Button
                    variant="outlined"
                    startIcon={<LogoutIcon />}
                    onClick={handleLogout}
                    color="error"
                >
                    Logout
                </Button>
            </Box>

            {/* Error Alert */}
            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {/* Stats Grid */}
            {stats && (
                <Grid container spacing={3} sx={{ mb: 4 }}>
                    <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                            title="Total Users"
                            value={stats.total_users}
                            icon={PeopleIcon}
                            color="#2196F3"
                            action={() => navigate('/admin-users')}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                            title="Admin Accounts"
                            value={stats.total_admins}
                            icon={AdminPanelSettingsIcon}
                            color="#FF9800"
                            action={() => navigate('/admin-management')}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                            title="Credits Sold"
                            value={stats.total_credits_sold}
                            icon={AttachMoneyIcon}
                            color="#4CAF50"
                        />
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <StatCard
                            title="Total Transactions"
                            value={stats.total_transactions}
                            icon={HistoryIcon}
                            color="#9C27B0"
                        />
                    </Grid>
                </Grid>
            )}

            {/* Quick Actions */}
            <Paper sx={{ p: 3, mb: 4 }}>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                    Quick Actions
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm={6} md={3}>
                        <Button
                            fullWidth
                            variant="contained"
                            startIcon={<AdminPanelSettingsIcon />}
                            onClick={() => navigate('/admin-management')}
                            sx={{
                                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                py: 1.5,
                            }}
                        >
                            Manage Admins
                        </Button>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Button
                            fullWidth
                            variant="outlined"
                            startIcon={<PeopleIcon />}
                            onClick={() => navigate('/admin-users')}
                            sx={{ py: 1.5 }}
                        >
                            View Users
                        </Button>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Button
                            fullWidth
                            variant="outlined"
                            startIcon={<HistoryIcon />}
                            sx={{ py: 1.5 }}
                        >
                            Transactions
                        </Button>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Button
                            fullWidth
                            variant="outlined"
                            startIcon={<SettingsIcon />}
                            sx={{ py: 1.5 }}
                        >
                            Settings
                        </Button>
                    </Grid>
                </Grid>
            </Paper>

            {/* Info Box */}
            <Paper sx={{ p: 3, bgcolor: '#f5f5f5', borderLeft: '4px solid #667eea' }}>
                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                    📊 System Information
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="textSecondary">
                            <strong>Total Users:</strong> {stats?.total_users}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="textSecondary">
                            <strong>Admin Count:</strong> {stats?.total_admins}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="textSecondary">
                            <strong>Active Transactions:</strong> {stats?.total_transactions}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="textSecondary">
                            <strong>Revenue (Credits):</strong> ₹{(stats?.total_credits_sold * 0.5).toFixed(2)}
                        </Typography>
                    </Grid>
                </Grid>
            </Paper>
        </Container>
    );
};

export default AdminDashboard;
