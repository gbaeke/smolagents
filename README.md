# AI Web Assistant

A Python-based AI assistant that combines web search, browser automation, and web scraping capabilities to help users find information online.

## Features

- 🔍 **Bing Search Integration**: Search the web using Bing's API
- 🌐 **Browser Automation**: Automate browser tasks using natural language commands
- 📑 **Web Scraping**: Extract data from websites
- 🤖 **AI-Powered**: Uses GPT-4 for natural language understanding and task execution

## Setup

1. Clone the repository and navigate into the project directory
2. Install dependencies with: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   - OPENAI_API_KEY=your_openai_key
   - BING_SUBSCRIPTION_KEY=your_bing_key
4. For telemetry, run `python -m phoenix.server.main serve` before running the agent
   - See https://huggingface.co/docs/smolagents/tutorials/inspect_runs for more information


Note: PDF generation requires WeasyPrint system dependencies. Check https://doc.courtbouillon.org/weasyprint/stable/index.html for more information.

## Usage

Run the assistant by providing your question as a command-line argument:

```
python app.py "your question in quotes"
```

Example commands:
- `python app.py "Find the cheapest laptop on bol.com"`
- `python app.py "Search for Python API tutorials"`
- `python app.py "Extract product information from a website"`

## How it Works

The assistant uses three main components:

1. **CodeAgent**: Orchestrates the tools and processes natural language commands
2. **Tools**:
   - `BingSearchTool`: Performs web searches
   - `BrowserTool`: Automates browser actions
   - `ScrapeTool`: Extracts web content
3. **LLM**: Uses GPT-4 to understand commands and generate responses

## Requirements

- Python 3.8+
- OpenAI API key
- Bing API key

## Notes

Token consumption can be high. For example, the query `Research the DeepSeek R1 LLM. Use at least 5 different sources and summarize what you learn. In addtion, find images that are related and list them as well in your answer. Create a PDF from the info you gathered` consumed a total of close to 50k tokens. This simply depends on the query and how the agent decides what tools to use.

If you use Phoenix Arize, you can see the traces in the UI:

![alt text](image.png)