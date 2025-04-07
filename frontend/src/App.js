import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import './styles/tailwind.css';

function App() {
  const [messages, setMessages] = useState([
    {
      type: 'system',
      content: 'Welcome to Duke Chatbot! Ask me anything about Duke University, the AI MEng program, events, or other Duke resources.'
    }
  ]);
  
  const [isThinking, setIsThinking] = useState(false);
  const [thinkingProcess, setThinkingProcess] = useState('');
  const [toolCalls, setToolCalls] = useState([]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-duke-navy text-white p-4">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">Duke Chatbot</h1>
          <p className="text-sm">Powered by Duke University</p>
        </div>
      </header>
      
      <main className="flex-grow container mx-auto p-4 flex flex-col">
        <ChatInterface 
          messages={messages} 
          setMessages={setMessages}
          isThinking={isThinking}
          setIsThinking={setIsThinking}
          thinkingProcess={thinkingProcess}
          setThinkingProcess={setThinkingProcess}
          toolCalls={toolCalls}
          setToolCalls={setToolCalls}
        />
      </main>
      
      <footer className="bg-gray-200 p-4">
        <div className="container mx-auto text-center text-sm text-gray-600">
          &copy; {new Date().getFullYear()} Duke University. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

export default App;
