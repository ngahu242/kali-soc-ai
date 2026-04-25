import subprocess


def firewall_status():
    return subprocess.getoutput("netsh advfirewall show allprofiles")


def installed_updates():
    return subprocess.getoutput("wmic qfe list brief")