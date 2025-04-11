import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import ThinkingProcess from './ThinkingProcess';
import EvaluationBadge from './EvaluationBadge';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

function Message({ message, showThinking }) {
  const [viewThinking, setViewThinking] = useState(false);
  
  const isUserMessage = message.role === 'user';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`message-container ${isUserMessage ? 'user-message' : 'assistant-message'}`}
    >
      <div className="flex items-start gap-3">
        {!isUserMessage && (
          <div className="flex-shrink-0">
            <div className="bg-duke-blue rounded-full h-8 w-8 flex items-center justify-center text-white font-medium">
              D
            </div>
          </div>
        )}
        
        <div className={`flex-1 ${isUserMessage ? 'ml-auto' : 'mr-auto'}`}>
          <div className={`px-4 py-3 rounded-xl ${
            isUserMessage 
              ? 'bg-blue-600 text-white ml-auto' 
              : 'bg-white border border-slate-200 shadow-sm'
          }`}>
            <div className="prose prose-blue max-w-none">
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>
            
            {!isUserMessage && message.evaluation && (
              <div className="mt-2 flex flex-wrap gap-2">
                <EvaluationBadge 
                  label="Accuracy" 
                  score={message.evaluation.accuracy} 
                />
                <EvaluationBadge 
                  label="Relevance" 
                  score={message.evaluation.relevance} 
                />
                <EvaluationBadge 
                  label="Completeness" 
                  score={message.evaluation.completeness} 
                />
              </div>
            )}
          </div>
          
          {!isUserMessage && message.thinking && showThinking && (
            <div className="mt-2">
              <button 
                onClick={() => setViewThinking(!viewThinking)}
                className="text-xs text-blue-600 hover:text-blue-800 flex items-center bg-blue-50 px-3 py-1 rounded-full"
              >
                {viewThinking ? (
                  <ChevronUpIcon className="h-3 w-3 mr-1" />
                ) : (
                  <ChevronDownIcon className="h-3 w-3 mr-1" />
                )}
                <span>{viewThinking ? 'Hide' : 'Show'} thinking process</span>
              </button>
              
              {viewThinking && <ThinkingProcess thinking={message.thinking} />}
            </div>
          )}
        </div>
        
        {isUserMessage && (
          <div className="flex-shrink-0">
            <div className="bg-blue-500 rounded-full h-8 w-8 flex items-center justify-center text-white font-medium">
              U
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default Message;