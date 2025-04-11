from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv
from graph.agent_workflow import create_agent_workflow
from utils.gemini_client import GeminiClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Gemini client
gemini_client = GeminiClient(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the agent workflow
agent_graph = create_agent_workflow(gemini_client)

@app.route('/api/chat', methods=['POST'])
def chat():
    start_time = time.time()
    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversationId', None)
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Process the message through the agent workflow
    try:
        result = agent_graph.invoke({
            "message": user_message,
            "conversation_id": conversation_id,
        })
        
        # Add processing time
        result["processing_time"] = int((time.time() - start_time) * 1000)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return jsonify({
            "error": "Failed to process message",
            "details": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)