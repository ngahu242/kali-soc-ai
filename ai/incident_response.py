import subprocess
from tools.platform_engine import get_os

def block_ip(ip):

    if get_os() == "windows":
        return subprocess.getoutput(f'netsh advfirewall firewall add rule name="BLOCK {ip}" dir=in action=block remoteip={ip}')

    return subprocess.getoutput(f"ufw deny from {ip}")


def kill_process(pid):

    if get_os() == "windows":
        return subprocess.getoutput(f"taskkill /PID {pid} /F")

    return subprocess.getoutput(f"kill -9 {pid}")