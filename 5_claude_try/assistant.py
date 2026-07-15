#!/usr/bin/python3
import speech_recognition as sr
import numpy as np
import sounddevice as sd
from piper import PiperVoice, SynthesisConfig   # offline neural text-to-speech

# -----Step 0: Load the Piper voice once at startup-----
# Loading the ONNX model is relatively expensive, so we do it once
# and reuse the same voice object for every speak() call.
VOICE = PiperVoice.load("en_US-lessac-medium.onnx")

# Controls speaking rate/volume/etc.
# length_scale: lower = faster, higher = slower (1.0 is the model's default pace)
SYN_CONFIG = SynthesisConfig(length_scale=0.9)

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

    # synthesize() streams AudioChunk objects; each chunk's raw
    # 16-bit PCM audio lives in chunk.audio_int16_bytes
    audio_chunks = []
    for chunk in VOICE.synthesize(text, syn_config=SYN_CONFIG):
        audio_chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))

    if not audio_chunks:
        return

    audio = np.concatenate(audio_chunks)
    sd.play(audio, samplerate=VOICE.config.sample_rate)
    sd.wait()   # block until playback finishes, same as runAndWait()


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