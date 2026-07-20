#!/usr/bin/python3
from fastmcp import FastMCP

# Creates an MCP server
mcp=FastMCP("My First Server")

# python decorator-->expose the function as a tool.
# without it AI will never know it is a tool
@mcp.tool()
def hello(): #our function which is a tool now for an AI
    """Say Hello"""   # Docstring---> AI reads it to know when to use the tool
    return "Hello from FastMCP!"  # the returned data from the tool to the AI

# We can have multiple tools
@mcp.tool()
def calculator(a: int, b: int)-> int:
    """Add two numbers"""
    return a + b

# We can have data thats not a string but a dictionary or a list
@mcp.tool()
def student():
    """Return the student information"""
    # our dictionary. In a real world scenario this queries the data base.
    return {
        "name":"Allan",
        "course":"computing scnience",
        "year":2
    }

if __name__=="__main__":
    # Starts the MCP server.
    mcp.run(transport="http", host="127.0.0.1", port=8000)


"""
le_1>python server.py


                                           ┌──────────────────────────────────────────────────────────────────────────────┐
                                           │                                                                              │
                                           │                                                                              │
                                           │                         ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█                        │
                                           │                         █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀                        │
                                           │                                                                              │
                                           │                                                                              │
                                           │                                                                              │
                                           │                                FastMCP 3.4.4                                 │
                                           │                            https://gofastmcp.com                             │
                                           │                                                                              │
                                           │                  🖥   Server:      My First Server, 3.4.4                      │                                            
                                           │                  🚀 Deploy free: https://horizon.prefect.io                  │
                                           │                                                                              │
                                           └──────────────────────────────────────────────────────────────────────────────┘


[07/18/26 00:17:29] INFO     Starting MCP server 'My First Server' with transport 'http' on http://127.0.0.1:8000/mcp                                  transport.py:361
←[32mINFO←[0m:     Started server process [←[36m3364←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
"""
