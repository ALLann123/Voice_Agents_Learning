#!/usr/bin/python3
import speech_recognition as sr
import pyttsx3      # python library for offline text-to-speech

# -----Step 1: listening to your voice(Speech-to-Text)-----
#Function records audio from the microphone
# converts it into text using Google's speech recognition API
def listen():
    # create a speach recognizer object
    recognizer= sr.Recognizer()

    # open the default microphone
    with sr.Microphone() as source:
        # Notify the user that recording has started
        print("🎤Listening....")

        # Listen until the user stops speaking
        # recorded audio is stored in a variable 'audio'
        audio=recognizer.listen(source)

    try:
        # send the recorded audio to Google's Speech recognition service
        # and convert he spoken words into text
        text = recognizer.recognize_google(audio)

        # Display what the recognizer understood
        print("You said:", text)

        # return the text in lowercase
        # Makes easier to compare commands later
        return text.lower()
    
    # Exceptions happen when speech was no detected or understood
    except sr.UnknownValueError:
        return ""
    
    # Exception is when Google's speech API cannot be reached
    except sr.RequestError:
        return "Error: Check Internet Connection"
    

#----Step 2: Talking Back(Text-to-Speech)
def speak(text):
    print("Jarvis: ", text)

    # Create a fresh engine instance every time.
    # Reusing one global engine across multiple runAndWait() calls
    # is unreliable on many platforms and causes audio to stop after
    # the first utterance.
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1)

    engine.say(text)
    engine.runAndWait()
    engine.stop()   # cleanup after speaking, not before


# ----Step 3: Visit 'commands.py'------
# this is a user defined function
from commands import process_command

# -----Step 4: Putting It All Together--------
def main():
    speak("Hello Sir, I am Jarvis. How can I help you today?")

    # Trap it in an infinity loop
    while True:
        # get the input voice and convert to text using the listen function(Uses Google)
        command=listen()

        # check in command is empty we continue
        if command=="":
            # just restarts execution of the function
            continue
        
        # if the command has exit or quit terminate the program
        if "exit" in command or "quit" in command:
            speak("Goodbye Sir!")
            break

        # process the commands with "commands.py" file using the nested if----else statements
        response=process_command(command)

        # Output the result of the execution:
        speak(response)

if __name__ == "__main__":
    main()

"""
(11_Voice_Assistant) J:\11_Voice_Assistant\1_simple_voice_text>python assistant.py
Jarvis:  Hello Sir, I am Jarvis. How can I help you today?
🎤Listening....
You said: what's the weather today
Jarvis:  Sir, It is sunny outside but cold!!
🎤Listening....
You said: okay I need
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
You said: tell me a joke
Jarvis:  Why did the computer go to therapy? Because it had too many bytes
🎤Listening....
You said: that was a good one Alan
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
You said: tell me about Wikipedia
Jarvis:  Wikipedia Search not implemented yet sir, but you can add it!
🎤Listening....
You said: your name please
Jarvis:  I am Jarvis, an incomplete Python assistant. Anything else Sir?
🎤Listening....
You said: nothing exit
Jarvis:  Goodbye Sir!

"""