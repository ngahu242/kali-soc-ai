from ai.brain import ask_ai
from tools.system_info import get_system_info
from tools.service_checker import failed_services
from tools.disk_tools import disk_usage

def system_health():

    prompt = f"""
Analyze machine health (Windows or Linux).

SYSTEM INFO:
{get_system_info()}

FAILED SERVICES:
{failed_services()}

DISK USAGE:
{disk_usage()}

Return:
1. Health summary
2. Performance issues
3. Security risks
4. Recommendations
"""

    return ask_ai(prompt, mode="health")