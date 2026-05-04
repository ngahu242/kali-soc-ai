import subprocess
import platform

def disk_usage():

    system = platform.system().lower()

    if system == "windows":
        return subprocess.getoutput("wmic logicaldisk get caption,freespace,size")

    return subprocess.getoutput("df -h")


def large_files():

    system = platform.system().lower()

    if system == "windows":
        return subprocess.getoutput(
            'powershell "Get-ChildItem C:\\ -Recurse -ErrorAction SilentlyContinue | '
            'Sort-Object Length -Descending | Select-Object -First 20 FullName,Length"'
        )

    return subprocess.getoutput("find / -type f -size +200M 2>/dev/null | head -20")