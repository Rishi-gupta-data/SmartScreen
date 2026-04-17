import axios from 'axios';

// Backend API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';  // ✅ API versioning

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL + API_VERSION,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ===== REQUEST INTERCEPTOR =====
// Add JWT token to all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ===== RESPONSE INTERCEPTOR =====
// Handle errors and token expiry
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized - token expired
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
      return Promise.reject(new Error('Session expired. Please login again.'));
    }

    // Handle other errors with detail messages
    if (error.response?.status === 400) {
      const detail = error.response.data?.detail;
      if (detail) {
        return Promise.reject(new Error(detail));
      }
    }

    return Promise.reject(error);
  }
);

// ===== Authentication API =====
export const authAPI = {
  signup: async (email, password) => {
    const response = await api.post('/auth/signup', { email, password });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
};

// ===== Resume Operations API =====
export const resumeAPI = {
  parse: async (resumeText, fileName = null) => {
    const response = await api.post('/resume/parse', {
      resume_text: resumeText,
      file_name: fileName,
    });
    return response.data;
  },

  parseFile: async (file) => {
    const formData = new FormData();
    formData.append('resume_text', ''); // Empty text (using file instead)
    formData.append('file', file);
    formData.append('file_name', file.name);

    const response = await api.post('/resume/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// ===== Job Description Operations API =====
export const jdAPI = {
  parse: async (jdText, fileName = null) => {
    const response = await api.post('/jd/parse', {
      jd_text: jdText,
      file_name: fileName,
    });
    return response.data;
  },

  parseFile: async (file) => {
    const formData = new FormData();
    formData.append('jd_text', ''); // Empty text (using file instead)
    formData.append('file', file);
    formData.append('file_name', file.name);

    const response = await api.post('/jd/parse', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

// ===== Matching Operations API =====
export const matchAPI = {
  match: async (resumeText, jdText) => {
    const response = await api.post('/match', {  // ✅ Normalized: no trailing slash
      resume_text: resumeText,
      jd_text: jdText,
    });
    return response.data;
  },
};

// ===== Billing & Credits API =====
export const billingAPI = {
  getCredits: async () => {
    const response = await api.get('/credits');  // ✅ Normalized: no trailing slash
    return response.data;
  },

  buyCredits: async (amount) => {
    const response = await api.post('/billing/buy-credits', {
      amount: amount,
    });
    return response.data;
  },

  getTransactions: async (skip = 0, limit = 50) => {
    const response = await api.get('/billing/transactions', {
      params: { skip, limit },
    });
    return response.data;
  },
};

// ===== Health Check API (not under /api/v1) =====
export const healthAPI = {
  check: async () => {
    // Health endpoint is at root, not under /api/v1
    const response = await axios.get(API_BASE_URL + '/health');
    return response.data;
  },
};

// ===== Legacy exports (backward compatibility) =====
export const signup = authAPI.signup;
export const login = authAPI.login;
export const parseResume = resumeAPI.parse;
export const parseJD = jdAPI.parse;
export const matchResumeToJD = matchAPI.match;
export const getCredits = billingAPI.getCredits;
export const buyCredits = billingAPI.buyCredits;
export const getTransactions = billingAPI.getTransactions;

export default api;