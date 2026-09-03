#!/usr/bin/python3
from piper import PiperVoice
import sounddevice as sd
import numpy as np 

MODEL_PATH="piper_voices/en_US-amy-medium.onnx"

# Load once at startup — reuse across calls, loading the model is the slow part
voice = PiperVoice.load(MODEL_PATH)

def speak(text: str):
    """Synthesize text to speech and play it immediately."""
    audio_chunks = []
    for chunk in voice.synthesize(text):
        audio_chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))

    audio = np.concatenate(audio_chunks)
    sd.play(audio, samplerate=voice.config.sample_rate)
    sd.wait()  # block until playback finishes