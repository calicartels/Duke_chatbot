import requests
from langchain_core.tools import BaseTool
from typing import Dict, Any, Optional

class DukeGeneralInfoTool(BaseTool):
    """Tool for searching general information about Duke University."""
    
    name: str = "DukeGeneralInfoTool"
    description: str = "Search for general information about Duke University"
    api_url: str
    auth_token: Optional[str] = None
    
    def __init__(self, api_url: str, auth_token: Optional[str] = None, **kwargs: Any):
        """
        Initialize the Duke General Information Tool.
        
        Args:
            api_url: The URL of the Duke General Info API
            auth_token: Optional authentication token for the API
        """
        super().__init__(api_url=api_url, auth_token=auth_token, **kwargs)
        # Pydantic/BaseModel handles assigning api_url and auth_token now
    
    def _run(self, query: str) -> Dict[str, Any]:
        """
        Search for general information about Duke University.
        
        Args:
            query: The query to search for (e.g., 'AI MEng program', 'dining options')
            
        Returns:
            A dictionary containing the search results
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        payload = {
            "query": query
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            results = response.json()
            return {
                "status": "success",
                "data": results,
                "source": "DukeGeneralInfoTool",
                "query_params": payload
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "source": "DukeGeneralInfoTool",
                "query_params": payload
            }
    
    def _arun(self, query: str) -> Dict[str, Any]:
        """Async implementation of the tool."""
        # This would be an async implementation in a real application
        # For simplicity, we're just calling the sync method
        return self._run(query)