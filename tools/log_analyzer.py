import subprocess
from tools.platform_engine import get_os

def auth_logs():

    if get_os() == "windows":
        return subprocess.getoutput('wevtutil qe Security /c:30 /f:text')

    return subprocess.getoutput("tail -30 /var/log/auth.log")


def sys_logs():

    if get_os() == "windows":
        return subprocess.getoutput('wevtutil qe System /c:30 /f:text')

    return subprocess.getoutput("tail -30 /var/log/syslog")


def failed_logins():

    if get_os() == "windows":
        return subprocess.getoutput(
            'wevtutil qe Security /q:"*[System[(EventID=4625)]]" /c:20 /f:text'
        )

    return subprocess.getoutput("grep 'Failed password' /var/log/auth.log | tail -20")