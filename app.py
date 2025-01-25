from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent
import os
from dotenv import load_dotenv
from bing_search import BingSearchTool
from scrape_tool import ScrapeTool
from browser_tool import BrowserTool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# get keys from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
bing_subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")

# Initialize the LLM for browser tool
browser_llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)

# Initialize the tools
bing_search_tool = BingSearchTool(api_key=bing_subscription_key)
scrape_tool = ScrapeTool()
browser_tool = BrowserTool(llm=browser_llm)

model = LiteLLMModel(model_id="openai/gpt-4o-mini", api_key=openai_api_key)

agent = CodeAgent(model=model, tools=[bing_search_tool, scrape_tool, browser_tool])

def main():
    result = agent.run("Use the browser tool to find the cheapest laptop on bol.com. Ensure I can see the browser window.")
    print(result)

if __name__ == "__main__":
    main()
    