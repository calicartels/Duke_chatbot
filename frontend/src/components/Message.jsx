import React from 'react';

const Message = ({ message }) => {
  const { type, content } = message;
  
  // Render different message types with appropriate styling
  switch (type) {
    case 'user':
      return (
        <div className="flex justify-end mb-4">
          <div className="bg-blue-100 rounded-lg py-2 px-4 max-w-[80%]">
            <p className="text-gray-800">{content}</p>
          </div>
        </div>
      );
      
    case 'bot':
      return (
        <div className="flex mb-4">
          <div className="mr-2 bg-duke-navy text-white rounded-full p-2 self-start">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <div className="bg-gray-100 rounded-lg py-2 px-4 max-w-[80%]">
            <p className="text-gray-800 whitespace-pre-wrap">{content}</p>
          </div>
        </div>
      );
      
    case 'system':
      return (
        <div className="flex justify-center mb-4">
          <div className="bg-gray-200 rounded-lg py-2 px-4 max-w-[90%] text-center">
            <p className="text-gray-600 text-sm">{content}</p>
          </div>
        </div>
      );
      
    default:
      return null;
  }
};

export default Message;
