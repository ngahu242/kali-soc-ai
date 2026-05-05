# ==========================================================
# FILE: ai/incident_response.py
# ENTERPRISE INCIDENT RESPONSE ENGINE (SOC LEVEL)
# ==========================================================

from datetime import datetime
import psutil

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from ai.brain import ask_ai
from ai.report_generator import save_report
from tools.network_scanner import scan_target

console = Console()


# ==========================================================
# CORE ACTIONS (SAFE WRAPPERS)
# ==========================================================
def block_ip(ip):
    import os
    return os.system(f"iptables -A INPUT -s {ip} -j DROP")


def kill_process(pid):
    try:
        p = psutil.Process(int(pid))
        p.kill()
        return f"Process {pid} terminated"
    except Exception as e:
        return f"Failed to kill process: {e}"


# ==========================================================
# INCIDENT RESPONSE TOOLKIT
# ==========================================================
def incident_toolkit(render_output=None):
    incident_log = []

    # ======================================================
    # STEP 1: DISCOVERY
    # ======================================================
    console.print(
        Panel.fit(
            """
[bold red]INCIDENT RESPONSE - DISCOVERY[/bold red]

Scanning:
• Processes
• Network connections
• Active sessions
""",
            border_style="red",
            title="SOC IR ENGINE"
        )
    )

    # ------------------ PROCESS SCAN ------------------
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            cpu = p.info['cpu_percent'] or 0
            if cpu > 10:
                processes.append(p.info)
        except:
            pass

    # ------------------ NETWORK SCAN ------------------
    connections = []
    for c in psutil.net_connections(kind="inet"):
        if c.raddr:
            connections.append({
                "ip": c.raddr.ip,
                "port": c.raddr.port,
                "pid": c.pid,
                "status": c.status
            })

    incident_log.append(f"[{datetime.now()}] Discovery completed")

    # ======================================================
    # STEP 2: ORGANIZED DISPLAY
    # ======================================================

    # -------- PROCESS TABLE --------
    table = Table(title="Suspicious Processes", border_style="red")
    table.add_column("Index")
    table.add_column("PID")
    table.add_column("Name")
    table.add_column("CPU %")

    for i, p in enumerate(processes):
        table.add_row(str(i), str(p['pid']), str(p['name']), str(p['cpu_percent']))

    console.print(table)

    # -------- CONNECTION TABLE --------
    table = Table(title="Active External Connections", border_style="cyan")
    table.add_column("Index")
    table.add_column("Remote IP")
    table.add_column("Port")
    table.add_column("PID")
    table.add_column("Status")

    for i, c in enumerate(connections):
        table.add_row(
            str(i),
            c["ip"],
            str(c["port"]),
            str(c["pid"]),
            c["status"]
        )

    console.print(table)

    # ======================================================
    # STEP 3: RESPONSE MENU
    # ======================================================
    console.print(
        Panel.fit(
            """
[bold green]RESPONSE OPTIONS[/bold green]

1. Kill Process
2. Block IP
3. Deep AI Investigation
4. Full Containment (Auto)
""",
            border_style="green"
        )
    )

    choice = Prompt.ask("Select action", choices=["1", "2", "3", "4"])

    selected_data = ""

    # ======================================================
    # ACTION 1: KILL PROCESS
    # ======================================================
    if choice == "1":
        idx = int(Prompt.ask("Select process index"))
        target = processes[idx]

        result = kill_process(target["pid"])
        console.print(f"[red]{result}[/red]")

        incident_log.append(f"Killed PID {target['pid']}")
        selected_data = str(target)

    # ======================================================
    # ACTION 2: BLOCK IP
    # ======================================================
    elif choice == "2":
        idx = int(Prompt.ask("Select connection index"))
        target = connections[idx]

        result = block_ip(target["ip"])
        console.print(f"[red]Blocked {target['ip']}[/red]")

        incident_log.append(f"Blocked IP {target['ip']}")
        selected_data = str(target)

    # ======================================================
    # ACTION 3: AI INVESTIGATION
    # ======================================================
    elif choice == "3":
        selected_data = f"""
PROCESSES:
{processes}

CONNECTIONS:
{connections}
"""

    # ======================================================
    # ACTION 4: FULL AUTO RESPONSE
    # ======================================================
    elif choice == "4":
        for c in connections[:3]:
            block_ip(c["ip"])
            incident_log.append(f"Auto-blocked {c['ip']}")

        for p in processes[:3]:
            kill_process(p["pid"])
            incident_log.append(f"Auto-killed {p['pid']}")

        selected_data = "Automatic containment executed"

    # ======================================================
    # STEP 4: AI ANALYSIS (CORE UPGRADE)
    # ======================================================
    console.print("\n[bold cyan]Running AI Incident Analysis...[/bold cyan]\n")

    analysis = ask_ai(f"""
You are a senior SOC Incident Responder.

Analyze this incident:

{selected_data}

Return:

[INCIDENT SUMMARY]
[ATTACK TYPE]
[RISK LEVEL]
[AFFECTED COMPONENTS]
[RECOMMENDED ACTIONS]
[CONTAINMENT STRATEGY]
""", mode="incident")

    console.print(
        Panel(analysis, title="AI INCIDENT REPORT", border_style="red")
    )

    incident_log.append("AI analysis completed")

    # ======================================================
    # STEP 5: REPORT GENERATION
    # ======================================================
    report = "\n".join(incident_log) + "\n\n" + analysis

    file_path = save_report(report)

    console.print(
        Panel.fit(
            f"""
[bold green]INCIDENT REPORT GENERATED[/bold green]

File: {file_path}
""",
            border_style="green"
        )
    )