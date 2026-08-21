#!/usr/bin/python3
import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# get our environment variables
load_dotenv()

# llm 
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"
)
# lets create a tool
def get_weather(city: str)-> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"

#create our agent
agent=create_deep_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

# Run the agent
result=agent.invoke(
    {
        "messages":[
            {
                "role":"user",
                "content":"what is the weather in sf"
            },
        ]
    }
)

# get the last message
print(f"AI: {result['messages'][-1].content}")

"""
>python testing_deep_agents.py
AI: The current weather in San Francisco is: **“It’s always sunny in San Francisco.”**

"""