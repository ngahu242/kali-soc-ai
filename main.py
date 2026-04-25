from ai.system_audit import full_audit
from ai.it_support import system_health
from ai.threat_detector import detect_threats
from tools.network_scanner import scan_target
from ai.brain import ask_ai


def analyze_everything():
    return full_audit()


def health():
    return system_health()


def threats():
    return detect_threats()


def scan(ip):
    result = scan_target(ip)

    prompt = f"""
Analyze this Nmap scan:

{result}
"""

    return ask_ai(prompt)