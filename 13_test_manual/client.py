#!/usr/bin/python3
import asyncio
from fastmcp import Client

# wait for tool results without freezing the application
async def main():
    # get the server name. Run it using stdio
    print("\n Testing MCP SERVER MANUALLY\n\n")
    async with Client("mcp_server.py") as client:
        # List tools
        tools=await client.list_tools()
        print(f"Tools: {[t.name for t in tools]}")

        # call all tools
        # 1. Time tool
        result=await client.call_tool("current_time")
        print(f"\nCurrent time result: {result}")

        # 2. Calculator tool.The second argument is a Dictionary like we see in the mcp server "key: value"
        result = await client.call_tool("calculate", {"expression": "25 * (18 + 7) / 5"})
        print(f"\n Calculator tool result: {result.data}")

        # 3. Weather tool. The second argument is a Dictionary like we see in the mcp server "key: value"
        result = await client.call_tool("weather_forecast", {"city": "London"})
        print(f"\nWeather tool result: {result}")

        # 4. Firecrawl Result. The second argument is a Dictionary like we see in the mcp server "key: value"
        result = await client.call_tool("scrape_webpage", {"url": "https://medium.com/@karisallan237/tor-network-proxy-c7d45eb0ba3a"})
        print(f"\n\nScrape tool result: {result}")

# run main function
asyncio.run(main())

"""
==========Dont Add this. It is my Program Result==========
13_test_manual>python client.py

 Testing MCP SERVER MANUALLY


Tools: ['current_time', 'calculate', 'image_info', 'internet_search', 'scrape_webpage', 'weather_forecast']

Current time result: CallToolResult(content=[TextContent(type='text', text='2026-08-26 11:58:10', annotations=None, meta=None)], structured_content={'result': '2026-08-26 11:58:10'}, meta={'fastmcp': {'wrap_result': True}}, data='2026-08-26 11:58:10', is_error=False)

 Calculator tool result:
Calculation

Expression: 25 * (18 + 7) / 5
Result: 125.0


Weather tool result: CallToolResult(content=[TextContent(type='text', text='\n    Current Weather Report\n\n    Location: London\n    Temperature: 21.96°C\n    Humidity: 78%\n    Conditions: scattered clouds\n    Wind Speed: 2.9 m/s\n    ', annotations=None, meta=None)], structured_content={'result': '\n    Current Weather Report\n\n    Location: London\n    Temperature: 21.96°C\n    Humidity: 78%\n    Conditions: scattered clouds\n    Wind Speed: 2.9 m/s\n    '}, meta={'fastmcp': {'wrap_result': True}}, data='\n    Current Weather Report\n\n    Location: London\n    Temperature: 21.96°C\n    Humidity: 78%\n    Conditions: scattered clouds\n    Wind Speed: 2.9 m/s\n    ', is_error=False)


Scrape tool result: CallToolResult(content=[TextContent(type='text', text='\nSource URL: \nhttps://medium.com/@karisallan237/tor-network-proxy-c7d45eb0ba3a\n\nExtracted Content:\n[Sitemap](https://medium.com/sitemap/sitemap.xml)\n\n[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=---top_nav_layout_nav-----------------------------------------)\n\nSign up\n\n[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40karisallan237%2Ftor-network-proxy-c7d45eb0ba3a&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)\n\n[Medium Logo](https://medium.com/?source=---top_nav_layout_nav-----------------------------------------)\n\nGet app\n\n[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)\n\n[Search](https://medium.com/search?source=---top_nav_layout_nav-----------------------------------------)\n\nSign up\n\n[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F%40karisallan237%2Ftor-network-proxy-c7d45eb0ba3a&source=post_page---top_nav_layout_
"""