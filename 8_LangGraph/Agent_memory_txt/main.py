#!/usr/bin/python3
from typing import TypedDict, List, Union
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

# load our enviroment variables
load_dotenv()

# load our LLM--> GPT 4
api_key=os.getenv("GITHUB_TOKEN")

#create llm
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)

# create the graph schema
class AgentState(TypedDict):
    # Restricts the messages variabble to contain only two interactions. Human and AI messages
    messages:List[Union[HumanMessage, AIMessage]]

# Create node---> A function that performs one task
def process(state: AgentState)-> AgentState:
    """This node will resolve the request from our input"""
    # we pass our message History to the LLM
    response=llm.invoke(state['messages'])

    # now append the new message to the graph state
    state['messages'].append(AIMessage(content=response.content))

    # display the AI output to the user
    print(f"\nAI: {response.content}")

    return state

# create the graph
graph=StateGraph(AgentState)

# add node
graph.add_node('process', process)

# add edge--> control the flow of the next node execution
graph.set_entry_point('process')
graph.set_finish_point('process')

#compile our graph to an executable
app=graph.compile()


print("***************************************")
print("     LOCAL MEMORY AGENT     ")
print("***************************************")

#-------- hold our chat history----------
# will hold only two types of messages
conversation_history:List[Union[HumanMessage, AIMessage]]=[]

# Load previors conversation if logging.txt exists
if os.path.exists('logging.txt'):
    # open and read the file
    with open('logging.txt', 'r', encoding='utf-8') as file:
        # copy each line to the variable lines
        lines=file.readlines()

    for line in lines:
        # remove any trailing spaces
        line=line.strip()
        # get user lines starting with "You", append to our variable created and replace with the word HumanMessage
        # instead of You
        if line.startswith('You: '):
            conversation_history.append(HumanMessage(content=line.replace('You: ', "")))

        # Get the AI messages and save with AIMessage to our new variable
        elif line.startswith('AI: '):
            conversation_history.append(AIMessage(content=line.replace('AI: ', "")))

    if conversation_history:
        print('[+]Loaded previous history from logging.txt....')

#----Start an interactive shell
while True:
    # get keyboard input
    user_input=input("\nALLAN: ")

    if user_input in ['exit', 'quit']:
        print('Goodbye!!')
        break

    # prevent blank input from calling the LLM:
    if not user_input.strip():
       #restarts the loop
       continue

    # add the human message to our in memory conversation history
    conversation_history.append(HumanMessage(content=user_input))

    # invoke the agent with our query
    result=app.invoke({'messages': conversation_history})

    # the node process will append our AI response to the state messages with AIMessage
    # update the whole variable with new list of messages. The current new state
    conversation_history=result['messages']


# This is executed after the user closes the session above
#-------Check the log.txt file for conversation history/creates it if non-existence
with open('logging.txt', 'w', encoding='utf-8')as file:
    file.write("Your conversation Log:\n")

    # iterate through our in memory variable with the current state
    for message in conversation_history:
        # identify user messages
        if isinstance(message, HumanMessage):
            # write to our file in disk
            file.write(f"You: {message.content}\n")

        # get the AI Message
        if isinstance(message, AIMessage):
            # write to our file in disk
            file.write(f"AI: {message.content}\n")

print("[+] Conversation saved to logging.txt")


"""
***************************************
     LOCAL MEMORY AGENT
***************************************

ALLAN: Hey, I am Allan. An aspiring computer science student. I love computers, playing soccer and rollball.

AI: Hi Allan! It's great to meet you. Being an aspiring computer science student sounds exciting—there’s so much to learn and discover in the tech world. It's awesome that you not only enjoy working with computers but also balance your time with physical activities like soccer and rollball. That’s a cool combination of interests! Do you have a specific area in computer science you're passionate about, like coding, AI, cybersecurity, or game development? Or are you still exploring your options? Let me know if you ever want to brainstorm or discuss anything related to your passions—I'd be happy to help!

ALLAN:

=====After we closed Appplication and restarted to check persistence=====
***************************************
     LOCAL MEMORY AGENT
***************************************
[+]Loaded previous history from logging.txt....

ALLAN: can you tell me about myself in a single sentence?

AI: Allan, you're an aspiring computer science student who loves exploring the world of computers while balancing your passion for soccer and rollball, showcasing a blend of intellect and athleticism.

ALLAN: what type of malware did we talk about in one word

AI: **Clipper.**

ALLAN: Clipper what?

AI: **Crypto clipper malware.**

ALLAN: quit
Goodbye!!
[+] Conversation saved to logging.txt
"""