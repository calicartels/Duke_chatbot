import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/index.css'; // Import Tailwind styles
// Assuming you might have global styles, uncomment if needed
// import './index.css'; // Or './styles/index.css' if you have it there

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 