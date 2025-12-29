import asyncio
import os
import platform
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

load_dotenv()

MCP_FOLDER = r"C:\Users\shram\mcp"

def npx_command():
    return r"C:\Program Files\nodejs\npx.cmd" if platform.system().lower().startswith("win") else "npx"

async def chat(query: str) -> str:
    client = MultiServerMCPClient({
        "filesystem": {
            "transport": "stdio",
            "command": npx_command(),
            "args": ["-y", "@modelcontextprotocol/server-filesystem", MCP_FOLDER],
        }
    })
    
    tools = await client.get_tools()
    
    llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    llm_with_tools = llm.bind_tools(tools)
    
    messages = []
    messages.append(SystemMessage(content=f"All file operations are in: {MCP_FOLDER}"))
    messages.append(HumanMessage(content=query))
    
    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
        
        if not ai_msg.tool_calls:
            return ai_msg.content
        
        for tc in ai_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            tool_fn = next(t for t in tools if t.name == tool_name)
            tool_result = await tool_fn.ainvoke(tool_args)
            messages.append(ToolMessage(content=str(tool_result), tool_call_id=tc["id"]))

response = asyncio.run(chat("create a file named python.txt with content 'Hello, World!'"))
print(response)