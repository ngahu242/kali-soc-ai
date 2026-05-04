import platform
import subprocess


def get_os():
    return platform.system().lower()


def run(cmd_linux=None, cmd_windows=None):
    system = get_os()

    try:
        if system == "windows":
            if not cmd_windows:
                return "[WARN] No Windows command provided."
            return subprocess.getoutput(cmd_windows)

        else:
            if not cmd_linux:
                return "[WARN] No Linux command provided."
            return subprocess.getoutput(cmd_linux)

    except Exception as e:
        return f"[ERROR] {e}"