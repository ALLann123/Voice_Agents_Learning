#!/usr/bin/python3
from datetime import datetime
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph import add_messages
from langgraph.prebuilt import ToolNode
from typing import Annotated
from typing_extensions import TypedDict
# import a helper conditional routing
from langgraph.prebuilt import tools_condition
# add memory using
from langgraph.checkpoint.memory import MemorySaver

# load our .env file to this file
load_dotenv()

# Our state schema
class AgentState(TypedDict):
    # messages returned by the individual nodes are appended here
    messages: Annotated[list, add_messages]

# add the tools.
# '@' decorator turns our function to a tool
@tool
def current_time():
    """Return the current local time."""
    return datetime.now().strftime("%H:%M:%S")

# add our tools to a list in order to bind them to the llm
tools=[
    current_time, # we have one tool
]

# set up our Groq LLM
#- remember the groq API we used in building vision.py in Part 1. We can use  that
#- Add the API key to a .env file like we did

llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"   # our model in here we pick this. 
)
"""
llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=os.getenv("GPT_5")
)
"""

# Bind our tools to the model
llm_with_tools=llm.bind_tools(tools)


# Add a Node
def chatbot(state:AgentState)-> AgentState:
    """Send in messages to our LLM"""
    # call the LLM
    response=llm_with_tools.invoke(state["messages"])

    # append our LLM response to our state
    return {
        "messages":[response]
    }

# Buiild the graph blueprint
graph=StateGraph(AgentState)

# add nodes
graph.add_node("chatbot", chatbot)
graph.add_node("tools", ToolNode(tools))  # we covered this

# Add edges--> Tells the graph what to execute next.
graph.set_entry_point('chatbot')

# Decides if the LLM needs a tool
graph.add_conditional_edges(
    'chatbot',
    tools_condition, # we imported this
)

# Bring back execution to the LLM after running chatbot
graph.add_edge('tools', 'chatbot')
graph.set_finish_point('chatbot')

# ---NOW add memory to our graph
memory=MemorySaver()

# turn graph to an executable
app=graph.compile(
    checkpointer=memory,
)

# After adding memory we need to set up the threat_id
# Each conversation has a different thread_id and LangGraph will
# call each one with its unique id
config={
    "configurable":{
        "thread_id":"user1"
    }
}

# lets test if our agent responds
while True:
    user_input=input("\nYOU: ")

    # check if exit or quit and terminate program
    if user_input =='exit' or user_input == 'quit':
        print("\nGoodbye!")
        break

    elif user_input=='':
        # if user input is empty restart the infinity loop
        continue

    # invoke our graph
    response=app.invoke(
        {
            "messages":[
                HumanMessage(content=user_input)
            ]
        }, 
        config=config # add our checkpointer here 
    )

    # display output
    print(f"AI🤖: {response['messages'][-1].content}") # retrieve the last message in our dictionary


"""
============Do not Add: This is my CMD results===================
agent_mem_tool>python agent_memory_tool.py

YOU: Hey, I am Fred a CS student. I love skating
AI🤖: Hey Fred! 👋 Great to meet a fellow CS enthusiast who also loves skating on Rollerblades.

**CS side:** What areas are you diving into right now—algorithms, AI, systems, graphics, something else? If you ever want project ideas that blend coding with skating (e.g., a skate‑track visualizer, a sensor‑based trick analyzer, or a simple game), just let me know!

YOU:

YOU: Can You tell me the time right now and date
AI🤖: It’s currently **00:11:01** on **2026‑08‑28** (local time).


YOU: me in one statement
AI🤖: Fred is a computer‑science student who fuels his creativity and focus by roller‑blading whenever he can.

"""