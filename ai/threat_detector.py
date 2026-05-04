from ai.brain import ask_ai
from tools.process_monitor import suspicious_processes
from tools.network_scanner import local_ports
from tools.log_analyzer import failed_logins

def detect_threats():
    prompt = f"""
Analyze for active threats.

PROCESSES:
{suspicious_processes()}

PORTS:
{local_ports()}

FAILED SSH:
{failed_logins()}
"""
    return ask_ai(prompt)