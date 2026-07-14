#!/usr/bin/python3
import whisper
import warnings

warnings.filterwarnings(
    "ignore",
    message="FP16 is not supported on CPU; using FP32 instead"
)

import whisper
model=whisper.load_model("tiny")

result=model.transcribe("recording.wav")

print(result["text"])

"""
(11_Voice_Assistant) J:record_transcribe>python transcribe.py
 Hello, how are you? Can you come in?
"""