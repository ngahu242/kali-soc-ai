import subprocess

def running_processes():
    return subprocess.getoutput("ps aux --sort=-%mem | head -25")

def suspicious_processes():
    data = subprocess.getoutput("ps aux")

    keywords = [
        "nc",
        "netcat",
        "python -c",
        "bash -i",
        "curl http",
        "wget http"
    ]

    found = []

    for line in data.split("\n"):
        for word in keywords:
            if word in line.lower():
                found.append(line)

    return "\n".join(found) if found else "No suspicious process names found."