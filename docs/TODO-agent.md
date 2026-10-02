# TODO — agent (Claude-facing)

This is the mirror of [TODO-arcticoder.md](TODO-arcticoder.md) for work
that doesn't need the user's hands, eyes, or a purchasing decision — just
writing files. Design/simulate/document a circuit here (netlist,
`breadboard.md`, `smoke_test.py`, `README.md`, optionally `main.py`) as
its own PR-sized unit of work, *before* it ever gets a "physically
assemble" bullet added to `TODO-arcticoder.md`'s "Ready to build now"
section. See
[docs/kb/todo_list_conventions.md](kb/todo_list_conventions.md) for why
this split exists and the reasoning behind each entry's queue position.

Mirrors the sibling `aqei-bridge` repo's `docs/TODO.md` (a pure
agent-task list — see that repo for the pattern this one is modeled on).

**Workflow**: pick an item below (top-to-bottom isn't a strict ordering
requirement here the way it is in `TODO-arcticoder.md` — none of these
block each other), design and verify it (simulate with `ngspice -b`,
confirm the numbers, run `smoke_test.py` and get it green) the same way
`signal_conditioning/transimpedance_amplifier/` and
`measurement_tools/capacitance_bridge/` were built 2026-09-13, then:

1. Move the item from here to `TODO-completed.md` (dated entry, same
   convention as `TODO-arcticoder.md`'s completions).
2. Add a "physically assemble" bullet for it to `TODO-arcticoder.md`'s
   "Ready to build now" section, stating its real dependency (check
   `general_purpose_circuit_dependency.md`/`spacetime_circuits_dependency.md`
   first — don't infer one from list position, see
   `kb/todo_list_conventions.md`'s TIA correction) and whether anything
   downstream currently needs it built, or whether it's optional/no-rush
   like `TIA`/`CAPBRIDGE` turned out to be.
3. Update this file's own item count/status references elsewhere (this
   file's own intro doesn't currently carry one, but `TODO-arcticoder.md`'s
   "Next order" section does — check it).

---

## Open items

### `THERM` — main.py has no debounce on the alarm decision, non-urgent

Surfaced 2026-09-21 during `THERM`'s bench-test run (see
`kb/bench_photo_diagnostics_notes.md`'s matching entry): a momentary
contact glitch during finger-pinch handling produced one wildly-off
sample (698639Ω/−47.4°C) sandwiched between physically-sane readings.
Harmless this time (the glitch read cold, not hot), but `main.py`'s
alarm LED currently fires off a single print's reading with no
consecutive-reads guard, so a same-class glitch reading *hot* would
trigger a spurious momentary trip with no real over-temperature behind
it. Not blocking `THERM`'s own PASS (the sensor/divider path is
confirmed working) and not urgent — this bench doesn't yet run `THERM`
unattended against a real hazard. Worth a small debounce (e.g. N
consecutive over-threshold reads before lighting the LED) before this
circuit is ever trusted as an unattended monitor; pick N against how
often this kind of breadboard contact glitch actually recurs rather than
guessing a number now.

### Next design pass — what to pick and why (2026-10-01)

The user won't pay shipping on a cart under the AliExpress $10 line and
won't place a one-item RobotShop order, so new circuit designs are also how
the carts fill: a design that needs a part not on hand puts that part on
`TODO-arcticoder.md`'s "Next order" (see `kb/todo_list_conventions.md`,
"Carts fill from designs"). The 2026-10-01 pass added `adc_ads1115` and
`vibration_driver` (below). If the user reports that the AliExpress cart
still shows a shipping fee, pick the next design below that needs a
cheap AliExpress part and add that part to "Next order"; otherwise pick for
the research chain's value, not for the cart.

Candidates, none blocked on a decision:

- **`FORCEBAL` optical shadow readout** (LED + flag on the beam +
  PT334-6C into `TIA`; see the 2026-10-01 correction in the
  `FORCEBAL` entry below) — all parts on hand, no purchase.
- **`LOCKIN`** — the best-justified tier6 target per
  `spacetime_circuits_dependency.md`; a CD4066 synchronous demodulator
  and a TL082 low-pass are on hand. Needs the `PHASED` square wave as its
  reference. May show a purchase (a matched-resistor or precision-rectifier
  part) only once designed.
- **`AAF`** — an active anti-alias filter in front of `adc_ads1115`
  (TL082 Sallen-Key, corner chosen against the ADS1115's data rate); on-hand
  parts, and it follows directly from the 2026-10-01 design.
- **`IA`** (tier4 instrumentation amplifier) — for bridge and Hall signals;
  a dedicated IA chip is the likely cheap AliExpress purchase.

### AA-battery power budget

Tally recorded 2026-10-01 in `kb/power_rail_budget_notes.md`. The earlier
claim that this bench can't run off AA cells was over-broad: it was true
only of `ACTIVELIM`'s 2A check. Keep that file current as designs are added;
the SparkFun kit (shelved 2026-10-01) is revived by a design that breaks the
budget, not by the tier label `psu_medlow`.

### `FORCEBAL` / `SIPMFE` / `LASERDRV` — new tier5/7 nodes (2026-09-18); `SIPMFE`/`LASERDRV` blocked on part sourcing, `FORCEBAL`'s optical readout startable (see the 2026-10-01 correction below)

Added to `spacetime_circuits_dependency.md` 2026-09-18 (see that file's
"Why these new tiers" section) at the user's explicit direction, alongside
two non-circuit mechanical build objectives (`VIBISO`, `RIPPLETANK`, no
`TODO-agent.md` item — nothing to design/simulate for those). Same
situation as `HVPULSE` below in one respect (not startable yet) but for a
different reason: this isn't a scope judgment call, it's that **none of
the three have a specific part sourced yet**, and this file's own workflow
(design/simulate against a real component's real values, the same way
every completed entry below was built) needs one to mean anything —
`FORCEBAL`'s design depends on which displacement-sensing approach gets
picked, and `SIPMFE`/`LASERDRV` both need an actual SiPM/laser-diode part
number before bias/drive values can be simulated. **Don't start a netlist
for any of the three from the tier-graph label alone** — check
`TODO-arcticoder.md`'s "Next order" and "Blocked" sections
first; move this entry to a real open item once a part from any of them
is confirmed received.

**Corrected 2026-10-01: `CAPBRIDGE` is not a displacement readout route.**
An earlier pass listed "a capacitive plate read by `CAPBRIDGE`" as the
no-purchase way to instrument `FORCEBAL`. `CAPBRIDGE` times an RC charge
through 100kΩ with ~1ms ADC polling and its README rates anything near
10pF "No"; a foil plate pair is 3–90pF (see `spacetime_circuits_dependency.md`'s
"Bench-scale resolution budget", reproduced by `tools/resolution_budget.py`),
a charge time of microseconds. So the no-purchase capacitive route needs a
different transduction (a 555 astable with the plate as timing capacitance,
frequency read in hardware), which is a new circuit, not a reuse. The
purchase-free route that *does* reuse built circuits is an optical
readout: on-hand LED + a flag/shadow on the balance beam + on-hand PT334-6C
photodiode into the bench-tested `TIA`. That is a startable design item
(netlist, `breadboard.md`, `smoke_test.py`) independent of the mechanical
balance, and its output range maps directly onto the budget's `R` and `k`
table. Recommendation when it's picked up: the optical shadow readout
first, since every part is on hand and `TIA` is already validated; the 555
C-to-f route second, and only if the optical one proves insufficient.

### `HVPULSE` — tier7/8 high-voltage pulse generator

**Still blocked on a scope decision, not a part.** The only IRLZ44N
currently *wired* is in [ACTIVELIM](../protection/active_current_limiter/)
(see that circuit's README § Design notes for why it was designed
first) — but per this repo's ephemeral-circuit convention (nothing stays
assembled once its own bench check passes and nothing else currently
needs it wired — see `README.md` § Circuits — built & bench-tested),
that single on-hand IRLZ44N returns to inventory once `ACTIVELIM` is
bench-validated, and can then be reused here. **A second unit is only
actually required if `ACTIVELIM` and `HVPULSE` need to be physically
assembled at the same time** — not the case today: both protect/generate
for PSU tiers (`psu_medhigh`/`psu_high`) that are themselves still
backlog with no folder, and this repo doesn't run the experiments that
would ever need two such circuits live simultaneously (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)).
Ordering a second IRLZ44N ahead of that is optional, not a blocker.

More fundamentally: nothing on this bench currently defines what "high
voltage" means here numerically. **This bench's numeric threshold: above
50V DC / 30V AC RMS counts as high voltage** — the same limit IEC 61140's
SELV (safety extra-low voltage) classification uses. Reasoning: dry-skin
resistance runs roughly 100kΩ–600kΩ, but broken/damp-skin contact
resistance can fall to ~1,000Ω — at 1,000Ω, 50V drives 50mA, inside the
30–50mA range that can paralyze respiratory muscles and bordering the
50–100mA range that can induce ventricular fibrillation. Nothing on the
bench today exceeds this threshold (the Lenovo 65W adapter tops out at
20V; no PSU circuit is built around it yet — see
`docs/general_purpose_circuit_dependency.md`'s `PSUMEDHIGH` node) and no
HV source of any kind is in inventory; no isolation/discharge-path safety
design has been done either. **Don't start a netlist for this without
first getting an actual target peak voltage/energy figure and a real
safety design pass (isolation, discharge paths) from the human** — this
is a judgment call, not something to infer from the tier graph's generic
label.

**Once scoped, a netlist/BOM here is fine even with no near-term
physical-assembly plans** — the point is dependency-graph/build-order
clarity, not an assembly commitment (see
[kb/circuit_lifecycle_and_repo_scope.md](kb/circuit_lifecycle_and_repo_scope.md)
for the repo-scope reasoning). Physical assembly of anything exceeding
the 50V/30V threshold above stays out of scope until the human decides
to raise the hazard level of assembled circuits on this bench — don't
add a "physically assemble" bullet for it to `TODO-arcticoder.md` on the
strength of a netlist alone.

---

## Completed (moved out)

- **2026-10-01** (second pass): `oscillators/vibration_driver/`
  (`SIMPGEN`'s actuator stage, the `RIPPLETANK` dipper driver) and
  `signal_conditioning/adc_ads1115/` (`ADCDRV`, a 16-bit external ADC with a
  protected input) — both designed, simulated (`ngspice -b`, numbers
  confirmed against hand calculation), smoke-tested (green) and documented;
  `main.py` files exercised against host mocks only. The motor was chosen
  (a 3V coin vibration motor, the open question in the former `SIMPGEN`
  entry): the servo option was dropped because it needs a supply this bench
  doesn't have, and the motor needs only the 3V3 pin. Their parts are added
  to `TODO-arcticoder.md`'s "Next order". Also fixed the `logic_analyzer_check`
  host script so it prints sigrok's own error (the first run's traceback
  hid a usbipd re-enumeration failure) and added `--find-channel`.

- **2026-10-01**: `measurement_tools/logic_analyzer_check/` (`SCOPELA`'s
  first capture) — not a circuit, so no netlist: a Pico 1kHz/25% PWM
  script, a host-side `sigrok-cli` capture/analysis script, and a
  smoke test (analysis checks, mocked-`machine` check of `main.py`, csv
  parser against real `sigrok-cli` demo output; the live-capture check
  SKIPs without the board). Added to `TODO-arcticoder.md`'s "Ready to
  build now"; nothing downstream needs it — it's an instrument bring-up.
- **2026-09-23**: `measurement_tools/inductance_bridge/` (`INDBRIDGE`)
  and `signal_conditioning/accelerometer_interface/` (`ACCELIF`) —
  designed, simulated, smoke-tested (green) and documented. Both
  `main.py` files were exercised against host-side mocks only. See
  [TODO-completed.md](TODO-completed.md) for the design decisions and
  `TODO-arcticoder.md`'s "Ready to build now" / "Deferred" for their
  assembly status. The same pass corrected `protection/active_current_
  limiter/` (LM358 supply, TL431A pull-up, and a validation plan that
  fits a 2A-rated source).
- **2026-09-13**: `signal_conditioning/transimpedance_amplifier/` (`TIA`)
  and `measurement_tools/capacitance_bridge/` (`CAPBRIDGE`) — both
  designed, simulated (`ngspice -b`, confirmed against hand-derived
  expected values), smoke-tested (green), and documented
  (`README.md`/`breadboard.md`/`main.py`). See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for their new
  physically-assemble bullets.
- **2026-09-13** (second pass, same day): `signal_conditioning/
  electric_field_probe/` (`EPFIELD`, tier5), `signal_conditioning/
  charge_amplifier/` (`CHGAMP`, tier5), `safety/thermal_monitor/`
  (`THERM`), `signal_conditioning/phase_detector/` (`PHASED`, tier4),
  and `protection/active_current_limiter/` (`ACTIVELIM`) — all five
  designed, simulated, smoke-tested (green), and documented. This was
  the direct spacetime-research sensor chain (`EPFIELD`/`CHGAMP` are
  named tier5 nodes in `spacetime_circuits_dependency.md`, not general
  infrastructure) plus the `PHASED` node that unlocks tier6 `LOCKIN`
  processing of their output — see
  [kb/spacetime_sensor_chain_notes.md](kb/spacetime_sensor_chain_notes.md)
  for the design decisions made along the way (single-supply ADC-safety
  bias pattern, the resolved "second oscillator" question for `PHASED`,
  and a real hard-trip chattering limitation `ACTIVELIM`'s own
  simulation surfaced). `HVPULSE` (shares `ACTIVELIM`'s MOSFET) remains
  open above — it needs a scope decision, not more design time. See
  [TODO-completed.md](TODO-completed.md) for the full entry and
  `TODO-arcticoder.md`'s "Ready to build now" for the new
  physically-assemble bullets.
