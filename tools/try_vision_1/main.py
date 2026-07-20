#!/usr/bin/python3
import base64
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
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

#-------Step 1: Convert the image to base64 function
def encode_image(image):
    # open the image binary and encode it
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()


#-----Step 2: Call the function to send encoded image data to LLM
def describe_image(image):
    # get encoded image data
    encoded_image=encode_image(image)

    print("[+] FInished Converting image to base64......")

    # Prepate prompt
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

    print("[+] Done with prompt...")

    # call our LLM passing the above prompt with our encoded image data
    result=llm.invoke([message])

    print("[+] Passed to AI.....\n\n")

    return result.content


# call the function
image="error.png"

# call our function
image_info=describe_image(image)
print(f"AI: {image_info}")

"""
>python main.py
[+] FInished Converting image to base64......
[+] Done with prompt...
[+] Passed to AI.....


AI: This image displays an error message:

- The text reads "**403**" in large, bold font at the center, usually indicating the HTTP 403 Forbidden error.
- Below it, the word "**Forbidden**" appears in smaller font, signaling restricted access.
- Underneath, the message "**Access to this resource on the server is denied!**" is displayed.
- The background is plain white with black text, offering a minimal and straightforward design common for HTTP error pages.

"""