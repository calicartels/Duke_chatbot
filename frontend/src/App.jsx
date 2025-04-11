import React, { useState, useEffect, useRef } from 'react';
import { fetchResponse } from './services/api';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header'; // Optional: if you want to use the Header component

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [showThinking, setShowThinking] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Generate a random conversation ID
    setConversationId(`conv-${Date.now()}`);
    
    // Add welcome message
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: "Hi there! I'm the Duke University Assistant. Ask me anything about Duke University, academic programs, campus life, or upcoming events!",
        thinking: null,
      }
    ]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (messageText) => {
    if (!messageText.trim() || loading) return;

    // Add user message to the UI
    const userMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: messageText,
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      // Call the API
      const response = await fetchResponse(messageText, conversationId);

      // Add the response to the UI
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response || "I'm sorry, I couldn't process that request.",
        thinking: response.thinking_explanation || null,
        toolResults: response.tool_results || null,
        evaluation: response.evaluation || null,
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: "I'm sorry, there was an error processing your request. Please try again later.",
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const toggleThinking = () => {
    setShowThinking(!showThinking);
  };

  // Now use ChatInterface instead of DukeChatDemo
  return (
    <div className="flex flex-col min-h-screen">
      <Header onToggleThinking={toggleThinking} showThinking={showThinking} />
      <div className="flex-1 container mx-auto px-4 py-6">
        <ChatInterface 
          messages={messages}
          onSendMessage={sendMessage}
          loading={loading}
          showThinking={showThinking}
        />
      </div>
    </div>
  );
}

export default App;