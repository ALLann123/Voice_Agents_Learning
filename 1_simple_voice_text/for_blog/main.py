#!/usr/bin/python3
import speech_recognition as sr  
import pyttsx3
# our user defined library actions.py
from actions import process_action

# -----Step 1: Listening your Voice(Speech-to-text)-----
# > Function records audio from the microphone
# > Converts it into text using Google's speech recognition API
def listen():
    # create a speech recognizer object
    recognizer=sr.Recognizer()

    # open the default microphone--> get our voice input
    with sr.Microphone() as source:
        # Print on terminal recording has started
        print("\n\n🎤Listening.....")

        # listen until the user stops speaking
        # recorded audio is stored in a variable 'audio'
        audio=recognizer.listen(source)

    # -Since interacting with an API better to use exception handling. Prevents program from crashing
    try:
        # send the recorded audio to Google's Speech Recognition services
        # transcribe our input into text
        text=recognizer.recognize_google(audio)

        # Display what has been transcribed
        print(f"You Said: {text}")

        # return text in lower case. Easier to compare it later
        return text.lower() #--> now we want to pass it to actions.py

    except sr.UnknownValueError:
        # if empty whatever was transcribed
        return ""

    except sr.RequestError:
        # incase no internet or googles speech API is unreachable
        return "\nError: Check Internet Connection"


# ------Step 2: Talking Back using pyttsx(Text-to-Speech)
def speak(text):
    # display what is to be spoken
    print(f"JARVIS🤖: {text}")

    # To avoid error we create a freshh engine instance every time
    engine=pyttsx3.init()
    # speed of the audio
    engine.setProperty('rate', 170)
    # the volume
    engine.setProperty('volume', 1)

    # execute our text to be spoken now
    engine.say(text)
    engine.runAndWait()
    engine.stop()    # clean up after speaking since we are creating a new instance each time


#------Step 3: Execute Everything---------
def main():
    speak("Hello Sir, I am JARVIS. How can I help you today? ")

    # Create an infinity loop for user interaction
    while True:
        # get the input voice and convert to text using the listen function(Has our microphone, Google text-to-speech model)
        command=listen()

        # Check if command is empty we continue--> restarts execution of the infinity loop and skips the other code
        if command=="":
            continue

        # if the command has exit or quit terminate the program
        elif "exit" in command or "quit" in command:
            speak("Goodbye Sir!")
            break

        # Now pass our command transcribed to our action.py. Process_action command will execute and return results
        response=process_action(command)

        #Output the results from our user defined function
        speak(response)

# call main function
if __name__=="__main__":
    main()

"""
=====================Do Not Add this Part: My results on CMD=======
for_blog>python main.py
JARVIS🤖: Hello Sir, I am JARVIS. How can I help you today?

🎤Listening.....
You Said: what is the weather today
JARVIS🤖: Sir, no storm today. Wear a Tshirt!


🎤Listening.....
You Said: do you do you have Wikipedia
JARVIS🤖: Sir we have not implemented that, sorry!

🎤Listening.....
You Said: tell me a joke
JARVIS🤖: Why did the Computer go to therapy? Because it had too many bytes


🎤Listening.....
You Said: exit
JARVIS🤖: Goodbye Sir!

"""