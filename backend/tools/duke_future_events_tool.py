import requests
from langchain_core.tools import BaseTool
from typing import Dict, Any, Optional
import json
from datetime import datetime, timedelta

class DukeFutureEventsSearchTool(BaseTool):
    """Tool for searching future events at Duke University by keyword and date range."""
    
    name: str = "DukeFutureEventsSearchTool"
    description: str = "Search for future events at Duke University by keyword and date range"
    api_url: str
    auth_token: Optional[str] = None
    
    def __init__(self, api_url: str, auth_token: Optional[str] = None, **kwargs: Any):
        """
        Initialize the Duke Future Events Search Tool.
        
        Args:
            api_url: The URL of the Duke Future Events API
            auth_token: Optional authentication token for the API
        """
        super().__init__(api_url=api_url, auth_token=auth_token, **kwargs)
        # Pydantic/BaseModel handles assigning api_url and auth_token now
    
    def _run(self, keyword: str, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """
        Search for future events at Duke University.
        
        Args:
            keyword: The keyword to search for (e.g., 'career', 'seminar')
            start_date: Start date in 'YYYY-MM-DD' format (default: today)
            end_date: End date in 'YYYY-MM-DD' format (default: 30 days from start_date)
            limit: Maximum number of events to return (default: 5)
            
        Returns:
            A dictionary containing the search results
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        # Default dates if not provided
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        if not end_date:
            end_date_obj = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=30)
            end_date = end_date_obj.strftime("%Y-%m-%d")
        
        payload = {
            "keyword": keyword,
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            results = response.json()
            return {
                "status": "success",
                "data": results,
                "source": "DukeFutureEventsSearchTool",
                "query_params": payload
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": str(e),
                "source": "DukeFutureEventsSearchTool",
                "query_params": payload
            }
    
    def _arun(self, keyword: str, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """Async implementation of the tool."""
        # This would be an async implementation in a real application
        # For simplicity, we're just calling the sync method
        return self._run(keyword, start_date, end_date, limit)