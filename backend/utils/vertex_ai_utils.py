import os
import logging
from pathlib import Path
from google.cloud import aiplatform
from google.oauth2 import service_account

def initialize_vertex_ai():
    """
    Initialize the Vertex AI SDK with credentials from environment
    """
    # Get project details from environment variables
    project_id = os.environ.get("PROJECT_ID")
    location = os.environ.get("LOCATION", "us-central1")
    
    if not project_id:
        logging.warning("PROJECT_ID not set in environment variables")
        return False
    
    # Check if credentials file path is provided
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    
    if credentials_path:
        credentials_path = Path(credentials_path)
        if credentials_path.exists():
            print(f"Using credentials from: {credentials_path}")
            # Initialize with service account credentials
            credentials = service_account.Credentials.from_service_account_file(str(credentials_path))
            aiplatform.init(
                project=project_id,
                location=location,
                credentials=credentials
            )
            return True
        else:
            logging.error(f"Credentials file not found at: {credentials_path}")
            return False
    else:
        # Try using default credentials (e.g., when running in GCP)
        try:
            print("Trying to use default credentials")
            aiplatform.init(
                project=project_id,
                location=location
            )
            return True
        except Exception as e:
            logging.error(f"Failed to initialize Vertex AI with default credentials: {str(e)}")
            return False

def get_gemini_model(model_name="gemini-1.5-pro"):
    """
    Get a Gemini model for inference
    
    Args:
        model_name: The name of the Gemini model to use
        
    Returns:
        A Gemini model instance
    """
    try:
        # Import here to avoid circular imports
        from vertexai.generative_models import GenerativeModel
        
        return GenerativeModel(model_name)
    except ImportError as e:
        logging.error(f"Failed to import Vertex AI modules: {str(e)}")
        logging.error("Make sure you have installed the Vertex AI SDK: pip install google-cloud-aiplatform")
        return None
    except Exception as e:
        logging.error(f"Failed to create Gemini model: {str(e)}")
        return None

def create_tool_config(tools):
    """
    Create a tool configuration for Vertex AI
    
    Args:
        tools: List of tool instances
        
    Returns:
        Tool configuration dictionary
    """
    tool_configs = []
    
    for tool in tools:
        if hasattr(tool, "get_tool_definition"):
            tool_configs.append(tool.get_tool_definition())
    
    return tool_configs

def test_vertex_ai_connection():
    """
    Test Vertex AI connection and configuration
    
    Returns:
        True if successful, False otherwise
    """
    print("Testing Vertex AI connection...")
    
    # Initialize Vertex AI
    if not initialize_vertex_ai():
        print("❌ Failed to initialize Vertex AI!")
        return False
    
    # Test getting a model
    try:
        model = get_gemini_model()
        if model:
            print("✅ Successfully created Gemini model!")
            return True
        else:
            print("❌ Failed to create Gemini model!")
            return False
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False
