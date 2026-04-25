import subprocess


def running_processes():
    return subprocess.getoutput("tasklist")


def suspicious_processes():
    output = subprocess.getoutput("tasklist")

    keywords = [
        "powershell",
        "cmd.exe",
        "python",
        "nc.exe",
        "netcat"
    ]

    found = []

    for line in output.split("\n"):
        for word in keywords:
            if word.lower() in line.lower():
                found.append(line)

    return "\n".join(found) if found else "No suspicious process names found."