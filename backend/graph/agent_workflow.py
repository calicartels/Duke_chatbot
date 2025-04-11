from langgraph.graph import StateGraph, END
from typing import Dict, Any, List
from utils.gemini_client import GeminiClient
from agents.planning_agent import PlanningAgent
from agents.thinking_agent import ThinkingAgent
from agents.evaluation_agent import EvaluationAgent
from tools.duke_events_tool import DukeEventsSearchTool
from tools.duke_future_events_tool import DukeFutureEventsSearchTool
from tools.duke_general_tool import DukeGeneralInfoTool
import os

def create_agent_workflow(gemini_client: GeminiClient):
    """Create the agent workflow graph."""
    # Initialize the tools
    tools = [
        DukeEventsSearchTool(
            api_url=os.environ.get("DUKE_EVENTS_API_URL", "https://dukeevents-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        ),
        DukeFutureEventsSearchTool(
            api_url=os.environ.get("DUKE_FUTURE_EVENTS_API_URL", "https://dukeeventsfuture-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        ),
        DukeGeneralInfoTool(
            api_url=os.environ.get("DUKE_GENERAL_API_URL", "https://dukegeneral-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        )
    ]
    
    # Initialize the agents
    planning_agent = PlanningAgent(tools, gemini_client)
    thinking_agent = ThinkingAgent(gemini_client)
    evaluation_agent = EvaluationAgent(gemini_client)
    
    # Create the state graph
    workflow = StateGraph(Dict[str, Any])
    
    # Add nodes to the graph
    workflow.add_node("planning", planning_agent)
    workflow.add_node("execute_tools", execute_tools)
    workflow.add_node("thinking", thinking_agent)
    workflow.add_node("evaluate_response", evaluation_agent)
    
    # Define the edges (transitions)
    workflow.add_edge("planning", "execute_tools")
    workflow.add_edge("execute_tools", "thinking")
    workflow.add_edge("thinking", "evaluate_response")
    workflow.add_edge("evaluate_response", END)
    
    # Set the entry point
    workflow.set_entry_point("planning")
    
    # Compile the graph
    return workflow.compile()

def execute_tools(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the tools specified in the planning stage.
    """
    plan = state.get("plan", {})
    tools_to_use = plan.get("tools", [])
    
    # Get tool instances from their names
    tool_dict = {
        "DukeEventsSearchTool": DukeEventsSearchTool(
            api_url=os.environ.get("DUKE_EVENTS_API_URL", "https://dukeevents-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        ),
        "DukeFutureEventsSearchTool": DukeFutureEventsSearchTool(
            api_url=os.environ.get("DUKE_FUTURE_EVENTS_API_URL", "https://dukeeventsfuture-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        ),
        "DukeGeneralInfoTool": DukeGeneralInfoTool(
            api_url=os.environ.get("DUKE_GENERAL_API_URL", "https://dukegeneral-695116221974.us-central1.run.app"),
            auth_token=os.environ.get("DUKE_API_AUTH_TOKEN")
        )
    }
    
    tool_results = {}
    
    # Execute each tool with its parameters
    for tool_spec in tools_to_use:
        tool_name = tool_spec.get("name")
        parameters = tool_spec.get("parameters", {})
        
        if tool_name in tool_dict:
            tool = tool_dict[tool_name]
            try:
                result = tool._run(**parameters)
                tool_results[tool_name] = result
            except Exception as e:
                tool_results[tool_name] = {
                    "status": "error",
                    "message": f"Error executing tool: {str(e)}",
                    "source": tool_name
                }
        else:
            tool_results[tool_name] = {
                "status": "error",
                "message": f"Tool not found: {tool_name}",
                "source": "execute_tools"
            }
    
    return {
        **state,
        "tool_results": tool_results,
        "next": "thinking"
    }