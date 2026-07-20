#!/usr/bin/python3
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import base64
from langchain_core.messages import HumanMessage

# load environment variables
load_dotenv()

# the llm setup---> take note of the model_name that has vision
api_key=os.getenv("GITHUB_TOKEN")

#create llm
llm=ChatOpenAI(
    model="gpt-4o",
    openai_api_key=api_key,
    base_url="https://models.inference.ai.azure.com"
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
                "text":"Describe this Image"
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

    return result.content

image="my_quiz.png"
result=describe_image(image)

print(f"AI: {result}")