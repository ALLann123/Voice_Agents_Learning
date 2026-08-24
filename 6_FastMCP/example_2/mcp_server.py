#!/usr/bin/python3
from fastmcp import FastMCP     # our library
from datetime import datetime  # used in our second tool

# create an object from the library
mcp=FastMCP("Demo🚀🚀")

# Python decorator--> from the FastMCP library
# The "@" decorator below exposes the function as a tool
@mcp.tool
def add(a:int, b:int)-> int:
    """
    Add two Numbers.
    """
    # the above is a Python DocString--> AI reads it to know when to use the tool

    return a+b

# lets add another tool
@mcp.tool
def current_time()-> str:
    """
    Returns the current local date and time
    """

    # call the datetime library to get this
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__=="__main__":
    # We now change the mode of transport to http from the default stdio 
    mcp.run(transport="http", host="127.0.0.1", port=8000)


