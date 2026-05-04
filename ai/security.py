def is_safe(command):

    blocked = [
        "rm -rf",
        "mkfs",
        "shutdown",
        "reboot",
        "poweroff",
        "dd if=",
        ":(){:|:&};:"
    ]

    for item in blocked:
        if item in command.lower():
            return False

    return True