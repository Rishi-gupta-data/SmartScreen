import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Check if user is already logged in on mount
    useEffect(() => {
        const savedToken = localStorage.getItem('access_token');
        if (savedToken) {
            setToken(savedToken);
            validateToken(savedToken);
        } else {
            setLoading(false);
        }
    }, []);

    const validateToken = async (tokenToValidate) => {
        try {
            const response = await api.get('/credits/');
            setUser(response.data);
            setError(null);
        } catch (err) {
            localStorage.removeItem('access_token');
            setToken(null);
            setUser(null);
            setError('Session expired. Please login again.');
        } finally {
            setLoading(false);
        }
    };

    const signup = async (email, password) => {
        try {
            setLoading(true);
            setError(null);
            const response = await api.post('/auth/signup', { email, password });
            const accessToken = response.data.access_token;
            
            // Store token
            localStorage.setItem('access_token', accessToken);
            setToken(accessToken);
            
            // Validate and fetch user data
            await validateToken(accessToken);
            return response.data;
        } catch (err) {
            const errorMsg = err.response?.data?.detail || 'Signup failed';
            setError(errorMsg);
            throw new Error(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        try {
            setLoading(true);
            setError(null);
            const response = await api.post('/auth/login', { email, password });
            const accessToken = response.data.access_token;
            
            // Store token
            localStorage.setItem('access_token', accessToken);
            setToken(accessToken);
            
            // Validate and fetch user data
            await validateToken(accessToken);
            return response.data;
        } catch (err) {
            const errorMsg = err.response?.data?.detail || 'Login failed';
            setError(errorMsg);
            throw new Error(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        setToken(null);
        setUser(null);
        setError(null);
    };

    const isAuthenticated = !!token && !!user;

    return (
        <AuthContext.Provider 
            value={{ 
                user, 
                token,
                loading, 
                error, 
                signup, 
                login, 
                logout,
                isAuthenticated 
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
