#!/usr/bin/python3

def process_command(command):
    # chekc if the user asked about the weather
    command=command.lower()
    if "weather" in command:
        return "Sir, It is sunny!!"
    
    #check if the user asked todays date
    elif "date" in command:
        return "Today is fourteenth June, Sir"
    
    # check if asked about us
    elif "name" in command:
        return "I am Jarvis, the next local version of the assistant. Anything else Sir?"
    
    # check if joke is requested
    elif "joke" in command:
        return "I went to the American capital, I saw a Bee and it noded at me. That is a USB"
    
    # Check if wikipedia is mentioned
    elif "wikipedia" in command:
        return "Wikipedia Search not implemented yet sir, please code me!"
    
    # About the creater
    elif "maker" in command:
        return "Allan build me, stop being lazy sir and improve me!!"
    
    # Brain check
    elif "brain" in command:
        return "Sir, I lack a large language Model to control my decision making."
    
    else:
        return "Sorry Sir, I didn't Understand that!"

"""
pytts_whisper>python assistant.py
100%|████████████████████████████████████████| 139M/139M [03:45<00:00, 645kiB/s]
Jarvis:  Hello Sir, I am JARVIS. Your Personal Assistant, how can I help you Today?
🎤Listening........
Language Identified: en
You said:  Wikipedia
Jarvis:  Wikipedia Search not implemented yet sir, please code me!
🎤Listening........
Language Identified: en
You said:  your brain
Jarvis:  Sir, I lack a large language Model to control my decision making.
🎤Listening........
Language Identified: en
You said:  dead early
Jarvis:  Sorry Sir, I didn't Understand that!
🎤Listening........
Language Identified: en
You said:  Better
Jarvis:  Sorry Sir, I didn't Understand that!
🎤Listening........
Language Identified: en
You said:  Exit
Jarvis:  Goodbye Sir!
"""