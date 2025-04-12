import React, { useState, useRef, useEffect } from 'react';
import Message from './Message';
import { motion } from 'framer-motion';
import { PaperAirplaneIcon } from '@heroicons/react/24/solid';

function ChatInterface({ messages, onSendMessage, loading, showThinking }) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on load
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim() && !loading) {
      onSendMessage(inputText);
      setInputText('');
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] rounded-xl bg-white shadow-xl overflow-hidden border border-blue-100">
      <div 
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-6 py-8"
      >
        <div className="space-y-8">
          {messages.map((message) => (
            <Message 
              key={message.id} 
              message={message} 
              showThinking={showThinking}
            />
          ))}
          
          {loading && (
            <motion.div 
              className="message-container assistant-message w-fit"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center space-x-4">
                <div className="flex-shrink-0">
                  <div className="bg-duke-blue rounded-full h-10 w-10 flex items-center justify-center text-white font-medium text-lg">
                    D
                  </div>
                </div>
                
                <div className="flex space-x-3 items-center bg-slate-100 px-5 py-3 rounded-xl">
                  <div className="flex space-x-1.5">
                    <div className="animate-pulse bg-duke-blue rounded-full h-2.5 w-2.5"></div>
                    <div className="animate-pulse bg-duke-blue rounded-full h-2.5 w-2.5 delay-100"></div>
                    <div className="animate-pulse bg-duke-blue rounded-full h-2.5 w-2.5 delay-200"></div>
                  </div>
                  <span className="text-base text-slate-500">Thinking...</span>
                </div>
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      <div className="border-t border-slate-200 bg-slate-50 p-5">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <input
            ref={inputRef}
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask about Duke University..."
            className="flex-1 px-5 py-4 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-duke-blue focus:border-transparent shadow-sm text-base"
            disabled={loading}
          />
          <button
            type="submit"
            className="bg-duke-blue text-white px-5 py-4 rounded-xl hover:bg-blue-800 
            transition-colors duration-300 font-medium flex items-center justify-center shadow-md disabled:bg-slate-400 h-14 w-14"
            disabled={loading || !inputText.trim()}
          >
            <PaperAirplaneIcon className="h-6 w-6" />
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;