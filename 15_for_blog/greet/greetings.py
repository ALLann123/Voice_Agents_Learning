#!/usr/bin/python3
from typing import TypedDict  # we will use this to 
from langgraph.graph import StateGraph, START, END


# ---Step 1: Define the state Schema
#- State holds shared data passed between nodes
#- Each node updates the field in our case now it is message
class AgentState(TypedDict):
    # holds our message---> read on pydantic to understand the state better
    message: str

# ----Step 2: Create a node
# - Node a python function that performs one task
# - The node receives the current state we defined above, does some work, and returns the updated state
def greet(state: AgentState)-> AgentState:
    """This simple node adds a greeting message"""
    state['message']='Hey ' + state['message'] +' , how are you doing?'

    # updated state returned
    return state

# create graph schema
graph=StateGraph(AgentState)

# add the node to our graph
graph.add_node("greeter", greet)

# Set starting point
# Remember: To connect the nodes together we use edges
graph.add_edge(START, "greeter") # the START is where execution of the graph begins

# Set the endpoint
graph.add_edge("greeter", END)

# compile our graph to an executable
app=graph.compile()

# test our graph using the invoke keyword
result=app.invoke({"message":"Allan"})

# view the currenn updated graph state
print(f"Current Graph State:\n{result['message']}")


"""
===========Ignore this part: Is my result on CMD=======
cmd>> python greetings.py
Current Graph State:
Hey Allan , how are you doing?

"""