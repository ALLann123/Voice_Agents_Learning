#!/usr/bin/python3
from typing import TypedDict
from langgraph.graph import StateGraph

# State Schema: Shared amoung all nodes
class AgentState(TypedDict):
    length: int
    width: int
    area: int
    perimeter: int
    operation: str     # we will use it in our router function

# Node--> Function that performs an action
def get_area(state: AgentState)-> AgentState:
    """Calculate the area"""
    state['area']=state['length'] * state ['width']

    return state

# Another Node for calculating perimeter
def get_perimeter(state: AgentState)-> AgentState:
    """Calculate the Perimeter"""
    state['perimeter']=2*(state['length'] + state['width'])

    return state

# Router---> Decides what function to run. Either get_area() or get_perimeter(). 
def decide_next_node(state: AgentState)-> AgentState:
    """Decide the next node to run"""
    # u will see this when we invoke the graph changing the operation value in state. 
    if state['operation']=='a':
        return "area_operation"
    elif state['operation']=='p':
        return "perimeter_operation"

# Graph Schema
graph=StateGraph(AgentState)

# add our two nodes
graph.add_node('area', get_area)
graph.add_node('perimeter', get_perimeter)
graph.add_node('router', lambda state:state) # pass through function. Initial state passes through here

# Below is a quicker way to set the start of the graph without using START being imported
graph.set_entry_point('router')

# Now add conditional edge--> Selects the node to run using our router(decide_next_node)
graph.add_conditional_edges(
    'router', #the node we added
    decide_next_node, # the function to run inorder to decide what to execute next
    {
        # the function decide_next_node returns strings that we match with the names given to our nodes
        "area_operation":"area",
        "perimeter_operation":"perimeter"
    }
)

# Connect both our nodes to the END
# Only one node will be run by our conditional edge. Either we get perimeter or area
# this is another way to connect nodes to the END without importing END
graph.set_finish_point("area")
graph.set_finish_point("perimeter")

# Compile--> make our graph executable
app=graph.compile()

print("---------------We will demonstrate Area fisrt--------")
result=app.invoke({'length':15, 'width':6, 'operation':'a'})

print(f"The Area is: {result['area']}")
print('\n---------------------------------------------------')
"""
=======Dont Add this part: this is my cmd result==============
area_perimeter>python area_perimeter_rect.py
---------------We will demonstrate Area fisrt--------
The Area is: 90

---------------------------------------------------
"""

print("---------------We will demonstrate Perimeter--------")
result=app.invoke({'length':20, 'width':10, 'operation':'p'})

print(f"The Perimeter is: {result['perimeter']}")
print('\n---------------------------------------------------')

"""
======Dont Add this part: this is my cmd result========
area_perimeter>python area_perimeter_rect.py
---------------We will demonstrate Area fisrt--------
The Area is: 90

---------------------------------------------------
---------------We will demonstrate Perimeter--------
The Perimeter is: 60

---------------------------------------------------

"""