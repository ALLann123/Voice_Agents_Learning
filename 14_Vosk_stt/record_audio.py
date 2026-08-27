#!/usr/bin/python3
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

DURATION = 15          # seconds
SAMPLE_RATE = 16000    # Vosk small models expect 16kHz
CHANNELS = 1            # mono
#OUTPUT_FILE = "test.wav"
OUTPUT_FILE = "to_clone.wav"

print(f"[+] Recording {DURATION} seconds... speak now!")

# records as int16 directly -> already correct PCM format for Vosk
recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16"
)
sd.wait()  # block until recording is finished

write(OUTPUT_FILE, SAMPLE_RATE, recording)
print(f"[+] Saved to {OUTPUT_FILE}")

"""
> python record_audio.py
[+] Recording 5 seconds... speak now!
[+] Saved to test.wav

"""