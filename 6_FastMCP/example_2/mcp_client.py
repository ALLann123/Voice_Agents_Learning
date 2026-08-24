#!/usr/bin/python3
import asyncio   
from fastmcp import Client

# our function will be an asynchronous function:
# MCP transport is I/O bound and the async library lets our program
# wait for tool results without freezing the whole program
# Async library also allows the AI to run multiple tools concurrently
async def main():
    # we pass the localIP:port url that our server is listening on
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # Now list available tools
        tools=await client.list_tools()
        # iterate through the list of tools and display only there names
        print(f"Tools: {[t.name for t in tools]}") 

        # call the add tool
        result=await client.call_tool("add", {"a":3, "b":4})
        print(f"\nTool Result: {result}")

        # call the second tool(remember, it had no arguments)
        result=await client.call_tool("current_time")
        print(f"\nCurrent time result: {result}")

# run our function
asyncio.run(main())

"""
====Dont add. This is my result when writing the tool==
example_2>python mcp_client.py
Tools: ['add', 'current_time']

Tool Result: CallToolResult(content=[TextContent(type='text', text='7', annotations=None, meta=None)], structured_content={'result': 7}, meta={'fastmcp': {'wrap_result': True}}, data=7, is_error=False)

Current time result: CallToolResult(content=[TextContent(type='text', text='2026-08-23 19:54:50', annotations=None, meta=None)], structured_content={'result': '2026-08-23 19:54:50'}, meta={'fastmcp': {'wrap_result': True}}, data='2026-08-23 19:54:50', is_error=False)

"""