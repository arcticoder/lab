# TODO — completed (arcticoder)

Entries move here from
[TODO-arcticoder.md](TODO-arcticoder.md) once done, instead of being
deleted — this is the audit trail of what was on the active checklist and
when it was closed out, so finished work stays visible and isn't
accidentally re-proposed or duplicated later. Mirrors the format used in
the sibling `aqei-bridge` repo's `docs/TODO-completed.md`: one `##
YYYY-MM-DD` heading per closure batch, with a short bullet per item under
it.

This is a different record from `README.md`'s "built & bench-tested"
table and `docs/history.md`: those track a *circuit's* real-world status
(has it been physically assembled and validated), while this file tracks
the *TODO item's* lifecycle (was it on the list, and when did it come
off). A circuit can be bench-tested without its TODO wording exactly
matching, so don't assume one file makes the other redundant.

---

## 2026-09-23

- **SparkFun Breadboard Power Supply Kit (`psu_medlow_lm317`) moved from
  "Deferred" to "Next order" (RobotShop).** The purchase is decided and
  no longer waits on the `psu_medlow_usbc` CC-pin check; the kit is the
  adjustable-rail PSU that follows `psu_4xaa`. Its 9–12V DC input has no
  source on the bench yet — the PD trigger board's 9V/12V tap off the
  Lenovo adapter is the candidate, pending a look at the adapter's label.
- **Mini-USB cable added to the AliExpress cart** (for `SCOPELA`). The
  cart is still under the $10 free-shipping threshold; `TODO-arcticoder.md`
  now leads with adding the PD trigger board and power-resistor
  assortment (both real `ACTIVELIM` needs) and checking out.
- **`measurement_tools/resistance_measurement` set up for the USB-C
  breakout CC-pin check (`breadboard3.jpg`); first pass read open,
  which was not yet a CC measurement.** The drifting 700kΩ–850kΩ
  prints were the open-input signature of this jig (ADC top-of-range
  noise, ~3.26V), not a resistance. `main.py` now reports "Circuit Open"
  above 97% of `V_IN`; its README documents the range limits and a
  probe-tip positive control. The CC-pin check stays in "Ready to build
  now" with concrete steps.

## 2026-09-22

- **`measurement_tools/capacitance_bridge` (`CAPBRIDGE`) — physically
  assembled and bench-tested, PASS.** Reseated `Rref`'s far lead (was
  resting on the breadboard's center divider ridge, not in the junction
  hole — the near-zero/near-instant "Cx" readings from the first attempt
  the same day were a floating ADC node, not a `main.py` bug, per
  `kb/bench_photo_diagnostics_notes.md`'s matching entry), then swapped
  `Cx` for a 47µF (25V) unit from the electrolytic kit: three consecutive
  runs read 48.87µF/47.75µF/47.64µF, all within the kit's own ±20%
  tolerance of nominal. Moved from `TODO-arcticoder.md`'s "Ready to build
  now" to `README.md`'s "built & bench-tested" table; that section now
  has only the `psu_medlow_usbc` CC-pin check left.
- **`TODO-arcticoder.md` trimmed of several no-current-consumer bench-
  validation bullets that had accumulated in the "standalone validation
  tail."** The 1N5817 diode-drop check + `psu_3xaa` assembly,
  `psu_ultralow_v1`'s demo power-on check, CD4066BCN switches 2–4, and
  the glass-tube-fuse test jig all moved to "Deferred" — each is
  genuinely parts-on-hand-but-nothing-needs-it-yet busywork, not staged
  inventory for a real build. See
  [kb/todo_list_conventions.md](kb/todo_list_conventions.md)'s new entry
  refining the ranking criteria: criterion 5 alone no longer earns a
  standing spot in "Ready to build now."
- **`VIBISO` and `RIPPLETANK` moved from "Ready to build now" to
  "Blocked."** `VIBISO`: holding off on the mechanical build itself until
  `ACCELIF` exists to actually measure isolation quality, rather than
  building a platform with nothing to bench-test it against yet.
  `RIPPLETANK`: the file had overclaimed that `pico/leds/gpio_pwm_led/`
  "drives a small motor/speaker dipper directly" — it only generates a
  GPIO-level PWM signal; an actual motor/speaker driver stage (transistor
  switch + flyback diode) doesn't exist yet. New design task opened in
  `TODO-agent.md`. Noted for both: the on-hand Creality K1 (with PLA
  filament stock) is a real fabrication option once either build becomes
  actionable (platform feet for `VIBISO`; a precise stepped/sloped depth
  insert for `RIPPLETANK`).
- **`SCOPELA` moved back to "Blocked."** The CY7C68013A board uses a
  Mini-USB port — its own listing title said so, missed at ingestion time
  (see `kb/ordering_ingestion_notes.md`'s corrected entry) — and only
  Micro-USB/USB-C cables are on hand. A Mini-USB cable is now in "Next
  order," bundled into the same not-yet-checked-out cart as the piezo
  disc/Hall sensor.
- **USB-C 16-pin breakout board pinout resolved, not re-asked.**
  `parts_reference.md` already had the full pad list and had already
  flagged the `U+`/`D+` ambiguity as a likely transcription slip
  (2026-08-24); confirmed `D+` against the listing's own full spec text.
  See `kb/todo_list_conventions.md`'s new entry on checking existing docs
  before re-asking for a spec already on file.
- **PD trigger board bullet in "Next order" now states an explicit
  voltage rule**: use the lowest selectable tap that still hits 2A
  within the resistor assortment's 5W/10W rating (5V → 10W at 2A, well
  within one resistor's rating; 20V → 40W, not), not the trigger board's
  max. Hard ceiling regardless: never paired with anything but the
  on-hand Lenovo 65W adapter, never a tap above what that adapter itself
  outputs (20V/3.25A, 65W).

## 2026-09-21

- **`safety/thermal_monitor` (`THERM`) — physically assembled and
  bench-tested, PASS.** Ambient baseline stable (1.708–1.713V /
  10723–10790Ω / 23.3–23.5°C); a sustained finger pinch produced a
  monotonic, physically-consistent response (resistance 10362Ω→8106Ω,
  temperature 24.2°C→29.8°C) as the thermistor warmed, and the alarm LED
  correctly stayed off the whole run (never reached
  `ALARM_THRESHOLD_C=40.0`) — a real alarm *trip* hasn't been
  bench-tested yet, only the divider/temperature-conversion path. One
  transient single-sample outlier mid-run (698639Ω, −47.4°C) attributed
  to a momentary contact disturbance from handling the thermistor, not a
  wiring fault — see `kb/bench_photo_diagnostics_notes.md`'s matching
  entry for the full diagnosis and a flagged main.py robustness gap it
  surfaced. Removed from `TODO-arcticoder.md`'s "Ready to build now"
  (was item 1); remaining items renumbered 1–12, including the two
  internal "item N above" cross-references and one in `TODO-agent.md`.
  Moved to `README.md`'s "built & bench-tested" table.
- **Disassembled `signal_conditioning/phase_detector` +
  `oscillators/ne555_astable`.** Both bench-tested (2026-09-19); nothing
  else under construction needed them wired, so SN74HC86N, NE555, and the
  3296 trimpot returned to inventory per this repo's ephemeral-circuit
  convention. Removed from `TODO-arcticoder.md`'s "Ready to build now"
  (was item 1); remaining items renumbered 1–13.
- **`GY-521` (MPU6050), `EZ-USB FX2LP CY7C68013A` (SCOPELA), and the
  color-ring inductor assortment reorder all received 2026-09-20.** All
  three moved from "on order" to "received" in `orders.md`,
  `inventory.md`, and `parts_reference.md`. `SCOPELA` needs no circuit
  design (the board itself is the purchase) — added as a zero-cost
  plug-in verification to `TODO-arcticoder.md`'s "Ready to build now".
  `ACCELIF` (tier5) and `INDBRIDGE` (tier3) both need a netlist designed
  against the new part before anything can be physically assembled —
  removed from `TODO-arcticoder.md`'s "Blocked" section and added as new
  open items in `TODO-agent.md` instead.
- **Piezo disc (leaded, 12mm ×12) and linear/analog Hall sensor (49E
  ×10) added to the same AliExpress cart**, not yet checked out — logged
  in `orders.md`'s new "In cart" stage and `TODO-arcticoder.md`'s "Next
  order" section, cross-referenced in "Blocked" (`CHGAMP`/`HALLAMP`).
- **Moved the SparkFun Breadboard Power Supply Kit bullet from "Next
  order" to "Deferred"** in `TODO-arcticoder.md` — its own text already
  said to hold off pending a free continuity check, so it didn't belong
  in the top (action-needed) section; fixed the cross-reference from the
  check's own bullet to point at its new location.
- **Reviewed `docs/FTL-research-state-sept-2026.md`'s "Engineering
  Hurdles" section against both dependency-graph files** — no new node
  or edit warranted; existing `FORCEBAL`/`LASERDRV`/`CALORIF`/`VIBISO`/
  `RFRAD` already cover the bench-relevant subset (radiation-pressure
  steering, thermal measurement, seismic/EM isolation), the rest
  (exotic-matter sourcing, causal-structure computation, quantum-vacuum
  engineering) is materials-science/theoretical-physics work with no
  buildable apparatus. Full reasoning in
  `kb/spacetime_sensor_chain_notes.md`'s matching 2026-09-21 entry.
- **The "don't name a specific theory/institute" doc convention is
  lifted**, per explicit user direction — it was a holdover from an
  earlier, narrower complaint. `kb/repo_docs_conventions.md`'s matching
  entry updated; no existing doc needed retroactive renaming.

## 2026-09-10

- Checked out the AliExpress cart: CY7C68013A / EZ-USB FX2LP USB logic
  analyzer board (`SCOPELA`) and GY-521 (MPU6050) accelerometer module,
  plus a color-ring inductor assortment reorder added to clear the $10
  free-shipping minimum. All three now "on order" in
  [orders.md](orders.md) — see [TODO-arcticoder.md](TODO-arcticoder.md)
  § "Blocked — waiting on a shipment."
- Sourced a replacement for the cancelled color-ring inductor assortment
  (0307 1/4W, 12 values) — reordered the same listing/variant, still
  cheapest available.

## 2026-09-11

- **`power_supplies/psu_4xaa` § Validation check — passed.** GP26 read
  ~1.9V through the output's divider, confirming the PSU's 4-cell chain,
  Schottky, and polyfuse are all wired and working. An earlier attempt on
  a different breadboard read ~0.14V even with the battery pack confirmed
  installed/powered and the Schottky reseated/correctly oriented; the
  fault was never pinned to one component — rebuilding the identical
  circuit on a second breadboard fixed it immediately. The divider ended
  up as 10 kΩ + 5.1 kΩ (not the originally-documented two 10 kΩ), kept as
  the standard going forward. See `power_supplies/psu_4xaa/README.md`
  § Validation/§ Troubleshooting and `README.md`'s bench-tested table.
- Unblocked `oscillators/ne555_astable`, which was waiting specifically
  on this PSU's bench-test — moved from "Blocked" to the top of "Ready to
  build now" in `TODO-arcticoder.md`.

## 2026-09-13

- **`oscillators/ne555_astable` — output divider fault fixed.** Isolated
  with `measurement_tools/resistance_measurement` (reconfigured to
  10kΩ reference / GP28, on its own breadboard, per instruction from the
  user to keep it off GP26 so `oscillation_probe`'s wiring doesn't need
  to move): R1 read ~10kΩ as expected, but R2 read ~273Ω — a mis-picked
  220Ω resistor (confirmed by color bands), not the intended 10kΩ.
  Swapped in a verified 10kΩ; `oscillation_probe` re-run shows swing no
  longer pinned at 3.300V (now ~2.2V) with the same crossing
  count/toggle-rate as both earlier readings. Removed from
  `TODO-arcticoder.md`'s "Open correctness issues" — see
  `oscillators/ne555_astable/README.md` § Validation for the full
  resolution.
- Also found and fixed a stale `R_REF` in
  `measurement_tools/resistance_measurement/main.py` — the working tree
  had `R_REF = 0.1` (an old ammeter-shunt value), which would have
  produced meaningless "Measured Resistance" numbers for anyone running
  it going forward. Corrected to `R_REF = 10000.0` to match the currently
  wired 10kΩ reference resistor.
- **NE555 batch — remaining 9 of 10 units validated PASS.** With the
  output-divider fault fixed (same day, above), swapped IC 2 through IC
  10 through the same `ne555_astable` socket/wiring and ran
  `oscillation_probe` on each (`breadboard3.jpg`): all 9 show swing
  ~2.2-2.25V and crossings in the low hundreds, matching IC 1's already-
  passed reading. **All 10 units in the batch are now validated** — see
  `oscillators/ne555_astable/README.md` § Validation for the per-unit
  table and `docs/inventory.md`'s NE555 row. Removed from
  `TODO-arcticoder.md`'s "Needs a validation step" section.
- **`signal_conditioning/transimpedance_amplifier/` (tier2 `TIA`) —
  designed, simulated, smoke-tested.** PT334-6C photodiode in zero-bias
  mode into an LM358 transimpedance stage (photodiode modeled as an ideal
  10µA current source, `Rf`=100kΩ from the on-hand kit, giving a 1.0V
  design-point output — confirmed by `ngspice -b`, current-source node
  order specifically verified by simulation to give the documented
  positive polarity). `smoke_test.py` checks virtual-ground behavior,
  headroom against `psu_low_v2`'s rail, and the Iph×Rf functional
  relationship — all green. `breadboard.md`, `README.md`, and a streaming
  `main.py` (mirrors `voltage_reference_lm358`'s style) also written. Not
  yet physically assembled — see `TODO-arcticoder.md`'s "Ready to build
  now" for that bullet (no current downstream urgency).
- **`measurement_tools/capacitance_bridge/` (tier3 `CAPBRIDGE`) —
  designed, simulated, smoke-tested.** RC charge-time capacitance meter
  (known `Rref`=100kΩ + unknown `Cx`, timed crossing of 63.2% of Vin)
  substituting for a classical 4-arm AC bridge, the same kind of
  substitution `resistance_measurement` already made for `OHMMETER`.
  Confirmed by `ngspice -b` (10µF nominal test point recovers ~9.997µF).
  `smoke_test.py` checks `Rref` dissipation and the derived-capacitance
  functional relationship — both green. `README.md` documents a "Range"
  table showing this technique targets the 1µF–470µF electrolytic kit,
  not the pF/nF ceramic assortment; `main.py` polls both a discharge and
  a charge phase (not a fixed sleep, so the largest kit values discharge
  fully before timing). Not yet physically assembled — see
  `TODO-arcticoder.md`'s "Ready to build now" for that bullet.
- **`OHMMETER` (tier3) — resolved as already satisfied, removed from the
  active list.** The user pointed out an ohmmeter (`resistance_measurement`)
  already exists and is in active use; re-checked
  `general_purpose_circuit_dependency.md` and found `OHMMETER`'s only
  consumer (tier4) is itself undesigned, so there's no concrete need for
  the originally-scoped 4-wire Kelvin precision upgrade right now. Removed
  the "New `OHMMETER` build" bullet from `TODO-arcticoder.md`'s "Ready to
  build now" (was previously listed there with no folder, which read as
  an open task) and replaced it with a short prose note explaining why
  it's intentionally absent, instead of silently deleting it.
- **`TODO-agent.md` created** — a new Claude-facing counterpart to
  `TODO-arcticoder.md`, tracking file/folder/netlist-creation work (not
  physical bench work) so it gets done proactively instead of surfacing
  as a "no folder exists yet" line item on the user's own list. Moved the
  5 remaining "parts on hand, no folder yet" items (`PHASED`, a `THERM`
  replacement, `ACTIVELIM`/`HVPULSE`, `EPFIELD`, `CHGAMP`) there from
  `TODO-arcticoder.md`'s "Ready to build now", each with enough of its
  current design/sourcing state written down for a future session to pick
  up without re-deriving it. See `docs/kb/todo_list_conventions.md` for
  the reasoning this split is based on.
- **`signal_conditioning/electric_field_probe/` (tier5 `EPFIELD`) —
  designed, simulated, smoke-tested.** Bare-electrode electrostatic
  sensor: 1MΩ/1MΩ bias divider to VCC/2, TL082 unity-gain follower.
  Powered from `psu_pico_rail` (not a battery tier) specifically so the
  output can never exceed the Pico ADC's 0-3.3V range regardless of
  op-amp behavior — a deliberate departure from this repo's usual
  battery-PSU-plus-headroom-caveat pattern. No calibrated sensitivity
  claimed (a floating electrode's real coupling depends on geometry, not
  a representable SPICE current) — simulation only confirms the bias
  divider and follower feedback loop. `smoke_test.py` green.
  `breadboard.md`/`README.md`/`main.py` written. Not yet physically
  assembled — see `TODO-arcticoder.md`'s "Ready to build now."
- **`signal_conditioning/charge_amplifier/` (tier5 `CHGAMP`) — designed,
  simulated, smoke-tested.** 12mm piezo disc into a TL082 inverting
  charge amp (10nF `Cf` feedback capacitor parallel with a 1MΩ
  `Rf_bias`), same VCC/2 bias-divider pattern as `EPFIELD` for bipolar
  swing. Corner frequency ~16Hz documented (above it, true charge-
  integrator behavior; below it, `Rf_bias` dominates). `.op` simulation
  only checks the DC bias-stabilization math (this repo's smoke tests
  don't run `.tran`) — real tap-transient behavior is a hardware
  validation step, documented as such rather than faked in SPICE.
  `smoke_test.py` green. Not yet physically assembled.
- **`safety/thermal_monitor/` (`THERM`) — designed, simulated,
  smoke-tested.** Resolved as the literal safety-subgraph `THERM` node
  ("Thermal Monitoring with Alarm Threshold"), not a new node — MF52AT
  divider (`Rref`=10kΩ matching R25, centers at VCC/2 at room temp) plus
  a GPIO-driven alarm LED, satisfying the "with alarm threshold" half of
  the node's own label, not just bare temperature readout. `main.py`
  implements the beta-equation resistance→temperature conversion.
  `smoke_test.py` green (LED current/power bounds + divider-ratio
  check).
- **`signal_conditioning/phase_detector/` (tier4 `PHASED`) — designed,
  simulated, smoke-tested.** Resolved the previously-open "what's the
  second square wave" design question: a Pico GPIO PWM output,
  independently generated and deliberately **not** phase-locked to
  `ne555_astable`'s oscillator — their natural phase drift sweeps the
  XOR's filtered output through its full range, which is what actually
  validates the XOR primitive on real hardware (see this circuit's own
  README § Design notes for why true phase-locking is out of scope here
  and belongs to whatever eventually builds tier6 `LOCKIN`). First
  digital-logic element in this repo's SPICE conventions (an ideal
  behavioral XOR + RC lowpass, two static logic-level cases). Taps
  `ne555_astable`'s existing output divider for input 1A rather than
  wiring a fresh connection to its raw output. `smoke_test.py` green.
- **`protection/active_current_limiter/` (`ACTIVELIM`) — designed,
  simulated, smoke-tested.** IRLZ44N + 0.1Ω sense resistor + LM358
  comparator, hard-trip (bang-bang) current limiter at a 2A threshold.
  Consumed the only IRLZ44N on hand, ahead of `HVPULSE` (see
  `TODO-agent.md`'s remaining open item) — prioritized because it's
  well-scoped and low-risk (protects a `psu_medhigh`-class rail, well
  within bench-safe voltages) while `HVPULSE` still has no defined target
  voltage or safety design. **Simulation surfaced a real design
  limitation, not just a documented caveat**: forcing the fault case as
  a single closed-loop operating point fails to converge in ngspice
  (`Error: Transient op failed, timestep too small`) — a bang-bang
  comparator with no hysteresis/latch has no stable DC operating point
  under a sustained fault (real hardware would chatter at the trip
  boundary). Worked around by simulating the fault case open-loop
  (checking only the comparator's threshold decision) instead of forcing
  a fixed point that doesn't exist — documented in both the netlist
  header and `README.md` as a real limitation, with linear foldback or
  an explicit latch named as the actual fix if chattering ever proves to
  be a problem. `smoke_test.py` green.

## 2026-09-15

- **`signal_conditioning/electric_field_probe/` (tier5 `EPFIELD`) —
  physically assembled and bench-tested.** TL082 unity-gain follower
  confirmed working at 3.3V single-supply (rest output ~1.693–1.701V vs.
  the simulated 1.650V ideal, a small stable offset, not railed) —
  resolves that circuit's README caveat about running the TL082 below
  its typical minimum supply. A piezo-igniter spark and a
  triboelectrically-charged object (tape peeled off a roll) both
  produced no deflection beyond that same offset band — consistent with,
  not contradicting, the design's own predicted sensitivity ceiling from
  its 1MΩ (not GΩ) bias divider, not a wiring fault. Full diagnosis and
  concrete next steps (free direct-touch retest, then a GΩ resistor
  candidate, then trying `CHGAMP`'s charge-integrating topology instead)
  in that circuit's own README § Bench findings; the GΩ resistor is now
  a standing candidate in `TODO-arcticoder.md`'s "Next AliExpress order"
  section.

## 2026-09-17

- **`power_supplies/psu_low_v2` § Validation check — passed, and
  `signal_conditioning/transimpedance_amplifier` (tier2 `TIA`) —
  re-tested and confirmed working.** `psu_low_v2`'s GP26 divider check
  (assembled 2026-09-16, left unrun) came back 1.007V average over 20
  readings, matching the ~1.0V correct-orientation target. Root cause of
  the gap: the Schottky's cathode band paint had worn off, so its
  orientation was guessed and installed backward — flipping it fixed the
  rail. Re-running `TIA`'s `main.py` afterward gave a genuine
  light-dependent response (~0.505–0.510V ambient, ~0.72–0.78V under a
  phone flashlight, higher held close) in place of the earlier flat,
  light-independent ~0.38V reading — confirming the prior diagnosis that
  the unvalidated `psu_low_v2` rail, not `TIA`'s own wiring, was the
  cause (see `docs/kb/bench_photo_diagnostics_notes.md`). Both circuits
  moved from `README.md`'s "designed, not yet built" table to "built &
  bench-tested." Removed both bullets from `TODO-arcticoder.md`; the
  1N5817 diode bullet there was updated to reflect `psu_low_v2`'s unit
  now being confirmed-good (though unmarkable by eye — see
  `docs/parts_reference.md#1n5817-schottky-diode`), with only `psu_3xaa`'s
  diode check still open. Also fixed an unrelated pre-existing
  contradiction in `transimpedance_amplifier/breadboard.md`'s PT334-6C
  wiring table (anode/cathode were swapped relative to its own prose and
  `parts_reference.md`) while touching that file.

## 2026-09-19

- **`oscillators/ne555_astable` — reassembled and `signal_conditioning/
  phase_detector` (tier4 `PHASED`) — physically assembled and
  bench-tested.** `ne555_astable` had been broken back down to inventory
  since its 2026-09-13 batch validation (per this repo's ephemeral-
  circuit convention), so it was rebuilt first per its own
  `breadboard.md` (powered from `psu_4xaa`) before `phase_detector` could
  tap its output divider. `main.py` streamed the RC-lowpassed XOR output
  continuously; the reading moved (0.871V–1.546V over a ~3.5s sample
  window) rather than pinning at one extreme, which is the real pass
  criterion per `README.md`'s Validation section — the two oscillators
  aren't phase-locked, so a genuinely responding gate shows a moving
  reading, not a specific target voltage. The observed band is narrower
  than the full ~0–3.3V range `README.md`/`breadboard.md` describe, which
  is expected for a short capture window against two close, slowly-
  drifting frequencies (see `docs/kb/bench_photo_diagnostics_notes.md`
  for the same-reading-window nuance) — not a sign of a problem, since it
  did move. A `breadboard.jpg` photo of the as-built jig was saved.
  Circuit broken back down afterward (Pico unplugged), per the same
  ephemeral-circuit convention. Moved `phase_detector` from `README.md`'s
  "designed, not yet built" table to "built & bench-tested"; removed its
  bullet from `TODO-arcticoder.md`'s "Ready to build now" (`CHGAMP` is
  now the sole remaining `LOCKIN` prerequisite, still blocked on flux —
  see that file's ranked list, renumbered #1–#6 accordingly).
- **Five 2026-09-18 tier5/7 shopping-list items resolved into explicit
  decisions, not left as open questions** (see
  `TODO-arcticoder.md`'s "Next AliExpress order" and "mech" paragraph for
  the reasoning behind each): SiPM module and scintillator tile/paddle
  (`SIPMFE`) deferred — the sensor alone is expensive enough that you're
  holding off on the whole node for now, revisit later. Laser-diode
  option for `LASERDRV` taken off the table indefinitely over a real
  eye-safety gap (no enclosure/beam-dump/laser-rated goggles on this
  bench) — staying on the free on-hand-LED path; a plain higher-power LED
  (not a laser) remains a legitimate future upgrade without that safety
  question attached. Torsion fiber + mirror for `FORCEBAL` also taken off
  the shopping list — `FORCEBAL`'s own node name allows a knife-edge
  beam-balance mechanical form (no suspension fiber) paired with a
  `CAPBRIDGE` capacitive-plate readout (foil/scrap-copper, no purchase),
  so the node is buildable now without ordering anything; the torsion
  variant stays a possible future upgrade if the beam-balance/capacitive
  route proves insufficient. Also clarified what `VIBISO`/`RIPPLETANK`
  each still need to go from "built" to "used in an experiment"
  (`ACCELIF`, still blocked on the in-transit GY-521, for quantifying
  `VIBISO`'s isolation; the sibling repo's `pico/leds/gpio_pwm_led/` for
  `RIPPLETANK`'s wave driver, no new build needed for a first qualitative
  demo).
- **Resolved 2026-09-18: possible missing tier5 node (precision
  force/displacement-balance readout).** Added as `FORCEBAL` at your own
  explicit direction — see `spacetime_circuits_dependency.md`'s "Why
  these new tiers" section. `LVDTAMP` is one way to instrument it; a
  capacitive-plate readout via `CAPBRIDGE` (designed/simulated, ranked in
  `TODO-arcticoder.md`'s "Ready to build now") is the other, and needs no
  new purchase. (Moved here from `TODO-arcticoder.md`'s Backlog section,
  where it had sat as a checked-off historical note instead of being
  logged and removed.)
- **`CHGAMP` status corrected — it was never "in progress," and the
  attempt is paused, not active.** `TODO-arcticoder.md` had drifted into
  presenting `CHGAMP` as `LOCKIN`'s in-progress remaining prerequisite;
  the actual state is that the 2026-09-16 bare-piezo soldering attempt
  failed (no flux on hand), and the build was stopped there — all its
  parts (TL082, piezo disc, resistors, capacitor) went back to inventory
  rather than staying mid-assembly. Moved the bullet from "Ready to build
  now" to "Blocked" (blocked on flux sourcing, not on-hand parts), and
  corrected `inventory.md`'s TL082/piezo rows and
  `parts_reference.md`'s piezo entry to match. Confirmed decision: retry
  later once flux is sourced, not abandon the node.
- **Flux sourcing: not AliExpress, and RobotShop doesn't carry it.**
  You've ruled out AliExpress for flux specifically (a toxicity/quality
  concern distinct from the general "wait out AliExpress transit"
  preference), and RobotShop — where the SparkFun Breadboard Power Supply
  Kit is going instead — doesn't sell it. `TODO-arcticoder.md`'s "Next
  order" section now tracks flux as its own open sourcing decision (which
  non-AliExpress, non-RobotShop retailer) rather than folding it into the
  AliExpress shopping list.
- **`TODO-arcticoder.md` restructured to cut backstory out of the
  checklist itself.** The file had accumulated multi-paragraph
  ranking-rationale, arrival-date narrative, and session-history asides
  that duplicated content already in `kb/todo_list_conventions.md`,
  `spacetime_circuits_dependency.md`'s "Why these tiers" sections, and
  this file. Trimmed every bullet to a checklist item plus a one-line
  "why," with the ranking method and literature justification left as
  pointers rather than restated. Also fixed the "Ready to build now"
  section reading like it had settled, lower-priority items ahead of
  higher-priority ones (the deferred 2026-09-18 shopping-list items had
  been interleaved into "Next AliExpress order" ahead of active items) —
  deferred items are now grouped in their own "Deferred" subsection below
  the actionable ones. See `kb/todo_list_conventions.md`'s matching
  2026-09-19 entry for the fuller reasoning.
