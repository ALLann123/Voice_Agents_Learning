#!/usr/bin/python3
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage
import base64

# load environment variables
load_dotenv()

# build the model
llm=ChatGroq(
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="meta-llama/llama-4-scout-17b-16e-instruct"
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
try_vision_1>python groq_vision.py
[+] FInished Converting image to base64......
[+] Done with prompt...
[+] Passed to AI.....


AI: The image displays a 403 Forbidden error message.

* The main points of the image are:
        + A large number "403" in the center of the image
        + The word "Forbidden" below the number
        + A sentence explaining the error below the word "Forbidden"

The image is a simple white rectangle with black text and a thin black border. The large number "403" is prominently displayed in the center of the image, with the word "Forbidden" written below it in smaller text. Below that, there is a sentence that reads, "Access to this resource on the server is denied!"

The overall design of the image is minimalistic and straightforward, effectively conveying the error message to the user.
"""