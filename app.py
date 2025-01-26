from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent
import os
import sys
from dotenv import load_dotenv
from tools.bing_search import BingSearchTool
from tools.scrape_tool import ScrapeTool
from tools.browser_tool import BrowserTool
from tools.pdf_tool import PDFTool
from langchain_openai import ChatOpenAI

def print_usage():
    print("\nUsage: python app.py \"your question in quotes\"")
    print("\nExample:")
    print("  python app.py \"Find the cheapest laptop on bol.com\"")
    print("  python app.py \"Search for Python tutorials\"")
    sys.exit(1)

def main():
    # Check if a question was provided
    if len(sys.argv) != 2:
        print("\nError: Please provide a question as a command-line argument.")
        print_usage()

    # Get the question from command line
    question = sys.argv[1]

    # Load environment variables from .env file
    load_dotenv()

    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY not found in .env file")
        sys.exit(1)
    if not os.getenv("BING_SUBSCRIPTION_KEY"):
        print("\nError: BING_SUBSCRIPTION_KEY not found in .env file")
        sys.exit(1)

    # get keys from .env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    bing_subscription_key = os.getenv("BING_SUBSCRIPTION_KEY")

    # Initialize the LLM for browser tool
    browser_llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key)

    # Initialize the tools
    bing_search_tool = BingSearchTool(api_key=bing_subscription_key)
    scrape_tool = ScrapeTool()
    browser_tool = BrowserTool(llm=browser_llm)
    pdf_tool = PDFTool()

    model = LiteLLMModel(model_id="openai/gpt-4o-mini", api_key=openai_api_key, max_tokens=4096)

    agent = CodeAgent(model=model, tools=[bing_search_tool, scrape_tool, browser_tool, pdf_tool])

    result = agent.run(question)
    print(result)

if __name__ == "__main__":
    main()
    