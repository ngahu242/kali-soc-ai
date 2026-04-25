import platform
import subprocess


def get_system_info():
    return f"""
OS: {platform.system()}
Release: {platform.release()}
Machine: {platform.machine()}

CPU:
{subprocess.getoutput("wmic cpu get name")}

RAM:
{subprocess.getoutput("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value")}

DISK:
{subprocess.getoutput("wmic logicaldisk get caption,freespace,size")}
"""