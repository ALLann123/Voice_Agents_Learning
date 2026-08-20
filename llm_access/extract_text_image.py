#!/usr/bin/python3
#from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os
import base64

# Environment variables
load_dotenv()

"""
#set llm
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="qwen/qwen3.6-27b"
)
"""

llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=os.getenv("GPT_5")
)

#----1. Convert our image to base64
# - Send the image to the API in this format
def encode_image(image):
    #open image in binary and encode it
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

# call the function to send our encoded image data to llm
def describe_image(image):
    # get encoded image data
    encoded_image=encode_image(image)

    # Prepare prompt
    message=HumanMessage(
        content=[
            {
                "type":"text",
                "text":"Describe the image"
            },
            {
                "type":"image_url",
                # fetching image locally.
                "image_url":{
                    "url":f"data:image/png;base64,{encoded_image}"
                }
            }
        ]
    )

    # call our LLM passing the above prompt with our encoded image data
    result=llm.invoke([message])

    return result.content

# put to the test
response=describe_image("Layers_of_OSI_Model.png")
print(f"AI: {response}")

"""
---> GPT 5:
python extract_text_image.py
AI: The image is a diagram of the OSI model. On the left is a vertical stack of seven rounded green pills labeled (from top to bottom): Application, Presentation, Session, Transport, Network, Data Link, Physical. To the right, a large curly brace groups these as “Software Layers,” with reference text (e.g., “Heart Of OSI”) and a note about hardware layers. A watermark from InterviewBit is in the bottom-right.

"""