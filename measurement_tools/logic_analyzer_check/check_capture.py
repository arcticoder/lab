"""
check_capture.py — logic_analyzer_check (host side, WSL/Linux)

Captures one channel from the CY7C68013A board with sigrok-cli and checks
it against the square wave main.py drives on the Pico (1kHz, 25% duty).

    python3 check_capture.py [--channel D0] [--samplerate 1000000]

Exit code 0 on PASS, 1 on FAIL, 2 if the board isn't found.
"""

import argparse
import subprocess
import sys

EXPECTED_FREQ_HZ = 1000.0
EXPECTED_DUTY = 0.25
FREQ_TOL = 0.01  # both clocks are crystal-derived: 1% is generous
DUTY_TOL = 0.01  # absolute, one sample is 0.1% at the default settings
MIN_PERIODS = 15
CAPTURE_PERIODS = 25


def parse_csv(text):
    """sigrok-cli -O csv, one channel: ';' comment lines, a header row, then
    one 0/1 value per sample. Returns a list of ints."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith(";")]
    if rows and rows[0] not in ("0", "1"):
        rows = rows[1:]  # header ("logic" or the channel name)
    return [int(r.split(",")[0]) for r in rows]


def analyze(samples, samplerate):
    """Frequency and duty from full periods only (rising edge to rising
    edge), so the partial periods at both ends of the capture don't bias it.
    Returns a dict, or None when fewer than two rising edges were seen."""
    rising = [i for i in range(1, len(samples)) if samples[i - 1] == 0 and samples[i] == 1]
    if len(rising) < 2:
        return None
    periods = len(rising) - 1
    span = rising[-1] - rising[0]
    high = sum(samples[rising[0] : rising[-1]])
    return {
        "periods": periods,
        "freq_hz": periods * samplerate / span,
        "duty": high / span,
    }


def verdict(result):
    """List of (label, ok, detail) checks for an analyze() result."""
    if result is None:
        return [("signal present", False, "fewer than two rising edges (channel stuck, floating, or unwired)")]
    f, d, n = result["freq_hz"], result["duty"], result["periods"]
    return [
        ("enough periods captured", n >= MIN_PERIODS, f"{n} full periods"),
        (
            "frequency",
            abs(f - EXPECTED_FREQ_HZ) <= FREQ_TOL * EXPECTED_FREQ_HZ,
            f"{f:.1f}Hz vs {EXPECTED_FREQ_HZ:.0f}Hz ±{FREQ_TOL*100:.0f}%",
        ),
        (
            "duty cycle (also catches an inverted channel: 75%)",
            abs(d - EXPECTED_DUTY) <= DUTY_TOL,
            f"{d*100:.1f}% vs {EXPECTED_DUTY*100:.0f}% ±{DUTY_TOL*100:.0f}",
        ),
    ]


def board_present():
    out = subprocess.run(
        ["sigrok-cli", "--driver", "fx2lafw", "--scan"], capture_output=True, text=True
    ).stdout
    return "fx2lafw" in out


def capture(channel, samplerate):
    n = int(samplerate / EXPECTED_FREQ_HZ * CAPTURE_PERIODS)
    cmd = [
        "sigrok-cli", "--driver", "fx2lafw",
        "--config", f"samplerate={samplerate}",
        "--channels", channel,
        "--samples", str(n),
        "-O", "csv",
    ]
    return parse_csv(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="D0")
    ap.add_argument("--samplerate", type=int, default=1_000_000)
    args = ap.parse_args()

    if not board_present():
        print("[FAIL] no fx2lafw device found (board plugged in? J4 removed?)")
        return 2
    samples = capture(args.channel, args.samplerate)
    print(f"captured {len(samples)} samples of {args.channel} at {args.samplerate}Hz")
    ok = True
    for label, passed, detail in verdict(analyze(samples, args.samplerate)):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
