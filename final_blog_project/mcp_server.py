#!/usr/bin/python3
from datetime import datetime
from fastmcp import FastMCP
from simpleeval import simple_eval
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from firecrawl import FirecrawlApp
from typing import Literal
import psutil

# user defined function here. Located in the tools directory
from tools.vision import describe_image
from tools.weather import get_weather

# ----------Loads APIs Accessible to our Program----------
#loads environment variables. Our APIs in .env file to be accessible here
load_dotenv()  

# we get the Tavily API here--> use os library and save to a variable
tavily_client=TavilyClient(api_key=os.getenv("TAVILLY_API")) # Tavily

# firecrawl setup. Get API key using OS library and save to a variable
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
# ability to describe images. We wrote the code in the tools directory "vision.py"
@mcp.tool
def image_info(image_path: str)-> str:
    """
    Use this when user wants to know what the image entails
    User must have provided the path to where the image is
    The image can be on the web via URL or on local machine
    Returns the description of the image content
    """
    # call the function that will carry this task
    try:
        # call our "vision.py" function we have imported from tools
        result=describe_image(image_path)
        # return the result gotten from the model
        return result

    except Exception as e:
        return f"Image Description Error: {e}"

# ----4. Tavily Search Tool
@mcp.tool
def internet_search(
    query: str,
    max_results: int=3,
    topic: Literal["general", "news", "finance"] = "general", # Literal forces LLM to choose 1 from the 3 in the List
    include_raw_content:bool=False,
):
    """Run a web search"""
    try:
        return tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
    except Exception as e:
        return f"Web Search Error: {e}"

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
    try:
        result=get_weather(city)
        return result
    except Exception as e:
        return f"Weather tool Error: {e}"

# ----7. System Info
@mcp.tool
def system_info()-> list[str]:
    """
    Get the current CPU, RAM, and disk usage of the computer
    """
    usage=[]
    # CPU usage
    cpu_usage = f"CPU Usage: {psutil.cpu_percent()}%"
    usage.append(cpu_usage)

    # RAM usage
    memory = psutil.virtual_memory()
    ram_usage = f"RAM Usage: {memory.percent}%"
    usage.append(ram_usage)

    # Disk usage
    disk = psutil.disk_usage("/")
    disk_usage = f"Disk Usage: {disk.percent}%"
    usage.append(disk_usage)

    return usage

if __name__=="__main__":
    # run the MCP server over stdio
    mcp.run()
    


