import os
import json
import google.generativeai as genai
from typing import List, Dict, Any, Optional

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini client with API key."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate a response using Gemini API."""
        try:
            if system_instruction:
                chat = self.model.start_chat(system_instruction=system_instruction)
                response = chat.send_message(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"Error generating text with Gemini: {str(e)}")
            return f"Error: {str(e)}"
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Attempt to parse a JSON response."""
        try:
            # Extract JSON if it's wrapped in markdown code blocks
            if "```json" in response:
                json_content = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_content)
            elif "```" in response:
                json_content = response.split("```")[1].split("```")[0].strip()
                return json.loads(json_content)
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract a JSON-like structure
            print(f"Failed to parse JSON response: {response}")
            return {"error": "Failed to parse response as JSON"}
    
    def evaluate_response(self, query: str, response: str, criteria: List[str]) -> Dict[str, float]:
        """Evaluate a response based on specified criteria."""
        prompt = f"""
        You are an evaluation agent for a Duke University chatbot. Please evaluate the following response to a user query.
        
        USER QUERY: {query}
        
        RESPONSE: {response}
        
        For each criterion, rate the response on a scale of 0 to 10, where 0 is the worst performance and 10 is the best performance.
        
        CRITERIA:
        {', '.join(criteria)}
        
        Provide your evaluation as a JSON object with the criteria as keys and the numeric scores (integers) as values.
        Include a brief 'feedback' field with suggestions for improvement.
        
        Format your response as follows:
        ```json
        {{
          "accuracy": 8,
          "relevance": 7,
          "completeness": 9,
          "clarity": 8,
          "feedback": "Brief feedback here"
        }}
        ```
        """
        
        try:
            eval_response = self.generate_text(prompt)
            eval_dict = self.parse_json_response(eval_response)
            
            # Ensure all criteria are present with fallback values
            for criterion in criteria:
                if criterion not in eval_dict:
                    eval_dict[criterion] = 7  # Default score
            
            return eval_dict
        except Exception as e:
            print(f"Error evaluating response: {str(e)}")
            return {criterion: 7 for criterion in criteria}