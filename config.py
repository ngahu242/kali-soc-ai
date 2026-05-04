import os
from dotenv import load_dotenv

load_dotenv()

AI_MODE = os.getenv("AI_MODE", "auto")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")