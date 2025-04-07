import React, { useState } from 'react';

const ThinkingProcess = ({ thinking }) => {
  const [expanded, setExpanded] = useState(false);
  
  // If thinking is empty, don't render
  if (!thinking) return null;
  
  // Truncate thinking text if not expanded
  const displayText = expanded ? thinking : `${thinking.substring(0, 150)}${thinking.length > 150 ? '...' : ''}`;
  
  return (
    <div className="mb-4 border border-gray-200 rounded-lg p-2 bg-gray-50">
      <div className="flex items-center justify-between mb-1">
        <div className="text-sm font-semibold text-gray-600">Thinking Process:</div>
        {thinking.length > 150 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-blue-500 hover:text-blue-700"
          >
            {expanded ? 'Show Less' : 'Show More'}
          </button>
        )}
      </div>
      <div className="text-xs text-gray-600 whitespace-pre-wrap font-mono">
        {displayText}
      </div>
    </div>
  );
};

export default ThinkingProcess;
