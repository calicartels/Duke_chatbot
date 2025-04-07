import os
import json
import logging
from pathlib import Path
from google.cloud import aiplatform
from google.oauth2 import service_account

from backend.tools.duke_api_tool import DukeApiTool
from backend.tools.duke_website_tool import DukeWebsiteTool
from backend.tools.ai_program_tool import AiProgramTool
from backend.tools.events_tool import EventsTool
from backend.utils.vertex_ai_utils import initialize_vertex_ai, get_gemini_model
from .discovery_agent import DiscoveryAgent

class SimpleVertexAgent:
    """
    Simple agent implementation using Vertex AI Gemini model with tools
    """
    def __init__(self, model, system_prompt, tools=None):
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools or []
        
    def _execute_tool(self, tool_name, tool_params):
        """Execute a tool by name with given parameters"""
        for tool in self.tools:
            tool_def = tool.get_tool_definition()
            if tool_def["name"] == tool_name:
                # Call the execute method with unpacked parameters
                return tool.execute(**tool_params)
        
        return {"status": "error", "error": f"Tool '{tool_name}' not found"}
    
    def process(self, message, history=None):
        """Process a user message and return a response"""
        try:
            # Simple response without tools for now, just to test Google Cloud connection
            prompt = f"{self.system_prompt}\n\nUser: {message}\n\nAssistant:"
            
            print(f"Sending message to Gemini: {message}")
            
            response = self.model.generate_content(prompt)
            answer = response.text if hasattr(response, 'text') else str(response)
            
            # For demonstration, no tool calls yet
            return {
                "answer": answer,
                "thinking": "Direct response without tool calls",
                "tool_calls": []
            }
        
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
            print(f"Error processing message: {str(e)}")
            return {
                "answer": f"I'm sorry, I encountered an error while processing your request: {str(e)}",
                "thinking": "",
                "tool_calls": []
            }

def load_system_prompt():
    """
    Load the system prompt from the prompt templates directory
    """
    prompt_dir = Path(__file__).parent / "prompt_templates"
    system_prompt_path = prompt_dir / "system_prompt.txt"
    
    if system_prompt_path.exists():
        with open(system_prompt_path, "r") as f:
            return f.read()
    else:
        # Default system prompt if file doesn't exist
        return """You are Duke Chatbot, an AI assistant for Duke University.
Your purpose is to help students, faculty, and staff access information about Duke programs,
events, resources, and answer questions about the university."""

def build_agent():
    """
    Build and configure the Agent for Duke Chatbot
    """
    # Check if we should use Discovery Engine
    use_discovery = os.getenv("USE_DISCOVERY_ENGINE", "").lower() == "true"
    data_store_exists = os.getenv("DATA_STORE_ID") is not None
    
    if use_discovery and data_store_exists:
        # Use Discovery Engine agent
        try:
            logging.info("Building Discovery Engine agent")
            return DiscoveryAgent()
        except Exception as e:
            logging.error(f"Failed to build Discovery Engine agent: {str(e)}")
            # Fall back to Vertex AI agent
            logging.info("Falling back to Vertex AI agent")
    
    # Use Vertex AI agent
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        logging.error("Failed to initialize Vertex AI")
        # Return a fallback agent that doesn't use Vertex AI
        return FallbackAgent()
    
    # Get the model
    model = get_gemini_model()
    if not model:
        logging.error("Failed to get Gemini model")
        return FallbackAgent()
    
    # Initialize tools
    tools = [
        DukeApiTool(),
        DukeWebsiteTool(),
        AiProgramTool(),
        EventsTool()
    ]
    
    # Load system prompt
    system_prompt = load_system_prompt()
    
    # Create and return the agent
    return SimpleVertexAgent(model, system_prompt, tools)

class FallbackAgent:
    """
    Fallback agent when Vertex AI is not available
    """
    def process(self, message, history=None):
        return {
            "answer": "I'm sorry, I'm currently unable to access Duke information services. The Vertex AI connection is not available. Please try again later or contact support.",
            "thinking": "Vertex AI connection failed",
            "tool_calls": []
        }
