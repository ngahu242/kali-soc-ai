import subprocess
from tools.platform_engine import get_os

def detect_reverse_shell():

    data = subprocess.getoutput("ps aux && ss -tulpn")

    keywords = [
        "bash -i",
        "nc -e",
        "netcat",
        "python -c",
        "perl -e",
        "ruby -rsocket",
        "/dev/tcp/",
        "powershell",
        "cmd.exe /c",
        "bitsadmin"
    ]

    found = []

    for line in data.split("\n"):
        for word in keywords:
            if word.lower() in line.lower():
                found.append(line)

    if found:
        return "\n".join(found)

    return "No reverse shell indicators found."