#!/usr/bin/python3
from fastmcp import FastMCP
import os
from tavily import TavilyClient
from typing import Literal
from dotenv import load_dotenv

# load our APIs from .env file
load_dotenv()

# create an object from the class
tavily_client=TavilyClient(api_key=os.getenv("TAVILLY_API"))#set our API

# create an object from the class
mcp=FastMCP("local-tools")

# ----1. Our search tool
# we a python decorator below. Turns a normal python function into a tool
@mcp.tool
def internet_search(
    query: str,
    max_results: int=5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content:bool=False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


# run the MCP server over stdio
if __name__=="__main__":
    mcp.run()