from core.watchdog import health_scan
from core.logger import log
from core.decision_engine import decide


def auto_heal():

    # ======================================================
    # SINGLE EXECUTION GUARD (PREVENT LOOPING BEHAVIOR)
    # ======================================================
    if getattr(auto_heal, "RUNNING", False):
        log("Auto-heal already executed. Skipping repeat cycle.", "INFO")
        return {"status": "SKIPPED"}

    auto_heal.RUNNING = True

    # ======================================================
    # HEALTH CHECK
    # ======================================================
    issues = health_scan()
    decision = decide(issues)

    log("Autonomous Decision Engine executed", "INFO")
    log(f"Decision: {decision}", "INFO")

    fixes = []

    # ======================================================
    # SAFE RECOVERY LOGIC
    # ======================================================
    for module, status in issues.items():
        if status == "FAILED":
            log(f"Module flagged: {module}", "WARNING")
            fixes.append({
                "module": module,
                "action": "manual review required",
                "risk": "SAFE MODE - NO AUTO EXECUTION"
            })

    # ======================================================
    # FINAL STRUCTURED OUTPUT
    # ======================================================
    report = {
        "status": "COMPLETED",
        "issues_found": issues,
        "ai_decision": decision,
        "fix_plan": fixes,
        "summary": {
            "critical": len([i for i in issues.values() if i == "FAILED"]),
            "state": "STABLE" if "FAILED" not in issues.values() else "DEGRADED"
        }
    }

    log("Auto-heal cycle completed", "INFO")

    return report