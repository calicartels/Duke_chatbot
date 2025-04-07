import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional

class DukeWebsiteTool:
    """
    Tool for scraping and querying Duke University websites
    """
    
    def __init__(self):
        self.base_urls = {
            "main": "https://duke.edu",
            "cs": "https://cs.duke.edu",
            "pratt": "https://pratt.duke.edu",
            "aiprogram": "https://ai.meng.duke.edu"
        }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Return the tool definition for Vertex AI
        """
        return {
            "name": "duke_website_tool",
            "description": "Tool for querying Duke University websites to retrieve information",
            "parameters": {
                "type": "object",
                "properties": {
                    "site": {
                        "type": "string",
                        "description": "The Duke site to query (e.g., 'main', 'cs', 'pratt', 'aiprogram')"
                    },
                    "query": {
                        "type": "string",
                        "description": "The search query or information to look for"
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional specific path to query"
                    }
                },
                "required": ["site", "query"]
            }
        }
    
    def execute(self, site: str, query: str, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a query on a Duke website
        
        Args:
            site: The Duke site to query
            query: The search query
            path: Optional specific path to query
            
        Returns:
            The scraped information
        """
        if site not in self.base_urls:
            return {
                "status": "error",
                "error": f"Site '{site}' not found. Available sites: {', '.join(self.base_urls.keys())}"
            }
        
        base_url = self.base_urls[site]
        
        if path:
            url = f"{base_url}/{path.lstrip('/')}"
        else:
            # Default to search endpoint
            url = f"{base_url}/search"
            query_param = {"q": query}
        
        try:
            if path:
                response = requests.get(url)
                response.raise_for_status()
                
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text content
                content = soup.get_text(separator='\n', strip=True)
                
                # Extract headings
                headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
                
                return {
                    "status": "success",
                    "url": url,
                    "headings": headings,
                    "content": content[:2000] + ("..." if len(content) > 2000 else "")  # Limit content length
                }
            else:
                response = requests.get(url, params=query_param)
                response.raise_for_status()
                
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results
                results = []
                search_results = soup.select('.search-result')  # Adjust selector based on the site's structure
                
                for result in search_results[:5]:  # Limit to top 5 results
                    title_elem = result.select_one('.search-result-title')
                    desc_elem = result.select_one('.search-result-description')
                    link_elem = result.select_one('a')
                    
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description"
                    link = link_elem.get('href') if link_elem else "#"
                    
                    results.append({
                        "title": title,
                        "description": description,
                        "link": link
                    })
                
                return {
                    "status": "success",
                    "url": url,
                    "query": query,
                    "results": results
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error parsing website: {str(e)}"
            }
