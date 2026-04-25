import subprocess


def all_services():
    return subprocess.getoutput("sc query type= service state= all")


def failed_services():
    return subprocess.getoutput("sc query state= inactive")