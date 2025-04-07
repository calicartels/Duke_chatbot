import os
from typing import Dict, Any, List
from vertexai.generative_models import GenerativeModel

class LLMJudge:
    """
    An LLM-based judge for evaluating the quality of the chatbot responses
    """
    
    def __init__(self, model_name="gemini-1.5-pro"):
        self.model_name = model_name
        self._model = None
    
    @property
    def model(self):
        """Lazy-loaded model property"""
        if self._model is None:
            self._model = GenerativeModel(self.model_name)
        return self._model
    
    def evaluate_response(self, query: str, response: str, criteria: List[str] = None) -> Dict[str, Any]:
        """
        Evaluate a chatbot response using LLM as a judge
        
        Args:
            query: The user's query
            response: The chatbot's response
            criteria: List of evaluation criteria
            
        Returns:
            Evaluation results
        """
        if criteria is None:
            criteria = [
                "factual_accuracy",
                "relevance",
                "helpfulness",
                "clarity",
                "completeness"
            ]
        
        # Construct the evaluation prompt
        prompt = self._build_evaluation_prompt(query, response, criteria)
        
        # Get evaluation from LLM
        llm_response = self.model.generate_content(prompt)
        
        # Parse the evaluation
        try:
            evaluation = self._parse_evaluation(llm_response.text, criteria)
            return {
                "status": "success",
                "overall_score": evaluation.get("overall_score", 0),
                "criteria_scores": {criterion: evaluation.get(criterion, 0) for criterion in criteria},
                "feedback": evaluation.get("feedback", ""),
                "raw_evaluation": llm_response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to parse evaluation: {str(e)}",
                "raw_evaluation": llm_response.text
            }
    
    def _build_evaluation_prompt(self, query: str, response: str, criteria: List[str]) -> str:
        """Build the prompt for the LLM judge"""
        
        criteria_str = "\n".join([f"- {criterion}" for criterion in criteria])
        
        return f"""Act as an expert judge evaluating the quality of an AI assistant's response.

USER QUERY:
{query}

AI ASSISTANT RESPONSE:
{response}

Evaluate the AI assistant's response based on the following criteria:
{criteria_str}

For each criterion, provide a score from 1 to 5, where:
1 = Poor
2 = Fair
3 = Good
4 = Very Good
5 = Excellent

Please provide your evaluation in the following JSON format:
{{
  "overall_score": <overall score from 1 to 5>,
  {", ".join([f'"{criterion}": <score from 1 to 5>' for criterion in criteria])},
  "feedback": "<your detailed feedback and suggestions for improvement>"
}}

Your evaluation should be fair, objective, and based solely on the quality of the response in relation to the query.
"""
    
    def _parse_evaluation(self, evaluation_text: str, criteria: List[str]) -> Dict[str, Any]:
        """Parse the evaluation response from the LLM"""
        import json
        import re
        
        # Extract JSON from the response
        json_match = re.search(r'```json\n(.*?)\n```', evaluation_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'{{(.*?)}}', evaluation_text, re.DOTALL)
            if json_match:
                json_str = "{" + json_match.group(1) + "}"
            else:
                # Try to find any JSON-like structure in the text
                json_str = evaluation_text
        
        try:
            # Clean up the string to ensure it's valid JSON
            json_str = json_str.replace("'", '"')
            evaluation = json.loads(json_str)
            
            # Ensure all criteria are present
            for criterion in criteria:
                if criterion not in evaluation:
                    evaluation[criterion] = 0
            
            if "overall_score" not in evaluation:
                # Calculate average if not provided
                scores = [evaluation.get(criterion, 0) for criterion in criteria]
                evaluation["overall_score"] = sum(scores) / len(scores) if scores else 0
            
            return evaluation
        except json.JSONDecodeError:
            # Fallback to simple scoring
            evaluation = {}
            
            # Extract scores for each criterion
            for criterion in criteria:
                score_match = re.search(rf'{criterion}[^\d]*(\d+)', evaluation_text, re.IGNORECASE)
                if score_match:
                    score = int(score_match.group(1))
                    evaluation[criterion] = min(max(score, 1), 5)  # Ensure score is between 1 and 5
                else:
                    evaluation[criterion] = 0
            
            # Extract or calculate overall score
            overall_match = re.search(r'overall[^\d]*(\d+)', evaluation_text, re.IGNORECASE)
            if overall_match:
                overall_score = int(overall_match.group(1))
                evaluation["overall_score"] = min(max(overall_score, 1), 5)
            else:
                scores = [evaluation.get(criterion, 0) for criterion in criteria]
                evaluation["overall_score"] = sum(scores) / len(scores) if scores else 0
            
            # Extract feedback
            feedback_match = re.search(r'feedback[^"\']*["\']([^"\']+)["\']', evaluation_text, re.IGNORECASE)
            if feedback_match:
                evaluation["feedback"] = feedback_match.group(1)
            else:
                evaluation["feedback"] = "No detailed feedback provided."
            
            return evaluation
