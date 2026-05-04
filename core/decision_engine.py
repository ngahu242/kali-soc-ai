# core/decision_engine.py

from ai.brain import ask_ai


def decide(issue_report):
    """
    SOC AI Decision Engine
    Determines safe response actions based on system issues
    """

    prompt = f"""
You are a SOC autonomous decision engine.

Analyze the following system issue and decide:

1. Severity (Low / Medium / High / Critical)
2. Is auto-fix safe? (Yes/No)
3. Recommended action
4. Should escalate to human analyst?

ISSUE REPORT:
{issue_report}
"""

    return ask_ai(prompt)