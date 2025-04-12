from typing import Dict, Any, List
from utils.gemini_client import GeminiClient
from utils.prompt_templates import EVALUATION_AGENT_PROMPT, RESPONSE_GENERATION_PROMPT

class EvaluationAgent:
    """
    Agent responsible for generating and evaluating responses.
    """
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
        self.evaluation_criteria = ["accuracy", "relevance", "completeness", "clarity"]
    
    def generate_response(self, query: str, information: Dict[str, Any], context: str = "") -> str:
        """
        Generate a response based on the gathered information and conversation context.
        """
        prompt = RESPONSE_GENERATION_PROMPT.format(
            query=query,
            context=context,
            information=str(information)
        )
        
        response = self.gemini_client.generate_text(prompt)
        return response
    
    def evaluate_response(self, query: str, tool_results: Dict[str, Any], proposed_response: str) -> Dict[str, Any]:
        """
        Evaluate the proposed response.
        """
        prompt = EVALUATION_AGENT_PROMPT.format(
            query=query,
            tool_results=str(tool_results),
            proposed_response=proposed_response
        )
        
        evaluation_json = self.gemini_client.generate_text(prompt)
        
        try:
            evaluation = self.gemini_client.parse_json_response(evaluation_json)
            
            # Ensure all criteria have values
            for criterion in self.evaluation_criteria:
                if criterion not in evaluation:
                    evaluation[criterion] = 7  # Default score
                    
            return evaluation
        except Exception as e:
            print(f"Error parsing evaluation: {str(e)}")
            # Fallback evaluation
            return {
                "accuracy": 7,
                "relevance": 7,
                "completeness": 7,
                "clarity": 7,
                "feedback": "Unable to generate detailed evaluation."
            }
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the current state to generate and evaluate a response.
        """
        query = state.get("message", "")
        tool_results = state.get("tool_results", {})
        plan = state.get("plan", {})
        context = state.get("context", "")  # Get context if available
        
        # Check if query was deemed out of scope (empty tools)
        if not plan.get("tools"):
            out_of_scope_response = "I'm sorry, but I can only answer questions about Duke University, its academic programs, campus life, or events. Your question appears to be outside my scope of knowledge. Could you ask something related to Duke University instead?"
            return {
                **state,
                "proposed_response": out_of_scope_response,
                "evaluation": {
                    "accuracy": 10,
                    "relevance": 10,
                    "completeness": 10,
                    "clarity": 10,
                    "feedback": "Out of scope query correctly identified."
                },
                "response": out_of_scope_response,
                "next": "final"
            }
        
        # Continue with normal response generation for in-scope queries
        proposed_response = self.generate_response(query, tool_results, context)
        evaluation = self.evaluate_response(query, tool_results, proposed_response)
        
        return {
            **state,
            "proposed_response": proposed_response,
            "evaluation": evaluation,
            "response": proposed_response,
            "next": "final"
        }