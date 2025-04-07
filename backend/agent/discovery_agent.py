import os
from dotenv import load_dotenv
from google.cloud import discoveryengine_v1 as discoveryengine

class DiscoveryAgent:
    """
    Agent implementation using Google's Discovery Engine (Agent Builder)
    """
    
    def __init__(self):
        load_dotenv()
        self.project_id = os.getenv("PROJECT_ID")
        self.location = os.getenv("LOCATION", "global")  # Using global region
        self.data_store_id = os.getenv("DATA_STORE_ID", "duke-university-store")
        self.collection_id = "default_collection"
        
        # Initialize clients
        self.conversation_client = discoveryengine.ConversationalSearchServiceClient()
        self.data_store_client = discoveryengine.DataStoreServiceClient()
        
        # Data store path with collection
        self.data_store_path = f"projects/{self.project_id}/locations/{self.location}/collections/{self.collection_id}/dataStores/{self.data_store_id}"
        
        # For serving config
        self.serving_config = f"{self.data_store_path}/servingConfigs/default_config"
        
        # Use the path from .env if available
        if os.getenv("DATA_STORE_PATH"):
            self.data_store_path = os.getenv("DATA_STORE_PATH")
            self.serving_config = f"{self.data_store_path}/servingConfigs/default_config"
        
        # Test connecting to Discovery Engine
        print("Testing Discovery Engine connection...")
        self.use_fallback = not self._test_connection()
        if self.use_fallback:
            print("⚠️ Discovery Engine connection failed. Using fallback mode.")
        else:
            print("✅ Discovery Engine connection successful.")
    
    def _test_connection(self):
        """Test connection to Discovery Engine"""
        try:
            # Check if we can access the data store
            self.data_store_client.get_data_store(name=self.data_store_path)
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def process(self, message, chat_history=None):
        """
        Process a message using Discovery Engine
        
        Args:
            message (str): User message
            chat_history (list): Chat history
            
        Returns:
            dict: Response containing answer, thinking, and tool calls
        """
        if self.use_fallback:
            return self._fallback_response(message)
        
        # Get or create conversation ID for this session
        session_id = self._get_session_id(chat_history)
        
        try:
            # Create conversation request with proper text format
            request = discoveryengine.ConverseConversationRequest()
            request.name = f"{self.data_store_path}/conversations/{session_id}"
            
            # For text input, we need to set it differently based on API version
            try:
                # Try direct assignment first (newer API versions)
                request.query.text = message
            except (AttributeError, TypeError):
                try:
                    # Try with TextInput class
                    text_input = discoveryengine.TextInput()
                    text_input.text = message
                    request.query = text_input
                except Exception as text_error:
                    print(f"Error setting text input: {text_error}")
                    # Last resort - set raw dict format
                    request.query = {"text": message}
            
            request.serving_config = self.serving_config
            
            # Get response from Discovery Engine
            try:
                response = self.conversation_client.converse_conversation(request)
                
                # Extract reply and any tool calls
                answer = response.reply.summary if hasattr(response.reply, 'summary') else str(response.reply)
                tool_calls = self._extract_tool_calls(response)
                thinking = self._extract_thinking(response)
                
                return {
                    "answer": answer,
                    "thinking": thinking,
                    "tool_calls": tool_calls,
                    "session_id": session_id
                }
            except Exception as api_error:
                print(f"API Error: {api_error}")
                # If we hit permission issues, fall back to simulated response
                if "PERMISSION_DENIED" in str(api_error) or "IAM_PERMISSION_DENIED" in str(api_error):
                    print("⚠️ Permission denied when calling Discovery Engine API. Using fallback response.")
                    return self._fallback_response(message)
                elif "NOT_FOUND" in str(api_error):
                    print("⚠️ Resource not found. The data store or conversation may not exist.")
                    return self._fallback_response(message)
                else:
                    return {
                        "answer": f"I encountered an error processing your request: {str(api_error)}",
                        "thinking": str(api_error),
                        "tool_calls": [],
                        "session_id": session_id
                    }
        except Exception as e:
            print(f"General error: {e}")
            return {
                "answer": f"I'm having trouble processing your request. Error: {str(e)}",
                "thinking": str(e),
                "tool_calls": [],
                "session_id": session_id
            }
    
    def _get_session_id(self, chat_history):
        """
        Get or create a session ID for this conversation
        """
        # If first message or no history, create a new conversation
        if not chat_history or len(chat_history) == 0:
            try:
                # Create a conversation
                conversation = discoveryengine.Conversation()
                conversation.user_pseudo_id = f"user-{os.urandom(4).hex()}"
                
                try:
                    created_conversation = self.conversation_client.create_conversation(
                        parent=self.data_store_path,
                        conversation=conversation
                    )
                    
                    # Extract conversation ID from name
                    session_id = created_conversation.name.split("/")[-1]
                    return session_id
                except Exception as api_error:
                    print(f"Error creating conversation: {api_error}")
                    # If permission issues, return a fallback session ID
                    return f"fallback-session-{os.urandom(4).hex()}"
                    
            except Exception as e:
                print(f"Error creating conversation: {e}")
                return f"fallback-session-{os.urandom(4).hex()}"
        
        # If conversation has a session ID, use it
        for message in reversed(chat_history):
            if message.get("session_id"):
                return message["session_id"]
        
        # Fallback to creating a new session
        return self._get_session_id([])
    
    def _extract_tool_calls(self, response):
        """
        Extract tool calls from Discovery Engine response
        """
        tool_calls = []
        
        # Extract any tool calls from the response
        if hasattr(response, 'search_results') and response.search_results:
            for result in response.search_results:
                if hasattr(result, 'document') and result.document:
                    tool_calls.append({
                        "name": "retrieve_document",
                        "input": {"document_id": result.document.id},
                        "output": result.document.derived_struct_data if hasattr(result.document, 'derived_struct_data') else {}
                    })
        
        return tool_calls
    
    def _extract_thinking(self, response):
        """
        Extract thinking/reasoning from Discovery Engine response
        """
        # Extract references and citations if available
        if hasattr(response, 'reply') and hasattr(response.reply, 'references') and response.reply.references:
            thinking = "References:\n"
            for ref in response.reply.references:
                thinking += f"- {ref.uri if hasattr(ref, 'uri') else str(ref)}\n"
            return thinking
        
        return ""
    
    def _fallback_response(self, message):
        """Generate a fallback response when Discovery Engine is not available"""
        return {
            "answer": self._generate_fallback_answer(message),
            "thinking": "Using fallback mode since Discovery Engine is not accessible.",
            "tool_calls": [],
            "session_id": f"fallback-{os.urandom(4).hex()}"
        }
    
    def _generate_fallback_answer(self, message):
        """Generate a simulated response based on the message content"""
        message_lower = message.lower()
        
        if "ai meng" in message_lower or "ai program" in message_lower:
            return ("The Duke AI MEng program offers a comprehensive curriculum in artificial intelligence "
                   "and machine learning. Students gain technical knowledge while developing business and "
                   "management skills necessary for leadership roles in the AI field. The program includes "
                   "coursework in machine learning, deep learning, computer vision, natural language processing, "
                   "and AI ethics.")
        
        elif "service" in message_lower or "support" in message_lower:
            return ("Duke University offers a wide range of services to support students, including "
                   "academic advising, career counseling, health and wellness services, library resources, "
                   "and IT support.")
        
        elif "apply" in message_lower or "admission" in message_lower:
            return ("For information about admissions to Duke University programs, including deadlines, "
                   "requirements, and application procedures, please visit the Duke admissions website "
                   "or contact the admissions office. The typical application process involves submitting "
                   "transcripts, test scores, letters of recommendation, and a personal statement.")
        
        elif "curriculum" in message_lower or "course" in message_lower:
            return ("Duke's curriculum includes a variety of courses across different disciplines. "
                   "Specific program curricula vary, but most degree programs include a mix of core "
                   "requirements and electives to provide a well-rounded education.")
        
        else:
            return ("I'm using a simplified response mode due to Discovery Engine configuration issues. "
                   "I can provide basic information about Duke University programs and services. "
                   "For more specific or detailed information, please try again later when the full "
                   "Discovery Engine integration is available.") 