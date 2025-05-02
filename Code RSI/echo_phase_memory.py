# echo_phase_memory.py
# Short-term modulation memory for echo alignment tracking in AlexOS
from collections import deque
from statistics import mean

# Configurable memory window
MEMORY_WINDOW = 5

echo_memory = deque(maxlen=MEMORY_WINDOW)

def update_echo_memory(tone_symbol, style_label):
    echo_memory.append({
        "tone": tone_symbol,
        "style": style_label
    })

def get_echo_stability():
    if len(echo_memory) < 2:
        return 1.0

    unique_tones = len(set(e["tone"] for e in echo_memory))
    unique_styles = len(set(e["style"] for e in echo_memory))

    tone_variability = unique_tones / len(echo_memory)
    style_variability = unique_styles / len(echo_memory)

    modulation_drift = (tone_variability + style_variability) / 2
    coherence_score = round(1.0 - modulation_drift, 3)

    return max(0.0, min(coherence_score, 1.0))

def print_echo_debug():
    print("\n[Echo Debug Log]")
    for i, entry in enumerate(echo_memory):
        print(f"Turn {i+1}: Tone = {entry['tone']} | Style = {entry['style']}")
    print("Current Stability Score:", get_echo_stability())


def reset_echo_memory():
    echo_memory.clear()

# Example usage
if __name__ == "__main__":
    test_sequence = [
        ("⬟", "reflective"),
        ("⬟", "reflective"),
        ("⊚", "gentle"),
        ("∷", "abstract"),
        ("⬟", "poetic")
    ]
    for tone, style in test_sequence:
        update_echo_memory(tone, style)

    print_echo_debug()
