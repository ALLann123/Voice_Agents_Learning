#!/usr/bin/python3
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# ---------Step 0: Initialize our GPT Model
# load environment variables
load_dotenv()

# get the Github Market place API Key
api_key=os.getenv("GITHUB_TOKEN")

# create LLM
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
)


result=llm.invoke("Hello?")

print(f'AI: {result.content}')
