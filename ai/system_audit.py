from ai.brain import ask_ai
from tools.system_info import get_system_info
from tools.network_scanner import local_ports
from tools.firewall_tools import firewall_status
from ai.vuln_scanner import installed_updates

def full_audit():
    prompt = f"""
Perform full security audit.

SYSTEM:
{get_system_info()}

PORTS:
{local_ports()}

FIREWALL:
{firewall_status()}

UPDATES:
{installed_updates()}
"""
    return ask_ai(prompt)