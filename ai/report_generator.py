# ==========================================================
# FILE: ai/report_generator.py
# SOC-GRADE REPORT ENGINE
# ==========================================================

from datetime import datetime
import os
import json


REPORT_DIR = "reports"


# ==========================================================
# ENSURE REPORT DIRECTORY EXISTS
# ==========================================================
def ensure_dir():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)


# ==========================================================
# SOC RISK SCORING ENGINE
# ==========================================================
def calculate_risk_level(content):
    text = content.lower()

    score = 0

    keywords = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1,
        "vulnerability": 2,
        "exploit": 3,
        "malware": 3,
        "breach": 4,
        "unauthorized": 3,
        "open port": 2,
        "rce": 4
    }

    for k, v in keywords.items():
        if k in text:
            score += v

    if score >= 10:
        return "CRITICAL", score
    elif score >= 7:
        return "HIGH", score
    elif score >= 4:
        return "MEDIUM", score
    else:
        return "LOW", score


# ==========================================================
# BUILD STRUCTURED REPORT
# ==========================================================
def build_report(content):
    risk, score = calculate_risk_level(content)

    return f"""
============================================================
                 🛡 SOC INTELLIGENCE REPORT
============================================================

📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠ Risk Level: {risk}
📊 Risk Score: {score}/20

------------------------------------------------------------
📌 EXECUTIVE SUMMARY
------------------------------------------------------------
Automated SOC analysis performed on target system.

------------------------------------------------------------
📡 RAW INTELLIGENCE OUTPUT
------------------------------------------------------------
{content}

------------------------------------------------------------
🧠 SOC INTERPRETATION
------------------------------------------------------------
- System behavior analyzed
- Threat indicators evaluated
- Exposure level classified

------------------------------------------------------------
🛠 RECOMMENDATIONS
------------------------------------------------------------
- Patch vulnerable services immediately if detected
- Monitor suspicious network activity
- Restrict exposed ports and services
- Enable logging and intrusion detection

============================================================
END OF REPORT
============================================================
"""


# ==========================================================
# SAVE REPORT
# ==========================================================


def save_report(content, prefix="report"):

    base_dir = os.path.join(os.getcwd(), "Documents")
    os.makedirs(base_dir, exist_ok=True)

    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    full_path = os.path.abspath(os.path.join(base_dir, filename))

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[REPORT SAVED] {full_path}")  # DEBUG TRACE

    return full_path