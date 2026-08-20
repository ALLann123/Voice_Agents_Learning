#!/usr/bin/python3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"
)

response=llm.invoke("Hello, define AI in one sentence")
print(f"AI: {response.content}")

"""
AI: Artificial intelligence is the field of computer science that creates systems capable of performing tasks that normally require human intelligence, such as learning, reasoning, perception, and decision‑making.
"""
