import { useState, useCallback } from 'react';
import { sendChatMessage } from '../services/api';

export const useChat = ({
  setMessages,
  setIsThinking,
  setThinkingProcess,
  setToolCalls
}) => {
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (messageText) => {
    if (!messageText.trim()) return;
    
    // Add user message to chat
    setMessages(prev => [
      ...prev,
      { type: 'user', content: messageText }
    ]);
    
    // Set thinking state
    setIsThinking(true);
    setThinkingProcess('');
    setToolCalls([]);
    
    try {
      // Create history from previous messages (this could be expanded)
      const history = [];
      
      console.log('Sending message:', messageText);
      // Send to API
      const response = await sendChatMessage(messageText, history);
      console.log('Received response:', response);
      
      // Show thinking process if available
      if (response.thinking) {
        setThinkingProcess(response.thinking);
      }
      
      // Show tool calls if available
      if (response.tool_calls && response.tool_calls.length > 0) {
        setToolCalls(response.tool_calls);
      }
      
      // Add bot response to chat after a short delay to show thinking process
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          { type: 'bot', content: response.message || 'No response from the server' }
        ]);
        setIsThinking(false);
      }, 500);  // Adjust delay as needed
      
    } catch (err) {
      console.error('Error sending message:', err);
      const errorMessage = err.response?.data?.error || err.message || 'Error communicating with the chat service';
      setError(errorMessage);
      
      // Add error message to chat
      setMessages(prev => [
        ...prev,
        { 
          type: 'system', 
          content: `Sorry, there was an error: ${errorMessage}. Please try again later.`
        }
      ]);
      
      setIsThinking(false);
    }
  }, [setMessages, setIsThinking, setThinkingProcess, setToolCalls]);

  return {
    sendMessage,
    error
  };
};
