import subprocess
from tools.platform_engine import get_os

def detect_mitm():

    if get_os() == "windows":
        arp = subprocess.getoutput("arp -a")
    else:
        arp = subprocess.getoutput("arp -a")

    suspicious = []

    for line in arp.split("\n"):
        if "incomplete" in line.lower():
            suspicious.append(line)

    if suspicious:
        return "Possible MITM / ARP spoofing:\n" + "\n".join(suspicious)

    return "No MITM indicators found."