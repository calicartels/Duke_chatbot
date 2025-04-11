import React from 'react';

function EvaluationBadge({ label, score }) {
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
}

export default EvaluationBadge;