DISABLED = set()
FAILED_MODULES = {}
SYSTEM_STATUS = "HEALTHY"


def disable(module, reason):
    DISABLED.add(module)
    FAILED_MODULES[module] = reason


def is_disabled(module):
    return module in DISABLED