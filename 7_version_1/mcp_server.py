#!/usr/bin/python3
from datetime import datetime
from fastmcp import FastMCP
from simpleeval import simple_eval
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from firecrawl import FirecrawlApp
# user defined function here. Located in the tools directory in pwd
from tools.vision import describe_image
from tools.weather import get_weather

# ----------Loads APIs Accessible to our Program----------
load_dotenv()  #loads environment variables
client=TavilyClient(api_key=os.getenv("TAVILLY_API")) # Tavily

# firecrawl setup
app=FirecrawlApp(api_key=os.getenv("FIRECRAWL"))
#---------------------------------------------------------

# create an MCP object from the class
mcp=FastMCP("local-tools")

#-----1. Time tool
# the decorator turns our function into a tool
@mcp.tool
def current_time()-> str:
    """
    Return the current local date and time
    Use this when the user asks what time or date it is
    """
    # Docstring provides tool description to the LLM
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#----2: Calculator to solve expressions
#Next tool will be a calculator. Can solve complex maths equations
@mcp.tool
def calculate(expression: str)-> str:
    """
    Safely evaluate a mathematical expression
    Returns a string suitable for an LLM
    """
    try:
        # pass the expression from an LLM here
        result=simple_eval(expression)
        return f"""
Calculation

Expression: {expression}
Result: {result}
"""
    except Exception as e:
        return f"Calculation Error: {e}"
    
#----3. Vision into images
# ability to describe images
@mcp.tool
def image_info(image_path: str)-> str:
    """
    Use this when user wants to know what the image entails
    User must have provided the path to where the image is
    The image can be on the web via URL or on local machine
    Returns the description of the image content
    """
    # call the function that will carry this task
    result=describe_image(image_path)
    return result

# ----4. Ability to Perform Web-Search using Tavily
@mcp.tool
def web_search(query: str)-> str:
    """
    Search the web using Tavily and return a formatted string
    suitable for an LLM
    """

    response=client.search(
        query=query,
        search_depth="advanced",
        max_results=3
    )

    results=response.get("results", [])

    #if result is empty
    if not results:
        return "No relevant search results were found"
    
    # ----This is done for proper formating to the LLM
    output=f"Search Query: {query}\n\n"
    output+="Search Result:\n\n"

    for i, result in enumerate(results, start=1):
        output+=(
            f"Result {i}\n"
            f"Title: {result.get('content')}\n"
            f"URL: {result.get('url')}\n\n"
            f"Content: {result.get('content')}\n\n"
        )

    return output 


# ----5. Scrape Webpage and return result in markdown
@mcp.tool
def scrape_webpage(url: str)-> str:
    """
    Read a webpage and return clean markdown suitable for an LLM
    """
    # Send our request and store the markdown data
    response=app.scrape_url(
        url=url,
        formats=["markdown"]
    )

    markdown=getattr(response, "markdown", "")

    # if the response is empty
    if not markdown:
        return "Unable to extract content from the webpage."
    
    return f"""
Source URL: 
{url}

Extracted Content:
{markdown}
"""

# -----6. Weather forecast
@mcp.tool
def weather_forecast(city: str)-> str:
    """
    Use this tool when you have the city/Town name you want to look
    up for the current weather conditions
    """
    # call our function
    result=get_weather(city)
    return result


if __name__=="__main__":
    # run the MCP server over stdio
    mcp.run()
    


