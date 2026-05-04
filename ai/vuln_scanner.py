import subprocess

def installed_updates():
    return subprocess.getoutput("apt list --upgradable 2>/dev/null")

def suid_files():
    return subprocess.getoutput("find / -perm -4000 2>/dev/null | head -50")