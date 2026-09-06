# TODO: General-Purpose Circuit Build-Out — Blocked Items (for arcticoder)

> Active queue is in
> [general_purpose_circuit_dependency-arcticoder.md](general_purpose_circuit_dependency-arcticoder.md).
> Long-term/undesigned backlog is in
> [general_purpose_circuit_dependency-arcticoder-backlog.md](general_purpose_circuit_dependency-arcticoder-backlog.md).

## Still Blocked

- [ ] **`CAPBRIDGE` (tier3, capacitance bridge).**
      Blocked on: multilayer ceramic capacitor assortment (50V, 10 values)
      and aluminum electrolytic capacitor kit (16V/25V/50V, 12 values),
      both ordered 2026-08-30, not yet received.

- [ ] **`INDBRIDGE` (tier3, inductance bridge).**
      Blocked on: color-ring inductor assortment (0307 1/4W, 12 values),
      ordered 2026-08-30, not yet received.

- [ ] **`ACTIVELIM` (protection, required by `psu_medhigh`/`psu_high`) —
      also feeds spacetime tier7 `HVPULSE`.**
      Blocked on: IRLZ44N logic-level MOSFET, ordered 2026-09-03, not yet
      received. No switching MOSFET of any kind was previously on hand.

- [ ] **`THERM` (safety monitoring) replacement sensor.**
      Blocked on: MF52AT 10kΩ NTC thermistor batch, ordered 2026-09-03,
      not yet received. The existing thermistor in inventory is flagged
      "suspect faulty," so this node currently has no trustworthy sensor
      behind it.

- [ ] **`PHASED` (tier4) → feeds `LOCKIN` (tier6).**
      Blocked on: SN74HC86N quad XOR gate, ordered 2026-09-03, not yet
      received. No logic gate IC suited to phase detection was previously
      on hand (only a 74HC595 shift register).

## Unblocked (resolved)

- [x] **`psu_low_v2` AA-holder lead-termination blocker** — resolved
      2026-09-03 when the 18-in-1 wire stripper/crimper was received.
      Physical build moved to the active queue.
