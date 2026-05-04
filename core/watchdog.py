import importlib
from core.logger import log
from core.registry import disable


REQUIRED_MODULES = [
    "ai.brain",
    "ai.soc_engine",
    "ai.threat_detector",
    "ai.system_audit"
]


def health_scan():
    results = {}

    for mod in REQUIRED_MODULES:
        try:
            importlib.import_module(mod)
            results[mod] = "OK"

        except Exception as e:
            disable(mod, str(e))
            log(f"Module failure: {mod} -> {e}", "ERROR")
            results[mod] = "FAILED"

    return results