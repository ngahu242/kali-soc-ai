# ==========================================================
# FILE: ai/remote_assessor.py
# REMOTE CYBER INTELLIGENCE ENGINE (AUTO MODE v5)
# ==========================================================

import subprocess
import socket
import platform
import ipaddress
import re
from urllib.parse import urlparse

import requests
from ai.brain import ask_ai


# ==========================================================
# 1. AUTO DETECT TARGET TYPE
# ==========================================================
def normalize_target(target: str):
    """
    Extract hostname from:
    - IP
    - Domain
    - URL
    """

    target = target.strip()

    # URL handling
    if "://" in target:
        parsed = urlparse(target)
        target = parsed.netloc

    # remove port if exists
    target = target.split(":")[0]

    return target


# ==========================================================
# 2. CHECK IF INPUT IS IP
# ==========================================================
def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except:
        return False


# ==========================================================
# 3. RESOLVE DOMAIN → IP
# ==========================================================
def resolve_ip(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None


# ==========================================================
# 4. PING CHECK
# ==========================================================
def is_host_reachable(ip):
    try:
        if platform.system().lower() == "windows":
            cmd = f"ping -n 1 -w 1000 {ip}"
        else:
            cmd = f"ping -c 1 -W 1 {ip}"

        result = subprocess.getoutput(cmd).lower()

        success_markers = [
            "ttl=",
            "bytes=",
            "reply from",
            "time="
        ]

        return any(marker in result for marker in success_markers)

    except:
        return False

# ==========================================================
# 5. HOSTNAME LOOKUP
# ==========================================================
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown Host"


# ==========================================================
# 6. OS FINGERPRINT (LIGHTWEIGHT)
# ==========================================================
def detect_os(ip):
    try:
        result = subprocess.getoutput(f"ping -c 1 {ip}").lower()

        if "ttl=64" in result:
            return "Linux / Unix (Likely)"
        elif "ttl=128" in result:
            return "Windows (Likely)"
        elif "ttl=255" in result:
            return "Network Device (Router/Switch)"
        return "Unknown OS"
    except:
        return "Unknown"


# ==========================================================
# 7. PORT SCANNER
# ==========================================================
def scan_ports(ip):
    ports = [21,22,23,25,53,80,110,139,143,443,445,3389,8080]
    open_ports = []

    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)

            s.close()
        except:
            continue

    return open_ports


# ==========================================================
# 8. SERVICE MAPPING
# ==========================================================
def map_services(ports):
    mapping = {
        21: "FTP (Insecure)",
        22: "SSH (Secure Remote Access)",
        23: "Telnet (Critical Risk)",
        25: "SMTP Mail Server",
        53: "DNS Service",
        80: "HTTP Web Server",
        110: "POP3 Email",
        139: "NetBIOS",
        143: "IMAP Email",
        443: "HTTPS Secure Web",
        445: "SMB (High Risk)",
        3389: "RDP (Critical Risk)",
        8080: "Web Proxy / Admin Panel"
    }

    return [mapping.get(p, f"Unknown Service ({p})") for p in ports]


# ==========================================================
# 9. WEB INTELLIGENCE (FOR DOMAINS / URLS)
# ==========================================================
def web_intel(host):
    try:
        url = host if host.startswith("http") else "http://" + host
        r = requests.get(url, timeout=5)

        return {
            "status": r.status_code,
            "server": r.headers.get("Server"),
            "powered_by": r.headers.get("X-Powered-By")
        }
    except:
        return {}


# ==========================================================
# 10. MAIN AUTO INTELLIGENCE ENGINE
# ==========================================================
def remote_scan(target, confirm=False):

    host = normalize_target(target)

    # STEP 1: RESOLVE ONLY IF NOT IP
    ip = host if is_ip(host) else resolve_ip(host)

    if not ip:
        return f"""
[REMOTE INTELLIGENCE REPORT]

TARGET: {target}

STATUS: ❌ RESOLUTION FAILED

- Cannot resolve host or IP
- Invalid or unreachable target
"""

    # STEP 2: PING CHECK
    reachable = is_host_reachable(ip)

    if not reachable:
        return f"""
[REMOTE INTELLIGENCE REPORT]

TARGET: {target}
IP: {ip}

STATUS: ❌ UNREACHABLE

- No ICMP response
- Firewall or offline host
"""

    # STEP 3: CONFIRMATION MODE
    if confirm:
        return f"""
[HOST DISCOVERY]

TARGET: {target}
IP: {ip}

STATUS: ✅ REACHABLE

System is ready for FULL SOC intelligence scan.

Includes:
- OS fingerprinting
- Port scan
- Service mapping
- Web intelligence (if applicable)

Proceed to deep analysis?
"""

    # STEP 4: FULL RECON
    hostname = get_hostname(ip)
    os_guess = detect_os(ip)
    ports = scan_ports(ip)
    services = map_services(ports)
    web_data = web_intel(host)

    # STEP 5: AI ANALYSIS
    prompt = f"""
You are an elite SOC Cyber Intelligence Analyst.

Perform FULL remote security assessment.

--------------------------------------------------
TARGET
--------------------------------------------------
Input: {target}
Resolved IP: {ip}
Hostname: {hostname}
OS: {os_guess}

Open Ports: {ports}
Services: {services}

Web Intelligence: {web_data}

--------------------------------------------------
TASKS
--------------------------------------------------

1. Attack Surface Mapping
2. System Role Identification
3. Threat Actor Profiling
4. Risk Assessment (NO EXPLOITS)
5. Security Rating (LOW → CRITICAL)
6. Defensive Recommendations

--------------------------------------------------
OUTPUT FORMAT:

[REMOTE PROFILE]
[ATTACK SURFACE]
[THREAT INTELLIGENCE]
[RISK LEVEL]
[DEFENSE STRATEGY]

RULES:
- No hacking instructions
- No exploitation steps
- SOC defensive analysis only
"""

    return ask_ai(prompt, mode="scan")