#!/usr/bin/python3
import speech_recognition as sr  # Gets the audio from the speaker.
import pyttsx3  # python library for offline text-to-speech.
import whisper # local speech-to-text converter
import warnings
import io    # lets us treat bytes like a file
import soundfile as sf # Reads WAV audio into samples
import numpy as np

# suppress whisper warning
warnings.filterwarnings(
    "ignore",
    message="FP16 is not supported on CPU; using FP32 instead"
)

# Load the whisper model ones
model = whisper.load_model("base")

def convert_audio_text(audio):
    # Resample to 16kHz, 16-bit — this is what Whisper expects.
    audio_bytes = audio.get_wav_data(convert_rate=16000, convert_width=2)

    audio_file = io.BytesIO(audio_bytes)
    audio_array, samplerate = sf.read(audio_file, dtype="float32")

    # Skip language auto-detection if you always speak English —
    # it's unreliable on short/noisy clips and was likely contributing
    # to your "nn" result and the garbled final transcript.
    result = model.transcribe(audio_array, language="en", fp16=False)

    print(f"Language Identified: {result['language']}")
    return result['text']

# ------Step 1: Listening to your voice(recording) & Convert to text using whisper--------
# Function records audio from microphone
def listen():
    # create a speech recognizer object
    recognizer=sr.Recognizer()

    # Open the default microphone
    with sr.Microphone() as source:
        # Notify the user that recording has started
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤Listening........")

        # Listen until the user stops speaking
        # recorded audio is stoed in a variable 'audio'
        audio=recognizer.listen(source)

    try:
        # send the recorded audio to whisper 
        # convert the spoken words into text
        # Call the convert speech to text function
        text=convert_audio_text(audio)
        print(f"You said: {text}")

        # return the text in lowercase
        # make easier to compare commands in lower case later
        return text.lower()
    
    except sr.UnknownValueError:
        return ""
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return ""


# -----Step 2: Talking Back(Text-To-Speech)
# we are using the python built in pyttsx3
def speak(text):
    print(f"Jarvis: ", text)

    # Create a fresh engine instance every time
    # Reusing one global engine accross multiple runAndWait() calls
    # is unreliable on many platforms and causes audio to stop after
    # the first utterance
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1)

    engine.say(text)
    engine.runAndWait()
    engine.stop() # clean up after speaking not before


# ----Step 3: Visit 'commands.py'
# import it here
from commands import process_command

# ----Step 4: Putting All Together---------
def main():
    speak("Hello Sir, I am JARVIS. Your Personal Assistant, how can I help you Today?")

    # Trap it in an infinity loop
    while True:
        # get the input voice and convert to text using the listen function(local whisper)
        command=listen()

        # check if commpand is empty we continue(prevents program from breaking/processing empty things)
        if command=="":
            # just restarts  execution no need to continue processing an empty string
            continue
        
        # if the command has exit or quit terminate the program
        if "exit" in command or "quit" in command:
            speak("Goodbye Sir!")
            break
        
        # process the commands with commands.py file
        response=process_command(command)

        # Ouput the result
        speak(response)

if __name__=="__main__":
    main()



