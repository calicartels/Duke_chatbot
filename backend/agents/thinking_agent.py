# backend/agents/thinking_agent.py
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
        # Check if query was out of scope (empty tools list)
        if not planning.get("tools", []):
            return """I analyzed your question and determined it's outside the scope of my knowledge. As a Duke University chatbot, I'm specifically designed to answer questions about Duke University, including its academic programs, campus life, events, facilities, and services. Your question appears to be unrelated to Duke, so I can't provide a helpful response. I'd be happy to answer any Duke-specific questions you might have instead."""
        
        # For Duke-related queries, use the normal thinking explanation
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