import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Box,
    Button,
    Card,
    CardContent,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Dialog,
    TextField,
    Typography,
    Alert,
    CircularProgress,
    IconButton,
    Chip,
    Paper,
} from '@mui/material';
import axios from 'axios';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';

const AdminManagement = () => {
    const navigate = useNavigate();
    const [admins, setAdmins] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [editingAdmin, setEditingAdmin] = useState(null);
    const [formData, setFormData] = useState({ email: '', password: '' });
    const [saving, setSaving] = useState(false);

    const token = localStorage.getItem('token');

    useEffect(() => {
        fetchAdmins();
    }, []);

    const fetchAdmins = async () => {
        try {
            setLoading(true);
            const response = await axios.get('http://localhost:8000/api/v1/admin/list', {
                headers: { Authorization: `Bearer ${token}` },
            });
            setAdmins(response.data);
            setError('');
        } catch (err) {
            setError('Failed to load admins');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleOpenDialog = (admin = null) => {
        if (admin) {
            setEditingAdmin(admin);
            setFormData({ email: admin.email, password: '' });
        } else {
            setEditingAdmin(null);
            setFormData({ email: '', password: '' });
        }
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setEditingAdmin(null);
        setFormData({ email: '', password: '' });
    };

    const handleSaveAdmin = async () => {
        if (!formData.email) {
            setError('Email is required');
            return;
        }

        if (!editingAdmin && !formData.password) {
            setError('Password is required for new admins');
            return;
        }

        try {
            setSaving(true);
            setError('');

            if (editingAdmin) {
                // Update existing admin
                await axios.put(
                    `http://localhost:8000/api/v1/admin/${editingAdmin.id}`,
                    {
                        email: formData.email,
                        password: formData.password || undefined,
                    },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                setError('Admin updated successfully');
            } else {
                // Create new admin
                await axios.post(
                    'http://localhost:8000/api/v1/admin/create',
                    {
                        email: formData.email,
                        password: formData.password,
                    },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                setError('Admin created successfully');
            }

            handleCloseDialog();
            await fetchAdmins();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to save admin');
        } finally {
            setSaving(false);
        }
    };

    const handleDeleteAdmin = async (adminId) => {
        if (!window.confirm('Are you sure you want to delete this admin? This cannot be undone.')) {
            return;
        }

        try {
            await axios.delete(`http://localhost:8000/api/v1/admin/${adminId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setError('Admin deleted successfully');
            await fetchAdmins();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to delete admin');
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
            {/* Header */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/admin-dashboard')}
                    sx={{ mb: 2 }}
                >
                    Back to Dashboard
                </Button>
            </Box>

            <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                Admin Management
            </Typography>
            <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
                Create, edit, and manage admin accounts
            </Typography>

            {/* Error/Success Alert */}
            {error && (
                <Alert
                    severity={error.includes('success') ? 'success' : 'error'}
                    onClose={() => setError('')}
                    sx={{ mb: 2 }}
                >
                    {error}
                </Alert>
            )}

            {/* Add Admin Button */}
            <Box sx={{ mb: 3 }}>
                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpenDialog()}
                    sx={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        py: 1,
                    }}
                >
                    Create New Admin
                </Button>
            </Box>

            {/* Stats Card */}
            <Paper sx={{ p: 2, mb: 3, bgcolor: '#f5f5f5' }}>
                <Typography variant="body2" color="textSecondary">
                    <strong>Total Admins:</strong> {admins.length}
                </Typography>
            </Paper>

            {/* Admins Table */}
            {admins.length > 0 ? (
                <TableContainer component={Card}>
                    <Table>
                        <TableHead>
                            <TableRow sx={{ bgcolor: '#f5f5f5' }}>
                                <TableCell sx={{ fontWeight: 'bold' }}>Email</TableCell>
                                <TableCell sx={{ fontWeight: 'bold' }}>Created Date</TableCell>
                                <TableCell sx={{ fontWeight: 'bold' }} align="right">
                                    Actions
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {admins.map((admin) => (
                                <TableRow key={admin.id} hover>
                                    <TableCell>
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                                {admin.email}
                                            </Typography>
                                            {admin.id === JSON.parse(atob(localStorage.getItem('token')?.split('.')[1] || '{}')).id && (
                                                <Chip label="YOU" size="small" color="primary" variant="outlined" />
                                            )}
                                        </Box>
                                    </TableCell>
                                    <TableCell>
                                        {new Date(admin.created_at).toLocaleDateString()}
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton
                                            size="small"
                                            onClick={() => handleOpenDialog(admin)}
                                            color="primary"
                                            title="Edit admin"
                                        >
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton
                                            size="small"
                                            onClick={() => handleDeleteAdmin(admin.id)}
                                            color="error"
                                            title="Delete admin"
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            ) : (
                <Card>
                    <CardContent sx={{ textAlign: 'center', py: 3 }}>
                        <Typography color="textSecondary">
                            No admins found. Create your first admin.
                        </Typography>
                    </CardContent>
                </Card>
            )}

            {/* Create/Edit Admin Dialog */}
            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
                <Box sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                        {editingAdmin ? 'Edit Admin' : 'Create New Admin'}
                    </Typography>

                    <TextField
                        fullWidth
                        label="Email Address"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        margin="normal"
                        disabled={saving}
                        required
                    />

                    <TextField
                        fullWidth
                        label="Password"
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        margin="normal"
                        disabled={saving}
                        required={!editingAdmin}
                        placeholder={editingAdmin ? 'Leave blank to keep current password' : ''}
                    />

                    <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
                        <Button
                            fullWidth
                            variant="outlined"
                            onClick={handleCloseDialog}
                            disabled={saving}
                        >
                            Cancel
                        </Button>
                        <Button
                            fullWidth
                            variant="contained"
                            onClick={handleSaveAdmin}
                            disabled={saving}
                        >
                            {saving ? <CircularProgress size={24} /> : editingAdmin ? 'Update' : 'Create'}
                        </Button>
                    </Box>
                </Box>
            </Dialog>
        </Container>
    );
};

export default AdminManagement;
