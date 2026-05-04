import time
from datetime import datetime

from tools.log_analyzer import auth_logs, sys_logs, failed_logins
from tools.network_scanner import local_ports
from tools.process_monitor import suspicious_processes
from tools.platform_engine import get_os


# ==========================================================
# EVENT NORMALIZATION
# ==========================================================
def normalize_event(source, data, severity="low"):
    return {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "data": data,
        "severity": severity,
        "os": get_os()
    }


# ==========================================================
# LOG COLLECTION LAYER
# ==========================================================
def collect_events():

    events = []

    # AUTH LOGS
    auth = auth_logs()
    if "failed" in auth.lower() or "invalid" in auth.lower():
        events.append(normalize_event("AUTH_LOGS", auth, "medium"))

    # FAILED LOGINS
    failed = failed_logins()
    if failed and len(failed) > 10:
        events.append(normalize_event("FAILED_LOGINS", failed, "high"))

    # SYSTEM LOGS
    sys = sys_logs()
    if "error" in sys.lower():
        events.append(normalize_event("SYSTEM_LOGS", sys, "medium"))

    # NETWORK PORTS
    ports = local_ports()
    if "LISTEN" in ports or "0.0.0.0" in ports:
        events.append(normalize_event("NETWORK", ports, "low"))

    # SUSPICIOUS PROCESSES
    proc = suspicious_processes()
    if proc and proc != "No suspicious process names found.":
        events.append(normalize_event("PROCESS", proc, "high"))

    return events


# ==========================================================
# CORRELATION ENGINE
# ==========================================================
def correlate(events):

    attack_score = 0
    findings = []

    for e in events:

        if e["severity"] == "high":
            attack_score += 3
        elif e["severity"] == "medium":
            attack_score += 2
        else:
            attack_score += 1

        findings.append(f"{e['source']} → {e['severity']}")

    # Attack classification
    if attack_score >= 10:
        level = "CRITICAL ATTACK"
    elif attack_score >= 6:
        level = "HIGH RISK"
    elif attack_score >= 3:
        level = "SUSPICIOUS ACTIVITY"
    else:
        level = "NORMAL"

    return {
        "attack_score": attack_score,
        "level": level,
        "findings": findings,
        "event_count": len(events)
    }


# ==========================================================
# SIEM CORE ENGINE (MAIN ENTRY)
# ==========================================================
def run_siem_core():

    start = time.time()

    events = collect_events()
    result = correlate(events)

    duration = round(time.time() - start, 2)

    return {
        "timestamp": datetime.now().isoformat(),
        "runtime_seconds": duration,
        "os": get_os(),
        "events": events,
        "analysis": result
    }