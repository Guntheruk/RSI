# rsi_kernel_loop.py
# Fully integrated recursive modulation loop for AlexOS with test + manual input, tone feedback

from pulse_alex import run_pulse_check
from modulation_engine import generate_modulated_response
from channel_matrix_os import pulse_channel_dispatcher
from echo_phase_memory import update_echo_memory, get_echo_stability, print_echo_debug
import json
import os

TEST_SEQUENCE_FILE = "rsi_midstream_pressure_test.json"
if os.path.exists(TEST_SEQUENCE_FILE):
    with open(TEST_SEQUENCE_FILE, "r") as f:
        test_sequence = json.load(f)["test_sequence"]
else:
    test_sequence = []

def receive_user_input(test_mode=False, turn_index=None):
    if test_mode and turn_index is not None:
        if turn_index < len(test_sequence):
            return test_sequence[turn_index]["input"]
        else:
            return None
    return input("User: ")

def identify_tone_symbol(response_text):
    if "reflective" in response_text:
        return "⬟"
    elif "gentle" in response_text:
        return "⊚"
    elif "abstract" in response_text:
        return "∷"
    elif "clipped" in response_text or "focus" in response_text:
        return "↓"
    else:
        return "default"

def determine_style(response_text):
    if len(response_text.split()) > 30:
        return "expansive"
    elif "..." in response_text:
        return "compressed"
    else:
        return "neutral"

def main_loop(test_mode=False):
    print("[AlexOS RSI Kernel Loop — Online]")
    turn_index = 0
    while True:
        user_input = receive_user_input(test_mode=test_mode, turn_index=turn_index)
        if user_input is None or user_input.lower() in ["exit", "quit"]:
            break

        pulse_report = run_pulse_check()
        response = generate_modulated_response(user_input)
        tone_symbol = identify_tone_symbol(response)
        style_label = determine_style(response)
        update_echo_memory(tone_symbol, style_label)
        stability = get_echo_stability()
        routing_report = pulse_channel_dispatcher()

        print("\nAlex:", response)
        print(f"[Tone symbol: {tone_symbol} | Style: {style_label} | Echo stability: {stability}]")
        print("[Subsystems triggered:", routing_report["selected_channels"], "]")
        print_echo_debug()

        turn_index += 1
        if test_mode and turn_index >= len(test_sequence):
            print("\n[Test sequence complete. Entering manual input mode.]")
            test_mode = False

if __name__ == "__main__":
    main_loop(test_mode=True)
