#!/usr/bin/python3
from datetime import datetime
from fastmcp import FastMCP
# user defined function for image description
from vision import describe_image

# create an object from the class
mcp=FastMCP("local-tools")

# the decorator turns our function into a tool
@mcp.tool
def current_time()-> str:
    """
    Return the current local date and time
    Use this wehn the user asks what time or date it is
    """
    # the above Docstring provides tool description to the llm
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# our next tool
@mcp.tool
def word_count(text: str)-> int:
    """
    Count the number of words in a piece of text
    Use this when the user asks how long a piece of writing is or
    asks you to count the words in something they've shared.
    Returns the word count as an integer
    """
    return len(text.split())

# add our extra tool---> Image description using a free model
@mcp.tool
def image_info(image_path: str)-> str:
    """
    Use this when user wants to know what the image entails
    User must have provided the path to where the image is
    Returns the description of the image content
    """
    # call our function that will carry this task
    result=describe_image(image_path)
    return result

if __name__=="__main__":
    # run the MCP server over stdio
    mcp.run()

