#!/usr/bin/python3
from datetime import datetime
from fastmcp import FastMCP
from simpleeval import simple_eval


# create an MCP object
mcp=FastMCP("Calculator")

# The decorator tuns our function to a tool
@mcp.tool
def calculate(expression: str)-> str:
    """
    Safely evaluate a mathematical expression
    Returns a string suitable for an llm
    """
    # Docstring provides tool description to the LLM
    try:
        # pass the expression from the LLM here
        result=simple_eval(expression)
        return f"""
Calculation
Expression: {expression}

Result: {result}
"""
    except Exception as e:
        return f"Calculation Error: {e}"

if __name__=="__main__":
    # run the MCP in stdio transport mode
    mcp.run()
