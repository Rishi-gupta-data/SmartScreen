import React from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import theme from './theme';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

// Auth Pages
import Login from './pages/Login';
import Signup from './pages/Signup';

// Protected Pages
import Dashboard from './pages/Dashboard';
import ResumeParse from './pages/ResumeParse';
import JDParse from './pages/JDParse';
import Match from './pages/Match';
import Billing from './pages/Billing';
import Transactions from './pages/Transactions';

// Admin Pages
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import AdminManagement from './pages/AdminManagement';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <AuthProvider>
                    <Routes>
                        {/* Public Routes */}
                        <Route path="/login" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/admin-login" element={<AdminLogin />} />

                        {/* Protected Routes */}
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/resume"
                            element={
                                <ProtectedRoute>
                                    <ResumeParse />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/jd"
                            element={
                                <ProtectedRoute>
                                    <JDParse />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/match"
                            element={
                                <ProtectedRoute>
                                    <Match />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/billing"
                            element={
                                <ProtectedRoute>
                                    <Billing />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/transactions"
                            element={
                                <ProtectedRoute>
                                    <Transactions />
                                </ProtectedRoute>
                            }
                        />

                        {/* Admin Routes */}
                        <Route path="/admin-dashboard" element={<AdminDashboard />} />
                        <Route path="/admin-management" element={<AdminManagement />} />

                        {/* Default Route */}
                        <Route path="/" element={<Navigate to="/dashboard" />} />
                        <Route path="*" element={<Navigate to="/dashboard" />} />
                    </Routes>
                </AuthProvider>
            </Router>
        </ThemeProvider>
    );
}

export default App;
