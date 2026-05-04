import subprocess
from tools.platform_engine import get_os

def local_ports():

    if get_os() == "windows":
        return subprocess.getoutput("netstat -ano")

    return subprocess.getoutput("ss -tulpn")


def ping_test():

    if get_os() == "windows":
        return subprocess.getoutput("ping 8.8.8.8 -n 4")

    return subprocess.getoutput("ping -c 4 8.8.8.8")

def scan_target(ip):

    system = platform.system().lower()

    if system == "windows":
        # Windows fallback (nmap still required if installed)
        return subprocess.getoutput(f"nmap -sV -Pn {ip}")

    else:
        # Linux / Kali
        return subprocess.getoutput(f"nmap -sV -Pn {ip}")