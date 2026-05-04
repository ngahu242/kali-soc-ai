from tools.platform_engine import run


def firewall_status():
    return run(
        cmd_linux="ufw status verbose",
        cmd_windows="netsh advfirewall show allprofiles"
    )


def iptables_rules():
    return run(
        cmd_linux="iptables -L",
        cmd_windows="netsh advfirewall firewall show rule name=all"
    )