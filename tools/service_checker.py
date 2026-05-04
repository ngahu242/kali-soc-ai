import subprocess
import platform

def all_services():

    system = platform.system().lower()

    if system == "windows":
        return subprocess.getoutput("wmic service list brief")

    return subprocess.getoutput("systemctl list-units --type=service --all")


def failed_services():

    system = platform.system().lower()

    if system == "windows":
        return subprocess.getoutput(
            'powershell "Get-Service | Where-Object {$_.Status -ne \'Running\'}"'
        )

    return subprocess.getoutput("systemctl --failed")