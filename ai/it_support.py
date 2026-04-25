from ai.brain import ask_ai
from tools.system_info import get_system_info
from tools.network_scanner import ping_test


def system_health():
    data = f"""
SYSTEM:
{get_system_info()}

NETWORK:
{ping_test()}
"""

    prompt = f"""
Analyze this machine for health/performance issues.
Recommend fixes.

{data}
"""

    return ask_ai(prompt)