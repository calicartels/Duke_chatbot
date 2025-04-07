import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_directory_info():
    """Get directory information for vt81"""
    print("\n===== Duke Directory Information for vt81 =====\n")
    
    # Get API key from environment
    api_key = os.environ.get("DUKE_API_KEY")
    if not api_key:
        print("❌ Error: API key not found in .env file")
        return
    
    # Define request parameters
    base_url = "https://streamer.oit.duke.edu"
    endpoint = "ldap/people/netid/vt81"  # Remove the leading slash
    url = f"{base_url}/{endpoint}"
    
    # Set up authentication using query parameter
    params = {
        "access_token": api_key
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    # Make the request
    print(f"Making request to: {url}")
    print(f"With access_token: {api_key}")
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Success! Here's your information:\n")
            
            # Format and print the data
            formatted_data = json.dumps(data, indent=2)
            print(formatted_data)
            
            # Extract key information if available
            if isinstance(data, dict):
                print("\n----- Key Information -----")
                
                if "duid" in data:
                    print(f"Duke ID: {data.get('duid')}")
                
                if "display_name" in data:
                    print(f"Name: {data.get('display_name')}")
                
                if "email" in data:
                    print(f"Email: {data.get('email')}")
                
                if "telephone_number" in data:
                    print(f"Phone: {data.get('telephone_number')}")
                
                if "title" in data:
                    print(f"Title: {data.get('title')}")
                
                if "department" in data:
                    print(f"Department: {data.get('department')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {str(e)}")
        print(f"Response text: {response.text}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    get_directory_info() 