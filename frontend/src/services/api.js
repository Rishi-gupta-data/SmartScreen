import axios from 'axios';

// Backend API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// ===== Authentication =====
export const signup = async (email, password) => {
  const response = await api.post('/auth/signup', { email, password });
  return response.data;
};

export const login = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

// ===== Resume Operations =====
export const parseResume = async (resumeText, filename = null) => {
  const response = await api.post('/resume/parse', {
    resume_text: resumeText,
    filename: filename,
  });
  return response.data;
};

// ===== Job Description Operations =====
export const parseJD = async (jdText, filename = null) => {
  const response = await api.post('/jd/parse', {
    jd_text: jdText,
    filename: filename,
  });
  return response.data;
};

// ===== Matching =====
export const matchResumeToJD = async (resumeText, jdText) => {
  const response = await api.post('/match/', {
    resume_text: resumeText,
    jd_text: jdText,
  });
  return response.data;
};

// ===== Billing & Credits =====
export const getCredits = async () => {
  const response = await api.get('/billing/credits');
  return response.data;
};

export const buyCredits = async (amount) => {
  const response = await api.post('/billing/buy-credits', { amount });
  return response.data;
};

export const getTransactions = async (skip = 0, limit = 50) => {
  const response = await api.get('/billing/transactions', {
    params: { skip, limit },
  });
  return response.data;
};

// ===== Legacy API calls (kept for backward compatibility) =====
export const analyzeResume = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error analyzing resume');
  }
};

export const analyzeBulkResumes = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/bulk-analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error analyzing resumes');
  }
};