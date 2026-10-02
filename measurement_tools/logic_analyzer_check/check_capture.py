"""
check_capture.py — logic_analyzer_check (host side, WSL/Linux)

Captures one channel from the CY7C68013A board with sigrok-cli and checks
it against the square wave main.py drives on the Pico (1kHz, 25% duty).

    python3 check_capture.py [--channel D0] [--samplerate 1000000]

Exit code 0 on PASS, 1 on FAIL, 2 if the board isn't found or sigrok-cli
can't open/capture from it (the reason is printed).

    python3 check_capture.py --find-channel

captures all 16 channels and reports which ones toggle: run it with the
signal wire on a header pad to learn which `Dn` that pad is.
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


class CaptureError(Exception):
    pass


def explain_failure(stderr):
    """Plain-language cause for a failed sigrok-cli run, from its stderr."""
    err = stderr.lower()
    if "failed to renumerate" in err or "failed to open device" in err or "no devices found" in err:
        return (
            "the board didn't come back after sigrok loaded its firmware. Under WSL this is "
            "usbipd: the reconnected board is a new, unshared device. In an administrator "
            "PowerShell: `usbipd bind --busid <id>` (id from `usbipd list`; the board shows as "
            "'fx2lafw' once the firmware is loaded), then "
            "`usbipd attach --wsl --busid <id> --auto-attach`. See breadboard.md."
        )
    if "access" in err or "permission" in err:
        return "USB permission denied: check the sigrok udev rules and that your user is in plugdev"
    return "unrecognised sigrok-cli failure; its stderr is above"


def run_sigrok(args):
    r = subprocess.run(["sigrok-cli", "--driver", "fx2lafw", *args], capture_output=True, text=True)
    if r.returncode != 0:
        msg = r.stderr.strip() or "(no stderr)"
        raise CaptureError(f"sigrok-cli exit {r.returncode}: {msg}\n  -> {explain_failure(r.stderr)}")
    return r.stdout


def capture(channel, samplerate):
    n = int(samplerate / EXPECTED_FREQ_HZ * CAPTURE_PERIODS)
    out = run_sigrok([
        "--config", f"samplerate={samplerate}",
        "--channels", channel,
        "--samples", str(n),
        "-O", "csv",
    ])
    return parse_csv(out)


def parse_csv_columns(text):
    """Multi-channel sigrok csv -> {channel_name: [0/1, ...]}. sigrok writes
    'logic' for every header cell; the real names are in the
    '; Channels (n/m): D0, D1, ...' comment line, in column order."""
    names = None
    rows = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln.startswith("; Channels"):
            names = [n.strip() for n in ln.split(":", 1)[1].split(",")]
        elif ln and not ln.startswith(";"):
            rows.append(ln)
    rows = rows[1:]  # the 'logic,logic,...' header
    names = names or [f"D{i}" for i in range(len(rows[0].split(",")))]
    cols = {n: [] for n in names}
    for row in rows:
        for n, v in zip(names, row.split(",")):
            cols[n].append(int(v))
    return cols


def toggling_channels(cols):
    """Channels with at least two rising edges."""
    return [n for n, s in cols.items() if sum(1 for i in range(1, len(s)) if s[i - 1] == 0 and s[i] == 1) >= 2]


def find_channel(samplerate):
    n = int(samplerate / EXPECTED_FREQ_HZ * CAPTURE_PERIODS)
    out = run_sigrok(["--config", f"samplerate={samplerate}", "--samples", str(n), "-O", "csv"])
    hits = toggling_channels(parse_csv_columns(out))
    if hits:
        print(f"toggling: {', '.join(hits)}")
        return 0
    print("[FAIL] no channel toggled: signal wire not on a data pad, or GND not shared")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="D0")
    ap.add_argument("--samplerate", type=int, default=1_000_000)
    ap.add_argument("--find-channel", action="store_true", help="report which of the 16 channels toggles")
    args = ap.parse_args()

    if not board_present():
        print("[FAIL] no fx2lafw device found (board plugged in? J4 removed? attached to WSL via usbipd?)")
        return 2
    try:
        if args.find_channel:
            return find_channel(args.samplerate)
        samples = capture(args.channel, args.samplerate)
    except CaptureError as e:
        print(f"[FAIL] {e}")
        return 2
    print(f"captured {len(samples)} samples of {args.channel} at {args.samplerate}Hz")
    ok = True
    for label, passed, detail in verdict(analyze(samples, args.samplerate)):
        print(f"[{'PASS' if passed else 'FAIL'}] {label}: {detail}")
        ok = ok and passed
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
