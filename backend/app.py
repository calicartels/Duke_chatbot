import os
import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agent modules
from backend.agent.agent_builder import build_agent

# Import tools
from backend.tools.duke_api_tool import DukeApiTool
from backend.tools.duke_website_tool import DukeWebsiteTool
from backend.tools.ai_program_tool import AiProgramTool
from backend.tools.events_tool import EventsTool

app = Flask(__name__)
# Enable CORS for all routes and origins (important for development)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint with API information
    """
    return jsonify({
        "name": "Duke Chatbot API",
        "description": "API for interacting with the Duke University chatbot",
        "endpoints": [
            {
                "path": "/api/chat",
                "method": "POST",
                "description": "Send a message to the chatbot"
            },
            {
                "path": "/api/health",
                "method": "GET",
                "description": "Health check endpoint"
            }
        ],
        "version": "1.0.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint for chat interactions with the Duke Chatbot
    """
    data = request.json
    message = data.get('message', '')
    chat_history = data.get('history', [])
    
    # Build agent with tools
    agent = build_agent()
    
    # Process the message
    response = agent.process(message, chat_history)
    
    return jsonify({
        'message': response.get('answer', ''),
        'thinking': response.get('thinking', ''),
        'tool_calls': response.get('tool_calls', [])
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on port {port}, API URL: http://localhost:{port}/api")
    app.run(host='0.0.0.0', port=port, debug=True)
