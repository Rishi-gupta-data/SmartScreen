import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
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
    TablePagination,
} from '@mui/material';
import { billingAPI } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const Transactions = () => {
    const navigate = useNavigate();
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    useEffect(() => {
        fetchTransactions();
    }, [page, rowsPerPage]);

    const fetchTransactions = async () => {
        try {
            setLoading(true);
            const skip = page * rowsPerPage;
            const data = await billingAPI.getTransactions(skip, rowsPerPage);
            setTransactions(data.transactions || []);
            setError('');
        } catch (err) {
            setError('Failed to load transactions');
        } finally {
            setLoading(false);
        }
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const getStatusColor = (type) => {
        if (type === 'credit') {
            return {
                bgcolor: '#c8e6c9',
                color: '#2e7d32',
            };
        } else {
            return {
                bgcolor: '#ffcccc',
                color: '#c62828',
            };
        }
    };

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
                Transaction History
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            <Card>
                <CardContent>
                    {transactions.length === 0 ? (
                        <Typography variant="body1" color="textSecondary" sx={{ textAlign: 'center', py: 4 }}>
                            No transactions yet
                        </Typography>
                    ) : (
                        <>
                            <TableContainer>
                                <Table>
                                    <TableHead>
                                        <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                                            <TableCell sx={{ fontWeight: 'bold' }}>Date & Time</TableCell>
                                            <TableCell sx={{ fontWeight: 'bold' }}>Type</TableCell>
                                            <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
                                            <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                                                Amount
                                            </TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {transactions.map((transaction, idx) => {
                                            const statusColor = getStatusColor(transaction.type);
                                            const createdAt = new Date(transaction.created_at);
                                            return (
                                                <TableRow key={idx} hover>
                                                    <TableCell>
                                                        {createdAt.toLocaleDateString()} {createdAt.toLocaleTimeString()}
                                                    </TableCell>
                                                    <TableCell>
                                                        <Box
                                                            component="span"
                                                            sx={{
                                                                ...statusColor,
                                                                px: 2,
                                                                py: 0.5,
                                                                borderRadius: 1,
                                                                textTransform: 'capitalize',
                                                                fontWeight: 'bold',
                                                                display: 'inline-block',
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
                                                                fontSize: '1.1rem',
                                                            }}
                                                        >
                                                            {transaction.type === 'credit' ? '+' : '-'}
                                                            {transaction.amount}
                                                        </Typography>
                                                    </TableCell>
                                                </TableRow>
                                            );
                                        })}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                            <TablePagination
                                rowsPerPageOptions={[10, 25, 50]}
                                component="div"
                                count={transactions.length > 0 ? transactions.length + 1 : 0}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                onPageChange={handleChangePage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                            />
                        </>
                    )}
                </CardContent>
            </Card>
        </Container>
    );
};

export default Transactions;
