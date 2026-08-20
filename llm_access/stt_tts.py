"""
Voice echo test on Windows using Groq's Whisper (STT) and Orpheus (TTS).

Flow:
1. Press Enter to start recording from your microphone.
2. Press Enter again to stop.
3. Groq Whisper transcribes what you said.
4. Groq Orpheus speaks the transcription back to you.

Install:
    pip install groq sounddevice soundfile numpy

Set your API key first (PowerShell):
    setx GROQ_API_KEY "your-key-here"
(then open a new terminal so the env var is picked up)
"""

import os
import queue
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SAMPLE_RATE = 16000  # Whisper downsamples to 16kHz mono anyway
CHANNELS = 1
RECORD_PATH = "mic_input.wav"
SPEECH_PATH = "tts_output.wav"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def record_audio(path: str) -> None:
    """Record from the default microphone until Enter is pressed again."""
    q: "queue.Queue[np.ndarray]" = queue.Queue()
    stop_flag = threading.Event()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback
    )
    frames = []

    def collector():
        with stream:
            while not stop_flag.is_set():
                try:
                    frames.append(q.get(timeout=0.1))
                except queue.Empty:
                    continue

    t = threading.Thread(target=collector)
    t.start()
    input("Press Enter to STOP recording...")
    stop_flag.set()
    t.join()

    if not frames:
        raise RuntimeError("No audio captured.")

    audio = np.concatenate(frames, axis=0)
    sf.write(path, audio, SAMPLE_RATE)
    print(f"Saved recording to {path}")


def transcribe(path: str) -> str:
    with open(path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=(os.path.basename(path), f.read()),
            model="whisper-large-v3",
            response_format="text",
            language="en",
        )
    return result.strip()


def speak(text: str, path: str) -> None:
    # Orpheus input is limited to 200 characters; truncate for this simple test.
    if len(text) > 200:
        text = text[:200]
    response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice="troy",
        input=text,
        response_format="wav",
    )
    response.write_to_file(path)

    data, sr = sf.read(path)
    sd.play(data, sr)
    sd.wait()


def main():
    input("Press Enter to START recording...")
    record_audio(RECORD_PATH)

    print("Transcribing...")
    text = transcribe(RECORD_PATH)
    print(f"You said: {text}")

    if not text:
        print("Nothing was transcribed, skipping playback.")
        return

    print("Speaking it back...")
    speak(text, SPEECH_PATH)
    print("Done.")


if __name__ == "__main__":
    main()

"""
>python stt_tts.py
Press Enter to START recording...
Press Enter to STOP recording...
Saved recording to mic_input.wav
Transcribing...
You said: Hello, how are you?
Speaking it back...
Done.

>python stt_tts.py
Press Enter to START recording...
Press Enter to STOP recording...
Saved recording to mic_input.wav
Transcribing...
You said: Hello, how are you? Do you know the weather today? I am feeling cold today. What could you recommend for me?
Speaking it back...
Done.


For this edit the whisper setting 'language="de"'
----> By default when set to english it will translate it.
> >python stt_tts.py
Press Enter to START recording...
Press Enter to STOP recording...
Saved recording to mic_input.wav
Transcribing...
You said: Hallo, Koffie oder Tee. Ich bin Alan. Ich komme aus Berlin.
Speaking it back...
Done.

"""