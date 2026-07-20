#!/usr/bin/python3
import asyncio
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os

# load environment varibales
load_dotenv()

# the llm setup---> take note of the model_name that has vision
api_key=os.getenv("GITHUB_TOKEN")

#create llm
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)


# ----step 2: URL to our remote mcp server(HTTP)
DEEPWIKI_MCP_URL= "https://mcp.deepwiki.com/mcp"

# system prompt that tells the model what tools it has and how to behave
SYSTEM_PROMPT=(
    "You are a helpful assistance with access to tools for checking the current time" \
    "counting words, image content description, and looking up information about Github repositories" \
    "Use tools when the user's request needs information you don't already have." \
    "If a tool returns an erro, tell the user plainly and do not retry with made up arguments" \
    "If a question does not need a tool, just answer directly."
)

# ----Step 3: Call function in main to build the Agent with tools
async def build_agent(client:MultiServerMCPClient):
    # load tools from all connected MCP servers
    # This is async because MCP communication happens over I/O
    tools=await client.get_tools()
    # display on screen the loaded tools
    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    # build the agent with all MCP tools
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

async def main():
    # Create one MCP Client that connects to two servers
    #
    # 1. "tools" is our local MCP server started as a subprocess over stdio.
    #   > LangChain will launch "python mcp_server.py" for use
    # 2. "deepwiki" is a remote MCP server we connect to over HTTP

    client=MultiServerMCPClient({
        "tools": {
            "command":"python",
            "args":["mcp_server.py"],
            "transport":"stdio",
        },
        "deepwiki":{
            "url":DEEPWIKI_MCP_URL,
            "transport":"streamable_http",
        }
    })

    # Build the agent after the MCP client is ready and tools are loaded
    agent=await build_agent(client)

    print("*****************************************")
    print("         AGENT_MCP           ")
    print("*****************************************")
    print("\nReady! Ask the agent something.")
    print("Type 'exit' / 'quit' to terminate")

    # ---step 4: User interactive CLI
    while True:
        question=input("You: ").strip()

        # check if user wants to terminate session by there input
        if not question or question.lower() in {"exit", "quit"}:
            break
        
        # Send the user's message to the agent
        # we use "ainvoke()" because AI may call async MCP tools
        result=await agent.ainvoke({
            "messages":[{"role":"user", "content": question}]
        })

        # We walk through a returned messages and print any tool calls
        # the agent made during this turn
        for msg in result['messages']:
            tool_calls=getattr(msg, "tool_calls", None)
            if tool_calls:
                for call in tool_calls:
                    print(f"[tool call] {call['name']}({call['args']})")

        # The final message in the list is the agent's final answer
        print(f"\nAnswer: {result['messages'][-1].content}\n")


if __name__=="__main__":
    # Run the async program
    asyncio.run(main())

"""
6_FastMCP/tutorial_2>python agent_with_mcp.py
Loaded 6 tools: ['current_time', 'word_count', 'image_info', 'ask_question', 'read_wiki_contents', 'read_wiki_structure']
*****************************************
         AGENT_MCP
*****************************************

Ready! Ask the agent something.
Type 'exit' / 'quit' to terminate
You: Hey

Answer: It's nice to meet you. Is there something I can help you with or would you like to chat?

You: what is the current time here
[tool call] current_time({})

Answer: The current time is 08:50:52.

You: What tools do you have access to?

Answer: I have access to the following tools:

1. Current Time: I can retrieve the current local date and time.
2. Word Count: I can count the number of words in a given piece of text.
3. Image Info: I can provide a description of the content of an image, given the path to the image.
4. GitHub Repository Info: I can ask questions about a GitHub repository and receive an AI-powered response.
5. GitHub Wiki Contents: I can view the documentation about a GitHub repository.
6. GitHub Wiki Structure: I can retrieve a list of documentation topics for a GitHub repository.

I can use these tools to assist with tasks such as answering questions, providing information, and completing tasks that require external data or processing.


## Changing the Model to GPT from groq llama models:
*****************************************
         AGENT_MCP
*****************************************

Ready! Ask the agent something.
Type 'exit' / 'quit' to terminate
You: Answer the questions from the image "J:\11_Voice_Assistant\6_FastMCP\tutorial_2\my_quiz.png"
[tool call] image_info({'image_path': 'J:\\11_Voice_Assistant\\6_FastMCP\\tutorial_2\\my_quiz.png'})

Answer: Here are the answers for the "Python Quick Quiz":

1. **Define Python in one line:**
   Python is a high-level, interpreted programming language known for its simplicity and readability, used for a wide range of applications.

2. **Difference between variable and constant in one line:**
   A variable can change its value during program execution, whereas a constant has a fixed value that cannot be altered once assigned.

3. **Write code to get input from the user and add the two numbers:**
   ```python
   # Code to add two numbers entered by the user
   num1 = float(input("Enter first number: "))
   num2 = float(input("Enter second number: "))
   result = num1 + num2
   print("The sum is:", result)
   ```

You: exit
"""