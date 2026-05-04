from tools.platform_engine import run


def sudo_users():
    return run(
        cmd_linux="getent group sudo",
        cmd_windows="net localgroup administrators"
    )


def last_logins():
    return run(
        cmd_linux="last -10",
        cmd_windows="wevtutil qe Security /c:10 /f:text"
    )


def logged_users():
    return run(
        cmd_linux="who",
        cmd_windows="query user"
    )