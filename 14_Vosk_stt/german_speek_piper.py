#!/usr/bin/python3
from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np

MODEL_PATH = "piper_voices/de_DE-thorsten-medium.onnx"

voice = PiperVoice.load(MODEL_PATH)

# length_scale > 1.0 = slower, < 1.0 = faster
syn_config = SynthesisConfig(length_scale=1.3)

def speak(text: str):
    """Synthesize text to speech and play it immediately."""
    audio_chunks = []
    for chunk in voice.synthesize(text, syn_config=syn_config):
        audio_chunks.append(np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16))

    audio = np.concatenate(audio_chunks)
    sd.play(audio, samplerate=voice.config.sample_rate)
    sd.wait()

if __name__ == "__main__":
    speak("Hallo, ich bin David. Wo ist das Café?")
    speak("Ohhh, da drüben meine Frau!")
    speak("Kaffee mit milch und kekse bitte. Neine Zucker. Tschüss!")