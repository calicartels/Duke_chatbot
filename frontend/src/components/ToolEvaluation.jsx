import React, { useState } from 'react';

const ToolEvaluation = ({ tools }) => {
  const [expandedTool, setExpandedTool] = useState(null);
  
  if (!tools || tools.length === 0) return null;
  
  return (
    <div className="mb-4 border border-gray-200 rounded-lg p-2 bg-gray-50">
      <div className="text-sm font-semibold text-gray-600 mb-2">Tools Used:</div>
      
      <div className="space-y-2">
        {tools.map((tool, index) => (
          <div key={index} className="border rounded-md p-1.5 bg-white">
            <div 
              className="flex items-center justify-between cursor-pointer"
              onClick={() => setExpandedTool(expandedTool === index ? null : index)}
            >
              <div className="flex items-center">
                <div className="h-4 w-4 rounded-full bg-green-500 flex items-center justify-center text-white mr-2">
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <span className="text-xs font-medium">{tool.name || 'Unknown Tool'}</span>
              </div>
              <svg 
                className={`w-4 h-4 text-gray-400 transform transition-transform ${expandedTool === index ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
              </svg>
            </div>
            
            {expandedTool === index && (
              <div className="mt-2 text-xs text-gray-600 border-t pt-2">
                <div className="font-mono whitespace-pre-wrap overflow-x-auto">
                  {JSON.stringify(tool.parameters || {}, null, 2)}
                </div>
                {tool.result && (
                  <div className="mt-1 pt-1 border-t">
                    <div className="font-semibold mb-0.5">Result:</div>
                    <div className="font-mono whitespace-pre-wrap overflow-x-auto">
                      {typeof tool.result === 'string' 
                        ? tool.result 
                        : JSON.stringify(tool.result, null, 2)}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ToolEvaluation;
