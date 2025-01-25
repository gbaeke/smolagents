from smolagents import Tool
import requests
from typing import Dict, List

class BingSearchTool(Tool):
    name = "bing_search"
    description = """
    This tool performs a Bing web search and returns the top search results for a given query.
    It returns a string containing formatted search results.
    It is best for overview information."""
    
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
        }
    }
    output_type = "string"

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.endpoint = "https://api.bing.microsoft.com/v7.0/search"
        
    def forward(self, query: str, num_results: int = 5) -> str:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {
            "q": query,
            "count": num_results,
            "textDecorations": False,
            "textFormat": "Raw"
        }
        
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()
            
            formatted_results = []
            for item in search_results.get("webPages", {}).get("value", []):
                result = f"Title: {item['name']}\nSnippet: {item['snippet']}\nURL: {item['url']}\n"
                formatted_results.append(result)
            
            return "\n".join(formatted_results)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Bing search failed: {str(e)}") 