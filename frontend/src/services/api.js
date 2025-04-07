import axios from 'axios';

// Get API URL from environment variable or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Log the API URL for debugging
console.log('Using API URL:', API_URL);

/**
 * Send a chat message to the backend API
 * 
 * @param {string} message - The user's message
 * @param {Array} history - Chat history array
 * @returns {Promise<Object>} - Response with message, thinking, and tool_calls
 */
export const sendChatMessage = async (message, history = []) => {
  try {
    console.log('Sending message to API:', message);
    
    const response = await apiClient.post('/chat', {
      message,
      history,
    });
    
    console.log('API response:', response.data);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    console.error('Error details:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Check if the backend API is healthy
 * 
 * @returns {Promise<boolean>} - True if API is healthy
 */
export const checkApiHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    console.log('Health check response:', response.status);
    return response.status === 200;
  } catch (error) {
    console.error('Health check error:', error);
    return false;
  }
};
