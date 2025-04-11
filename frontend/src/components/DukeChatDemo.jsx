import React, { useState } from 'react';
import { MessageCircle, Send, Info, ChevronDown, ChevronUp, X } from 'lucide-react';

const EvaluationBadge = ({ label, score }) => {
  // Get color based on score
  const getColor = (score) => {
    if (score >= 8) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 6) return 'bg-blue-100 text-blue-800 border-blue-200';
    if (score >= 4) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-red-100 text-red-800 border-red-200';
  };

  return (
    <div className={`text-xs px-2 py-1 rounded-full border ${getColor(score)}`}>
      {label}: {score}/10
    </div>
  );
};

const ThinkingProcess = ({ thinking }) => {
  return (
    <div className="mt-2 bg-slate-50 border border-slate-200 p-4 rounded-lg text-sm">
      <h4 className="font-medium text-slate-700 mb-2 flex items-center">
        <Info className="h-4 w-4 mr-1 text-blue-500" />
        Agent Thinking Process
      </h4>
      <div className="text-slate-600 leading-relaxed whitespace-pre-wrap">
        {thinking}
      </div>
    </div>
  );
};

const Message = ({ message, showThinking }) => {
  const [viewThinking, setViewThinking] = useState(false);
  const isUserMessage = message.role === 'user';
  
  return (
    <div className={`mb-6 ${isUserMessage ? 'flex justify-end' : 'flex justify-start'}`}>
      <div className="flex items-start gap-3 max-w-3xl">
        {!isUserMessage && (
          <div className="flex-shrink-0">
            <div className="bg-blue-700 rounded-full h-8 w-8 flex items-center justify-center text-white font-medium">
              D
            </div>
          </div>
        )}
        
        <div className={`flex-1 ${isUserMessage ? 'ml-auto' : 'mr-auto'}`}>
          <div className={`px-4 py-3 rounded-xl ${
            isUserMessage 
              ? 'bg-blue-600 text-white' 
              : 'bg-white border border-slate-200 shadow-sm'
          }`}>
            <div className="prose prose-blue max-w-none">
              {message.content}
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
                <EvaluationBadge 
                  label="Clarity" 
                  score={message.evaluation.clarity} 
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
                  <ChevronUp className="h-3 w-3 mr-1" />
                ) : (
                  <ChevronDown className="h-3 w-3 mr-1" />
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
    </div>
  );
};

const DukeChatDemo = ({ messages, loading, onSendMessage, showThinking, onToggleThinking }) => {
  const [inputText, setInputText] = useState('');
  const [showHelp, setShowHelp] = useState(false);

  const handleSendMessage = () => {
    if (!inputText.trim() || loading) return;
    onSendMessage(inputText);
    setInputText('');
  };

  return (
    <div className="flex flex-col h-screen w-full max-w-4xl mx-auto bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-700 text-white shadow-lg px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 bg-white rounded-full flex items-center justify-center">
              <div className="h-8 w-8 bg-blue-900 rounded-full flex items-center justify-center text-white font-bold">D</div>
            </div>
            <div>
              <h1 className="text-xl font-bold">Duke University Assistant</h1>
              <p className="text-blue-200 text-sm">AI-powered with Agentic Search</p>
            </div>
          </div>
          
          <div className="flex items-center">
            <div className="flex items-center mr-4">
              <button 
                onClick={onToggleThinking}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${showThinking ? 'bg-blue-500' : 'bg-gray-600'}`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${showThinking ? 'translate-x-6' : 'translate-x-1'}`}
                />
              </button>
              <span className="ml-2 text-sm text-blue-100">Show Agent Thinking</span>
            </div>
            
            <button 
              onClick={() => setShowHelp(!showHelp)}
              className="bg-blue-800 hover:bg-blue-900 rounded-full px-4 py-1.5 text-sm font-medium"
            >
              Help
            </button>
          </div>
        </div>
      </header>
      
      {/* Help Modal */}
      {showHelp && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10 p-4">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-blue-900">About Duke Assistant</h3>
              <button onClick={() => setShowHelp(false)} className="text-gray-500 hover:text-gray-700">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="space-y-4 text-gray-700">
              <p><strong>Welcome to the Duke University Assistant!</strong></p>
              <p>This chatbot uses an agentic search approach with the Gemini model to answer questions about Duke University.</p>
              <p>You can ask about:</p>
              <ul className="list-disc pl-5">
                <li>The AI MEng program details</li>
                <li>Campus events and activities</li>
                <li>General information about Duke</li>
                <li>Admissions information</li>
              </ul>
              <p>Toggle the "Show Agent Thinking" switch to see how the AI reasons about your questions!</p>
            </div>
            <button 
              onClick={() => setShowHelp(false)}
              className="mt-6 w-full bg-blue-700 hover:bg-blue-800 text-white py-2 rounded-lg"
            >
              Got it!
            </button>
          </div>
        </div>
      )}
      
      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="space-y-6">
          {messages.map((message) => (
            <Message 
              key={message.id} 
              message={message} 
              showThinking={showThinking}
            />
          ))}
          
          {loading && (
            <div className="flex items-start gap-3 max-w-3xl">
              <div className="flex-shrink-0">
                <div className="bg-blue-700 rounded-full h-8 w-8 flex items-center justify-center text-white font-medium">
                  D
                </div>
              </div>
              
              <div className="flex space-x-2 items-center bg-slate-100 px-4 py-2 rounded-xl">
                <div className="flex space-x-1">
                  <div className="bg-blue-700 rounded-full h-2 w-2 animate-ping"></div>
                  <div className="bg-blue-700 rounded-full h-2 w-2 animate-ping delay-100"></div>
                  <div className="bg-blue-700 rounded-full h-2 w-2 animate-ping delay-200"></div>
                </div>
                <span className="text-sm text-slate-500">Thinking...</span>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Input Area */}
      <div className="border-t border-slate-200 bg-slate-50 p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask about Duke University..."
            className="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-700 focus:border-transparent shadow-sm"
            disabled={loading}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button
            onClick={handleSendMessage}
            className="bg-blue-700 text-white px-4 py-3 rounded-xl hover:bg-blue-800 
            transition-colors duration-300 font-medium flex items-center justify-center shadow-md disabled:bg-slate-400"
            disabled={loading || !inputText.trim()}
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
        <div className="mt-2 text-xs text-center text-slate-500 flex items-center justify-center">
          <MessageCircle className="h-3 w-3 mr-1" />
          Powered by Gemini & LangGraph
        </div>
      </div>
    </div>
  );
};

export default DukeChatDemo;