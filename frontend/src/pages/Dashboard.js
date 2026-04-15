import React, { useContext, useEffect, useState } from 'react';
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
    AppBar,
    Toolbar,
    LinearProgress,
    List,
    ListItem,
    ListItemText,
    Chip,
} from '@mui/material';
import { AuthContext } from '../context/AuthContext';
import { billingAPI } from '../services/api';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import DescriptionIcon from '@mui/icons-material/Description';
import AssignmentIcon from '@mui/icons-material/Assignment';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import HistoryIcon from '@mui/icons-material/History';

const Dashboard = () => {
    const navigate = useNavigate();
    const { user, logout } = useContext(AuthContext);
    const [credits, setCredits] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            const creditsData = await billingAPI.getCredits();
            setCredits(creditsData.credits);
            
            const transactionsData = await billingAPI.getTransactions(0, 5);
            setTransactions(transactionsData.transactions || []);
            setError('');
        } catch (err) {
            setError('Failed to load dashboard data');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const handleBuyCredits = () => {
        navigate('/billing');
    };

    // Calculate stats
    const creditsUsedThisMonth = transactions
        .filter(t => t.type === 'deduct')
        .reduce((sum, t) => sum + t.amount, 0);
    
    const creditsAddedThisMonth = transactions
        .filter(t => t.type === 'add')
        .reduce((sum, t) => sum + t.amount, 0);

    const getTransactionIcon = (type) => {
        return type === 'deduct' ? '📉' : '📈';
    };

    const getTransactionColor = (type) => {
        return type === 'deduct' ? '#ff6b6b' : '#51cf66';
    };

    const QuickActionCard = ({ icon: Icon, title, description, action, actionLabel }) => (
        <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Icon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                    {title}
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    {description}
                </Typography>
                <Button
                    variant="contained"
                    color="primary"
                    size="small"
                    onClick={action}
                >
                    {actionLabel}
                </Button>
            </CardContent>
        </Card>
    );

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            {/* Header with Logout */}
            <AppBar position="static" sx={{ backgroundColor: '#1a237e' }}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        SmartScreen Dashboard
                    </Typography>
                    <Button
                        color="inherit"
                        onClick={handleLogout}
                        sx={{ ml: 2 }}
                    >
                        Logout
                    </Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ py: 4 }}>
                {/* Credits Section */}
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Card sx={{ bgcolor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                            <CardContent>
                                <Box display="flex" justifyContent="space-between" alignItems="center">
                                    <Box>
                                        <Typography variant="body2" sx={{ opacity: 0.9 }}>
                                            Available Credits
                                        </Typography>
                                        {loading ? (
                                            <CircularProgress size={32} sx={{ color: 'white' }} />
                                        ) : (
                                            <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                                                {credits}
                                            </Typography>
                                        )}
                                    </Box>
                                    <Box>
                                        <Button
                                            variant="contained"
                                            color="secondary"
                                            onClick={handleBuyCredits}
                                            sx={{ bgcolor: 'white', color: 'primary', '&:hover': { bgcolor: '#f0f0f0' } }}
                                        >
                                            Buy Credits
                                        </Button>
                                    </Box>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Error Alert */}
                    {error && (
                        <Grid item xs={12}>
                            <Alert severity="error">{error}</Alert>
                        </Grid>
                    )}

                    {/* Quick Actions */}
                    <Grid item xs={12}>
                        <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
                            Quick Actions
                        </Typography>
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <QuickActionCard
                            icon={DescriptionIcon}
                            title="Parse Resume"
                            description="Extract information from resumes (5 credits)"
                            action={() => navigate('/resume')}
                            actionLabel="Upload Resume"
                        />
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <QuickActionCard
                            icon={AssignmentIcon}
                            title="Parse Job Description"
                            description="Extract job details (3 credits)"
                            action={() => navigate('/jd')}
                            actionLabel="Add Job Description"
                        />
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <QuickActionCard
                            icon={CompareArrowsIcon}
                            title="Match Resume to Job"
                            description="Find compatibility (5 credits)"
                            action={() => navigate('/match')}
                            actionLabel="Match Now"
                        />
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <QuickActionCard
                            icon={CreditCardIcon}
                            title="Transaction History"
                            description="View credit usage history"
                            action={() => navigate('/transactions')}
                            actionLabel="View History"
                        />
                    </Grid>

                    {/* Statistics */}
                    <Grid item xs={12}>
                        <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
                            📊 Statistics
                        </Typography>
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <TrendingUpIcon sx={{ fontSize: 32, color: '#51cf66', mb: 1 }} />
                                <Typography color="textSecondary" variant="body2">
                                    Credits Added
                                </Typography>
                                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#51cf66' }}>
                                    +{creditsAddedThisMonth}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <CompareArrowsIcon sx={{ fontSize: 32, color: '#ff6b6b', mb: 1 }} />
                                <Typography color="textSecondary" variant="body2">
                                    Credits Used
                                </Typography>
                                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#ff6b6b' }}>
                                    -{creditsUsedThisMonth}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <HistoryIcon sx={{ fontSize: 32, color: '#ffa94d', mb: 1 }} />
                                <Typography color="textSecondary" variant="body2">
                                    Recent Activity
                                </Typography>
                                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#ffa94d' }}>
                                    {transactions.length}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent sx={{ textAlign: 'center' }}>
                                <CreditCardIcon sx={{ fontSize: 32, color: '#667eea', mb: 1 }} />
                                <Typography color="textSecondary" variant="body2">
                                    Balance
                                </Typography>
                                <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#667eea' }}>
                                    {credits}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Recent Activity */}
                    {transactions.length > 0 && (
                        <>
                            <Grid item xs={12}>
                                <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
                                    📝 Recent Activity
                                </Typography>
                            </Grid>

                            <Grid item xs={12}>
                                <Card>
                                    <CardContent>
                                        <List dense>
                                            {transactions.slice(0, 5).map((transaction, idx) => (
                                                <ListItem key={idx} sx={{ py: 1 }}>
                                                    <ListItemText
                                                        primary={
                                                            <Box display="flex" alignItems="center" gap={1}>
                                                                <span>{getTransactionIcon(transaction.type)}</span>
                                                                <span>{transaction.description || `${transaction.type} credits`}</span>
                                                            </Box>
                                                        }
                                                        secondary={
                                                            <Box display="flex" justifyContent="space-between">
                                                                <span>
                                                                    {new Date(transaction.created_at).toLocaleDateString()}
                                                                </span>
                                                                <Chip
                                                                    label={`${transaction.type === 'deduct' ? '-' : '+'}${transaction.amount}`}
                                                                    size="small"
                                                                    sx={{
                                                                        bgcolor: getTransactionColor(transaction.type),
                                                                        color: 'white',
                                                                        fontWeight: 'bold',
                                                                    }}
                                                                />
                                                            </Box>
                                                        }
                                                    />
                                                </ListItem>
                                            ))}
                                        </List>
                                        <Button
                                            variant="text"
                                            fullWidth
                                            onClick={() => navigate('/transactions')}
                                            sx={{ mt: 1 }}
                                        >
                                            View All Transactions
                                        </Button>
                                    </CardContent>
                                </Card>
                            </Grid>
                        </>
                    )}

                    {/* Usage Information */}
                    <Grid item xs={12}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    💡 Credit Usage Guide
                                </Typography>
                                <Box component="ul" sx={{ pl: 2 }}>
                                    <Typography component="li" variant="body2">
                                        Parse Resume: 5 credits
                                    </Typography>
                                    <Typography component="li" variant="body2">
                                        Parse Job Description: 3 credits
                                    </Typography>
                                    <Typography component="li" variant="body2">
                                        Match Resume to Job: 5 credits
                                    </Typography>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            </Container>
        </Box>
    );
};

export default Dashboard;
