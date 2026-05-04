# ai/soc_engine.py

from ai.system_audit import full_audit
from ai.it_support import system_health
from ai.threat_detector import detect_threats


def audit():
    return full_audit()


def health():
    return system_health()


def threats():
    return detect_threats()