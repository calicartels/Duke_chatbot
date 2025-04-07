import React, { useRef, useEffect } from 'react';
import Message from './Message';
import MessageInput from './MessageInput';
import ThinkingProcess from './ThinkingProcess';
import ToolEvaluation from './ToolEvaluation';
import { useChat } from '../hooks/useChat';

const ChatInterface = ({ 
  messages, 
  setMessages,
  isThinking,
  setIsThinking,
  thinkingProcess,
  setThinkingProcess,
  toolCalls,
  setToolCalls
}) => {
  const chatRef = useRef(null);
  const { sendMessage } = useChat({
    setMessages,
    setIsThinking,
    setThinkingProcess,
    setToolCalls
  });

  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, isThinking]);

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg overflow-hidden">
      <div 
        ref={chatRef}
        className="flex-grow p-4 overflow-y-auto"
        style={{ maxHeight: 'calc(100vh - 240px)' }}
      >
        {messages.map((message, index) => (
          <Message
            key={index}
            message={message}
          />
        ))}
        
        {isThinking && (
          <div className="mt-4">
            <div className="flex items-center mb-2">
              <div className="mr-2 bg-duke-navy text-white rounded-full p-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <div className="text-gray-600 font-medium">Duke Chatbot is thinking...</div>
            </div>
            
            {thinkingProcess && <ThinkingProcess thinking={thinkingProcess} />}
            
            {toolCalls.length > 0 && <ToolEvaluation tools={toolCalls} />}
          </div>
        )}
      </div>
      
      <div className="border-t p-4">
        <MessageInput onSendMessage={sendMessage} disabled={isThinking} />
      </div>
    </div>
  );
};

export default ChatInterface;
