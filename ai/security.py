def is_safe(command):
    blocked = [
        "rm -rf",
        "shutdown",
        "reboot",
        "mkfs",
        "dd if=",
        "format",
        "del /f"
    ]

    for item in blocked:
        if item in command.lower():
            return False

    return True