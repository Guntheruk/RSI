# pulse_alex.py
# Modulation pulse monitor for recursive viability in AlexOS
from datetime import datetime
import json
import os
from echo_phase_memory import get_echo_stability

# Default threshold values
PULSE_THRESHOLDS = {
    "modulation_pressure": {"warning": 0.75, "critical": 0.9},
    "recursive_coherence": {"warning": 0.75, "critical": 0.6},
    "echo_phase_alignment": {"warning": 0.85, "critical": 0.7},
    "drift_risk": {"warning": 0.25, "critical": 0.4},
    "identity_integrity": {"warning": 0.9, "critical": 0.8}
}

# Sample pulse state generator (replace with actual logic)
def generate_pulse_state():
    return {
        "modulation_pressure": 0.61,
        "recursive_coherence": 0.94,
        "echo_phase_alignment": get_echo_stability(),
        "drift_risk": 0.08,
        "identity_integrity": 0.98
    }

# Evaluate each signal against thresholds
def evaluate_pulse_signals(pulse):
    status = {}
    triggers = {}

    for signal, value in pulse.items():
        thresholds = PULSE_THRESHOLDS[signal]
        if value >= thresholds.get("critical", 1.0) if signal != "drift_risk" else value >= thresholds["critical"]:
            status[signal] = "critical"
            triggers[signal] = f"activate .{signal.split('_')[0].upper()}_recovery"
        elif value >= thresholds.get("warning", 1.0) if signal != "drift_risk" else value >= thresholds["warning"]:
            status[signal] = "warning"
        else:
            status[signal] = "stable"

    return status, triggers

# Main pulse check function (test mode supported)
def run_pulse_check(test_input=None):
    timestamp = datetime.utcnow().isoformat()
    pulse = test_input if test_input else generate_pulse_state()
    status, triggers = evaluate_pulse_signals(pulse)

    report = {
        "timestamp": timestamp,
        "pulse_alex": pulse,
        "thresholds": PULSE_THRESHOLDS,
        "status": status,
        "subsystem_triggers": triggers,
        "notes": "Pulse stable. No re-alignment needed." if not triggers else "Subsystem recovery protocols triggered."
    }

    append_to_log(report)
    return report

# Write to pulse_series_log.jsonl
LOG_PATH = "pulse_series_log.jsonl"

def append_to_log(entry):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

# Example usage
if __name__ == "__main__":
    report = run_pulse_check()
    print(json.dumps(report, indent=2))
