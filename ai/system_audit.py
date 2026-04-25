from ai.brain import ask_ai
from tools.system_info import get_system_info
from tools.process_monitor import suspicious_processes
from tools.network_scanner import local_ports
from ai.vuln_scanner import firewall_status


def full_audit():
    data = f"""
SYSTEM:
{get_system_info()}

SUSPICIOUS PROCESSES:
{suspicious_processes()}

OPEN PORTS:
{local_ports()}

FIREWALL:
{firewall_status()}
"""

    prompt = f"""
Perform a full security audit:

{data}
"""

    return ask_ai(prompt)