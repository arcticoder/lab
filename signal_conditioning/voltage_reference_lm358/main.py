"""
voltage_reference_lm358/main.py
--------------------------------
Pico ADC probe implementing README.md's "Validation without a
multimeter" check: read the LM358 buffered reference (pin 1) with and
without R_load (a separate 1kOhm resistor, not R1/R2 from the divider)
connected, and confirm the reading barely moves.

Hardware
--------
  GP26 (ADC0) — probe lead, on LM358 pin 1 (buffered reference output)
  GND         — probe lead, shared with the LM358's own GND (pin 4)
  GP15        — push button, other leg to GND, internal pull-up (ready signal)

Each phase waits on the push button instead of a keypress or a fixed
countdown: `mpremote run` executes this script over the raw REPL
protocol, which streams device output back but never forwards your
terminal's keystrokes to the device, so a blocking input() call here
would hang forever (confirmed — see docs/kb/repo_docs_conventions.md's
"mpremote run cannot forward host keystrokes" entry). Don't reintroduce
input() in a script meant to run this way. A GPIO read isn't a keystroke,
though, so a physical push button gives you an unbounded, no-guesswork
"I'm ready" signal instead of a hardcoded timeout you have to pad out by
trial and error (this one started at 10s and had to be bumped to 13s
after a too-fast unplug/replug touched the leads together).

Run from MicroPico (or rshell / mpremote), Pico connected to the PC by USB:
  mpremote run main.py
"""

from machine import ADC, Pin
import time

ADC_PROBE = ADC(Pin(26))  # GP26 / ADC0, on LM358 pin 1
BUTTON = Pin(15, Pin.IN, Pin.PULL_UP)  # GP15, other leg to GND; pressed = 0

ADC_MAX = 65535  # 16-bit ADC full scale
VREF = 3.3  # Pico ADC reference voltage
SAMPLES = 20  # averaged per reading, to smooth ADC noise
SAMPLE_INTERVAL_S = 0.05
TOLERANCE = 0.02  # matches smoke_test.py's buffered-vs-unloaded tolerance
POLL_INTERVAL_S = 0.05
DEBOUNCE_S = 0.05


def raw_to_voltage(raw: int) -> float:
    """Convert 16-bit ADC reading to voltage."""
    return raw * VREF / ADC_MAX


def stable_reading() -> float:
    """Average several samples into one steady reading."""
    total = 0.0
    for _ in range(SAMPLES):
        total += raw_to_voltage(ADC_PROBE.read_u16())
        time.sleep(SAMPLE_INTERVAL_S)
    return total / SAMPLES


def wait_for_button() -> None:
    """Block until the button is pressed and released, however long that takes."""
    while BUTTON.value() == 1:
        time.sleep(POLL_INTERVAL_S)
    time.sleep(DEBOUNCE_S)
    while BUTTON.value() == 0:
        time.sleep(POLL_INTERVAL_S)


def main() -> None:
    print("voltage_reference_lm358 validation — probing GP26 (LM358 pin 1)")
    print()

    print("Disconnect R_load (1kOhm) from pin 1, then press the button (GP15):")
    wait_for_button()
    v_unloaded = stable_reading()
    print(f"unloaded: {v_unloaded:.3f}V")
    print()

    print("Now connect R_load (1kOhm) between pin 1 and GND, then press the button:")
    wait_for_button()
    v_loaded = stable_reading()
    print(f"loaded:   {v_loaded:.3f}V")
    print()

    delta = abs(v_loaded - v_unloaded) / v_unloaded
    status = "PASS" if delta < TOLERANCE else "FAIL"
    print(
        f"[{status}] loaded reading within {TOLERANCE * 100:.0f}% of unloaded "
        f"(actual change: {delta * 100:.2f}%)"
    )
    if status == "FAIL":
        print(
            "Check the feedback wire (pin 1 -> pin 2) and LM358 power "
            "(pin 8 VCC / pin 4 GND)."
        )


if __name__ == "__main__":
    main()
