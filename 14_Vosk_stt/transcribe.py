#!/usr/bin/python3
import json
import wave
import sys
from vosk import Model, KaldiRecognizer

# define paths
#MODEL_PATH="vosk-model-small-en-us-0.15"
MODEL_PATH="vosk-model-small-de-0.15"
AUDIO_FILE="test.wav"

# 2. Load the model
try:
    model = Model(MODEL_PATH)
except Exception:
    print(
        f"Please download the model from ://alphacephei.com and unpack as '{MODEL_PATH}' in the current folder."
    )
    sys.exit(1)

# open audio file
wf=wave.open(AUDIO_FILE)

# Verify audio file compatibility
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

# Initialize recognizer 
recognizer=KaldiRecognizer(model, wf.getframerate())

print("[+]Transcribing audio file....please wait!")

# 5. Read and process the audio data in chunks
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break

    # AcceptWaveform streams data chunk by chunk (simulating real-time)
    if recognizer.AcceptWaveform(data):
        # Printed when a full sentence/phrase is finalized
        result = json.loads(recognizer.Result())
        print(result["text"])

# 6. Print the final remaining text block
final_result = json.loads(recognizer.FinalResult())
print(final_result["text"])

"""
Vosk_stt>python transcribe.py
LOG (VoskAPI:ReadDataFiles():model.cc:213) Decoding params beam=10 max-active=3000 lattice-beam=2
LOG (VoskAPI:ReadDataFiles():model.cc:216) Silence phones 1:2:3:4:5:6:7:8:9:10
LOG (VoskAPI:RemoveOrphanNodes():nnet-nnet.cc:948) Removed 0 orphan nodes.
LOG (VoskAPI:RemoveOrphanComponents():nnet-nnet.cc:847) Removing 0 orphan components.
LOG (VoskAPI:ReadDataFiles():model.cc:248) Loading i-vector extractor from vosk-model-small-en-us-0.15/ivector/final.ie
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:183) Computing derived variables for iVector extractor
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:204) Done.
LOG (VoskAPI:ReadDataFiles():model.cc:282) Loading HCL and G from vosk-model-small-en-us-0.15/graph/HCLr.fst vosk-model-small-en-us-0.15/graph/Gr.fst
LOG (VoskAPI:ReadDataFiles():model.cc:308) Loading winfo vosk-model-small-en-us-0.15/graph/phones/word_boundary.int
[+]Transcribing audio file....please wait!
what is the time today

=============When I changed to German====================
Vosk_stt>python transcribe.py
LOG (VoskAPI:ReadDataFiles():model.cc:213) Decoding params beam=10 max-active=3000 lattice-beam=2
LOG (VoskAPI:ReadDataFiles():model.cc:216) Silence phones 1:2:3:4:5:6:7:8:9:10
LOG (VoskAPI:RemoveOrphanNodes():nnet-nnet.cc:948) Removed 0 orphan nodes.
LOG (VoskAPI:RemoveOrphanComponents():nnet-nnet.cc:847) Removing 0 orphan components.
LOG (VoskAPI:ReadDataFiles():model.cc:248) Loading i-vector extractor from vosk-model-small-de-0.15/ivector/final.ie
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:183) Computing derived variables for iVector extractor
LOG (VoskAPI:ComputeDerivedVars():ivector-extractor.cc:204) Done.
LOG (VoskAPI:ReadDataFiles():model.cc:282) Loading HCL and G from vosk-model-small-de-0.15/graph/HCLr.fst vosk-model-small-de-0.15/graph/Gr.fst
LOG (VoskAPI:ReadDataFiles():model.cc:308) Loading winfo vosk-model-small-de-0.15/graph/phones/word_boundary.int
[+]Transcribing audio file....please wait!
hallo kaffee oder tee danke
"""