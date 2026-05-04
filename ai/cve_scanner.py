# ==========================================================
# FILE: ai/cve_scanner.py (EXPLOIT INTELLIGENCE MODE)
# ==========================================================

import subprocess
import re
from ai.brain import ask_ai
from ai.exploit_intel import get_cve_details


def extract_packages():
    raw = subprocess.getoutput(
        "apt list --upgradable 2>/dev/null | grep -v Listing | head -40"
    )

    packages = []

    for line in raw.splitlines():
        match = re.match(r"([^/]+)/", line)
        if match:
            packages.append(match.group(1))

    return packages, raw


def scan_packages():

    packages, raw_output = extract_packages()

    if not packages:
        return "🟢 SYSTEM CLEAN: No vulnerable packages detected."

    enriched_data = []

    # ======================================================
    # STEP 1: SIMULATED CVE MAPPING (SOC DEMO LOGIC)
    # ======================================================
    for pkg in packages:

        # Simulated CVE mapping (replace later with real DB mapping)
        fake_cve = f"CVE-2024-{abs(hash(pkg)) % 9999}"

        intel = get_cve_details(fake_cve)

        enriched_data.append(
            f"- {pkg} → {intel['cve']} | CVSS: {intel['cvss']} | {intel['exploit_hint']}"
        )

    # ======================================================
    # STEP 2: BUILD SOC INTELLIGENCE PROMPT
    # ======================================================
    prompt = f"""
YOU ARE A SOC VULNERABILITY INTELLIGENCE ENGINE.

Analyze enriched vulnerability intelligence:

{chr(10).join(enriched_data)}

---

TASK:
1. Rank vulnerabilities by risk
2. Identify exploit-priority targets
3. Provide patch urgency
4. Highlight critical exposure paths

FORMAT:

[VULNERABILITIES]
- package → CVE → CVSS → exploit status → severity

[EXPLOIT INTELLIGENCE]
summary of attack exposure

[RECOMMENDATIONS]
- prioritized patching steps
"""

    return ask_ai(prompt, mode="cve")