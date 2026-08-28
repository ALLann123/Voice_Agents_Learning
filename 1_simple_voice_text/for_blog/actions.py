#!/usr/bin/python3

# Function processes the user's spoken command as transcribed by Google text to speech
# returns appropriate response
def process_action(command):
    # Checked if the user asked about the weather
    command=command.lower()   # convert the user input to lower case

    if "weather" in command:
        return "Sir, no storm today. Wear a Tshirt!"

    # check if the user requested a joke
    elif "joke" in command:
        return "Why did the Computer go to therapy? Because it had too many bytes"

    # check if the user mentions wikipedia
    elif "wikipedia" in command:
        return "Sir we have not implemented that, sorry!"

    else:
        return "Sorry Sir, I didn't understand that"

# We are not using an LLM yet
