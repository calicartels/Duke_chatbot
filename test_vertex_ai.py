import os
import json
from dotenv import load_dotenv
from backend.utils.vertex_ai_utils import test_vertex_ai_connection
from backend.tools.duke_api_tool import DukeApiTool
from backend.tools.duke_website_tool import DukeWebsiteTool
from backend.tools.ai_program_tool import AiProgramTool
from backend.tools.events_tool import EventsTool
from backend.agent.agent_builder import VertexAgent, load_system_prompt

# Load environment variables
load_dotenv()

def test_agent_setup():
    """Test agent setup with tools"""
    print("\nTesting Agent Builder setup...")
    
    # First test Vertex AI connection
    if not test_vertex_ai_connection():
        print("Skipping agent tests due to Vertex AI connection failure")
        return
    
    # Import here to avoid errors if Vertex AI is not set up
    try:
        from google.cloud import aiplatform
        from vertexai.generative_models import GenerativeModel, Tool
        
        # Initialize tools
        tools = [
            DukeApiTool(),
            DukeWebsiteTool(),
            AiProgramTool(),
            EventsTool()
        ]
        
        print("\nSetting up tools for Vertex AI agent...")
        
        # Check each tool
        for i, tool in enumerate(tools):
            print(f"\nTool {i+1}: {tool.__class__.__name__}")
            if hasattr(tool, 'get_tool_definition'):
                tool_def = tool.get_tool_definition()
                print(f"  Name: {tool_def.get('name')}")
                print(f"  Description: {tool_def.get('description')}")
                print("  Parameters:", list(tool_def.get('parameters', {}).get('properties', {}).keys()))
                print("  ✅ Tool definition available")
            else:
                print("  ❌ Missing get_tool_definition method")
        
        # Test creating Vertex AI tools
        try:
            # Get the model
            print("\nInitializing Gemini model...")
            model = GenerativeModel("gemini-1.5-pro")
            
            # Create agent
            print("Creating Vertex AI agent with tools...")
            system_prompt = load_system_prompt()
            agent = VertexAgent(model, system_prompt, tools)
            
            if agent.vertex_tools:
                print(f"✅ Successfully created {len(agent.vertex_tools)} Vertex AI tools")
                
                # Test a simple query
                print("\nTesting agent with a simple query...")
                result = agent.process("Tell me about Duke University")
                
                print("\nAgent response:")
                print("-" * 50)
                print(result.get("answer", "No response"))
                print("-" * 50)
                
                print("\nAgent tool calls:")
                if result.get("tool_calls"):
                    for i, tool_call in enumerate(result["tool_calls"]):
                        print(f"Tool call {i+1}: {tool_call['name']}")
                        print(f"Parameters: {tool_call['parameters']}")
                        print(f"Result status: {tool_call['result'].get('status')}")
                else:
                    print("No tool calls made")
                
                print("\n✅ Agent test complete!")
            else:
                print("❌ No tools were created")
        except Exception as e:
            print(f"❌ Failed to create or test Vertex AI agent: {str(e)}")
    
    except ImportError as e:
        print(f"❌ Failed to import Vertex AI modules: {str(e)}")
        print("Make sure you have installed the Vertex AI SDK: pip install google-cloud-aiplatform")

if __name__ == "__main__":
    test_agent_setup() 