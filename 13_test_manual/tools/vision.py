#!/usr/bin/python3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import base64
from langchain_core.messages import HumanMessage

# load environment variables--> API keys from the 
load_dotenv()

# the llm setup---> take note of the model_name that has vision
api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="qwen/qwen3.6-27b"
)

# first step is to convert the image to base64
# We will send it to the API in this format
def encode_image(image):
    # open the image in binary and encode it
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
# Call the function to send encoded image data to LLM
def describe_image(image):
    # get encoded image data
    encoded_image=encode_image(image)

    # Prepare prompt
    message= HumanMessage(
        content=[
            {
                "type":"text",
                "text":"Describe this Image. Be brief"
            },
            {
                "type":"image_url",
                # fetching image locally. If not local use: 'url':'https:<url_for_iamge>'
                "image_url":{
                    "url":f"data:image/png;base64,{encoded_image}"
                }
            }
        ]
    )

    # call our LLM passing the above prompt with our encoded image data
    result=llm.invoke([message])

    # get the content part. Thats what we care about to be returned
    result=result.content

    # Remove reasoning section--> we want to reduce the amount of text returned--> reducing token 
    if "</think>" in result:
        result = result.split("</think>", 1)[1].strip()

    return result

