#!/usr/bin/python3
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

# load our environment variables
load_dotenv()


#build our model
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


# call the llm
result=llm.invoke("Hey")
print(f"AI: {result.content}")

