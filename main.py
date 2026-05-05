# ==========================================================
# FILE: main.py
# KALI SOC AI - ENTERPRISE SOC COMMAND CENTER
# Remote Assessment Integrated
# ==========================================================

import os
import signal
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
from rich import box

# ================= CORE =================
from ai.soc_engine import audit, health, threats
from ai.brain import ask_ai

# ================= DETECTION =================
from ai.siem_engine import correlate_logs
from ai.brute_force_detector import detect_bruteforce
from ai.reverse_shell_detector import detect_reverse_shell
from ai.mitm_detector import detect_mitm
from ai.cve_scanner import scan_packages

# ================= RESPONSE =================
from ai.incident_response import block_ip, kill_process

# ================= MEMORY =================
from ai.memory import remember, recall

# ================= EXTRA =================
from ai.voice_control import voice_mode
from ai.report_generator import save_report
from ai.malware_hunter import scan_tmp, hidden_files

# ================= TOOLS =================
from tools.network_scanner import scan_target
from tools.firewall_tools import firewall_status
from tools.user_audit import sudo_users, last_logins, logged_users
from tools.disk_tools import disk_usage, large_files

# ================= REMOTE ASSESSOR =================
from ai.remote_assessor import remote_scan

# ================= AUTONOMOUS =================
from core.engine import run_autonomous_mode
from core.auto_repair import auto_heal
from core.autonomous_formatter import format_autonomous_report

console = Console()
last_output = ""

scan_session = []

CURRENT_CONTEXT = {
    "mode": "IDLE",
    "title": "",
    "data": "",
    "last_action": "",
    "flow_lock": False   #
}


SYSTEM_ACTIVE = True
FLOW_ENABLED = True

# ==========================================================
# SOC WORKFLOW ENGINE
# ==========================================================
def related_module_selector():
    console.print(
        Panel.fit(
            """
[bold yellow]RELATED MODULES[/bold yellow]

1. Security Analysis Suite
2. Threat Intelligence Engine
3. Incident Response Toolkit
4. Forensics Suite
5. Remote Device Scan
""",
            border_style="yellow",
            title="MODULE SELECTOR"
        )
    )

    return Prompt.ask(
        "Select module",
        choices=["1", "2", "3", "4", "5"]
    )

# ==========================================================
# CTRL + C HANDLER
# ==========================================================
def handle_ctrl_c(sig, frame):
    global CURRENT_CONTEXT

    console.print("\n[bold yellow]CTRL + C INTERRUPT DETECTED[/bold yellow]")

    console.print(
        Panel.fit(
            f"""
[bold cyan]CURRENT SOC STATE[/bold cyan]

Mode: {CURRENT_CONTEXT.get('mode')}
Module: {CURRENT_CONTEXT.get('title')}
Last Action: {CURRENT_CONTEXT.get('last_action')}
""",
            border_style="yellow",
            title="INTERRUPT CONTEXT"
        )
    )

    console.print("[green]Returning safely to SOC dashboard...[/green]")
# ==========================================================
# UI
# ==========================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    logo = r"""
██╗  ██╗ █████╗ ██╗     ██╗    ███████╗ ██████╗  ██████╗     █████╗ ██╗
██║ ██╔╝██╔══██╗██║     ██║    ██╔════╝██╔═══██╗██╔════╝    ██╔══██╗██║
█████╔╝ ███████║██║     ██║    ███████╗██║   ██║██║         ███████║██║
██╔═██╗ ██╔══██║██║     ██║    ╚════██║██║   ██║██║         ██╔══██║██║
██║  ██╗██║  ██║███████╗██║    ███████║╚██████╔╝╚██████╗    ██║  ██║██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝    ╚══════╝ ╚═════╝  ╚═════╝    ╚═╝  ╚═╝╚═╝
"""

    console.print(
        Panel.fit(
            Align.center(
                f"[bold green]{logo}[/bold green]\n"
                "[bold cyan]Elite SOC | Threat Hunting | Kali Linux AI[/bold cyan]"
            ),
            border_style="green",
            title="🛡 KALI SOC AI",
            subtitle="Cyber Defense Command Center"
        )
    )


def status_bar():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(
        Panel(
            f"[green]ONLINE[/green] | [cyan]{now}[/cyan]",
            border_style="green"
        )
    )


# ==========================================================
# HELP CENTER
# ==========================================================
def help_center():
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()

    # ==========================================
    # HEADER
    # ==========================================
    console.print(
        Panel.fit(
            "[bold cyan]📘 SOC AI HELP CENTER & DOCUMENTATION[/bold cyan]\n"
            "[dim]Your complete guide to the SOC Voice & AI System[/dim]",
            border_style="cyan"
        )
    )

    # ==========================================
    # CORE MODULES TABLE
    # ==========================================
    table = Table(title="🧩 SOC Modules Overview", border_style="green")

    table.add_column("Module", style="cyan", no_wrap=True)
    table.add_column("Command", style="yellow")
    table.add_column("Description", style="white")

    table.add_row("Help Center", "help", "Open help and documentation")
    table.add_row("System Analysis", "analysis / audit", "Run full system security scan")
    table.add_row("Threat Intelligence", "threat / malware", "Check vulnerabilities, CVEs")
    table.add_row("Incident Response", "incident / block ip", "Respond to active threats")
    table.add_row("Forensics", "forensics", "Investigate system activity/logs")
    table.add_row("System Admin", "system / firewall", "Manage users, firewall, services")
    table.add_row("Reporting", "report", "Generate/export reports")
    table.add_row("Maintenance", "health / maintenance", "Auto-heal + system fixes")
    table.add_row("Remote Scan", "remote / scan host", "Scan external systems")
    table.add_row("Clear UI", "clear", "Reset dashboard UI")

    console.print(table)

    # ==========================================
    # VOICE COMMAND GUIDE
    # ==========================================
    console.print(
        Panel.fit(
            "[bold green]🎤 VOICE COMMAND GUIDE[/bold green]\n\n"
            "• Say commands clearly (e.g. 'run analysis')\n"
            "• Use exact commands for SOC modules\n"
            "• Anything else → handled by AI\n\n"
            "[cyan]Examples:[/cyan]\n"
            "- 'analysis'\n"
            "- 'threat scan'\n"
            "- 'check system health'\n"
            "- 'what is a firewall'\n",
            border_style="green"
        )
    )

    # ==========================================
    # VOICE CONTROL COMMANDS
    # ==========================================
    console.print(
        Panel.fit(
            "[bold magenta]🎯 VOICE CONTROL COMMANDS[/bold magenta]\n\n"
            "• exit voice mode  → Exit voice assistant\n"
            "• stop voice       → Stop listening\n"
            "• switch to ai     → Open chat mode\n"
            "• exit system      → Shutdown entire system\n\n"
            "[dim]These commands always override everything[/dim]",
            border_style="magenta"
        )
    )

    # ==========================================
    # AI MODE EXPLANATION
    # ==========================================
    console.print(
        Panel.fit(
            "[bold yellow]🧠 AI MODE (JARVIS)[/bold yellow]\n\n"
            "The AI assistant can:\n"
            "• Answer cybersecurity questions\n"
            "• Explain logs, threats, vulnerabilities\n"
            "• Assist with Linux & SOC operations\n"
            "• Continue conversations with memory\n\n"
            "[cyan]Example:[/cyan]\n"
            "'Explain CVE vulnerabilities'\n"
            "'Analyze this log: ...'\n",
            border_style="yellow"
        )
    )

    # ==========================================
    # SYSTEM FLOW EXPLANATION
    # ==========================================
    console.print(
        Panel.fit(
            "[bold blue]⚙️ SYSTEM FLOW[/bold blue]\n\n"
            "1. Voice Input Captured\n"
            "2. Exact Command Match → Runs SOC Module\n"
            "3. If no match → AI handles request\n"
            "4. Returns to listening mode automatically\n\n"
            "[dim]No crashes. No resets. Continuous session.[/dim]",
            border_style="blue"
        )
    )

    # ==========================================
    # TROUBLESHOOTING
    # ==========================================
    console.print(
        Panel.fit(
            "[bold red]🛠 TROUBLESHOOTING[/bold red]\n\n"
            "• No voice detected → Check microphone\n"
            "• Wrong command → Speak clearly / use exact command\n"
            "• Module not responding → Check imports in main.py\n"
            "• AI not responding → Check API / offline mode\n\n"
            "[cyan]Tip:[/cyan] Use 'clear' to reset interface",
            border_style="red"
        )
    )

    # ==========================================
    # FOOTER
    # ==========================================
    console.print(
        Panel.fit(
            "[bold cyan]🚀 SOC AI SYSTEM READY[/bold cyan]\n"
            "[dim]Voice + AI + Security Automation in one system[/dim]",
            border_style="cyan"
        )
    )
# ==========================================================
# OUTPUT ENGINE
# ==========================================================
def investigation_mode():
    if not CURRENT_CONTEXT["data"]:
        console.print("[red]No active investigation context.[/red]")
        return

    console.print(
        Panel.fit(
            """
[bold cyan]INVESTIGATION MODE ACTIVE[/bold cyan]

Ask follow-up questions based on the latest analysis.
Type 'exit' to return.
""",
            border_style="cyan",
            title="SOC INVESTIGATION"
        )
    )

    while True:
        q = Prompt.ask("SOC AI")

        if q.lower() in ["exit", "quit", "back"]:
            return

        prompt = f"""
You are a SOC analyst continuing an investigation.

CASE TITLE:
{CURRENT_CONTEXT["title"]}

FORENSIC DATA:
{CURRENT_CONTEXT["data"]}

USER QUESTION:
{q}

Respond as a cybersecurity investigator:
- explain findings
- connect indicators
- suggest defensive actions
"""

        response = ask_ai(prompt)

        console.print(
            Panel(response, title="AI ANALYSIS", border_style="green")
        )
def render_output(title, data):
    global last_output, scan_session, SYSTEM_ACTIVE, CURRENT_CONTEXT

    # ======================================================
    # HARD STOP CHECK
    # ======================================================
    if not SYSTEM_ACTIVE:
        return

    formatted = str(data)
    last_output = formatted

    # ======================================================
    # SAFE CONTEXT INIT (prevents KeyError)
    # ======================================================
    if "mode" not in CURRENT_CONTEXT:
        CURRENT_CONTEXT["mode"] = "IDLE"
    if "title" not in CURRENT_CONTEXT:
        CURRENT_CONTEXT["title"] = None
    if "data" not in CURRENT_CONTEXT:
        CURRENT_CONTEXT["data"] = None
    if "last_action" not in CURRENT_CONTEXT:
        CURRENT_CONTEXT["last_action"] = None

    CURRENT_CONTEXT["mode"] = "ANALYSIS"
    CURRENT_CONTEXT["title"] = title
    CURRENT_CONTEXT["data"] = formatted
    CURRENT_CONTEXT["last_action"] = "render_output"

    # ======================================================
    # SESSION TRACKING
    # ======================================================
    scan_session.append({
        "title": title,
        "data": formatted
    })

    # ======================================================
    # DISPLAY OUTPUT
    # ======================================================
    console.print(
        Panel(
            formatted,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="green"
        )
    )

    # ======================================================
    # FLOW CONTROL (FIXED - NON-INTERFERING NETFLOW SAFE)
    # ======================================================

    analysis_modules = {
        "SYSTEM AUDIT",
        "SYSTEM HEALTH",
        "THREAT OVERVIEW",
        "SIEM CORRELATION",
        "BRUTE FORCE DETECTION",
        "REVERSE SHELL DETECTION",
        "MITM DETECTION",
        "CVE SCANNER",
        "REMOTE INTELLIGENCE",
        "FORENSIC ENGINE",
        "FULL SOC ANALYSIS",
        "AUTONOMOUS MODE"
    }

    # ONLY SHOW OPTIONS AFTER REAL ANALYSIS MODULES
    if FLOW_ENABLED and not CURRENT_CONTEXT.get("flow_lock", False) and title not in [
        "REMOTE INTELLIGENCE",
        "HOST DISCOVERY"
    ]:
        console.print(
            Panel.fit(
                """
    [bold cyan]NEXT ACTION[/bold cyan]

    1. Continue investigation
    2. Generate report
    """,
                border_style="cyan",
                title="SOC OPTIONS"
            )
        )

        action = Prompt.ask(
            "Choose next step",
            choices=["1", "2"]
        )
        # LOCK FLOW to prevent re-entry bugs
        CURRENT_CONTEXT["flow_lock"] = True

        # ==============================
        # 1. INVESTIGATION MODE
        # ==============================
        if action == "1":
            CURRENT_CONTEXT["last_action"] = "investigation_mode"
            CURRENT_CONTEXT["flow_lock"] = False  # allow reuse later
            investigation_mode()
            return

        # ==============================
        # 2. REPORT GENERATION (FIXED)
        # ==============================
        elif action == "2":
            from ai.report_generator import save_report

            if not scan_session:
                console.print("[red]No scan data available for report.[/red]")
                CURRENT_CONTEXT["flow_lock"] = False
                return

            final_report = "\n\n".join(
                f"[{s['title']}]\n{s['data']}"
                for s in scan_session
            )

            file_path = save_report(final_report)

            console.print(
                Panel.fit(
                    f"[green]REPORT SAVED SUCCESSFULLY[/green]\n{file_path}",
                    title="REPORT ENGINE",
                    border_style="green"
                )
            )

            CURRENT_CONTEXT["last_action"] = "report_generated"
            CURRENT_CONTEXT["flow_lock"] = False
            return
# ==========================================================
# MODULE GROUPS
# ==========================================================
def analysis_engine():
    render_output("SYSTEM AUDIT", audit())
    render_output("SYSTEM HEALTH", health())

def threat_engine():
    render_output("THREAT OVERVIEW", threats())
    render_output("SIEM CORRELATION", correlate_logs())
    render_output("BRUTE FORCE DETECTION", detect_bruteforce())
    render_output("REVERSE SHELL DETECTION", detect_reverse_shell())
    render_output("MITM DETECTION", detect_mitm())
    render_output("CVE SCANNER", scan_packages())

# ==========================================================
# AI CHAT MODE
# ==========================================================
def ai_chat_mode():
    console.print(
        Panel.fit(
            "[bold cyan]AI CHAT MODE ACTIVE[/bold cyan]\nCTRL + C to exit safely",
            border_style="cyan"
        )
    )

    while True:
        try:
            q = Prompt.ask("[green]You[/green]")
            response = ask_ai(q)

            console.print(Panel(response, title="AI RESPONSE", border_style="cyan"))

            # ================= POST RESPONSE OPTIONS =================
            action = Prompt.ask(
                "\n[bold yellow]Next Action[/bold yellow]",
                choices=["continue", "menu", "clear"],
            )

            if action == "menu":
                return

            elif action == "clear":
                clear()
                banner()
                menu ()

        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting AI Mode → Dashboard[/yellow]")
            return

def remote_assessment():
    ip = Prompt.ask("Enter Target IP / Hostname / URL")

    # STEP 1: Initial discovery mode (confirmation prompt inside engine)
    CURRENT_CONTEXT["flow_lock"] = True
    result = remote_scan(ip, confirm=True)
    render_output("REMOTE INTELLIGENCE", result)
    CURRENT_CONTEXT["flow_lock"] = False

    # STEP 2: Only continue if host is reachable
    if "REACHABLE" in str(result) or "HOST DISCOVERY" in str(result):

        console.print(
            Panel.fit(
                "[bold yellow]Proceed to deep analysis?[/bold yellow]\nType YES to continue",
                border_style="yellow"
            )
        )

        choice = Prompt.ask("Proceed?", choices=["yes", "no"])

        if choice == "yes":
            result = remote_scan(ip, confirm=False)
            render_output("FULL SOC ANALYSIS", result)




def incident_toolkit():
    from datetime import datetime
    from ai.brain import ask_ai
    from tools.network_scanner import scan_target
    from ai.report_generator import save_report
    import psutil

    incident_log = []

    # ======================================================
    # STEP 1: AUTO DISCOVERY
    # ======================================================
    console.print(
        Panel.fit(
            """
[bold red]INCIDENT RESPONSE TOOLKIT - DISCOVERY MODE[/bold red]

Scanning system intelligence layer:
• Process anomalies
• Network connections
• Active sessions
""",
            border_style="red",
            title="SOC IR INITIALIZATION"
        )
    )

    # ================= PROCESS ANALYSIS =================
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = p.info['cpu_percent'] or 0
            if cpu > 15:   # lower threshold = better SOC sensitivity
                processes.append({
                    "pid": p.info['pid'],
                    "name": p.info['name'],
                    "cpu": cpu
                })
        except:
            pass

    # ================= NETWORK ANALYSIS =================
    connections = []
    for c in psutil.net_connections(kind="inet"):
        if c.raddr:
            connections.append({
                "local": c.laddr.ip if c.laddr else "-",
                "remote_ip": c.raddr.ip,
                "remote_port": c.raddr.port,
                "status": c.status,
                "pid": c.pid
            })

    incident_log.append(f"[{datetime.now()}] System discovery completed")

    # ======================================================
    # STEP 2: ORGANIZED SOC PRESENTATION
    # ======================================================

    console.print(
        Panel.fit(
            "[bold yellow]SUSPICIOUS PROCESS TABLE[/bold yellow]",
            border_style="yellow"
        )
    )

    if processes:
        for p in processes:
            console.print(f"[red]PID[/red]: {p['pid']} | [cyan]{p['name']}[/cyan] | CPU: {p['cpu']}%")
    else:
        console.print("[green]No high-risk processes detected[/green]")

    console.print(
        Panel.fit(
            "[bold cyan]ACTIVE NETWORK CONNECTIONS[/bold cyan]",
            border_style="cyan"
        )
    )

    if connections:
        for c in connections:
            console.print(
                f"[yellow]{c['remote_ip']}[/yellow]:{c['remote_port']} "
                f"→ PID {c['pid']} | Status: {c['status']}"
            )
    else:
        console.print("[green]No external connections detected[/green]")

    # ======================================================
    # STEP 3: ACTION SELECTION
    # ======================================================
    console.print(
        Panel.fit(
            """
[bold green]RESPONSE OPTIONS[/bold green]

1. Kill Suspicious Process
2. Block Remote IP
3. Full AI Investigation (Deep Forensics)
""",
            border_style="green"
        )
    )

    choice = Prompt.ask("Select Action", choices=["1", "2", "3"])

    scan_result = {}

    # ======================================================
    # 1. KILL PROCESS
    # ======================================================
    if choice == "1":
        if not processes:
            console.print("[red]No suspicious processes found[/red]")
            return

        for i, p in enumerate(processes):
            console.print(f"{i}. PID {p['pid']} | {p['name']} | CPU {p['cpu']}%")

        sel = int(Prompt.ask("Select process index"))
        target = processes[sel]

        render_output("PROCESS TERMINATION", kill_process(target["pid"]))

        incident_log.append(f"Killed process {target['pid']}")
        scan_result = target

    # ======================================================
    # 2. BLOCK IP
    # ======================================================
    elif choice == "2":
        if not connections:
            console.print("[red]No suspicious connections found[/red]")
            return

        for i, c in enumerate(connections):
            console.print(f"{i}. {c['remote_ip']}:{c['remote_port']} (PID {c['pid']})")

        sel = int(Prompt.ask("Select connection index"))
        target = connections[sel]

        render_output("NETWORK CONTAINMENT", block_ip(target["remote_ip"]))

        incident_log.append(f"Blocked IP {target['remote_ip']}")
        scan_result = target

    # ======================================================
    # 3. FULL AI INVESTIGATION (UPGRADED)
    # ======================================================
    elif choice == "3":
        scan_result = {
            "processes": processes,
            "connections": connections
        }

        render_output("FORENSIC SNAPSHOT", scan_result)

        incident_log.append("Full AI investigation initiated")

    # ======================================================
    # STEP 4: DEEP AI SOC ANALYSIS (UPGRADED)
    # ======================================================
    ai_prompt = f"""
You are a SENIOR SOC INCIDENT RESPONSE ANALYST working in a Tier-1 Security Operations Center.

You are analyzing LIVE system telemetry.

========================
SYSTEM DATA
========================

SUSPICIOUS PROCESSES:
{processes}

ACTIVE NETWORK CONNECTIONS:
{connections}

INCIDENT ACTIONS TAKEN:
{incident_log}

========================
ANALYSIS REQUIREMENTS
========================

Provide a structured SOC investigation report:

1. EXECUTIVE SUMMARY
- Is the system SAFE / SUSPECT / COMPROMISED?

2. THREAT ANALYSIS
- Identify malicious processes (if any)
- Identify suspicious network activity
- Explain behavior patterns

3. ATTACK CLASSIFICATION (if applicable)
- MITRE ATT&CK mapping (if possible)
- Type: malware / persistence / C2 / lateral movement / exfiltration

4. RISK SCORING
- Low / Medium / High / Critical
- Justification required

5. INDICATORS OF COMPROMISE (IOCs)
- IPs
- Processes
- Ports
- Behaviors

6. DEFENSIVE ACTION PLAN
- Immediate containment steps
- Hardening recommendations
- Monitoring suggestions

7. FINAL VERDICT
- CLEAN / SUSPICIOUS / COMPROMISED
"""

    ai_analysis = ask_ai(ai_prompt)

    render_output("AI INCIDENT ANALYSIS", ai_analysis)

    incident_log.append("AI analysis completed")

    # ======================================================
    # STEP 5: FINAL STRUCTURED REPORT
    # ======================================================
    full_report = f"""
=============================
KALI SOC INCIDENT REPORT
=============================

[DATE]
{datetime.now()}

[DISCOVERY SUMMARY]
Processes Found: {len(processes)}
Connections Found: {len(connections)}

[INCIDENT LOG]
{incident_log}

[RAW DATA]
Processes:
{processes}

Connections:
{connections}

=============================
AI FORENSIC ANALYSIS
=============================
{ai_analysis}
"""

    file_path = save_report(full_report)

    console.print(
        Panel.fit(
            f"""
[bold green]INCIDENT REPORT GENERATED[/bold green]

File: {file_path}

Status: ANALYSIS COMPLETE
""",
            border_style="green"
        )
    )

    CURRENT_CONTEXT["last_action"] = "incident_response"

def forensics_suite():

    from ai.malware_hunter import scan_tmp, hidden_files, malware_patterns
    from ai.persistence_checker import detect_persistence
    from ai.brain import ask_ai
    from rich.prompt import Prompt

    # ======================================================
    # HELPERS (DFIR CLEANING LAYER)
    # ======================================================
    def filter_evidence(data):
        noise_keywords = [
            "windows\\system32",
            "microsoft",
            "onedrive",
            "chrome.exe",
            "chrome_proxy.exe",
            "securityhealth",
            "driverstore",
            "rtkauduservice",
            "program files",
            "orbita-browser",
            "gologin",
            "notification_helper",
            "chrome_pwa_launcher"
        ]

        cleaned = []
        for line in str(data).split("\n"):
            if not any(n.lower() in line.lower() for n in noise_keywords):
                cleaned.append(line)

        return "\n".join(cleaned)

    def trim(data, limit=1200):
        return str(data)[:limit]

    # ======================================================
    # STEP 1: OFFLINE DFIR COLLECTION
    # ======================================================
    print("\n[FORENSIC ENGINE] Running offline DFIR scan...\n")

    persistence = detect_persistence()
    artifacts = malware_patterns()
    temp_files = scan_tmp()
    hidden = hidden_files()

    # ======================================================
    # CLEAN + FILTER EVIDENCE
    # ======================================================
    persistence_clean = trim(filter_evidence(persistence))
    artifacts_clean = trim(filter_evidence(artifacts))
    temp_clean = trim(filter_evidence(temp_files))
    hidden_clean = trim(filter_evidence(hidden))

    # ======================================================
    # OFFLINE REPORT (NO AI)
    # ======================================================
    offline_report = f"""
[OFFLINE FORENSIC SNAPSHOT]

[PERSISTENCE]
{persistence_clean}

[MALWARE PATTERNS]
{artifacts_clean}

[TEMP ARTIFACTS]
{temp_clean}

[HIDDEN FILES]
{hidden_clean}
"""

    print("\n" + offline_report)

    # ======================================================
    # STEP 2: USER CONFIRMATION
    # ======================================================
    choice = Prompt.ask(
        "Continue with AI deep forensic analysis?",
        choices=["yes", "no"],
    )

    if choice == "no":
        print("\nFORENSICS STOPPED - Offline analysis complete.")
        return

    # ======================================================
    # STEP 3: AI DFIR ANALYSIS (CLEAN INPUT ONLY)
    # ======================================================
    prompt = f"""
You are a senior DFIR + SOC forensic analyst.

You are performing INCIDENT RECONSTRUCTION based ONLY on validated evidence.

--------------------------------------------------
CLEAN FORENSIC EVIDENCE
--------------------------------------------------

[PERSISTENCE]
{persistence_clean}

[MALWARE PATTERNS]
{artifacts_clean}

[TEMP FILES]
{temp_clean}

[HIDDEN FILES]
{hidden_clean}

--------------------------------------------------
STRICT RULES
--------------------------------------------------
- Ignore system/vendor software
- Do NOT flag Chrome, OneDrive, Windows components
- Do NOT assume malware without execution evidence
- Focus ONLY on anomalies and suspicious behavior
- No speculation without supporting indicators

--------------------------------------------------
TASKS
--------------------------------------------------
1. Identify real intrusion indicators
2. Detect malware staging behavior
3. Validate persistence mechanisms (must be executable-backed)
4. Reconstruct attack timeline if possible
5. Determine compromise likelihood
6. Remove false positives
7. Provide defensive actions

--------------------------------------------------
OUTPUT FORMAT:

[FORENSIC SUMMARY]
[ATTACK TIMELINE]
[PERSISTENCE ANALYSIS]
[MALWARE INDICATORS]
[RISK LEVEL]
[RECOMMENDATIONS]
"""

    try:
        result = ask_ai(prompt, mode="forensics")
        print("\n[AI FORENSIC RECONSTRUCTION]\n")
        print(result)

    except Exception as e:
        print(f"\nAI FORENSIC ENGINE ERROR:\n{e}")

def system_admin():
    render_output("FIREWALL STATUS", firewall_status())
    render_output("DISK USAGE", disk_usage())
    render_output("SUDO USERS", sudo_users())
    render_output("LAST LOGINS", last_logins())
    render_output("ACTIVE USERS", logged_users())


def reporting():
    from ai.report_generator import save_report

    render_output("REPORT ENGINE", "Generating SOC report...")

    if not scan_session:
        render_output("REPORT ENGINE", "No scan session data available.")
        return

    # Build full SOC report
    final_report = "\n\n".join(
        f"[{item['title']}]\n{item['data']}"
        for item in scan_session
    )

    file_path = save_report(final_report)

    render_output("REPORT GENERATED", f"Saved at: {file_path}")




    render_output("MEMORY STORED", "Saved successfully")
    render_output("REPORT GENERATED", save_report(last_output))


# ==========================================================
# MENU
# ==========================================================
def menu():
    table = Table(
        title="SOC CONTROL CENTER",
        box=box.DOUBLE_EDGE,
        border_style="cyan"
    )

    table.add_column("ID", justify="center", style="green")
    table.add_column("AI MODULE", style="white")
    table.add_column("DESCRIPTION", style="cyan")

    table.add_row("0", "Help Center", "SOC documentation & guide")
    table.add_row("1", "Security Analysis Suite", "Audit + Health + Overview")
    table.add_row("2", "Threat Intelligence Engine", "SIEM + Malware + CVEs")
    table.add_row("3", "Incident Response Toolkit", "Block IP + Kill Process")
    table.add_row("4", "Forensics Suite", "Malware + persistence analysis")
    table.add_row("5", "System Administration", "Users + Disk + Firewall")
    table.add_row("6", "SOC AI Assistant", "Chat with AI analyst")
    table.add_row("7", "Reporting Engine", "Memory + export reports")
    table.add_row("8", "Maintenance Mode", "System health monitoring & safe recovery recommendations")
    table.add_row("9", "Clear Workspace", "Clean screen")
    table.add_row("10", "Remote Device Scan", "Ping → Confirm → Full scan")
    table.add_row("0X", "Voice Assistant", "Speech interaction")
    table.add_row("EXIT", "Shutdown", "Exit system safely")

    console.print(table)
# ==========================================================
# MAIN LOOP (PERSISTENT SOC MODE)
# ==========================================================
# Draw UI ONLY ONCE
clear()
banner()
menu()
status_bar()

while True:
    try:

        choice = Prompt.ask("\nSelect Module")

        if choice == "0":
            help_center()

        elif choice == "1":
            analysis_engine()

        elif choice == "2":
            threat_engine()

        elif choice == "3":
            incident_toolkit()

        elif choice == "4":
            forensics_suite()

        elif choice == "5":
            system_admin()

        elif choice == "6":
            ai_chat_mode()

        elif choice == "7":
            reporting()

        elif choice == "8":
            result = auto_heal()
            render_output(
                "AUTONOMOUS MODE",
                format_autonomous_report(result)
            )

        elif choice == "9":
            clear()
            banner()
            menu()
            status_bar()

        elif choice == "10":
            remote_assessment()

        elif choice.upper() == "0X":
            voice_mode()



        elif choice.upper() == "EXIT":
            SYSTEM_ACTIVE = False
            render_output("SHUTDOWN", "KALI SOC AI shutting down...")
            break

        else:
            console.print("[red]Invalid Option[/red]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted → returning to dashboard[/yellow]")