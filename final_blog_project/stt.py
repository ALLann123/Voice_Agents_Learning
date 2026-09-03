#!/usr/bin/python3
import os
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Audio to Groq's whisper model for transcription
def listen():
    # create the speech recognizer object
    recognizer = sr.Recognizer()
    # open the default microphone
    with sr.Microphone() as source:
        #Notify the user recording has started.
        print("\n🎤Listening...")
        # Listen until the user stops speaking
        # recorded audio is stored in a variable 'audio'
        audio = recognizer.listen(source)

    try:
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
        # return the text in lowercase
        return text.lower()

    # Exception when nothing usable was returned (empty/failed transcription)
    except Exception as e:
        print(f"Transcription error: {e}")
        # Return empty string, not the error text itself - the caller
        return ""