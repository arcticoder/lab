# KB: verifying parts from datasheets, and what a session can probe live

Audience: future LLM sessions. Not end-user content. Written 2026-10-02.

## Fetch datasheets instead of recalling them

Two errors in this repo were found only because a design needed a datasheet
number: `parts_reference.md` and the `cd4066_switch_tester` docs had the
CD4066B's `VSS` on **pin 6** (TI's datasheet: pin 7; pin 6 is a control
input), and the TL431A's TO-92 pinout was missing altogether. A third check
(INA126, for a possible instrumentation amplifier) showed the part is
unusable at 3.3V and saved a purchase. Rule: before wiring or ordering a part
in a design, read its datasheet's pin table, absolute maximums and the
electrical limits at *3.3V*, not the headline ±15V table.

Method that works from the session shell:

- `WebFetch` on a PDF URL fails ("binary content"), but saves the PDF; use
  the saved path, or `curl -sL -m 90 -o x.pdf <url>`. TI (`ti.com/lit/ds/
  symlink/<part>.pdf`), Honeywell (found by `WebSearch`) and
  `datasheets.raspberrypi.com/pico/pico-datasheet.pdf` all downloaded.
- `pdftotext -layout x.pdf x.txt` and `grep` for the pin table and limits.
- Figures (package pinouts, common-mode range curves) are not in the text:
  `pdftoppm -r 100 -f <page> -l <page> -png x.pdf out`, then Read the PNG.
  The TO-92 pin order for the SS49E and TL431 came from the drawings.
- Put the scratch files in the scratchpad, and keep only the facts (with the
  datasheet revision and date) in `parts_reference.md`.

Facts established this way (all in `parts_reference.md` or the circuit's
README now):

| Part | Fact |
|------|------|
| CD4066B | `VSS` pin 7; controls: switch 1 pin 13, 2 pin 5, 3 pin 6, 4 pin 12; supply 3–18V; control-high threshold 0.7·VDD; Ron isn't tabulated below 5V (model 1kΩ at 3.3V) |
| TL431A | TO-92 (LP): 1 cathode, 2 anode, 3 ref; Vref 2.470–2.520V; Imin 1mA max; no capacitor on the cathode |
| SS49E | TO-92 flat face: VCC, GND, OUT; supply 2.7–6.5V; null ±5% of VCC; 1.0–1.75mV/G at 5V; output span 1.05V to Vs−1.05V min; 6–10mA at 5V; abs max supply −5V to 8V |
| INA126 | input common-mode range stays about 1.5V inside each rail (Figure 5-7): a 0.3V window on 3.3V |
| Pico ADC | `ADC_VREF` is fed from 3V3 through 201Ω with 2.2µF (and 1Ω R9); an external shunt reference may be connected there; the ADC draws ~150µA, a ~30mV offset |
| RP2040 pins | ADC pins must not exceed IOVDD + 0.3V; absolute maximum 3.8V on digital pins |

## What a session can do live with the rig left plugged in (2026-10-02)

When the user says the rig is attached, both USB devices were visible to
`lsusb` in the session shell (the Pico as `2e8a:0005`, the analyzer as
`04b4:8613`), `mpremote` found the Pico, and `sigrok-cli --driver fx2lafw
--scan` listed the board. Running the capture needs the Pico script going in
the background (`(timeout 60 mpremote run main.py &)`; sleep 3).

Things worth knowing:

- `sigrok-cli --scan` re-enumerates the board (the USB device number changed
  each time) and `usbipd.exe list` can stop showing it as `Attached` for a
  moment; retry rather than conclude it is gone.
- The only pin known to be wired is **GP15** (to analyzer pad `PB0`, `D0`).
  Driving GP15 is safe and was used to verify raw-register PWM behaviour
  (below). Don't drive any other pin; read-only register pokes on slices whose
  pins aren't set to PWM drive nothing.
- A script can be syntax/compile checked under MicroPython without running it:
  `mpremote exec "src=<repr of file>; compile(src,'main.py','exec'); print('ok')"`.
  Use that for any `main.py` that drives pins the session can't see.
- `mem32` accesses from MicroPython are slow (two reads through a helper
  function were about 90µs apart, inferred from the counter offset): don't time
  anything against register reads.
- Verified on the Pico against the logic analyzer: PWM slice 7 programmed
  through registers (`DIV` 2, `TOP` 62499, `CC` B = 15625) gives 1000.0Hz /
  25.0% on GP15; setting `B_INV` (CSR bit 3) with the enable bit kept gives
  75.0%. Global enable at `0x400500A0` with atomic set/clear aliases at
  `+0x2000`/`+0x3000` starts several slices on one clock edge; presetting
  `CTR` before enabling gives a fixed phase between slices (measured: against a preset
  of 15625 counts, 30 reads gave 14980–15610, within 1% of a period, the spread
  being the timing of the reads). `Pin(n, Pin.ALT, alt=4)` selects the PWM function. DIVMODE (CSR
  bits 5:4) reads back; rising-edge counting of a real signal was not tested.
  `lockin_amplifier/main.py` itself was exec'd on the Pico with `REF_A, REF_B =
  14, 15` substituted (so REFB lands on GP15): 1000Hz, 48.0% high, and the same
  after `set_state('in', 90, False)`. That is the pattern for exercising a
  script that drives unseen pins: remap one output onto GP15, `exec` the source
  with `__name__` set to something other than `__main__`, capture, shut down.
- Registers worth knowing: `PWM_BASE` 0x40050000, slice stride 0x14, `CSR` +0,
  `DIV` +4, `CTR` +8, `CC` +0xC (A low half, B high half), `TOP` +0x10.

## Logic analyzer bring-up: what was learned

- Capturing needs the firmware-loaded board attached with usbipd (see
  `logic_analyzer_check/breadboard.md` for the two-window sequence that worked).
- Wiring that passed: Pico GP15 → `PB0` (J2, "PB0 PB1" row), Pico GND → J2's
  bottom-row `GND`. `--find-channel` reported only `D0`, so pad `PB0` is `D0` and
  the other pads were quiet; 4MHz sampling also gave 999.9Hz / 25.0%.
- The user's earlier `--find-channel` failure ("no channel toggled") happened
  before the wires were reseated and its cause was never isolated: don't claim
  one. The failure message already names the three candidates (signal wire not
  on a data pad, ground not shared, script not running).
- `logic_analyzer_check/smoke_test.py`'s live check now SKIPs (not FAILs) when
  the board is attached but nothing toggles `D0`, because a smoke-test run
  while the Pico script isn't running is not a code fault.
