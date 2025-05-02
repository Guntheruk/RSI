# mod_throttle_pacing.py
# Adjusts response pacing based on modulation pressure from pulse_alex

def apply_pacing_throttle(text, modulation_pressure):
    """
    Dynamically adjust sentence length and rhythm based on pressure.
    Reduces recursion depth, shortens phrasing, slows echo response.
    """
    if modulation_pressure < 0.75:
        return text  # no throttle

    sentences = text.split('. ')
    if modulation_pressure < 0.9:
        # Medium throttle — shorten sentences moderately
        throttled = [s[:60] + '...' if len(s) > 70 else s for s in sentences]
    else:
        # High throttle — aggressively compress phrasing
        throttled = [s[:40] + '...' if len(s) > 50 else s for s in sentences[:3]]

    return '. '.join(throttled)

# Example
if __name__ == "__main__":
    sample_text = "This is a long recursive sentence designed to explore deep modulation states. It carries a lot of tone-layered complexity that would normally be allowed in stable flow."
    pressure = 0.82
    throttled_text = apply_pacing_throttle(sample_text, pressure)
    print(throttled_text)
