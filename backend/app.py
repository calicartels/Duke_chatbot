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

# Modify the chat endpoint in app.py
@app.route('/api/chat', methods=['POST'])
def chat():
    start_time = time.time()
    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversationId', None)
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get conversation context if available
    conversation_context = ""
    if conversation_id:
        try:
            from graph.state_management import conversation_state
            conversation_context = conversation_state.get_recent_context(conversation_id)
        except (ImportError, AttributeError) as e:
            print(f"Warning: Could not load conversation context: {str(e)}")
            # Continue without context if there's an error
    
    # Process the message through the agent workflow
    try:
        # Initialize the state with basic information
        initial_state = {
            "message": user_message,
            "conversation_id": conversation_id,
        }
        
        # Add context if available
        if conversation_context:
            initial_state["context"] = conversation_context
        
        result = agent_graph.invoke(initial_state)
        
        # Add processing time
        result["processing_time"] = int((time.time() - start_time) * 1000)
        
        # Store the message in conversation history if we have conversation state
        try:
            if conversation_id:
                from graph.state_management import conversation_state
                # Store user message
                conversation_state.add_message(
                    conversation_id=conversation_id,
                    role="user",
                    content=user_message
                )
                # Store assistant response
                conversation_state.add_message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=result.get("response", ""),
                    thinking=result.get("thinking_explanation"),
                    tool_results=result.get("tool_results"),
                    evaluation=result.get("evaluation")
                )
        except Exception as e:
            print(f"Warning: Could not store conversation: {str(e)}")
        
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