# KB: designing with the LM358 on the Pico's 3.3V rail

Audience: future LLM sessions designing analog circuits in this repo. Not
end-user content. Written 2026-10-02 after five designs (`lockin_amplifier`,
`optical_shadow_readout`, `hall_amplifier`, `frequency_counter`,
`overvoltage_monitor`) each hit one of these limits in simulation. The LM358
is the on-hand op-amp (10 pcs); the TL082's single-supply behaviour on 3.3V is
unverified (`EPFIELD` ran, nobody measured its limits).

## The four numbers that decide every 3.3V LM358 design

| Limit | Value on 3.3V | Consequence |
|-------|---------------|-------------|
| Input common-mode ceiling | about 1.8V (VCC − 1.5V) | Nothing can be sensed above 1.8V directly. Mid-rail (1.65V) is *marginal*; this repo centres small-signal work on 1.11V (10k/5.1k divider) |
| Output ceiling | about 1.8V | An op-amp can't produce a reference above 1.8V: a `Vn` of 1.815V (a Hall sensor's worst-case null) can't be generated. A comparator output needs an external pull-up to be a logic high |
| Output floor | about 0.02V | A TIA with its non-inverting input on ground idles on the floor in the dark and loses signal; bias it to 0.1V |
| Input range at the bottom | includes ground | Low-side sensing and photodiode TIAs are fine |

Consequences used in the designs:

- **Difference stage instead of non-inverting stage** (`hall_amplifier`): the
  10k/100k input divider keeps the amplifier's input nodes near 1.58V when the
  sensor sits at 1.65V. Matched legs also cancel supply movement when the
  sensor and the reference are both ratiometric to 3V3.
- **Centre outputs at about 0.93V**, where the LM358 has about 0.9V either way.
- **Don't put a trim on a node the op-amp has to drive above 1.8V.** The
  first `hall_amplifier` trim scheme failed at the datasheet's +0.25V null
  extreme for exactly this reason; a second scheme (injecting current into
  the inverting node) unbalanced the legs (+10% gain, common-mode gain of 1).
  The shipped design keeps the first and documents the limit.
- **Comparator output**: the LM358's source stage stops at 1.8V, so a logic
  line needs a pull-up to 3V3, and *whatever else loads that node pulls it
  down*: a 1kΩ base resistor held `overvoltage_monitor`'s tripped TRIP line at
  0.92V (base clamps at 0.7V). Check the loaded logic-high level in the
  smoke test, not just the unloaded one.
- **AC-coupled Schmitt trigger: don't.** `frequency_counter`'s first analog
  path had a capacitor in front. With a stiff source behind the capacitor
  the positive feedback has no impedance to push against at the signal
  frequency (chatter on 8mV of noise); with a series resistor added it could
  latch high for any input under about 45mV, because the capacitor's DC level
  settles to the output's average. DC-coupled with a trimpot-set level has
  neither problem.
- **Polarized coupling capacitor between nodes at different DC levels**
  (`optical_shadow_readout`: TIA output 0.2–1.5V into a stage at 1.11V): the
  electrolytic would be reverse-biased. Two 1µF electrolytics anti-series
  (a non-polar 0.5µF) fix it.
- **Averaging with a gated switch has an effective time constant R·C/duty**,
  not R·C: a CD4066B closed 48% of the time makes 100kΩ × 1µF settle with 0.21s.
  The first lock-in transient (0.6s) wasn't settled; the smoke test runs 2s
  and reads the last 0.4s.
- **Gain stage for a TIA output** (a few hundred mV) needs gain near 1, not
  the 91 that suits a millivolt signal; `optical_shadow_readout` lists gain
  options by swapping two resistors.
- **LM358 as a low-end current amplifier loses its first milliamps** to its
  input offset and 0.02V output floor unless the stage is referenced above
  ground (see `hall_amplifier`'s difference stage). Noted for `OVERCUR`.

## ngspice modeling conventions that worked

- Behavioral LM358 subcircuit: `Eg x 0 inp inn 1e5`, `Rp x y 1k`, `Cp y 0 15.9u`
  (pole at 10Hz: 1MHz GBW), `Bo o 0 V = min(max(V(y), 0.02), 1.8)`, `Ro o out 50`.
  The clamp must come *after* the pole; clamping the gain stage first turns
  the model into a slew-limited device and the closed-loop gain collapses.
- **DC operating-point convergence with the clamp**: a plain `.op` (or a
  transient that starts from `.op`) can land on a non-physical stuck solution
  (a unity buffer at 0.02V). For transients use `tran ... uic` plus `.ic` on
  every node *and on the subcircuit-internal nodes* (`v(xu1a.y)=1.114`);
  for static netlists drop the pole and add `.nodeset` on the outputs.
- **Parameterised netlists**: smoke tests rewrite `.param name=value` lines
  by regex, assert exactly one substitution, and run the file from a temp
  path. Results come out of ngspice as `meas` (parsed by regex) or `print`.
  `let` variables can't contain `.param` names (`vs` isn't visible inside
  `.control`); compute from `v(vcc)` instead (a check that read a hard-coded
  3.3 in a 2.83V-rail test passed for the wrong reason).
- **Hysteresis sweeps**: `dc vmon 0 9.5 0.002` then `9.5 0 -0.002` with
  `meas dc vx WHEN v(out)=1.65 RISE=1` / `FALL=1` finds trip and release.
  Works with the open-collector comparator model (`SW` sink, `Roff=1e12`).
- **Counting edges** from a transient: `print time v(out) > file`, parse the
  `index time value` rows in Python, count 0→1 crossings. `meas` can't count.
- **Speed**: 2s transients at 10µs steps take about 7s each; run cases in a
  `ThreadPoolExecutor(max_workers=4)` with `OMP_NUM_THREADS=1` and a 180s
  timeout of your own (`tools/ngspice_runner.run_ngspice` has a 30s timeout
  and no env control). The lock-in smoke test takes about 50s.
- Smoke tests should also pin *documented limits* as assertions (the
  `hall_amplifier` +0.25V null that can't be reached; the TIA saturating at
  25µA of ambient), so a README claim can't silently go stale.
