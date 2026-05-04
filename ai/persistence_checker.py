import os
import platform
import subprocess

def detect_persistence():
    system = platform.system()

    findings = []

    # =========================
    # LINUX PERSISTENCE
    # =========================
    if system != "Windows":
        try:
            cron = subprocess.getoutput("crontab -l 2>/dev/null")
            systemd = subprocess.getoutput("systemctl list-units --type=service --state=running")

            if cron.strip():
                findings.append("[Linux] Cron Jobs Detected:\n" + cron)

            if "enabled" in systemd.lower():
                findings.append("[Linux] Active Systemd Services Detected")

        except:
            pass

    # =========================
    # WINDOWS PERSISTENCE
    # =========================
    else:
        try:
            startup = subprocess.getoutput("wmic startup get caption,command")
            tasks = subprocess.getoutput("schtasks /query /fo LIST /v")

            if startup:
                findings.append("[Windows] Startup Entries:\n" + startup)

            if tasks:
                findings.append("[Windows] Scheduled Tasks Detected")

        except:
            pass

    return "\n\n".join(findings) if findings else "No persistence mechanisms detected."