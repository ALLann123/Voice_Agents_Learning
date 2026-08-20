from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()

for model in models.data:
    print(model.id)

"""
python list_groq_models.py
meta-llama/llama-prompt-guard-2-86m
openai/gpt-oss-120b
groq/compound
allam-2-7b
whisper-large-v3-turbo
whisper-large-v3
canopylabs/orpheus-v1-english
qwen/qwen3.6-27b
openai/gpt-oss-20b
canopylabs/orpheus-arabic-saudi
openai/gpt-oss-safeguard-20b
meta-llama/llama-prompt-guard-2-22m
groq/compound-mini

"""