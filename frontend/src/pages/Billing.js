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
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Dialog,
    TextField,
    Chip,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Divider,
    Paper,
    ToggleButton,
    ToggleButtonGroup,
} from '@mui/material';
import { billingAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import StarIcon from '@mui/icons-material/Star';
import LocalOfferIcon from '@mui/icons-material/LocalOffer';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

const Billing = () => {
    const navigate = useNavigate();
    const [credits, setCredits] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [buyAmount, setBuyAmount] = useState('100');
    const [buyLoading, setBuyLoading] = useState(false);
    const [selectedPlan, setSelectedPlan] = useState(null);

    const pricingPlans = [
        {
            id: 'starter',
            name: 'Starter',
            credits: 100,
            price: '₹50',
            pricePerCredit: '₹0.50',
            color: '#E3F2FD',
            borderColor: '#2196F3',
            badge: null,
            features: [
                '100 Credits',
                'Parse up to 20 resumes',
                'Basic matching',
                'Valid for 30 days',
            ],
            recommended: false,
        },
        {
            id: 'professional',
            name: 'Professional',
            credits: 500,
            price: '₹200',
            pricePerCredit: '₹0.40',
            color: '#FFF3E0',
            borderColor: '#FF9800',
            badge: 'POPULAR',
            features: [
                '500 Credits (20% bonus)',
                'Parse up to 100 resumes',
                'Advanced matching',
                'Email support',
                'Valid for 90 days',
            ],
            recommended: true,
        },
        {
            id: 'business',
            name: 'Business',
            credits: 1000,
            price: '₹350',
            pricePerCredit: '₹0.35',
            color: '#F3E5F5',
            borderColor: '#9C27B0',
            badge: 'BEST VALUE',
            features: [
                '1000 Credits (40% bonus)',
                'Unlimited parses',
                'Priority matching',
                'Priority support',
                'Valid for 180 days',
            ],
            recommended: false,
        },
        {
            id: 'enterprise',
            name: 'Enterprise',
            credits: 5000,
            price: '₹1500',
            pricePerCredit: '₹0.30',
            color: '#E8F5E9',
            borderColor: '#4CAF50',
            badge: 'SAVE 40%',
            features: [
                '5000 Credits (50% bonus)',
                'Unlimited everything',
                'Dedicated support',
                'Custom features',
                'Valid for 1 year',
            ],
            recommended: false,
        },
    ];

    useEffect(() => {
        fetchBillingData();
    }, []);

    const fetchBillingData = async () => {
        try {
            setLoading(true);
            const [creditsData, transactionsData] = await Promise.all([
                billingAPI.getCredits(),
                billingAPI.getTransactions(),
            ]);
            setCredits(creditsData.credits);
            setTransactions(transactionsData.transactions || []);
            setError('');
        } catch (err) {
            setError('Failed to load billing data');
        } finally {
            setLoading(false);
        }
    };

    const handleBuyCredits = async () => {
        const amount = parseInt(buyAmount);
        if (!amount || amount <= 0) {
            setError('Please enter a valid amount');
            return;
        }

        try {
            setBuyLoading(true);
            setError('');
            await billingAPI.buyCredits(amount);
            await fetchBillingData();
            setOpenDialog(false);
            setBuyAmount('100');
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to buy credits');
        } finally {
            setBuyLoading(false);
        }
    };

    const creditPackages = pricingPlans;

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
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
                Billing & Credits
            </Typography>

            <Grid container spacing={3}>
                {error && (
                    <Grid item xs={12}>
                        <Alert severity="error">{error}</Alert>
                    </Grid>
                )}

                {/* Current Balance */}
                <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                        <CardContent>
                            <Box display="flex" justifyContent="space-between" alignItems="center">
                                <Box>
                                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                                        Available Credits
                                    </Typography>
                                    <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                                        {credits}
                                    </Typography>
                                </Box>
                                <CreditCardIcon sx={{ fontSize: 48, opacity: 0.8 }} />
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Pricing Plans */}
                <Grid item xs={12}>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LocalOfferIcon /> Choose Your Plan
                    </Typography>
                    <Grid container spacing={3}>
                        {pricingPlans.map((plan) => (
                            <Grid item xs={12} sm={6} md={3} key={plan.id}>
                                <Card
                                    sx={{
                                        height: '100%',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        position: 'relative',
                                        border: `2px solid ${plan.borderColor}`,
                                        bgcolor: plan.color,
                                        cursor: 'pointer',
                                        transition: 'all 0.3s ease-in-out',
                                        transform: plan.recommended ? 'scale(1.05)' : 'scale(1)',
                                        boxShadow: plan.recommended ? 4 : 1,
                                        '&:hover': {
                                            transform: plan.recommended ? 'scale(1.08)' : 'scale(1.03)',
                                            boxShadow: 5,
                                        },
                                    }}
                                >
                                    {plan.badge && (
                                        <Box
                                            sx={{
                                                position: 'absolute',
                                                top: -12,
                                                right: 15,
                                                bgcolor: plan.borderColor,
                                                color: 'white',
                                                px: 2,
                                                py: 0.5,
                                                borderRadius: 1,
                                                fontSize: '0.75rem',
                                                fontWeight: 'bold',
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: 0.5,
                                            }}
                                        >
                                            {plan.badge === 'POPULAR' && <StarIcon sx={{ fontSize: '1rem' }} />}
                                            {plan.badge === 'BEST VALUE' && <TrendingUpIcon sx={{ fontSize: '1rem' }} />}
                                            {plan.badge === 'SAVE 40%' && <LocalOfferIcon sx={{ fontSize: '1rem' }} />}
                                            {plan.badge}
                                        </Box>
                                    )}

                                    <CardContent sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, pt: 3 }}>
                                        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                                            {plan.name}
                                        </Typography>

                                        <Box sx={{ mb: 2 }}>
                                            <Typography variant="h4" sx={{ fontWeight: 'bold', color: plan.borderColor }}>
                                                {plan.price}
                                            </Typography>
                                            <Typography variant="caption" color="textSecondary">
                                                {plan.pricePerCredit} per credit
                                            </Typography>
                                        </Box>

                                        <Divider sx={{ my: 1.5 }} />

                                        <List sx={{ py: 0, mb: 2, flex: 1 }}>
                                            {plan.features.map((feature, idx) => (
                                                <ListItem key={idx} sx={{ py: 0.5, px: 0 }}>
                                                    <ListItemIcon sx={{ minWidth: 32 }}>
                                                        <CheckCircleIcon
                                                            sx={{ fontSize: '1.2rem', color: plan.borderColor }}
                                                        />
                                                    </ListItemIcon>
                                                    <ListItemText
                                                        primary={feature}
                                                        primaryTypographyProps={{
                                                            variant: 'body2',
                                                            sx: { fontSize: '0.875rem' },
                                                        }}
                                                    />
                                                </ListItem>
                                            ))}
                                        </List>

                                        <Button
                                            variant={plan.recommended ? 'contained' : 'outlined'}
                                            sx={{
                                                bgcolor: plan.recommended ? plan.borderColor : 'transparent',
                                                color: plan.recommended ? 'white' : plan.borderColor,
                                                borderColor: plan.borderColor,
                                                '&:hover': {
                                                    bgcolor: plan.borderColor,
                                                    color: 'white',
                                                },
                                            }}
                                            fullWidth
                                            size="small"
                                            onClick={() => {
                                                setBuyAmount(plan.credits.toString());
                                                setSelectedPlan(plan.id);
                                                setOpenDialog(true);
                                            }}
                                        >
                                            Buy Now
                                        </Button>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>

                {/* Transaction History */}
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                                Transaction History
                            </Typography>

                            {transactions.length === 0 ? (
                                <Typography variant="body2" color="textSecondary" sx={{ textAlign: 'center', py: 3 }}>
                                    No transactions yet
                                </Typography>
                            ) : (
                                <TableContainer>
                                    <Table>
                                        <TableHead>
                                            <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                                                <TableCell sx={{ fontWeight: 'bold' }}>Date</TableCell>
                                                <TableCell sx={{ fontWeight: 'bold' }}>Type</TableCell>
                                                <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
                                                <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                                                    Amount
                                                </TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {transactions.map((transaction, idx) => (
                                                <TableRow key={idx}>
                                                    <TableCell>
                                                        {new Date(transaction.created_at).toLocaleDateString()}
                                                    </TableCell>
                                                    <TableCell>
                                                        <Box
                                                            component="span"
                                                            sx={{
                                                                bgcolor:
                                                                    transaction.type === 'credit'
                                                                        ? '#c8e6c9'
                                                                        : '#ffcccc',
                                                                color:
                                                                    transaction.type === 'credit'
                                                                        ? '#2e7d32'
                                                                        : '#c62828',
                                                                px: 2,
                                                                py: 0.5,
                                                                borderRadius: 1,
                                                                textTransform: 'capitalize',
                                                                fontWeight: 'bold',
                                                            }}
                                                        >
                                                            {transaction.type}
                                                        </Box>
                                                    </TableCell>
                                                    <TableCell>{transaction.description}</TableCell>
                                                    <TableCell align="right">
                                                        <Typography
                                                            sx={{
                                                                color:
                                                                    transaction.type === 'credit'
                                                                        ? '#4caf50'
                                                                        : '#f44336',
                                                                fontWeight: 'bold',
                                                            }}
                                                        >
                                                            {transaction.type === 'credit' ? '+' : '-'}
                                                            {transaction.amount}
                                                        </Typography>
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                {/* Pricing Breakdown */}
                <Grid item xs={12}>
                    <Card sx={{ bgcolor: '#fafafa', border: '1px solid #e0e0e0' }}>
                        <CardContent>
                            <Typography variant="h6" sx={{ mb: 3, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
                                <TrendingUpIcon /> Credit Usage & Pricing
                            </Typography>
                            <Grid container spacing={3}>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Paper sx={{ p: 2, bgcolor: '#E3F2FD', borderLeft: '4px solid #2196F3' }}>
                                        <Typography variant="body2" color="textSecondary" sx={{ mb: 0.5 }}>
                                            Parse Resume
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#2196F3' }}>
                                            5 Credits
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            ₹2.50 - ₹2.00 per parse
                                        </Typography>
                                    </Paper>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Paper sx={{ p: 2, bgcolor: '#FCE4EC', borderLeft: '4px solid #E91E63' }}>
                                        <Typography variant="body2" color="textSecondary" sx={{ mb: 0.5 }}>
                                            Parse Job Description
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#E91E63' }}>
                                            3 Credits
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            ₹1.50 - ₹1.20 per parse
                                        </Typography>
                                    </Paper>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Paper sx={{ p: 2, bgcolor: '#F3E5F5', borderLeft: '4px solid #9C27B0' }}>
                                        <Typography variant="body2" color="textSecondary" sx={{ mb: 0.5 }}>
                                            Match Candidate
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#9C27B0' }}>
                                            5 Credits
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            ₹2.50 - ₹2.00 per match
                                        </Typography>
                                    </Paper>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Paper sx={{ p: 2, bgcolor: '#E8F5E9', borderLeft: '4px solid #4CAF50' }}>
                                        <Typography variant="body2" color="textSecondary" sx={{ mb: 0.5 }}>
                                            Total Cost Example
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#4CAF50' }}>
                                            13 Credits
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            Full candidate evaluation
                                        </Typography>
                                    </Paper>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Buy Credits Dialog */}
            <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
                <Box sx={{ p: 3 }}>
                    {selectedPlan && pricingPlans.find(p => p.id === selectedPlan) ? (
                        <>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                    {pricingPlans.find(p => p.id === selectedPlan)?.name} Plan
                                </Typography>
                                <Chip label="SECURE" size="small" color="success" variant="outlined" />
                            </Box>
                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                                Confirm your purchase of {buyAmount} credits
                            </Typography>

                            <Paper sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={6}>
                                        <Typography variant="body2" color="textSecondary">
                                            Credits
                                        </Typography>
                                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                            {buyAmount}
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography variant="body2" color="textSecondary" sx={{ textAlign: 'right' }}>
                                            Price
                                        </Typography>
                                        <Typography variant="h6" sx={{ fontWeight: 'bold', textAlign: 'right' }}>
                                            {pricingPlans.find(p => p.id === selectedPlan)?.price}
                                        </Typography>
                                    </Grid>
                                </Grid>
                            </Paper>

                            <Alert severity="info" sx={{ mb: 2 }}>
                                You'll have {parseInt(credits) + parseInt(buyAmount)} total credits after purchase
                            </Alert>
                        </>
                    ) : (
                        <>
                            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                                Buy Credits
                            </Typography>

                            <TextField
                                fullWidth
                                type="number"
                                label="Number of Credits"
                                value={buyAmount}
                                onChange={(e) => setBuyAmount(e.target.value)}
                                sx={{ my: 2 }}
                                disabled={buyLoading}
                            />

                            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                                You will receive approximately ₹{Math.round(parseInt(buyAmount) * 0.5)} credit for {buyAmount}
                                credits
                            </Typography>
                        </>
                    )}

                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button
                            fullWidth
                            variant="outlined"
                            onClick={() => {
                                setOpenDialog(false);
                                setSelectedPlan(null);
                            }}
                            disabled={buyLoading}
                        >
                            Cancel
                        </Button>
                        <Button
                            fullWidth
                            variant="contained"
                            color="primary"
                            onClick={handleBuyCredits}
                            disabled={buyLoading}
                        >
                            {buyLoading ? <CircularProgress size={24} /> : 'Confirm Purchase'}
                        </Button>
                    </Box>
                </Box>
            </Dialog>
        </Container>
    );
};

export default Billing;
