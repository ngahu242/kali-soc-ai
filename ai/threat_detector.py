from ai.brain import ask_ai
from tools.process_monitor import suspicious_processes


def detect_threats():
    prompt = f"""
Analyze suspicious processes:

{suspicious_processes()}
"""

    return ask_ai(prompt)