import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const analyzeResume = async (formData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
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
    const response = await axios.post(`${API_BASE_URL}/analyze-bulk`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Error analyzing resumes');
  }
};