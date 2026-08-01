#!/usr/bin/python3
import speech_recognition as sr
import pyttsx3  #---> python library for offline text to speech


# set the MIC we will be using
MIC_INDEX=2

#----- Step 1: listening to your voice(speech-to-text)----
# function records audion from microphone
# converts to text using Google's speech recognition API
def listen():
    """Responsible for listening for audio"""
    # create a speech recognizer object
    recognizer=sr.Recognizer()

    # open the default microphone
    with sr.Microphone(device_index=MIC_INDEX) as source:
        # Notify user recording has started
        print("🎤Listening....")

        # Listen until the user stops speaking
        # store the audio here
        audio=recognizer.listen(source)

    try:
        print("Gotten audio....sending to google....")
        # send the recorded audion to Google's Speech recognition service
        # convert the spoken words into text
        text=recognizer.recognize_google(audio)

        # Display what the recognizer understood
        print(f"You Said: {text}")
        # here is where we call the grammar checker

        # return the text in lowercase
        return text.lower()

    # keyboard exit error handing
    except KeyboardInterrupt:
        return "ctrl+c detected, Exiting..."

     #Exceptions happen when speech was not detected or understood
    except sr.UnknownValueError:
        return ""

    #Exception is when Google's API cannot be reached
    except sr.RequestError:
        return "Error: Check Internet Connection"


#-----Step 2:Talking Back(Text-to-Speech)
def speak(text):
    print(f"JARVIS: {text}")

    # create a fresh engine instance every time
    # Reusing one global engine accross multiple runAndWait() calls
    # is unreliable on many platforms and causes audio to stop aftter
    # the first utterance
    engine=pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1)

    engine.say(text)
    engine.runAndWait()
    engine.stop()  # cleanup after speaking, not before


# ---Step 3: The Brain for processing user input
# this is a user defined function
from commands import process_command

# ----Step 4: Putting it All together-----
def main():
    speak("Hello Sir, I am Jarvis. How can I help you?")

    # trap it in an infinity loop
    while True:
        # get the input voice and convert to text using the listen function(Google Speech to text)
        command=listen()

        # check if command is empty we continue and restart execution
        if command=="":
            continue

        # if the command has exit or quit terminate program
        if command in ['exit', 'quit']:
            speak("Goodbye Sir!")
            break

        # hence we pass the command to the brain ofthe application LLM
        response=process_command(command)

        # output
        speak(response)

if __name__=="__main__":
    main()


"""
(11_Voice_Assistant) J:\11_Voice_Assistant\10_version_2_voice_llm>python main.py
JARVIS: Hello Sir, I am Jarvis. How can I help you?
🎤Listening....
Gotten audio....sending to google....
You Said: hello
JARVIS: Hello. How can I assist you?
🎤Listening....
Gotten audio....sending to google....
You Said: what's the weather today
JARVIS: No tools available
🎤Listening....
Gotten audio....sending to google....
You Said: lotto
JARVIS: No tools available
🎤Listening....
Gotten audio....sending to google....
You Said: okay what do you do what
JARVIS: I assist with information and tasks. No tools available.
🎤Listening....
Gotten audio....sending to google....
You Said: define python
JARVIS: Python: High-level, interpreted programming language used for web development, data analysis, and artificial intelligence.
🎤Listening....
Gotten audio....sending to google....
You Said: is it easy
JARVIS: Depends on the task. No tools available.
🎤Listening....
Gotten audio....sending to google....
You Said: please play the music
JARVIS: No tools available
🎤Listening....
Gotten audio....sending to google....
You Said: exit
JARVIS: Goodbye Sir!
"""