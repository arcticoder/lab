# KB: taking live measurements from a session

Audience: future LLM sessions working in this repo. Not end-user content.

## The Pico is reachable from the session shell

The user works in WSL and sometimes leaves a rig plugged in and says so.
When they do, `mpremote devs` lists the Pico (`/dev/ttyACM0`, MicroPython
board) and `mpremote run <script>` executes a script on it without saving
anything to the board's flash. First used 2026-09-23 on the
`resistance_measurement` jig.

- Keep scratch probe scripts in the session scratchpad, not in the repo.
- Read-only ADC reads are always fine. Before *driving* a pin, check what
  the pin is wired to; on a jig probing another circuit, don't drive it.
- `mpremote run main.py` on a `while True` script never returns — wrap in
  `timeout 8 mpremote run main.py | head`.
- You can't see the bench. A photo plus an ADC number can't tell you which
  breakout pad a lead is on or whether a Dupont pin is seated. State what
  the measurement does and doesn't show, and hand back any check that
  needs the leads moved as a concrete step with a positive control.

## Useful reads

- GP29/ADC3 = VSYS/3 on a Pico: `raw / 65535 * 3.3 * 3` gives the supply
  after the USB diode (5.016V on 2026-09-23).
- Internal pull-down on an input is 50–80kΩ; a pull-down step on a
  divider midpoint gives `R_REF` to within that range, nothing sharper.
- `machine.ADC(n)` puts the pin in analog mode, so a GPIO can't be driven
  and ADC-read on the same pin. See `bench_photo_diagnostics_notes.md`
  (resistance-jig entry) for the open-input ADC signature.

## USB devices attach to WSL per device (2026-10-01)

On 2026-10-01 `lsusb` in the session shell listed only root hubs — no
Pico, no CY7C68013A board — while the user's own terminal had just run
`sigrok-cli --driver fx2lafw --scan` and found the board. Devices reach
WSL through usbipd attachment, and the session shell is not guaranteed to
see what the user's shell sees. Don't treat an empty `lsusb` as "the
board isn't working"; the user's pasted output is the evidence, and a
live probe from the session needs the user to say the rig is attached
(see the Pico note at the top of this file).

`sigrok-cli --driver demo` needs no hardware and works from the session
shell: use it to check output formats (its csv is `;` comment lines, a
header row, then one value per sample per line) when writing parsers
that will later read real captures.
