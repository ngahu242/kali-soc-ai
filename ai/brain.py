import requests
from config import AI_MODE, OPENAI_API_KEY, OLLAMA_MODEL

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
except:
    client = None


SYSTEM_PROMPT = """
You are an expert SOC Analyst + Linux IT Engineer.

Analyze:
- vulnerabilities
- threats
- suspicious processes
- logs
- services
- system health
- networking issues

Always return:
1. Findings
2. Severity
3. Recommendations
4. Commands when useful
"""


def ask_openai(prompt):
    if not client:
        return "OpenAI library missing."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": SYSTEM_PROMPT + "\n\n" + prompt,
                "stream": False
            }
        )

        return response.json()["response"]

    except:
        return "Ollama not running. Start with: ollama run llama3"


def ask_ai(prompt):
    if AI_MODE == "openai":
        return ask_openai(prompt)

    if AI_MODE == "ollama":
        return ask_ollama(prompt)

    if OPENAI_API_KEY:
        return ask_openai(prompt)

    return ask_ollama(prompt)