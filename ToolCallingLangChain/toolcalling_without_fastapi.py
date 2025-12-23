import os
import requests

from dotenv import load_dotenv
from datetime import datetime

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_community.agent_toolkits.load_tools import load_tools


from zoneinfo import ZoneInfo


load_dotenv()

@tool("get_current_local_time")
def get_current_local_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool("get_current_time")
def get_current_time(timeZone: str) -> str:
    """Get current time in the given timezone. Example: Europe/London"""
    return datetime.now(ZoneInfo(timeZone)).strftime("%I:%M %p")


@tool("get_news_headlines")
def get_news_headlines(topic: str) -> str:
    """Get latest news headlines for a topic"""

    api_key = os.getenv("NEWS_API_KEY")

    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    articles = data["articles"][:5]  # take first 5 news

    news = []
    for article in articles:
        news.append(article["title"])

    return "\n".join(news)

google_search_tool = load_tools(["google-serper"])[0]  # inbuilt tool :contentReference[oaicite:2]{index=2}


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def call_agent(user_message: str, tools: list, rule: str = "") -> str:
    # 1) Tell LLM which tools it can use
    llm_with_tools = llm.bind_tools(tools, tool_choice="required")

    # 2) Create conversation messages
    messages = []
    if rule:
        messages.append(SystemMessage(content=rule))
    messages.append(HumanMessage(content=user_message))

    # 3) LLM decides which tool to call
    ai_message = llm_with_tools.invoke(messages)

    # 4) Take the first tool call
    tool_call = ai_message.tool_calls[0]
    tool_name = tool_call["name"]
    tool_input = tool_call["args"]

    # 5) Find that tool in our tools list
    tool_function = next(t for t in tools if t.name == tool_name)

    # 6) Run the tool
    tool_output = tool_function.invoke(tool_input)

    # 7) Send tool output back to LLM for final answer
    messages.append(ai_message)
    messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))

    final_answer = llm.invoke(messages).content
    return final_answer


print(call_agent(
    "What is the current time?",
    tools=[get_current_local_time],
    rule="Always call get_current_local_time to answer."
))

print("=============================================================================================================================")

print(call_agent(
    "What time is it in Europe/London?",
    tools=[get_current_time],
    rule="Always call get_current_time to answer."
))

print("=============================================================================================================================")

print(call_agent(
    "Give me latest news about india",
    tools=[get_news_headlines],
    rule="Always call get_news_headlines."
))

print("=============================================================================================================================")

print(call_agent(
    "Search Google: latest AI tools in 2025",
    tools=[google_search_tool],
    rule="Always use the google-serper tool."
))