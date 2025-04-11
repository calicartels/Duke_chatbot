import React from 'react';
import { Switch } from '@headlessui/react';

function Header({ onToggleThinking, showThinking }) {
  return (
    <header className="bg-gradient-to-r from-duke-navy to-duke-blue text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <img src="/duke-logo.svg" alt="Duke Logo" className="h-10 w-10" />
          <div>
            <h1 className="text-xl font-bold">Duke University Assistant</h1>
            <p className="text-blue-200 text-sm">AI-powered with Agentic Search</p>
          </div>
        </div>
        
        <div className="flex items-center">
          <div className="flex items-center mr-6">
            <Switch
              checked={showThinking}
              onChange={onToggleThinking}
              className={`${
                showThinking ? 'bg-blue-500' : 'bg-gray-600'
              } relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
            >
              <span
                className={`${
                  showThinking ? 'translate-x-6' : 'translate-x-1'
                } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
              />
            </Switch>
            <span className="ml-2 text-sm text-blue-100">Show Agent Thinking</span>
          </div>
          
          <div className="relative group">
            <button className="bg-blue-700 hover:bg-blue-800 rounded-full px-4 py-1.5 text-sm font-medium transition-colors shadow-md">
              About
            </button>
            <div className="absolute right-0 w-72 mt-2 p-4 bg-white rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-10 text-gray-800">
              <h3 className="font-bold text-blue-900 mb-1">Duke Agentic Chatbot</h3>
              <p className="text-sm">
                This chatbot uses an agentic search approach with the Gemini model to answer questions about Duke University, leveraging multiple specialized search tools and an evaluation system.
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;