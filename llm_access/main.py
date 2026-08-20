from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("GPT_5")

# Make sure OPENAI_API_KEY is set in your environment
llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=API_KEY
)

response = llm.invoke("hi")
print(response.content)

"""
>python main.py
Hi there! How can I help today? I can explain things, answer questions, help with writing or coding, brainstorm ideas, plan tasks, or just chat. Tell me what you’re working on or what you’d like to do.
"""