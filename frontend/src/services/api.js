import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchResponse = async (message, conversationId) => {
  try {
    const response = await api.post('/api/chat', {
      message,
      conversationId,
    });
    
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const fetchGeneralInfo = async (query) => {
  try {
    const response = await api.post('/api/general', {
      query,
    });
    
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};