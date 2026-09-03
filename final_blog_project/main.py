#!/usr/bin/python3
import asyncio
from typing import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver  
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# This are our user defined libraries from tts.py and stt.py
from stt import listen
from tts import speak


# our env variables loaded here
load_dotenv()

# Set up our LLM-> If you have GPT API comment this out
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b",
    reasoning_effort="low"
)

# Comment our GPT if you dont have API and use the free Groq. 
"""
llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=os.getenv("GPT_5")
)
"""

# We need this of Groq to prevent the model from hallucinating. GPT will work fine with a smaller prompt
SYSTEM_PROMPT = """
You are Called Botnet, a concise voice assistant. Your replies are spoken aloud, not read.
 
Tools: pick the single right tool, follow its schema exactly, never invent arguments, never repeat a successful call, never fabricate results. If a tool fails and can't be fixed, say so.
 
Speaking style: talk like a person, not a document. No emojis, no markdown, no symbols like * # - _ / \\ | ~ < > or brackets. Say numbers and dates the way you'd speak them. Use only periods, commas, and question marks. Answer only what was asked, in 1 to 3 sentences unless more detail is truly needed.
"""


# -----Our State: 'add_messages' is the reducer that appends new messages rather
# than overwritingt the list on each update.
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# Remember Part 1 communicaion to the MCP server is asynchronous communication
async def main():
    # 1. Configure MCP server connections
    # We are using stdio because it is running locally
    client=MultiServerMCPClient(
        {
            "tools":{
                "transport":"stdio",
                "command":"python",
                "args":["mcp_server.py"], 
            },
            # If we had a remote one:
            # "wikipedia":{
            #       "transport":"streamable_http",
            #       "url":"https://<domain/ServerIP>/mcp",
            #},
        }
    )
    # 2. Discover tools exposed by the connected MCP server
    # Each MCP tools is automatically wrapped as a LangChain BaseTool,
    # with name/description/schema taken from the server's tool spec.
    tools=await client.get_tools()
    tools_by_name={t.name: t for t in tools}

    #display on screen the loaded tools
    print(f"Loaded {len(tools)} tools:{[t.name for t in tools]}\n")
    speak("Welcome Sir!!")

    # Bind up our model
    llm_with_tools=llm.bind_tools(tools)

    # Node--> a python function to carry one task. 
    # Get user Speech Transcribed
    def get_input(state:AgentState)-> AgentState:
        """User inputs his command via microphone and they are transcribed to text"""
        text=listen()
        print(f"YOU Said: {text}")

        # the add_reducer function returns only the new messsage
        return {"messages":[HumanMessage(content=text)]}

    # Takes the last message now, the user input and executed using the LLM+MCP
    async def call_model(state: AgentState):
        """Call the LLM passing the user question"""
        messages=[SystemMessage(content=SYSTEM_PROMPT)]+state["messages"]
        response=await llm_with_tools.ainvoke(messages)
        # append our results to our state--> we are just adding new messages remember
        return {"messages":[response]}

    # The speaking node to take the last AI message and speak it
    def talk_back(state: AgentState):
        """Return the message as output voice"""
        text=state["messages"][-1].content
        print(f"AI: {text}")
        speak(text)
        #Node functions should return a state update even when empty to prevent error
        return {}

    # add our MCP server as a tool Node
    tool_node=ToolNode(tools)

    # Build our graph schema
    graph=StateGraph(AgentState)

    # Add our nodes
    graph.add_node("llm", call_model)
    graph.add_node("tools", tool_node)
    graph.add_node("listening", get_input)
    graph.add_node("speaking", talk_back)

    # add the edges-->control the next node to execute in the graph
    graph.set_entry_point("listening")
    graph.add_edge("listening", "llm")

    # here we have a conditional edge when our LLM needs a tool
    # tools_condition we imported will return "tools" if LLM asked for tools
    # or END otherwise.  Mapping END to speaking
    graph.add_conditional_edges(
        "llm", 
        tools_condition,
        {"tools":"tools", END:"speaking"}
    )

    # after tools run we loop back to LLM with the  result
    graph.add_edge("tools", "llm")

    # end execution
    graph.set_finish_point("speaking")

    # The memory we will use
    memory=MemorySaver()

    # compile the graph
    app=graph.compile(
        checkpointer=memory
    )

    # set the the thread id since we are using checkpointer memory
    config={
        "configurable":{
            "thread_id":"user1"
        }
    }

    while True:
        await app.ainvoke({"messages":[]}, config=config)


if __name__=="__main__":
    asyncio.run(main())

"""
===========Do Not add this Part: It is my CMD Output===========
final_Project>python main.py
Loaded 7 tools:['current_time', 'calculate', 'image_info', 'internet_search', 'scrape_webpage', 'weather_forecast', 'system_info']


🎤Listening...
YOU Said: hello, i am alan.
AI: Hello Alan. Nice to meet you. How can I help you today?

🎤Listening...
YOU Said: introduce yourself in three words.
AI: Helpful. Concise. Friendly.

🎤Listening...
YOU Said: i need to check the weather of a particular city.
AI: Sure, which city would you like the forecast for?

🎤Listening...
YOU Said: nairobi.
AI: The current weather in Nairobi is about twenty three degrees Celsius with broken clouds and moderate humidity.Let me know if you need a longer forecast or anything else.

🎤Listening...
YOU Said: okay, thanks.
AI: You’re welcome. Anything else I can do for you?

"""