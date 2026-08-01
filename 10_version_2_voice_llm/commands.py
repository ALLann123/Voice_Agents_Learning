#!/usr/bin/python3
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

# load our environment variables
load_dotenv()

# the llm setup
api_key=os.getenv("GITHUB_BRO")

# setup
#build our model
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def process_command(command):
    """We invoke the LLM with user message with system message for additional context"""
    messages=[
        SystemMessage(content="You are Jarvis, A helpful AI assistant. When asked questions that need you to carry an action answer with 'No tools available'. Summarize your answers to be brief"),
        HumanMessage(content=command)
    ]

    # call the llm
    result=llm.invoke(messages)

    # get the feed back only
    feedback=result.content

    return feedback


