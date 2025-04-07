import datetime
from typing import Dict, Any, List, Optional

class EventsTool:
    """
    Tool for accessing information about Duke University events
    """
    
    def __init__(self):
        # This would ideally come from a database or API
        # For demonstration purposes, we'll hardcode some events
        self.events = [
            {
                "id": "event001",
                "title": "AI Research Symposium",
                "description": "A day-long symposium featuring research presentations from Duke's AI faculty and graduate students.",
                "date": "2023-11-15",
                "time": "9:00 AM - 5:00 PM",
                "location": "Wilkinson Building Auditorium",
                "organizer": "Duke AI Institute",
                "category": "academic",
                "url": "https://ai.duke.edu/events/symposium2023"
            },
            {
                "id": "event002",
                "title": "Machine Learning Industry Panel",
                "description": "Join industry leaders to discuss the future of machine learning in technology companies.",
                "date": "2023-11-20",
                "time": "4:00 PM - 6:00 PM",
                "location": "Hudson Hall 125",
                "organizer": "Duke Engineering Career Development",
                "category": "career",
                "url": "https://pratt.duke.edu/events/ml-panel"
            },
            {
                "id": "event003",
                "title": "AI Ethics Workshop",
                "description": "Workshop on ethical considerations in AI development and deployment.",
                "date": "2023-12-05",
                "time": "1:00 PM - 4:00 PM",
                "location": "Gross Hall 330",
                "organizer": "Duke Science & Society",
                "category": "workshop",
                "url": "https://scienceandsociety.duke.edu/events/ai-ethics"
            },
            {
                "id": "event004",
                "title": "Duke Basketball vs. UNC",
                "description": "The Blue Devils take on the Tar Heels in this classic rivalry game.",
                "date": "2023-12-10",
                "time": "7:00 PM",
                "location": "Cameron Indoor Stadium",
                "organizer": "Duke Athletics",
                "category": "sports",
                "url": "https://goduke.com/sports/basketball"
            },
            {
                "id": "event005",
                "title": "Holiday Concert",
                "description": "Duke Chapel Choir and Orchestra present a concert of holiday music.",
                "date": "2023-12-15",
                "time": "8:00 PM",
                "location": "Duke Chapel",
                "organizer": "Duke Music Department",
                "category": "cultural",
                "url": "https://chapel.duke.edu/events/holiday-concert"
            }
        ]
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Return the tool definition for Vertex AI
        """
        return {
            "name": "events_tool",
            "description": "Tool for accessing information about Duke University events",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for events (optional)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category filter (e.g., 'academic', 'sports', 'cultural', 'career', 'workshop')"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date filter in YYYY-MM-DD format"
                    },
                    "upcoming": {
                        "type": "boolean",
                        "description": "Whether to return only upcoming events"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of events to return"
                    }
                }
            }
        }
    
    def execute(self, query: Optional[str] = None, category: Optional[str] = None, 
               date: Optional[str] = None, upcoming: bool = True, limit: int = 10) -> Dict[str, Any]:
        """
        Execute a query for Duke events
        
        Args:
            query: Optional search query
            category: Optional category filter
            date: Optional date filter
            upcoming: Whether to return only upcoming events
            limit: Maximum number of events to return
            
        Returns:
            Filtered events information
        """
        filtered_events = self.events.copy()
        
        # Filter by search query
        if query:
            query = query.lower()
            filtered_events = [
                event for event in filtered_events
                if query in event['title'].lower() or query in event['description'].lower()
            ]
        
        # Filter by category
        if category:
            filtered_events = [
                event for event in filtered_events
                if event['category'].lower() == category.lower()
            ]
        
        # Filter by date
        if date:
            try:
                target_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                filtered_events = [
                    event for event in filtered_events
                    if datetime.datetime.strptime(event['date'], '%Y-%m-%d').date() == target_date
                ]
            except ValueError:
                return {
                    "status": "error",
                    "error": "Invalid date format. Please use YYYY-MM-DD format."
                }
        
        # Filter upcoming events
        if upcoming:
            today = datetime.datetime.now().date()
            filtered_events = [
                event for event in filtered_events
                if datetime.datetime.strptime(event['date'], '%Y-%m-%d').date() >= today
            ]
        
        # Sort by date
        filtered_events.sort(key=lambda x: x['date'])
        
        # Apply limit
        filtered_events = filtered_events[:limit]
        
        return {
            "status": "success",
            "count": len(filtered_events),
            "events": filtered_events
        }
