# backend/tools/duke_ai_meng_tool.py
import requests
import os
from langchain_core.tools import BaseTool
from typing import Dict, Any, Optional
from pydantic import Field  # Add this import

class DukeAIMEngTool(BaseTool):
    """Tool for searching AI MEng program information using Google PSE."""
    
    name: str = "DukeAIMEngTool"
    description: str = "Search for specific information about Duke's AI MEng program"
    api_key: str = Field(default="")  # Define field with default
    cx: str = Field(default="40ad5871d1ccf4b4e")  # Define field with default
    
    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None, **kwargs: Any):
        """Initialize the Duke AI MEng Tool."""
        api_key_val = api_key or os.environ.get("GOOGLE_API_KEY")
        cx_val = cx or "40ad5871d1ccf4b4e"  # Your PSE ID
        
        if not api_key_val:
            raise ValueError("Google API key not provided or found in environment")
        
        # Pass the values to the parent class constructor
        super().__init__(api_key=api_key_val, cx=cx_val, **kwargs)
    
    def _run(self, query: str) -> Dict[str, Any]:
        """Search for information about Duke's AI MEng program using Google PSE."""
        # Format query to specifically target Duke AI MEng content
        enhanced_query = f"Duke University AI MEng {query}"
        
        # Build URL for Google Custom Search API
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            "q": enhanced_query,
            "key": self.api_key,
            "cx": self.cx
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract and format results
            results = []
            if "items" in data:
                results = [{
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                } for item in data["items"]]
            
            return {
                "status": "success",
                "data": {
                    "results": results,
                    "total": len(results)
                },
                "source": "DukeAIMEngTool"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "source": "DukeAIMEngTool"
            }