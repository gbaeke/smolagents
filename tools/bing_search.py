from smolagents import Tool
import requests
from typing import Dict, List

class BingSearchTool(Tool):
    name = "bing_search"
    description = """
    This tool performs a Bing web and image search and returns the top search results for a given query.
    It returns a string containing formatted search results including web pages and images.
    It is best for overview information or to find a url to scrape."""
    
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to look up on Bing",
        },
        "num_results": {
            "type": "integer",
            "description": "Number of search results to return (default: 5)",
            "default": 5,
            "nullable": True
        },
        "include_images": {
            "type": "boolean",
            "description": "Whether to include image results (default: False)",
            "default": False,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.web_endpoint = "https://api.bing.microsoft.com/v7.0/search"
        self.image_endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
        
    def _get_web_results(self, query: str, num_results: int) -> List[str]:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {
            "q": query,
            "count": num_results,
            "textDecorations": False,
            "textFormat": "Raw"
        }
        
        response = requests.get(self.web_endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        formatted_results = []
        for item in search_results.get("webPages", {}).get("value", []):
            result = f"Title: {item['name']}\nSnippet: {item['snippet']}\nURL: {item['url']}\n"
            formatted_results.append(result)
            
        return formatted_results

    def _get_image_results(self, query: str, num_results: int) -> List[str]:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {
            "q": query,
            "count": num_results,
            "textDecorations": False,
            "textFormat": "Raw"
        }
        
        response = requests.get(self.image_endpoint, headers=headers, params=params)
        response.raise_for_status()
        image_results = response.json()
        
        formatted_results = []
        for item in image_results.get("value", []):
            result = f"Image Title: {item['name']}\nImage URL: {item['contentUrl']}\nThumbnail URL: {item['thumbnailUrl']}\nSource: {item['hostPageDisplayUrl']}\n"
            formatted_results.append(result)
            
        return formatted_results
        
    def forward(self, query: str, num_results: int = 5, include_images: bool = True) -> str:
        try:
            results = []
            
            # Get web results
            web_results = self._get_web_results(query, num_results)
            if web_results:
                results.append("=== Web Results ===")
                results.extend(web_results)
            
            # Get image results if requested
            if include_images:
                image_results = self._get_image_results(query, num_results)
                if image_results:
                    results.append("\n=== Image Results ===")
                    results.extend(image_results)
            
            return "\n".join(results) if results else "No results found."
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Bing search failed: {str(e)}") 