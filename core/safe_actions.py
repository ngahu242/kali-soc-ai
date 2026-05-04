import subprocess


def restart_service(service):
    return subprocess.getoutput(f"systemctl restart {service}")


def check_disk():
    return subprocess.getoutput("df -h")


def kill_process(pid):
    return subprocess.getoutput(f"kill -9 {pid}")