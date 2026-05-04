from ai.brain import ask_ai
from tools.log_analyzer import auth_logs, sys_logs

def correlate_logs():

    auth = auth_logs()[:1500]
    sys = sys_logs()[:1500]

    prompt = f"""
You are a SIEM analyst.

Return:
- Attack patterns
- Severity
- Timeline
- Recommendations

AUTH LOGS:
{auth}

SYSLOG:
{sys}
"""

    return ask_ai(prompt, mode="threat")