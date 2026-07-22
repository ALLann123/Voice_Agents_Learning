#!/usr/bin/python3
import asyncio
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os

# load envionment variables
load_dotenv()

# the llm setup
api_key=os.getenv("GITHUB_BRO")

# setup
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)


# System Prompt that tells the model what tools it has and how to behave
SYSTEM_PROMPT=(
    "You are a helpful assistant with access to tools for checking the current" \
    "time, calculations, image content description, web search, webpage scraping and" \
    "a weather tool. Use tools when the user's request needs information you dont" \
    "already have. If the tool returns an error, tell user plainly and do not retry" \
    "with made up arguments. If a question does not need a tool answer directly"
)


# ---Step 3: Call function in main to build the Agent with tools
async def build_agent(client:MultiServerMCPClient):
    # load tools from all connected MCP servers
    # This is async because MCP communication happens over I/O
    tools=await client.get_tools()

    #display on screen the loaded tools
    print(f"Loaded {len(tools)} tools:{[t.name for t in tools]}")

    # build the agent with all MCP tools
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

async def main():
    # Create one MCP client connecting to our local MCP server
    # The MCP server uses subprocess over stdio. WIll be run by the agent

    client=MultiServerMCPClient({
        "tools":{
            "command":"python",
            "args":["mcp_server.py"],
            "transport":"stdio",
        }
        # if we had a remote mcp server we would add here 
        # transport type will be "http"
    })

    # Build the agent after the MCP client is ready and tools are loaded
    agent=await build_agent(client)

    print("*****************************************")
    print("         AGENT_MCP           ")
    print("*****************************************")
    print("\nReady! Ask the agent something")
    print("Type 'exit'/ 'quit' to terminate")

    # User CLI
    while True:
        question=input("You: ").strip()

        # check if user wants to terminate session 
        if not question or question.lower()in{"exit", "quit"}:
            break
        
        # Send the user's message to the agent
        # we use "ainvoke()" because AI may call async MCP tools
        result=await agent.ainvoke({
            "messages":[{"role":"user", "content":question}]
        })

        # we walk through a returned messages and print any tool calls
        # the agent made during this turn
        for msg in result['messages']:
            tool_calls=getattr(msg, "tool_calls", None)
            if tool_calls:
                for call in tool_calls:
                    print(f"[tool call] {call['name']}({call['args']})")

        # final message from the list of agent final answer
        print(f"\nAnswer: {result['messages'][-1].content}\n")


if __name__=="__main__":
    asyncio.run(main())



"""
7_version_1>python agent_connect.py
Loaded 6 tools:['current_time', 'calculate', 'image_info', 'web_search', 'scrape_webpage', 'weather_forecast']
*****************************************
         AGENT_MCP
*****************************************

Ready! Ask the agent something
Type 'exit'/ 'quit' to terminate
You: Hey

Answer: Hello! How can I assist you today?

You: I am arriving in Nairobi Kenya in a few minutes, what is the time and can you reccomend if I should wear heavy cloths or light cloths depending on the weather
[tool call] current_time({})
[tool call] weather_forecast({'city': 'Nairobi, Kenya'})

Answer: The current time in Nairobi, Kenya, is 12:01 AM (past midnight), and the weather is cool. The temperature is 16.77°C (about 62°F) with overcast clouds, 73% humidity, and a light wind speed of 3.21 m/s.

Given the cool conditions, I suggest wearing moderately warm clothes, such as a light sweater or jacket, to stay comfortable.

You: Which world cup match is playing right now and the location it is playing at. Can we check the weather there
[tool call] web_search({'query': 'current FIFA World Cup match and location'})
[tool call] weather_forecast({'city': 'Atlanta, Georgia'})

Answer: The current FIFA World Cup match being played is between England and Argentina. It is taking place at the Mercedes-Benz Stadium in Atlanta, Georgia.

The current weather in Atlanta is approximately 33.08°C with 51% humidity, broken cloud conditions, and a light wind speed of 0.89 m/s.

You: solve this for me "J:\11_Voice_Assistant\7_version_1\my_quiz.png" and provide answers
[tool call] image_info({'image_path': 'J:\\11_Voice_Assistant\\7_version_1\\my_quiz.png'})

Answer: Here are the answers to the "Python Quick Quiz":

1. **Define Python in one line**:
   Python is a high-level, interpreted, and dynamically-typed programming language widely used for web development, data analysis, artificial intelligence, and more.

2. **Difference between a variable and a constant in one line**:
   A variable's value can be changed during the execution of a program, while a constant's value remains the same throughout the program.

3. **Code to get input from the user and add the two numbers**:
   ```python
   # Python code to get user input and add two numbers
   num1 = int(input("Enter the first number: "))
   num2 = int(input("Enter the second number: "))
   result = num1 + num2
   print("The sum is:", result)
   ```

You: What is the blog about in one statement:"https://medium.com/@karisallan237/steganography-kali-linux-3742519790f1"
[tool call] scrape_webpage({'url': 'https://medium.com/@karisallan237/steganography-kali-linux-3742519790f1'})

Answer: The blog "Steganography-Kali Linux" on Medium provides a beginner-friendly guide to using the Steghide tool on Kali Linux for hiding and extracting data within image files, including instructions on bruteforcing steganography-protected files and addressing capture-the-flag challenges like decoding Atbash cipher.

You: Get the date today and answer this. I had there was a by election recently in Kenya. Where was it and who won?
[tool call] current_time({})
[tool call] web_search({'query': 'recent by-election in Kenya July 2026 location and winner'})

Answer: The recent by-election in Kenya took place in Emurua Dikirr constituency. David Keter, the candidate from the United Democratic Alliance (UDA), was declared the winner with 18,266 votes.

You:
"""