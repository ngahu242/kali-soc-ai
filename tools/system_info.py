import subprocess
import platform


def get_system_info():
    system = platform.system()

    return f"""
OS: {platform.system()} {platform.release()}

HOSTNAME:
{subprocess.getoutput("hostname")}

UPTIME:
{subprocess.getoutput("uptime" if system != "Windows" else "net stats srv")}

CPU:
{subprocess.getoutput("wmic cpu get name" if system == "Windows" else "lscpu | head -20")}

RAM:
{subprocess.getoutput("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize" if system == "Windows" else "free -h")}

DISK:
{subprocess.getoutput("wmic logicaldisk get size,freespace,caption" if system == "Windows" else "df -h")}
"""