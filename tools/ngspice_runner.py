"""
tools/ngspice_runner.py
------------------------
Shared helper for per-circuit smoke_test.py scripts: run an ngspice
netlist in batch mode and parse its operating-point `name = value` print
lines into a dict, so each smoke test only has to define thresholds, not
reimplement ngspice invocation/parsing. Confirmed against real ngspice
output (2026-08-24): `op` + `print` produces one `name = value` line per
signal (e.g. `v(2) = 1.490385e+00`, `i(vbatt) = -9.61538e-02`) before any
`dc` sweep table — this only parses those lines, not sweep tables.
"""

import re
import subprocess

_VALUE_RE = re.compile(r"^([a-zA-Z_][\w().]*)\s*=\s*([-+0-9.eE]+)\s*$")


def run_ngspice(spice_path: str) -> str:
    """Run `ngspice -b <spice_path>` and return raw stdout."""
    result = subprocess.run(
        ["ngspice", "-b", spice_path],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ngspice failed on {spice_path}:\n{result.stderr}")
    return result.stdout


def parse_op_values(stdout: str) -> dict:
    """Parse `name = value` operating-point lines into {name: float}."""
    values = {}
    for line in stdout.splitlines():
        m = _VALUE_RE.match(line.strip())
        if m:
            values[m.group(1)] = float(m.group(2))
    return values


def get_op_values(spice_path: str) -> dict:
    """Run a netlist and return its parsed operating-point values."""
    return parse_op_values(run_ngspice(spice_path))
