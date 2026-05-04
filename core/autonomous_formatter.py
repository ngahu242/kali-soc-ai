# ==========================================================
# FILE: core/autonomous_formatter.py
# AUTONOMOUS SOC REPORT FORMATTER
# Presentation Layer Only
# ==========================================================

def format_autonomous_report(report):

    if not isinstance(report, dict):
        return "Invalid autonomous report format."

    summary = report.get("summary", {})

    status = report.get("status", "UNKNOWN")
    state = summary.get("state", "UNKNOWN")
    critical = summary.get("critical", 0)

    ai_decision = report.get("ai_decision", "No AI decision available.")
    issues = report.get("issues_found", "No issues detected.")
    fixes = report.get("fix_plan", [])

    # Convert fixes list into readable format
    if isinstance(fixes, list):
        fixes_text = "\n".join(
            f"- {item.get('module', 'unknown')} → {item.get('action', 'no action')}"
            for item in fixes
        ) if fixes else "No remediation required."
    else:
        fixes_text = str(fixes)

    return f"""
╭────────────── 🤖 AUTONOMOUS SOC ENGINE ──────────────╮

🟢 STATUS: {status}

📊 SYSTEM STATE: {state}

🚨 CRITICAL ISSUES: {critical}

──────────────────────────────────────────────

🧠 AI DECISION:
{ai_decision}

──────────────────────────────────────────────

🔍 ISSUES DETECTED:
{issues}

──────────────────────────────────────────────

🛠 FIX PLAN:
{fixes_text}

──────────────────────────────────────────────
"""