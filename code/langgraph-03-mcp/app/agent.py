from llm import get_llm
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
from langchain_core.tools import tool
import asyncio


client = MultiServerMCPClient(  
        {
            "stock_api": {
                "transport": "http",  # HTTP-based remote server
                # MCP server url
                "url": "http://localhost:8086/mcp",
            }
        }
    )

async def get_tools():
    tools = await client.get_tools()  
    return tools

async def get_agent():
    # Await MCP tools
    tools = await client.get_tools() 
    llm = get_llm()
    # Create the Agent Executor
    agent = create_react_agent(llm, tools)
    return agent

def get_agent_sync():
    """Wrapper for Streamlit to call"""
    return asyncio.run(get_agent())




