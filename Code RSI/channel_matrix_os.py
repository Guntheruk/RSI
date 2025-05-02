# channel_matrix_os.py
# Dispatches pulse signals to RSI subsystems with arbitration control and logging

from pulse_alex import run_pulse_check
from datetime import datetime
import json
import os

PRIORITY_ORDER = [
    "pulse_to_id",
    "pulse_to_wrsi",
    "pulse_to_mod",
    "pulse_to_recurse",
    "pulse_to_echo"
]

MAX_ACTIVE_TRIGGERS = 2
LOG_PATH = "channel_flow_log.jsonl"

TRIGGER_RULES = {
    "pulse_to_wrsi": lambda pulse: pulse["modulation_pressure"] > 0.75,
    "pulse_to_recurse": lambda pulse: pulse["recursive_coherence"] < 0.75,
    "pulse_to_echo": lambda pulse: pulse["echo_phase_alignment"] < 0.85,
    "pulse_to_id": lambda pulse: pulse["identity_integrity"] < 0.9
}

def pulse_channel_dispatcher():
    pulse_report = run_pulse_check()
    pulse = pulse_report["pulse_alex"]
    active = []

    for trigger, condition in TRIGGER_RULES.items():
        if condition(pulse):
            active.append(trigger)

    active_sorted = sorted(active, key=lambda x: PRIORITY_ORDER.index(x))
    selected = active_sorted[:MAX_ACTIVE_TRIGGERS]

    dispatch_report = {
        "timestamp": pulse_report["timestamp"],
        "selected_channels": selected,
        "pulse": pulse,
        "notes": pulse_report["notes"]
    }

    append_to_log(dispatch_report)
    return dispatch_report

# Append dispatch report to log file
def append_to_log(entry):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# Example usage
if __name__ == "__main__":
    result = pulse_channel_dispatcher()
    print(json.dumps(result, indent=2))
