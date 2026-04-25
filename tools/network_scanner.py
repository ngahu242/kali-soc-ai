import subprocess


def local_ports():
    return subprocess.getoutput("netstat -ano")


def ping_test():
    return subprocess.getoutput("ping 8.8.8.8 -n 4")


def scan_target(ip):
    return subprocess.getoutput(f"nmap -sV {ip}")