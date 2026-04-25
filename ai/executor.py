import subprocess
from ai.security import is_safe


def run_command(command):
    if not is_safe(command):
        return "Blocked dangerous command."

    return subprocess.getoutput(command)