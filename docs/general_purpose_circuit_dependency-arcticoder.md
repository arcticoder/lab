# TODO: General-Purpose Circuit Build-Out — Active Queue (for arcticoder)

> Blocked items (waiting on a shipment) are in
> [general_purpose_circuit_dependency-arcticoder-BLOCKED.md](general_purpose_circuit_dependency-arcticoder-BLOCKED.md).
> Long-term/undesigned backlog is in
> [general_purpose_circuit_dependency-arcticoder-backlog.md](general_purpose_circuit_dependency-arcticoder-backlog.md).
> Completed circuits are tracked in `README.md`'s "built & bench-tested"
> table and `docs/history.md` — there's no separate completed-TODO file
> here.
>
> This tracks the tiers in
> [general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md).
> Companion track:
> [spacetime_circuits_dependency-arcticoder.md](spacetime_circuits_dependency-arcticoder.md).
>
> Human-facing checklist — a future LLM chat's own working notes on this
> repo belong in `docs/kb/`, not here.

---

## Ready to build now — parts on hand

- [ ] **`oscillators/ne555_astable` (tier1 `OSC`) — bench-build it.** Design
      is simulated but never physically assembled. NE555 (10 on hand),
      3296W 10kΩ trimpot (10 on hand, used as Rb) are both received.
- [ ] **New `TIA` build (tier2, transimpedance amplifier).** PT334-6C
      photodiode (10 on hand) + LM358P (spares available beyond the one
      used in `voltage_reference_lm358`). No folder exists yet — create
      one under `signal_conditioning/` or `measurement_tools/` with the
      usual `.spice` + `breadboard.md` + `smoke_test.py` + `README.md`
      set.
- [ ] **New `OHMMETER` build (tier3, 4-wire Kelvin).** 0.1Ω and 1Ω metal
      film resistors (20 each on hand) are the reference legs. No folder
      exists yet.
- [ ] **`power_supplies/psu_low_v2` — physically assemble.** Was blocked
      on the wire stripper for AA-holder lead termination; that arrived
      2026-09-03. RXEF050 polyfuse batch already validated
      (`measurement_tools/ammeter_1ohm/`). Nothing else is blocking this.
- [ ] **`power_supplies/psu_3xaa` / `psu_4xaa` — confirm and assemble.**
      Likely share the same AA-holder lead-termination step as
      `psu_low_v2` above (same wire-stripper dependency) — verify that
      assumption once `psu_low_v2` is built, then assemble both.

## Needs a validation step before the part can be trusted

- [ ] **NE555 batch — no per-unit bring-up jig exists yet** (unlike
      CD4066B or the polyfuses). Either build one or accept the risk of
      wiring an unvalidated unit directly into `ne555_astable`.
- [ ] **1N5817 Schottky diodes — not validated per-unit.** Check forward
      drop (~0.35–0.45V) on each before wiring into `psu_low_v2`; see that
      circuit's README § "Validation without a multimeter."
- [ ] **CD4066BCN — switches 2–4 per chip still untested** (only switch 1
      of each of the 10 chips has been run through
      `measurement_tools/cd4066_switch_tester/`). Needed before trusting a
      specific chip/switch in a `MUX` or `DEMOD` build.
- [ ] **Glass tube fuses (2A fast-blow, 10 on hand) — no test jig built.**
      Needed before trusting one in the `psu_medlow` protection path
      (pairs with the panel-mount fuse holder, also on hand).

## Open correctness issues to resolve

- [ ] **`power_supplies/psu_medlow_usbc` — status is "incomplete /
      unverified."** The USB-C breakout is passive with no PD controller;
      VBUS may never come up without confirmed CC1/CC2 termination.
      Either physically verify CC1/CC2 termination, or add a PD sink
      controller IC + buck converter, before trusting this circuit.
      `smoke_test.py` has a static `PD_SINK_TERMINATION_CONFIRMED = False`
      check that fails on purpose until this is resolved.
- [ ] **`power_supplies/psu_medlow_lm317` — confirm whether the RobotShop
      kit order actually exists.** README says "not yet ordered, not yet
      built," but this was flagged as possibly having slipped through
      untracked (it's a RobotShop item, not AliExpress, so it wouldn't
      show up the same way). Either place the order or drop it as the
      `psu_medlow` alternative.
- [ ] **`power_supplies/psu_ultralow_v1` — no assembled-PSU demo has ever
      been run**, only component-level validation (battery holder +
      polyfuse individually confirmed). Worth one real bench check of the
      assembled circuit.
- [ ] *(low priority, not currently blocking anything)* **`fuse_test_voltmeter`
      trip detection is non-functional** since bench wiring diverged from
      its original design — the ammeter jigs (`ammeter_10ohm`/`ammeter_1ohm`)
      replaced its role for polyfuse sorting, so this is optional cleanup,
      not a blocker.

## Next parts to buy

- [ ] **8ch 24MHz USB logic analyzer** (`SCOPELA` tier, ~$5–8, built
      around the CY7C68013A / EZ-USB FX2LP chip — `sigrok`'s `fx2lafw`
      firmware supports it out of the box, no vendor software needed).
      First tier with real hardware-timed sampling/triggering; needed to
      properly validate tier2/tier3 circuits and the CD4066 `MUX` beyond
      what the Pico's software-timed ADC can confirm. Check whether the
      listing bundles an 8-wire test-clip cable and a USB cable (dongle
      vs. separate port) before assuming nothing else is needed.
- [ ] *(optional upgrade, not blocking)* **Tier 1 `REF`** — TL431A
      precision shunt reference (5 on hand, untested) could replace or
      supplement the resistor-divider + LM358 buffer for better precision.
