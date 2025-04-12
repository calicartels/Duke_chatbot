## agents/planning_agent.py
from langchain_core.tools import BaseTool
from typing import List, Dict, Any
from utils.gemini_client import GeminiClient
from utils.prompt_templates import PLANNING_AGENT_PROMPT
from datetime import datetime

class PlanningAgent:
    """
    Agent responsible for planning which tools to use based on the user query.
    """
    def __init__(self, available_tools: List[BaseTool], gemini_client: GeminiClient):
        self.available_tools = available_tools
        self.gemini_client = gemini_client
        self.tool_dict = {tool.name: tool for tool in available_tools}
    
    # In planning_agent.py, update the plan method:

    def plan(self, query: str) -> Dict[str, Any]:
        """
        Plan which tools to use and parameters to pass based on the user query.
        """
        # First, create a more contextual prompt that helps the model understand what's Duke-related
        contextual_prompt = f"""
        Analyze this user query: "{query}"
        
        Determine which Duke University information tool would be most appropriate:
        1. DukeEventsSearchTool - For current campus events
        2. DukeFutureEventsSearchTool - For upcoming events 
        3. DukeGeneralInfoTool - For general Duke information
        4. DukeAIMEngTool - SPECIFICALLY for AI MEng program information (faculty, courses, admissions)
        
        IMPORTANT: Questions about AI program faculty, teaching staff, or instructors should use the DukeAIMEngTool.
        If the query is not related to Duke University, indicate it's out of scope.
        
        Return a JSON with your decision.
        """
        
        # Get a decision from the LLM directly
        decision_response = self.gemini_client.generate_text(contextual_prompt)
        
        try:
            decision = self.gemini_client.parse_json_response(decision_response)
            
            if decision.get("out_of_scope", False):
                return {
                    "tools": [],
                    "reasoning": "This query appears to be outside the scope of the Duke University chatbot."
                }
                
            selected_tool = decision.get("selected_tool")
            if selected_tool == "DukeAIMEngTool" and "faculty" in query.lower():
                return {
                    "tools": [{
                        "name": "DukeAIMEngTool", 
                        "parameters": {"query": query}
                    }],
                    "reasoning": "Using specialized AI MEng tool for faculty information."
                }
                
            # Proceed with standard planning for other queries
            prompt = PLANNING_AGENT_PROMPT.format(query=query)
            response = self.gemini_client.generate_text(prompt)
            
            # Process the planning response
            plan_json = self.gemini_client.parse_json_response(response)
            
            # Extra validation - ensure AI faculty questions go to the right tool
            if "ai" in query.lower() and any(word in query.lower() for word in ["faculty", "teach", "professor"]):
                for tool in plan_json.get("tools", []):
                    if tool.get("name") != "DukeAIMEngTool":
                        # Override with the correct tool
                        return {
                            "tools": [{
                                "name": "DukeAIMEngTool",
                                "parameters": {"query": query}
                            }],
                            "reasoning": "Routing AI faculty question to specialized tool"
                        }
            
            return plan_json
        except Exception as e:
            print(f"Planning error: {str(e)}")
            # Even in case of errors, route AI faculty questions correctly
            if "ai" in query.lower() and any(word in query.lower() for word in ["faculty", "teach", "professor"]):
                return {
                    "tools": [{
                        "name": "DukeAIMEngTool",
                        "parameters": {"query": query}
                    }],
                    "reasoning": "Routing AI faculty question to specialized tool despite parsing error"
                }
            
            # Default fallback
            return {
                "tools": [{
                    "name": "DukeGeneralInfoTool",
                    "parameters": {"query": query}
                }],
                "reasoning": "Defaulting to general info tool due to planning error."
            }
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the user query and update the state with the planning information.
        """
        query = state.get("message", "")
        plan = self.plan(query)
        
        # Enhanced plan with current date for future reference
        plan["query_time"] = datetime.now().isoformat()
        
        # Check if plan has empty tools list - meaning query is out of scope
        if not plan.get("tools", []):
            # Make sure the reasoning indicates this is out of scope
            if "out of scope" not in plan.get("reasoning", "").lower():
                plan["reasoning"] = "This query appears to be outside the scope of the Duke University chatbot."
        
        return {
            "message": query,
            "plan": plan,
            "next": "execute_tools"
        }