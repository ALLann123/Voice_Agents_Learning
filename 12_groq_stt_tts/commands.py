#!/usr/bin/python3
import requests  # can be used later on with APIs

# function processes the user's spoken command
# returns an appropriate response
def process_command(command):
    # check if the user asked about the weather
    command=command.lower()
    if "weather" in command:
        return "Sir, It is sunny outside but cold!!"
    
    # check if the user asked for the assistant's name
    elif "your name" in command:
        return "I am Jarvis, an incomplete Python assistant. Anything else Sir?"
    
    # check if the user requested a joke
    elif "joke" in command:
        return "Why did the computer go to therapy? Because it had too many bytes"
    
    # check if the user mentioned wikipedia
    elif "wikipedia" in command:
        return "Wikipedia Search not implemented yet sir, but you can add it!"
    
    # About the created
    elif "allan" in command:
        return "Allan is my creater, He will improve me progressively."
    
    else:
        return "Sorry Sir, I didn't Understand that"

