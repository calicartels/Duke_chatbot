from typing import Dict, Any
from utils.gemini_client import GeminiClient
from utils.prompt_templates import THINKING_AGENT_PROMPT

class ThinkingAgent:
    """
    Agent responsible for explaining the thinking process to the user.
    """
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    def explain_thinking(self, query: str, planning: Dict[str, Any], tool_results: Dict[str, Any]) -> str:
        """
        Generate an explanation of the thinking process.
        """
        prompt = THINKING_AGENT_PROMPT.format(
            query=query,
            planning=str(planning),
            tool_results=str(tool_results)
        )
        
        explanation = self.gemini_client.generate_text(prompt)
        return explanation
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the current state and add thinking explanation.
        """
        query = state.get("message", "")
        planning = state.get("plan", {})
        tool_results = state.get("tool_results", {})
        
        thinking_explanation = self.explain_thinking(query, planning, tool_results)
        
        return {
            **state,
            "thinking_explanation": thinking_explanation,
            "next": "evaluate_response"
        }