# TODO: Spacetime-Research Circuit Build-Out — Blocked Items (for arcticoder)

> Active queue is in
> [spacetime_circuits_dependency-arcticoder.md](spacetime_circuits_dependency-arcticoder.md).
> Long-term/undesigned backlog is in
> [spacetime_circuits_dependency-arcticoder-backlog.md](spacetime_circuits_dependency-arcticoder-backlog.md).

## Still Blocked

- [ ] **`HALLAMP` (tier5) — partially unlocked once KY-003/A3144 arrives,
      but not fully.**
      Blocked on: KY-003/A3144 module, ordered 2026-09-03, not yet
      received — and even once received, it's digital switch-output (a
      presence/proximity read), not the linear-analog Hall element the
      original `HALLAMP` op-amp-amplifier design needs. A genuinely
      linear part (e.g. a 49E, see the active queue) is still needed for
      the amplifier circuit itself.

- [ ] **`EPFIELD` (tier5).**
      Blocked on: TL082 JFET-input dual op-amp, ordered 2026-09-03, not
      yet received. LM358 (on hand) is bipolar-input (~20–100nA bias
      current) — wrong device class for a high-impedance electrometer
      front end.

- [ ] **`CHGAMP` (tier5).**
      Blocked on: TL082 (same order as above) *and* the 12mm piezo disc
      batch, both ordered 2026-09-03, not yet received. Nothing currently
      on hand generates a charge signal for this node to condition.

- [ ] **`HVPULSE` (tier7).**
      Blocked on: IRLZ44N logic-level MOSFET, ordered 2026-09-03, not yet
      received. No switching MOSFET of any kind was previously on hand
      (the S8050/S8550 in inventory are small-signal BJTs). Same part
      also fills the general-purpose `ACTIVELIM` protection gap — see
      [general_purpose_circuit_dependency-arcticoder-BLOCKED.md](general_purpose_circuit_dependency-arcticoder-BLOCKED.md).

## Unblocked (resolved)

None yet.
