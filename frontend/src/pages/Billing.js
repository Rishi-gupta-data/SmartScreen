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
} from '@mui/material';
import { billingAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CreditCardIcon from '@mui/icons-material/CreditCard';

const Billing = () => {
    const navigate = useNavigate();
    const [credits, setCredits] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [buyAmount, setBuyAmount] = useState('100');
    const [buyLoading, setBuyLoading] = useState(false);

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

    const creditPackages = [
        { label: '100 Credits', value: 100, price: '₹50' },
        { label: '500 Credits', value: 500, price: '₹200' },
        { label: '1000 Credits', value: 1000, price: '₹350' },
        { label: '5000 Credits', value: 5000, price: '₹1500' },
    ];

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

                {/* Quick Buy Packages */}
                <Grid item xs={12}>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                        Quick Buy Packages
                    </Typography>
                    <Grid container spacing={2}>
                        {creditPackages.map((pkg) => (
                            <Grid item xs={12} sm={6} md={3} key={pkg.value}>
                                <Card
                                    sx={{
                                        cursor: 'pointer',
                                        transition: 'all 0.3s',
                                        '&:hover': {
                                            transform: 'translateY(-5px)',
                                            boxShadow: 3,
                                        },
                                    }}
                                >
                                    <CardContent sx={{ textAlign: 'center' }}>
                                        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                                            {pkg.label}
                                        </Typography>
                                        <Typography variant="h5" color="primary" sx={{ mb: 2 }}>
                                            {pkg.price}
                                        </Typography>
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            fullWidth
                                            size="small"
                                            onClick={() => {
                                                setBuyAmount(pkg.value.toString());
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

                {/* Pricing Info */}
                <Grid item xs={12}>
                    <Card sx={{ bgcolor: '#f5f5f5' }}>
                        <CardContent>
                            <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                                Credit Usage Costs
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={4}>
                                    <Box>
                                        <Typography variant="body2" color="textSecondary">
                                            Parse Resume
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                                            5 Credits
                                        </Typography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={4}>
                                    <Box>
                                        <Typography variant="body2" color="textSecondary">
                                            Parse Job Description
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                                            3 Credits
                                        </Typography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={4}>
                                    <Box>
                                        <Typography variant="body2" color="textSecondary">
                                            Match Candidate to Job
                                        </Typography>
                                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                                            5 Credits
                                        </Typography>
                                    </Box>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Buy Credits Dialog */}
            <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
                <Box sx={{ p: 3 }}>
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

                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button
                            fullWidth
                            variant="outlined"
                            onClick={() => setOpenDialog(false)}
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
