# optical_shadow_readout

A modulated LED, a photodiode and a TIA, read through the lock-in's
demodulator: a displacement sensor that measures how much of a light beam
gets past an object (the "flag"), with ambient light, lamp flicker and the
photodiode's DC level all rejected. It is the optical readout that
`FORCEBAL` (the torsion/beam-balance displacement readout, tier5 in
[spacetime_circuits_dependency.md](../../docs/spacetime_circuits_dependency.md))
needs, built entirely from parts on hand and from two circuits that have
already been designed: the bench-tested `TIA`
([transimpedance_amplifier](../transimpedance_amplifier/)) and
[lockin_amplifier](../lockin_amplifier/). It is the readout, not the balance:
nothing mechanical is designed here.

**Status: designed and simulated 2026-10-02 (`smoke_test.py` green, 22
checks); not built.** `main.py` was compiled under MicroPython on the Pico
and its register programming is the same as `lockin_amplifier`'s (checked on
the Pico with the logic analyzer); the whole script ran against mocks only.
Build `lockin_amplifier` first: this circuit is its demodulator with a
different front end, so validating that one validates most of this one.

---

## Files

| File | Purpose |
|------|---------|
| `optical_shadow_readout.spice` | ngspice transient netlist: photodiode as a current source (ambient + LED-driven + flicker), TIA, gain stage, demodulator |
| `smoke_test.py` | Nine simulated bench states, then `main.py`'s checks against a mocked bench (LED, ambient light, flag, button) |
| `main.py` | MicroPython: LED check, ambient-rejection test, flag test, then a live "percent of the beam getting through" |
| `breadboard.md` | Wiring and failure table |

---

## Design

```
GP8 ─1kΩ─►|─ GND   (red LED)        ┌──────────── flag ────────────┐
                    light ───────────┘     (blocks part of the beam)
                                  PT334-6C (anode GND, cathode to the TIA's − input)
                                         │
 TIA reference 0.105V (10k/330Ω) ──► LM358 U1A + 100kΩ ‖ 100pF ─► tout   (idles at 0.1V + Iph·100kΩ)
                                                                  │
   tout ─0.5µF─10kΩ─►(−) U1B (Rf = 10kΩ: gain −0.9; Vmid on +) ─► out1
   out1 ─ CD4066B #1 (REF) ─100k─ A ─1µF─ GND ─ follower ─► GP26       X = V(GP27) − V(GP26)
   out1 ─ CD4066B #2 (REFB) ─100k─ B ─1µF─ GND ─ follower ─► GP27       tout ─► GP28 (the TIA's DC level)
```

Everything from the 0.5µF (two 1µF electrolytics back to back, since `tout`'s DC level is below the stage's 1.1V) onward is `lockin_amplifier`, with its test-signal resistors removed
and `Rf` changed from 1MΩ to 10kΩ (that circuit's gain of 91 is for millivolt signals; a TIA
delivers hundreds of millivolts).

| Choice | Value | Why |
|--------|-------|-----|
| LED | red, yellow or green 5mm, from GP8 through 1kΩ | 1.1–1.5mA, inside a GPIO's 4mA default drive. A blue or white LED (Vf about 3V) would get 0.3mA and barely light. Photodiode response to red light is unverified, but the PT334-6C responded to white room light and a phone flashlight (2026-09-17), so visible light reaches it |
| Modulation | 1kHz square, in phase with the demodulator | One counter clock for the LED and for REF/REFB: the phase is exact (see `lockin_amplifier`) |
| TIA | `Rf` 100kΩ, `Cf` 100pF, photodiode held 0.1V reverse-biased | `Cf` keeps the 50pF photodiode from peaking the loop. The 0.1V reference keeps the output off the LM358's 20mV floor in a dark room: the first simulation, with the reference at ground, lost 20% of X when there was no ambient light |
| Gain stage | 10kΩ / 10kΩ (gain −0.9) | A 2µA modulation is 0.2V at the TIA; the gain stage's output can swing about 0.8V p-p. Other gains by swapping `Rf` and `Rin`: 10k/2k = 4.5, 100k/10k = 9, 100k/2k = 45, 1M/10k = 91 |
| Averaging | 100kΩ and 1µF, 0.21s effective time constant | A reading needs about 1.6s to settle |
| TIA level on GP28 | direct from `tout` | Shows the ambient light, so the rejection can be demonstrated rather than assumed |

Simulated numbers (modulation `imod` 2µA peak-to-peak at the photodiode, ambient 5µA, unless noted):

| Bench state | X = VB − VA | TIA DC level |
|-------------|-------------|--------------|
| Beam open | 195.3mV | 0.71V |
| Half the light (1µA) / a quarter (0.5µA) | 97.6mV / 48.8mV: exactly linear | |
| Beam blocked | 0.0µV | 0.61V |
| Dark room (no ambient) | 195.3mV | 0.21V |
| Ambient 13µA | 195.3mV | 1.51V |
| 100Hz flicker 3µA peak (0.8V p-p at the TIA) | 195.3mV | |
| Ambient 25µA | −0.1mV: **the TIA saturates at 1.8V and the signal is gone** | 1.80V |
| 100k/10k gain option, 0.2µA modulation | 194.7mV | |

The ambient limit is `(1.8V − 0.105V − modulation·Rf) / Rf`: about 15µA of ambient photocurrent with 2µA of
modulation. A phone flashlight held close reached 7µA-equivalent on the earlier TIA test (0.75V on
`Rf` = 100kΩ), and `main.py`'s ambient stage fails with a "too bright" message before the TIA saturates.

## What this does not show

- **The modulation amplitude.** `imod` is how much photocurrent the LED adds at the photodiode. It depends on the LED, its current (1.3mA here), the distance, any lens or tube between them and the flag. Nothing on this bench has measured it; 2µA is an estimate for a red 5mm LED 15mm from the photodiode. The simulation shows what each decade of it does and the gain table above says which resistors to pick; the first run of `main.py` tells which one is needed (the LED stage reports the X it got).
- **Electrical pickup.** The 3.3V LED drive and clock edges can couple into the TIA input, which is high impedance, through the breadboard. It is at the LED's frequency and in phase with it, so it reads as light. The flag stage's "removes at least 80%" check exposes it: with the beam physically blocked, X should fall to near zero. Keep the GP8 and GP10/GP11 wires away from the photodiode and TIA input rows.
- **The mechanics.** No flag, mount, beam balance or shadow geometry is designed here. The relation between flag position and X is whatever the optics give; `main.py`'s live percentage is relative to the two positions it was calibrated at, and it is only linear over the part of the beam that the flag edge crosses.
- **The photodiode's own numbers.** Junction capacitance (50pF), dark current and responsivity are assumed, not measured; the PT334-6C's datasheet isn't in `docs/manuals`.
- **Resolution in displacement terms.** The Pico ADC's 0.8mV step is 0.4% of a 195mV full scale; the ADS1115 (`adc_ads1115`) would give 0.06%. What that is in micrometres depends on the beam width at the flag, unknown here.
