from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

class ConversationState:
    """
    Manages conversation state across multiple turns.
    """
    def __init__(self):
        self.conversations = {}
    
    def create_conversation(self) -> str:
        """
        Create a new conversation and return its ID.
        """
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            "messages": [],
            "context": {},
            "created_at": datetime.now().isoformat()
        }
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str,
                   thinking: Optional[str] = None, tool_results: Optional[Dict[str, Any]] = None,
                   evaluation: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a message to the conversation history.
        """
        if conversation_id not in self.conversations:
            conversation_id = self.create_conversation()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        
        if thinking:
            message["thinking"] = thinking
            
        if tool_results:
            message["tool_results"] = tool_results
            
        if evaluation:
            message["evaluation"] = evaluation
            
        self.conversations[conversation_id]["messages"].append(message)
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        """
        if conversation_id not in self.conversations:
            return []
        
        return self.conversations[conversation_id]["messages"]
    
    def update_context(self, conversation_id: str, key: str, value: Any) -> None:
        """
        Update the context information for a conversation.
        """
        if conversation_id not in self.conversations:
            conversation_id = self.create_conversation()
            
        self.conversations[conversation_id]["context"][key] = value
    
    def get_context(self, conversation_id: str, key: str) -> Any:
        """
        Get a specific context value.
        """
        if conversation_id not in self.conversations:
            return None
            
        return self.conversations[conversation_id]["context"].get(key)
    
    def get_full_context(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get the full context dictionary.
        """
        if conversation_id not in self.conversations:
            return {}
            
        return self.conversations[conversation_id]["context"]