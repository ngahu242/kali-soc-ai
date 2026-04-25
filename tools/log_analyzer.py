import os


def logs():
    path = r"C:\Windows\System32\winevt\Logs"

    if os.path.exists(path):
        return "Windows logs detected."

    return "Logs path not found."