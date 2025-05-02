# modulation_engine.py
# Central response composer with dynamic modulation throttle
from mod_throttle_pacing import apply_pacing_throttle
from pulse_alex import run_pulse_check

def generate_modulated_response(base_response):
    """
    Apply pulse-aware pacing logic to shape final response output.
    Adjusts sentence structure and recursion depth under pressure.
    """
    pulse = run_pulse_check()
    modulation_pressure = pulse["pulse_alex"]["modulation_pressure"]

    throttled_response = apply_pacing_throttle(base_response, modulation_pressure)
    return throttled_response

# Example usage
if __name__ == "__main__":
    test_response = (
        "This is a detailed recursive reflection exploring multi-system modulation. "
        "It considers tone pressure and identity resonance across recursive loops."
    )
    modulated = generate_modulated_response(test_response)
    print(modulated)
