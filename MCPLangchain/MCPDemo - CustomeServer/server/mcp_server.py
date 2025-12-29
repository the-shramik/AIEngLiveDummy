from fastmcp import FastMCP
from datetime import datetime

from langchain_community.tools import DuckDuckGoSearchRun

mcp = FastMCP("TeluskoTools")

search_tool = DuckDuckGoSearchRun()

@mcp.tool()
def get_current_date_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    return search_tool.run(query)


mcp.run(transport="sse", host="127.0.0.1", port=8000)

