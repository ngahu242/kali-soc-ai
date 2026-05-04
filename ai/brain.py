# ==========================================================
# FILE: ai/brain.py
# ELITE DYNAMIC AI ENGINE
# Context-Aware SOC Intelligence Core
# ==========================================================

import requests
import threading
import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from config import AI_MODE, OLLAMA_MODEL, GROQ_API_KEY, GROQ_MODEL

console = Console()
loading_done = False


# ==========================================================
# MODE CONFIGURATION
# ==========================================================
MODES = {

    "general": {
        "title": "🤖 AI ASSISTANT",
        "color": "cyan",
        "phases": [
            "Thinking...",
            "Researching answer...",
            "Generating response...",
            "Finalizing output..."
        ],
        "prompt": """
You are a helpful, intelligent assistant.

You can answer:
- general questions
- coding
- cybersecurity
- Linux
- research
- productivity
- troubleshooting
"""
    },

    "threat": {
        "title": "🛡 THREAT ENGINE",
        "color": "red",
        "phases": [
            "Scanning suspicious processes...",
            "Checking persistence...",
            "Correlating indicators...",
            "Scoring threats..."
        ],
        "prompt": """
You are an elite SOC Threat Hunter.

Analyze:
- suspicious processes
- malware indicators
- persistence
- privilege abuse
- lateral movement
- reverse shells

Return:
1. Findings
2. Severity
3. Risk Score
4. Recommendations
"""
    },

    "audit": {
        "title": "🔍 AUDIT ENGINE",
        "color": "green",
        "phases": [
            "Reviewing system posture...",
            "Checking services...",
            "Inspecting ports...",
            "Finalizing audit..."
        ],
        "prompt": """
You are a Linux Security Auditor.

Analyze:
- services
- ports
- users
- firewall
- updates
- security weaknesses

Return:
1. Findings
2. Severity
3. Fixes
4. Hardening Tips
"""
    },

    "health": {
        "title": "⚙ SYSTEM ENGINE",
        "color": "yellow",
        "phases": [
            "Checking CPU usage...",
            "Checking RAM...",
            "Checking disk health...",
            "Analyzing performance..."
        ],
        "prompt": """
You are a Linux performance engineer.

Analyze:
- CPU
- RAM
- Disk
- Load
- Services

Return:
1. Problems
2. Severity
3. Optimizations
"""
    },

    "scan": {
        "title": "🌐 RECON ENGINE",
        "color": "blue",
        "phases": [
            "Parsing ports...",
            "Fingerprinting services...",
            "Checking exposures...",
            "Assessing target..."
        ],
        "prompt": """
You are a network penetration analyst.

Analyze:
- nmap scans
- ports
- services
- versions
- risks

Return:
1. Findings
2. Attack Surface
3. Severity
4. Recommendations
"""
    },

    # ==========================================================
    # FIXED CVE ENGINE (IMPORTANT UPGRADE)
    # ==========================================================
    "cve": {
        "title": "☣ VULNERABILITY ENGINE",
        "color": "magenta",
        "phases": [
            "Checking package versions...",
            "Matching CVEs...",
            "Evaluating exploitability...",
            "Generating SOC report..."
        ],
        "prompt": """
    You are a STRICT SOC Vulnerability Analyst.

    CRITICAL RULES:
    - DO NOT explain tools, scanning, or methodology
    - DO NOT ask for missing data
    - DO NOT say "no data provided"
    - ALWAYS infer risk from whatever is available
    - EVEN partial or messy input must be analyzed

    You are analyzing installed software / package outputs.

    --------------------------------------------------
    OUTPUT FORMAT ONLY:

    [VULNERABILITIES]
    - package → CVE (if inferable) → severity (Low/Medium/High/Critical)

    [ANALYSIS]
    Short SOC summary of system exposure and risk posture.

    [RECOMMENDATIONS]
    - prioritize patching order
    - mitigation steps
    - upgrade strategy

    --------------------------------------------------

    INTELLIGENCE RULES:
    - If CVE is not explicitly known, estimate risk based on:
      * package criticality (system, network, browser, crypto, kernel)
      * age/outdated nature
      * exploit likelihood pattern
    - Never return empty output
    - Always produce a risk assessment even with minimal data
    """
    },

    "incident": {
        "title": "🚨 INCIDENT RESPONSE",
        "color": "bright_red",
        "phases": [
            "Collecting evidence...",
            "Determining containment...",
            "Planning eradication...",
            "Generating response..."
        ],
        "prompt": """
You are an Incident Response Commander.

Return:
1. Immediate Actions
2. Containment
3. Eradication
4. Recovery
5. Lessons Learned
"""
    },

    "autonomous": {
        "title": "🔥 AUTONOMOUS SOC CORE",
        "color": "bright_green",
        "phases": [
            "Monitoring host...",
            "Evaluating anomalies...",
            "Selecting response...",
            "Preparing action..."
        ],
        "prompt": """
You are a fully autonomous SOC AI.

Analyze telemetry and decide safe actions.

Return:
1. Situation
2. Threat Level
3. Recommended Action
4. Reasoning
"""
    },

    "forensics": {
        "title": "🧬 FORENSICS ENGINE",
        "color": "white",
        "phases": [
            "Reviewing artifacts...",
            "Checking hidden files...",
            "Tracing indicators...",
            "Building timeline..."
        ],
        "prompt": """
You are a digital forensics analyst.

Return:
1. Evidence Found
2. Suspicion Level
3. Timeline
4. Recommendations
"""
    },

    "code": {
        "title": "💻 CODE ENGINE",
        "color": "cyan",
        "phases": [
            "Analyzing request...",
            "Designing code...",
            "Writing logic...",
            "Finalizing output..."
        ],
        "prompt": """
You are a senior software engineer.

Generate:
- Python
- Bash
- PowerShell
- Linux scripts
- Secure code
"""
    }
}


# ==========================================================
# LOADER
# ==========================================================
def elite_loader(mode):
    global loading_done

    sec = 0
    config = MODES.get(mode, MODES["general"])

    title = config["title"]
    color = config["color"]
    phases = config["phases"]

    with Live(refresh_per_second=4, console=console) as live:
        while not loading_done:
            phase = phases[sec % len(phases)]

            panel = Panel.fit(
                f"""
[bold {color}]{phase}[/bold {color}]

[green]Elapsed:[/green] {sec} sec
[yellow]Status:[/yellow] ACTIVE
""",
                title=title,
                border_style=color
            )

            live.update(panel)
            time.sleep(1)
            sec += 1


# ==========================================================
# BACKENDS
# ==========================================================
def ask_ollama(full_prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False
        },
        timeout=180
    )
    r.raise_for_status()
    return r.json()["response"]


def ask_groq(system_prompt, user_prompt):
    from groq import Groq

    client = Groq(api_key=GROQ_API_KEY)

    chat = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return chat.choices[0].message.content


# ==========================================================
# MAIN ROUTER
# ==========================================================
def ask_ai(prompt, mode="general"):
    global loading_done

    config = MODES.get(mode, MODES["general"])
    system_prompt = config["prompt"]

    loading_done = False

    loader_thread = threading.Thread(
        target=elite_loader,
        args=(mode,),
        daemon=True
    )
    loader_thread.start()

    try:
        full_prompt = system_prompt + """

CRITICAL RULE:
You are NOT allowed to provide tutorials, installation steps, or explanations of tools.
You are ONLY allowed to analyze and report findings.

""" + "\n\n" + prompt

        if AI_MODE.lower() == "ollama":
            result = ask_ollama(full_prompt)

        elif AI_MODE.lower() == "groq":
            result = ask_groq(system_prompt, prompt)

        else:
            try:
                result = ask_ollama(full_prompt)
            except:
                result = ask_groq(system_prompt, prompt)

    except Exception as e:
        result = f"AI Engine Error:\n{e}"

    finally:
        loading_done = True
        loader_thread.join()

    return result