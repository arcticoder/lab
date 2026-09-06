# TODO — Spacetime-Research Circuit Build-Out (for arcticoder)

Human task list for realizing tiers 5/7/8 laid out in
[spacetime_circuits_dependency.md](spacetime_circuits_dependency.md).
Companion file:
[general_purpose_circuit_dependency-arcticoder.md](general_purpose_circuit_dependency-arcticoder.md)
for the general-purpose foundation these tiers sit on top of.

This is a human-facing checklist — for a future LLM chat's own working
notes on this repo, see `docs/kb/` instead (not this file).

As of the last gap analysis, **tier5 has zero buildable nodes** — every
sensor-interface item is either unsourced or still in transit. Nothing
here is currently blocking general-purpose work; this whole tier is
further out.

---

## Waiting on parts already on order (placed 2026-09-03, not yet received)

- [ ] **`HALLAMP` (tier5) — partially unlocked once KY-003/A3144 arrives,
      but not fully.** That module is digital switch-output (a
      presence/proximity read), not the linear-analog Hall element the
      original `HALLAMP` op-amp-amplifier design needs. A genuinely linear
      part (e.g. a 49E) is still needed if the amplifier circuit itself is
      still wanted — see next section.
- [ ] **`EPFIELD` (tier5) and `CHGAMP` (tier5) — unlocked once the TL082
      JFET-input dual op-amp arrives.** LM358 (on hand) is bipolar-input
      (~20–100nA bias current) — wrong device class for a high-impedance
      electrometer/charge-amp front end; TL082's pA-range bias current is
      what these two nodes need.
- [ ] **`CHGAMP` (tier5) — also needs the 12mm piezo disc batch**, its
      charge-output transducer. Nothing currently on hand generates a
      charge signal.
- [ ] **`HVPULSE` (tier7) — unlocked once the IRLZ44N logic-level MOSFET
      arrives.** No switching MOSFET of any kind was previously on hand
      (the S8050/S8550 in inventory are small-signal BJTs). Same part
      also fills the general-purpose `ACTIVELIM` protection gap — see
      [general_purpose_circuit_dependency-arcticoder.md](general_purpose_circuit_dependency-arcticoder.md).

## Next parts to buy

- [ ] **Linear/analog Hall-effect sensor (e.g. 49E), 5–10pk** — the
      KY-003/A3144 module on order only covers digital switch-output; this
      is still needed for the `HALLAMP` op-amp amplifier circuit as
      originally scoped.
- [ ] **ADXL335 analog 3-axis accelerometer breakout (or equivalent, e.g.
      GY-521) — confirm/place the order.** This was identified as the
      `ACCELIF` gap and was last known to be sitting in a shopping cart,
      not a confirmed placed order — check whether it actually went
      through, and place it if not.
- [ ] **LVDT transducer** — the only tier5 node with zero hardware behind
      it (`LVDTAMP`). Pricier/more niche than the items above; lower
      priority but the last unaddressed tier5 sensor.

## Backlog — not yet designed or sourced at all

- [ ] **Tier 5 amplifier circuits** — once the parts above arrive, none of
      `HALLAMP`, `EPFIELD`, `LVDTAMP`, `ACCELIF`, `CHGAMP` have a folder,
      netlist, or breadboard guide yet. All five are net-new builds.
- [ ] **Tier 7 (RF power measurement, mixer, sweep generator)** —
      `RFPWR`, `MIXER`, `SWEEP` are completely unaddressed; no parts
      identified yet, let alone sourced. Lowest priority of the three
      tiers — nothing currently depends on this work starting.
- [ ] **Tier 8 (energy & complex measurement)** — `CALORIF`, `PWRFACT`,
      `ENGINT`, `NOISEFIG` are completely unaddressed; no parts identified
      yet. Same low-priority status as tier 7.
