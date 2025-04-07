import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application configuration
APP_CONFIG = {
    "port": int(os.environ.get("PORT", 5000)),
    "debug": os.environ.get("FLASK_ENV", "development") == "development",
    "host": "0.0.0.0"
}

# Vertex AI configuration
VERTEX_AI_CONFIG = {
    "project_id": os.environ.get("PROJECT_ID"),
    "location": os.environ.get("LOCATION", "us-central1"),
    "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
}

# API configuration
API_CONFIG = {
    "duke_api_key": os.environ.get("DUKE_API_KEY"),
    "duke_api_base_url": "https://api.duke.edu"  # Example URL
}

# LLM model configuration
MODEL_CONFIG = {
    "model_name": "gemini-1.5-pro",
    "temperature": 0.2,
    "max_output_tokens": 1024,
    "top_p": 0.95
}

# CORS configuration
CORS_CONFIG = {
    "origins": [
        "http://localhost:3000",
        "https://duke-chatbot-frontend-dot-*.run.app"
    ]
}

# Logging configuration
LOGGING_CONFIG = {
    "level": os.environ.get("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}
