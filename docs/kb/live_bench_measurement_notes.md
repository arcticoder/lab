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

## USB devices and usbipd: what a session can and can't do (2026-10-01 update)

Read-only probes of the Windows side work from the WSL session: `usbipd.exe
list` prints every USB device, its BUSID and whether it is `Attached`,
`Shared` or `Not shared`, plus a "Persisted" list of stale binds. The
session can't change that state: `usbipd bind` needs an administrator
shell, and `usbipd attach` of a device that isn't bound fails ("Device is not
shared"). Don't try to elevate from the session; hand the user the two
commands. The session can see a device only while it's `Attached`, and
`lsusb` there is the live truth for what the session shell sees, whatever
the user's own terminal showed a minute earlier.

**CY7C68013A with `sigrok` under WSL.** `sigrok-cli --driver fx2lafw --scan`
succeeds even when it can't use the board: the scan uploads the firmware
and lists the device either way. The capture that follows fails with
`fx2lafw: Device failed to renumerate` / `Failed to open device`, because
the board disconnects to re-enumerate with the firmware and `usbipd` doesn't
re-attach the new device (Windows then lists it as `fx2lafw ... Not shared`,
with a fresh device number on each attempt). A bind made before the firmware
loads doesn't survive it. The fix is on the Windows side: bind the board in
its firmware-loaded state, then `usbipd attach --wsl --busid <id>
--auto-attach`. Diagnose with `sigrok-cli ... -l 5`, which prints the upload
and the 3-second wait; `check_capture.py` now prints that stderr itself, so
a traceback that hides it is the failure of the tool, not of the board.
A "loose cable" explanation fits the symptom (a device that keeps
detaching) and is wrong here; read the sigrok log before suspecting hardware.

`sigrok-cli`'s csv output with several channels has `logic,logic,...` as its
header row, with the real names in the `; Channels (n/m): D0, D1, ...`
comment. The demo driver also returns about half of a requested 25 000
samples at 1MHz (12 713 lines seen), so don't use it to check sample
counts.

## Photos of wiring: what the 2026-10-01 bench photo could and couldn't show

The `logic_analyzer_check/breadboard.jpg` photo showed the Pico end of two
jumpers on the breadboard rows beside Pico pins 20 and 18 (consistent with
the guide) and, on the analyzer end, one wire seated on a header and one
jumper end hanging free near the board corner. At 2× crop the header was
too blurry to say which pad the seated wire was on. State that limit
instead of reading a pad off it; the user later reseated a loose lead.

## 2026-10-02: the same rig, attached and working

On 2026-10-02 the user left the Pico and the analyzer plugged in and attached,
and both showed up in the session shell (`lsusb`, `mpremote devs`, `sigrok-cli
--scan`). The first capture passed from the session; see
`datasheet_and_live_probe_notes.md` for what else was verified live, which
pin is the only one known to be wired (GP15), and how to run the capture with
the Pico script in the background. The earlier rule still holds: the session
can't elevate `usbipd`, and the user's pasted output is evidence of what the
Windows side looked like at that time, not a promise about now.
