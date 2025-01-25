from smolagents import Tool
from browser_use import Agent, Browser, BrowserConfig
from typing import Optional

class BrowserTool(Tool):
    name = "browser_automation"
    description = """
    This tool uses a browser to get information from a website.
    It can navigate websites, fill forms, click buttons, and extract information.
    Perfect for web automation tasks and data extraction from dynamic websites.
    Use it when users want to get information directly from a website and interaction
    with the website is required. If no interaction is required, use the search and scrape tool.
    """
    
    inputs = {
        "task": {
            "type": "string",
            "description": "The browser automation task to perform in natural language",
        },
        "headless": {
            "type": "boolean",
            "description": "Whether to run the browser in headless mode (default: True)",
            "default": True,
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self, llm):
        super().__init__()
        self.llm = llm
        
    def forward(self, task: str, headless: bool = True) -> str:
        # Create an async function and run it in the event loop
        async def _run_browser():
            config = BrowserConfig(
                headless=headless,
                disable_security=True
            )
            
            browser = Browser(config)
            
            try:
                agent = Agent(
                    task=task,
                    llm=self.llm,
                    browser=browser
                )
                result = await agent.run()
                return result
                
            except Exception as e:
                raise Exception(f"Browser automation failed: {str(e)}")
            finally:
                await browser.close()
        
        # Run the async function in an event loop
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(_run_browser()) 