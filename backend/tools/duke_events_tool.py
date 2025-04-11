import requests
from langchain_core.tools import BaseTool
from typing import Dict, Any, Optional
import json

class DukeEventsSearchTool(BaseTool):
    """Tool for searching current events at Duke University by topic."""
    
    name: str = "DukeEventsSearchTool"
    description: str = "Search for current events at Duke University by topic"
    api_url: str
    auth_token: Optional[str] = None
    
    def __init__(self, api_url: str, auth_token: Optional[str] = None, **kwargs: Any):
        """
        Initialize the Duke Events Search Tool.
        
        Args:
            api_url: The URL of the Duke Events API
            auth_token: Optional authentication token for the API
        """
        super().__init__(api_url=api_url, auth_token=auth_token, **kwargs)
        # Pydantic/BaseModel handles assigning api_url and auth_token now
    
    def _run(self, topic: str, days: int = 7, limit: int = 5) -> Dict[str, Any]:
        """
        Search for current events at Duke University.
        
        Args:
            topic: The topic to search for (e.g., 'career', 'academic', 'social')
            days: Number of days to look ahead (default: 7)
            limit: Maximum number of events to return (default: 5)
            
        Returns:
            A dictionary containing the search results
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        payload = {
            "topic": topic,
            "days": days,
            "limit": limit
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            results = response.json()
            return {
                "status": "success",
                "data": results,
                "source": "DukeEventsSearchTool",
                "query_params": payload
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "source": "DukeEventsSearchTool",
                "query_params": payload
            }
    
    def _arun(self, topic: str, days: int = 7, limit: int = 5) -> Dict[str, Any]:
        """Async implementation of the tool."""
        # This would be an async implementation in a real application
        # For simplicity, we're just calling the sync method
        return self._run(topic, days, limit)