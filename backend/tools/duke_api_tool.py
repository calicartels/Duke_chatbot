import os
import requests
from typing import Dict, Any, List, Optional

class DukeApiTool:
    """
    Tool for accessing Duke University APIs via Streamer
    """
    
    def __init__(self):
        self.api_key = os.environ.get("DUKE_API_KEY")
        self.base_url = "https://streamer.oit.duke.edu"
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Return the tool definition for Vertex AI
        """
        return {
            "name": "duke_api_tool",
            "description": "Tool for accessing Duke University APIs to retrieve official information",
            "parameters": {
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "The API endpoint to call (e.g., 'curriculum/courses/subject/COMPSCI', 'ldap/people/netid/vt81')"
                    },
                    "params": {
                        "type": "object",
                        "description": "Additional parameters for the API call"
                    }
                },
                "required": ["endpoint"]
            }
        }
    
    def execute(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute an API call to Duke's API
        
        Args:
            endpoint: The API endpoint to call
            params: Additional parameters for the API call
            
        Returns:
            The API response
        """
        # Use API key as a query parameter, not in headers
        all_params = params.copy() if params else {}
        all_params['access_token'] = self.api_key
        
        # Headers for JSON response
        headers = {
            "Accept": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            print(f"Making API request to: {url}")
            print(f"Params: {all_params}")
            
            response = requests.get(url, headers=headers, params=all_params)
            print(f"Response status code: {response.status_code}")
            
            response.raise_for_status()
            return {
                "status": "success",
                "data": response.json()
            }
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            try:
                if response.text:
                    error_msg += f" - Response: {response.text}"
            except:
                pass
            
            return {
                "status": "error",
                "error": error_msg
            }
    
    # Curriculum endpoints
    
    def get_courses_by_subject(self, subject: str) -> Dict[str, Any]:
        """Get courses for a specific subject"""
        return self.execute(endpoint=f"curriculum/courses/subject/{subject}")
    
    def get_course_details(self, crse_id: str, crse_offer_nbr: str) -> Dict[str, Any]:
        """Get details of a specific course offering"""
        return self.execute(endpoint=f"curriculum/courses/crse_id/{crse_id}/crse_offer_nbr/{crse_offer_nbr}")
    
    def get_classes(self, strm: str, crse_id: str) -> Dict[str, Any]:
        """Get a list of classes for a course"""
        return self.execute(endpoint=f"curriculum/classes/strm/{strm}/crse_id/{crse_id}")
    
    def get_class_section_details(self, strm: str, crse_id: str, crse_offer_nbr: str, 
                                session_code: str, class_section: str) -> Dict[str, Any]:
        """Get details of a specific class section"""
        return self.execute(endpoint=f"curriculum/classes/strm/{strm}/crse_id/{crse_id}/crse_offer_nbr/{crse_offer_nbr}/session_code/{session_code}/class_section/{class_section}")
    
    def get_list_of_values(self, fieldname: str) -> Dict[str, Any]:
        """Get a list of values for a specific field"""
        return self.execute(endpoint=f"curriculum/list_of_values/fieldname/{fieldname}")
    
    def get_class_synopsis(self, strm: str, subject: str, catalog_nbr: str, 
                         session_code: str, class_section: str) -> Dict[str, Any]:
        """Get a synopsis for a specific class"""
        return self.execute(endpoint=f"curriculum/synopsis/strm/{strm}/subject/{subject}/catalog_nbr/{catalog_nbr}/session_code/{session_code}/class_section/{class_section}")
    
    # Directory endpoints
    
    def get_people(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a list of people records"""
        return self.execute(endpoint="ldap/people", params=params)
    
    def get_person(self, ldapkey: str) -> Dict[str, Any]:
        """Get a person record by LDAP key"""
        return self.execute(endpoint=f"ldap/people/{ldapkey}")
    
    def get_person_by_netid(self, netid: str) -> Dict[str, Any]:
        """Get a person record by NetID"""
        return self.execute(endpoint=f"ldap/people/netid/{netid}")
    
    def get_person_by_duid(self, duid: str) -> Dict[str, Any]:
        """Get a person record by Duke unique ID"""
        return self.execute(endpoint=f"ldap/people/duid/{duid}")
    
    # Places endpoints
    
    def get_place_categories(self) -> Dict[str, Any]:
        """Get a list of place categories"""
        return self.execute(endpoint="places/categories")
    
    def get_places(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a list of places"""
        return self.execute(endpoint="places/items", params=params)
    
    def get_place(self, place_id: str) -> Dict[str, Any]:
        """Get a specific place by ID"""
        return self.execute(endpoint=f"places/items/index/{place_id}")
    
    # Social endpoints
    
    def get_social_messages(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get a list of social messages"""
        return self.execute(endpoint="social/messages", params=params)
    
    # EPrint endpoints
    
    def get_printer(self, printer_id: str) -> Dict[str, Any]:
        """Get a specific printer by ID"""
        return self.execute(endpoint=f"eprint/printers/{printer_id}")
    
    def get_departments(self) -> Dict[str, Any]:
        """Get a list of departments"""
        return self.execute(endpoint="eprint/departments")
    
    def get_department(self, dept_id: str) -> Dict[str, Any]:
        """Get a specific department by ID"""
        return self.execute(endpoint=f"eprint/departments/{dept_id}")
    
    def get_sites(self) -> Dict[str, Any]:
        """Get a list of sites"""
        return self.execute(endpoint="eprint/sites")
