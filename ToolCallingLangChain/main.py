from fastapi import FastAPI, Query
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

from tools_datetime import get_current_local_time, get_current_time
from tools_products import search_products
from tools_wishlist import save_to_wishlist, get_wishlist
from vectorstore import get_vectorstore

get_vectorstore()

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def call_agent(messages, tools):
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(messages)
    
    while response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Call the actual tool
        for tool in tools:
            if tool.name == tool_name:
                result = tool.invoke(tool_args)
                break
        
        # Add tool result to messages
        messages.append(response)
        messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
        
        # Get final response
        response = llm.invoke(messages)
    
    return response.content


@app.get("/api/tool/local-time")
def local_time(message: str = Query(...)):
    system = "You are a helpful assistant. Always call the getCurrentLocalTime tool to get the current time."
    messages = [SystemMessage(content=system), HumanMessage(content=message)]
    return call_agent(messages, [get_current_local_time, get_current_time])


@app.get("/api/tool/time")
def time(message: str = Query(...)):
    system = "You are a helpful assistant. Always call the getCurrentTime tool to get the current time."
    messages = [SystemMessage(content=system), HumanMessage(content=message)]
    return call_agent(messages, [get_current_local_time, get_current_time])


@app.get("/api/tool/products")
def products(query: str = Query(...)):
    system = """You are a product assistant for a small catalog.
    For any product question, call the tool `search_products` first.
    Answer ONLY using the tool results. If not found, say "I don't know"."""
    
    messages = [SystemMessage(content=system), HumanMessage(content=query)]
    return call_agent(messages, [search_products])


@app.get("/api/tool/wishlist")
def wishlist(message: str = Query(...), username: str = Query(...)):
    system = """You are an assistant that can save products.
    If the user asks to save/add/bookmark a product, call the tool `save_to_wishlist`.
    Always store the exact title mentioned by the user."""
    
    messages = [SystemMessage(content=system), HumanMessage(content=f"username={username}\n{message}")]
    return call_agent(messages, [save_to_wishlist])


@app.get("/api/tool/wishlist/view")
def view_wishlist(message: str = Query(...), username: str = Query(...)):
    system = "Always call the get_wishlist tool to retrieve the user's wishlist."
    messages = [SystemMessage(content=system), HumanMessage(content=f"username={username}\n{message}")]
    return call_agent(messages, [get_wishlist])