from tools.platform_engine import run

def detect_bruteforce():

    logs = run(
        cmd_linux="grep 'Failed password' /var/log/auth.log | tail -50",
        cmd_windows='wevtutil qe Security /q:"*[System[(EventID=4625)]]" /c:50 /f:text'
    )

    if not logs:
        return "No authentication logs found."

    lines = logs.split("\n")
    count = len([l for l in lines if l.strip()])

    if count > 5:
        return f"""🛡 BRUTE FORCE ALERT
--------------------------------
Events: {count}
Risk: HIGH
Recommendation: Enable MFA + block IPs
"""

    return f"""🟢 AUTH STATUS CLEAN
--------------------------------
Events analyzed: {count}
No brute force detected."""