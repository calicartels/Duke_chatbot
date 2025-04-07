import os
import json
from dotenv import load_dotenv
from backend.tools.duke_api_tool import DukeApiTool

# Load environment variables
load_dotenv()

def test_duke_api():
    """Test Duke Streamer API connection and endpoints"""
    print("\n===== Testing Duke Streamer API Connection =====")
    
    # Create Duke API tool
    duke_api = DukeApiTool()
    
    # Check if API key is loaded correctly
    api_key = os.environ.get("DUKE_API_KEY")
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    print(f"API Key: {api_key}")
    print(f"Base URL: {duke_api.base_url}\n")
    
    # Test directory endpoint with your netid (vt81)
    print("Testing: Directory API - Get person by netid (vt81)")
    try:
        result = duke_api.get_person_by_netid("vt81")
        if result["status"] == "success":
            print("✅ Success!")
            data_sample = json.dumps(result["data"], indent=2)
            print(f"Data: {data_sample}")
        else:
            print("❌ Failed!")
            print(f"Error: {result.get('error')}")
    except Exception as e:
        print("❌ Exception occurred!")
        print(f"Error: {str(e)}")
    print()
    
    # Test a simple endpoint like places/categories
    print("Testing: Places API - Get categories")
    try:
        result = duke_api.execute("places/categories")
        if result["status"] == "success":
            print("✅ Success!")
            data_sample = json.dumps(result["data"], indent=2)
            print(f"Data: {data_sample}")
        else:
            print("❌ Failed!")
            print(f"Error: {result.get('error')}")
    except Exception as e:
        print("❌ Exception occurred!")
        print(f"Error: {str(e)}")
    print()
    
    # Try a direct API call to see the raw response
    print("Testing: Raw API call to check service")
    try:
        import requests
        headers = {
            "Accept": "application/json"
        }
        params = {
            "access_token": api_key
        }
        url = f"{duke_api.base_url}/ldap/people/netid/vt81"
        
        print(f"Making direct request to: {url}")
        print(f"With access_token: {api_key}")
        
        response = requests.get(url, headers=headers, params=params)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:1000]}")
    except Exception as e:
        print(f"Error with direct API call: {str(e)}")

    # Test an example from the curriculum API
    print("\nTesting: Curriculum API - Get Computer Science courses")
    try:
        result = duke_api.execute("curriculum/courses/subject/COMPSCI")
        if result["status"] == "success":
            print("✅ Success!")
            # Print just the first course for brevity
            if isinstance(result["data"], list) and len(result["data"]) > 0:
                data_sample = json.dumps(result["data"][0], indent=2)
                print(f"First course data: {data_sample}")
                print(f"Total courses: {len(result['data'])}")
            else:
                print(f"Data: {json.dumps(result['data'], indent=2)}")
        else:
            print("❌ Failed!")
            print(f"Error: {result.get('error')}")
    except Exception as e:
        print("❌ Exception occurred!")
        print(f"Error: {str(e)}")

    # Test AIPI courses like in the example
    print("\nTesting: Curriculum API - Get AIPI courses")
    try:
        result = duke_api.execute("curriculum/courses/subject/AIPI")
        if result["status"] == "success":
            print("✅ Success!")
            # Check the structure and print appropriate information
            data_sample = json.dumps(result["data"], indent=2)[:1000]
            print(f"Data sample: {data_sample}...")
        else:
            print("❌ Failed!")
            print(f"Error: {result.get('error')}")
    except Exception as e:
        print("❌ Exception occurred!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_duke_api() 