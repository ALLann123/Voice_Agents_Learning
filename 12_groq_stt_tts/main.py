#!/usr/bin/python3
import os
import io

import speech_recognition as sr   # still used for microphone capture + silence detection
import soundfile as sf
import sounddevice as sd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # loads GROQ_API_KEY from a .env file

# Groq client, shared by both the STT and TTS calls below
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# -----Step 1: listening to your voice (Speech-to-Text via Groq Whisper)-----
# Function records audio from the microphone using speech_recognition
# (which handles "listen until silence" for us), then sends the raw
# audio to Groq's Whisper model for transcription instead of Google.
def listen():
    # create a speech recognizer object (only used for capturing mic audio here)
    recognizer = sr.Recognizer()

    # open the default microphone
    with sr.Microphone() as source:
        # Notify the user that recording has started
        print("🎤Listening....")

        # Listen until the user stops speaking
        # recorded audio is stored in a variable 'audio'
        audio = recognizer.listen(source)

    try:
        print("Gotten audio....sending to Groq...")

        # speech_recognition gives us the captured audio as WAV bytes,
        # which we can send straight to Groq's transcription endpoint
        wav_bytes = audio.get_wav_data()

        # send the recorded audio to Groq's Whisper model
        # and convert the spoken words into text
        result = client.audio.transcriptions.create(
            file=("mic_input.wav", wav_bytes),
            model="whisper-large-v3",
            response_format="text",
            language="en",
        )

        text = result.strip()

        # Display what the recognizer understood
        print("You said:", text)

        # return the text in lowercase
        # Makes easier to compare commands later
        return text.lower()

    # Exception when nothing usable was returned (empty/failed transcription)
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""


# ----Step 2: Talking Back (Text-to-Speech via Groq Orpheus)
def speak(text):
    print("Jarvis: ", text)

    # Orpheus input is limited to 200 characters per request, so long
    # responses are chunked and spoken in sequence.
    chunks = [text[i:i + 200] for i in range(0, len(text), 200)] or [""]

    for chunk in chunks:
        if not chunk.strip():
            continue

        # request speech audio from Groq's Orpheus TTS model
        response = client.audio.speech.create(
            model="canopylabs/orpheus-v1-english",
            voice="troy",          # swap for autumn, diana, hannah, austin, daniel if preferred
            input=chunk,
            response_format="wav",
        )

        # read the returned WAV bytes directly from memory (no temp file needed)
        audio_bytes = response.read()
        data, samplerate = sf.read(io.BytesIO(audio_bytes))

        # play the audio out loud through the default speaker
        sd.play(data, samplerate)
        sd.wait()  # block until this chunk finishes playing before speaking the next


# ----Step 3: Visit 'commands.py'------
# this is a user defined function
from commands import process_command

# -----Step 4: Putting It All Together--------
def main():
    speak("Hello Sir, I am Jarvis. How can I help you today?")

    # Trap it in an infinity loop
    while True:
        # get the input voice and convert to text using the listen function (now via Groq)
        command = listen()

        # check in command is empty we continue
        if command == "":
            # just restarts execution of the function
            continue

        # if the command has exit or quit terminate the program
        if "exit" in command or "quit" in command:
            speak("Goodbye Sir!")
            break

        # process the commands with "commands.py" file using the nested if----else statements
        response = process_command(command)

        # Output the result of the execution:
        speak(response)


if __name__ == "__main__":
    main()


"""
>python main.py
Jarvis:  Hello Sir, I am Jarvis. How can I help you today?
🎤Listening....
Gotten audio....sending to Groq...
You said: What is the weather today?
Jarvis:  Sir, It is sunny outside but cold!!
🎤Listening....
Gotten audio....sending to Groq...
You said: Do you have Wikipedia?
Jarvis:  Wikipedia Search not implemented yet sir, but you can add it!
🎤Listening....
Gotten audio....sending to Groq...
You said: Okay, thank you.
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
Gotten audio....sending to Groq...
You said: What can you do?
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
Gotten audio....sending to Groq...
You said: Can you tell me your name?
Jarvis:  I am Jarvis, an incomplete Python assistant. Anything else Sir?
🎤Listening....
Gotten audio....sending to Groq...
You said: Do you know Alam?
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
Gotten audio....sending to Groq...
You said: Do you know Alan?
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
Gotten audio....sending to Groq...
You said: Thank you.
Jarvis:  Sorry Sir, I didn't Understand that
🎤Listening....
Gotten audio....sending to Groq...
You said: Okay, can you tell me a joke?
Jarvis:  Why did the computer go to therapy? Because it had too many bytes
🎤Listening....
Gotten audio....sending to Groq...
You said: Exit
Jarvis:  Goodbye Sir!
"""