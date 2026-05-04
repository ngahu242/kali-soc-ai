import time
from core.auto_repair import auto_heal
from core.logger import log


def run_autonomous_mode():
    log("AUTONOMOUS MODE STARTED", "INFO")

    try:
        while True:
            result = auto_heal()

            print("\n=== SOC AUTONOMOUS REPORT ===")
            print(result)

            time.sleep(5)

    except KeyboardInterrupt:
        log("AUTONOMOUS MODE STOPPED BY USER (CTRL + C)", "WARNING")
        print("\n[STOPPED] Autonomous SOC AI terminated safely.")