from smolagents import Tool
import requests
from bs4 import BeautifulSoup
from typing import Optional
import json

class ScrapeTool(Tool):
    name = "web_scraper"
    description = """
    This tool scrapes the content from a given URL and returns the main text content.
    It removes scripts, styles, navigation, headers, and footers to focus on the main content.
    Use this tool for detailed information about user queries if you have the URLs."""
    
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL of the webpage to scrape in format https://www.example.com",
        },
        "max_length": {
            "type": "integer",
            "description": "Maximum length of text to return (default: 8000)",
            "default": 8000,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def forward(self, url: str, max_length: Optional[int] = 8000) -> str:
        try:
            # Try to parse URL as JSON if it looks like a JSON string
            if url.strip().startswith('{') and url.strip().endswith('}'):
                try:
                    url_data = json.loads(url)
                    if isinstance(url_data, dict) and "url" in url_data:
                        url = url_data["url"]
                except json.JSONDecodeError:
                    pass  # If JSON parsing fails, use the original URL string
            
            # Add scheme if not present
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "meta", "link"]):
                element.decompose()
            
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up the text
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            # Truncate if necessary
            if max_length and len(text) > max_length:
                text = text[:max_length] + "...[truncated]"
            
            return text if text else "No content could be extracted from the webpage."
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing webpage content: {str(e)}") 