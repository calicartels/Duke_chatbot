import React from 'react';
import { motion } from 'framer-motion';

function ThinkingProcess({ thinking }) {
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      className="mt-2 bg-slate-50 border border-slate-200 p-4 rounded-lg text-sm"
    >
      <h4 className="font-medium text-slate-700 mb-2 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
        </svg>
        Agent Thinking Process
      </h4>
      <div className="text-slate-600 leading-relaxed whitespace-pre-wrap">
        {thinking}
      </div>
    </motion.div>
  );
}

export default ThinkingProcess;