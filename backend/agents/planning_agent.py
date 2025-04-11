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
    
    def plan(self, query: str) -> Dict[str, Any]:
        """
        Plan which tools to use and parameters to pass based on the user query.
        """
        prompt = PLANNING_AGENT_PROMPT.format(query=query)
        response = self.gemini_client.generate_text(prompt)
        
        try:
            # Extract the JSON response
            plan_json = self.gemini_client.parse_json_response(response)
            
            # Validate the plan structure
            if "tools" not in plan_json:
                raise ValueError("Missing 'tools' key in planning response")
                
            return plan_json
        except Exception as e:
            print(f"Planning error: {str(e)}")
            # Fallback if JSON parsing fails
            return {
                "tools": [{
                    "name": "DukeGeneralInfoTool",
                    "parameters": {"query": query}
                }],
                "reasoning": "Defaulting to general info tool due to planning failure."
            }
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the user query and update the state with the planning information.
        """
        query = state.get("message", "")
        plan = self.plan(query)
        
        # Enhanced plan with current date for future reference
        plan["query_time"] = datetime.now().isoformat()
        
        return {
            "message": query,
            "plan": plan,
            "next": "execute_tools"
        }