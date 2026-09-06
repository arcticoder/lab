# TODO: Spacetime-Research Circuit Build-Out — Active Queue (for arcticoder)

> Blocked items (waiting on a shipment) are in
> [spacetime_circuits_dependency-arcticoder-BLOCKED.md](spacetime_circuits_dependency-arcticoder-BLOCKED.md).
> Long-term/undesigned backlog is in
> [spacetime_circuits_dependency-arcticoder-backlog.md](spacetime_circuits_dependency-arcticoder-backlog.md).
>
> This tracks tiers 5/7/8 in
> [spacetime_circuits_dependency.md](spacetime_circuits_dependency.md).
> Companion track:
> [general_purpose_circuit_dependency-arcticoder.md](general_purpose_circuit_dependency-arcticoder.md).
>
> Human-facing checklist — a future LLM chat's own working notes on this
> repo belong in `docs/kb/`, not here.

As of the last gap analysis, **tier5 has zero buildable nodes** — every
sensor-interface item is either unsourced or still in transit (see the
BLOCKED file). The only thing actually actionable right now in this track
is buying parts.

---

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
