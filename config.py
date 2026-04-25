import os
from dotenv import load_dotenv

load_dotenv()

# Modes:
# auto    = OpenAI if key exists else Ollama
# openai  = force OpenAI
# ollama  = force Ollama

AI_MODE = os.getenv("AI_MODE", "auto")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")