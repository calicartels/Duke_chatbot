import os
from dotenv import load_dotenv
from backend.agent.discovery_agent import DiscoveryAgent

def test_discovery_engine():
    """
    Test the Discovery Engine agent integration
    """
    # Load environment variables
    load_dotenv()
    
    # Check if DATA_STORE_ID is set
    data_store_id = os.getenv("DATA_STORE_ID")
    if not data_store_id:
        print("ERROR: DATA_STORE_ID environment variable is not set.")
        print("Please run setup_discovery_engine.py first to create a data store.")
        return False
    
    # Create the agent
    try:
        print("Initializing Discovery Engine agent...")
        agent = DiscoveryAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"⚠️ Error initializing agent: {e}")
        return False
    
    # Test sample queries
    sample_queries = [
        "Tell me about the AI MEng program at Duke",
        "What student services does Duke offer?",
        "How do I apply to Duke University?",
        "What is the curriculum for the AI MEng program?"
    ]
    
    # Process each query
    for i, query in enumerate(sample_queries):
        print(f"\n--- Test Query {i+1}: '{query}' ---")
        
        try:
            # Process the query
            response = agent.process(query)
            
            # Print the response
            print(f"Agent Response: {response['answer']}")
            print(f"Session ID: {response['session_id']}")
            
            if response['tool_calls']:
                print("Tool Calls:")
                for tool_call in response['tool_calls']:
                    print(f"  - {tool_call['name']}: {tool_call['input']}")
            
            if response['thinking']:
                print(f"Thinking: {response['thinking']}")
                
        except Exception as e:
            print(f"⚠️ Error processing query: {e}")
    
    print("\n✅ Discovery Engine agent test complete!")
    return True

if __name__ == "__main__":
    test_discovery_engine() 