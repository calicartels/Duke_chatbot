import os
import sys
from dotenv import load_dotenv, set_key
from google.cloud import discoveryengine_v1 as discoveryengine

def setup_discovery_engine():
    """
    Setup Discovery Engine data store and populate with initial Duke University data
    """
    # Load environment variables
    load_dotenv()
    
    # Get environment variables
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION", "global")
    data_store_id = os.getenv("DATA_STORE_ID", "duke-university-store")
    collection_id = "default_collection"
    
    if not project_id:
        print("ERROR: PROJECT_ID environment variable is not set.")
        print("Please set it in your .env file.")
        return False
    
    print(f"Setting up Discovery Engine for project: {project_id}")
    
    # Initialize clients
    data_store_client = discoveryengine.DataStoreServiceClient()
    document_client = discoveryengine.DocumentServiceClient()
    
    # Data store path
    data_store_path = f"projects/{project_id}/locations/{location}/collections/{collection_id}/dataStores/{data_store_id}"
    parent = f"projects/{project_id}/locations/{location}/collections/{collection_id}"
    
    # Try to get the data store to check if it exists
    try:
        print(f"Checking if data store {data_store_id} exists...")
        data_store = data_store_client.get_data_store(name=data_store_path)
        print(f"✅ Data store found: {data_store.name}")
    except Exception as e:
        # If the data store doesn't exist, try to create it
        if "NOT_FOUND" in str(e):
            print(f"Data store {data_store_id} not found. Creating new data store...")
            try:
                # 1. Create data store
                data_store = discoveryengine.DataStore(
                    display_name="Duke University Agent",
                    industry_vertical="GENERIC",
                    solution_types=["SOLUTION_TYPE_CHAT"],
                )
                
                operation = data_store_client.create_data_store(
                    parent=parent,
                    data_store_id=data_store_id,
                    data_store=data_store
                )
                created_data_store = operation.result()
                print(f"✅ Created data store: {created_data_store.name}")
                
                # Update the path in .env file
                set_key('.env', 'DATA_STORE_PATH', data_store_path)
                print("✅ Updated .env file with DATA_STORE_PATH")
            except Exception as create_error:
                if "PERMISSION_DENIED" in str(create_error) or "IAM_PERMISSION_DENIED" in str(create_error):
                    print("⚠️ Permission denied. You need discoveryengine.dataStores.create permission.")
                    print("Continuing with the assumption that the data store exists...")
                else:
                    print(f"⚠️ Error creating data store: {create_error}")
                    print("Continuing with data store ID in .env file...")
        else:
            print(f"⚠️ Error checking data store: {e}")
            print("Continuing with data store ID in .env file...")
    
    # 2. Add documents with Duke information
    documents = [
        {
            "id": "ai-meng-program",
            "title": "Duke AI MEng Program",
            "content": """
            <h1>Duke AI MEng Program</h1>
            <p>The Duke AI MEng program offers a comprehensive curriculum in artificial intelligence 
            and machine learning. Students gain technical knowledge while developing business and 
            management skills necessary for leadership roles in the AI field.</p>
            <p>The program includes coursework in machine learning, deep learning, computer vision, 
            natural language processing, and AI ethics.</p>
            """
        },
        {
            "id": "duke-services",
            "title": "Duke Student Services",
            "content": """
            <h1>Duke Student Services</h1>
            <p>Duke University offers a wide range of services to support students:</p>
            <ul>
                <li>Academic advising</li>
                <li>Career counseling</li>
                <li>Health and wellness services</li>
                <li>Library resources</li>
                <li>IT support</li>
            </ul>
            """
        },
        {
            "id": "duke-admissions",
            "title": "Duke Admissions",
            "content": """
            <h1>Duke Admissions</h1>
            <p>For information about admissions to Duke University programs, including deadlines, 
            requirements, and application procedures, please visit the Duke admissions website 
            or contact the admissions office.</p>
            <p>The typical application process involves submitting transcripts, test scores, 
            letters of recommendation, and a personal statement.</p>
            """
        }
    ]
    
    print("\nAttempting to add sample documents...")
    success_count = 0
    for doc_info in documents:
        try:
            document = discoveryengine.Document(
                id=doc_info["id"],
                content=discoveryengine.Document.Content(
                    mime_type="text/html",
                    raw_bytes=doc_info["content"].encode()
                )
            )
            
            branch_path = f"{data_store_path}/branches/default_branch"
            created_document = document_client.create_document(
                parent=branch_path,
                document=document,
                document_id=doc_info["id"]
            )
            print(f"✅ Created document: {doc_info['title']}")
            success_count += 1
            
        except Exception as e:
            if "already exists" in str(e):
                print(f"ℹ️ Document {doc_info['id']} already exists.")
                success_count += 1
            elif "NOT_FOUND" in str(e):
                print(f"⚠️ Could not create document {doc_info['id']}: {e}")
            elif "PERMISSION_DENIED" in str(e):
                print(f"⚠️ Permission denied when creating document {doc_info['id']}")
            else:
                print(f"⚠️ Error creating document {doc_info['id']}: {e}")
    
    if success_count > 0:
        print("\n✅ Documents added to Discovery Engine!")
    else:
        print("\n⚠️ No documents were added. There might be permission issues or the data store does not exist.")
    
    print("\nSetup complete. Discovery Engine configurations are set in .env file.")
    print("\nTo access the Agent Builder console (if you have permissions):")
    print(f"https://console.cloud.google.com/ai/gen-app-builder/data-stores?project={project_id}")
    
    # Test Discovery Engine connection
    try:
        print("\nTesting Discovery Engine connection...")
        conversation_client = discoveryengine.ConversationalSearchServiceClient()
        print("✅ Successfully initialized ConversationalSearchServiceClient")
        return True
    except Exception as e:
        print(f"⚠️ Error connecting to Discovery Engine: {e}")
        return False

if __name__ == "__main__":
    setup_discovery_engine() 