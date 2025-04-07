# Duke Chatbot

An AI-powered chatbot for Duke University that helps students, faculty, and staff access information about Duke programs, events, and resources.

## Features

- Interactive chat interface
- Integration with Duke APIs and websites
- Tools for accessing information about the AI MEng program
- Event discovery for Duke-related activities

## Project Structure

- `backend/`: Python Flask backend with agent implementation
- `frontend/`: React frontend with chat interface
- `deployment/`: Docker and cloud deployment configurations

## Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Cloud Platform account (for Vertex AI)

### Environment Variables
Copy the `.env.example` file to `.env` and fill in required API keys.

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Deployment
See the `deployment/` directory for Docker and Cloud Build configurations.
