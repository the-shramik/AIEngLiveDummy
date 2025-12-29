import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

load_dotenv()


async def chat(query: str) -> str:
    client = MultiServerMCPClient(
        {
           "telusko": {
            "transport": "sse",
            "url": "http://127.0.0.1:8000/sse"
           }
        }
    )

    tools = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content="Use tools when needed."),
        HumanMessage(content=query),
    ]

    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            return ai_msg.content

        for tc in ai_msg.tool_calls:
            tool_fn = next(t for t in tools if t.name == tc["name"])
            tool_result = await tool_fn.ainvoke(tc["args"])
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

response = asyncio.run(chat("Current time in the country where messi visited in Dec 2025"))

print(response)
